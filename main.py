import curses
import threading
import time

class global_clock:
    def __init__(self, interval, callback):
        self.interval = interval
        self.callback = callback
        self.running = False
        self.paused = False
        self.thread = None
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run)
            self.thread.start()
    def _run(self):
        while self.running:
            with self.condition:
                if self.paused:
                    self.condition.wait()
                if not self.running:
                    break
            time.sleep(self.interval)
            self.callback()
    def play_pause(self):
        with self.condition:
            self.paused = not self.paused
            if not self.paused:
                self.condition.notify()        
    def stop(self):
        with self.condition:
            self.running = False
            self.paused = False
            self.condition.notify()
        self.thread.join()

def addstr_mid(window, string, height=0, color=0):
    win_height, win_width = window.getmaxyx()
    spaces = win_width//2 - len(string)//2
    if color==0: window.addstr(height, spaces, string)
    else: window.addstr(height, spaces, string, curses.color_pair(color))

def color(string):
    string = string.lower()
    if string=="red":
        return 1
    elif string=="green":
        return 2
    elif string=="yellow":
        return 3
    elif string=="blue":
        return 4
    elif string=="magenta":
        return 5
    elif string=="cyan":
        return 6
    elif string=='white':
        return 0
    
def format_frequency(frequency):
    prefixes = ['', 'K', 'M', 'G'] 
    magnitude = 0
    while frequency >= 1000:
        frequency /= 1000
        magnitude += 1
    formatted_frequency = "{:.0f}{}".format(frequency, prefixes[magnitude] + 'Hz')
    return formatted_frequency

def update_clock(window, freq, color=0):
    window.addstr(1,2,"●", curses.color_pair(color))
    window.addstr(1,4,format_frequency(freq))
    window.refresh()
    
def update_bus(window, color_pair=0):
    connections = [0, 4, 10, 16, 22, 26]
    for i in range(curses.LINES-25):
        if i in connections: addstr_mid(window, "+", i+6, color_pair)
        else: addstr_mid(window, "|", i+6, color_pair)
    addstr_mid(window, "x8", i+7, color_pair)
    window.refresh()


def main(stdscr):

    # initialize colors
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK) 

    color_pairs = [1, 2, 3, 4, 5, 6]
    color_idx = [0]

    clock_state = [False]
    freq = 20

    def clock_tick():
        # color_idx[0] = (color_idx[0] + 1) % len(color_pairs)
        clock_state[0] = clock_state[0]^True
        if clock_state[0]: update_clock(clk, freq, color("yellow"))
        else: update_clock(clk, freq, color("white"))

    clock = global_clock(1/freq, clock_tick)

    # ----------STATIC ELEMENTS----------

    # title
    stdscr.box()
    addstr_mid(stdscr, " DSM Processor Simulator ")
    stdscr.refresh()

    # clock window
    height = 3; width = 11
    begin_x = width//2; begin_y = 2
    clk = curses.newwin(height, width, begin_y, begin_x)
    clk.box()
    addstr_mid(clk, " Clock ", color=3)
    clk.refresh()

    # external memory window
    height = 5; width = 60
    begin_x = curses.COLS//2 - width//2; begin_y = 2
    ext_mem = curses.newwin(height, width, begin_y, begin_x)
    ext_mem.box()
    addstr_mid(ext_mem, " External Memory ")
    ext_mem.refresh()

    # operand register window
    begin_x = curses.COLS//2 + 10; begin_y += height + 1
    height = 5; width = 20
    op_r = curses.newwin(height, width, begin_y, begin_x)
    op_r.box()
    addstr_mid(op_r, " Operand Register ")
    op_r.refresh()

    # alu window
    begin_x = curses.COLS//2 + 10; begin_y += height + 1
    height = 5; width = 20
    alu = curses.newwin(height, width, begin_y, begin_x)
    alu.box()
    addstr_mid(alu, " ALU ")
    alu.refresh()    

    # accumulator register window
    begin_x = curses.COLS//2 + 10; begin_y += height + 1
    height = 5; width = 20
    ac_r = curses.newwin(height, width, begin_y, begin_x)
    ac_r.box()
    addstr_mid(ac_r, " Accumulator ")
    ac_r.refresh()

    # register array window
    begin_x = curses.COLS//2 + 10; begin_y += height + 1
    height = 13; width = 20
    r_arr = curses.newwin(height, width, begin_y, begin_x)
    r_arr.box()
    addstr_mid(r_arr, " Registers ")
    r_arr.refresh()

    # flag register window
    begin_x = curses.COLS//2 + 10; begin_y += height + 1
    height = 5; width = 20
    f_r = curses.newwin(height, width, begin_y, begin_x)
    f_r.box()
    addstr_mid(f_r, " Flag Register ")
    f_r.refresh()

    begin_y = 2
    # memory address register window
    begin_x = curses.COLS//2 - width - 10; begin_y += height + 1
    height = 5; width = 20
    ma_r = curses.newwin(height, width, begin_y, begin_x)
    ma_r.box()
    addstr_mid(ma_r, " Address Reg ")
    ma_r.refresh()

    # program counter window
    begin_x = curses.COLS//2 - width - 10; begin_y += height + 1
    height = 5; width = 20
    pc = curses.newwin(height, width, begin_y, begin_x)
    pc.box()
    addstr_mid(pc, " Program Counter ")
    pc.refresh()

    # stack pointer window
    begin_x = curses.COLS//2 - width - 10; begin_y += height + 1
    height = 5; width = 20
    sp = curses.newwin(height, width, begin_y, begin_x)
    sp.box()
    addstr_mid(sp, " Stack Pointer ")
    sp.refresh()

    # instruction register window
    begin_x = curses.COLS//2 - width - 10; begin_y += height + 1
    height = 5; width = 20
    i_r = curses.newwin(height, width, begin_y, begin_x)
    i_r.box()
    addstr_mid(i_r, " Instruction Reg ")
    i_r.refresh()

    # microprogram sequencer window
    begin_x = curses.COLS//2 - width - 10; begin_y += height + 9
    height = 5; width = 20
    mps = curses.newwin(height, width, begin_y, begin_x)
    mps.box()
    addstr_mid(mps, " Microprogram Seq ")
    mps.refresh()

    # microprogram memory window
    height = 5; width = 60
    begin_x = curses.COLS//2 - width//2; begin_y += height + 1
    mp_mem = curses.newwin(height, width, begin_y, begin_x)
    mp_mem.box()
    addstr_mid(mp_mem, " Microprogram Memory ")
    mp_mem.refresh()


    # ----------ACTIVE ELEMENTS----------

    # clock 
    update_clock(clk, freq)

    # bus
    update_bus(stdscr)

    # OR -> BUS
    begin_y = 8
    stdscr.addstr(begin_y+height//2, curses.COLS//2 + 1, "-"*9+"+")

    # ALU -> BUS
    begin_y += 6
    stdscr.addstr(begin_y+height//2, curses.COLS//2 + 1, "-"*9+"+")
    # OR -> ALU
    begin_x = curses.COLS//2 + 10
    width = 20
    for i in range(3):
        if not i%2:
            stdscr.addstr(begin_y-2+i, begin_x+int(3/4*width), "+")
        else:
            stdscr.addstr(begin_y-2+i, begin_x+int(3/4*width), "|")

    # AR -> BUS
    begin_y += 6
    stdscr.addstr(begin_y+height//2, curses.COLS//2 + 1, "-"*9+"+")
    # ALU -> AR
    for i in range(3):
        if not i%2:
            stdscr.addstr(begin_y-2+i, begin_x+int(9/10*width), "+")
        else:
            stdscr.addstr(begin_y-2+i, begin_x+int(9/10*width), "|")

    # RG <-> BUS
    begin_y += 10
    stdscr.addstr(begin_y+height//2, curses.COLS//2 + 1, "-"*9+"+")

    begin_x = curses.COLS//2 - width - 10; begin_y = height + 3
    height = 5; width = 20
    # MR <- BUS
    stdscr.addstr(begin_y+height//2, begin_x+width-1, "+"+"-"*10)
    # MR -> extMemory
    for i in range(3):
        if not i%2:
            stdscr.addstr(begin_y-2+i, begin_x+int(1/7*width), "+")
        else:
            stdscr.addstr(begin_y-2+i, begin_x+int(1/7*width), "|")

    # PC <-> BUS
    begin_y += 6
    stdscr.addstr(begin_y+height//2, begin_x+width-1, "+"+"-"*10)

    # SP <-> BUS
    begin_y += 6
    stdscr.addstr(begin_y+height//2, begin_x+width-1, "+"+"-"*10)

    # IR <- BUS
    begin_y += 6
    stdscr.addstr(begin_y+height//2, begin_x+width-1, "+"+"-"*10)
    
    stdscr.refresh()

    clock.start()
    try:
        while True:
            key = stdscr.getch()
            if key == ord('q'):
                break
            elif key == ord(' '):
                clock.play_pause()
                if clock.paused: clock_state[0] = True
            elif clock.running and key == curses.KEY_RIGHT:
                clock.play_pause()
                clock_tick()
                clock.play_pause()
    finally:
        clock.stop()

curses.wrapper(main)