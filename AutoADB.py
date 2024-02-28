from zeroconf import ServiceBrowser, Zeroconf
from subprocess import run, CalledProcessError, Popen
from socket import inet_ntoa
import click
import time


class AdbListener:
    def __init__(self, name, auto_script=None):
        self.name = name
        self.auto_script = auto_script

    def remove_service(self, _, __, name):
        if not name.startswith(self.name):
            return
        try:
            run('adb disconnect', check=True, shell=True)
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
            run(['adb', 'disconnect'], check=True)
            run(['adb', 'connect', f'{ip_address}:{port}'], check=True)
            if self.auto_script:
                print("Script path configured: running script")
                Popen(["start", "", self.auto_script], shell=True)
        except CalledProcessError as e:
            print(f"Error executing comment: {e}")

    def update_service(self, *_, **__):
        pass


zeroconf = Zeroconf()


@click.command()
@click.argument('service-name', type=click.STRING)
@click.option('-p', '--script-path', type=click.Path(exists=True))
def main(service_name, script_path):
    listener = AdbListener(service_name, script_path)
    browser = ServiceBrowser(zeroconf, "_adb-tls-connect._tcp.local.", listener)

    try:
        while True:
            time.sleep(60)
    finally:
        zeroconf.close()


if __name__ == '__main__':
    main()
