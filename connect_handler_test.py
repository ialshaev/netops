from pprint import pprint
from netmiko import (ConnectHandler,NetmikoTimeoutException,NetmikoAuthenticationException,)
from inventory import devices
import getpass

username = input("login: ")
password = getpass.getpass()

def send_show_cmd(device, commands):
    result = {}
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            for command in commands:
                output = ssh.send_command(command)
                result[command] = output
        return result
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)

if __name__ == "__main__":



# from time import perf_counter
# from multiprocessing import Process

# start = perf_counter()

#     for dev in DEVICES:
#         device = {
#             "device_type": "cisco_ios_ssh",
#             "host": dev["host"],
#             "username": "cisco",
#             "password": "cisco",
#             "secret": "cisco",
#         }
#         result = send_show_command(device, ["sh clock", "sh ip int br"])
#         pprint(result, width=120)

#     end = perf_counter()
#     total_time = end - start
#     print(total_time)