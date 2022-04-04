class NetworkNode():
    def __init__(self, ip, username, password):
        self.device = {'host': ip, 'auth_username': username, 'auth_password': password, 'auth_strict_key': False}
    # def __str__(self):
    #     return f'{self.device}'

dev = NetworkNode('192.168.246.244', 'cisco', 'cisco')

print(dir(dev))

dev.__str__()

print(dev)