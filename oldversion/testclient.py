import socket
import errno
import sys
import os
import webbrowser
import datetime
import pathlib
import logging
extention = False
try:
    from loggingExtention import *
    extention = True
except:
    extention = False
#plugin support
try:
    from pluginHandler import *
except:
    pluginSupport = False

passwordInfo = [False, "missing key", 0, False]
pendingMessages = list()
# create log date
timeOfLaunch = str(datetime.datetime.now())
#split because there can't be : in a file name
timeOfLaunch = timeOfLaunch.split(":")
#put time back together
timeOfLaunchFixed = f"{timeOfLaunch[0]}.{timeOfLaunch[1]}.{timeOfLaunch[2]}"

#get the programs path
ownPath = pathlib.Path().resolve()
#create log folder if it doesn't exist
if not os.path.exists(f'{ownPath}/ClientFiles'):
    os.makedirs(f'{ownPath}/ClientFiles')

#list
commandList = ['//kick', '//ban', "/web", "/msg", "/rickroll", "/ping", "//plugin", "Oda5%%UGqhodajhciiuq3_Voa?zC0Gle1"]

#open settings if .settings.txt exists
if os.path.isfile(f"{ownPath}/ClientFiles/.Setting.txt"):
    settings = open(f"{ownPath}/ClientFiles/.Setting.txt", "r+")
#rename settings.txt to .settings.txt if settings.txt exists
elif os.path.isfile(f"{ownPath}/ClientFiles/Setting.txt"):
    os.rename(f"{ownPath}/ClientFiles/Setting.txt", f"{ownPath}/ServerFiles/.Setting.txt")
    settings = open(f"{ownPath}/ClientFiles/.Setting.txt", "r+")
#create .settings.txt
else:
    settings = open(f"{ownPath}/ClientFiles/.Setting.txt", "x")
    settings.write("#if you leave empty lines, or with other characters(unless the line starts with #, then it is okay), the program will choose by itself\n#\n#\n#BE AWARE THAT \"True\" AND \"False\" NEED TO HAVE THE FIRST LETTER CAPITALIZED\n#\n#\n#do you want to save logs? then put 'True' on the next line, if not, put 'False' on the next line without a #\nFalse\n#do you want to automatically set the IP adress, then put the IP next line (example: 127.0.1.1) if not, type 'False'\nFalse\n#Do you want to automatically enter a custom Port? if yes, type the port next line (example: 1234) if not, type 'False'\nFalse")
    settings.write("\n#if you want to use the same name automatically, type it here, otherwise, type \"False\"\nFalse")
settings.close()

#check the settings
settings = open(f"{ownPath}/ClientFiles/.Setting.txt", "r")
settingsNotSplitted = settings.read()
#split at every enter
settingsSplitted = settingsNotSplitted.split("\n")
#create list with things that aren't comments
settingsWithoutComments = list()
#for all lines, if the line starts with a # ignore it, else, add it to the list with settings
for x in range(len(settingsSplitted)):
    try:
        if settingsSplitted[x][0] != "#":
            settingsWithoutComments.append(settingsSplitted[x])
    except:
        input(f"There is a problem with \"{ownPath}/ClientFiles/.Setting.txt\" Go fix it, or Delete it\nPress Enter to close")
        exit()
ipAndPortConfig = [False,False]
#check if u want logging
if settingsWithoutComments[0] == "False":
    if extention == True:
        extention = False
#check if custom ip
if settingsWithoutComments[1] != "False":
    ipAndPortConfig[0] = settingsWithoutComments[1]
#check if custom port
if settingsWithoutComments[2] != "False":
    ipAndPortConfig[1] = settingsWithoutComments[2]
    try: ipAndPortConfig[1] = int(ipAndPortConfig[1])
    except: ipAndPortConfig[1] = False
my_username = ""
if settingsWithoutComments[3] != "False":
    if settingsWithoutComments[3] != "":
        my_username = settingsWithoutComments[3]
    else:
        my_username = "theDipshitThatLeftTheLineInTheConfigEmpty"


def getIp(configFiles):
    if configFiles[0] != False:
        ip = configFiles[0]
        if configFiles[1] != False:
            port = configFiles[1]
        else:
            loop = True
            while loop == True:
                port = input("input the Port\n").split(":")
                if port != "":
                    loop = False
    else:      

        loop = True
        while loop == True:
            ipadressAndPort = input("input the IP\n").split(":")
            
            if "." in ipadressAndPort[0]:
                ip = ipadressAndPort[0]
                try:
                    port = int(ipadressAndPort[1])
                except:
                    if configFiles[1] != False:
                        port = configFiles[1]
                    else:
                        port = 1234
                loop = False
            else:
                print("please try again")
    return ip,port
HEADER_LENGTH = 10
ip, port = getIp(ipAndPortConfig)
IP = ip
PORT = port
if my_username == "":
    my_username = input("Username: ")

def doACommand(command,message,username,my_username, message_header, username_header, passwordInfo):
    passwordInfo[2] += 1
    extention = "None"
    shotdown = False
    try:
        # check a command and use it
        # kick command
        #print(message)
        #print(command)
        if command[0] == commandList[0]:
            if command[1] == my_username:
                shotdown = True
                sys.exit()
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
                shotdown = True
                sys.exit()
        #web
        elif command[0] == commandList[2]:
            if command[1] == my_username or command[1] == "@all": 
                if extention == True:         
                    try:
                        google(command,message,username,my_username, commandList, timeOfLaunchFixed)
                        extention = True
                    except:
                        extention = False
                if "http" in command[2] and "/" in command[2] and "." in command[2] and ":" in command[2]:
                    webbrowser.open(command[2])
                elif extention == False:
                    webbrowser.open("https://www.google.com/search?client=opera-gx&q="+command[2]+"&sourceid=opera&ie=UTF-8&oe=UTF-8")
        #rickroll
        elif command[0] == commandList[4]:
            if extention == True:
                try:
                    google(command,message,username,my_username, commandList, timeOfLaunchFixed)
                    extention = True
                except:
                    extention = False
            if (command[1] == my_username or command[1] == "@all") and extention == False:
                webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        #plugin
        elif command[0] == commandList[6]:
            if pluginSupport == True:
                plugin(command, message, my_username, username, message_header, username_header)
        #password
        elif command[0] == commandList[7]:
            if command[1] == my_username and passwordInfo[0] == False:
                passwordInfo[3] = True
                passwordInfo[2] -= 1
                try:
                    if command[2] == passwordInfo[1]:
                        passwordInfo[0] = True
                        print("password accepted")
                    else:
                        print(f"please enter the password: /password\\ThePassword")
                except:
                    print(f"please enter the password: /password\\ThePassword")

        # private message 
        elif command[0] == commandList[3]:
            if command[1] == my_username:
                print(f"{username} whispered: \"{command[2]}\" to you")
    except:
        d = 0
    if shotdown == True:
        exit()
    return passwordInfo
# do a command you just sent
def doACommandYourself(command,message,my_username):
    try:
        # kick command
        if command[0] == commandList[0]:
            if command[1] == my_username:
                # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
                message = f"{my_username} kicked himself".encode('utf-8')
                message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(message_header + message)
                exit()
        #password
        elif command[0] == commandList[7]:
            passwordInfo[1] = command[1]




        # private message 
        if command[0] == commandList[3]:
            print(f"you whispered: \"{command[2]}\" to {command[1]}")
    except:
        ww = 8
    return passwordInfo


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
    command = message.split("\\")
    if command[0] in commandList:
        passwordInfo = doACommandYourself(command,message,my_username)

    # If message is not empty - send it
    if message:
        originalMessage = message
        # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)
    if message != "":
        splitMessage = originalMessage.split("\\")
        if splitMessage[0] != commandList[7] and passwordInfo[2] <= 3:
            passwordInfo[2] += 1
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
            
            if passwordInfo[2] > 5 and passwordInfo[3] == False:
                passwordInfo[0] = True
                for x in range(len(pendingMessages)):
                    command = pendingMessages[0].split("\\")
                if command[0] in commandList:
                    e = 0
                else:
                    try:
                        print(pendingMessages[0])
                    except:
                        e =5
                    pendingMessages.pop(0)
                    
                    
            
            # Print message
            command = message.split("\\")
            if command[0] in commandList:
                passwordInfo = doACommand(command,message,username,my_username, message_header, username_header, passwordInfo)
            else:
                if passwordInfo[0] == False and passwordInfo[2] > 5:
                    pendingMessages.append(f'{username} > {message}')
                else:
                    print(f'{username} > {message}')
                    

    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            logging.exception("Exception occurred", e)
            sys.exit()

        # We just did not receive anything
        continue

    except Exception as e:
        # Any other exception - something happened, exit
        print('Reading error: '.format(str(e)))
        logging.exception("Exception occurred", e)
        sys.exit()
