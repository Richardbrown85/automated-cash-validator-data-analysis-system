from protocols.ssp_event_decoder import decode_poll_response


test_responses = [
    "7F 80 02 F0 F1 1A 22",
    "7F 00 03 F0 EF 02 C3 F6",
    "7F 80 02 F0 CC 97 A2",
    "7F 00 04 F0 EE 02 CC E0 C2",
    "7F 80 03 F0 CC EB B6 82",
]


for hex_response in test_responses:
    response = bytes.fromhex(hex_response)

    print("\nRAW:", hex_response)

    events = decode_poll_response(response)

    for event in events:
        print(event)