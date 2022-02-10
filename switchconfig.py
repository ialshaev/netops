#!/home/admililiaa/netprog/bin/python3
import requests
import json
import socket
import os
from pprint import pprint
from netmiko import ConnectHandler
from rich.console import Console
from rich.table import Table

###Retreive device information from NetBox###
pprint('RETREIVING DEVICE INFORMATION')
url_devices = "http://192.168.246.130:8000/api/dcim/devices/"
url_vlans = "http://192.168.246.130:8000/api/ipam/vlans/"
headers = {'Content-Type': 'application/json','Accept': 'application/json','Authorization': 'Token 0123456789abcdef0123456789abcdef01234567'}
device_list = requests.request("GET", url_devices, headers=headers).json()
n_devices = len(device_list['results'])
# pprint(f'The device number is: {n_devices}')
pprint('GENERATING IP ADDRESS LIST') # create the list of IP addresses
ip_addr_list = []
for i in range (n_devices):
    ip = device_list['results'][i]['primary_ip4']['address']
    ip_addr_list.append(ip[:-3])
pprint(f'The list of ip addresses: {ip_addr_list}') # pprint(type(ip_addr_list[0])) --> check for the list element type, must be string
pprint('--------------------------------')


###Retreive VLAN information from NetBox and display result in table view###
output_vlans = requests.request("GET", url_vlans, headers=headers).json()
n_vlans = len(output_vlans['results'])
pprint(f'The VLAN number is: {n_vlans}')
table_vlans = Table(title="VLANs")
table_vlans.add_column("VLAN ID", justify="center", style="cyan", no_wrap=True)
table_vlans.add_column("NAME", style="magenta")
table_vlans.add_column("DESCRIPTION", style="green")
table_vlans.add_column("SITE", justify="center", style="blue")
for i in range (n_vlans):
  table_vlans.add_row(str(output_vlans['results'][i]['vid']), output_vlans['results'][i]['name'], output_vlans['results'][i]['description'], output_vlans['results'][i]['site']['name'])
console = Console()
console.print(table_vlans)

pprint('GENERSTING VLAN LISTS')
vlans_id_list = []
vlans_name_list = []
for vid,vname in zip(range(n_vlans),range(n_vlans)):
    vlans_id_list.append(output_vlans['results'][vid]['vid'])
    vlans_name_list.append(output_vlans['results'][vname]['name'])
print(vlans_id_list)
print(vlans_name_list)
pprint('--------------------------------')

###IP address availability scan###
# pprint('SCANNING FOR IP ADDRESS AVAILABILITY')
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# n = n_devices
# for num in range (n):
#     srv_ip = ip_addr_list[num]
#     ping = os.system('ping -c 1 ' + srv_ip)
#     if ping == 0:
#         print('server is up', srv_ip)
#     else:
#         print('server is down', srv_ip)

###Define admin credentials###
pprint('PROVIDE ADMIN CREDENTIALS')
username = input('login: ')
password = input('password: ')

###Create VLANs on 5 switches###
pprint('PUSH VLAN CONFIGURATION')
for ip in ip_addr_list:
    for v,n in zip(vlans_id_list,vlans_name_list):
        device = ConnectHandler(device_type='cisco_ios', ip=ip, username=username, password=password)
        vlancli = [f'vlan {v}', f'name {n}']
        device.send_config_set(vlancli)
        device.disconnect()

###Assign VLANs on 5 switches###
pprint('PUSH SWITCHPORT CONFIGURATION')
intf = ['gi0/2', 'gi0/3']
for gi in intf:
    for ip in ip_addr_list:
        device = ConnectHandler(device_type='cisco_ios', ip=ip, username=username, password=password)
        portcli = [f'interface {gi}', 'description **SPB-INFRASTRUCTURE cfg by netmiko**', 'switchport mode access', f'switchport access vlan 104']
        device.send_config_set(portcli)
        device.disconnect()
        
##Verify###
sw_ip = str(input('SWITCH IP: '))
pprint(f'DISPLAY CONFIGURATION FOR {sw_ip}')
device = ConnectHandler(device_type='cisco_ios', ip=sw_ip, username=username, password=password)
showvlanbri = device.send_command('show vlan bri')
print(showvlanbri)
showswpcfg = device.send_command('show run int gi0/2')
print(showswpcfg)
device.disconnect()