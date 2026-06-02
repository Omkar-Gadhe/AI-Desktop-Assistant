# action.py
import subprocess

# Your global app mapping stays exactly the same
APPS = {
    "open firefox": "firefox",
        "open browser": "firefox",
        "open files": "nautilus",
        "open file manager": "nautilus",
        "open terminal": "gnome-terminal",
        "open calculator": "gnome-calculator",
        "open vscode": "code",
        "open code": "code"
}

def find_app(text):
    text = text.lower()
    for name in APPS:
        if name in text:
            return name
    return None

def act_brain(user_input):
    app_name = find_app(user_input)
    if not app_name:
        print("Unknown app, please try again.")
        return

    try:
        subprocess.Popen([APPS[app_name]])
        print(f"Opening {app_name.title()}...")
    except FileNotFoundError:
        print("App is not installed or cannot be started.")