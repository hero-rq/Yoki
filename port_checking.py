import socket

# Function to collect ports
def collect_ports():
    ports = []
    while True:
        user_input = input("Enter a port number (or type any alphabet to finish): ")
        if user_input.isalpha():
            break
        try:
            ports.append(int(user_input))
        except ValueError:
            print("Please enter a valid integer.")
    return ports

# Function to scan ports
def port_scanner(target_ip, ports):
    open_ports = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Set timeout to 1 second
        try:
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                open_ports.append(port)
        except Exception as e:
            print(f"Error scanning port {port}: {e}")
        finally:
            sock.close()
    return open_ports

# Main execution
if __name__ == "__main__":
    target_ip = input("Enter the target IP: ")
    target_ports = collect_ports()
    open_ports = port_scanner(target_ip, target_ports)
    
    if open_ports:
        print(f"Open Ports: {open_ports}")
    else:
        print("No open ports found.")
