from netmiko import ConnectHandler
from jinja2 import Environment, FileSystemLoader
import yaml
import os

# Define the paths to the template and data file
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
# DATA_FILE = os.path.join(BASE_DIR, 'data', 'config.yml')

# Load the Jinja2 template
loader = FileSystemLoader('templates')
env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
template = env.get_template("router-nat.j2")

# Load the YAML data
with open("data/routers-nat.yml", 'r') as f:
    config_data = yaml.safe_load(f)

# Render the configuration from the template and data
config_output = template.render(config_data)

# Define device details
device = {
    'device_type': 'cisco_ios',  # Adjust based on your device type
    'host': '172.31.113.4',  # Replace with your device's management IP
    'username': os.environ.get('TELNET_USER'),  # Replace with your device's username
    'password': os.environ.get('TELNET_PASSWORD'),  # Replace with your device's password
}

# Establish connection to the device
net_connect = ConnectHandler(**device)

# Enter enable mode
net_connect.enable()

# Send the configuration to the device
output = net_connect.send_config_set(config_output.split('\n'))

# Print the output
print(output)

# Save the configuration
net_connect.save_config()

# Disconnect from the device
net_connect.disconnect()