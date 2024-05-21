main_mid = 51

extMemData = [0x00]*256
extMemState = [0]*256 # 0-empty 1-program 2-data segment 3-stack 4-other, also used for color
extMemState[-10:] = [3]*10 # temp stack

RGData = [0x00]*16
RGState = [0]*16 # 0-empty, 1-used, 2-enable, 3-load
RGState[:4] = [1]*4 # temp
RGState[1] = 2 # temp

ALUData = [0x00]*3
ALUState = 0 

FRData = 0x00 # S Z X A X P X C
FRState = [1]*8

MRData = 0x00
MRState = 0

PCData = 0x00
PCState = 0

SPData = 0x00
SPState = 0

ORData = 0x00
ORState = 0

ARData = 0x00
ARState = 0

IRData = 0x00
IRState = 0

MPSeqData = 0b0000000000
MPSeqState = 0

MPMemData = [0]*32

# clk = 0
# ext_mem_display = 0
# r_arr = 0
# ma_r = 0
# alu = 0
# f_r = 0
# pc = 0
# sp = 0
# op_r = 0
# ac_r = 0
# i_r = 0
# mps = 0
# mp_mem = 0