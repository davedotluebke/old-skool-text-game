def alt_startup(command):
    if command == "help":
        print("Enter the startup state you wish to engage.")
        return False
    elif command == "default":
        import startup
        return True
    else:
        print("Invalid command. Please try again.")
        return False