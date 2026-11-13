from serial.tools import list_ports


def find_validator_port():
    """
    Find the most likely USB serial port used by the validator.

    Looks for common FTDI / USB Serial descriptions.
    """

    ports = list_ports.comports()

    matching_ports = []

    for port in ports:
        description = (port.description or "").lower()
        manufacturer = (port.manufacturer or "").lower()

        if (
            "usb serial" in description
            or "ftdi" in description
            or "ftdi" in manufacturer
        ):
            matching_ports.append(port.device)

    if len(matching_ports) == 1:
        return matching_ports[0]

    if len(matching_ports) == 0:
        raise RuntimeError(
            "No validator USB serial port found."
        )

    raise RuntimeError(
        "Multiple possible validator serial ports found: "
        + ", ".join(matching_ports)
    )