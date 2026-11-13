from protocols.ssp_setup_parser import parse_setup_response


setup_hex = (
    "7F 80 19 F0 "
    "00 "
    "30 31 32 30 "
    "47 42 50 "
    "00 00 01 "
    "04 "
    "05 0A 14 32 "
    "02 02 02 02 "
    "00 00 64 "
    "04 "
    "7A DE"
)

response = bytes.fromhex(setup_hex)

setup = parse_setup_response(response)

print("Device type:", setup["device_type"])
print("Firmware:", setup["firmware"])
print("Currency:", setup["currency"])
print("Value multiplier:", setup["value_multiplier"])
print("Channels:", setup["number_of_channels"])
print("Protocol version:", setup["protocol_version"])

print("\nChannel map:")

for channel, details in setup["channel_map"].items():
    print(
        f"Channel {channel}: "
        f"{details['value']} "
        f"{details['currency']}"
    )