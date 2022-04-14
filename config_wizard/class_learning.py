from rich.table import Table
from rich.console import Console

class NetworkNode():
    def __init__(self, hostname, ipv4, username, password):
        self._hostname = hostname
        self._ipv4 = ipv4
        self.device = {'host': self._ipv4, 'auth_username': username, 'auth_password': password, 'auth_strict_key': False}

    def __str__(self): # adds __str__ magic method in the list of methods when execute print(dir(node))
        return f'{self._hostname}'

    @property
    def hostname(self):
        return self._hostname

    @property
    def ipv4(self):
        return self._ipv4

    @property
    def createTable(self):
        deviceTable = Table(title="Devices")
        table_properties = { 
            'NAME': ['center', 'cyan', True], 
            'IPv4': ['center', 'yellow', True]
            }
        for item in table_properties.items():
            deviceTable.add_column(
                item[0],
                justify=item[1][0],
                style=item[1][1],
                no_wrap=item[1][2]
                )
        deviceTable.add_row(
            self._hostname,
            self._ipv4
            )
        Console().print(deviceTable)

    @hostname.setter
    def hostname(self, hostname):
        if not isinstance(hostname, str):
            raise ValueError("Hostname must be a string value!")
        self._hostname = hostname

    @ipv4.setter
    def ipv4(self, ipv4):
        if not isinstance(ipv4, str):
            raise ValueError("IPv4 must be a string value!")
        self._ipv4 = ipv4

node = NetworkNode('spb-leaf01-mdf01', '192.168.246.241', 'cisco', 'cisco')

# print(dir(node))
# print(node)

node.hostname = 'sto-leaf03-mdf01'
node.ipv4 = '192.168.246.246/24'
node.createTable