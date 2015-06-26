from xsvm import vm, parser

machine = vm.Processor()
filename = "demos/function_call.s"
parser.load_file_into_memory(machine.memory, filename)

machine.execute_until_halted()

# dump all register values. will do the job for now :)
print machine.register_bank.registers