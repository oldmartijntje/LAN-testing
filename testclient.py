import socket
import select
import errno
import sys
import os
import webbrowser

#original links in sources.txt

#list
commandList = ['//kick', '//ban', "//webBrowsingBoii", "/msg", "//rickyricky"]

def getIp():
    loop = True
    while loop == True:
        ipadressAndPort = input("input the IP\n").split(":")
        
        if "." in ipadressAndPort[0]:
            ip = ipadressAndPort[0]
            try:
                port = int(ipadressAndPort[1])
            except:
                port = 1234
            loop = False
        else:
            print("please try again")
        return ip,port
HEADER_LENGTH = 10
ip, port = getIp()
IP = ip
PORT = port
my_username = input("Username: ")

def doACommand(command,message,username,my_username):


    # check a command and use it
    # kick command
    if command[0] == commandList[0]:
        if command[1] == my_username:
            exit()
    # ban command
    elif command[0] == commandList[1]:
        if command[1] == my_username:
            ban = open("bans.png", "r+")
            banList = ban.read()
            banList += f";{socket.gethostbyname(socket.gethostname())}"
            ban.truncate(0)
            ban.seek(0)
            ban.write(banList)
            ban.close()
            exit()
    elif command[0] == commandList[2]:
        if command[1] == my_username:
            webbrowser.open(command[2])
    elif command[0] == commandList[4]:
        if command[1] == my_username:
            webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")



    # private message 
    if command[0] == commandList[3]:
        if command[1] == my_username:
            print(f"{username} whispered: \"{command[2]}\" to you")

# do a command you just sent
def doACommandYourself(command,message,my_username):

    # kick command
    if command[0] == commandList[0]:
        if command[1] == my_username:
            # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
            message = f"{my_username} kicked himself".encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(message_header + message)
            exit()




    # private message 
    if command[0] == commandList[3]:
        if command[1] == my_username:
            print(f"you whispered: \"{command[2]}\" to {command[1]}")

# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a given ip and port
client_socket.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
client_socket.setblocking(False)

# Prepare username and header and send them
# We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

while True:

    # Wait for user to input a message
    message = input(f'{my_username} > ')
    command = message.split(".")
    if command[0] in commandList:
        doACommandYourself(command,message,my_username)

    # If message is not empty - send it
    if message:

        # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

    try:
        # Now we want to loop over received messages (there might be more than one) and print them
        while True:

            # Receive our "header" containing username length, it's size is defined and constant
            username_header = client_socket.recv(HEADER_LENGTH)

            # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())

            # Receive and decode username
            username = client_socket.recv(username_length).decode('utf-8')

            # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            # Print message
            command = message.split(".")
            if command[0] in commandList:
                doACommand(command,message,username,my_username)
            else:
                print(f'{username} > {message}')

    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        # We just did not receive anything
        continue

    except Exception as e:
        # Any other exception - something happened, exit
        print('Reading error: '.format(str(e)))
        sys.exit()