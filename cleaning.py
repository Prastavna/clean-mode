import platform
import time
import subprocess
import sys

def disable_keyboard():
    os_name = platform.system()

    if os_name == 'Windows':
        # Disable keyboard on Windows
        command = 'powershell -Command "$keyboard = Get-WmiObject Win32_Keyboard; $keyboard.SetDeviceState($keyboard.DeviceID, 1)"'
        subprocess.run(command, shell=True)

    elif os_name == 'Darwin':
        # Disable keyboard on macOS
        command = "sudo kextunload /System/Library/Extensions/AppleHIDKeyboard.kext"
        subprocess.run(command, shell=True, input=b"<password>\n", timeout=10, text=True)

    elif os_name == 'Linux':
        # Disable keyboard on Linux
        command = 'xinput list'
        output = subprocess.check_output(command, shell=True, text=True)

        keyboard_id = None

        for line in output.split("\n"):
            if "AT Translated Set 2 keyboard" in line:
                keyboard_id = line.split("id=")[1].split("\t")[0]
                break

        if keyboard_id:
            disable_command = "xinput float {}".format(keyboard_id)
            subprocess.run(disable_command, shell=True)
            print("Keyboard disabled for 10 seconds...")
            time.sleep(10)
            enable_command = "xinput reattach {} 3".format(keyboard_id)  # Assuming 3 is the master pointer ID
            subprocess.run(enable_command, shell=True)
            print("Keyboard re-enabled.")

        else:
            print("Keyboard ID not found.")

    else:
        print("Unsupported operating system.")
        sys.exit(1)

disable_keyboard()
