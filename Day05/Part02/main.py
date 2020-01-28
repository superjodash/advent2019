import sys
import computer


def main():
    runFile()
    # runTests()


def runFile():
    program = load_file()
    mem = runProgram(program)
    print(f"dump: {mem}")


def runTests():

    # # Equal (if input == 8, 1 otherwise 0), position mode
    # p1 = load_program("3,9,8,9,10,9,4,9,99,-1,8")
    # mem = runProgram(p1)

    # # Less Than (if input < 8, 1 otherwise 0), position mode
    # p1 = load_program("3,9,7,9,10,9,4,9,99,-1,8")
    # mem = runProgram(p1)

    # # Equal (if input == 8, 1 otherwise 0), immediate mode
    # p1 = load_program("3,3,1108,-1,8,3,4,3,99")
    # mem = runProgram(p1)

    # # Less Than (if input < 8, 1 otherwise 0), immediate mode
    # p1 = load_program("3,3,1107,-1,8,3,4,3,99")
    # mem = runProgram(p1)

    # # Jump false (opcode 6), position mode
    # p1 = load_program("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9")
    # mem = runProgram(p1)

    # # Jump true (opcode 5), immediate mode
    # p1 = load_program("3,3,1105,-1,9,1101,0,0,12,4,12,99,1")
    # mem = runProgram(p1)

    # # Full Test (if input < 8 (999), = 8 (1000), > 8 (1001))
    # p1 = load_program(
    #     "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99")
    # mem = runProgram(p1)
    pass


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
