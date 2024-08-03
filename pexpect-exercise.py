import pexpect
import sys
import os
#R1-13
R1_ip = "172.31.113.3"
R1_username = os.environ.get('TELNET_USER')
R1_password = os.environ.get('TELNET_PASSWORD')
R1_command = 'ip address 172.16.1.1 255.255.255.255'

try:

    child = pexpect.spawn('telnet %s'%R1_ip)
    child.expect('Username:')
    child.sendline(R1_username)
    child.expect('Password:')
    child.sendline(R1_password)
    child.expect('#')
except pexpect.ExceptionPexpect as e:
    print(f"Error connecting to router: {e}")
    sys.exit(1)

child.sendline('conf t')
child.expect('\(config\)#')
child.sendline('int loopback 0')
child.expect('\(config-if\)#')
child.sendline(R1_command)
child.expect('\(config-if\)#')
print("Loopback0 172.16.1.1 is created on %s"%R1_ip)


#R2-13
R2_ip = "172.31.113.4"
R2_username = os.environ.get('TELNET_USER')
R2_password = os.environ.get('TELNET_PASSWORD')
R2_command = 'ip address 172.16.2.2 255.255.255.255'
try:
    child = pexpect.spawn('telnet %s'%R2_ip)
    child.expect('Username:')
    child.sendline(R2_username)
    child.expect('Password:')
    child.sendline(R2_password)
    child.expect('#')
except pexpect.ExceptionPexpect as e:
    print(f"Error connecting to router: {e}")
    sys.exit(1)
    
child.sendline('conf t')
child.expect('\(config\)#')
child.sendline('int loopback 0')
child.expect('\(config-if\)#')
child.sendline(R2_command)
child.expect('\(config-if\)#')
print("Loopback0 172.16.2.2 is created on %s"%R2_ip)
