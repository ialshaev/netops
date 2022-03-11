from concurrent.futures import ThreadPoolExecutor
from time import perf_counter
from inventory import devices
from netmiko import ConnectHandler
from itertools import repeat
import getpass

def send_cmd(device,login,password,cmd):
    conn_params = {
        "device_type": "cisco_ios_ssh",
        "host": device['host'],
        "username": login,
        "password": password
    }
    with ConnectHandler(**conn_params) as conn:
        response = conn.send_command(cmd)
        return response


if __name__ == "__main__":

    cmd = input('Enter the command: ')
    username = input("Login: ")
    password = getpass.getpass()

    start = perf_counter()

    with ThreadPoolExecutor() as executor:
        results = executor.map(send_cmd, devices, repeat(username), repeat(password), repeat(cmd))

    for output in results:
        print(output)

    end = perf_counter()
    total_time = end - start
    print(total_time)