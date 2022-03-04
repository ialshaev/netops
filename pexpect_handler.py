import pexpect
from inventory import devices
from multiprocessing import Process

cmd_output = []

# for i in devices:    
#     hostname = i['hostname']
#     print(hostname)

for d in devices:
    device = d['host']
    name = d['hostname']
    ssh = pexpect.spawn('ssh cisco@{}'.format(device))
    if ssh.expect('*RSA key fingerprint is*') == True:
        ssh.sendline('yes')
        ssh.expect('[pP]assword')
        ssh.sendline('cisco')
        ssh.expect('[>#]')
        ssh.sendline('sh ip int bri')
        ssh.expect('{}#'.format(name))
        output = ssh.before.decode('utf-8')
        print(output)
    else:
        ssh.expect('[pP]assword')
        ssh.sendline('cisco')
        ssh.expect('[>#]')
        ssh.sendline('sh ip int bri')
        ssh.expect('{}#'.format(name))
        output = ssh.before.decode('utf-8')
        print(output)