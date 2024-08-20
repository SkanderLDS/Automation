import warnings
from netmiko import ConnectHandler

# Suppress all warnings, specifically deprecation warnings
warnings.simplefilter('ignore', category=DeprecationWarning)

def configure_device(device):
    """Function to send configuration commands to a Cisco device."""
    commands = [
        "no ip domain-lookup",
        "ip domain-name eve.com",
        "ip ssh version 2",
        "crypto key generate rsa modulus 1024",
        "vrf definition MGMT",
        "address-family ipv4",
        "exit"
    ]
    
    # Start an SSH session with the device
    with ConnectHandler(**device) as net_connect:
        net_connect.enable()
        
        # Send configuration commands
        output = net_connect.send_config_set(commands)
        print("Base configurations applied, output:")
        print(output)
        
        # Configure interface
        interface = input("Enter interface to configure (e.g., Gi0/0): ")
        ip_address = input(f"Enter IP address and subnet mask for {interface} (e.g., 192.168.1.1 255.255.255.0): ")
        int_commands = [
            f"interface {interface}",
            f"ip address {ip_address}",
            "vrf forwarding MGMT",
            "no shutdown"
        ]
        
        # Send interface configuration commands
        output = net_connect.send_config_set(int_commands)
        print(f"Interface {interface} configured, output:")
        print(output)

def main():
    # Ask for the IP address of the router to configure
    router_ip = input("Enter the IP address of the router you want to configure: ")

    # Device connection details
    device = {
        'device_type': 'cisco_ios',
        'ip': router_ip,
        'username': input("Enter SSH username: "),
        'password': input("Enter SSH password: "),
        'port': 22,  # Standard SSH port
        'secret': input("Enter enable secret: ")  # Needed for enable mode
    }

    # Call the configuration function
    configure_device(device)

    print("Configuration complete.")

if __name__ == "__main__":
    main()
