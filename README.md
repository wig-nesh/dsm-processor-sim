# 8-bit Microprocessor Simulator

## How to Use
- Make sure you have the `curses` module for python installed, and use a full screen terminal window.
- Type your assembly program using the Commands given below into `program/code.txt` 
- Compile it using `python program/compiler.py`
- Run it using `python scripts/main.py`

## Commands:
 **Command** | **Action** 
---|---
 `nop` | does literally nothing 
 `adi xx` | add immediate 
 `sbi xx` | subtract immediate 
 `xri xx` | xor immediate 
 `ani xx` | bitwise add immediate 
 `ori xx` | bitwise or immediate 
 `cmi xx` | compare immediate 
 `stop` | shuts down the processor 
 `ret<FL>` | returns to address on top of stack if flag is true 
 `add <R>` | add AR to <R> 
 `sub <R>` | subtract <R> from AR 
 `xor <R>` | xor AR with <R> 
 `and <R>` | and AR with <R> 
 `or <R>` | or AR with <R> 
 `cmp <R>` | compare AR with <R> 
 `movs <R>` | moves value from <R> to AR 
 `movd <R>` | moves value from AR to <R> 
 `movi <R> xx` | move value xx to <R> 
 `stor <R>` | writes value from <R> to memory in location given by AR 
 `load <R>` | reads value from memory to <R> in location given by AR 
 `push <R>` | pushes value from <R> to top of stack 
 `pop <R>` | pops value from top of stack to <R> 
 `jumpd<FL> xx` | if flag value is 1,  program jumps to given address xx 
 `jumpr<FL>` | if flag value is 1,  program jumps to address in AR 
 `cd<FL> xx` | if flag value is 1, program stores current address in stack and jumps to given address xx 
 `cr<FL>` | if flag value is 1, program stores current address in stack and jumps to address in AR 

