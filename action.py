 # action.py
import subprocess
from ass_log import logger

# The absolute source of truth for binaries
APPS = {
    "firefox": "firefox",
    "browser": "firefox",
    "files": "nautilus",
    "file manager": "nautilus",
    "terminal": "gnome-terminal",
    "calculator": "gnome-calculator",
    "vscode": "code",
    "vs code": "code",
    "code": "code"
}

def act_brain(app_name: str):
    """JOB: 100% Execution. 
    Expects a pre-validated app key from the registry and spawns the OS process.
    """
    # Guard clause in case something completely unregistered slips past the gate
    if app_name not in APPS:
        print("System Error: Attempted to launch an unregistered application.")
        logger.error(f"System Error: Attempted to launch an unregistered application")
        return

    try:
        subprocess.Popen([APPS[app_name]])
        print(f"Opening {app_name.title()}...")
        # ─── LOG A SUCCESSFUL ACTION ───
        logger.info(f"Successfully spawned system application: {app_name} (Binary: {APPS[app_name]})")
    except FileNotFoundError:
        print("App is not installed or cannot be started.")
        # ─── LOG A HARD HARDWARE/OS ERROR ───
        logger.error(f"Failed to execute binary for {app_name}. Path/Command '{APPS[app_name]}' not found on OS.")