# import warnings

# # Suppress all deprecation warnings
# warnings.simplefilter('ignore', category=DeprecationWarning)

# from netmiko import ConnectHandler

# # Collect the number of switches to configure
# switch_num = int(input("How many switches would you like to configure: "))

# # Collect common credentials
# USER = input('SSH Username: ')
# PASS = input('SSH Password: ')

# # Process each switch
# while switch_num > 0:
#     # Collect each switch's IP address
#     hostip = input('Switch IP: ')

#     # Define the device dictionary
#     switch = {
#         'device_type': 'cisco_ios',  # Ensure this matches your switch type in EVE-NG
#         'ip': hostip,
#         'username': USER,
#         'password': PASS
#     }

#     # Establish an SSH connection to the switch
#     try:
#         myssh = ConnectHandler(**switch)
#         hostname = myssh.send_command('show run | include hostname')
#         hostname = hostname.split()  # Example output: "hostname SwitchName"

#         if len(hostname) > 1:
#             device = hostname[1]
#             print(f'Configuring VLANs on {device}')
#         else:
#             raise ValueError("Hostname not found in the output.")

#         # Configuring VLANs from 2 to 100
#         vlan_config = []
#         for vlan_id in range(11):
#             vlan_config.append(f'vlan {vlan_id}')
#             vlan_config.append(f'name VLAN_{vlan_id}')

#         # Sending VLAN configuration
#         output = myssh.send_config_set(vlan_config)
#         print(output)

#         print(f'Configured VLANs on {device}')

#     except Exception as e:
#         print(f'Failed to configure {hostip}: {str(e)}')

#     finally:
#         # Decrease the counter and ensure to close the SSH session
#         switch_num -= 1
#         if 'myssh' in locals():
#             myssh.disconnect()

# input('Press ENTER To Continue')



# //////////////////////////////////////////////////////////////////////////////////// 


import warnings
from netmiko import ConnectHandler

# Suppress all deprecation warnings
warnings.simplefilter('ignore', category=DeprecationWarning)

# Collect the number of switches to configure
switch_num = int(input("How many switches would you like to configure: "))

# Collect common credentials
USER = input('SSH Username: ')
PASS = input('SSH Password: ')

# Process each switch
while switch_num > 0:
    # Collect each switch's IP address
    hostip = input('Switch IP: ')

    # Define the device dictionary
    switch = {
        'device_type': 'cisco_ios',  # Ensure this matches your switch type in EVE-NG
        'ip': hostip,
        'username': USER,
        'password': PASS
    }

    # Establish an SSH connection to the switch
    try:
        myssh = ConnectHandler(**switch)
        hostname = myssh.send_command('show run | include hostname')
        hostname = hostname.split()  # Example output: "hostname SwitchName"

        if len(hostname) > 1:
            device = hostname[1]
            print(f'Configuring VLANs on {device}')
        else:
            raise ValueError("Hostname not found in the output.")

        # Ask user for VLAN creation mode
        mode = input("Enter 'single' to configure one VLAN or 'range' to configure a range of VLANs: ").strip().lower()
        vlan_config = []
        if mode == 'single':
            vlan_id = input("Enter VLAN ID to create (e.g., 10): ")
            vlan_config.append(f'vlan {vlan_id}')
            vlan_config.append(f'name VLAN_{vlan_id}')
        elif mode == 'range':
            start_vlan = int(input("Enter the starting VLAN ID (e.g., 10): "))
            end_vlan = int(input("Enter the ending VLAN ID (e.g., 20): "))
            for vlan_id in range(start_vlan, end_vlan + 1):
                vlan_config.append(f'vlan {vlan_id}')
                vlan_config.append(f'name VLAN_{vlan_id}')

        # Sending VLAN configuration
        output = myssh.send_config_set(vlan_config)
        print(output)

        print(f'Configured VLANs on {device}')

    except Exception as e:
        print(f'Failed to configure {hostip}: {str(e)}')

    finally:
        # Decrease the counter and ensure to close the SSH session
        switch_num -= 1
        if 'myssh' in locals():
            myssh.disconnect()

input('Press ENTER To Continue')
