import socket
import threading
loop = True
while loop == True:
    ipadress = input("input the IP")
    portTest = input("input the port (if u say nothing it takes default port)")
    if "." in ipadress:
        ip = ipadress
        try:
            port = portTest
        except:
            port = 808
        loop = False
    else:
        print("please try again")
    
    
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT = port
ADDRESS = ip # Same as "127.0.1.1"
my_socket.connect((ADDRESS, PORT))
while True:
    message_to_send = input("Enter your message : ")
    my_socket.send(message_to_send.encode())