from netmiko import ConnectHandler
from netmiko import ConnectHandler, NetmikoAuthenticationException, NetmikoTimeoutException

# Now use ConnectHandler, NetmikoAuthenticationException, and NetmikoTimeoutException in your script


def configure_vlan_on_interface(switch_details, interface, vlan_id, description):
    """Configure VLAN on a specified interface with a description."""
    try:
        # Establish an SSH connection to the switch
        connection = ConnectHandler(**switch_details)
        # Create the commands for configuring the interface
        commands = [
            f"interface {interface}",
            f"description Connected to {description}",
            "switchport mode access",
            f"switchport access vlan {vlan_id}",
            "no shutdown"
        ]
        # Send the configuration commands
        output = connection.send_config_set(commands)
        # Disconnect from the switch
        connection.disconnect()
        return output
    except NetMikoAuthenticationException:
        return "Authentication failed. Please check your username or password."
    except NetMikoTimeoutException:
        return "Connection to device timed out. Please check the IP address and network connectivity."

def main():
    # Collect connection details for the switch
    switch = {
        'device_type': 'cisco_ios',
        'ip': input("Enter switch IP address: "),
        'username': input("Enter your SSH username: "),
        'password': input("Enter your SSH password: "),
        'port': 22  # Standard SSH port, adjust if your setup differs
    }

    # Gather VLAN and interface information
    vlan_id = input("Enter VLAN ID (e.g., 10): ")
    interface = input("Enter the switch interface connected to the router (e.g., Gi0/1): ")
    router_name = input("Enter the name of the router connected to this interface: ")

    # Call the function to configure the VLAN on the specified interface
    result = configure_vlan_on_interface(switch, interface, vlan_id, router_name)
    print("Configuration Result:\n", result)

if __name__ == "__main__":
    main()
