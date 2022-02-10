the switchconfig.py execution result:

19:59 $ ./switchconfig.py 
'RETREIVING DEVICE INFORMATION'
'number of devices defined in NetBox: 5'
'GENERATING IP ADDRESS LIST'
("The list of ip addresses: ['192.168.246.241', '192.168.246.242', "
 "'192.168.246.243', '192.168.246.244', '192.168.246.245']")
'--------------------------------'
'GENERATING VLAN TABLE'
'number of VLANs defined in NetBox: 11'
                           VLANs                            
┏━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┓
┃ VID ┃ NAME               ┃ DESCRIPTION            ┃ SITE ┃
┡━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━┩
│ 101 │ SPB-MGMT           │ network management     │ SPB  │
│ 102 │ SPB-IPMI           │ server management      │ SPB  │
│ 103 │ SPB-TRANSIT        │ transit connectivity   │ SPB  │
│ 104 │ SPB-INFRASTRUCTURE │ infrastructure servers │ SPB  │
│ 105 │ SPB-ENGINEERS      │ engeneering stuff      │ SPB  │
│ 106 │ SPB-USERS-1FLOOR   │ data                   │ SPB  │
│ 107 │ SPB-USERS-2FLOOR   │ data                   │ SPB  │
│ 108 │ SPB-USERS-3FLOOR   │ data                   │ SPB  │
│ 109 │ SPB-QA             │ QA data                │ SPB  │
│ 110 │ STO-QA             │ QA data                │ STO  │
│ 111 │ STO-MGMT           │ network management     │ STO  │
└─────┴────────────────────┴────────────────────────┴──────┘
'GENERATING VLAN LISTS'
[101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111]
['SPB-MGMT', 'SPB-IPMI', 'SPB-TRANSIT', 'SPB-INFRASTRUCTURE', 'SPB-ENGINEERS', 'SPB-USERS-1FLOOR', 'SPB-USERS-2FLOOR', 'SPB-USERS-3FLOOR', 'SPB-QA', 'STO-QA', 'STO-MGMT']
'--------------------------------'
'SCANNING FOR IP ADDRESS AVAILABILITY'
PING 192.168.246.241 (192.168.246.241) 56(84) bytes of data.
64 bytes from 192.168.246.241: icmp_seq=1 ttl=255 time=2.63 ms

--- 192.168.246.241 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 2.628/2.628/2.628/0.000 ms
Available
PING 192.168.246.242 (192.168.246.242) 56(84) bytes of data.
64 bytes from 192.168.246.242: icmp_seq=1 ttl=255 time=3.19 ms

--- 192.168.246.242 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 3.186/3.186/3.186/0.000 ms
Available
PING 192.168.246.243 (192.168.246.243) 56(84) bytes of data.
64 bytes from 192.168.246.243: icmp_seq=1 ttl=255 time=6.92 ms

--- 192.168.246.243 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 6.924/6.924/6.924/0.000 ms
Available
PING 192.168.246.244 (192.168.246.244) 56(84) bytes of data.
64 bytes from 192.168.246.244: icmp_seq=1 ttl=255 time=3.12 ms

--- 192.168.246.244 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 3.117/3.117/3.117/0.000 ms
Available
PING 192.168.246.245 (192.168.246.245) 56(84) bytes of data.
64 bytes from 192.168.246.245: icmp_seq=1 ttl=255 time=3.86 ms

--- 192.168.246.245 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 3.857/3.857/3.857/0.000 ms
Available
'PROVIDE ADMIN CREDENTIALS'
login: cisco
password: cisco
'PUSH VLAN CONFIGURATION'
'PUSH SWITCHPORT CONFIGURATION'
'DISPLAY CONFIGURATION FOR 192.168.246.242'

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Gi0/1, Gi1/0, Gi1/1, Gi1/2, Gi1/3
101  SPB-MGMT                         active    
102  SPB-IPMI                         active    
103  SPB-TRANSIT                      active    
104  SPB-INFRASTRUCTURE               active    Gi0/2, Gi0/3
105  SPB-ENGINEERS                    active    
106  SPB-USERS-1FLOOR                 active    
107  SPB-USERS-2FLOOR                 active    
108  SPB-USERS-3FLOOR                 active    
109  SPB-QA                           active    
110  STO-QA                           active    
111  STO-MGMT                         active    
1002 fddi-default                     act/unsup 
1003 token-ring-default               act/unsup 
1004 fddinet-default                  act/unsup 
1005 trnet-default                    act/unsup 
Building configuration...

Current configuration : 157 bytes
!
interface GigabitEthernet0/3
 description **SPB-INFRASTRUCTURE cfg by netmiko**
 switchport access vlan 104
 switchport mode access
 negotiation auto
end

!!!
For improvements:
- involve multithreading
- fix functions