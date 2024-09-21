import textfsm
from netmiko import ConnectHandler

# Function to normalize interface name
def normalize_interface(interface_name):
    interface_name = interface_name.lower().replace(" ", "")
    if  interface_name.startswith("gigabitethernet"):
        return "GigabitEthernet" + interface_name[15:]
    elif interface_name.startswith("giga"):
        return "GigabitEthernet" + interface_name[4:]
    elif interface_name.startswith("g"):
        return "GigabitEthernet" + interface_name.split('g')[-1]
    elif interface_name.startswith("f"):
        return "FastEthernet" + interface_name.split('f')[-1]
    
    # If no match, return the original input
    return interface_name

# # Function to normalize interface name
# def normalize_interface(interface_name):
#     interface_name = interface_name.lower().replace(" ", "")
    
#     if "gigabit" in interface_name:
#         # Look for GigabitEthernet
#         parts = interface_name.split("gigabit")
#         if len(parts) > 1:
#             return "GigabitEthernet" + parts[1]
#     elif "giga" in interface_name:
#         # Handle cases like "giga0/1"
#         return "GigabitEthernet" + interface_name.split("giga")[-1]
#     elif "g" in interface_name:
#         # Handle cases like "g0/1"
#         return "GigabitEthernet" + interface_name.split("g")[-1]
#     elif "f" in interface_name:
#         # Handle FastEthernet
#         return "FastEthernet" + interface_name.split("f")[-1]
    
#     # If no match, return the original input
#     return interface_name

# Example router connection details
router = {
    "device_type": "cisco_ios",
    "ip": "172.31.113.4",
    "username": "admin",
    "password": "cisco"
}

# User input for interface name
user_interface = input("Enter interface (e.g., GigabitEthernet 0/1, g0/1, giga0/1): ").strip()

# Normalize the user input
normalized_interface = normalize_interface(user_interface)

# Establish connection to the router
connection = ConnectHandler(**router)
connection.enable()
output = connection.send_command("show ip int brief")
connection.disconnect()

# Use the TextFSM template to parse output
template_file = "/home/devasc/.local/lib/python3.8/site-packages/ntc_templates/templates/cisco_ios_show_ip_interface_brief.textfsm"
with open(template_file) as template:
    fsm = textfsm.TextFSM(template)
    result = fsm.ParseText(output)

# Check for matching interface and print the IP address and status
found = False
for row in result:
    interface_name = row[0]  # Interface name
    ip_address = row[1]      # IP address
    status = row[2]          # Status
    
    if normalized_interface.lower() == interface_name.lower():
        print(f"Interface: {interface_name}, IP Address: {ip_address}, Status: {status}")
        found = True
        break

if not found:
    print(f"Interface {user_interface} not found.")