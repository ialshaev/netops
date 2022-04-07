#The script is designed to retrieve network device database from the Cisco ISE and visualize it in the table form per particular location

##To execute the script properly please follow the instructions:
'python ise_networkdevice_table.py "fqdn of the ISE server" "location for which all devices should be retrieved"'

##Auth: credentials are used to build base64 string and use it within Authorization Header.
When execute the script will propmt with the following:
ers-login:
ers-password:

##Expected output:
The device table for 'location' is generating...
                                      DEVICES                                      
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┓
┃               name                ┃ ip address     ┃ mask ┃ location ┃   type   ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━┩
│    firewall01.noc.domain.com      │ x.x.x.x        │ /X   │   MSK    │ Firewall │
│      core01.noc.domain.com        │ x.x.x.x        │ /X   │   SPB    │  Core    │
│ edge03.noc.domain.com             │ x.x.x.x        │ /X   │   EKB    │  Edge    │
│...                                │ ...            │ ...  │ ...      │ ...      │
└───────────────────────────────────┴────────────────┴──────┴──────────┴──────────┘
Total devices: N
