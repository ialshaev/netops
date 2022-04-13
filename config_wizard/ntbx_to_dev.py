import asyncio
import requests
import os
import re
import sys
import getpass
import asyncio
import logging
from pprint import pprint
from scrapli.driver.core import IOSXEDriver
from scrapli.driver.core import AsyncIOSXEDriver
from rich.console import Console
from rich.table import Table

class InvalidInput(Exception):
    """Raised when the invalid input has been entered"""
    pass

class InvalidIPAddress(Exception):
    """Raised when the wrong IP address has been entered"""
    pass

class ReExecute(Exception):
    """Raised when the function needs to be executed once again"""
    pass

class NetBox():
    def __init__(self,token,url):
        self.url = url
        self.headers = {'Content-Type': 'application/json','Accept': 'application/json','Authorization': token}
    def getDevices(self):
        self.Devices = requests.request("GET", f"http://{self.url}:8000/api/dcim/devices/", headers=self.headers).json()
        self.NDevices = self.Devices['count']
        DeviceListIPv4 = []
        for device in range (self.NDevices):
            ipv4 = self.Devices['results'][device]['primary_ip4']['address']
            DeviceListIPv4.append(ipv4[:-3])
        return self.NDevices, self.Devices, DeviceListIPv4
    def getVLANS(self):
        self.Vlans = requests.request("GET", f"http://{self.url}:8000/api/ipam/vlans/", headers=self.headers).json()
        self.NVlans = len(self.Vlans['results'])
        VIDList = []
        VNameList = []
        for vid,vname in zip(range(self.NVlans),range(self.NVlans)): #Generating 2 lists with VLAN IDs and names
            VIDList.append(self.Vlans['results'][vid]['vid'])
            VNameList.append(self.Vlans['results'][vname]['name'])
        return self.NVlans, self.Vlans, VIDList, VNameList
    def tableDevices(self):
        table = Table(title="Devices")
        table_properties = { 
            'DID': ['center', 'cyan', True],
            'NAME': ['left', 'green', False], 
            'TYPE': ['left', 'green', False], 
            'ROLE': ['left', 'green', False],
            'IPv4': ['center', 'green', False],
            }
        for item in table_properties.items():
            table.add_column(
                item[0],
                justify=item[1][0],
                style=item[1][1],
                no_wrap=item[1][2]
                )
        for device in range (self.NDevices):
            table.add_row(
                str(self.Devices['results'][device]['id']), 
                self.Devices['results'][device]['name'], 
                self.Devices['results'][device]['device_type']['model'], 
                self.Devices['results'][device]['device_role']['name'],
                self.Devices['results'][device]['primary_ip4']['address']
                )
        Console().print(table)
    def tableVLAN(self):
        table = Table(title="VLANs")
        table_properties = {
            'VID': ['center', 'cyan', True], 
            'NAME': ['left', 'green', False], 
            'DESCRIPTION': ['left', 'green', False], 
            'SITE': ['center', 'green', False]}
        for item in table_properties.items():
            table.add_column(
                item[0],
                justify=item[1][0],
                style=item[1][1],
                no_wrap=item[1][2]
                )
        for vlan in range (self.NVlans):
            table.add_row(
                str(self.Vlans['results'][vlan]['vid']), 
                self.Vlans['results'][vlan]['name'], 
                self.Vlans['results'][vlan]['description'], 
                self.Vlans['results'][vlan]['site']['name']
                )
        Console().print(table)

async def push_vlan_conf(vid,vname,ip,login,pwd):
    vlancli = [
        f'vlan {vid}' , 
        f'name {vname}'
        ]
    async with AsyncIOSXEDriver(
        host = ip, 
        auth_username = login, 
        auth_password = pwd, 
        auth_strict_key = False, 
        ssh_config_file = True, 
        transport = 'asyncssh'
    ) as vlan_conf_conn:
        await vlan_conf_conn.send_configs(vlancli)


async def push_swint_conf(ifname,ip,login,pwd):
    swintcli = [
        f'interface {ifname}', 
        'description cnfgred with scrapli', 
        'switchport mode access', 
        'switchport access vlan 111'
        ]
    async with AsyncIOSXEDriver(
        host = ip, 
        auth_username = login, 
        auth_password = pwd, 
        auth_strict_key = False, 
        ssh_config_file = True, 
        transport = 'asyncssh'
    ) as swint_conf_conn:
        await swint_conf_conn.send_configs(swintcli)

async def clear_conf(ip,login,pwd):
    clearcli = [
        'default interface range gi1/1-3', 
        'no vlan 101-111'
        ]
    async with AsyncIOSXEDriver(
        host = ip, 
        auth_username = login, 
        auth_password = pwd, 
        auth_strict_key = False, 
        ssh_config_file = True, 
        transport = 'asyncssh'
    ) as clear_conf_conn:
        await clear_conf_conn.send_configs(clearcli)
    
def show_cmd(username, password, ip):
    while True:
        try:        
            cmd = str(input('\nExit/exit <- to abort; change device -> 0; type "clear" -> to Clear/clear to clear config: '))
            if cmd == '0' or cmd == 'clear' or cmd == 'Clear':
                return cmd
            elif cmd == 'show memory':
                continue
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
                    with IOSXEDriver(
                        host = ip,
                        auth_username = username,
                        auth_password = password,
                        auth_strict_key = False,
                        ssh_config_file = True,
                        transport = 'paramiko',
                    ) as show_config_conn:
                        output = show_config_conn.send_command(cmd).result
                    if 'Invalid input detected' in output:
                        raise InvalidInput
                    else:   
                        print(output)
                except OSError as OSE:
                    print(OSE)
        except InvalidInput as II:
            pprint(II)
        except KeyboardInterrupt as KI:
            pprint (KI)
            res = 'Interrupted'
            return res

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

def check_availability(ip):
    status = os.system(f'ping -c 2 -W 2 {ip} > /dev/null')
    if status == False:
        pingresult = ip + ' is Available'
        print(pingresult)
        return(ip)
    else:
        pingresult = ip + ' is Unavailable'
        print(pingresult)

async def main(login,pwd,token,url_ip):

    netbox = NetBox(token,url_ip)
    devices_info = netbox.getDevices()
    vlans_info = netbox.getVLANS()

    pprint('STEP1: RETREIVING DEVICE INFORMATION AND GENERATING TABLE')
    pprint(f'number of devices defined in NetBox: {devices_info[0]}')
    netbox.tableDevices()
    pprint('STEP3: GENERATING IP ADDRESS LIST') # create the list of IP addresses
    pprint(devices_info[2])
    pprint('STEP2: RETREIVING VLAN INFORMATION AND GENERATING TABLE')
    pprint(f'number of VLANs defined in NetBox: {vlans_info[0]}')
    netbox.tableVLAN()
    pprint('STEP4: GENERATING VLAN LISTS')
    print(vlans_info[2])
    print(vlans_info[3])

    pprint('STEP5: SCANNING FOR IP ADDRESS AVAILABILITY')
    up_dev_list = []
    for ip in devices_info[2]:
        check_ip_result = check_availability(ip)
        if check_ip_result != None:
            up_dev_list.append(check_ip_result) #IP address availability scan 
    print('The list of available devices:')
    print(up_dev_list)

    pprint('STEP6: PUSH VLAN CONFIGURATION')
    for vid,vname in zip(vlans_info[2],vlans_info[3]):
        pprint(f'PUSHING {vname} ON SWITCHES')
        coroutines = [push_vlan_conf(vid,vname,ip,login,pwd) for ip in up_dev_list]
        await asyncio.gather(*coroutines)

    pprint('STEP7: PUSH SWITCHPORT CONFIGURATION')
    ifname_list = ['gi1/1', 'gi1/2', 'gi1/3']
    for ifname in ifname_list:
        pprint(f'PUSHING CONFIG ON SWITCHPORT - {ifname}')
        coroutines = [push_swint_conf(ifname,ip,login,pwd) for ip in up_dev_list]
        await asyncio.gather(*coroutines)

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
            elif dev_show == 'Clear' or dev_show == 'clear':
                coroutines = [clear_conf(ipv4,login,pwd) for ipv4 in up_dev_list]
                await asyncio.gather(*coroutines)

if __name__ == "__main__":

    logging.basicConfig(filename="ntbx_scrapli.log", level=logging.DEBUG)
    logger = logging.getLogger("scrapli")
    token = 'Token 0123456789abcdef0123456789abcdef01234567'
    netboxIPv4 = '192.168.246.130'

    pprint('PROVIDE ADMIN CREDENTIALS') #Define admin credentials
    username = input('Login: ')
    password = getpass.getpass('Password: ')
    asyncio.run(main(username,password,token,netboxIPv4))