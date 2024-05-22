main_mid = 51

extMemData = [0x00]*256
extMemData[:7] = [0x90,0x81,0x70,0x02,0x80,0x81,0x07] # temporary program
extMemState = [0]*256 # 0-empty 1-program 2-data segment 3-stack 4-other, also used for color
extMemState[-10:] = [3]*10 # temp stack

RGData = [0x00]*16
RGState = [0]*16 # 0-empty, 1-used, 2-enable, 3-load

ALUData = [0x00]*3
ALUState = 0 

FRData = [0]*8 # S Z X X X P X C

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
instruction_address = 0x00