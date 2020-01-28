import sys
import computer


def main():
    # runFile()
    runTests()


def runFile():
    #program = load_file()
    #mem = runProgram(program)
    #print(f"dump: {mem}")
    pass


def runTests():
    intcode = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
    sequences = [[4, 3, 2, 1, 0]]

    maxVal = 0
    for seq in sequences:
        output = max(maxVal, runProgram(intcode, seq))
    print(f"result: {output}")


def runProgram(intcode, sequence):
    output = 0
    for i in sequence:
        cx = computer.Computer(load_program(intcode))
        cx.input_add([i, output])
        output = cx.run().popleft()
    return output


def load_file():
    f = open('Day07/amplifier.intcode', 'r')
    x = [int(x) for x in f.read().split(',')]
    f.close()
    return x


def load_program(input):
    x = [int(x) for x in input.split(',')]
    return x


main()
