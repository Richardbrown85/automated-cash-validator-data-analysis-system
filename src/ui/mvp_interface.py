import queue
import threading
import tkinter as tk
from tkinter import ttk, messagebox

from core.test_controller import TestController
from validators.nv9_validator import NV9Validator


class MVPInterface:
    def __init__(self, root):
        self.root = root
        self.root.title(
            "Automated Cash Validator Test System"
        )
        self.root.geometry("900x650")

        self.validator = NV9Validator()
        self.controller = TestController(
            self.validator
        )

        self.message_queue = queue.Queue()
        self.stop_event = threading.Event()

        self._build_interface()

        self.root.after(
            100,
            self._process_messages
        )

    # --------------------------------------------------
    # Interface
    # --------------------------------------------------

    def _build_interface(self):
        main_frame = ttk.Frame(
            self.root,
            padding=20
        )
        main_frame.pack(
            fill="both",
            expand=True
        )

        title = ttk.Label(
            main_frame,
            text="Cash Validator Test System",
            font=("Segoe UI", 18, "bold"),
        )
        title.pack(
            anchor="w",
            pady=(0, 20)
        )

        # --------------------------------------------------
        # Test information
        # --------------------------------------------------

        test_frame = ttk.LabelFrame(
            main_frame,
            text="Test Information",
            padding=15
        )
        test_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        ttk.Label(
            test_frame,
            text="Job ID:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        self.job_entry = ttk.Entry(
            test_frame,
            width=25
        )
        self.job_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Label(
            test_frame,
            text="Test ID:"
        ).grid(
            row=0,
            column=2,
            sticky="w",
            padx=5,
            pady=5
        )

        self.test_entry = ttk.Entry(
            test_frame,
            width=25
        )
        self.test_entry.grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )

        ttk.Label(
            test_frame,
            text="Operator:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        self.operator_entry = ttk.Entry(
            test_frame,
            width=25
        )
        self.operator_entry.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        # --------------------------------------------------
        # Validator information
        # --------------------------------------------------

        validator_frame = ttk.LabelFrame(
            main_frame,
            text="Validator Information",
            padding=15
        )
        validator_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        self.validator_info = tk.StringVar(
            value="Validator not initialised."
        )

        ttk.Label(
            validator_frame,
            textvariable=self.validator_info,
            justify="left"
        ).pack(
            anchor="w"
        )

        button_frame = ttk.Frame(
            validator_frame
        )
        button_frame.pack(
            fill="x",
            pady=(15, 0)
        )

        self.detect_button = ttk.Button(
            button_frame,
            text="Detect Validator",
            command=self.detect_validator
        )
        self.detect_button.pack(
            side="left",
            padx=(0, 10)
        )

        self.start_button = ttk.Button(
            button_frame,
            text="Start Test",
            command=self.start_test,
            state="disabled"
        )
        self.start_button.pack(
            side="left",
            padx=(0, 10)
        )

        self.stop_button = ttk.Button(
            button_frame,
            text="Stop Test",
            command=self.stop_test,
            state="disabled"
        )
        self.stop_button.pack(
            side="left"
        )

        # --------------------------------------------------
        # Status
        # --------------------------------------------------

        self.status = tk.StringVar(
            value="Ready"
        )

        status_frame = ttk.Frame(
            main_frame
        )
        status_frame.pack(
            fill="x",
            pady=(0, 10)
        )

        ttk.Label(
            status_frame,
            text="Status:",
            font=("Segoe UI", 10, "bold")
        ).pack(
            side="left"
        )

        ttk.Label(
            status_frame,
            textvariable=self.status
        ).pack(
            side="left",
            padx=(5, 0)
        )

        # --------------------------------------------------
        # Live event stream
        # --------------------------------------------------

        event_frame = ttk.LabelFrame(
            main_frame,
            text="Live Event Stream",
            padding=10
        )
        event_frame.pack(
            fill="both",
            expand=True
        )

        self.event_text = tk.Text(
            event_frame,
            height=15,
            wrap="none",
            state="disabled"
        )
        self.event_text.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            event_frame,
            orient="vertical",
            command=self.event_text.yview
        )
        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.event_text.configure(
            yscrollcommand=scrollbar.set
        )

    # --------------------------------------------------
    # Validator detection
    # --------------------------------------------------

    def detect_validator(self):
        self.detect_button.config(
            state="disabled"
        )

        self.status.set(
            "Detecting validator..."
        )

        thread = threading.Thread(
            target=self._detect_validator_worker,
            daemon=True
        )
        thread.start()

    def _detect_validator_worker(self):
        try:
            info = (
                self.controller.initialise_validator()
            )

            self.message_queue.put(
                ("validator_info", info)
            )

        except Exception as error:
            self.message_queue.put(
                ("error", str(error))
            )

    # --------------------------------------------------
    # Test control
    # --------------------------------------------------

    def start_test(self):
        job_id = self.job_entry.get().strip()
        test_id = self.test_entry.get().strip()
        operator = (
            self.operator_entry.get().strip()
        )

        if not job_id:
            messagebox.showwarning(
                "Missing Job ID",
                "Enter a Job ID."
            )
            return

        if not test_id:
            messagebox.showwarning(
                "Missing Test ID",
                "Enter a Test ID."
            )
            return

        if not operator:
            messagebox.showwarning(
                "Missing Operator",
                "Enter the operator name."
            )
            return

        self.stop_event.clear()

        self.start_button.config(
            state="disabled"
        )

        self.detect_button.config(
            state="disabled"
        )

        self.stop_button.config(
            state="normal"
        )

        self.status.set(
            "Starting test..."
        )

        thread = threading.Thread(
            target=self._test_worker,
            args=(
                job_id,
                test_id,
                operator,
            ),
            daemon=True
        )
        thread.start()

    def _test_worker(
        self,
        job_id,
        test_id,
        operator,
    ):
        try:
            session = self.controller.start_test(
                job_id=job_id,
                test_id=test_id,
                operator=operator,
            )

            self.message_queue.put(
                ("test_started", session)
            )

            while not self.stop_event.is_set():
                result = (
                    self.controller.poll_once()
                )

                for event in result["events"]:
                    self.message_queue.put(
                        ("event", event)
                    )

        except Exception as error:
            self.message_queue.put(
                ("error", str(error))
            )

        finally:
            try:
                self.controller.stop_test()
            except Exception as error:
                self.message_queue.put(
                    ("error", str(error))
                )

            self.message_queue.put(
                ("test_stopped", None)
            )

    def stop_test(self):
        self.status.set(
            "Stopping test..."
        )

        self.stop_button.config(
            state="disabled"
        )

        self.stop_event.set()

    # --------------------------------------------------
    # UI message handling
    # --------------------------------------------------

    def _process_messages(self):
        try:
            while True:
                message_type, data = (
                    self.message_queue.get_nowait()
                )

                if message_type == "validator_info":
                    self._show_validator_info(
                        data
                    )

                elif message_type == "test_started":
                    self.status.set(
                        "Test running"
                    )

                    self._add_event_line(
                        "TEST STARTED"
                    )

                elif message_type == "event":
                    self._show_event(
                        data
                    )

                elif message_type == "test_stopped":
                    self.status.set(
                        "Test stopped"
                    )

                    self._add_event_line(
                        "TEST STOPPED"
                    )

                    self.start_button.config(
                        state="normal"
                    )

                    self.detect_button.config(
                        state="normal"
                    )

                    self.stop_button.config(
                        state="disabled"
                    )

                elif message_type == "error":
                    self.status.set(
                        "Error"
                    )

                    messagebox.showerror(
                        "Error",
                        data
                    )

                    self.start_button.config(
                        state="normal"
                    )

                    self.detect_button.config(
                        state="normal"
                    )

                    self.stop_button.config(
                        state="disabled"
                    )

        except queue.Empty:
            pass

        self.root.after(
            100,
            self._process_messages
        )

    def _show_validator_info(self, info):
        channel_lines = []

        for channel, details in (
            info["channel_map"].items()
        ):
            channel_lines.append(
                f"Channel {channel}: "
                f"{details['value']} "
                f"{details['currency']}"
            )

        channel_text = "\n".join(
            channel_lines
        )

        text = (
            f"Model: {info['model']}\n"
            f"Serial: {info['serial_number']}\n"
            f"Firmware: {info['firmware']}\n"
            f"Dataset: {info['dataset']}\n"
            f"Port: {info['port']}\n\n"
            f"Channel Map:\n"
            f"{channel_text}"
        )

        self.validator_info.set(text)

        self.status.set(
            "Validator ready"
        )

        self.start_button.config(
            state="normal"
        )

        self.detect_button.config(
            state="disabled"
        )

    def _show_event(self, event):
        event_type = event["event_type"]
        channel = event["channel"]
        value = event["value"]
        currency = event["currency"]

        if value is not None:
            line = (
                f"{event_type} | "
                f"Channel {channel} | "
                f"{value} {currency}"
            )
        else:
            line = (
                f"{event_type} | "
                f"Channel {channel}"
            )

        self._add_event_line(line)

    def _add_event_line(self, text):
        self.event_text.config(
            state="normal"
        )

        self.event_text.insert(
            "end",
            text + "\n"
        )

        self.event_text.see(
            "end"
        )

        self.event_text.config(
            state="disabled"
        )


def main():
    root = tk.Tk()

    MVPInterface(root)

    root.mainloop()


if __name__ == "__main__":
    main()