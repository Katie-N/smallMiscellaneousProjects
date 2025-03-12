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
    if (len(sys.argv) > 3 and sys.argv[3] == "True"):
        rtt = True
    else:
        rtt = False

    if (port < 5000):
        print("Invalid port. Choose something over 5000")
        return -1
    
    # setup the client side socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (host, port)
    addressString = str(host) + ":" + str(port)
    print("Connected to socket at " + addressString)

    # UDP should have timeouts since it is doesnt use ACKs. 
    client_socket.settimeout(5)

    # We will just use the word "time?" to ask the server what time it is
    message = "time?"
    # Get the current time just before sending the packet
    time_sent = datetime.now(timezone.utc)

    # Send the request. 
    # sendto takes the message and the address to send to.
    client_socket.sendto(message.encode(), server_address)
    print("Sent request to " + addressString)
    try:
        # Receive the response from the server
        data, server_address = client_socket.recvfrom(1024)
        time_response_received = datetime.now(timezone.utc)
        print("Response received from " + addressString)
        data = data.decode()
    except socket.timeout:
        print("Timed out: The server took too long to respond or the response was dropped along the way")
        return -1
    
    # Print the results
    print("-"*50)
    datetime_format = "%Y-%m-%d %H:%M:%S.%f%z"
    time_received_by_server = datetime.strptime(data, datetime_format)
    print("Time Sent: " + str(time_sent))
    print("Time Received by Server: " + str(time_received_by_server))
    # Extract the milliseconds by multiplying the seconds by 1000
    # We have to use total_seconds() instead of just seconds because we want to preserve the fractions of seconds
    print("Latency: " + str((time_received_by_server - time_sent).total_seconds() * 1000))

    if (rtt):
        print("RTT = " + str((time_response_received - time_sent).total_seconds() * 1000))

    client_socket.close()

def main():
    if (len(sys.argv) < 3):
        print("Enter the ip address and port to connect to!")
        return -1
    if (sys.argv[2].isnumeric() and valid_ip(sys.argv[1])):
        client_program(int(sys.argv[2]), sys.argv[1])

if __name__ == '__main__':
    main()