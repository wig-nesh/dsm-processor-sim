import curses
import threading
import time

from helper_functions import *
from global_variables import *
from update import *
from static import *
from encoder import *
from select import Srg

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
    def immediate_stop(self):
        with self.condition:
            self.running = False
            self.paused = False
            self.condition.notify_all()

def main(stdscr):

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK) 

    clock_state = [False]
    clock_cycle = [0]
    instruction_address = [0]
    value = [0]
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

        # -----------------RISING EDGE-----------------
        if clock_state[0]:  
            update_clock(clk, freq, color("yellow"))
            
            if clock_cycle[0]==0: # 1
                # Epc
                PCState = color("green")
                update_PCData(pc, PCData, PCState)
            elif clock_cycle[0]==1: # 2
                # RD
                instruction_address[0] = extMemData[MRData]
                extMemState[MRData] = color("green")
                update_ExtMemData(ext_mem_display, extMemData, extMemState)

            elif clock_cycle[0]==2:
                # nop-3
                if MPSeqData == encode_IRtoMPS(0x00):
                    pass
                # adi,sbi,xri,ani,ori,cmi-3
                if MPSeqData in [encode_IRtoMPS(0x01), encode_IRtoMPS(0x02), encode_IRtoMPS(0x03), encode_IRtoMPS(0x04), encode_IRtoMPS(0x05), encode_IRtoMPS(0x06)]:
                    # Epc
                    PCState = color("green")
                    update_PCData(pc, PCData, PCState)
                # stop-3
                if MPSeqData == encode_IRtoMPS(0x07):
                    pass
                # movs-3
                if MPSeqData in [encode_IRtoMPS(0x70), encode_IRtoMPS(0x71), encode_IRtoMPS(0x72), encode_IRtoMPS(0x73), encode_IRtoMPS(0x74), encode_IRtoMPS(0x75), encode_IRtoMPS(0x76), encode_IRtoMPS(0x77), encode_IRtoMPS(0x78), encode_IRtoMPS(0x79), encode_IRtoMPS(0x7A), encode_IRtoMPS(0x7B), encode_IRtoMPS(0x7C), encode_IRtoMPS(0x7D), encode_IRtoMPS(0x7E), encode_IRtoMPS(0x7F)]:
                    # Erg
                    RegNum = Srg(MPSeqData)
                    value[0] = RGData[RegNum]
                    RGState[RegNum] = color("green")
                    update_RGData(r_arr, RGData, RGState)
                # movd-3
                if MPSeqData in [encode_IRtoMPS(0x80), encode_IRtoMPS(0x81), encode_IRtoMPS(0x82), encode_IRtoMPS(0x83), encode_IRtoMPS(0x84), encode_IRtoMPS(0x85), encode_IRtoMPS(0x86), encode_IRtoMPS(0x87), encode_IRtoMPS(0x88), encode_IRtoMPS(0x89), encode_IRtoMPS(0x8A), encode_IRtoMPS(0x8B), encode_IRtoMPS(0x8C), encode_IRtoMPS(0x8D), encode_IRtoMPS(0x8E), encode_IRtoMPS(0x8F)]:
                    #Ear
                    value[0] = ARData
                    ARState = color("green")
                    update_ARData(ac_r, ARData, ARState)
                # movi-3
                elif MPSeqData in [encode_IRtoMPS(0x90), encode_IRtoMPS(0x91), encode_IRtoMPS(0x92), encode_IRtoMPS(0x93), encode_IRtoMPS(0x94), encode_IRtoMPS(0x95), encode_IRtoMPS(0x96), encode_IRtoMPS(0x97), encode_IRtoMPS(0x98), encode_IRtoMPS(0x99), encode_IRtoMPS(0x9A), encode_IRtoMPS(0x9B), encode_IRtoMPS(0x9C), encode_IRtoMPS(0x9D), encode_IRtoMPS(0x9E), encode_IRtoMPS(0x9F)]:
                    # Epc
                    PCState = color("green")
                    update_PCData(pc, PCData, PCState)

            elif clock_cycle[0]==3:
                # adi,sbi,xri,ani,ori,cmi-4
                if MPSeqData in [encode_IRtoMPS(0x01)+1, encode_IRtoMPS(0x02)+1, encode_IRtoMPS(0x03)+1, encode_IRtoMPS(0x04)+1, encode_IRtoMPS(0x05)+1, encode_IRtoMPS(0x06)+1]:
                    # RD
                    value[0] = extMemData[MRData]
                    extMemState[MRData] = color("green")
                    update_ExtMemData(ext_mem_display, extMemData, extMemState)
                # movi-4
                if MPSeqData in  [encode_IRtoMPS(0x90)+1, encode_IRtoMPS(0x91)+1, encode_IRtoMPS(0x92)+1, encode_IRtoMPS(0x93)+1, encode_IRtoMPS(0x94)+1, encode_IRtoMPS(0x95)+1, encode_IRtoMPS(0x96)+1, encode_IRtoMPS(0x97)+1, encode_IRtoMPS(0x98)+1, encode_IRtoMPS(0x99)+1, encode_IRtoMPS(0x9A)+1, encode_IRtoMPS(0x9B)+1, encode_IRtoMPS(0x9C)+1, encode_IRtoMPS(0x9D)+1, encode_IRtoMPS(0x9E)+1, encode_IRtoMPS(0x9F)+1]:
                    # RD 
                    value[0] = extMemData[MRData]
                    extMemState[MRData] = color("green")
                    update_ExtMemData(ext_mem_display, extMemData, extMemState)
            
            elif clock_cycle[0]==4:
                # adi,sbi,xri,ani,ori,cmi-5
                if MPSeqData in [encode_IRtoMPS(0x01)+2, encode_IRtoMPS(0x02)+2, encode_IRtoMPS(0x03)+2, encode_IRtoMPS(0x04)+2, encode_IRtoMPS(0x05)+2, encode_IRtoMPS(0x06)+2]:
                    # Eor
                    ALUData[0] = ORData
                    ORState = color("green")
                    update_ORData(op_r, ORData, ORState)
                    # Ear
                    ALUData[1] = ARData
                    ARState = color("green")
                    update_ARData(ac_r, ARData, ARState)
                    if MPSeqData==encode_IRtoMPS(0x01)+2: ALUData[2] = ALUData[0]+ALUData[1]; ALUState = 1
                    if MPSeqData==encode_IRtoMPS(0x02)+2: ALUData[2] = ALUData[1]-ALUData[0]; ALUState = 2
                    if MPSeqData==encode_IRtoMPS(0x03)+2: ALUData[2] = ALUData[0]^ALUData[1]; ALUState = 3
                    if MPSeqData==encode_IRtoMPS(0x04)+2: ALUData[2] = ALUData[0]&ALUData[1]; ALUState = 4
                    if MPSeqData==encode_IRtoMPS(0x05)+2: ALUData[2] = ALUData[0]|ALUData[1]; ALUState = 5
                    if MPSeqData==encode_IRtoMPS(0x06)+2: ALUData[2] = ALUData[1]-ALUData[0]; ALUState = 6
                    update_ALUData(alu, ALUData, ALUState)

    
        # -----------------FALLING EDGE-----------------
        else:
            update_clock(clk, freq, color("white"))

            if clock_cycle[0]==0: # 1
                # Lmr
                MRData = PCData
                update_MRData(ma_r, MRData, color("blue"))
                # Ipc
                PCData += 1
                update_PCData(pc, PCData, color("yellow"))
            elif clock_cycle[0]==1: # 2
                # Lir
                IRData = instruction_address[0]
                update_IRData(i_r, IRData, color("blue"))
                # Lms
                MPSeqData = encode_IRtoMPS(IRData)
                MPMemData = encode_MPStoCSSig(MPSeqData)
                update_MPSeqData(mp_s, MPSeqData, color("blue"))
                update_MPMemData(mp_mem, MPMemData)

            elif clock_cycle[0]==2:
                # nop-3
                if MPSeqData == encode_IRtoMPS(0x00):
                    # End
                    clock_cycle[0] = -1
                # adi,sbi,xri,ani,ori,cmi-3
                if MPSeqData in [encode_IRtoMPS(0x01), encode_IRtoMPS(0x02), encode_IRtoMPS(0x03), encode_IRtoMPS(0x04), encode_IRtoMPS(0x05), encode_IRtoMPS(0x06)]:
                    # Lmr
                    MRData = PCData
                    update_MRData(ma_r, MRData, color("blue"))
                    # Ipc
                    PCData += 1
                    update_PCData(pc, PCData, color("yellow"))
                # stop-3
                if MPSeqData == encode_IRtoMPS(0x07):
                    # End
                    clock_cycle[0] = -1
                    # Stop Clock
                    clock.immediate_stop()
                # movs-3
                if MPSeqData in [encode_IRtoMPS(0x70), encode_IRtoMPS(0x71), encode_IRtoMPS(0x72), encode_IRtoMPS(0x73), encode_IRtoMPS(0x74), encode_IRtoMPS(0x75), encode_IRtoMPS(0x76), encode_IRtoMPS(0x77), encode_IRtoMPS(0x78), encode_IRtoMPS(0x79), encode_IRtoMPS(0x7A), encode_IRtoMPS(0x7B), encode_IRtoMPS(0x7C), encode_IRtoMPS(0x7D), encode_IRtoMPS(0x7E), encode_IRtoMPS(0x7F)]:
                    # Lar
                    ARData = value[0]
                    ARState = color("blue")
                    update_ARData(ac_r, ARData, ARState)
                    # End
                    clock_cycle[0] = -1 
                # movd-3
                if MPSeqData in [encode_IRtoMPS(0x80), encode_IRtoMPS(0x81), encode_IRtoMPS(0x82), encode_IRtoMPS(0x83), encode_IRtoMPS(0x84), encode_IRtoMPS(0x85), encode_IRtoMPS(0x86), encode_IRtoMPS(0x87), encode_IRtoMPS(0x88), encode_IRtoMPS(0x89), encode_IRtoMPS(0x8A), encode_IRtoMPS(0x8B), encode_IRtoMPS(0x8C), encode_IRtoMPS(0x8D), encode_IRtoMPS(0x8E), encode_IRtoMPS(0x8F)]:
                    # Lrg
                    RegNum = Srg(MPSeqData)
                    RGData[RegNum] = value[0]
                    RGState[RegNum] = color("blue")
                    update_RGData(r_arr, RGData, RGState)
                    # End
                    clock_cycle[0] = -1
                # movi-3
                if MPSeqData in [encode_IRtoMPS(0x90), encode_IRtoMPS(0x91), encode_IRtoMPS(0x92), encode_IRtoMPS(0x93), encode_IRtoMPS(0x94), encode_IRtoMPS(0x95), encode_IRtoMPS(0x96), encode_IRtoMPS(0x97), encode_IRtoMPS(0x98), encode_IRtoMPS(0x99), encode_IRtoMPS(0x9A), encode_IRtoMPS(0x9B), encode_IRtoMPS(0x9C), encode_IRtoMPS(0x9D), encode_IRtoMPS(0x9E), encode_IRtoMPS(0x9F)]:
                    # Lmr
                    MRData = PCData
                    update_MRData(ma_r, MRData, color("blue"))
                    # Ipc
                    PCData += 1
                    update_PCData(pc, PCData, color("yellow"))
                
                MPSeqData += 1
                update_MPSeqData(mp_s, MPSeqData, color("blue"))
                MPMemData = encode_MPStoCSSig(MPSeqData)
                update_MPMemData(mp_mem, MPMemData)

            elif clock_cycle[0]==3:
                # adi,sbi,xri,ani,ori,cmi-4
                if MPSeqData in [encode_IRtoMPS(0x01)+1, encode_IRtoMPS(0x02)+1, encode_IRtoMPS(0x03)+1, encode_IRtoMPS(0x04)+1, encode_IRtoMPS(0x05)+1, encode_IRtoMPS(0x06)+1]:
                    # Lor
                    ORData = value[0]
                    ORState = color("blue")
                    update_ORData(op_r, ORData, ORState)
                # movi-4
                if MPSeqData in [encode_IRtoMPS(0x90)+1, encode_IRtoMPS(0x91)+1, encode_IRtoMPS(0x92)+1, encode_IRtoMPS(0x93)+1, encode_IRtoMPS(0x94)+1, encode_IRtoMPS(0x95)+1, encode_IRtoMPS(0x96)+1, encode_IRtoMPS(0x97)+1, encode_IRtoMPS(0x98)+1, encode_IRtoMPS(0x99)+1, encode_IRtoMPS(0x9A)+1, encode_IRtoMPS(0x9B)+1, encode_IRtoMPS(0x9C)+1, encode_IRtoMPS(0x9D)+1, encode_IRtoMPS(0x9E)+1, encode_IRtoMPS(0x9F)+1]:
                    RegNum = Srg(MPSeqData)
                    # Lrg
                    RGData[RegNum] = value[0]
                    RGState[RegNum] = color("blue")
                    update_RGData(r_arr, RGData, RGState)
                    # End
                    clock_cycle[0] = -1
                
                MPSeqData += 1
                update_MPSeqData(mp_s, MPSeqData, color("blue"))
                MPMemData = encode_MPStoCSSig(MPSeqData)
                update_MPMemData(mp_mem, MPMemData)


            elif clock_cycle[0]==4:
                # adi,sbi,xri,ani,ori-5
                if MPSeqData in [encode_IRtoMPS(0x01)+2, encode_IRtoMPS(0x02)+2, encode_IRtoMPS(0x03)+2, encode_IRtoMPS(0x04)+2, encode_IRtoMPS(0x05)+2]:
                    # Lar
                    ARData = ALUData[2]
                    ARState = color("blue")
                    update_ARData(ac_r, ARData, ARState)
                    # End
                    clock_cycle[0] = -1
                if MPSeqData == encode_IRtoMPS(0x06)+2:
                    # End
                    clock_cycle[0] = -1
                
                MPSeqData += 1
                update_MPSeqData(mp_s, MPSeqData, color("blue"))
                MPMemData = encode_MPStoCSSig(MPSeqData)
                update_MPMemData(mp_mem, MPMemData)

            
            clock_cycle[0] = (clock_cycle[0]+1)%5

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