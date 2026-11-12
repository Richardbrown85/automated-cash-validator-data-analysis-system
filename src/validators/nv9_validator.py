import serial
import time

from .base_validator import BaseValidator
from config.settings import SERIAL_PORT, BAUD_RATE


class NV9Validator(BaseValidator):
    """
    Validator adapter for the NV9USB.

    This class contains the NV9-specific SSP communication
    while presenting the common BaseValidator interface
    to the rest of the application.
    """

    SYNC_PACKET = bytes.fromhex("7F 80 01 11 65 82")

    SET_INHIBITS_COMMAND = 0x02
    POLL_COMMAND = 0x07
    DISABLE_COMMAND = 0x09
    ENABLE_COMMAND = 0x0A
    GET_SERIAL_COMMAND = 0x0C
    GET_FIRMWARE_COMMAND = 0x20
    GET_DATASET_COMMAND = 0x21

    def __init__(self, port=SERIAL_PORT, baud_rate=BAUD_RATE):
        self.port = port
        self.baud_rate = baud_rate

        self.serial_connection = None
        self.connected = False
        self.enabled = False

        # SSP sequence bit.
        # SYNC resets the next expected sequence to 0.
        self.sequence = 0x00

    # --------------------------------------------------
    # SSP packet handling
    # --------------------------------------------------

    def _ssp_crc(self, data):
        crc = 0xFFFF
        polynomial = 0x8005

        for byte in data:
            crc ^= byte << 8

            for _ in range(8):
                if crc & 0x8000:
                    crc = ((crc << 1) ^ polynomial) & 0xFFFF
                else:
                    crc = (crc << 1) & 0xFFFF

        return crc

    def _build_packet(self, command, data=b""):
        payload = bytes([command]) + data

        body = bytes([
            self.sequence,
            len(payload)
        ]) + payload

        crc = self._ssp_crc(body)

        crc_low = crc & 0xFF
        crc_high = (crc >> 8) & 0xFF

        return (
            bytes([0x7F])
            + body
            + bytes([crc_low, crc_high])
        )

    def _toggle_sequence(self):
        if self.sequence == 0x00:
            self.sequence = 0x80
        else:
            self.sequence = 0x00

    def _send_command(self, command, data=b""):
        if not self.connected:
            raise RuntimeError("Validator is not connected.")

        packet = self._build_packet(
            command,
            data
        )

        self.serial_connection.write(packet)

        time.sleep(0.2)

        response = self.serial_connection.read_all()

        self._toggle_sequence()

        return response

    def _response_ok(self, response):
        return (
            len(response) >= 6
            and response[3] == 0xF0
        )

    # --------------------------------------------------
    # Connection
    # --------------------------------------------------

    def connect(self):
        if self.connected:
            return

        self.serial_connection = serial.Serial(
            port=self.port,
            baudrate=self.baud_rate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_TWO,
            timeout=1
        )

        self.serial_connection.reset_input_buffer()
        self.serial_connection.reset_output_buffer()

        self.connected = True

        # SYNC should be the first SSP command.
        self.serial_connection.write(
            self.SYNC_PACKET
        )

        time.sleep(0.2)

        response = self.serial_connection.read_all()

        if not self._response_ok(response):
            self.disconnect()

            raise RuntimeError(
                "NV9 did not respond correctly to SSP SYNC."
            )

        # After SYNC, the next sequence bit should be 0.
        self.sequence = 0x00

        print(
            f"NV9 connected on {self.port}"
        )

    def disconnect(self):
        if self.serial_connection:
            if self.serial_connection.is_open:
                self.serial_connection.close()

        self.serial_connection = None
        self.connected = False
        self.enabled = False

        print("NV9 disconnected.")

    # --------------------------------------------------
    # Device information
    # --------------------------------------------------

    def get_serial_number(self):
        response = self._send_command(
            self.GET_SERIAL_COMMAND
        )

        if not self._response_ok(response):
            raise RuntimeError(
                "Could not read NV9 serial number."
            )

        serial_bytes = response[4:8]

        return int.from_bytes(
            serial_bytes,
            byteorder="big"
        )

    def get_firmware_version(self):
        response = self._send_command(
            self.GET_FIRMWARE_COMMAND
        )

        if not self._response_ok(response):
            raise RuntimeError(
                "Could not read NV9 firmware version."
            )

        firmware_bytes = response[4:-2]

        return firmware_bytes.decode(
            "ascii",
            errors="replace"
        )

    def get_dataset_version(self):
        response = self._send_command(
            self.GET_DATASET_COMMAND
        )

        if not self._response_ok(response):
            raise RuntimeError(
                "Could not read NV9 dataset version."
            )

        dataset_bytes = response[4:-2]

        return dataset_bytes.decode(
            "ascii",
            errors="replace"
        )

    # --------------------------------------------------
    # Validator control
    # --------------------------------------------------

    def enable(self):
        # Enable channels 1-16.
        inhibit_response = self._send_command(
            self.SET_INHIBITS_COMMAND,
            bytes([0xFF, 0xFF])
        )

        if not self._response_ok(inhibit_response):
            raise RuntimeError(
                "Could not enable NV9 note channels."
            )

        enable_response = self._send_command(
            self.ENABLE_COMMAND
        )

        if not self._response_ok(enable_response):
            raise RuntimeError(
                "Could not enable NV9."
            )

        self.enabled = True

        print("NV9 enabled.")

    def disable(self):
        response = self._send_command(
            self.DISABLE_COMMAND
        )

        if not self._response_ok(response):
            raise RuntimeError(
                "Could not disable NV9."
            )

        self.enabled = False

        print("NV9 disabled.")

    # --------------------------------------------------
    # Polling
    # --------------------------------------------------

    def poll(self):
    from protocols.ssp_event_decoder import decode_poll_response

    response = self._send_command(
        self.POLL_COMMAND
    )

    if not response:
        return None

    return {
        "raw": response,
        "raw_hex": response.hex(" ").upper(),
        "events": decode_poll_response(response),
    }