import sys
import computer


def main():
    runFile()
    #runTests()

def runFile():
    program = load_file()
    mem = runProgram(program)
    print(f"dump: {mem}")

def runTests():
    #p1 = load_program("3,0,4,0,99")
    # mem = runProgram(p1)
    
    p1 = load_program("1002,4,3,4,33")
    mem = runProgram(p1)
    assert mem[4] == 99

    p1 = load_program("1101,100,-1,4,0")
    mem = runProgram(p1)
    assert mem[4] == 99


def runProgram(program):
    cx = computer.Computer(program)
    try:
        cx.run()
        return cx.memory_dump()
    except ValueError as e:
        print(f"Exception: {e}")
        #mem0 = cx.memory_read(0)
        #print(f"CRASH [{mem0}]")
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def load_file():
    f = open('Day05/program.intcode', 'r')
    x = [int(x) for x in f.read().split(',')]
    f.close()
    return x


def load_program(input):
    x = [int(x) for x in input.split(',')]
    return x


main()
