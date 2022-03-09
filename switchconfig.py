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

def rest(url,token):
    headers = {'Content-Type': 'application/json','Accept': 'application/json','Authorization': token}
    result = requests.request("GET", url, headers=headers).json()
    return(result)

def check_availability(ip):
    status = os.system('ping -c 1 -W 2 %s > /dev/null'%ip)
    if status == False:
        pingresult = ip + ' is Available'
    else:
        pingresult = ip + ' is Unavailable'
    return(pingresult)

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

def config_check(username,password):
    while True:
        ip = str(input('\ntype the device ip address or Exit to end the check procedure: '))
        if ip == 'Exit':
            break
        cmd = str(input('type the command or Exit to end the check procedure: '))
        if cmd != 'Exit':     
            device = ConnectHandler(device_type='cisco_ios', ip=ip, username=username, password=password)
            output = device.send_command(cmd)
            print(output)
        else:
            pprint('Ended')
            break

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
    pprint('The list of ip addresses: %s'%ip_addr_list) # pprint(type(ip_addr_list[0])) --> check for the list element type, must be string

    pprint('STEP3: GENERATING VLAN TABLE')
    url_vlans = "http://192.168.246.130:8000/api/ipam/vlans/"
    vlans = rest(url_vlans,token) #Retreive VLAN information from NetBox and display result in table view
    n_vlans = len(vlans['results'])
    pprint(f'number of VLANs defined in NetBox: {n_vlans}')
    create_table(n_vlans,vlans)

    pprint('STEP4: GENERATING VLAN LISTS')
    vlans_id_list = []
    vlans_name_list = []
    for vid,vname in zip(range(n_vlans),range(n_vlans)):
        vlans_id_list.append(vlans['results'][vid]['vid'])
        vlans_name_list.append(vlans['results'][vname]['name'])
    print(vlans_id_list)
    print(vlans_name_list)

    pprint('STEP5: SCANNING FOR IP ADDRESS AVAILABILITY')
    for ip in ip_addr_list:
        res = check_availability(ip) #IP address availability scan
        print(res)

    pprint('STEP6: PUSH VLAN CONFIGURATION')
    process1 = []
    for v,n in zip(vlans_id_list,vlans_name_list):
        for ip in ip_addr_list:
            proc = Process(target=push_config_vlan, args=(ip,v,n,username,password)) #Create VLANs on switches
            process1.append(proc)
            proc.start()
        proc.join()

    pprint('STEP7: PUSH SWITCHPORT CONFIGURATION')
    process2 = []
    intf = ['gi0/2', 'gi0/3']
    for int in intf:
        for ip in ip_addr_list:
            proc = Process(target=push_config_switchport, args=(ip,int,username,password)) #Assign VLANs on 5 switches
            process2.append(proc)
            proc.start()
        proc.join()

    pprint('STEP8: VERIFY SWITCH CONFIGURATION')
    config_check(username,password)