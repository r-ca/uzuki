# Uzuki - A Vim-like Text Editor in Python

Uzuki is a lightweight, Vim-inspired text editor built in Python using the `curses` library. It provides a familiar editing experience with modal editing, customizable keymaps, and a clean architecture.

## Features

### Core Editing
- **Modal Editing**: Normal, Insert, Command, and File Browser modes
- **Vim-like Keybindings**: Familiar navigation and editing commands
- **Multi-key Sequences**: Support for commands like `dd` (delete line)
- **True Color Support**: Rich color display with 256-color and true color support

### File Management
- **File Loading/Saving**: Basic file I/O with encoding detection
- **File Browser**: Built-in file browser for navigation
- **Encoding Support**: Automatic encoding detection and switching

### UI Features
- **Status Line**: Dynamic status line showing mode, file info, and cursor position
- **Line Numbers**: Optional line number display
- **Current Line Highlighting**: Visual highlighting of the current line
- **Notifications**: Toast-style notifications for user feedback
- **Greeting Screen**: Customizable startup screen

### Configuration
- **Python-based Config**: Configuration via Python scripts (similar to Neovim's Lua)
- **Dynamic Keymaps**: Runtime keymap customization
- **Plugin System**: Extensible architecture for plugins

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd uzuki
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the editor:
```bash
python -m uzuki.app [filename]
```

## Basic Usage

### Modes
- **Normal Mode**: Default mode for navigation and commands
- **Insert Mode**: For text input (press `i` to enter)
- **Command Mode**: For executing commands (press `:` to enter)
- **File Browser Mode**: For file navigation (press `Ctrl+e` to enter)

### Basic Commands
- `h`, `j`, `k`, `l`: Move cursor left, down, up, right
- `i`: Enter Insert mode
- `Esc`: Return to Normal mode
- `:q`: Quit
- `:w`: Save file
- `:wq`: Save and quit
- `dd`: Delete current line
- `yy`: Yank (copy) current line
- `p`: Paste
- `x`: Delete character under cursor

### Configuration

Create a configuration file `init.py` in your home directory:

```python
# ~/.uzuki/init.py

# Keymap customization
def setup_keymaps(editor):
    # Add custom keybindings
    editor.keymap.bind('normal', 'ctrl_s', 'save')
    editor.keymap.bind('insert', 'ctrl_s', 'save')

# UI customization
def setup_ui(editor):
    # Toggle line numbers
    editor.ui.toggle_line_numbers()
    
    # Set greeting content
    editor.ui.set_greeting_content([
        "Welcome to Uzuki!",
        "Press any key to continue..."
    ])

# Apply configuration
def apply_config(editor):
    setup_keymaps(editor)
    setup_ui(editor)
```

## Architecture

Uzuki follows a clean architecture with clear separation of concerns:

### Core Components
- **Buffer**: Text storage and manipulation
- **Cursor**: Cursor position management
- **Modes**: Modal editing system
- **Keymaps**: Dynamic key binding system

### UI Layer
- **UIController**: Main UI coordination
- **EditorDisplay**: Text rendering and display
- **StatusLine**: Status line management
- **Notifications**: User notification system

### Services
- **EditorService**: Core editing operations
- **FileService**: File I/O operations
- **ConfigService**: Configuration management
- **NotificationService**: Notification handling

## Development

### Project Structure
```
uzuki/
├── app.py                 # Main application entry point
├── core/                  # Core editor components
├── modes/                 # Editing modes
├── ui/                    # User interface components
├── services/              # Business logic services
├── controllers/           # Controller layer
├── input/                 # Input handling
├── keymaps/               # Key mapping system
├── commands/              # Command system
├── config/                # Configuration management
└── utils/                 # Utility functions
```

### Running Tests
```bash
python -m pytest tests/
```

### Debugging
The editor includes a debug logging system. Logs are written to `uzuki_debug_YYYYMMDD_HHMMSS.log` files.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by Vim and Neovim
- Built with Python's `curses` library
- Uses `colorama` for cross-platform color support 