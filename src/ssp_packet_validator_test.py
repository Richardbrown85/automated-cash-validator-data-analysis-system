from protocols.ssp_packet_validator import validate_ssp_packet


def expect_failure(name, packet, expected_sequence=0x80):
    try:
        validate_ssp_packet(
            packet,
            expected_sequence=expected_sequence
        )
    except ValueError as error:
        print(f"PASS - {name}: {error}")
        return

    raise AssertionError(
        f"FAIL - {name}: invalid packet was accepted."
    )


# Real NV9 NOTE_READ response
valid_packet = bytes.fromhex(
    "7F 80 03 F0 EF 02 C0 4A"
)

# Test 1: Valid packet
payload = validate_ssp_packet(
    valid_packet,
    expected_sequence=0x80
)

assert payload == bytes.fromhex("F0 EF 02")
print("PASS - Valid SSP packet")

# Test 2: Corrupted CRC
corrupted = bytearray(valid_packet)
corrupted[-1] ^= 0x01

expect_failure(
    "Corrupted CRC",
    bytes(corrupted)
)

# Test 3: Incomplete packet
expect_failure(
    "Incomplete packet",
    valid_packet[:-1]
)

# Test 4: Incorrect sequence
expect_failure(
    "Incorrect sequence",
    valid_packet,
    expected_sequence=0x00
)

# Test 5: Invalid start byte
expect_failure(
    "Invalid start byte",
    b"\x00" + valid_packet[1:]
)

print("\nAll SSP validation tests passed!")