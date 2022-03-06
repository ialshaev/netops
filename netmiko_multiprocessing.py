from multiprocessing import Process
from time import perf_counter
from scrapli.driver.core import IOSXEDriver
from inventory import DEVICES
from netmiko import ConnectHandler

start = perf_counter()

processes = []

# def send_cmd(device):
#     with IOSXEDriver(
#         host = device["host"],
#         auth_username="cisco",
#         auth_password="cisco",
#         auth_strict_key=False,
#         ssh_config_file=True,
#     ) as conn:
#         response = conn.send_command("show int status")
#         print(response.result)

def send_cmd(device):
    conn_params = {
        "device_type": "cisco_ios_ssh",
        "host": "192.168.241.246",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }
    with ConnectHandler(**conn_params) as conn:
        response = conn.send_show_command("show int status")
        print(response.result)

if __name__ == "__main__":
    for device in DEVICES:
        proc = Process(target=send_cmd, args=(device,))
        processes.append(proc)

    for proc in processes:
        proc.start()

    for proc in processes:
        proc.join()

    end = perf_counter()
    total_time = end - start
    print(total_time)