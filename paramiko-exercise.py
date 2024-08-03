import paramiko
import time

R2_IP = '172.31.113.4'
USERNAME = 'admin'
key_path = '/home/devasc/.ssh/adminR2_id_rsa'

commands = ["conf t\n",
            "int g0/1\n", 
            "vrf forwarding control-data\n", 
            "ip address 192.168.2.2 255.255.255.0\n", 
            "no shutdown\n",
            "exit\n",
            "int g0/2\n", 
            "vrf forwarding control-data\n", 
            "ip address 192.168.3.1 255.255.255.0\n",
            "no shutdown\n",
            "exit\n",
            "int g0/3\n", 
            "vrf forwarding control-data\n", 
            "ip address dhcp\n",
            "no shutdown\n",
            "exit\n",

            ]

def configure_router(hostname, port, username, private_key_path, commands):
    try:

        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port, username, pkey=private_key)
        shell = client.invoke_shell()
        for i in commands:
            shell.send(i)
            output = shell.recv(65535).decode('utf-8')
            print(output)
            time.sleep(1)
            
        shell.close()
        client.close()
        print("Configuration applied successfully.")

    except paramiko.SSHException as e:
        print(f"SSH Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

# Call the function to configure the router
configure_router(R2_IP, 22, USERNAME, key_path, commands)
