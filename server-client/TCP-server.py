import socket
import sys
from datetime import datetime, timezone

# Server
def server_program(port):
    host = socket.gethostname()
    
    if (port < 5000):
        print("Invalid port. Choose something over 5000")
        return -1

    # Create the server side socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Server listening on " + str(host) + ":" + str(port))

    # When a connection comes in
    conn, address = server_socket.accept()
    addressString = str(address[0]) + ":" + str(address[1])
    print("Connection from " + addressString)

    try:
        request = conn.recv(1024).decode()
        print("Received request from " + addressString)

        if (request == "time?"):
            data = datetime.now(timezone.utc)
            conn.send(str(data).encode())
            print("Sent response to " + addressString)

    except ConnectionResetError or BrokenPipeError:
        # Some error detection
        print("Client disconnected")
    finally:
        # Close the connection
        conn.close()

def main():
    if (len(sys.argv) == 1):
        print("Enter the port to connect to!")
        return -1
    if (sys.argv[1].isnumeric()):
        server_program(int(sys.argv[1]))

if __name__ == '__main__':
    main()
