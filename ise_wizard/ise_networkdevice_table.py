import requests
import sys
import base64
from rich.console import Console
from rich.table import Table


def parse_device_type(string):
    string_formatted = string.split('#')
    types = ['Edge','Core','Distribution','Access','Management','Firewall','SD-WAN','Voice','Market','Wireless']
    for item in string_formatted:
        if item in types:
            device_type = item
            return device_type
        else:
            continue

def parse_device_location(string):
    string_formatted = string.split('#')
    locations = ['CH1','CHI','HKG','LON','STO','SPB','NYC','MAN','MIL','CLU','TKY','SYD','MUM','LUN']
    for item in string_formatted:
        if item in locations:
            device_location = item
            return device_location
        else:
            continue

if __name__ == "__main__":

    login = str(input('ers-login: '))
    password = str(input('ers-password: '))
    credentials = login + ':' + password
    credentials_bytes = credentials.encode('ascii')

    encoded_bytes = base64.b64encode(credentials_bytes)
    encoded_string = encoded_bytes.decode('ascii')

    base64 = 'Basic ' + str(encoded_string)

    try:
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': base64
        }

        url_fqdn = sys.argv[1].lower()
        url_networkdevices_location = sys.argv[2].upper()
        url_networkdevices = "https://" + url_fqdn + ":9060/ers/config/networkdevice?filter=location.CONTAINS." + url_networkdevices_location
        networkdevices = requests.request("GET", url_networkdevices, headers=headers, data={}).json()
        networkdevices_resources = networkdevices['SearchResult']['resources']

        device_names = []
        for device in networkdevices_resources:
            device_names.append(device['name'])

        try:
            if networkdevices['SearchResult']['nextPage']['rel'] == "next":
                networkdevices_next = "https://" + url_fqdn + ":9060/ers/config/networkdevice?filter=location.CONTAINS." + url_networkdevices_location +"&page=2"
                networkdevices_nextpage = requests.request("GET", networkdevices_next, headers=headers, data="").json()['SearchResult']['resources']
                for device_nextpage in networkdevices_nextpage:
                    device_names.append(device_nextpage['name'])
        except:
            pass

        devicetable = Table(title="DEVICES")
        devicetable.add_column("name", justify="center", style="cyan", no_wrap=True)
        devicetable.add_column("ip address", style="magenta")
        devicetable.add_column("mask", style="green")
        devicetable.add_column("location", justify="center", style="blue")
        devicetable.add_column("type", justify="center", style="yellow")

        print(f'The device table for {url_networkdevices_location} is generating...')
        for name in device_names:
            url_device = "https://" + url_fqdn + ":9060/ers/config/networkdevice/name/" + name
            device_details = requests.request("GET", url_device, headers=headers, data="")
            devicetable.add_row(device_details.json()['NetworkDevice']['name'], 
                                device_details.json()['NetworkDevice']['NetworkDeviceIPList'][0]['ipaddress'],
                                str(device_details.json()['NetworkDevice']['NetworkDeviceIPList'][0]['mask']), 
                                parse_device_location(device_details.json()['NetworkDevice']['NetworkDeviceGroupList'][0]), 
                                parse_device_type(device_details.json()['NetworkDevice']['NetworkDeviceGroupList'][2]))
            console = Console()
        console.print(devicetable)
        print(f'Total devices: {len(device_names)}')
    except IndexError:
        print('\ndid you add an argument next to the script?\n')