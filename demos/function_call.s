mov r1, #1
mov r2, #3
bl func1
swi #0

func1    push lr
         add r0, r1, r2
         pop pc