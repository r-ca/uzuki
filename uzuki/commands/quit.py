class QuitCommand:
    def execute(self, screen, args):
        # Log the quit command execution
        screen.notify_info("Exiting the application...")
        raise SystemExit
