import curses
from uzuki.core.buffer import Buffer
from uzuki.core.cursor import Cursor
from uzuki.core.history import History
from uzuki.input.handler import InputHandler
from uzuki.modes.normal_mode import NormalMode
from uzuki.modes.insert_mode import InsertMode
from uzuki.commands.command_mode import CommandMode

class Screen:
    def __init__(self):
        self.buffer = Buffer()
        self.cursor = Cursor()
        self.history = History()
        self.normal_mode = NormalMode(self)
        self.insert_mode = InsertMode(self)
        self.command_mode = CommandMode(self)
        self.mode = self.normal_mode
        self.input_handler = InputHandler(self)
        self.filename = 'untitled.txt'

    def run(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(1)
        while True:
            self.draw()
            raw = stdscr.getch()
            self.input_handler.handle(raw)

    def draw(self):
        self.stdscr.erase()
        h, w = self.stdscr.getmaxyx()
        for idx, line in enumerate(self.buffer.lines[:h-1]):
            self.stdscr.addstr(idx, 0, line)
        status = f"--{self.mode.__class__.__name__.upper()}-- {self.filename} {self.cursor.row+1}:{self.cursor.col+1}"
        self.stdscr.addstr(h-1, 0, status[:w-1], curses.A_REVERSE)
        self.stdscr.move(self.cursor.row, self.cursor.col)
        self.stdscr.refresh()
