# xs-vm [![Build Status](https://travis-ci.org/GedRap/xs-vm.svg)](https://travis-ci.org/GedRap/xs-vm)
## eXtremely Simple Virtual Machine

The purpose of this project is to implement a simple virtual machine, capable of executing assembly code similar to ARM.
I will keep it simple (so probably no operation modes, interrupt handling, etc) because I built it for educational
 purposes. Yet, it's powerful enough to do things like recursion (see the [Fibonacci example](https://github.com/GedRap/xs-vm/blob/master/demos/fibonacci.s) ). Why Python? Development speed, as opposed to performance, is the key priority for this project so Python
 fits in perfectly.

It is distributed under MIT license (see license.txt for the details).

All Python versions from 2.7 up to 3.4 are supported.
 
## Installing and running
 
### Executing code

```
$ cat demos/function_call.s
mov r1, #1
mov r2, #3
bl func1
swi #0

func1    push lr
         add r0, r1, r2
         pop pc
         
$ python run.py demos/function_call.s
Instructions executed: 7
Instructions executed by type:
╒═══════════════╤═════════╤═══════════════╤═════════╕
│ Instruction   │   Count │ Instruction   │   Count │
╞═══════════════╪═════════╪═══════════════╪═════════╡
│ swi           │       1 │ bl            │       1 │
├───────────────┼─────────┼───────────────┼─────────┤
│ mov           │       2 │ pop           │       1 │
├───────────────┼─────────┼───────────────┼─────────┤
│ add           │       1 │ push          │       1 │
╘═══════════════╧═════════╧═══════════════╧═════════╛
Register bank after halting:
╒═════╤═══╤═════╤══════════╕
│ r0  │ 4 │ r1  │        1 │
├─────┼───┼─────┼──────────┤
│ r2  │ 3 │ r3  │        0 │
├─────┼───┼─────┼──────────┤
│ r4  │ 0 │ r5  │        0 │
├─────┼───┼─────┼──────────┤
│ r6  │ 0 │ r7  │        0 │
├─────┼───┼─────┼──────────┤
│ r8  │ 0 │ r9  │        0 │
├─────┼───┼─────┼──────────┤
│ r10 │ 0 │ r11 │        0 │
├─────┼───┼─────┼──────────┤
│ r12 │ 0 │ r13 │ 16777215 │
├─────┼───┼─────┼──────────┤
│ r14 │ 3 │ r15 │        4 │
╘═════╧═══╧═════╧══════════╛
```

Using `-d` or `--debug` will enable the debugging mode, in which the values of the register bank will be dumped after executing every instruction:

```
$ python run.py --debug demos/function_call.s
Debug mode: True
Executing mov r1, #1 from 0
Register bank after executing the instruction:
╒═════╤═══╤═════╤══════════╕
│ r0  │ 0 │ r1  │        1 │
├─────┼───┼─────┼──────────┤
│ r2  │ 0 │ r3  │        0 │
├─────┼───┼─────┼──────────┤
│ r4  │ 0 │ r5  │        0 │
├─────┼───┼─────┼──────────┤
│ r6  │ 0 │ r7  │        0 │
├─────┼───┼─────┼──────────┤
│ r8  │ 0 │ r9  │        0 │
├─────┼───┼─────┼──────────┤
│ r10 │ 0 │ r11 │        0 │
├─────┼───┼─────┼──────────┤
│ r12 │ 0 │ r13 │ 16777215 │
├─────┼───┼─────┼──────────┤
│ r14 │ 0 │ r15 │        1 │
╘═════╧═══╧═════╧══════════╛
Executing mov r2, #3 from 1
Register bank after executing the instruction:
╒═════╤═══╤═════╤══════════╕
│ r0  │ 0 │ r1  │        1 │
├─────┼───┼─────┼──────────┤
│ r2  │ 3 │ r3  │        0 │
├─────┼───┼─────┼──────────┤
│ r4  │ 0 │ r5  │        0 │
├─────┼───┼─────┼──────────┤
│ r6  │ 0 │ r7  │        0 │
├─────┼───┼─────┼──────────┤
│ r8  │ 0 │ r9  │        0 │
├─────┼───┼─────┼──────────┤
│ r10 │ 0 │ r11 │        0 │
├─────┼───┼─────┼──────────┤
│ r12 │ 0 │ r13 │ 16777215 │
├─────┼───┼─────┼──────────┤
│ r14 │ 0 │ r15 │        2 │
╘═════╧═══╧═════╧══════════╛
Executing bl func1 from 2
.......................
```

### Installing and running tests

Just clone this repository and install the dependencies (`pip install -r requirements.txt`).

You can run the tests simply by running `nosetests` from the project root directory.

## Architecture

The VM has 16 registers (R0-R15). Most of the are general purpose, with a few special ones:

* SP (R13). Stack pointer. Points to the last element pushed to the stack (or 0xFFFFFF if nothing has been pushed yet).

* LR (R14). Link register. Holds a return address of the function call.

* PC (R15). Program counter. Holds the address of the instruction in memory which will be executed next.

For function calls, the result is stored in R0, and R1-R3 are normally used to pass the parameters.

### Supported instructions

| Instruction | Example            | Description                                                                       |
|-------------|--------------------|-----------------------------------------------------------------------------------|
| mov         | mov r1, #5         | Move some value (either other register or a constant) to the register.            |
|             | mov r1, r2         |                                                                                   |
| add         | add r0, r1, #3     | r0 = r1 + 3                                                                       |
| sub         | sub r0, r1, #3     | r0 = r1 - 3                                                                       |
| mul         | mul r0, r1, #4     | r0 = r1 * 4                                                                       |
| mla         | mla r0, r1, #3, #5 | r0 = r1 * 3 + 5                                                                   |
| cmp         | cmp r0, r1         | Compare 2 numerical values and store the difference in comparison register (comp_reg = r0 - r1). The value is used later for conditional branching. |
| b           | b main             | Always branch. Set PC to the instruction to which the given label is pointing to. |
|             | b 0x001            | Instead of label, memory location can be also passed.                             |
| beq         | beq main           | Branch if equal, the result of cmp instruction is used.                           |
| bne         | bne main           | Branch if not equal.                                                              |
| blt         | blt foo            | Branch if less than (comp_reg < 0).                                               |
| bgt         | bgt foo            | Branch if greater than (comp_reg > 0).                                            |
| bl          | bl printf          | Branch and link. Stores PC in LR, equivalent of a function call.                  |
| nop         | nop                | No OPeration. Do nothing.                                                         |
| push        | push r0            | Push the value of r0 to the stack.                                                |
| pop         | pop r1             | Pop the element from the stack and store the value in r1.                         |
| swi         | swi #0             | Software interrupt. See below.                                                    |

#### Software interrupts

In xs-vm, software interrupts is a method of communication between the application being executed and the virtual 
machine executing it.

The list of supported software interrupts:

| Interrupt | Description                                   |
|-----------|-----------------------------------------------|
| swi #0    | Halt. Stop executing the application and quit |
