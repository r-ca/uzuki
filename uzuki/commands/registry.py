from uzuki.commands import quit as quit_command, save as save_command

COMMANDS = {
    'q': quit_command.QuitCommand,
    'w': save_command.SaveCommand,
}

class CommandRegistry:
    @staticmethod
    def execute(screen, name: str):
        parts = name.split()
        cmd = parts[0]
        handler = COMMANDS.get(cmd)
        if handler:
            handler().execute(screen, parts[1:])
        else:
            screen.set_message(f"Unknown command: {cmd}")
