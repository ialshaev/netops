from multiprocessing import Process
from time import perf_counter
from inventory import devices
from netmiko import ConnectHandler
import getpass

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

def send_cmd(device,login,password,cmd):
    conn_params = {
        "device_type": "cisco_ios_ssh",
        "host": device,
        "username": login,
        "password": password
    }
    with ConnectHandler(**conn_params) as conn:
        response = conn.send_command(cmd)
        print(response)
    # connection = ConnectHandler(**conn_params)


if __name__ == "__main__":
    cmd = input('Enter the command: ')
    username = input("Login: ")
    password = getpass.getpass()
    processes = []
    start = perf_counter()
    for d in devices:
        device = d['host']
        name = d['hostname']
        proc = Process(target=send_cmd, args=(device,username,password,cmd))
        processes.append(proc)

    for proc in processes:
        proc.start()

    for proc in processes:
        proc.join()

    end = perf_counter()
    total_time = end - start
    print(total_time)