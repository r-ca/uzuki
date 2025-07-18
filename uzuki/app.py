import curses
from uzuki.ui.screen import Screen

def main():
    curses.wrapper(Screen().run)

if __name__ == '__main__':
    main()
