import curses
from helper_functions import *
from global_variables import *

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
    # main_mid = curses.COLS//2-38
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

def update_MPSeqtoMPMem(window, color_pair=0):
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

def update_ExtMemData(window, extMemData=[0x00]*256, extMemState=[0]*256):
    for i in range(8):
        for j in range(32):
            idx = i*32+j
            window.addstr(1+(j%32), 2+i*11, "●", curses.color_pair(extMemState[idx]))
            window.addstr(1+(j%32), 3+i*11, f" {idx:02x} {extMemData[idx]:02x}")
    window.refresh()

def update_RGData(window, RGData=[0x00]*16, RGState=[0]*16):
    for i in range(16):
        window.addstr(1+i, 2, "●", curses.color_pair(RGState[i]))
        window.addstr(1+i, 3, f" {i:2} {RGData[i]:02x} {RGData[i]:08b}")
    window.refresh()

def update_ALUData(window, ALUData=[0x00]*3, ALUState=0):
    for i in range(3):
        if i==2: 
            window.addstr(1+i, 4, "●", curses.color_pair(ALUState))
            window.addstr(1+i, 5, f" {ALUData[i]:02x} {ALUData[i]:08b}")
        else: window.addstr(1+i, 5, f" {ALUData[i]:02x} {ALUData[i]:08b}")
    window.refresh()

def update_FRData(window, FRData=[0]*8):
    for i in range(8):
        if i in [2, 3, 4, 6]: window.addstr(1, 6+i, " ")
        else: window.addstr(1, 6+i, "●", curses.color_pair(FRData[i]+1))
        window.addstr(3, 6+i, str(FRData[i]))
    window.addstr(2, 6, "SZ   P C")
    # window.addstr(3, 6, f"{FRData:08b}")
    window.refresh()

def update_MRData(window, MRData=0x00, MRState=0):
    window.addstr(2, 3, "●", curses.color_pair(MRState))
    window.addstr(2, 4, f" {MRData:02x} {MRData:08b}")
    window.refresh()

def update_PCData(window, PCData=0x00, PCState=0):
    window.addstr(2, 3, "●", curses.color_pair(PCState))
    window.addstr(2, 4, f" {PCData:02x} {PCData:08b}")
    window.refresh()

def update_SPData(window, SPData=0x00, SPState=0):
    window.addstr(2, 3, "●", curses.color_pair(SPState))
    window.addstr(2, 4, f" {SPData:02x} {SPData:08b}")
    window.refresh()

def update_ORData(window, ORData=0x00, ORState=0):
    window.addstr(2, 4, "●", curses.color_pair(ORState))
    window.addstr(2, 5, f" {ORData:02x} {ORData:08b}")
    window.refresh()

def update_ARData(window, ARData=0x00, ARState=0):
    window.addstr(2, 4, "●", curses.color_pair(ARState))
    window.addstr(2, 5, f" {ARData:02x} {ARData:08b}")
    window.refresh()

def update_IRData(window, IRData=0x00, IRState=0):
    window.addstr(2, 4, "●", curses.color_pair(IRState))
    window.addstr(2, 5, f" {IRData:02x} {IRData:08b}")
    window.refresh()

def update_MPSeqData(window, MPSeqData=0x00, MPSeqState=0):
    window.addstr(2, 4, "●", curses.color_pair(MPSeqState))
    window.addstr(2, 5, f" {MPSeqData:010b}")
    window.refresh()

def update_MPMemData(window, MPMemData=[0]*32):
    for i in range(32):
        window.addstr(2, i+14, f"{MPMemData[i]}")
    window.refresh()
