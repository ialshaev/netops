The switchconfig.py script implies to gather VLAN information from IPAM system - NetBox and use these information further to configure switchports

the switchconfig.py execution result:

13:52 $ ./ntbx_to_dev.py 
'PROVIDE ADMIN CREDENTIALS'
Login: cisco
Password: 
'STEP1: RETREIVING DEVICE INFORMATION'
'number of devices defined in NetBox: 6'
'STEP2: GENERATING IP ADDRESS LIST'
("The list of ip addresses: ['192.168.246.241', '192.168.246.242', "
 "'192.168.246.243', '192.168.246.244', '192.168.246.245', '192.168.246.246']")
'STEP3: GENERATING VLAN TABLE'
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
'STEP4: GENERATING VLAN LISTS'
[101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111]
['SPB-MGMT', 'SPB-IPMI', 'SPB-TRANSIT', 'SPB-INFRASTRUCTURE', 'SPB-ENGINEERS', 'SPB-USERS-1FLOOR', 'SPB-USERS-2FLOOR', 'SPB-USERS-3FLOOR', 'SPB-QA', 'STO-QA', 'STO-MGMT']
'STEP5: SCANNING FOR IP ADDRESS AVAILABILITY'
192.168.246.241 is Available
192.168.246.242 is Available
192.168.246.243 is Available
192.168.246.244 is Available
192.168.246.245 is Available
192.168.246.246 is Available
The list of available devices:
['192.168.246.241', '192.168.246.242', '192.168.246.243', '192.168.246.244', '192.168.246.245', '192.168.246.246']
'STEP6: PUSH VLAN CONFIGURATION'
'PUSHING CONFIG ON 192.168.246.241'
'PUSHING CONFIG ON 192.168.246.242'
'PUSHING CONFIG ON 192.168.246.243'
'PUSHING CONFIG ON 192.168.246.244'
'PUSHING CONFIG ON 192.168.246.245'
'PUSHING CONFIG ON 192.168.246.246'
--Output omitted (same for each thread)--
'STEP7: PUSH SWITCHPORT CONFIGURATION'
'PUSHING CONFIG ON 192.168.246.241'
'PUSHING CONFIG ON 192.168.246.242'
'PUSHING CONFIG ON 192.168.246.243'
'PUSHING CONFIG ON 192.168.246.244'
'PUSHING CONFIG ON 192.168.246.245'
'PUSHING CONFIG ON 192.168.246.246'
'PUSHING CONFIG ON 192.168.246.241'
'PUSHING CONFIG ON 192.168.246.242'
'PUSHING CONFIG ON 192.168.246.243'
'PUSHING CONFIG ON 192.168.246.244'
'PUSHING CONFIG ON 192.168.246.245'
'PUSHING CONFIG ON 192.168.246.246'
'STEP8: VERIFY SWITCH CONFIGURATION'

Enter the device ip address or exit/interrupt to end the check procedure: 192.168.246.243
'IP address is valid'

Enter the command or exit/interrupt to end the check procedure. To change the device enter 0(zero): show clock
*10:53:40.930 UTC Mon Mar 21 2022

Enter the command or exit/interrupt to end the check procedure. To change the device enter 0(zero): 0

Changing device ip address

Enter the device ip address or exit/interrupt to end the check procedure: 192.168.246.246
'IP address is valid'

Enter the command or exit/interrupt to end the check procedure. To change the device enter 0(zero): show vlan bri
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

Enter the command or exit/interrupt to end the check procedure. To change the device enter 0(zero): show int status
Port      Name               Status       Vlan       Duplex  Speed Type
Gi0/0                        connected    routed     a-full   auto RJ45
Gi0/1                        connected    1          a-full   auto RJ45
Gi0/2     **SPB-INFRASTRUCTU connected    104        a-full   auto RJ45
Gi0/3     **SPB-INFRASTRUCTU connected    104        a-full   auto RJ45
Gi1/0                        connected    1          a-full   auto RJ45
Gi1/1                        connected    1          a-full   auto RJ45
Gi1/2                        connected    1          a-full   auto RJ45
Gi1/3                        connected    1          a-full   auto RJ45

Enter the command or exit/interrupt to end the check procedure. To change the device enter 0(zero): Exit
'Ended'

!!!
For improvements:
- disaply each thread output in a more short manner
- make push functions able to differentiate between sites and assign vlans according to site belonging