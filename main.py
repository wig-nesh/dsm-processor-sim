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
    # stdscr.move(80,0)
    stdscr.refresh()

    # clock window
    height = 5; width = 30
    begin_x = width//2; begin_y = 2
    clk = curses.newwin(height, width, begin_y, begin_x)
    clk.box()
    addstr_mid(clk, " Clock ")
    clk.refresh()

    # bus
    connections = [3, 9, 15, 21, 25]
    for i in range(curses.LINES-21):
        if i-5 in connections: addstr_mid(stdscr, "+", i+2)
        else: addstr_mid(stdscr, "|", i+2)
        stdscr.refresh()
    addstr_mid(stdscr, "x8", i+3)

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
    stdscr.addstr(begin_y+height//2, curses.COLS//2 + 1, "-"*9+"+")
    stdscr.refresh()

    # alu window
    begin_x = curses.COLS//2 + 10; begin_y += height + 1
    height = 5; width = 20
    alu = curses.newwin(height, width, begin_y, begin_x)
    alu.box()
    addstr_mid(alu, " ALU ")
    alu.refresh()    
    stdscr.addstr(begin_y+height//2, curses.COLS//2 + 1, "-"*9+"+")
    for i in range(3):
        if not i%2:
            stdscr.addstr(begin_y-2+i, begin_x+int(3/4*width), "+")
        else:
            stdscr.addstr(begin_y-2+i, begin_x+int(3/4*width), "|")
    stdscr.refresh()

    # accumulator register window
    begin_x = curses.COLS//2 + 10; begin_y += height + 1
    height = 5; width = 20
    ac_r = curses.newwin(height, width, begin_y, begin_x)
    ac_r.box()
    addstr_mid(ac_r, " Accumulator ")
    ac_r.refresh()
    stdscr.addstr(begin_y+height//2, curses.COLS//2 + 1, "-"*9+"+")
    stdscr.refresh()
    for i in range(3):
        if not i%2:
            stdscr.addstr(begin_y-2+i, begin_x+int(9/10*width), "+")
        else:
            stdscr.addstr(begin_y-2+i, begin_x+int(9/10*width), "|")
    stdscr.refresh()

    # register array window
    begin_x = curses.COLS//2 + 10; begin_y += height + 1
    height = 13; width = 20
    r_arr = curses.newwin(height, width, begin_y, begin_x)
    r_arr.box()
    addstr_mid(r_arr, " Registers ")
    r_arr.refresh()
    stdscr.addstr(begin_y+height//2, curses.COLS//2 + 1, "-"*9+"+")
    stdscr.refresh()

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
    stdscr.addstr(begin_y+height//2, begin_x+width-1, "+"+"-"*10)
    stdscr.refresh()
    for i in range(3):
        if not i%2:
            stdscr.addstr(begin_y-2+i, begin_x+int(1/7*width), "+")
        else:
            stdscr.addstr(begin_y-2+i, begin_x+int(1/7*width), "|")
    stdscr.refresh()

    # program counter window
    begin_x = curses.COLS//2 - width - 10; begin_y += height + 1
    height = 5; width = 20
    pc = curses.newwin(height, width, begin_y, begin_x)
    pc.box()
    addstr_mid(pc, " Program Counter ")
    pc.refresh()
    stdscr.addstr(begin_y+height//2, begin_x+width-1, "+"+"-"*10)
    stdscr.refresh()

    # stack pointer window
    begin_x = curses.COLS//2 - width - 10; begin_y += height + 1
    height = 5; width = 20
    sp = curses.newwin(height, width, begin_y, begin_x)
    sp.box()
    addstr_mid(sp, " Stack Pointer ")
    sp.refresh()
    stdscr.addstr(begin_y+height//2, begin_x+width-1, "+"+"-"*10)
    stdscr.refresh()

    # instruction register window
    begin_x = curses.COLS//2 - width - 10; begin_y += height + 1
    height = 5; width = 20
    i_r = curses.newwin(height, width, begin_y, begin_x)
    i_r.box()
    addstr_mid(i_r, " Instruction Reg ")
    i_r.refresh()
    stdscr.addstr(begin_y+height//2, begin_x+width-1, "+"+"-"*10)
    stdscr.refresh()

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