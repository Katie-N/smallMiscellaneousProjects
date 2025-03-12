import socket
import sys
from datetime import datetime, timezone
import time

def cause_timeout(timeout):
    time.sleep(timeout+1)

# Server
def server_program(port):
    host = socket.gethostname()
    
    if (port < 5000):
        print("Invalid port. Choose something over 5000")
        return -1

    # Create the server side socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Only the server needs to bind to the port so it can keep listening. 
    # The client will get its response through the socket and doesn't need to bind to a port to do so. 
    server_socket.bind((host, port))
    print("Server listening on " + str(host) + ":" + str(port))

    # Receive from the socket directly in UDP since there are no connections
    # Also UDP packets have both the message and the source address so we know where to respond
    # Note that client_address is NOT the second parameter in sendto(). I got confused by this.
    # But it is the address the request is coming from while the second parameter in sendto() 
    # is the address the request is going to (which is the address of this server)
    request, client_address = server_socket.recvfrom(1024)
    addressString = str(client_address[0]) + ":" + str(client_address[1])
    print("Received request from " + addressString)
    if (request.decode() == "time?"):
        data = datetime.now(timezone.utc)

        # UDP can still respond to the request by utilizing the address of the sender.
        # TCP doesn't worry about this address because it already has an open connection it can use to reply.
        
        # I used this to test if the client handles timeouts from the server.
        # cause_timeout(5)

        server_socket.sendto(str(data).encode(), client_address)
        print("Sent response to " + addressString)


    # Close the connection
    server_socket.close()

def main():
    if (len(sys.argv) == 1):
        print("Enter the port to connect to!")
        return -1
    if (sys.argv[1].isnumeric()):
        server_program(int(sys.argv[1]))

if __name__ == '__main__':
    main()
