def alt_begin(alt_run):
    import alt_startup
    complete = alt_startup.alt_startup(alt_run)
    if complete:
        return
    
    while True:
        value = input('Startup command:')
        complete = alt_startup.alt_startup(value)
        if complete:
            return

print("Welcome to Firefile Scorcery School server. Press enter to begin the game, or enter a startup command.")
alt_run = input('Startup command:')
if not alt_run:
    import startup
else:
    alt_begin(alt_run)
