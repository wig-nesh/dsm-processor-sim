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
    clock_cycle = [0]
    instruction_address = [0]
    value = [0]
    freq = 10   

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
            
            if clock_cycle[0]==0:
                # Epc
                update_PCData(pc, PCData, color("green"))
            elif clock_cycle[0]==1:
                # RD
                instruction_address[0] = extMemData[MRData]
                extMemState[MRData] = color("green")
                update_ExtMemData(ext_mem_display, extMemData, extMemState)

            elif clock_cycle[0]==2:
                if MPSeqData in [0b0100001110,0b0100010000,0b0100010010,0b0100010100,0b0100010110,0b0100011000,0b0100011010,0b0100011100,0b0100011110,0b0100100000,0b0100100010,0b0100100100,0b0100100110,0b0100101000,0b0100101010,0b0100101100]:
                    # Epc
                    update_PCData(pc, PCData, color("green"))

            elif clock_cycle[0]==3:
                if MPSeqData in [0b0100001111,0b0100010001,0b0100010011,0b0100010101,0b0100010111,0b0100011001,0b0100011011,0b0100011101,0b0100011111,0b0100100001,0b0100100011,0b0100100101,0b0100100111,0b0100101001,0b0100101011,0b0100101101]:
                    # RD 
                    value[0] = extMemData[MRData]
                    extMemState[MRData] = color("green")
                    update_ExtMemData(ext_mem_display, extMemData, extMemState)

        else: # falling
            update_clock(clk, freq, color("white"))
            if clock_cycle[0]==0:
                # Lmr
                MRData = PCData
                update_MRData(ma_r, MRData, color("blue"))
                # Ipc
                PCData += 1
                update_PCData(pc, PCData, color("yellow"))
            elif clock_cycle[0]==1:
                # Lir
                IRData = instruction_address[0]
                update_IRData(i_r, IRData, color("blue"))
                # Lms
                MPSeqData = encode_IRtoMPS(IRData)
                MPMemData = encode_MPStoCSSig(MPSeqData)
                update_MPSeqData(mp_s, MPSeqData, color("blue"))
                update_MPMemData(mp_mem, MPMemData)

            elif clock_cycle[0]==2:
                if MPSeqData in [0b0100001110,0b0100010000,0b0100010010,0b0100010100,0b0100010110,0b0100011000,0b0100011010,0b0100011100,0b0100011110,0b0100100000,0b0100100010,0b0100100100,0b0100100110,0b0100101000,0b0100101010,0b0100101100]:
                    # Lmr
                    MRData = PCData
                    update_MRData(ma_r, MRData, color("blue"))
                    # Ipc
                    PCData += 1
                    update_PCData(pc, PCData, color("yellow"))
                
                MPSeqData+=1
                update_MPSeqData(mp_s, MPSeqData, color("blue"))
                MPMemData = encode_MPStoCSSig(MPSeqData)
                update_MPMemData(mp_mem, MPMemData)

            elif clock_cycle[0]==3:
                if MPSeqData==0b0100001111: # R0
                    # Lrg
                    RGData[0] = value[0]
                    RGState[0] = color("blue")
                    update_RGData(r_arr, RGData, RGState)
                    # End
                    clock_cycle[0] = -1
                if MPSeqData==0b0100010001: # R1
                    # Lrg
                    RGData[1] = value[0]
                    RGState[1] = color("blue")
                    update_RGData(r_arr, RGData, RGState)
                    # End
                    clock_cycle[0] = -1
                if MPSeqData==0b0100010011: # R2
                    # Lrg
                    RGData[2] = value[0]
                    RGState[2] = color("blue")
                    update_RGData(r_arr, RGData, RGState)
                    # End
                    clock_cycle[0] = -1
                if MPSeqData==0b0100010101: # R3
                    # Lrg
                    RGData[3] = value[0]
                    RGState[3] = color("blue")
                    update_RGData(r_arr, RGData, RGState)
                    # End
                    clock_cycle[0] = -1
                if MPSeqData==0b0100010111: # R4
                    # Lrg
                    RGData[4] = value[0]
                    RGState[4] = color("blue")
                    update_RGData(r_arr, RGData, RGState)
                    # End
                    clock_cycle[0] = -1
                if MPSeqData==0b0100011001: # R5
                    # Lrg
                    RGData[5] = value[0]
                    RGState[5] = color("blue")
                    update_RGData(r_arr, RGData, RGState)
                    # End
                    clock_cycle[0] = -1
                if MPSeqData==0b0100011011: # R6
                    # Lrg
                    RGData[6] = value[0]
                    RGState[6] = color("blue")
                    update_RGData(r_arr, RGData, RGState)
                    # End
                    clock_cycle[0] = -1
                if MPSeqData==0b0100011101: # R7
                    # Lrg
                    RGData[7] = value[0]
                    RGState[7] = color("blue")
                    update_RGData(r_arr, RGData, RGState)
                    # End
                    clock_cycle[0] = -1
                if MPSeqData==0b0100011111: # R8
                    # Lrg
                    RGData[8] = value[0]
                    RGState[8] = color("blue")
                    update_RGData(r_arr, RGData, RGState)
                    # End
                    clock_cycle[0] = -1
                if MPSeqData==0b0100100001: # R9
                    # Lrg
                    RGData[9] = value[0]
                    RGState[9] = color("blue")
                    update_RGData(r_arr, RGData, RGState)
                    # End
                    clock_cycle[0] = -1
                if MPSeqData==0b0100100011: # R10
                    # Lrg
                    RGData[10] = value[0]
                    RGState[10] = color("blue")
                    update_RGData(r_arr, RGData, RGState)
                    # End
                    clock_cycle[0] = -1
                if MPSeqData==0b0100100101: # R11
                    # Lrg
                    RGData[11] = value[0]
                    RGState[11] = color("blue")
                    update_RGData(r_arr, RGData, RGState)
                    # End
                    clock_cycle[0] = -1
                if MPSeqData==0b0100100111: # R12
                    # Lrg
                    RGData[12] = value[0]
                    RGState[12] = color("blue")
                    update_RGData(r_arr, RGData, RGState)
                    # End
                    clock_cycle[0] = -1
                if MPSeqData==0b0100101001: # R13
                    # Lrg
                    RGData[13] = value[0]
                    RGState[13] = color("blue")
                    update_RGData(r_arr, RGData, RGState)
                    # End
                    clock_cycle[0] = -1
                if MPSeqData==0b0100101011: # R14
                    # Lrg
                    RGData[14] = value[0]
                    RGState[14] = color("blue")
                    update_RGData(r_arr, RGData, RGState)
                    # End
                    clock_cycle[0] = -1
                if MPSeqData==0b0100101101: # R15
                    # Lrg
                    RGData[15] = value[0]
                    RGState[15] = color("blue")
                    update_RGData(r_arr, RGData, RGState)
                    # End
                    clock_cycle[0] = -1

            clock_cycle[0] = (clock_cycle[0]+1)%4


            # IRData = (IRData+1)%(0xFF+1)
            # MPSeqData = encode_IRtoMPS(IRData)
            # MPMemData = encode_MPStoCSSig(MPSeqData)
            # update_IRData(i_r, IRData)
            # update_MPSeqData(mp_s, MPSeqData)
            # update_MPMemData(mp_mem, MPMemData)

        


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

    update_ExtMemData(ext_mem_display, extMemData)
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