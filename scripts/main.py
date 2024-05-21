import curses
import threading
import time

from helper_functions import *
from global_variables import *
from update import *
from static import *
from encoder import *

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


def main(stdscr):

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
        global MPSeqData
        global MPSeqState
        global MPMemData

        clock_state[0] = not clock_state[0]
        if clock_state[0]: # rising
            update_clock(clk, freq, color("yellow"))
        else: # falling
            update_clock(clk, freq, color("white"))
            IRData = (IRData+1)%(0xFF+1)
            MPSeqData = encode_IRtoMPS(IRData)
            MPMemData = encode_MPStoCSSig(MPSeqData)
            update_IRData(i_r, IRData)
            update_MPSeqData(mp_s, MPSeqData)
            update_MPMemData(mp_mem, MPMemData)


    clock = GlobalClock(1/freq, clock_tick)

    # ----------STATIC ELEMENTS----------

    static_title(stdscr)
    clk = static_clock()
    ext_mem = static_extMem()
    op_r = static_OR()
    alu = static_ALU()
    ac_r = static_AR()
    f_r = static_FR()
    i_r = static_IR()
    mp_s = static_MPSeq()
    mp_mem = static_MPMem()
    ma_r = static_MR()
    pc = static_PC()
    sp = static_SP()
    r_arr = static_RG()
    ext_mem_display = static_extMemDisplay()

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
    update_MPSeqtoMPMem(stdscr)
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
    update_MPSeqData(mp_s)
    update_MPMemData(mp_mem)

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