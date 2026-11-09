import serial
import time

PORT = "COM6"
BAUD_RATE = 9600

ENABLE_COMMAND = 0x0A
POLL_COMMAND = 0x07


def ssp_crc(data):
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


def build_packet(seq_address, command):
    body = bytes([
        seq_address,
        0x01,
        command
    ])

    crc = ssp_crc(body)

    crc_low = crc & 0xFF
    crc_high = (crc >> 8) & 0xFF

    return bytes([0x7F]) + body + bytes([
        crc_low,
        crc_high
    ])


SYNC_PACKET = bytes.fromhex(
    "7F 80 01 11 65 82"
)


try:
    with serial.Serial(
        port=PORT,
        baudrate=BAUD_RATE,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        timeout=1
    ) as nv9:

        nv9.reset_input_buffer()
        nv9.reset_output_buffer()

        print("Connected to NV9 on", PORT)

        # -------------------------
        # SYNC
        # -------------------------

        print("\nSending SYNC...")

        nv9.write(SYNC_PACKET)
        time.sleep(0.2)

        sync_response = nv9.read_all()

        print(
            "SYNC response:",
            sync_response.hex(" ").upper()
        )

        # After SYNC, next sequence bit is 0
        sequence = 0x00

        # -------------------------
        # ENABLE
        # -------------------------

        print("\nEnabling NV9...")

        enable_packet = build_packet(
            sequence,
            ENABLE_COMMAND
        )

        print(
            "ENABLE packet:",
            enable_packet.hex(" ").upper()
        )

        nv9.write(enable_packet)
        time.sleep(0.2)

        enable_response = nv9.read_all()

        print(
            "ENABLE response:",
            enable_response.hex(" ").upper()
        )

        # Toggle sequence after ENABLE
        sequence = 0x80

        # -------------------------
        # POLLING
        # -------------------------

        print("\nStarting NV9 polling...")
        print("Insert a banknote into the validator.")
        print("Press Ctrl+C to stop.\n")

        while True:

            poll_packet = build_packet(
                sequence,
                POLL_COMMAND
            )

            nv9.write(poll_packet)
            time.sleep(0.15)

            response = nv9.read_all()

            if response:
                print(
                    "POLL:",
                    response.hex(" ").upper()
                )

            # Toggle sequence bit
            if sequence == 0x00:
                sequence = 0x80
            else:
                sequence = 0x00

            time.sleep(0.15)


except KeyboardInterrupt:
    print("\nPolling stopped.")


except serial.SerialException as error:
    print("Serial error:")
    print(error)