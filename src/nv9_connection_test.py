import serial

PORT = "COM6"
BAUD_RATE = 9600

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
    print("Port open:", nv9.is_open)

    nv9.close()
    print("Connection closed successfully.")

except serial.SerialException as error:
    print("Serial error:")
    print(error)