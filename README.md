# Basic Local Machine Key Logger

A Python-based keyboard monitoring project built to explore keyboard event handling, GUI development and basic input analysis.

The project started as a simple `pynput` key logger and has been developed into a desktop application with a graphical interface.

## Features

- Keyboard monitoring using `pynput`
- Desktop GUI built with Tkinter
- Start, stop and clear controls
- Live keystroke display
- Keystroke counter
- Suspected login detection
- Separate Username and Password display
- Basic credential-pattern detection
- Automated tests for the detection logic
- Windows application icon

## Requirements

- Python 3
- `pynput`

Install the project dependencies with:

```powershell
pip install -r requirements.txt
```

## Usage

Launch the graphical application with:

```powershell
python security_gui.py
```

The application provides controls for starting and stopping keyboard monitoring and clearing the current session.

The original command-line implementation is also retained in `Keylogger.py`.

## Project Structure

```text
Basic-Local-Machine-Key-Logger/
├── assets/
│   └── keylogger.ico
├── tests/
│   └── test_credential_detection.py
├── credential_detection.py
├── Keylogger.py
├── security_gui.py
├── requirements.txt
├── README.md
├── SECURITY.md
├── LICENSE
└── .gitignore
```

## Testing

Run the automated tests with:

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

## Development

This is a personal cybersecurity project for learning and experimentation. The project is being developed incrementally to explore keyboard event handling, desktop interfaces, input processing and security-related detection techniques.

## Responsible Use

This project is intended for personal learning, experimentation and use on systems that you own or have permission to monitor.

Please ensure that you have appropriate authorisation before using the software to capture or inspect keyboard input.

## Licence

MIT Licence.
