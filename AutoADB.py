import os
import subprocess
import sys
import time
from socket import inet_ntoa
from subprocess import CalledProcessError, Popen, run
from time import sleep

import click
import win32com.client
from zeroconf import ServiceBrowser, ServiceInfo, Zeroconf


def create_shortcut(target_path, args, shortcut_path):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.TargetPath = target_path
    shortcut.Arguments = args
    shortcut.WorkingDirectory = os.path.dirname(target_path)
    shortcut.save()


class AdbListener:
    def __init__(self, name, auto_script=None):
        self.name = name
        self.auto_script = auto_script

    def remove_service(self, _, __, name):
        if not name.startswith(self.name):
            return
        try:
            run("adb disconnect", check=True, shell=True)
        except CalledProcessError as e:
            print(f"Error executing comment: {e}")

    def add_service(self, _, service_type, name):
        if not name.startswith(self.name):
            return
        info = zeroconf.get_service_info(service_type, name)
        if not info:
            return

        ip_address = inet_ntoa(info.addresses[0])
        port = info.port

        try:
            run(["adb", "disconnect"], check=True)
            run(["adb", "connect", f"{ip_address}:{port}"], check=True)
            if self.auto_script:
                print("Script path configured: running script")
                Popen(["start", "", self.auto_script], shell=True)
        except CalledProcessError as e:
            print(f"Error executing comment: {e}")

    def update_service(self, *_, **__):
        pass


class SetupListener:
    def __init__(self):
        self.names: list[str] = []
        self.infos: list[ServiceInfo] = []

    def remove_service(self, _, __, name):
        pass

    def add_service(self, _, service_type, name):
        short_name = name.split(".")[0]
        if short_name not in self.names:
            self.names.append(short_name)
            self.infos.append(zeroconf.get_service_info(service_type, name))
            print(f"\r{len(self.names)}: {short_name}\n Which service (input row number only)? ", end="")

    def update_service(self, *_, **__):
        pass


class PairingListener:
    def __init__(self, name, conf):
        self.name = name
        self.done = False
        self.conf: Zeroconf = conf

    def remove_service(self, _, __, name):
        pass

    def add_service(self, _, service_type, name):
        if not name.startswith(self.name):
            print(
                f"Pairing service detected from device {name.split('.')[0]}. "
                f"Are you sure you're configuring the right service name?"
            )
            return
        info: ServiceInfo = self.conf.get_service_info(service_type, name)
        if not info:
            print("Service detected with no config data, try re-launching pairing service.")
            return

        ip_address = inet_ntoa(info.addresses[0])
        port = info.port
        code = ""

        while not code:
            # noinspection PyBroadException
            try:
                code = input("Pairing code: ")
                assert len(code) == 6
                int(code)
            except Exception:
                print("Invalid input!")

        run(["adb", "pair", f"{ip_address}:{port}", code], check=True)
        self.done = True

    def update_service(self, *_, **__):
        pass


zeroconf = Zeroconf()


@click.command()
@click.argument("service-name", type=click.STRING, default=None, required=False)
@click.option("-p", "--script-path", type=click.Path(exists=True))
@click.option("-s", "--silent", is_flag=True, default=False)
def main(service_name: str, script_path: str, silent: bool):
    if service_name:
        if silent:
            execute = [sys.executable, service_name]
            if script_path:
                execute.extend(["-p", script_path])
            t = Popen(execute, creationflags=subprocess.CREATE_NO_WINDOW)
            return

        listener = AdbListener(service_name, script_path)
        browser = ServiceBrowser(zeroconf, "_adb-tls-connect._tcp.local.", listener)

        try:
            while True:
                time.sleep(60)
        finally:
            return zeroconf.close()

    listener = SetupListener()
    ServiceBrowser(zeroconf, "_adb-tls-connect._tcp.local.", listener)

    print("Ensure android device has wireless debugging enabled and is on the same network\n"
          "Searching for ADB services...")
    index = -1
    while index < 0 or index >= len(listener.names):
        # noinspection PyBroadException
        try:
            index = int(input("")) - 1
        except Exception:
            pass

    zeroconf.close()

    if input("Pair device? (Y/n) ").lower().strip()[:1] in "1yt":
        pairing_conf = Zeroconf()
        pairing_listener = PairingListener(listener.names[index], pairing_conf)
        ServiceBrowser(pairing_conf, "_adb-tls-pairing._tcp.local.", pairing_listener)
        print(
            'Open wireless debugging settings and tap "Pair device with pairing code"\n'
            "Searching for pairing services..."
        )
        while not pairing_listener.done:
            sleep(1)
        pairing_conf.close()

    if input("Automate connection? (Y/n) ").lower().strip()[:1] in "1yt":
        arguments = f"{listener.names[0]} -s"
        script_path = input("Enter automated command to run on connection (default blank): ")
        if script_path:
            script_path = script_path.replace('"', '^"')
            arguments += f' -p "{script_path}"'

        shortcut_path = os.path.join(
            os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs\Startup", f"AutoADB.lnk"
        )

        create_shortcut(sys.executable, arguments, shortcut_path)

        Popen([shortcut_path], shell=True)


if __name__ == "__main__":
    main()
