import tkinter as tk

from tkinter import ttk


class KeyloggerGUI:
    """Desktop interface for local keyboard monitoring."""

    def __init__(self, root):
        """Initialise the application window and interface."""
        self.root = root

        self.root.title("Local Key Logger")
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

        header.pack(
            fill=tk.X
        )

        title = ttk.Label(
            header,
            text="Local Key Logger",
            font=("Segoe UI", 18, "bold")
        )

        title.pack(
            side=tk.LEFT
        )

        self.clear_button = ttk.Button(
            header,
            text="Clear Capture",
            command=self.clear_capture
        )

        self.clear_button.pack(
            side=tk.RIGHT
        )

        self.stop_button = ttk.Button(
            header,
            text="Stop Logging",
            command=self.stop_logging,
            state=tk.DISABLED
        )

        self.stop_button.pack(
            side=tk.RIGHT,
            padx=5
        )

        self.start_button = ttk.Button(
            header,
            text="Start Logging",
            command=self.start_logging
        )

        self.start_button.pack(
            side=tk.RIGHT
        )

        status_frame = ttk.Frame(
            self.root,
            padding=(10, 0, 10, 10)
        )

        status_frame.pack(
            fill=tk.X
        )

        self.status_label = ttk.Label(
            status_frame,
            text="Status: Stopped"
        )

        self.status_label.pack(
            side=tk.LEFT
        )

        self.key_count_label = ttk.Label(
            status_frame,
            text="Keystrokes: 0"
        )

        self.key_count_label.pack(
            side=tk.LEFT,
            padx=25
        )

        self.login_count_label = ttk.Label(
            status_frame,
            text="Suspected logins: 0"
        )

        self.login_count_label.pack(
            side=tk.LEFT
        )

        self.notebook = ttk.Notebook(
            self.root
        )

        self.notebook.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        self.build_keystroke_tab()
        self.build_login_tab()

    def build_keystroke_tab(self):
        """Create the keystroke log table."""
        frame = ttk.Frame(
            self.notebook,
            padding=5
        )

        self.notebook.add(
            frame,
            text="Keystroke Log"
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
            row=0,
            column=0,
            sticky="nsew"
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        frame.rowconfigure(
            0,
            weight=1
        )

        frame.columnconfigure(
            0,
            weight=1
        )

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

        columns = (
            "username",
            "password"
        )

        self.login_tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings"
        )

        self.login_tree.heading(
            "username",
            text="Username"
        )

        self.login_tree.heading(
            "password",
            text="Password"
        )

        self.login_tree.column(
            "username",
            width=350,
            anchor=tk.W
        )

        self.login_tree.column(
            "password",
            width=350,
            anchor=tk.W
        )

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

        frame.rowconfigure(
            0,
            weight=1
        )

        frame.columnconfigure(
            0,
            weight=1
        )

    def start_logging(self):
        """Update the interface to indicate that logging is active."""
        self.status_label.config(
            text="Status: Logging"
        )

        self.start_button.config(
            state=tk.DISABLED
        )

        self.stop_button.config(
            state=tk.NORMAL
        )

    def stop_logging(self):
        """Update the interface to indicate that logging has stopped."""
        self.status_label.config(
            text="Status: Stopped"
        )

        self.start_button.config(
            state=tk.NORMAL
        )

        self.stop_button.config(
            state=tk.DISABLED
        )

    def clear_capture(self):
        """Clear captured data from the interface."""
        self.keystroke_tree.delete(
            *self.keystroke_tree.get_children()
        )

        self.login_tree.delete(
            *self.login_tree.get_children()
        )

        self.key_count_label.config(
            text="Keystrokes: 0"
        )

        self.login_count_label.config(
            text="Suspected logins: 0"
        )

        self.stop_logging()

    def close_application(self):
        """Close the application."""
        self.root.destroy()


def main():
    """Launch the desktop application."""
    root = tk.Tk()

    KeyloggerGUI(
        root
    )

    root.mainloop()


if __name__ == "__main__":
    main()
