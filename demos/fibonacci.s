mov r1, #6
bl fibonacci
swi #0

fibonacci     push lr
              push r1
              push r2
              push r3
              cmp r1, #1
              blt fib_zero
              beq fib_one
              sub r2, r1, #1
              sub r3, r1, #2
              mov r1, r2
              bl fibonacci
              mov r2, r0
              mov r1, r3
              bl fibonacci
              add r0, r0, r2
              pop r3
              pop r2
              pop r1
              pop pc

fib_zero      mov r0, #0
              pop r3
              pop r2
              pop r1
              pop pc

fib_one       mov r0, #1
              pop r3
              pop r2
              pop r1
              pop pc