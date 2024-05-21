from helper_functions import *
from global_variables import *

def static_title(stdscr):
    stdscr.box()
    addstr_mid(stdscr, " DSM Processor Simulator ")
    stdscr.refresh()

def static_clock():
    height = 3; width = 11
    begin_x = 4; begin_y = 2
    clk = curses.newwin(height, width, begin_y, begin_x)
    clk.box()
    addstr_mid(clk, " Clock ", color_pair=3)
    clk.refresh()
    return clk

def static_extMem():
    height = 5; width = 60
    begin_x = main_mid - width//2; begin_y = 2
    ext_mem = curses.newwin(height, width, begin_y, begin_x)
    ext_mem.box()
    addstr_mid(ext_mem, " External Memory ")
    ext_mem.refresh()
    return ext_mem

def static_OR():
    begin_x = main_mid + 10; begin_y = 8
    height = 5; width = 20
    op_r = curses.newwin(height, width, begin_y, begin_x)
    op_r.box()
    addstr_mid(op_r, " Operand Register ")
    op_r.refresh()
    return op_r

def static_ALU():
    begin_x = main_mid + 10; begin_y = 13
    height = 5; width = 20
    alu = curses.newwin(height, width, begin_y, begin_x)
    alu.box()
    addstr_mid(alu, " ALU ")
    alu.refresh()  
    return alu

def static_AR():
    begin_x = main_mid + 10; begin_y = 19
    height = 5; width = 20
    ac_r = curses.newwin(height, width, begin_y, begin_x)
    ac_r.box()
    addstr_mid(ac_r, " Accumulator ")
    ac_r.refresh()
    return ac_r

def static_FR():
    begin_x = main_mid + 10; begin_y = 26
    height = 5; width = 20
    f_r = curses.newwin(height, width, begin_y, begin_x)
    f_r.box()
    addstr_mid(f_r, " Flag Register ")
    f_r.refresh()
    return f_r

def static_IR():
    begin_x = main_mid + 10; begin_y = 32
    height = 5; width = 20
    i_r = curses.newwin(height, width, begin_y, begin_x)
    i_r.box()
    addstr_mid(i_r, " Instruction Reg ")
    i_r.refresh()
    return i_r

def static_MPSeq():
    begin_x = main_mid + 10; begin_y = 38
    height = 5; width = 20
    mp_s = curses.newwin(height, width, begin_y, begin_x)
    mp_s.box()
    addstr_mid(mp_s, " Microprogram Seq ")
    mp_s.refresh()
    return mp_s

def static_MPMem():
    height = 5; width = 60
    begin_x = main_mid - width//2; begin_y = 44
    mp_mem = curses.newwin(height, width, begin_y, begin_x)
    mp_mem.box()
    addstr_mid(mp_mem, " Microprogram Memory ")
    mp_mem.refresh()
    return mp_mem

def static_MR():
    begin_x = main_mid - 30; begin_y = 7
    height = 5; width = 20
    ma_r = curses.newwin(height, width, begin_y, begin_x)
    ma_r.box()
    addstr_mid(ma_r, " Address Reg ")
    ma_r.refresh()
    return ma_r

def static_PC():
    begin_x = main_mid - 30; begin_y = 13
    height = 5; width = 20
    pc = curses.newwin(height, width, begin_y, begin_x)
    pc.box()
    addstr_mid(pc, " Program Counter ")
    pc.refresh()
    return pc

def static_SP():
    begin_x = main_mid - 30; begin_y = 19
    height = 5; width = 20
    sp = curses.newwin(height, width, begin_y, begin_x)
    sp.box()
    addstr_mid(sp, " Stack Pointer ")
    sp.refresh()
    return sp

def static_RG():
    begin_x = main_mid - 30; begin_y = 26
    height = 18; width = 20
    r_arr = curses.newwin(height, width, begin_y, begin_x)
    r_arr.box()
    addstr_mid(r_arr, " Reg Array ")
    r_arr.refresh()
    return r_arr

def static_extMemDisplay():
    height = 32+2; width = 11*8
    begin_y = 2; begin_x = curses.COLS - width - 4
    ext_mem_display = curses.newwin(height, width, begin_y, begin_x)
    ext_mem_display.box()
    addstr_mid(ext_mem_display, " External Memory Display ")
    ext_mem_display.refresh()
    return ext_mem_display