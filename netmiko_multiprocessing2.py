from concurrent.futures import ProcessPoolExecutor
from time import perf_counter
from inventory import devices
from netmiko import ConnectHandler

def send_cmd(device):
    conn_params = {
        "device_type": "cisco_ios_ssh",
        "host": device['host'],
        "username": 'cisco',
        "password": 'cisco'
    }
    with ConnectHandler(**conn_params) as conn:
        response = conn.send_command('show clock')
        return response


if __name__ == "__main__":

    start = perf_counter()

    with ProcessPoolExecutor() as exec:
        results = exec.map(send_cmd, devices)

    for output in results:
        print(output)

    end = perf_counter()
    total_time = end - start
    print(total_time)