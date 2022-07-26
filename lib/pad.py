import curses

class Pad:
    def __init__(self):
        self.scr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.scr.keypad(True)
        self.scr.timeout(5000)
        self.scr.refresh()
        self.scr_height, self.width = self.scr.getmaxyx()
        self.pad_height = self.scr_height + 1000
        self.pad = curses.newpad(self.pad_height, self.width)
        self.pad.scrollok(True)
        self.pad_pos = 0

    def refresh(self):
        self.scr.refresh()
        self.pad.refresh(self.pad_pos, 0, 0, 0, self.scr_height - 1, self.width)

    def fill_in(self, contents):
        self.pad.clear()
        for i, line in enumerate(contents):
            self.pad.addstr(line)

    def getch(self):
        return self.scr.getch()

    def release(self):
        curses.nocbreak()
        self.scr.keypad(False)
        curses.echo()
        curses.endwin()
