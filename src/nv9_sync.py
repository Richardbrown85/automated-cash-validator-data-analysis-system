import serial
import time

PORT = "COM6"
BAUD_RATE = 9600

SYNC_PACKET = bytes.fromhex("7F 80 01 11 65 82")
EXPECTED_RESPONSE = "7F 80 01 F0 23 80"

try:
    nv9 = serial.Serial(
        port=PORT,
        baudrate=BAUD_RATE,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        timeout=1
    )

    print(f"Connected to {PORT}")

    nv9.reset_input_buffer()
    nv9.reset_output_buffer()

    print("Sending SSP SYNC command...")

    nv9.write(SYNC_PACKET)

    time.sleep(0.2)

    response = nv9.read_all()

    hex_response = response.hex(" ").upper()

    print("Raw response:", response)
    print("Hex response:", hex_response)

    if hex_response == EXPECTED_RESPONSE:
        print("SUCCESS: NV9 replied OK to SSP SYNC.")
    else:
        print("Response received, but it was not the expected SYNC reply.")

    nv9.close()
    print("Connection closed.")

except serial.SerialException as error:
    print("Serial error:")
    print(error)