import curses

def addstr_mid(window, string, height=0):
    win_height, win_width = window.getmaxyx()
    spaces = win_width//2 - len(string)//2
    window.addstr(height, spaces, string)

def main(stdscr):
    stdscr.clear()

    # starting curses
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    # title
    # stdscr.border(
    #     '|', '|', '-', '-',
    #     '+', '+', '+', '+'
    # )
    stdscr.box()
    addstr_mid(stdscr, " DSM Processor Simulator ")
    stdscr.refresh()

    # clock window
    begin_x = 20; begin_y = 7
    height = 5; width = 40
    clock = curses.newwin(height, width, begin_y, begin_x)
    clock.box()
    addstr_mid(clock, " Clock ")
    clock.refresh()

    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break

    # ending curses
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

curses.wrapper(main)