from xsvm import vm, parser
from argparse import ArgumentParser


args = ArgumentParser()
args.add_argument("filename")
args.add_argument("-d", "--debug", action="store_true", default=False)
args.add_argument("-m", "--max-instructions", metavar='', type=int, default=5000)
args = args.parse_args()

print("Debug mode: {d}".format(d=args.debug))

machine = vm.Processor(debug=args.debug)
parser.load_file_into_memory(machine.memory, args.filename)

machine.execute_until_halted(instructions_limit=args.max_instructions)

print("Instructions executed: {i}".format(i=machine.instructions_executed))
print("Instructions executed by type:")
print(machine.dump_instructions_executed_grouped())
print("Register bank after halting:")
print(machine.register_bank.dump_content())
