import telnetlib
import time
import os

HOST = "172.31.113.3"
R1_username = os.environ.get('TELNET_USER')
R1_password = os.environ.get('TELNET_PASSWORD')


tn = telnetlib.Telnet(HOST, 23, 5)

# Wait for login prompt
tn.read_until(b"Username: ")
print(R1_username)
tn.write(R1_username.encode('ascii') + b"\n")
time.sleep(1)

tn.read_until(b"Password: ")
print(R1_password)
tn.write(R1_password.encode('ascii') + b"\n")
time.sleep(1)

COMMANDS = [
    "conf t",
    "int g0/1",
    "vrf forwarding control-data",
    "ip add 192.168.1.1 255.255.255.0",
    "no shutdown",
    "int g0/2",
    "vrf forwarding control-data",
    "ip add 192.168.2.1 255.255.255.0",
    "no sh",
    "exit"
]

# Send commands
for command in COMMANDS:
    tn.write(command.encode('ascii') + b"\n")
    time.sleep(1)


# Close connection
tn.close()
