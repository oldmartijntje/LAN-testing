import socket
import json

# Ask the user for the server IP and port
server_input = input("Enter the server IP and port (in the format 'ip:port'): ")
server_parts = server_input.split(':')

if len(server_parts) == 2:
    server_ip = server_parts[0]
    server_port = int(server_parts[1])
else:
    server_ip = server_input
    server_port = int(input("Enter the server port: "))

# Create a client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# Define a function to send messages to the server
def send_message():
    # Ask the user for the message and recipient
    message = input("Enter the message: ")

    # Send the message to the server
    message_data = {"message": message}
    client_socket.send(json.dumps(message_data).encode())

# Send messages until the user types "quit"
while True:
    send_message()

    # Check for any incoming messages from the server
    message = client_socket.recv(1024).decode()
    if message:
        print(message)
