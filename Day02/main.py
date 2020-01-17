import computer

instrptr: int = 0
program = []
ops = {1: 4, 2: 4, 99: 1}


def load_file():
    f = open('program.intcode', 'r')
    x = [int(x) for x in f.read().split(',')]
    f.close()
    return x


program = load_file()

expectedAnswer = 19690720
computedAnswer = 0
mem0 = 0

for noun in range(0, 100):
    for verb in range(0, 100):
        cx = computer.Computer(program)
        cx.memory_write(1, noun)
        cx.memory_write(2, verb)
        try:
            cx.run()
            mem0 = cx.memory_read(0)
            #print(f"Job [{mem0}, {noun}, {verb}]")
        except:
            mem0 = cx.memory_read(0)
            print(f"CRASH [{mem0}, {noun}, {verb}]")

        if mem0 == expectedAnswer:
            print(f"Correct combination found: mem0: {mem0}, noun: {noun}, verb: {verb}")
            break
