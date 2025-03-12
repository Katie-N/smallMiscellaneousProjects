import socket
import sys
from datetime import datetime, timezone
import ipaddress

def valid_ip(ip_str):
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False

# Client
def client_program(port, host):
    
    if (port < 5000):
        print("Invalid port. Choose something over 5000")
        return -1

    # setup the client side socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # We will just use the word "time?" to ask the server what time it is
    message = "time?"
    # Get the current time just before sending the packet
    time_sent = datetime.now(timezone.utc)
    # Send the request
    client_socket.send(message.encode())
    # Receive the response from the server
    data = client_socket.recv(1024).decode()
    
    datetime_format = "%Y-%m-%d %H:%M:%S.%f%z"
    time_received_by_server = datetime.strptime(data, datetime_format)
    print("Time Sent: " + str(time_sent))
    print("Time Received by Server: " + str(time_received_by_server))
    # Extract the milliseconds by multiplying the seconds by 1000
    # We have to use total_seconds() instead of just seconds because we want to preserve the fractions of seconds
    print("Latency: " + str((time_received_by_server - time_sent).total_seconds() * 1000))

    client_socket.close()

def main():
    if (len(sys.argv) != 3):
        print("Enter the ip address and port to connect to!")
        return -1
    if (sys.argv[2].isnumeric() and valid_ip(sys.argv[1])):
        client_program(int(sys.argv[2]), sys.argv[1])

if __name__ == '__main__':
    main()