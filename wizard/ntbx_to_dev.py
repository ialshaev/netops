import requests
import os
import re
import sys
import threading
import getpass
from pprint import pprint
from scrapli.driver.core import IOSXEDriver
from rich.console import Console
from rich.table import Table

class NetworkNodeConfig():
    def __init__(self, ip, uname, pwd):
        self.device = {'host': ip, 'auth_username': uname, 'auth_password': pwd, 'auth_strict_key': False}
    def push_vlan_conf(self, v_id, v_name):
        self.vlancli =  [f'vlan {v_id}', f'name {v_name}']
        with IOSXEDriver(**self.device) as connection:
            connection.send_configs(self.vlancli)
    def push_swint_conf(self, i_name):
        self.swintcli = [f'interface {i_name}', 'description cnfgred with scrapli', 'switchport mode access', 'switchport access vlan 111']
        with IOSXEDriver(**self.device) as connection:
            connection.send_configs(self.swintcli)

class InvalidInput(Exception):
    """Raised when the invalid input has been entered"""
    pass

class InvalidIPAddress(Exception):
    """Raised when the wrong IP address has been entered"""
    pass

class ReExecute(Exception):
    """Raised when the function needs to be executed once again"""
    pass


def rest(url,token):
    headers = {'Content-Type': 'application/json','Accept': 'application/json','Authorization': token}
    result = requests.request("GET", url, headers=headers).json()
    return(result)

def create_table(n_vlans,vlans):
    table_vlans = Table(title="VLANs")
    table_vlans.add_column("VID", justify="center", style="cyan", no_wrap=True)
    table_vlans.add_column("NAME", style="magenta")
    table_vlans.add_column("DESCRIPTION", style="green")
    table_vlans.add_column("SITE", justify="center", style="blue")
    for i in range (n_vlans):
        table_vlans.add_row(str(vlans['results'][i]['vid']), vlans['results'][i]['name'], vlans['results'][i]['description'], vlans['results'][i]['site']['name'])
    console = Console()
    console.print(table_vlans)

def check_availability(ip):
    status = os.system(f'ping -c 2 -W 2 {ip} > /dev/null')
    if status == False:
        pingresult = ip + ' is Available'
        print(pingresult)
        return(ip)
    else:
        pingresult = ip + ' is Unavailable'
        print(pingresult)

def check_ip(ip_address_list):
    while True:
        try:
            ip = str(input('\nEnter the device ip address or exit/interrupt to end the check procedure: '))
            ip_addr = re.match(r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$",ip)
            if ip_addr:
                pprint('IP address is valid')
                if ip in ip_address_list:
                    return ip
                else:
                    pprint('IP address is out of range')
            elif ip == 'Exit':
                pprint('Ended')
                res = 'Ended'
                return res
            elif ip == 'exit':
                pprint('Ended')
                res = 'Ended'
                return res
            else:
                raise InvalidIPAddress
        except InvalidIPAddress as IIPA:
            pprint(IIPA)
        except KeyboardInterrupt as KI:
            pprint (KI)
            res = 'Interrupted'
            return res


def show_cmd(username, password, ip):
    while True:
        try:        
            cmd = str(input('\nEnter the command or exit/interrupt to end the check procedure. To change the device enter 0(zero): '))
            if cmd == '0':
                return cmd
            elif cmd == 'Exit':
                pprint('Ended')
                res = 'Ended'
                return res
            elif cmd == 'exit':
                pprint('Ended')
                res = 'Ended'
                return res
            else:
                try:
                    device = {'host': ip, 'auth_username': username, 'auth_password': password, 'auth_strict_key': False}
                    with IOSXEDriver(**device) as connection:
                        output = connection.send_command(cmd)
                        output_result = output.result
                    if 'Invalid input detected' in output_result:
                        raise InvalidInput
                    else:   
                        print(output_result)
                except OSError as OSE:
                    print(OSE)
        except InvalidInput as II:
            pprint(II)
        except KeyboardInterrupt as KI:
            pprint (KI)
            res = 'Interrupted'
            return res


if __name__ == "__main__":
    token = 'Token 0123456789abcdef0123456789abcdef01234567'
    pprint('PROVIDE ADMIN CREDENTIALS') #Define admin credentials
    username = input('Login: ')
    password = getpass.getpass()

    pprint('STEP1: RETREIVING DEVICE INFORMATION')
    url_devices = "http://192.168.246.130:8000/api/dcim/devices/"
    devices = rest(url_devices,token) #Retreive device information from NetBox
    n_devices = len(devices['results'])
    pprint(f'number of devices defined in NetBox: {n_devices}')

    pprint('STEP2: GENERATING IP ADDRESS LIST') # create the list of IP addresses
    ip_addr_list = []
    for i in range (n_devices):
        ip = devices['results'][i]['primary_ip4']['address']
        ip_addr_list.append(ip[:-3])
    pprint(f'The list of ip addresses: {ip_addr_list}') # pprint(type(ip_addr_list[0])) --> check for the list element type, must be string

    pprint('STEP3: GENERATING VLAN TABLE')
    url_vlans = "http://192.168.246.130:8000/api/ipam/vlans/"
    vlans = rest(url_vlans,token) #Retreive VLAN information from NetBox and display result in table view
    n_vlans = len(vlans['results'])
    pprint(f'number of VLANs defined in NetBox: {n_vlans}')
    create_table(n_vlans,vlans)

    pprint('STEP4: GENERATING VLAN LISTS')
    vlans_id_list = []
    vlans_name_list = []
    for vid,vname in zip(range(n_vlans),range(n_vlans)): #Generating 2 lists with VLAN IDs and names
        vlans_id_list.append(vlans['results'][vid]['vid'])
        vlans_name_list.append(vlans['results'][vname]['name'])
    print(vlans_id_list)
    print(vlans_name_list)

    pprint('STEP5: SCANNING FOR IP ADDRESS AVAILABILITY')
    up_dev_list = []
    for ip in ip_addr_list:
        check_ip_result = check_availability(ip)
        if check_ip_result != None:
            up_dev_list.append(check_ip_result) #IP address availability scan 
    print('The list of available devices:')
    print(up_dev_list)

    pprint('STEP6: PUSH VLAN CONFIGURATION')
    first_thread = []
    for v_id,v_name in zip(vlans_id_list,vlans_name_list):
        for ip in up_dev_list:
            pprint(f'PUSHING CONFIG ON {ip}')
            net_node = NetworkNodeConfig(ip, username, password)
            thread = threading.Thread(target=net_node.push_vlan_conf, args=(v_id,v_name)) #Create VLANs on switches
            first_thread.append(thread)
            thread.start()
        for thread in first_thread:
            thread.join()

    pprint('STEP7: PUSH SWITCHPORT CONFIGURATION')
    second_thread = []
    int_list = ['gi0/2', 'gi0/3']
    for int in int_list:
        for ip in up_dev_list:
            pprint(f'PUSHING CONFIG ON {ip}')
            net_node = NetworkNodeConfig(ip, username, password)
            thread = threading.Thread(target=net_node.push_swint_conf, args=(int,)) #Assign VLANs on switches with description
            second_thread.append(thread)
            thread.start()
        for thread in second_thread:
            thread.join()

    pprint('STEP8: VERIFY SWITCH CONFIGURATION')
    while True:
        dev_ip = check_ip(up_dev_list)
        if dev_ip == 'Ended' or dev_ip == 'Interrupted':
            sys.exit()
        else:
            dev_show = show_cmd(username, password, dev_ip)
            if dev_show == '0':
                print('\nChanging device ip address')
            elif dev_show == 'Ended' or dev_show == 'Interrupted':
                sys.exit()