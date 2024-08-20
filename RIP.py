from netmiko import ConnectHandler
from getpass import getpass

router_num = int(input("How many routers would you like to configure: "))

while router_num > 0:
    hostip = input('Router IP: ')
    USER = input('SSH Username: ')
    PASS = getpass('SSH Password: ')  # Securely handle password input

    Router = {
        'device_type': 'cisco_ios',
        'ip': hostip,
        'username': USER,
        'password': PASS
    }

    try:
        myssh = ConnectHandler(**Router)
        # Improved command to get hostname correctly
        hostname_output = myssh.send_command('show run | include hostname')
        if hostname_output:
            device_name = hostname_output.split()[-1]
        else:
            device_name = "Unknown Router"

        # Configure RIP
        print(f"Configuring RIP on {device_name}...")
        rip_commands = [
            'router rip',
            'version 2',
            'no auto-summary'
        ]
        network_num = int(input("How many networks would you like to enable in RIP: "))
        for _ in range(network_num):
            network_i = input('Please specify the network to enable (e.g., 192.168.1.0): ')
            rip_commands.append(f'network {network_i}')

        output = myssh.send_config_set(rip_commands)
        print(f"RIP configuration output for {device_name}:\n{output}")
        print(f'RIP configured successfully on {device_name}')
        print('-' * 79)

    except Exception as e:
        print(f"Failed to configure {hostip}: {str(e)}")

    router_num -= 1

input("Press ENTER to finish")
