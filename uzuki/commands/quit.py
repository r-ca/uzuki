class QuitCommand:
    def execute(self, screen, args):
        # Log the quit command execution
        screen.set_message("Exiting the application...")
        raise SystemExit
