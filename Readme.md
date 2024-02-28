# ADB Auto-Connect

This tool automatically detects Android devices advertising ADB services over the network and establishes an ADB
connection without user intervention. It's designed to run in the background, making it perfect for developers who
frequently connect to Android devices for debugging or automation tasks.

## Intended Use

This tool was developed to automate the task of launching a scrcpy window for the user's phone. It likely has other use
cases, but it was not developed with those in mind.

## Features

- **Automatic Device Detection**: Automatically detects when the configured Android device is advertising its ADB service over the network.
- **Seamless Connection**: Establishes an ADB connection to the detected device without requiring manual input.
- **Custom Script Execution**: Optionally runs a custom script upon successfully connecting to the device, allowing for automated task execution (In my case this is a scrcpy-noconsole window).
- **Background Operation**: Runs silently in the background, without opening a terminal window.

## Getting Started

### Prerequisites

- ADB installed and added to your system's PATH.
- An Android device.
- Familiarity with Android developer settings.

### Installation

1. **Download the Executable**: Download the latest version of the `AutoADB.exe` from the Releases section.
2. **Place the Executable**: Put the `.exe` file in a convenient location on your system.

### Configuration

1. **Create a Shortcut**: Right-click on the `AutoADB.exe` and create a shortcut.
2. **Modify the Shortcut Target**: Right-click the shortcut, go to Properties, and modify the Target field by adding the Android device name and the optional script path. For example:

```
"path\to\AutoADB.exe" adb-0123456789ABCD-XXXXXX -p C:\Users\MyUserName\Desktop\scrcpy-noconsole.lnk
```
or if you're not interested in automating an external script:
```
"path\to\AutoADB.exe" adb-0123456789ABCD-XXXXXX
```
You **must** specify the adb service name, the applicaiton will not run without knowing which android device to connect to.

3. **Add to Startup**: Place the shortcut in your startup folder to have it run automatically at system startup. The startup folder can typically be found at:

```
C:\Users\MyUserName\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```

4. Use the Android developer settings to enable wireless debugging, use adb to pair your computer to your device

## Usage

Once configured, the tool will automatically start with your system, immediately beginning to listen for the specified Android device's ADB service advertisements. When detected, it will connect to the device and, if configured, execute your specified script.

## Building and Contributing

This was created using pyinstaller on python 3.9.13

1. Clone the repository.
2. Install packages: `pip install -r requirements.txt`
3. Run PyInstaller with the script: `pyinstaller --onefile --hidden-import=zeroconf._utils.ipaddress --hidden-import=zeroconf._handlers.answers -w .\AutoADB.py`

## Tentative future plans

- I may add a feature to allow the app to make it easier to browse and copy adb service names
- I may add a feature to allow the app to generate and display adb pairing QR codes

## License

This project is licensed under the MIT License - see the LICENSE file for details.
