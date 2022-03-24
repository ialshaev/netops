from scrapli.driver.core import IOSXEDriver
from pprint import pprint
import threading
import getpass
import requests
import os

class NetworkNodeConfig():
    def __init__(self, ip, uname, pwd):
        self.device = {'host': ip, 'auth_username': uname, 'auth_password': pwd, 'auth_strict_key': False}
    def show_cdp_neigh(self):
        self.send_show = 'show cdp nei'
        with IOSXEDriver(**self.device) as connection:
            output = connection.send_command(self.send_show)
            print(output.result)

def rest(url,token):
    headers = {'Content-Type': 'application/json','Accept': 'application/json','Authorization': token}
    result = requests.request("GET", url, headers=headers).json()
    return(result)

def check_availability(ip):
    status = os.system(f'ping -c 2 -W 2 {ip} > /dev/null')
    if status == False:
        pingresult = ip + ' is Available'
        print(pingresult)
        return(ip)
    else:
        pingresult = ip + ' is Unavailable'
        print(pingresult)

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

    pprint('STEP3: SCANNING FOR IP ADDRESS AVAILABILITY')
    up_dev_list = []
    for ip in ip_addr_list:
        check_ip_result = check_availability(ip)
        if check_ip_result != None:
            up_dev_list.append(check_ip_result) #IP address availability scan 
    print('The list of available devices:')
    print(up_dev_list)

    pprint('STEP4: RETRIEVE CDP INFORMATION')
    main_thread = []
    for ip in up_dev_list:
        pprint(f'RETRIEVING NEIGHBOURS FROM {ip}')
        net_node = NetworkNodeConfig(ip, username, password)
        thread = threading.Thread(target=net_node.show_cdp_neigh, args=()) #Assign VLANs on switches with description
        main_thread.append(thread)
        thread.start()
    for thread in main_thread:
        thread.join()