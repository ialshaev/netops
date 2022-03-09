#!/home/admililiaa/netprog/bin/python3
import requests
import os
from pprint import pprint
from netmiko import ConnectHandler
from rich.console import Console
from rich.table import Table
from multiprocessing import Process
import getpass

def push_config_vlan(ip,v,n,username,password):
    device = ConnectHandler(device_type='cisco_ios', ip=ip, username=username, password=password)
    vlancli = [f'vlan {v}', f'name {n}']
    device.send_config_set(vlancli)
    device.disconnect()

def push_config_switchport(ip,int,username,password):
    device = ConnectHandler(device_type='cisco_ios', ip=ip, username=username, password=password)
    portcli = [f'interface {int}', 'description **SPB-INFRASTRUCTURE cfg by netmiko**', 'switchport mode access', f'switchport access vlan 104']
    device.send_config_set(portcli)
    device.disconnect()

def check_config(ip,cmds,username,password):
    for cmd in cmds:
        device = ConnectHandler(device_type='cisco_ios', ip=ip, username=username, password=password)
        device.send_command(cmd)
        device.disconnect()

def rest(url):
    headers = {'Content-Type': 'application/json','Accept': 'application/json','Authorization': 'Token 0123456789abcdef0123456789abcdef01234567'}
    result = requests.request("GET", url, headers=headers).json()
    return(result)

def check_availability(ip):
    status = os.system('ping -c 1 -W 2 %s > /dev/null'%ip)
    if status == False:
        pingresult = ip + ' is Available'
    else:
        pingresult = ip + ' is Unavailable'
    return(pingresult)

if __name__ == "__main__":
    ###Retreive device information from NetBox###
    pprint('RETREIVING DEVICE INFORMATION')
    url_devices = "http://192.168.246.130:8000/api/dcim/devices/"
    devices = rest(url_devices)
    n_devices = len(devices['results'])
    pprint(f'number of devices defined in NetBox: {n_devices}')
    pprint('GENERATING IP ADDRESS LIST') # create the list of IP addresses
    ip_addr_list = []
    for i in range (n_devices):
        ip = devices['results'][i]['primary_ip4']['address']
        ip_addr_list.append(ip[:-3])
    pprint(f'The list of ip addresses: {ip_addr_list}') # pprint(type(ip_addr_list[0])) --> check for the list element type, must be string
    pprint('--------------------------------')

    ###Retreive VLAN information from NetBox and display result in table view###
    url_vlans = "http://192.168.246.130:8000/api/ipam/vlans/"
    pprint('GENERATING VLAN TABLE')
    vlans = rest(url_vlans)
    n_vlans = len(vlans['results'])
    pprint(f'number of VLANs defined in NetBox: {n_vlans}')
    table_vlans = Table(title="VLANs")
    table_vlans.add_column("VID", justify="center", style="cyan", no_wrap=True)
    table_vlans.add_column("NAME", style="magenta")
    table_vlans.add_column("DESCRIPTION", style="green")
    table_vlans.add_column("SITE", justify="center", style="blue")
    for i in range (n_vlans):
        table_vlans.add_row(str(vlans['results'][i]['vid']), vlans['results'][i]['name'], vlans['results'][i]['description'], vlans['results'][i]['site']['name'])
    console = Console()
    console.print(table_vlans)
    pprint('GENERATING VLAN LISTS')
    vlans_id_list = []
    vlans_name_list = []
    for vid,vname in zip(range(n_vlans),range(n_vlans)):
        vlans_id_list.append(vlans['results'][vid]['vid'])
        vlans_name_list.append(vlans['results'][vname]['name'])
    print(vlans_id_list)
    print(vlans_name_list)
    pprint('--------------------------------')

    ###IP address availability scan###
    pprint('SCANNING FOR IP ADDRESS AVAILABILITY')
    for ip in ip_addr_list:
        res = check_availability(ip)
        print(res)

    ###Define admin credentials###
    pprint('PROVIDE ADMIN CREDENTIALS')
    username = input('Login: ')
    password = getpass.getpass()

    ###Create VLANs on switches###
    pprint('PUSH VLAN CONFIGURATION')
    process1 = []
    for v,n in zip(vlans_id_list,vlans_name_list):
        for ip in ip_addr_list:
            proc = Process(target=push_config_vlan, args=(ip,v,n,username,password))
            process1.append(proc)
            proc.start()
        proc.join()

    ###Assign VLANs on 5 switches###
    pprint('PUSH SWITCHPORT CONFIGURATION')
    process2 = []
    intf = ['gi0/2', 'gi0/3']
    for int in intf:
        for ip in ip_addr_list:
            proc = Process(target=push_config_switchport, args=(ip,int,username,password))
            process2.append(proc)
            proc.start()
        proc.join()

    ##Verify###
    # ip = str(input('SWITCH IP: '))
    ip = '192.168.246.242'
    pprint(f'DISPLAY CONFIGURATION FOR {ip}')
    commands = ['sh vlan bri', 'sh run int gi0/3']
    for cmd in commands:
        device = ConnectHandler(device_type='cisco_ios', ip=ip, username=username, password=password)
        output = device.send_command(cmd)
        print(output)