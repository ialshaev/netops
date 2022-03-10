import time
import logging
from datetime import datetime
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor
from inventory import devices
from netmiko import ConnectHandler


logging.getLogger('paramiko').setLevel(logging.WARNING)

logging.basicConfig(
    format = '%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO,
)


def send_show(device, show):
    start_msg = '===> {} Connection: {}'
    received_msg = '<=== {} Received:   {}'
    ip = device['host']
    conn_param = {
        "device_type": "cisco_ios_ssh",
        "username": "cisco",
        "password": "cisco",
        "host": ip
    }
    logging.info(start_msg.format(datetime.now().time(), ip))
    if ip == '192.168.100.1':
        time.sleep(5)

    with ConnectHandler(**conn_param) as ssh:
        ssh.enable()
        result = ssh.send_command(show)
        logging.info(received_msg.format(datetime.now().time(), ip))
        return result

with ThreadPoolExecutor() as executor:
    result = executor.map(send_show, devices, repeat('sh clock'))
    for device, output in zip(devices, result):
        print(device['host'] + ' ' + output)