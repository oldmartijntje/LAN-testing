#server.py
import threading
import socket
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def inputInt(text, feedback="that is not a number"):
    test = 1
    while test == 1:
        potentialNumber = input(text)
        try:
            number = int(potentialNumber)
            test = 0
        except:
            print(feedback)
    return number
ip = socket.gethostbyname(socket.gethostname())
portNumber = 1234
print(f"{ip}:{portNumber}")
PORT = portNumber
ADDRESS = ip
my_socket.bind((ADDRESS, PORT))
my_socket.listen()
client, client_address = my_socket.accept()
# Instead of receiving only one message, let's make an infinite loop
while True:
    result = client.recv(1024)
    print(result.decode())