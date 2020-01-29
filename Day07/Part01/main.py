import sys
import computer


def main():
    runFile()
    # runTests()


def runFile():
    test = load_file()
    sequences = getSequences()
    
    maxVal = 0
    maxSeq = ""
    for seq in sequences:
        output = runProgram(test, seq)
        if(output > maxVal):
            maxVal = output
            maxSeq = seq
        maxVal = max(maxVal, output)
    print(f"result: {maxVal}, seq: {maxSeq}")

def runTests():
    tests = {
        43210:"3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0",
        54321:"3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0",
        65210:"3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"
    }
    sequences = getSequences()

    for expected in tests:
        test = load_program(tests[expected])
        maxVal = 0
        maxSeq = ""
        for seq in sequences:
            output = runProgram(test, seq)
            if(output > maxVal):
                maxVal = output
                maxSeq = seq
            maxVal = max(maxVal, output)
        print(f"result: {maxVal}, seq: {maxSeq}, expected: {expected}")


def runProgram(intcode, sequence):
    output = 0
    for i in sequence:
        cx = computer.Computer(intcode)
        cx.input_add([i, output])
        output = cx.run().popleft()
    return output

def getSequences():
    seq = []
    for a in range(0,5):
        for b in range(0,5):
            for c in range(0,5):
                for d in range(0,5):
                    for e in range(0,5):
                        v = [a,b,c,d,e]
                        if(is_valid(v)):
                            seq.append(v)
    return seq

def is_valid(value):
    if(value == [4,3,2,1,0]):
        value = [4,3,2,1,0]
    flag = [0,0,0,0,0]
    flag[value[0]] += 1
    flag[value[1]] += 1
    flag[value[2]] += 1
    flag[value[3]] += 1
    flag[value[4]] += 1
    return flag[0] == 1 and flag[1] == 1 and flag[2] == 1 and flag[3] == 1 and flag[4] == 1

def load_file():
    f = open('Day07/amplifier.intcode', 'r')
    x = [int(x) for x in f.read().split(',')]
    f.close()
    return x


def load_program(input):
    x = [int(x) for x in input.split(',')]
    return x


main()
