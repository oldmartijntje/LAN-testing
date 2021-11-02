import socket
import select
import errno
import sys

# original links in sources.txt

# admin
listOfAdmins = list()

# commands
commandList = ['//kick', '//ban', "//google", "//claimAdmin", "//addAdmin", "//removeAdmin", "/msg"]

# it is the ip input
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

# do a command you receive
def doACommand(command,message,username,my_username):
    if len(listOfAdmins) > 0:
        if username in listOfAdmins:
            # check a command and use it
            # kick command
            if command[0] == commandList[0]:
                if command[1] == my_username:
                    message = f"//removeAdmin.{my_username}".encode('utf-8')
                    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                    client_socket.send(message_header + message)
                    exit()
            # ban command
            elif command[0] == commandList[1]:
                if command[1] == my_username:
                    message = f"//removeAdmin.{my_username}".encode('utf-8')
                    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                    client_socket.send(message_header + message)
                    exit()
            # add admin 
            elif command[0] == commandList[4]:
                if command[1] not in listOfAdmins:
                    listOfAdmins.append(command[1])
                    if command[1] == my_username:
                        print(f"{username} gave you admin powers")
            # remove admin 
            elif command[0] == commandList[5]:
                if command[1] in listOfAdmins:
                    listOfAdmins.remove(command[1])
                    if command[1] == my_username:
                        print(f"{username} revoked your admin powers")


    # make person admin if there is none            
    elif command[0] == commandList[3]:
        listOfAdmins.append(username)
    # private message 
    if command[0] == commandList[6]:
        if command[1] == my_username:
            print(f"{username} whispered: \"{command[2]}\" to you")

# do a command you just sent
def doACommandYourself(command,message,my_username):
    if len(listOfAdmins) > 0:
        if username in listOfAdmins:
            # check a command and use it
            # kick command
            if command[0] == commandList[0]:
                if command[1] == my_username:
                    # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
                    message = f"//removeAdmin.{my_username}".encode('utf-8')
                    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                    client_socket.send(message_header + message)
                    exit()
            # add admin 
            elif command[0] == commandList[4]:
                if command[1] not in listOfAdmins:
                    listOfAdmins.append(command[1])
                    print(f"you gave {command[1]} their admin powers")
            # remove admin 
            elif command[0] == commandList[5]:
                if command[1] in listOfAdmins:
                    listOfAdmins.remove(command[1])
                    print(f"you revoked {command[1]} their admin powers")


    # make person admin if there is none            
    elif command[0] == commandList[3]:
        listOfAdmins.append(username)
        print(f"you are now admin")
    # private message 
    if command[0] == commandList[6]:
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
    # If message is not empty - send it
    if message:

        # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
        message = str(message+"<>"+my_username).encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

    if command[0] in commandList:
        doACommandYourself(command,message,my_username)
    try:
        # Now we want to loop over received messages (there might be more than one) and print them
        while True:

            try:
                result = client_socket.recv(1024)
                listOfAdmins = (result.decode())
            except:
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
            #remove the user from the message
            messageList = message.split("<>")
            # checks if it is an command
            command = messageList[0].split(".")
            if command[0] in commandList:
                doACommand(command,messageList,username,my_username)
            # Print message
            else:
                print(f'{username} > {messageList[0]}')

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