import socket

def get_ip_address(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.error as e:
        return f"Error: {e}"

# Example usage:
domain = input("Enter a domain: ")
ip_address = get_ip_address(domain)

print(f"The IP address of {domain} is: {ip_address}")
