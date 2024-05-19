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

def addstr_mid(window, string, height=0, color_pair=0):
    win_height, win_width = window.getmaxyx()
    window.addstr(height, win_width//2 - len(string)//2, string, curses.color_pair(color_pair))

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

def update_clock(window, freq, color_pair=0):
    window.addstr(1,2,"●", curses.color_pair(color_pair))
    window.addstr(1,4,format_frequency(freq))
    window.refresh()

def update_bus(window, color_pair=0):
    connections = [0, 4, 10, 16, 22, 28]
    for i in range(29):
        if i in connections: addstr_mid(window, "+", i+6, color_pair)
        else: addstr_mid(window, "|", i+6, color_pair)
    addstr_mid(window, "x8", i+7, color_pair)
    window.refresh()

def update_ORtoBUS(window, color_pair=0):
    window.addstr(10, curses.COLS//2 + 1, "-"*9+"+", curses.color_pair(color_pair))

def update_ALUtoBUS(window, color_pair=0):
    window.addstr(16, curses.COLS//2 + 1, "-"*9+"+", curses.color_pair(color_pair))

def update_ARtoBUS(window, color_pair=0):
    window.addstr(22, curses.COLS//2 + 1, "-"*9+"+", curses.color_pair(color_pair))

def update_IRtoBUS(window, color_pair=0):
    window.addstr(34, curses.COLS//2 + 1, "-"*9+"+", curses.color_pair(color_pair))

def update_MRtoBUS(window, color_pair=0):
    window.addstr(10, curses.COLS//2 - 11, "+"+"-"*10, curses.color_pair(color_pair))

def update_PCtoBUS(window, color_pair=0):
    window.addstr(16, curses.COLS//2 - 11, "+"+"-"*10, curses.color_pair(color_pair))

def update_SPtoBUS(window, color_pair=0):
    window.addstr(22, curses.COLS//2 - 11, "+"+"-"*10, curses.color_pair(color_pair))

def update_RGtoBUS(window, color_pair=0):
    window.addstr(28, curses.COLS//2 - 11, "+"+"-"*10, curses.color_pair(color_pair))

def update_ORtoALU(window, color_pair=0):
    for i in range(3):
        if i%2:
            window.addstr(i+12, curses.COLS//2 + 26, "|", curses.color_pair(color_pair))
        else:
            window.addstr(i+12, curses.COLS//2 + 26, "+", curses.color_pair(color_pair))

def update_ALUtoAR_FR(window, color_pair=0):
    for i in range(13):
        if i in [0, 6, 12]:
            window.addstr(i+16, curses.COLS//2 + 31, "+", curses.color_pair(color_pair))
            window.addstr(i+16, curses.COLS//2 + 29, "+-", curses.color_pair(color_pair))
        else:
            window.addstr(i+16, curses.COLS//2 + 31, "|", curses.color_pair(color_pair))

def update_MRtoExtM(window, color_pair=0):
    for i in range(3):
        if i%2:
            window.addstr(i+6, curses.COLS//2 - 28, "|", curses.color_pair(color_pair))
        else:
            window.addstr(i+6, curses.COLS//2 - 28, "+", curses.color_pair(color_pair))

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
    addstr_mid(clk, " Clock ", color_pair=3)
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

    # flag register window
    begin_x = curses.COLS//2 + 10; begin_y += height + 1
    height = 5; width = 20
    f_r = curses.newwin(height, width, begin_y, begin_x)
    f_r.box()
    addstr_mid(f_r, " Flag Register ")
    f_r.refresh()

    # instruction register window
    begin_x = curses.COLS//2 + 10; begin_y += height + 1
    height = 5; width = 20
    i_r = curses.newwin(height, width, begin_y, begin_x)
    i_r.box()
    addstr_mid(i_r, " Instruction Reg ")
    i_r.refresh()

    # microporgram sequencer window
    begin_x = curses.COLS//2 + 10; begin_y += height + 1
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

    begin_y = 2
    width = 20
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

    # register array window
    begin_x = curses.COLS//2 -width - 10; begin_y += height + 1
    height = 18; width = 20
    r_arr = curses.newwin(height, width, begin_y, begin_x)
    r_arr.box()
    addstr_mid(r_arr, " Reg Array ")
    r_arr.refresh()



    # ----------ACTIVE ELEMENTS----------

    update_clock(clk, freq)
    update_bus(stdscr)
    update_ORtoBUS(stdscr)
    update_ALUtoBUS(stdscr)
    update_ARtoBUS(stdscr)
    update_IRtoBUS(stdscr)
    update_MRtoBUS(stdscr)
    update_PCtoBUS(stdscr)
    update_SPtoBUS(stdscr)
    update_RGtoBUS(stdscr)
    update_ORtoALU(stdscr)
    update_ALUtoAR_FR(stdscr)
    update_MRtoExtM(stdscr)
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