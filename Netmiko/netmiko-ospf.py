from netmiko import ConnectHandler
import os
username = os.environ.get('TELNET_USER')
password = os.environ.get('TELNET_PASSWORD')

routers = [
    {   
        'device_type':'cisco_ios',
        'ip': '172.31.113.3',
        'username': username,
        'password': password,
        'commands': [
            'router ospf 1 vrf control-data',
            'network 192.168.1.0 0.0.0.255 area 0',
            'network 192.168.2.0 0.0.0.255 area 0',
        ]
    },
    {
        'device_type':'cisco_ios',
        'ip': '172.31.113.4',
        'username': username,
        'password': password,
        'commands': [
            'router ospf 1 vrf control-data',
            'network 192.168.2.0 0.0.0.255 area 0',
            'network 192.168.3.0 0.0.0.255 area 0',
            'default-information originate',
        ]
    }
]
for router in routers:

        connection = ConnectHandler(
            device_type=router['device_type'],
            ip=router['ip'],
            username=router['username'],
            password=router['password']
        )
        
        print(f"กำลังกำหนดค่าเราเตอร์ IP: {router['ip']}")

        # ส่งคำสั่งทีละคำสั่ง
        output = connection.send_config_set(router['commands'])
                
        # แสดงผลลัพธ์
        print(output)
        print('-' * 50)

        connection.disconnect()
    