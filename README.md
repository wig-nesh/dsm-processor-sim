# 8-bit Microprocessor Simulator

## How to Use
- Make sure you have the `curses` module for python installed, and use a full screen terminal window.
- Type your assembly program using the commands given below into `program/code.txt` 
- Compile it using `python program/compiler.py`
- A test program is provided in `code.txt` already, which calculates the n-th Fibonacci number.
- Run it using `python scripts/main.py`
- If you get any errors, try reducing your display scaling and retry. It would most probably be an issue related to your terminal not having enough space.

## Commands
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
 `add <R>` | add AR to `<R>` 
 `sub <R>` | subtract `<R>` from AR 
 `xor <R>` | xor AR with `<R>` 
 `and <R>` | and AR with `<R>` 
 `or <R>` | or AR with `<R>` 
 `cmp <R>` | compare AR with `<R>` 
 `movs <R>` | moves value from `<R>` to AR 
 `movd <R>` | moves value from AR to `<R>` 
 `movi <R> xx` | move value xx to `<R>` 
 `stor <R>` | writes value from `<R>` to memory in location given by AR 
 `load <R>` | reads value from memory to `<R>` in location given by AR 
 `push <R>` | pushes value from `<R>` to top of stack 
 `pop <R>` | pops value from top of stack to `<R>` 
 `jumpd<FL> xx` | if flag value is 1,  program jumps to given address xx 
 `jumpr<FL>` | if flag value is 1,  program jumps to address in AR 
 `cd<FL> xx` | if flag value is 1, program stores current address in stack and jumps to given address xx 
 `cr<FL>` | if flag value is 1, program stores current address in stack and jumps to address in AR 

## Credits
A lot of the architecture design was taken from the document provided at the end of Digital Systems and Microcontrollers (EC2.101) taken at IIIT Hyderabad in Monsoon-23. This project would not be possible without it.