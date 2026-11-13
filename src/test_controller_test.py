import time

from core.test_controller import TestController
from validators.nv9_validator import NV9Validator


validator = NV9Validator()
controller = TestController(validator)

try:
    print("Initialising validator...")

    validator_info = controller.initialise_validator()

    print("\nValidator information:")
    print(validator_info)

    job_id = input("\nEnter Job ID: ").strip()
    test_id = input("Enter Test ID: ").strip()
    operator = input("Enter Operator Name: ").strip()

    print("\nStarting test...")

    session = controller.start_test(
        job_id=job_id,
        test_id=test_id,
        operator=operator,
    )

    print("\nTest session:")
    print(session)

    print("\nPolling started.")
    print("Insert a banknote now.")
    print("Press Ctrl+C to stop.\n")

    while controller.is_running():
        result = controller.poll_once()

        print("POLL:", result["raw_hex"])

        for event in result["events"]:
            print(
                event["event_type"],
                "Channel:",
                event["channel"],
                "Value:",
                event["value"],
                "Currency:",
                event["currency"],
            )

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nPolling stopped by user.")

finally:
    controller.stop_test()