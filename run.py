from xsvm import vm, parser

machine = vm.Processor()
filename = "demos/function_call.s"
parser.load_file_into_memory(machine.memory, filename)

machine.execute_until_halted()

print "Instructions executed: {i}".format(i=machine.instructions_executed)
print machine.register_bank.dump_content()