from xsvm import vm, parser
import sys

if len(sys.argv) >= 3 and sys.argv[2] == "debug":
    debug = True
else:
    debug = False

print "Debug mode: {d}".format(d=debug)

machine = vm.Processor(debug=debug)
filename = sys.argv[1]
parser.load_file_into_memory(machine.memory, filename)

machine.execute_until_halted(instructions_limit=5000)

print "Instructions executed: {i}".format(i=machine.instructions_executed)
print "Instructions executed by type:"
print machine.dump_instructions_executed_grouped()
print "Register bank after halting:"
print machine.register_bank.dump_content()