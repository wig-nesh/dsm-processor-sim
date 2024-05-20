import curses
import threading
import time

class GlobalClock:
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

main_mid = 0

def update_clock(window, freq, color_pair=0):
    window.addstr(1,2,"●", curses.color_pair(color_pair))
    window.addstr(1,4,format_frequency(freq))
    window.refresh()

def update_bus(window, color_pair=0):
    connections = [0, 4, 10, 16, 22, 27]
    for i in range(28):
        if i in connections: window.addstr(i+6, main_mid, "+", curses.color_pair(color_pair))
        else: window.addstr(i+6, main_mid, "|", curses.color_pair(color_pair))
    window.addstr(i+7, main_mid, "x8", curses.color_pair(color_pair))
    window.refresh()

def update_ORtoBUS(window, color_pair=0):
    window.addstr(10, main_mid + 1, "-"*9+"+", curses.color_pair(color_pair))
    window.refresh()

def update_ALUtoBUS(window, color_pair=0):
    window.addstr(16, main_mid + 1, "-"*9+"+", curses.color_pair(color_pair))
    window.refresh()

def update_ARtoBUS(window, color_pair=0):
    window.addstr(22, main_mid + 1, "-"*9+"+", curses.color_pair(color_pair))
    window.refresh()

def update_IRtoBUS(window, color_pair=0):
    window.addstr(33, main_mid + 1, "-"*9+"+", curses.color_pair(color_pair))
    window.refresh()

def update_MRtoBUS(window, color_pair=0):
    window.addstr(10, main_mid - 11, "+"+"-"*10, curses.color_pair(color_pair))
    window.refresh()

def update_PCtoBUS(window, color_pair=0):
    window.addstr(16, main_mid - 11, "+"+"-"*10, curses.color_pair(color_pair))
    window.refresh()

def update_SPtoBUS(window, color_pair=0):
    window.addstr(22, main_mid - 11, "+"+"-"*10, curses.color_pair(color_pair))
    window.refresh()

def update_RGtoBUS(window, color_pair=0):
    window.addstr(28, main_mid - 11, "+"+"-"*10, curses.color_pair(color_pair))
    window.refresh()

def update_ORtoALU(window, color_pair=0):
    for i in range(3):
        if i%2:
            window.addstr(i+12, main_mid + 26, "|", curses.color_pair(color_pair))
        else:
            window.addstr(i+12, main_mid + 26, "+", curses.color_pair(color_pair))
    window.refresh()

def update_ALUtoAR(window, color_pair=0):
    for i in range(3):
        if i%2:
            window.addstr(i+18, main_mid + 28, "|", curses.color_pair(color_pair))
        else:
            window.addstr(i+18, main_mid + 28, "+", curses.color_pair(color_pair))
    window.refresh()

def update_ALUtoFR(window, color_pair=0):
    for i in range(12):
        if i in [0, 11]:
            window.addstr(i+16, main_mid + 29, "+-+", curses.color_pair(color_pair))
        else:
            window.addstr(i+16, main_mid + 31, "|", curses.color_pair(color_pair))
    window.refresh()

def update_FRtoMemSeq(window, color_pair=0):
    for i in range(12):
        if i in [0, 11]:
            window.addstr(i+29, main_mid + 29, "+-+", curses.color_pair(color_pair))
        else:
            window.addstr(i+29, main_mid + 31, "|", curses.color_pair(color_pair))
    window.refresh()

def update_IRtoMemSeq(window, color_pair=0):
    for i in range(6):
        if i in [0, 5]:
            window.addstr(i+35, main_mid + 8, "+-+", curses.color_pair(color_pair))
        else:
            window.addstr(i+35, main_mid + 8, "|", curses.color_pair(color_pair))
    window.refresh()

def update_MSeqtoMMem(window, color_pair=0):
    for i in range(3):
        if i%2:
            window.addstr(i+42, main_mid + 26, "|", curses.color_pair(color_pair))
        else:
            window.addstr(i+42, main_mid + 26, "+", curses.color_pair(color_pair))
    window.refresh()

def update_MRtoExtMem(window, color_pair=0):
    for i in range(3):
        if i%2:
            window.addstr(i+6, main_mid - 28, "|", curses.color_pair(color_pair))
        else:
            window.addstr(i+6, main_mid - 28, "+", curses.color_pair(color_pair))
    window.refresh()

extMemData = [0x00]*256
extMemState = [0]*256 # 0-empty 1-program 2-data segment 3-stack 4-other, also used for color
extMemState[-10:] = [3]*10 # temp stack
def update_ExtMemData(window):
    for i in range(8):
        for j in range(32):
            idx = i*32+j
            window.addstr(1+(j%32), 2+i*11, "●", curses.color_pair(extMemState[idx]))
            window.addstr(1+(j%32), 3+i*11, f" {idx:02x} {extMemData[idx]:02x}")
    window.refresh()

RGData = [0x00]*16
RGState = [0]*16 # 0-empty, 1-used, 2-enable, 3-load
RGState[:4] = [1]*4 # temp
RGState[1] = 2 # temp
def update_RGData(window):
    for i in range(16):
        window.addstr(1+i, 2, "●", curses.color_pair(RGState[i]))
        window.addstr(1+i, 3, f" {i:2} {RGData[i]:02x} {RGData[i]:08b}")
    window.refresh()

ALUData = [0x00]*3
ALUState = 0 
def update_ALUData(window):
    for i in range(3):
        if i==2: 
            window.addstr(1+i, 4, "●", curses.color_pair(ALUState))
            window.addstr(1+i, 5, f" {ALUData[i]:02x} {ALUData[i]:08b}")
        else: window.addstr(1+i, 5, f" {ALUData[i]:02x} {ALUData[i]:08b}")
    window.refresh()

FRData = 0x00 # S Z X A X P X C
FRState = [1]*8
def update_FRData(window):
    for i in range(8):
        if i in [2, 4, 6]: window.addstr(1, 6+i, " ")
        else: window.addstr(1, 6+i, "●", curses.color_pair(FRState[i]))
    window.addstr(2, 6, "SZ A P C")
    window.addstr(3, 6, f"{FRData:08b}")
    window.refresh()

MRData = 0x00
MRState = 0
def update_MRData(window):
    window.addstr(2, 3, "●", curses.color_pair(MRState))
    window.addstr(2, 4, f" {MRData:02x} {MRData:08b}")
    window.refresh()

PCData = 0x00
PCState = 0
def update_PCData(window):
    window.addstr(2, 3, "●", curses.color_pair(PCState))
    window.addstr(2, 4, f" {PCData:02x} {PCData:08b}")
    window.refresh()

SPData = 0x00
SPState = 0
def update_SPData(window):
    window.addstr(2, 3, "●", curses.color_pair(SPState))
    window.addstr(2, 4, f" {SPData:02x} {SPData:08b}")
    window.refresh()

ORData = 0x00
ORState = 0
def update_ORData(window):
    window.addstr(2, 4, "●", curses.color_pair(ORState))
    window.addstr(2, 5, f" {ORData:02x} {ORData:08b}")
    window.refresh()

ARData = 0x00
ARState = 0
def update_ARData(window):
    window.addstr(2, 4, "●", curses.color_pair(ARState))
    window.addstr(2, 5, f" {ARData:02x} {ARData:08b}")
    window.refresh()

IRData = 0x00
IRState = 0
def update_IRData(window):
    window.addstr(2, 4, "●", curses.color_pair(IRState))
    window.addstr(2, 5, f" {IRData:02x} {IRData:08b}")
    window.refresh()


def main(stdscr):
    global main_mid
    main_mid= curses.COLS//2-38

    global extMemData
    global extMemState
    global RGData
    global RGState
    global ALUData
    global ALUState
    global MRData
    global MRState
    global PCData
    global PCState
    global SPData
    global SPState
    global ORData
    global ORState
    global ARData
    global ARState
    global IRData
    global IRState

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

    clock = GlobalClock(1/freq, clock_tick)

    # ----------STATIC ELEMENTS----------

    # title
    stdscr.box()
    addstr_mid(stdscr, " DSM Processor Simulator ")
    stdscr.refresh()

    # clock window
    height = 3; width = 11
    begin_x = 4; begin_y = 2
    clk = curses.newwin(height, width, begin_y, begin_x)
    clk.box()
    addstr_mid(clk, " Clock ", color_pair=3)
    clk.refresh()

    # external memory window
    height = 5; width = 60
    begin_x = main_mid - width//2; begin_y = 2
    ext_mem = curses.newwin(height, width, begin_y, begin_x)
    ext_mem.box()
    addstr_mid(ext_mem, " External Memory ")
    ext_mem.refresh()

    # operand register window
    begin_x = main_mid + 10; begin_y += height + 1
    height = 5; width = 20
    op_r = curses.newwin(height, width, begin_y, begin_x)
    op_r.box()
    addstr_mid(op_r, " Operand Register ")
    op_r.refresh()

    # alu window
    begin_x = main_mid + 10; begin_y += height + 1
    height = 5; width = 20
    alu = curses.newwin(height, width, begin_y, begin_x)
    alu.box()
    addstr_mid(alu, " ALU ")
    alu.refresh()    

    # accumulator register window
    begin_x = main_mid + 10; begin_y += height + 1
    height = 5; width = 20
    ac_r = curses.newwin(height, width, begin_y, begin_x)
    ac_r.box()
    addstr_mid(ac_r, " Accumulator ")
    ac_r.refresh()

    # flag register window
    begin_x = main_mid + 10; begin_y += height + 1
    height = 5; width = 20
    f_r = curses.newwin(height, width, begin_y, begin_x)
    f_r.box()
    addstr_mid(f_r, " Flag Register ")
    f_r.refresh()

    # instruction register window
    begin_x = main_mid + 10; begin_y += height + 1
    height = 5; width = 20
    i_r = curses.newwin(height, width, begin_y, begin_x)
    i_r.box()
    addstr_mid(i_r, " Instruction Reg ")
    i_r.refresh()

    # microporgram sequencer window
    begin_x = main_mid + 10; begin_y += height + 1
    height = 5; width = 20
    mps = curses.newwin(height, width, begin_y, begin_x)
    mps.box()
    addstr_mid(mps, " Microprogram Seq ")
    mps.refresh()

    # microprogram memory window
    height = 5; width = 60
    begin_x = main_mid - width//2; begin_y += height + 1
    mp_mem = curses.newwin(height, width, begin_y, begin_x)
    mp_mem.box()
    addstr_mid(mp_mem, " Microprogram Memory ")
    mp_mem.refresh()

    begin_y = 2
    width = 20
    # memory address register window
    begin_x = main_mid - width - 10; begin_y += height + 1
    height = 5; width = 20
    ma_r = curses.newwin(height, width, begin_y, begin_x)
    ma_r.box()
    addstr_mid(ma_r, " Address Reg ")
    ma_r.refresh()

    # program counter window
    begin_x = main_mid - width - 10; begin_y += height + 1
    height = 5; width = 20
    pc = curses.newwin(height, width, begin_y, begin_x)
    pc.box()
    addstr_mid(pc, " Program Counter ")
    pc.refresh()

    # stack pointer window
    begin_x = main_mid - width - 10; begin_y += height + 1
    height = 5; width = 20
    sp = curses.newwin(height, width, begin_y, begin_x)
    sp.box()
    addstr_mid(sp, " Stack Pointer ")
    sp.refresh()

    # register array window
    begin_x = main_mid -width - 10; begin_y += height + 1
    height = 18; width = 20
    r_arr = curses.newwin(height, width, begin_y, begin_x)
    r_arr.box()
    addstr_mid(r_arr, " Reg Array ")
    r_arr.refresh()

    # external memory display window
    height = 32+2; width = 11*8
    begin_y = 2; begin_x = curses.COLS - width - 4
    ext_mem_display = curses.newwin(height, width, begin_y, begin_x)
    ext_mem_display.box()
    addstr_mid(ext_mem_display, " External Memory Display ")
    ext_mem_display.refresh()

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
    update_ALUtoAR(stdscr)
    update_ALUtoFR(stdscr)
    update_FRtoMemSeq(stdscr)
    update_IRtoMemSeq(stdscr)
    update_MSeqtoMMem(stdscr)
    update_MRtoExtMem(stdscr)

    update_ExtMemData(ext_mem_display)
    update_RGData(r_arr)
    update_MRData(ma_r)
    update_ALUData(alu)
    update_FRData(f_r)
    update_PCData(pc)
    update_SPData(sp)
    update_ORData(op_r)
    update_ARData(ac_r)
    update_IRData(i_r)

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