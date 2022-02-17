
from scrapli import Scrapli

device = {
   "host": "192.168.246.241",
   "auth_username": "cisco",
   "auth_password": "cisco",
   "auth_strict_key": False,
   "platform": "cisco_iosxe"
}

conn = Scrapli(**device)
conn.open()
print(conn.get_prompt())