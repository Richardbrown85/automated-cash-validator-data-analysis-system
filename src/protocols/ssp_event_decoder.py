EVENT_CODES = {
    0xF1: "SLAVE_RESET",
    0xEF: "NOTE_READ",
    0xEE: "NOTE_CREDIT",
    0xED: "REJECTING",
    0xEC: "REJECTED",
    0xCC: "STACKING",
    0xEB: "STACKED",
    0xE9: "UNSAFE_JAM",
    0xE8: "DISABLED",
    0xE7: "STACKER_FULL",
    0xE6: "FRAUD_ATTEMPT",
    0xE2: "NOTE_CLEARED_INTO_CASHBOX",
    0xE1: "NOTE_CLEARED_FROM_FRONT",
    0xB5: "CHANNEL_DISABLE",
    0xB6: "INITIALISING",
}


EVENTS_WITH_CHANNEL = {
    0xEF,  # NOTE_READ
    0xEE,  # NOTE_CREDIT
}


def decode_poll_response(response):
    """
    Decode SSP poll-event bytes into structured event dictionaries.

    Raw SSP data is always retained so we do not lose the original
    validator response.
    """

    if not response or len(response) < 6:
        return []

    # Byte 3 should be the SSP OK response (F0).
    if response[3] != 0xF0:
        return []

    # Remove SSP header/status and final two CRC bytes.
    event_data = response[4:-2]

    events = []
    index = 0

    while index < len(event_data):
        event_code = event_data[index]

        event = {
            "event_code": f"{event_code:02X}",
            "event_type": EVENT_CODES.get(
                event_code,
                "UNKNOWN_EVENT"
            ),
            "channel": None,
            "raw_hex": response.hex(" ").upper(),
        }

        if event_code in EVENTS_WITH_CHANNEL:
            if index + 1 < len(event_data):
                event["channel"] = event_data[index + 1]
                index += 2
            else:
                index += 1
        else:
            index += 1

        events.append(event)

    return events