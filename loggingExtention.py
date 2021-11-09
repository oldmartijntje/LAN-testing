def google(command,message,username,my_username, commandList, timeOfLaunch):
    import os
    import datetime
    import pathlib
    import logging

    #get the programs path
    ownPath = pathlib.Path().resolve()

    #create log folder if it doesn't exist
    if not os.path.exists(f'{ownPath}/ClientFiles'):
        os.makedirs(f'{ownPath}/ClientFiles')
        
    #logging setup
    logging.basicConfig(filename=f"{ownPath}/ClientFiles/redirectLog-{timeOfLaunch}.log",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

    if command[0] == commandList[2]:
        if "http" in command[2] and "/" in command[2] and "." in command[2] and ":" in command[2]:
            logging.info(f"{command[2]} by {username} sent to {command[1]}")
        else:
            logging.info(f"https://www.google.com/search?client=opera-gx&q={command[2]}&sourceid=opera&ie=UTF-8&oe=UTF-8 by {username} sent to {command[1]} (google search for {command[2]})")
    elif command[0] == commandList[4]:
        logging.info(f"https://www.youtube.com/watch?v=dQw4w9WgXcQ by {username} sent to {command[1]} (rickroll)")