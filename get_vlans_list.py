#!/home/admililiaa/netprog/bin/python3
import requests
import json
from pprint import pprint
from rich.console import Console
from rich.table import Table

url = "http://192.168.246.130:8000/api/ipam/vlans/"
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Token 0123456789abcdef0123456789abcdef01234567'
}

vlans_output = requests.request("GET", url, headers=headers).json()
vlans_number = len(vlans_output['results'])
print(f'The cureent VLAN number is: {vlans_number}')

table_vlans = Table(title="VLANs")
table_vlans.add_column("VLAN ID", justify="center", style="cyan", no_wrap=True)
table_vlans.add_column("NAME", style="magenta")
table_vlans.add_column("DESCRIPTION", style="green")
table_vlans.add_column("SITE", style="blue")
for vl in range (vlans_number):
     table_vlans.add_row(str(vlans_output['results'][vl]['vid']), vlans_output['results'][vl]['name'], vlans_output['results'][vl]['description'], vlans_output['results'][vl]['site']['name'])

console = Console()
console.print(table_vlans)