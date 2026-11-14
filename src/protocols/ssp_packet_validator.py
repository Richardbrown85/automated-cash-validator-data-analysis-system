def calculate_ssp_crc(data):
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


def validate_ssp_packet(packet, expected_sequence=None):
    if len(packet) < 6:
        raise ValueError("SSP packet is too short.")

    if packet[0] != 0x7F:
        raise ValueError("Invalid SSP start byte.")

    declared_length = packet[2]
    expected_length = declared_length + 5

    if len(packet) != expected_length:
        raise ValueError(
            "SSP packet length does not match."
        )

    if expected_sequence is not None:
        if packet[1] != expected_sequence:
            raise ValueError(
                "SSP sequence does not match."
            )

    calculated_crc = calculate_ssp_crc(packet[1:-2])

    received_crc = int.from_bytes(
        packet[-2:],
        byteorder="little"
    )

    if calculated_crc != received_crc:
        raise ValueError("SSP CRC validation failed.")

    return packet[3:-2]