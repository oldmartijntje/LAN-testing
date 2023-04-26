import socket
import json

def send_message(username, message):
    # create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # get local machine name
    host = socket.gethostname()
    
    # define the port on which you want to connect
    port = 1234
    
    # connect to the server on local machine
    client_socket.connect((host, port))
    
    # create message dictionary
    message_dict = {"username": username, "message": message}
    
    # convert message dictionary to json string
    message_json = json.dumps(message_dict)
    
    # send message to the server
    client_socket.send(message_json.encode('utf-8'))
    
    # receive data from the server
    data = client_socket.recv(1024)
    
    # decode data from bytes to string
    response = data.decode('utf-8')
    
    # print the response from the server
    print("Response from server: ", response)
    
    # close the client socket
    client_socket.close()

# example usage
my_username = "Alice"
my_message = "Hello, World!"
send_message(my_username, my_message)
