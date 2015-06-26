from xsvm import vm, parser
import sys

machine = vm.Processor()
filename = sys.argv[1]
parser.load_file_into_memory(machine.memory, filename)

machine.execute_until_halted()

print "Instructions executed: {i}".format(i=machine.instructions_executed)
print "Instructions executed by type:"
print machine.dump_instructions_executed_grouped()
print "Register bank after halting:"
print machine.register_bank.dump_content()