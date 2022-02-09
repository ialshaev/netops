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

output_vlans = requests.request("GET", url, headers=headers).json()
number_vlans = len(output_vlans['results'])
print(f'The cureent VLAN number is: {number_vlans}')

table_vlans = Table(title="VLANs")
table_vlans.add_column("VLAN ID", justify="center", style="cyan", no_wrap=True)
table_vlans.add_column("NAME", style="magenta")
table_vlans.add_column("DESCRIPTION", style="green")
table_vlans.add_column("SITE", style="blue")
for vl in range (number_vlans):
  table_vlans.add_row(str(output_vlans['results'][vl]['vid']), output_vlans['results'][vl]['name'], output_vlans['results'][vl]['description'], output_vlans['results'][vl]['site']['name'])

console = Console()
console.print(table_vlans)

# for vl in range (number_vlans):
#   pprint(output_vlans['results'][vl]['name'])
#   pprint('------------')