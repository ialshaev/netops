import pexpect
from inventory import devices
from multiprocessing import Process
from time import perf_counter
import getpass

def send_cmd (device,name,cmd,login,password):
    ssh = pexpect.spawn('ssh {}@{}'.format(login,device))
    ssh.expect('[pP]assword')
    ssh.sendline(password)
    ssh.expect('[>#]')
    ssh.sendline(cmd)
    ssh.expect('{}#'.format(name))
    output = ssh.before.decode('utf-8')
    print(output)

if __name__ == "__main__":
    cmd = input('Enter the command: ')
    username = input("Login: ")
    password = getpass.getpass()
    processes = []
    start = perf_counter()
    for d in devices:
        device = d['host']
        name = d['hostname']
        proc = Process(target=send_cmd, args=(device,name,cmd,username,password))
        processes.append(proc)

    for proc in processes:
        proc.start()

    for proc in processes:
        proc.join()

    end = perf_counter()
    total_time = end - start
    print(total_time)