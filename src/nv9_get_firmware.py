import serial
import time

PORT = "COM6"
BAUD_RATE = 9600


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


# SSP SYNC command
SYNC_PACKET = bytes.fromhex(
    "7F 80 01 11 65 82"
)

# After SYNC, the next sequence bit is 0
GET_FIRMWARE_PACKET = build_packet(
    0x00,
    0x20
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

        # -------------------------
        # GET FIRMWARE VERSION
        # -------------------------

        print("\nSending GET FIRMWARE VERSION...")

        print(
            "Packet:",
            GET_FIRMWARE_PACKET.hex(" ").upper()
        )

        nv9.write(GET_FIRMWARE_PACKET)
        time.sleep(0.2)

        response = nv9.read_all()

        print(
            "Hex response:",
            response.hex(" ").upper()
        )

        if len(response) >= 6 and response[3] == 0xF0:

            # Remove:
            # 7F = start
            # seq/address
            # length
            # F0 = OK
            # final 2 bytes = CRC

            firmware_bytes = response[4:-2]

            firmware = firmware_bytes.decode(
                "ascii",
                errors="replace"
            )

            print("\nSUCCESS")
            print("Firmware version:", firmware)

        else:
            print(
                "\nCould not decode firmware version."
            )

except serial.SerialException as error:

    print("Serial error:")
    print(error)