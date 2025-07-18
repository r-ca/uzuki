class SaveCommand:
    def execute(self, screen, args):
        screen.save_file()
        screen.set_message("File saved successfully.")
