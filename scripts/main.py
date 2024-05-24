import curses
import threading
import time
import os.path as osp

from helper_functions import *
from global_variables import *
from update import *
from static import *
from encoder import *
from select import Srg, Sfl

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

    # upload program to memory
    with open(osp.join("program","compiled_code.txt"),'r') as f:
        i = 0
        for line in f.readlines():
            extMemData[i] = int(line,16)
            i += 1

    clock_state = [False]
    clock_cycle = [0]
    address = [0]
    value = [0]
    freq = 100

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
                address[0] = extMemData[MRData]
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
                # add,sub,xor,and,or,cmp-3
                if MPSeqData in [encode_IRtoMPS(0x10),encode_IRtoMPS(0x11),encode_IRtoMPS(0x12),encode_IRtoMPS(0x13),encode_IRtoMPS(0x14),encode_IRtoMPS(0x15),encode_IRtoMPS(0x16),encode_IRtoMPS(0x17),encode_IRtoMPS(0x18),encode_IRtoMPS(0x19),encode_IRtoMPS(0x1a),encode_IRtoMPS(0x1b),encode_IRtoMPS(0x1c),encode_IRtoMPS(0x1d),encode_IRtoMPS(0x1e),encode_IRtoMPS(0x1f),encode_IRtoMPS(0x20),encode_IRtoMPS(0x21),encode_IRtoMPS(0x22),encode_IRtoMPS(0x23),encode_IRtoMPS(0x24),encode_IRtoMPS(0x25),encode_IRtoMPS(0x26),encode_IRtoMPS(0x27),encode_IRtoMPS(0x28),encode_IRtoMPS(0x29),encode_IRtoMPS(0x2a),encode_IRtoMPS(0x2b),encode_IRtoMPS(0x2c),encode_IRtoMPS(0x2d),encode_IRtoMPS(0x2e),encode_IRtoMPS(0x2f),encode_IRtoMPS(0x30),encode_IRtoMPS(0x31),encode_IRtoMPS(0x32),encode_IRtoMPS(0x33),encode_IRtoMPS(0x34),encode_IRtoMPS(0x35),encode_IRtoMPS(0x36),encode_IRtoMPS(0x37),encode_IRtoMPS(0x38),encode_IRtoMPS(0x39),encode_IRtoMPS(0x3a),encode_IRtoMPS(0x3b),encode_IRtoMPS(0x3c),encode_IRtoMPS(0x3d),encode_IRtoMPS(0x3e),encode_IRtoMPS(0x3f),encode_IRtoMPS(0x40),encode_IRtoMPS(0x41),encode_IRtoMPS(0x42),encode_IRtoMPS(0x43),encode_IRtoMPS(0x44),encode_IRtoMPS(0x45),encode_IRtoMPS(0x46),encode_IRtoMPS(0x47),encode_IRtoMPS(0x48),encode_IRtoMPS(0x49),encode_IRtoMPS(0x4a),encode_IRtoMPS(0x4b),encode_IRtoMPS(0x4c),encode_IRtoMPS(0x4d),encode_IRtoMPS(0x4e),encode_IRtoMPS(0x4f),encode_IRtoMPS(0x50),encode_IRtoMPS(0x51),encode_IRtoMPS(0x52),encode_IRtoMPS(0x53),encode_IRtoMPS(0x54),encode_IRtoMPS(0x55),encode_IRtoMPS(0x56),encode_IRtoMPS(0x57),encode_IRtoMPS(0x58),encode_IRtoMPS(0x59),encode_IRtoMPS(0x5a),encode_IRtoMPS(0x5b),encode_IRtoMPS(0x5c),encode_IRtoMPS(0x5d),encode_IRtoMPS(0x5e),encode_IRtoMPS(0x5f),encode_IRtoMPS(0x60),encode_IRtoMPS(0x61),encode_IRtoMPS(0x62),encode_IRtoMPS(0x63),encode_IRtoMPS(0x64),encode_IRtoMPS(0x65),encode_IRtoMPS(0x66),encode_IRtoMPS(0x67),encode_IRtoMPS(0x68),encode_IRtoMPS(0x69),encode_IRtoMPS(0x6a),encode_IRtoMPS(0x6b),encode_IRtoMPS(0x6c),encode_IRtoMPS(0x6d),encode_IRtoMPS(0x6e),encode_IRtoMPS(0x6f)]:
                    # Erg
                    RegNum = Srg(MPSeqData)
                    value[0] = RGData[RegNum]
                    RGState[RegNum] = color("green")
                    update_RGData(r_arr, RGData, RGState)
                # movs-3
                if MPSeqData in [encode_IRtoMPS(0x70), encode_IRtoMPS(0x71), encode_IRtoMPS(0x72), encode_IRtoMPS(0x73), encode_IRtoMPS(0x74), encode_IRtoMPS(0x75), encode_IRtoMPS(0x76), encode_IRtoMPS(0x77), encode_IRtoMPS(0x78), encode_IRtoMPS(0x79), encode_IRtoMPS(0x7A), encode_IRtoMPS(0x7B), encode_IRtoMPS(0x7C), encode_IRtoMPS(0x7D), encode_IRtoMPS(0x7E), encode_IRtoMPS(0x7F)]:
                    # Erg
                    RegNum = Srg(MPSeqData)
                    value[0] = RGData[RegNum]
                    RGState[RegNum] = color("green")
                    update_RGData(r_arr, RGData, RGState)
                    ALUData[1] = ARData
                    ALUData[2] = ALUData[1]
                    ALUState = 0
                    update_ALUData(alu, ALUData, ALUState)
                    if ALUData[2]<0: FRData[0] = 1 # S
                    else: FRData[0] = 0
                    if ALUData[2]==0: FRData[1] = 1 # Z
                    else: FRData[1] = 0
                    if ALUData[2]!=0: FRData[4] = 1 # N
                    else: FRData[4] = 0
                    if parity(ALUData[2])==1: FRData[5] = 1 # P
                    else: FRData[5] = 0
                    if ALUData[2]>127: FRData[7] = 1 # C
                    else: FRData[7] = 0
                    ALUData[2] &= 0xff # twos complement
                    update_FRData(f_r, FRData)
                # movd-3
                if MPSeqData in [encode_IRtoMPS(0x80), encode_IRtoMPS(0x81), encode_IRtoMPS(0x82), encode_IRtoMPS(0x83), encode_IRtoMPS(0x84), encode_IRtoMPS(0x85), encode_IRtoMPS(0x86), encode_IRtoMPS(0x87), encode_IRtoMPS(0x88), encode_IRtoMPS(0x89), encode_IRtoMPS(0x8A), encode_IRtoMPS(0x8B), encode_IRtoMPS(0x8C), encode_IRtoMPS(0x8D), encode_IRtoMPS(0x8E), encode_IRtoMPS(0x8F)]:
                    # Ear
                    value[0] = ARData
                    ARState = color("green")
                    update_ARData(ac_r, ARData, ARState)
                # movi-3
                if MPSeqData in [encode_IRtoMPS(0x90), encode_IRtoMPS(0x91), encode_IRtoMPS(0x92), encode_IRtoMPS(0x93), encode_IRtoMPS(0x94), encode_IRtoMPS(0x95), encode_IRtoMPS(0x96), encode_IRtoMPS(0x97), encode_IRtoMPS(0x98), encode_IRtoMPS(0x99), encode_IRtoMPS(0x9A), encode_IRtoMPS(0x9B), encode_IRtoMPS(0x9C), encode_IRtoMPS(0x9D), encode_IRtoMPS(0x9E), encode_IRtoMPS(0x9F)]:
                    # Epc
                    PCState = color("green")
                    update_PCData(pc, PCData, PCState)
                # stor-3
                if MPSeqData in [encode_IRtoMPS(0xa0),encode_IRtoMPS(0xa1),encode_IRtoMPS(0xa2),encode_IRtoMPS(0xa3),encode_IRtoMPS(0xa4),encode_IRtoMPS(0xa5),encode_IRtoMPS(0xa6),encode_IRtoMPS(0xa7),encode_IRtoMPS(0xa8),encode_IRtoMPS(0xa9),encode_IRtoMPS(0xaa),encode_IRtoMPS(0xab),encode_IRtoMPS(0xac),encode_IRtoMPS(0xad),encode_IRtoMPS(0xae),encode_IRtoMPS(0xaf),encode_IRtoMPS(0xb0),encode_IRtoMPS(0xb1),encode_IRtoMPS(0xb2),encode_IRtoMPS(0xb3),encode_IRtoMPS(0xb4),encode_IRtoMPS(0xb5),encode_IRtoMPS(0xb6),encode_IRtoMPS(0xb7),encode_IRtoMPS(0xb8),encode_IRtoMPS(0xb9),encode_IRtoMPS(0xba),encode_IRtoMPS(0xbb),encode_IRtoMPS(0xbc),encode_IRtoMPS(0xbd),encode_IRtoMPS(0xbe),encode_IRtoMPS(0xbf)]:
                    # Ear
                    address[0] = ARData
                    ARState = color("green")
                    update_ARData(ac_r, ARData, ARState)   
                # pop-3
                if MPSeqData in [encode_IRtoMPS(0xd0),encode_IRtoMPS(0xd1),encode_IRtoMPS(0xd2),encode_IRtoMPS(0xd3),encode_IRtoMPS(0xd4),encode_IRtoMPS(0xd5),encode_IRtoMPS(0xd6),encode_IRtoMPS(0xd7),encode_IRtoMPS(0xd8),encode_IRtoMPS(0xd9),encode_IRtoMPS(0xda),encode_IRtoMPS(0xdb),encode_IRtoMPS(0xdc),encode_IRtoMPS(0xdd),encode_IRtoMPS(0xde),encode_IRtoMPS(0xdf)]:
                    # Esp
                    address[0] = SPData
                    SPState = color("green")
                    update_SPData(sp, SPData, SPState)
                # jumpd-3
                if MPSeqData in [encode_IRtoMPS(0xe0),encode_IRtoMPS(0xe1),encode_IRtoMPS(0xe2),encode_IRtoMPS(0xe3),encode_IRtoMPS(0xe4),encode_IRtoMPS(0xe5),encode_IRtoMPS(0xe6),encode_IRtoMPS(0xe7)]:
                    # Epc
                    PCState = color("green")
                    update_PCData(pc, PCData, PCState)
                # cd-3
                if MPSeqData in [encode_IRtoMPS(0xf0),encode_IRtoMPS(0xf1),encode_IRtoMPS(0xf2),encode_IRtoMPS(0xf3),encode_IRtoMPS(0xf4),encode_IRtoMPS(0xf5),encode_IRtoMPS(0xf6),encode_IRtoMPS(0xf7)]:
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
                # ret-4
                if MPSeqData in [encode_IRtoMPS(0x08)+1,encode_IRtoMPS(0x09)+1,encode_IRtoMPS(0x0a)+1,encode_IRtoMPS(0x0b)+1,encode_IRtoMPS(0x0c)+1,encode_IRtoMPS(0x0d)+1,encode_IRtoMPS(0x0e)+1,encode_IRtoMPS(0x0f)+1]:
                    # Esp
                    address[0] = SPData
                    SPState = color("green")
                    update_SPData(sp, SPData, SPState)
                # add,sub,xor,and,or,cmp-4
                if MPSeqData in [encode_IRtoMPS(0x10)+1,encode_IRtoMPS(0x11)+1,encode_IRtoMPS(0x12)+1,encode_IRtoMPS(0x13)+1,encode_IRtoMPS(0x14)+1,encode_IRtoMPS(0x15)+1,encode_IRtoMPS(0x16)+1,encode_IRtoMPS(0x17)+1,encode_IRtoMPS(0x18)+1,encode_IRtoMPS(0x19)+1,encode_IRtoMPS(0x1a)+1,encode_IRtoMPS(0x1b)+1,encode_IRtoMPS(0x1c)+1,encode_IRtoMPS(0x1d)+1,encode_IRtoMPS(0x1e)+1,encode_IRtoMPS(0x1f)+1,encode_IRtoMPS(0x20)+1,encode_IRtoMPS(0x21)+1,encode_IRtoMPS(0x22)+1,encode_IRtoMPS(0x23)+1,encode_IRtoMPS(0x24)+1,encode_IRtoMPS(0x25)+1,encode_IRtoMPS(0x26)+1,encode_IRtoMPS(0x27)+1,encode_IRtoMPS(0x28)+1,encode_IRtoMPS(0x29)+1,encode_IRtoMPS(0x2a)+1,encode_IRtoMPS(0x2b)+1,encode_IRtoMPS(0x2c)+1,encode_IRtoMPS(0x2d)+1,encode_IRtoMPS(0x2e)+1,encode_IRtoMPS(0x2f)+1,encode_IRtoMPS(0x30)+1,encode_IRtoMPS(0x31)+1,encode_IRtoMPS(0x32)+1,encode_IRtoMPS(0x33)+1,encode_IRtoMPS(0x34)+1,encode_IRtoMPS(0x35)+1,encode_IRtoMPS(0x36)+1,encode_IRtoMPS(0x37)+1,encode_IRtoMPS(0x38)+1,encode_IRtoMPS(0x39)+1,encode_IRtoMPS(0x3a)+1,encode_IRtoMPS(0x3b)+1,encode_IRtoMPS(0x3c)+1,encode_IRtoMPS(0x3d)+1,encode_IRtoMPS(0x3e)+1,encode_IRtoMPS(0x3f)+1,encode_IRtoMPS(0x40)+1,encode_IRtoMPS(0x41)+1,encode_IRtoMPS(0x42)+1,encode_IRtoMPS(0x43)+1,encode_IRtoMPS(0x44)+1,encode_IRtoMPS(0x45)+1,encode_IRtoMPS(0x46)+1,encode_IRtoMPS(0x47)+1,encode_IRtoMPS(0x48)+1,encode_IRtoMPS(0x49)+1,encode_IRtoMPS(0x4a)+1,encode_IRtoMPS(0x4b)+1,encode_IRtoMPS(0x4c)+1,encode_IRtoMPS(0x4d)+1,encode_IRtoMPS(0x4e)+1,encode_IRtoMPS(0x4f)+1,encode_IRtoMPS(0x50)+1,encode_IRtoMPS(0x51)+1,encode_IRtoMPS(0x52)+1,encode_IRtoMPS(0x53)+1,encode_IRtoMPS(0x54)+1,encode_IRtoMPS(0x55)+1,encode_IRtoMPS(0x56)+1,encode_IRtoMPS(0x57)+1,encode_IRtoMPS(0x58)+1,encode_IRtoMPS(0x59)+1,encode_IRtoMPS(0x5a)+1,encode_IRtoMPS(0x5b)+1,encode_IRtoMPS(0x5c)+1,encode_IRtoMPS(0x5d)+1,encode_IRtoMPS(0x5e)+1,encode_IRtoMPS(0x5f)+1,encode_IRtoMPS(0x60)+1,encode_IRtoMPS(0x61)+1,encode_IRtoMPS(0x62)+1,encode_IRtoMPS(0x63)+1,encode_IRtoMPS(0x64)+1,encode_IRtoMPS(0x65)+1,encode_IRtoMPS(0x66)+1,encode_IRtoMPS(0x67)+1,encode_IRtoMPS(0x68)+1,encode_IRtoMPS(0x69)+1,encode_IRtoMPS(0x6a)+1,encode_IRtoMPS(0x6b)+1,encode_IRtoMPS(0x6c)+1,encode_IRtoMPS(0x6d)+1,encode_IRtoMPS(0x6e)+1,encode_IRtoMPS(0x6f)+1]:
                    # Eor
                    ALUData[0] = ORData
                    ORState = color("green")
                    update_ORData(op_r, ORData, ORState)
                    # Ear
                    ALUData[1] = ARData
                    ARState = color("green")
                    update_ARData(ac_r, ARData, ARState)
                    if MPSeqData in [encode_IRtoMPS(0x30)+1,encode_IRtoMPS(0x31)+1,encode_IRtoMPS(0x32)+1,encode_IRtoMPS(0x33)+1,encode_IRtoMPS(0x34)+1,encode_IRtoMPS(0x35)+1,encode_IRtoMPS(0x36)+1,encode_IRtoMPS(0x37)+1,encode_IRtoMPS(0x38)+1,encode_IRtoMPS(0x39)+1,encode_IRtoMPS(0x3a)+1,encode_IRtoMPS(0x3b)+1,encode_IRtoMPS(0x3c)+1,encode_IRtoMPS(0x3d)+1,encode_IRtoMPS(0x3e)+1,encode_IRtoMPS(0x3f)+1]: 
                        ALUData[2] = ALUData[0]^ALUData[1] 
                        ALUState = 3
                    if MPSeqData in [encode_IRtoMPS(0x40)+1,encode_IRtoMPS(0x41)+1,encode_IRtoMPS(0x42)+1,encode_IRtoMPS(0x43)+1,encode_IRtoMPS(0x44)+1,encode_IRtoMPS(0x45)+1,encode_IRtoMPS(0x46)+1,encode_IRtoMPS(0x47)+1,encode_IRtoMPS(0x48)+1,encode_IRtoMPS(0x49)+1,encode_IRtoMPS(0x4a)+1,encode_IRtoMPS(0x4b)+1,encode_IRtoMPS(0x4c)+1,encode_IRtoMPS(0x4d)+1,encode_IRtoMPS(0x4e)+1,encode_IRtoMPS(0x4f)+1]: 
                        ALUData[2] = ALUData[0]&ALUData[1]
                        ALUState = 4
                    if MPSeqData in [encode_IRtoMPS(0x50)+1,encode_IRtoMPS(0x51)+1,encode_IRtoMPS(0x52)+1,encode_IRtoMPS(0x53)+1,encode_IRtoMPS(0x54)+1,encode_IRtoMPS(0x55)+1,encode_IRtoMPS(0x56)+1,encode_IRtoMPS(0x57)+1,encode_IRtoMPS(0x58)+1,encode_IRtoMPS(0x59)+1,encode_IRtoMPS(0x5a)+1,encode_IRtoMPS(0x5b)+1,encode_IRtoMPS(0x5c)+1,encode_IRtoMPS(0x5d)+1,encode_IRtoMPS(0x5e)+1,encode_IRtoMPS(0x5f)+1]: 
                        ALUData[2] = ALUData[0]|ALUData[1]
                        ALUState = 5
                    if MPSeqData in [encode_IRtoMPS(0x10)+1,encode_IRtoMPS(0x11)+1,encode_IRtoMPS(0x12)+1,encode_IRtoMPS(0x13)+1,encode_IRtoMPS(0x14)+1,encode_IRtoMPS(0x15)+1,encode_IRtoMPS(0x16)+1,encode_IRtoMPS(0x17)+1,encode_IRtoMPS(0x18)+1,encode_IRtoMPS(0x19)+1,encode_IRtoMPS(0x1a)+1,encode_IRtoMPS(0x1b)+1,encode_IRtoMPS(0x1c)+1,encode_IRtoMPS(0x1d)+1,encode_IRtoMPS(0x1e)+1,encode_IRtoMPS(0x1f)+1]: 
                        ALUState = 1
                    if MPSeqData in [encode_IRtoMPS(0x20)+1,encode_IRtoMPS(0x21)+1,encode_IRtoMPS(0x22)+1,encode_IRtoMPS(0x23)+1,encode_IRtoMPS(0x24)+1,encode_IRtoMPS(0x25)+1,encode_IRtoMPS(0x26)+1,encode_IRtoMPS(0x27)+1,encode_IRtoMPS(0x28)+1,encode_IRtoMPS(0x29)+1,encode_IRtoMPS(0x2a)+1,encode_IRtoMPS(0x2b)+1,encode_IRtoMPS(0x2c)+1,encode_IRtoMPS(0x2d)+1,encode_IRtoMPS(0x2e)+1,encode_IRtoMPS(0x2f)+1]: 
                        ALUState = 2
                    if MPSeqData in [encode_IRtoMPS(0x60)+1,encode_IRtoMPS(0x61)+1,encode_IRtoMPS(0x62)+1,encode_IRtoMPS(0x63)+1,encode_IRtoMPS(0x64)+1,encode_IRtoMPS(0x65)+1,encode_IRtoMPS(0x66)+1,encode_IRtoMPS(0x67)+1,encode_IRtoMPS(0x68)+1,encode_IRtoMPS(0x69)+1,encode_IRtoMPS(0x6a)+1,encode_IRtoMPS(0x6b)+1,encode_IRtoMPS(0x6c)+1,encode_IRtoMPS(0x6d)+1,encode_IRtoMPS(0x6e)+1,encode_IRtoMPS(0x6f)+1]: 
                        ALUState = 6
                    if MPSeqData in [encode_IRtoMPS(0x10)+1,encode_IRtoMPS(0x11)+1,encode_IRtoMPS(0x12)+1,encode_IRtoMPS(0x13)+1,encode_IRtoMPS(0x14)+1,encode_IRtoMPS(0x15)+1,encode_IRtoMPS(0x16)+1,encode_IRtoMPS(0x17)+1,encode_IRtoMPS(0x18)+1,encode_IRtoMPS(0x19)+1,encode_IRtoMPS(0x1a)+1,encode_IRtoMPS(0x1b)+1,encode_IRtoMPS(0x1c)+1,encode_IRtoMPS(0x1d)+1,encode_IRtoMPS(0x1e)+1,encode_IRtoMPS(0x1f)+1,encode_IRtoMPS(0x20)+1,encode_IRtoMPS(0x21)+1,encode_IRtoMPS(0x22)+1,encode_IRtoMPS(0x23)+1,encode_IRtoMPS(0x24)+1,encode_IRtoMPS(0x25)+1,encode_IRtoMPS(0x26)+1,encode_IRtoMPS(0x27)+1,encode_IRtoMPS(0x28)+1,encode_IRtoMPS(0x29)+1,encode_IRtoMPS(0x2a)+1,encode_IRtoMPS(0x2b)+1,encode_IRtoMPS(0x2c)+1,encode_IRtoMPS(0x2d)+1,encode_IRtoMPS(0x2e)+1,encode_IRtoMPS(0x2f)+1,encode_IRtoMPS(0x60)+1,encode_IRtoMPS(0x61)+1,encode_IRtoMPS(0x62)+1,encode_IRtoMPS(0x63)+1,encode_IRtoMPS(0x64)+1,encode_IRtoMPS(0x65)+1,encode_IRtoMPS(0x66)+1,encode_IRtoMPS(0x67)+1,encode_IRtoMPS(0x68)+1,encode_IRtoMPS(0x69)+1,encode_IRtoMPS(0x6a)+1,encode_IRtoMPS(0x6b)+1,encode_IRtoMPS(0x6c)+1,encode_IRtoMPS(0x6d)+1,encode_IRtoMPS(0x6e)+1,encode_IRtoMPS(0x6f)+1]:
                        a = ALUData[0]; b = ALUData[1]
                        if a&0x80: a=-((a^0xff)+1)
                        if b&0x80: b=-((b^0xff)+1)
                        if MPSeqData in [encode_IRtoMPS(0x10)+1,encode_IRtoMPS(0x11)+1,encode_IRtoMPS(0x12)+1,encode_IRtoMPS(0x13)+1,encode_IRtoMPS(0x14)+1,encode_IRtoMPS(0x15)+1,encode_IRtoMPS(0x16)+1,encode_IRtoMPS(0x17)+1,encode_IRtoMPS(0x18)+1,encode_IRtoMPS(0x19)+1,encode_IRtoMPS(0x1a)+1,encode_IRtoMPS(0x1b)+1,encode_IRtoMPS(0x1c)+1,encode_IRtoMPS(0x1d)+1,encode_IRtoMPS(0x1e)+1,encode_IRtoMPS(0x1f)+1]: 
                            ALUData[2] = a+b
                        else: ALUData[2] = b-a
                    if ALUData[2]<0: FRData[0] = 1 # S
                    else: FRData[0] = 0
                    if ALUData[2]==0: FRData[1] = 1 # Z
                    else: FRData[1] = 0
                    if ALUData[2]!=0: FRData[4] = 1 # N
                    else: FRData[4] = 0
                    if parity(ALUData[2])==1: FRData[5] = 1 # P
                    else: FRData[5] = 0
                    if ALUData[2]>127: FRData[7] = 1 # C
                    else: FRData[7] = 0
                    ALUData[2] &= 0xff # twos complement
                    update_ALUData(alu, ALUData, ALUState)
                    update_FRData(f_r, FRData)
                # movi-4
                if MPSeqData in  [encode_IRtoMPS(0x90)+1, encode_IRtoMPS(0x91)+1, encode_IRtoMPS(0x92)+1, encode_IRtoMPS(0x93)+1, encode_IRtoMPS(0x94)+1, encode_IRtoMPS(0x95)+1, encode_IRtoMPS(0x96)+1, encode_IRtoMPS(0x97)+1, encode_IRtoMPS(0x98)+1, encode_IRtoMPS(0x99)+1, encode_IRtoMPS(0x9A)+1, encode_IRtoMPS(0x9B)+1, encode_IRtoMPS(0x9C)+1, encode_IRtoMPS(0x9D)+1, encode_IRtoMPS(0x9E)+1, encode_IRtoMPS(0x9F)+1]:
                    # RD 
                    value[0] = extMemData[MRData]
                    extMemState[MRData] = color("red")
                    update_ExtMemData(ext_mem_display, extMemData, extMemState)
                # stor-4
                if MPSeqData in [encode_IRtoMPS(0xa0)+1,encode_IRtoMPS(0xa1)+1,encode_IRtoMPS(0xa2)+1,encode_IRtoMPS(0xa3)+1,encode_IRtoMPS(0xa4)+1,encode_IRtoMPS(0xa5)+1,encode_IRtoMPS(0xa6)+1,encode_IRtoMPS(0xa7)+1,encode_IRtoMPS(0xa8)+1,encode_IRtoMPS(0xa9)+1,encode_IRtoMPS(0xaa)+1,encode_IRtoMPS(0xab)+1,encode_IRtoMPS(0xac)+1,encode_IRtoMPS(0xad)+1,encode_IRtoMPS(0xae)+1,encode_IRtoMPS(0xaf)+1]:
                    # Erg
                    RegNum = Srg(MPSeqData)
                    address[0] = RGData[RegNum]
                    RGState[RegNum] = color("green")
                    update_RGData(r_arr, RGData, RGState)
                # load-4
                if MPSeqData in [encode_IRtoMPS(0xb0)+1,encode_IRtoMPS(0xb1)+1,encode_IRtoMPS(0xb2)+1,encode_IRtoMPS(0xb3)+1,encode_IRtoMPS(0xb4)+1,encode_IRtoMPS(0xb5)+1,encode_IRtoMPS(0xb6)+1,encode_IRtoMPS(0xb7)+1,encode_IRtoMPS(0xb8)+1,encode_IRtoMPS(0xb9)+1,encode_IRtoMPS(0xba)+1,encode_IRtoMPS(0xbb)+1,encode_IRtoMPS(0xbc)+1,encode_IRtoMPS(0xbd)+1,encode_IRtoMPS(0xbe)+1,encode_IRtoMPS(0xbf)+1]:
                    # RD
                    value[0] = extMemData[MRData]
                    extMemState[MRData] = color("red")
                    update_ExtMemData(ext_mem_display, extMemData, extMemState)
                # push-4
                if MPSeqData in [encode_IRtoMPS(0xc0)+1,encode_IRtoMPS(0xc1)+1,encode_IRtoMPS(0xc2)+1,encode_IRtoMPS(0xc3)+1,encode_IRtoMPS(0xc4)+1,encode_IRtoMPS(0xc5)+1,encode_IRtoMPS(0xc6)+1,encode_IRtoMPS(0xc7)+1,encode_IRtoMPS(0xc8)+1,encode_IRtoMPS(0xc9)+1,encode_IRtoMPS(0xca)+1,encode_IRtoMPS(0xcb)+1,encode_IRtoMPS(0xcc)+1,encode_IRtoMPS(0xcd)+1,encode_IRtoMPS(0xce)+1,encode_IRtoMPS(0xcf)+1]:
                    # Esp
                    address[0] = SPData
                    SPState = color("green")
                    update_SPData(sp, SPData, SPState)
                # pop-4
                if MPSeqData in [encode_IRtoMPS(0xd0)+1,encode_IRtoMPS(0xd1)+1,encode_IRtoMPS(0xd2)+1,encode_IRtoMPS(0xd3)+1,encode_IRtoMPS(0xd4)+1,encode_IRtoMPS(0xd5)+1,encode_IRtoMPS(0xd6)+1,encode_IRtoMPS(0xd7)+1,encode_IRtoMPS(0xd8)+1,encode_IRtoMPS(0xd9)+1,encode_IRtoMPS(0xda)+1,encode_IRtoMPS(0xdb)+1,encode_IRtoMPS(0xdc)+1,encode_IRtoMPS(0xdd)+1,encode_IRtoMPS(0xde)+1,encode_IRtoMPS(0xdf)+1]:
                    # RD
                    value[0] = extMemData[MRData]
                    extMemState[MRData] = color("red")
                    update_ExtMemData(ext_mem_display, extMemData, extMemState)
                # jumpd-4
                if MPSeqData in [encode_IRtoMPS(0xe0)+1,encode_IRtoMPS(0xe1)+1,encode_IRtoMPS(0xe2)+1,encode_IRtoMPS(0xe3)+1,encode_IRtoMPS(0xe4)+1,encode_IRtoMPS(0xe5)+1,encode_IRtoMPS(0xe6)+1,encode_IRtoMPS(0xe7)+1]:
                    # RD
                    address[0] = extMemData[MRData]
                    extMemState[MRData] = color("red")
                    update_ExtMemData(ext_mem_display, extMemData, extMemState)
                # jumpr-4
                if MPSeqData in [encode_IRtoMPS(0xe8)+1,encode_IRtoMPS(0xe9)+1,encode_IRtoMPS(0xea)+1,encode_IRtoMPS(0xeb)+1,encode_IRtoMPS(0xec)+1,encode_IRtoMPS(0xed)+1,encode_IRtoMPS(0xee)+1,encode_IRtoMPS(0xef)+1]:
                    # Ear
                    address[0] = ARData
                    ARState = color("green")
                    update_ARData(ac_r, ARData, ARState)
                # cd-4
                if MPSeqData in [encode_IRtoMPS(0xf0)+1,encode_IRtoMPS(0xf1)+1,encode_IRtoMPS(0xf2)+1,encode_IRtoMPS(0xf3)+1,encode_IRtoMPS(0xf4)+1,encode_IRtoMPS(0xf5)+1,encode_IRtoMPS(0xf6)+1,encode_IRtoMPS(0xf7)+1]:
                    # RD
                    address[0] = extMemData[MRData]
                    extMemState[MRData] = color("red")
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
                    if MPSeqData==encode_IRtoMPS(0x03)+2: ALUData[2] = ALUData[0]^ALUData[1]; ALUState = 3
                    if MPSeqData==encode_IRtoMPS(0x04)+2: ALUData[2] = ALUData[0]&ALUData[1]; ALUState = 4
                    if MPSeqData==encode_IRtoMPS(0x05)+2: ALUData[2] = ALUData[0]|ALUData[1]; ALUState = 5
                    if MPSeqData==encode_IRtoMPS(0x01)+2: ALUState = 1
                    if MPSeqData==encode_IRtoMPS(0x02)+2: ALUState = 2
                    if MPSeqData==encode_IRtoMPS(0x06)+2: ALUState = 6
                    if MPSeqData in [encode_IRtoMPS(0x01)+2, encode_IRtoMPS(0x02)+2, encode_IRtoMPS(0x06)+2]:
                        a = ALUData[0]; b = ALUData[1]
                        if a&0x80: a=-((a^0xff)+1)
                        if b&0x80: b=-((b^0xff)+1)
                        if MPSeqData==encode_IRtoMPS(0x01)+2: ALUData[2] = a+b
                        else: ALUData[2] = b-a
                    if ALUData[2]<0: FRData[0] = 1 # S
                    else: FRData[0] = 0
                    if ALUData[2]==0: FRData[1] = 1 # Z
                    else: FRData[1] = 0
                    if ALUData[2]!=0: FRData[4] = 1 # N
                    else: FRData[4] = 0
                    if parity(ALUData[2])==1: FRData[5] = 1 # P
                    else: FRData[5] = 0
                    if ALUData[2]>127: FRData[7] = 1 # C
                    else: FRData[7] = 0
                    ALUData[2] &= 0xff # twos complement
                    update_ALUData(alu, ALUData, ALUState)
                    update_FRData(f_r, FRData)
                # ret-5
                if MPSeqData in [encode_IRtoMPS(0x08)+2,encode_IRtoMPS(0x09)+2,encode_IRtoMPS(0x0a)+2,encode_IRtoMPS(0x0b)+2,encode_IRtoMPS(0x0c)+2,encode_IRtoMPS(0x0d)+2,encode_IRtoMPS(0x0e)+2,encode_IRtoMPS(0x0f)+2]:
                    # RD
                    address[0] = extMemData[MRData]
                    extMemData[MRState] = color("green")
                    update_ExtMemData(ext_mem_display, extMemData, extMemState)
                # push-5
                if MPSeqData in [encode_IRtoMPS(0xc0)+2,encode_IRtoMPS(0xc1)+2,encode_IRtoMPS(0xc2)+2,encode_IRtoMPS(0xc3)+2,encode_IRtoMPS(0xc4)+2,encode_IRtoMPS(0xc5)+2,encode_IRtoMPS(0xc6)+2,encode_IRtoMPS(0xc7)+2,encode_IRtoMPS(0xc8)+2,encode_IRtoMPS(0xc9)+2,encode_IRtoMPS(0xca)+2,encode_IRtoMPS(0xcb)+2,encode_IRtoMPS(0xcc)+2,encode_IRtoMPS(0xcd)+2,encode_IRtoMPS(0xce)+2,encode_IRtoMPS(0xcf)+2]:
                    # Erg
                    RegNum = Srg(MPSeqData)
                    value[0] = RGData[RegNum]
                    RGState[RegNum] = color("green")
                    update_RGData(r_arr, RGData, RGState)
                # cd,cr-5
                if MPSeqData in [encode_IRtoMPS(0xf0)+2,encode_IRtoMPS(0xf1)+2,encode_IRtoMPS(0xf2)+2,encode_IRtoMPS(0xf3)+2,encode_IRtoMPS(0xf4)+2,encode_IRtoMPS(0xf5)+2,encode_IRtoMPS(0xf6)+2,encode_IRtoMPS(0xf7)+2,encode_IRtoMPS(0xf8)+2,encode_IRtoMPS(0xf9)+2,encode_IRtoMPS(0xfa)+2,encode_IRtoMPS(0xfb)+2,encode_IRtoMPS(0xfc)+2,encode_IRtoMPS(0xfd)+2,encode_IRtoMPS(0xfe)+2,encode_IRtoMPS(0xff)+2]:
                    # Esp
                    address[0] = SPData
                    SPState = color("green")
                    update_SPData(sp, SPData, SPState)
            
            elif clock_cycle[0]==5:
                # cd,cr-6
                # Epc
                PCState = color("green")
                update_PCData(pc, PCData, PCState)

            elif clock_cycle[0]==6:
                # cd,cr-7
                # Ear
                address[0] = ARData
                ARState = color("green")
                update_ARData(ac_r, ARData, ARState)
    
        # -----------------FALLING EDGE-----------------
        else:
            update_clock(clk, freq, color("white"))

            if clock_cycle[0]==0: # 1
                # Lmr
                MRData = PCData
                MRState = color("blue")
                update_MRData(ma_r, MRData, MRState)
                # Ipc
                PCData += 1
                PCState = color("yellow")
                update_PCData(pc, PCData, PCState)
            elif clock_cycle[0]==1: # 2
                # Lir
                IRData = address[0]
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
                    MRState = color("blue")
                    update_MRData(ma_r, MRData, MRState)
                    # Ipc
                    PCData += 1
                    PCState = color("yellow")
                    update_PCData(pc, PCData, PCState)
                # stop-3
                if MPSeqData == encode_IRtoMPS(0x07):
                    # End
                    clock_cycle[0] = -1
                    # Stop Clock
                    clock.immediate_stop()
                # ret-3
                if MPSeqData in [encode_IRtoMPS(0x08),encode_IRtoMPS(0x09),encode_IRtoMPS(0x0a),encode_IRtoMPS(0x0b),encode_IRtoMPS(0x0c),encode_IRtoMPS(0x0d),encode_IRtoMPS(0x0e),encode_IRtoMPS(0x0f)]:
                    # Efl
                    flag = Sfl(MPSeqData)
                    if not FRData[flag]:
                        # End
                        clock_cycle[0] = -1                
                # add,sub,xor,and,or,cmp-3
                if MPSeqData in [encode_IRtoMPS(0x10),encode_IRtoMPS(0x11),encode_IRtoMPS(0x12),encode_IRtoMPS(0x13),encode_IRtoMPS(0x14),encode_IRtoMPS(0x15),encode_IRtoMPS(0x16),encode_IRtoMPS(0x17),encode_IRtoMPS(0x18),encode_IRtoMPS(0x19),encode_IRtoMPS(0x1a),encode_IRtoMPS(0x1b),encode_IRtoMPS(0x1c),encode_IRtoMPS(0x1d),encode_IRtoMPS(0x1e),encode_IRtoMPS(0x1f),encode_IRtoMPS(0x20),encode_IRtoMPS(0x21),encode_IRtoMPS(0x22),encode_IRtoMPS(0x23),encode_IRtoMPS(0x24),encode_IRtoMPS(0x25),encode_IRtoMPS(0x26),encode_IRtoMPS(0x27),encode_IRtoMPS(0x28),encode_IRtoMPS(0x29),encode_IRtoMPS(0x2a),encode_IRtoMPS(0x2b),encode_IRtoMPS(0x2c),encode_IRtoMPS(0x2d),encode_IRtoMPS(0x2e),encode_IRtoMPS(0x2f),encode_IRtoMPS(0x30),encode_IRtoMPS(0x31),encode_IRtoMPS(0x32),encode_IRtoMPS(0x33),encode_IRtoMPS(0x34),encode_IRtoMPS(0x35),encode_IRtoMPS(0x36),encode_IRtoMPS(0x37),encode_IRtoMPS(0x38),encode_IRtoMPS(0x39),encode_IRtoMPS(0x3a),encode_IRtoMPS(0x3b),encode_IRtoMPS(0x3c),encode_IRtoMPS(0x3d),encode_IRtoMPS(0x3e),encode_IRtoMPS(0x3f),encode_IRtoMPS(0x40),encode_IRtoMPS(0x41),encode_IRtoMPS(0x42),encode_IRtoMPS(0x43),encode_IRtoMPS(0x44),encode_IRtoMPS(0x45),encode_IRtoMPS(0x46),encode_IRtoMPS(0x47),encode_IRtoMPS(0x48),encode_IRtoMPS(0x49),encode_IRtoMPS(0x4a),encode_IRtoMPS(0x4b),encode_IRtoMPS(0x4c),encode_IRtoMPS(0x4d),encode_IRtoMPS(0x4e),encode_IRtoMPS(0x4f),encode_IRtoMPS(0x50),encode_IRtoMPS(0x51),encode_IRtoMPS(0x52),encode_IRtoMPS(0x53),encode_IRtoMPS(0x54),encode_IRtoMPS(0x55),encode_IRtoMPS(0x56),encode_IRtoMPS(0x57),encode_IRtoMPS(0x58),encode_IRtoMPS(0x59),encode_IRtoMPS(0x5a),encode_IRtoMPS(0x5b),encode_IRtoMPS(0x5c),encode_IRtoMPS(0x5d),encode_IRtoMPS(0x5e),encode_IRtoMPS(0x5f),encode_IRtoMPS(0x60),encode_IRtoMPS(0x61),encode_IRtoMPS(0x62),encode_IRtoMPS(0x63),encode_IRtoMPS(0x64),encode_IRtoMPS(0x65),encode_IRtoMPS(0x66),encode_IRtoMPS(0x67),encode_IRtoMPS(0x68),encode_IRtoMPS(0x69),encode_IRtoMPS(0x6a),encode_IRtoMPS(0x6b),encode_IRtoMPS(0x6c),encode_IRtoMPS(0x6d),encode_IRtoMPS(0x6e),encode_IRtoMPS(0x6f)]:
                    # Lor
                    ORData = value[0]
                    ORState = color("blue")
                    update_ORData(op_r, ORData, ORState)
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
                    MRState = color("blue")
                    update_MRData(ma_r, MRData, MRState)
                    # Ipc
                    PCData += 1
                    PCState = color("yellow")
                    update_PCData(pc, PCData, PCState)
                # stor,load-3
                if MPSeqData in [encode_IRtoMPS(0xa0),encode_IRtoMPS(0xa1),encode_IRtoMPS(0xa2),encode_IRtoMPS(0xa3),encode_IRtoMPS(0xa4),encode_IRtoMPS(0xa5),encode_IRtoMPS(0xa6),encode_IRtoMPS(0xa7),encode_IRtoMPS(0xa8),encode_IRtoMPS(0xa9),encode_IRtoMPS(0xaa),encode_IRtoMPS(0xab),encode_IRtoMPS(0xac),encode_IRtoMPS(0xad),encode_IRtoMPS(0xae),encode_IRtoMPS(0xaf),encode_IRtoMPS(0xb0),encode_IRtoMPS(0xb1),encode_IRtoMPS(0xb2),encode_IRtoMPS(0xb3),encode_IRtoMPS(0xb4),encode_IRtoMPS(0xb5),encode_IRtoMPS(0xb6),encode_IRtoMPS(0xb7),encode_IRtoMPS(0xb8),encode_IRtoMPS(0xb9),encode_IRtoMPS(0xba),encode_IRtoMPS(0xbb),encode_IRtoMPS(0xbc),encode_IRtoMPS(0xbd),encode_IRtoMPS(0xbe),encode_IRtoMPS(0xbf)]:
                    # Lmr
                    MRData = address[0]
                    MRState = color("blue")
                    update_MRData(ma_r, MRData, MRState)
                # push-3
                if MPSeqData in [encode_IRtoMPS(0xc0),encode_IRtoMPS(0xc1),encode_IRtoMPS(0xc2),encode_IRtoMPS(0xc3),encode_IRtoMPS(0xc4),encode_IRtoMPS(0xc5),encode_IRtoMPS(0xc6),encode_IRtoMPS(0xc7),encode_IRtoMPS(0xc8),encode_IRtoMPS(0xc9),encode_IRtoMPS(0xca),encode_IRtoMPS(0xcb),encode_IRtoMPS(0xcc),encode_IRtoMPS(0xcd),encode_IRtoMPS(0xce),encode_IRtoMPS(0xcf)]:
                    # Dsp
                    SPData -= 1
                    SPData &= 0xff
                    SPState = color("red")
                    update_SPData(sp, SPData, SPState)
                # pop-3
                if MPSeqData in [encode_IRtoMPS(0xd0),encode_IRtoMPS(0xd1),encode_IRtoMPS(0xd2),encode_IRtoMPS(0xd3),encode_IRtoMPS(0xd4),encode_IRtoMPS(0xd5),encode_IRtoMPS(0xd6),encode_IRtoMPS(0xd7),encode_IRtoMPS(0xd8),encode_IRtoMPS(0xd9),encode_IRtoMPS(0xda),encode_IRtoMPS(0xdb),encode_IRtoMPS(0xdc),encode_IRtoMPS(0xdd),encode_IRtoMPS(0xde),encode_IRtoMPS(0xdf)]:
                    # Lmr
                    MRData = address[0]
                    MRState = color("blue")
                    update_MRData(ma_r, MRData, MRState)
                    # Isp
                    SPData += 1
                    SPData &= 0xff
                    SPState = color("cyan")
                    update_SPData(sp, SPData, SPState)
                # jumpd-3
                if MPSeqData in [encode_IRtoMPS(0xe0),encode_IRtoMPS(0xe1),encode_IRtoMPS(0xe2),encode_IRtoMPS(0xe3),encode_IRtoMPS(0xe4),encode_IRtoMPS(0xe5),encode_IRtoMPS(0xe6),encode_IRtoMPS(0xe7)]:
                    # Lmr
                    MRData = PCData
                    MRState = color("blue")
                    update_MRData(ma_r, MRData, MRState)
                    # Ipc
                    PCData += 1
                    PCState = color("yellow")
                    update_PCData(pc, PCData, PCState)
                    # Efl
                    flag = Sfl(MPSeqData)
                    if not FRData[flag]:
                        # End
                        clock_cycle[0] = -1
                # jumpr-3
                if MPSeqData in [encode_IRtoMPS(0xe8),encode_IRtoMPS(0xe9),encode_IRtoMPS(0xea),encode_IRtoMPS(0xeb),encode_IRtoMPS(0xec),encode_IRtoMPS(0xed),encode_IRtoMPS(0xee),encode_IRtoMPS(0xef)]:
                    # Efl
                    flag = Sfl(MPSeqData)
                    if not FRData[flag]:
                        # End
                        clock_cycle[0] = -1
                # cd-3
                if MPSeqData in [encode_IRtoMPS(0xf0),encode_IRtoMPS(0xf1),encode_IRtoMPS(0xf2),encode_IRtoMPS(0xf3),encode_IRtoMPS(0xf4),encode_IRtoMPS(0xf5),encode_IRtoMPS(0xf6),encode_IRtoMPS(0xf7)]:
                    # Lmr
                    MRData = PCData
                    MRState = color("blue")
                    update_MRData(ma_r, MRData, MRState)
                    # Ipc
                    PCData += 1
                    PCState = color("yellow")
                    update_PCData(pc, PCData, PCState)
                    # Efl
                    flag = Sfl(MPSeqData)
                    if not FRData[flag]:
                        # End
                        clock_cycle[0] = -1
                # cr-3
                if MPSeqData in [encode_IRtoMPS(0xf8),encode_IRtoMPS(0xf9),encode_IRtoMPS(0xfa),encode_IRtoMPS(0xfb),encode_IRtoMPS(0xfc),encode_IRtoMPS(0xfd),encode_IRtoMPS(0xfe),encode_IRtoMPS(0xff)]:
                    # Efl
                    flag = Sfl(MPSeqData)
                    if not FRData[flag]:
                        # End
                        clock_cycle[0] = -1
                
                    
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
                # ret-4
                if MPSeqData in [encode_IRtoMPS(0x08)+1,encode_IRtoMPS(0x09)+1,encode_IRtoMPS(0x0a)+1,encode_IRtoMPS(0x0b)+1,encode_IRtoMPS(0x0c)+1,encode_IRtoMPS(0x0d)+1,encode_IRtoMPS(0x0e)+1,encode_IRtoMPS(0x0f)+1]:
                    # Lmr
                    MRData = address[0]
                    MRState = color("blue")
                    update_MRData(ma_r, MRData, MRState)
                    # Isp
                    SPData += 1
                    SPData &= 0xff
                    SPState = color("cyan")
                    update_SPData(sp, SPData, SPState)

                # add,sub,xor,and,or,cmp-4
                if MPSeqData in [encode_IRtoMPS(0x10)+1,encode_IRtoMPS(0x11)+1,encode_IRtoMPS(0x12)+1,encode_IRtoMPS(0x13)+1,encode_IRtoMPS(0x14)+1,encode_IRtoMPS(0x15)+1,encode_IRtoMPS(0x16)+1,encode_IRtoMPS(0x17)+1,encode_IRtoMPS(0x18)+1,encode_IRtoMPS(0x19)+1,encode_IRtoMPS(0x1a)+1,encode_IRtoMPS(0x1b)+1,encode_IRtoMPS(0x1c)+1,encode_IRtoMPS(0x1d)+1,encode_IRtoMPS(0x1e)+1,encode_IRtoMPS(0x1f)+1,encode_IRtoMPS(0x20)+1,encode_IRtoMPS(0x21)+1,encode_IRtoMPS(0x22)+1,encode_IRtoMPS(0x23)+1,encode_IRtoMPS(0x24)+1,encode_IRtoMPS(0x25)+1,encode_IRtoMPS(0x26)+1,encode_IRtoMPS(0x27)+1,encode_IRtoMPS(0x28)+1,encode_IRtoMPS(0x29)+1,encode_IRtoMPS(0x2a)+1,encode_IRtoMPS(0x2b)+1,encode_IRtoMPS(0x2c)+1,encode_IRtoMPS(0x2d)+1,encode_IRtoMPS(0x2e)+1,encode_IRtoMPS(0x2f)+1,encode_IRtoMPS(0x30)+1,encode_IRtoMPS(0x31)+1,encode_IRtoMPS(0x32)+1,encode_IRtoMPS(0x33)+1,encode_IRtoMPS(0x34)+1,encode_IRtoMPS(0x35)+1,encode_IRtoMPS(0x36)+1,encode_IRtoMPS(0x37)+1,encode_IRtoMPS(0x38)+1,encode_IRtoMPS(0x39)+1,encode_IRtoMPS(0x3a)+1,encode_IRtoMPS(0x3b)+1,encode_IRtoMPS(0x3c)+1,encode_IRtoMPS(0x3d)+1,encode_IRtoMPS(0x3e)+1,encode_IRtoMPS(0x3f)+1,encode_IRtoMPS(0x40)+1,encode_IRtoMPS(0x41)+1,encode_IRtoMPS(0x42)+1,encode_IRtoMPS(0x43)+1,encode_IRtoMPS(0x44)+1,encode_IRtoMPS(0x45)+1,encode_IRtoMPS(0x46)+1,encode_IRtoMPS(0x47)+1,encode_IRtoMPS(0x48)+1,encode_IRtoMPS(0x49)+1,encode_IRtoMPS(0x4a)+1,encode_IRtoMPS(0x4b)+1,encode_IRtoMPS(0x4c)+1,encode_IRtoMPS(0x4d)+1,encode_IRtoMPS(0x4e)+1,encode_IRtoMPS(0x4f)+1,encode_IRtoMPS(0x50)+1,encode_IRtoMPS(0x51)+1,encode_IRtoMPS(0x52)+1,encode_IRtoMPS(0x53)+1,encode_IRtoMPS(0x54)+1,encode_IRtoMPS(0x55)+1,encode_IRtoMPS(0x56)+1,encode_IRtoMPS(0x57)+1,encode_IRtoMPS(0x58)+1,encode_IRtoMPS(0x59)+1,encode_IRtoMPS(0x5a)+1,encode_IRtoMPS(0x5b)+1,encode_IRtoMPS(0x5c)+1,encode_IRtoMPS(0x5d)+1,encode_IRtoMPS(0x5e)+1,encode_IRtoMPS(0x5f)+1]:
                    # Lar
                    ARData = ALUData[2]
                    ARState = color("blue")
                    update_ARData(ac_r, ARData, ARState)
                    # End
                    clock_cycle[0] = -1
                # cmp-4
                if MPSeqData in [encode_IRtoMPS(0x60)+1,encode_IRtoMPS(0x61)+1,encode_IRtoMPS(0x62)+1,encode_IRtoMPS(0x63)+1,encode_IRtoMPS(0x64)+1,encode_IRtoMPS(0x65)+1,encode_IRtoMPS(0x66)+1,encode_IRtoMPS(0x67)+1,encode_IRtoMPS(0x68)+1,encode_IRtoMPS(0x69)+1,encode_IRtoMPS(0x6a)+1,encode_IRtoMPS(0x6b)+1,encode_IRtoMPS(0x6c)+1,encode_IRtoMPS(0x6d)+1,encode_IRtoMPS(0x6e)+1,encode_IRtoMPS(0x6f)+1]:
                    # End
                    clock_cycle[0] = -1
                # movi-4
                if MPSeqData in [encode_IRtoMPS(0x90)+1, encode_IRtoMPS(0x91)+1, encode_IRtoMPS(0x92)+1, encode_IRtoMPS(0x93)+1, encode_IRtoMPS(0x94)+1, encode_IRtoMPS(0x95)+1, encode_IRtoMPS(0x96)+1, encode_IRtoMPS(0x97)+1, encode_IRtoMPS(0x98)+1, encode_IRtoMPS(0x99)+1, encode_IRtoMPS(0x9A)+1, encode_IRtoMPS(0x9B)+1, encode_IRtoMPS(0x9C)+1, encode_IRtoMPS(0x9D)+1, encode_IRtoMPS(0x9E)+1, encode_IRtoMPS(0x9F)+1]:
                    RegNum = Srg(MPSeqData)
                    # Lrg
                    RGData[RegNum] = value[0]
                    RGState[RegNum] = color("blue")
                    update_RGData(r_arr, RGData, RGState)
                    # End
                    clock_cycle[0] = -1
                # stor-4
                if MPSeqData in [encode_IRtoMPS(0xa0)+1,encode_IRtoMPS(0xa1)+1,encode_IRtoMPS(0xa2)+1,encode_IRtoMPS(0xa3)+1,encode_IRtoMPS(0xa4)+1,encode_IRtoMPS(0xa5)+1,encode_IRtoMPS(0xa6)+1,encode_IRtoMPS(0xa7)+1,encode_IRtoMPS(0xa8)+1,encode_IRtoMPS(0xa9)+1,encode_IRtoMPS(0xaa)+1,encode_IRtoMPS(0xab)+1,encode_IRtoMPS(0xac)+1,encode_IRtoMPS(0xad)+1,encode_IRtoMPS(0xae)+1,encode_IRtoMPS(0xaf)+1]:
                    # WR
                    extMemData[MRData] = value[0]
                    extMemState[MRData] = color("blue")
                    update_ExtMemData(ext_mem_display, extMemData, extMemState)
                    # End
                    clock_cycle[0] = -1
                # load-4
                if MPSeqData in [encode_IRtoMPS(0xb0)+1,encode_IRtoMPS(0xb1)+1,encode_IRtoMPS(0xb2)+1,encode_IRtoMPS(0xb3)+1,encode_IRtoMPS(0xb4)+1,encode_IRtoMPS(0xb5)+1,encode_IRtoMPS(0xb6)+1,encode_IRtoMPS(0xb7)+1,encode_IRtoMPS(0xb8)+1,encode_IRtoMPS(0xb9)+1,encode_IRtoMPS(0xba)+1,encode_IRtoMPS(0xbb)+1,encode_IRtoMPS(0xbc)+1,encode_IRtoMPS(0xbd)+1,encode_IRtoMPS(0xbe)+1,encode_IRtoMPS(0xbf)+1]:
                    # Lrg
                    RegNum = Srg(MPSeqData)
                    RGData[RegNum] = address[0]
                    RGState[RegNum] = color("blue")
                    update_RGData(r_arr, RGData, RGState)
                    # End
                    clock_cycle[0] = -1
                # push-4
                if MPSeqData in [encode_IRtoMPS(0xc0)+1,encode_IRtoMPS(0xc1)+1,encode_IRtoMPS(0xc2)+1,encode_IRtoMPS(0xc3)+1,encode_IRtoMPS(0xc4)+1,encode_IRtoMPS(0xc5)+1,encode_IRtoMPS(0xc6)+1,encode_IRtoMPS(0xc7)+1,encode_IRtoMPS(0xc8)+1,encode_IRtoMPS(0xc9)+1,encode_IRtoMPS(0xca)+1,encode_IRtoMPS(0xcb)+1,encode_IRtoMPS(0xcc)+1,encode_IRtoMPS(0xcd)+1,encode_IRtoMPS(0xce)+1,encode_IRtoMPS(0xcf)+1]:
                    # Lmr
                    MRData = address[0]
                    MRState = color("blue")
                    update_MRData(ma_r, MRData, MRState)
                # pop-4
                if MPSeqData in [encode_IRtoMPS(0xd0)+1,encode_IRtoMPS(0xd1)+1,encode_IRtoMPS(0xd2)+1,encode_IRtoMPS(0xd3)+1,encode_IRtoMPS(0xd4)+1,encode_IRtoMPS(0xd5)+1,encode_IRtoMPS(0xd6)+1,encode_IRtoMPS(0xd7)+1,encode_IRtoMPS(0xd8)+1,encode_IRtoMPS(0xd9)+1,encode_IRtoMPS(0xda)+1,encode_IRtoMPS(0xdb)+1,encode_IRtoMPS(0xdc)+1,encode_IRtoMPS(0xdd)+1,encode_IRtoMPS(0xde)+1,encode_IRtoMPS(0xdf)+1]:
                    # Lrg
                    RegNum = Srg(MPSeqData)
                    RGData[RegNum] = value[0]
                    RGState[RegNum] = color("blue")
                    update_RGData(r_arr, RGData, RGState)
                    # End
                    clock_cycle[0] = -1
                # jumpd-4
                if MPSeqData in [encode_IRtoMPS(0xe0)+1,encode_IRtoMPS(0xe1)+1,encode_IRtoMPS(0xe2)+1,encode_IRtoMPS(0xe3)+1,encode_IRtoMPS(0xe4)+1,encode_IRtoMPS(0xe5)+1,encode_IRtoMPS(0xe6)+1,encode_IRtoMPS(0xe7)+1]:
                    # Lpc
                    PCData = address[0]
                    PCState = color("blue")
                    update_PCData(pc, PCData, PCState)
                    # End
                    clock_cycle[0] = -1
                # jumpr-4
                if MPSeqData in [encode_IRtoMPS(0xe8)+1,encode_IRtoMPS(0xe9)+1,encode_IRtoMPS(0xea)+1,encode_IRtoMPS(0xeb)+1,encode_IRtoMPS(0xec)+1,encode_IRtoMPS(0xed)+1,encode_IRtoMPS(0xee)+1,encode_IRtoMPS(0xef)+1]:
                    # Lpc
                    PCData = address[0]
                    PCState = color("blue")
                    update_PCData(pc, PCData, PCState)
                    # End
                    clock_cycle[0] = -1
                # cd-4
                if MPSeqData in [encode_IRtoMPS(0xf0)+1,encode_IRtoMPS(0xf1)+1,encode_IRtoMPS(0xf2)+1,encode_IRtoMPS(0xf3)+1,encode_IRtoMPS(0xf4)+1,encode_IRtoMPS(0xf5)+1,encode_IRtoMPS(0xf6)+1,encode_IRtoMPS(0xf7)+1]:
                    # Lar
                    ARData = address[0]
                    ARState = color("blue")
                    update_ARData(ac_r, ARData, ARState)
                    # Dsp
                    SPData -= 1
                    SPData &= 0xff
                    SPState = color("red")
                    update_SPData(sp, SPData, SPState)
                # cr-4
                if MPSeqData in [encode_IRtoMPS(0xf8)+1,encode_IRtoMPS(0xf9)+1,encode_IRtoMPS(0xfa)+1,encode_IRtoMPS(0xfb)+1,encode_IRtoMPS(0xfc)+1,encode_IRtoMPS(0xfd)+1,encode_IRtoMPS(0xfe)+1,encode_IRtoMPS(0xff)+1]:
                    # Dsp
                    SPData -= 1
                    SPData &= 0xff
                    SPState = color("red")
                    update_SPData(sp, SPData, SPState)
                    
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
                # cmi-5
                if MPSeqData == encode_IRtoMPS(0x06)+2:
                    # End
                    clock_cycle[0] = -1
                # ret-5
                if MPSeqData in [encode_IRtoMPS(0x08)+2,encode_IRtoMPS(0x09)+2,encode_IRtoMPS(0x0a)+2,encode_IRtoMPS(0x0b)+2,encode_IRtoMPS(0x0c)+2,encode_IRtoMPS(0x0d)+2,encode_IRtoMPS(0x0e)+2,encode_IRtoMPS(0x0f)+2]:
                    # Lpc
                    PCData = address[0]
                    PCState = color("blue")
                    update_PCData(pc, PCData, PCState)
                    # End
                    clock_cycle[0] = -1
                # push-5
                if MPSeqData in [encode_IRtoMPS(0xc0)+2,encode_IRtoMPS(0xc1)+2,encode_IRtoMPS(0xc2)+2,encode_IRtoMPS(0xc3)+2,encode_IRtoMPS(0xc4)+2,encode_IRtoMPS(0xc5)+2,encode_IRtoMPS(0xc6)+2,encode_IRtoMPS(0xc7)+2,encode_IRtoMPS(0xc8)+2,encode_IRtoMPS(0xc9)+2,encode_IRtoMPS(0xca)+2,encode_IRtoMPS(0xcb)+2,encode_IRtoMPS(0xcc)+2,encode_IRtoMPS(0xcd)+2,encode_IRtoMPS(0xce)+2,encode_IRtoMPS(0xcf)+2]:
                    # WR
                    extMemData[MRData] = value[0]
                    extMemState[MRData] = color("blue")
                    update_ExtMemData(ext_mem_display, extMemData, extMemState)
                    # End
                    clock_cycle[0] = -1
                # cd,cr-5
                if MPSeqData in [encode_IRtoMPS(0xf0)+2,encode_IRtoMPS(0xf1)+2,encode_IRtoMPS(0xf2)+2,encode_IRtoMPS(0xf3)+2,encode_IRtoMPS(0xf4)+2,encode_IRtoMPS(0xf5)+2,encode_IRtoMPS(0xf6)+2,encode_IRtoMPS(0xf7)+2,encode_IRtoMPS(0xf8)+2,encode_IRtoMPS(0xf9)+2,encode_IRtoMPS(0xfa)+2,encode_IRtoMPS(0xfb)+2,encode_IRtoMPS(0xfc)+2,encode_IRtoMPS(0xfd)+2,encode_IRtoMPS(0xfe)+2,encode_IRtoMPS(0xff)+2]:
                    # Lmr
                    MRData = address[0]
                    MRState = color("blue")
                    update_MRData(ma_r, MRData, MRState)
                
                MPSeqData += 1
                update_MPSeqData(mp_s, MPSeqData, color("blue"))
                MPMemData = encode_MPStoCSSig(MPSeqData)
                update_MPMemData(mp_mem, MPMemData)
            
            elif clock_cycle[0]==5:
                # cd,cr-6
                # WR
                extMemData[MRData] = address[0]
                extMemState[MRData] = color("blue")
                update_ExtMemData(ext_mem_display, extMemData, extMemState)

                MPSeqData += 1
                update_MPSeqData(mp_s, MPSeqData, color("blue"))
                MPMemData = encode_MPStoCSSig(MPSeqData)
                update_MPMemData(mp_mem, MPMemData)

            elif clock_cycle[0]==6:
                # cd,cr-7
                # Lpc
                PCData = address[0]
                PCState = color("blue")
                update_PCData(pc, PCData, PCState)

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