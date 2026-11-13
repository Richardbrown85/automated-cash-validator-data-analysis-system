def parse_setup_response(response):
    """
    Decode an SSP Setup Request response from an NV9.

    This parser currently supports the legacy Setup Request format
    used by our NV9 running SSP protocol version 4.
    """

    if not response:
        raise ValueError("Setup response is empty.")

    if len(response) < 10:
        raise ValueError("Setup response is too short.")

    # SSP response:
    # 7F | SEQ/ADDR | LENGTH | F0 | SETUP DATA... | CRC LOW | CRC HIGH

    if response[0] != 0x7F:
        raise ValueError("Invalid SSP start byte.")

    if response[3] != 0xF0:
        raise ValueError(
            f"Setup Request failed. Response code: {response[3]:02X}"
        )

    # Remove SSP header/status and CRC
    setup_data = response[4:-2]

    if len(setup_data) < 12:
        raise ValueError("Setup payload is too short.")

    device_type = setup_data[0]

    firmware = setup_data[1:5].decode(
        "ascii",
        errors="replace"
    )

    currency = setup_data[5:8].decode(
        "ascii",
        errors="replace"
    )

    value_multiplier = int.from_bytes(
        setup_data[8:11],
        byteorder="big"
    )

    number_of_channels = setup_data[11]

    channel_values_start = 12
    channel_values_end = (
        channel_values_start + number_of_channels
    )

    if len(setup_data) < channel_values_end:
        raise ValueError(
            "Setup payload does not contain all channel values."
        )

    channel_values = setup_data[
        channel_values_start:channel_values_end
    ]

    security_start = channel_values_end
    security_end = (
        security_start + number_of_channels
    )

    if len(setup_data) < security_end + 4:
        raise ValueError(
            "Setup payload is incomplete."
        )

    security_levels = setup_data[
        security_start:security_end
    ]

    real_value_multiplier = int.from_bytes(
        setup_data[security_end:security_end + 3],
        byteorder="big"
    )

    protocol_version = setup_data[
        security_end + 3
    ]

    channel_map = {}

    for index, channel_value in enumerate(
        channel_values,
        start=1
    ):
        channel_map[index] = {
            "value": channel_value * value_multiplier,
            "currency": currency,
        }

    return {
        "device_type": device_type,
        "firmware": firmware,
        "currency": currency,
        "value_multiplier": value_multiplier,
        "number_of_channels": number_of_channels,
        "security_levels": list(security_levels),
        "real_value_multiplier": real_value_multiplier,
        "protocol_version": protocol_version,
        "channel_map": channel_map,
    }