import startup

print("Welcome to Firefile Scorcery School server. Press enter to begin the game, or enter a startup command.")
while True:
    cmd = input('Startup command:')
    if cmd == "":
        cmd = "default"
    try:
        if startup.launch_cmds[cmd]["type"] == "message":
            print(startup.launch_cmds[cmd]["message"])
        elif startup.launch_cmds[cmd]["type"] == "function":
            startup.launch_cmds[cmd]["function"]()
        
        if startup.launch_cmds[cmd]["complete"] == True:
            break
    except KeyError:
        print("Invalid command. Please try again.")
