from netmiko import ConnectHandler
import getpass

def configure_stp_on_switch(switch_info):
    """Configure STP settings on a given switch."""
    try:
        # Establishing a connection to the switch
        net_connect = ConnectHandler(**switch_info)

        # Fetching and displaying the current hostname for clarity
        hostname = net_connect.send_command('show run | include hostname')
        device_name = hostname.split()[-1] if hostname else "Unknown Device"
        print(f"Configuring STP on {device_name}...")

        # Input STP settings from user
        stp_mode = input("Enter STP mode (pvst, rapid-pvst, mstp): ")
        stp_priority = input("Enter STP priority (0-61440 in increments of 4096): ")
        root_bridge = input("Is this the root bridge? (yes/no): ").lower()

        # Configuring STP mode and priority
        commands = [
            f'spanning-tree mode {stp_mode}',
            f'spanning-tree vlan 1 priority {stp_priority if root_bridge == "yes" else "32768"}'
        ]
        
        # Configuring this switch as the root bridge if required
        if root_bridge == "yes":
            commands.append('spanning-tree vlan 1 root primary')

        # Sending configuration commands to the switch
        output = net_connect.send_config_set(commands)
        print(f"STP configuration completed on {device_name}:\n{output}")

        # Optional: configure other VLANs similarly or copy to all VLANs
        additional_vlan_config = input("Configure additional VLANs with these settings? (yes/no): ")
        if additional_vlan_config.lower() == "yes":
            vlan_range = input("Enter VLAN range (e.g., 2-100): ")
            commands = [
                f'spanning-tree vlan {vlan_range} priority {stp_priority if root_bridge == "yes" else "32768"}'
            ]
            output = net_connect.send_config_set(commands)
            print(f"Additional VLAN STP configuration completed on {device_name}:\n{output}")

        net_connect.disconnect()

    except Exception as e:
        print(f"Failed to configure STP on {switch_info['ip']}: {str(e)}")

# Main loop to configure multiple switches
switch_count = int(input("How many switches would you like to configure: "))
while switch_count > 0:
    ip_address = input('Switch IP: ')
    username = input('SSH Username: ')
    password = getpass.getpass('SSH Password: ')

    switch = {
        'device_type': 'cisco_ios',
        'ip': ip_address,
        'username': username,
        'password': password
    }
    configure_stp_on_switch(switch)
    switch_count -= 1

input("Press ENTER to finish.")
