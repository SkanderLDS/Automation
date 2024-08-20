from netmiko import ConnectHandler

# Define the device connection details
device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.192.21',  # Replace with your switch's IP address
    'username': 'skander',  # Replace with your SSH username
    'password': 'mypasss',  # Replace with your SSH password
    'port': 22  # Default SSH port
}

# VLANs to delete: specifying a range from 20 to 100
vlan_ids_to_delete = range(2, 11)  # This creates a list from 20 to 100

try:
    # Establish SSH connection to the device
    myssh = ConnectHandler(**device)
    hostname = myssh.send_command('show run | include hostname')
    hostname = hostname.split()
    
    if len(hostname) > 1:
        device_name = hostname[1]
        print(f'Deleting VLANs on {device_name}')
        
        # Delete VLANs
        vlan_delete_commands = [f'no vlan {vlan_id}' for vlan_id in vlan_ids_to_delete]
        output = myssh.send_config_set(vlan_delete_commands)
        print(output)
        
        # Verify VLAN deletion
        print('Verifying VLAN deletion...')
        vlan_brief = myssh.send_command('show vlan brief')
        print(vlan_brief)
        
        print(f'Deleted VLANs on {device_name}')
    
except Exception as e:
    print(f'Failed to delete VLANs on {device["ip"]}: {str(e)}')

finally:
    if 'myssh' in locals():
        myssh.disconnect()
