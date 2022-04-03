import socket
import select
import os
import datetime
import pathlib
import logging

#####original links in sources.txt######

#standard ip and port
ip = socket.gethostbyname(socket.gethostname())
port = 1234

# create log date
timeOfLaunch = str(datetime.datetime.now())
#split because there can't be : in a file name
timeOfLaunch = timeOfLaunch.split(":")
#put time back together
timeOfLaunchFixed = f"{timeOfLaunch[0]}.{timeOfLaunch[1]}.{timeOfLaunch[2]}"

#get the programs path
ownPath = pathlib.Path().resolve()

#create log name
LOG_FILENAME = f"{ownPath}/ServerFiles/Logs/log-{timeOfLaunchFixed}.log"

#create ServerFiles folder if it doesn't exist
if not os.path.exists(f'{ownPath}/ServerFiles'):
    os.makedirs(f'{ownPath}/ServerFiles')

#open banlist
if os.path.isfile(f"{ownPath}/ServerFiles/bans.png"):
    ban = open(f"{ownPath}/ServerFiles/bans.png", "r+")
    banlist = ban.read().split(";")
else:
    banlist = list()
    ban = open(f"{ownPath}/ServerFiles/bans.png", "x") 
ban.close()


#open settings if .settings.txt exists
if os.path.isfile(f"{ownPath}/ServerFiles/.Setting.txt"):
    settings = open(f"{ownPath}/ServerFiles/.Setting.txt", "r+")
#rename settings.txt to .settings.txt if settings.txt exists
elif os.path.isfile(f"{ownPath}/ServerFiles/Setting.txt"):
    os.rename(f"{ownPath}/ServerFiles/Setting.txt", f"{ownPath}/ServerFiles/.Setting.txt")
    settings = open(f"{ownPath}/ServerFiles/.Setting.txt", "r+")
#create .settings.txt
else:
    settings = open(f"{ownPath}/ServerFiles/.Setting.txt", "x")
    settings.write("#if you leave empty lines, or with other characters(unless the line starts with #, then it is okay), the program will choose by itself\n#\n#\n#BE AWARE THAT \"True\" AND \"False\" NEED TO HAVE THE FIRST LETTER CAPITALIZED\n#\n#\n#do you want to save logs? then put 'True' on the next line, if not, put 'False' on the next line without a #\nFalse\n#do you want a password? then put 'True' on the next line, if not, put 'False' on the next line without a #\nFalse\n#do you want custom IP adress (will probably do nothing) then put the IP next line (example: 127.0.1.1) if not, type 'False'\nFalse\n#Do you want custom Port? if yes, type the port next line (example: 1234) if not, type 'False'\nFalse")
settings.close()

#check the settings
settings = open(f"{ownPath}/ServerFiles/.Setting.txt", "r")
settingsNotSplitted = settings.read()
#split at every enter
settingsSplitted = settingsNotSplitted.split("\n")
#create list with things that aren't comments
settingsWithoutComments = list()
#for all lines, if the line starts with a # ignore it, else, add it to the list with settings
for x in range(len(settingsSplitted)):
    if settingsSplitted[x][0] != "#":
        settingsWithoutComments.append(settingsSplitted[x])
try:
    #if it's true, create a log file
    if settingsWithoutComments[0] == "True":
        makeLog = True
    else:
        makeLog = False
    #check for password
    password = False
    if settingsWithoutComments[1] != "False":
        password = settingsWithoutComments[1]
    #if not false, use the input as IP adress
    if settingsWithoutComments[2] != "False":
        ip = settingsWithoutComments[2]
    #if not false, use the input as the Port
    if settingsWithoutComments[3] != "False":
        port = settingsWithoutComments[3]
except:
    input(f"There is a problem with \"{ownPath}/ServerFiles/.Setting.txt\" Go fix it, or Delete it\nPress Enter to close")
    exit()



if makeLog == True:
    #create log folder if it doesn't exist
    if not os.path.exists(f'{ownPath}/ServerFiles/Logs'):
        os.makedirs(f'{ownPath}/ServerFiles/Logs')
    #setup log file
    logging.basicConfig(filename=LOG_FILENAME ,level=logging.DEBUG)

#it adds messages to log file
def addToLog(username, message = "", action = 0):
    #check if the settings are set to: pls create a log for me
    if makeLog == True:
        if action == 0:
            logging.info(f"{username} did say \"{message}\"  {datetime.datetime.now()}")
        elif action == 1:
            logging.critical(f"{username} just landed  {datetime.datetime.now()}")
        elif action == 2:
            logging.critical(f"{username} wanted to get the fuck outta here  {datetime.datetime.now()}")
        elif action == 3:
            logging.debug(f"{message} {datetime.datetime.now()}")
        elif action == 4:
            logging.critical(f"{message} {datetime.datetime.now()}")

def commandCheck(check, user, playerList, playerListData):
    command = False
    pingCommand = False
    if check[0] == "/ping":
        customMessage = f"{username} wanted to see who is online: {playerList}"
        #get length of custom message
        customMessageLenght = (str(len(customMessage)))
        #if lengthe of number of lenght not long enough, add spaces
        for x in range(HEADER_LENGTH - len(customMessageLenght)):
            customMessageLenght += " "
        #change things that are needed to send custom message
        message['header'] = customMessageLenght.encode('utf-8')
        message['data'] = customMessage.encode('utf-8')
        #add the ping to the log
        addToLog(username, customMessage, 3)
        #say that it is a ping command
        pingCommand = True
        command = True
    #send password command
    if check[0] == "/password" and password != False:
        if check[1] == password:
            for x in range(len(playerList)):
                if playerList[x] == user:
                    playerListData[x] == "True"
                    addToLog(username, f"{username} entered the password correctly", 3)
                command = True
        else:
            customMessage = f"//kick\\{username}"
            #get length of custom message
            customMessageLenght = (str(len(customMessage)))
            #if lengthe of number of lenght not long enough, add spaces
            for x in range(HEADER_LENGTH - len(customMessageLenght)):
                customMessageLenght += " "
            #change things that are needed to send custom message
            message['header'] = customMessageLenght.encode('utf-8')
            message['data'] = customMessage.encode('utf-8')
            #add the ping to the log
            addToLog(username, f"{username} had the password wrong and got kicked", 3)
            #say that it is a ping command
            pingCommand = True
            command = True
            
    return [command, pingCommand, playerListData], message

def sendPasswordRequest(testForCommand, username, playerList, playerListData):
    customMessage = f"Oda5%%UGqhodajhciiuq3_Voa?zC0Gle1\\{username}"
    #get length of custom message
    customMessageLenght = (str(len(customMessage)))
    #if lengthe of number of lenght not long enough, add spaces
    for x in range(HEADER_LENGTH - len(customMessageLenght)):
        customMessageLenght += " "
    #change things that are needed to send custom message
    message['header'] = customMessageLenght.encode('utf-8')
    message['data'] = customMessage.encode('utf-8')
    #add the ping to the log
    addToLog(username, f"{username} needs to enter the password before he could talk", 3)
    #say that it is a ping command
    pingCommand = True
    command = True
    return [command, pingCommand, playerListData], message

# playerlist
playerList = list()
playerListData = list()

HEADER_LENGTH = 10

IP = ip
PORT = port
# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# SO_ - socket option
# SOL_ - socket option level
# Sets REUSEADDR (as a socket option) to 1 on socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind, so server informs operating system that it's going to use given IP and port
# For a server using 0.0.0.0 means to listen on all available interfaces, useful to connect locally to 127.0.0.1 and remotely to LAN interface IP
server_socket.bind((IP, PORT))

# This makes server listen to new connections
server_socket.listen()

# List of sockets for select.select()
sockets_list = [server_socket]

# List of connected clients - socket as a key, user header and name as data
clients = {}

print(f'Listening for connections on {IP}:{PORT}...')

# Handles message receiving
def receive_message(client_socket):

    try:

        # Receive our "header" containing message length, it's size is defined and constant
        message_header = client_socket.recv(HEADER_LENGTH)
        # If we received no data, client gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
        if not len(message_header):
            return False

        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())
        # Return an object of message header and message data
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:

        # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
        # or just lost his connection
        # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
        # and that's also a cause when we receive an empty message
        return False


while True:

    # Calls Unix select() system call or Windows select() WinSock call with three parameters:
    #   - rlist - sockets to be monitored for incoming data
    #   - wlist - sockets for data to be send to (checks if for example buffers are not full and socket is ready to send some data)
    #   - xlist - sockets to be monitored for exceptions (we want to monitor all sockets for errors, so we can use rlist)
    # Returns lists:
    #   - reading - sockets we received some data on (that way we don't have to check sockets manually)
    #   - writing - sockets ready for data to be send thru them
    #   - errors  - sockets with some exceptions
    # This is a blocking call, code execution will "wait" here and "get" notified in case any action should be taken
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)


    # Iterate over notified sockets
    for notified_socket in read_sockets:

        # If notified socket is a server socket - new connection, accept it
        if notified_socket == server_socket:
            if os.path.isfile(f"{ownPath}/ServerFiles/bans.png"):
                log = open(f"{ownPath}/ServerFiles/bans.png", "r+")
                banlist = log.read().split(";")
            else:
                banlist = list()
                log = open(f"{ownPath}/ServerFiles/bans.png", "x") 
            log.close()
            # Accept new connection
            # That gives us new socket - client socket, connected to this given client only, it's unique for that client
            # The other returned object is ip/port set
            client_socket, client_address = server_socket.accept()
            if client_address[0] in banlist:
                client_socket.close()
            # Client should send his name right away, receive it
            user = receive_message(client_socket)
            
            # If False - client disconnected before he sent his name
            if user is False:
                continue

            # Add accepted socket to select.select() list
            sockets_list.append(client_socket)


            clients[client_socket] = user
            
            # save user to the user list
            playerList.append(user['data'].decode('utf-8'))
            playerListData.append("False")
            # Also save username and username header
            print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))
            addToLog(user['data'].decode('utf-8'), "", action = 1)
            
        # Else existing socket is sending a message
        else:

            # Receive message
            message = receive_message(notified_socket)

            


            # If False, client disconnected, cleanup
            if message is False:
                
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                addToLog(clients[notified_socket]['data'].decode('utf-8'), "", action = 2)

                # remove user from user list
                try:
                    for x in range(len(playerList)):
                        if playerList[x] == clients[notified_socket]['data'].decode('utf-8'):
                            playerListData.pop(x)
                    playerList.remove(clients[notified_socket]['data'].decode('utf-8'))
                except:
                    e = 0
                # Remove from list for socket.socket()
                sockets_list.remove(notified_socket)

                # Remove from our list of users
                del clients[notified_socket]

                continue

            # Get user by notified socket, so we will know who sent the message
            user = clients[notified_socket]
            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
            #define the pingcommand
            pingCommand = False
            #define username
            username = user['data'].decode('utf-8')
            #check if it is a command
            testForCommand = message["data"].decode("utf-8").split("\\")
            #check for commands
            returnedValues, message = commandCheck(testForCommand, username, playerList, playerListData)
            #say if there was a command    
            if returnedValues[0] == False:
                passwordEntered = False
                addToLog(username, f'{message["data"].decode("utf-8")}', 0)
                for x in range(len(playerList)):
                    if playerList[x] == username:
                        #print(playerListData)
                        if playerListData[x] == "True" or password == False:
                            passwordEntered = True
                            #print("false")
                        else:
                            returnedValues, message = sendPasswordRequest(testForCommand, username, playerList, playerListData)
                            pingCommand = True
                            #print("true")
                        
            pingCommand = returnedValues[1]
            playerListData = returnedValues[2]
            
            # Iterate over connected clients and broadcast message
            for client_socket in clients:
    
                # But don't sent it to sender unless it is a ping command
                if client_socket != notified_socket or pingCommand == True:
    
                    # Send user and message (both with their headers)
                    # We are reusing here message header sent by sender, and saved username header send by user when he connected
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
                
                
                
                
    # It's not really necessary to have this, but will handle some socket exceptions just in case
    for notified_socket in exception_sockets:

        # Remove from list for socket.socket()
        sockets_list.remove(notified_socket)

        # Remove from our list of users
        del clients[notified_socket]