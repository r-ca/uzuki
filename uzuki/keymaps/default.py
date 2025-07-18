class DefaultKeyMaps:
    @staticmethod
    def get_global_bindings():
        return {
            'ctrl_c': 'quit',
            'ctrl_s': 'save',
            'ctrl_q': 'quit',
        }
    
    @staticmethod
    def get_normal_mode_bindings():
        return {
            'h': 'move_left',
            'j': 'move_down', 
            'k': 'move_up',
            'l': 'move_right',
            'i': 'enter_insert_mode',
            'x': 'delete_char',
            'o': 'new_line_below',
            'O': 'new_line_above',
            'a': 'append',
            'A': 'append_end',
            'dd': 'delete_line',
            'yy': 'yank_line',
            'p': 'paste',
            'P': 'paste_before',
            ':': 'enter_command_mode',
            'escape': 'noop',
        }
    
    @staticmethod
    def get_insert_mode_bindings():
        return {
            'escape': 'enter_normal_mode',
            'enter': 'new_line',
            'backspace': 'delete_backward',
            'tab': 'indent',
            'shift_tab': 'unindent',
        }
    
    @staticmethod
    def get_command_mode_bindings():
        return {
            'escape': 'enter_normal_mode',
            'enter': 'execute_command',
            'backspace': 'delete_backward',
        } 