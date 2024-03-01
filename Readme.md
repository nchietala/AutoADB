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

Download the latest release. The process runs from a standalone executable, there is no installation.

### Configuration / Usage

Run the executable. It is a command line tool and when launched without options it will create a terminal wizard to configure the android device and to automate its own startup.

If you choose to automate the connection you will be asked to specify a command to run when the connection is made, in my case the command is `scrcpy-noconsole`

## Building and Contributing

This was created using pyinstaller on python 3.9.13

1. Clone the repository.
2. Install packages: `pip install -r requirements.txt`
3. Run PyInstaller with the script: `pyinstaller --onefile --hidden-import=zeroconf._utils.ipaddress --hidden-import=zeroconf._handlers.answers -w .\AutoADB.py`

## License

This project is licensed under the MIT License - see the LICENSE file for details.
