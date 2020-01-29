import sys
from acu import AmplifierControlUnit
import computer


def main():
    # runFile()
    runTests()


def runFile():
    test = load_file()
    sequences = getSequences(5,9)
    
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
        139629729:"3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5",
        18216:"3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"
    }
    sequences = getSequences(5,9)

    for expected in tests:
        test = load_program(tests[expected])
        maxVal = 0
        maxSeq = ""
        for seq in sequences:
            unit = AmplifierControlUnit(seq, test)
            output = unit.run()
            if(output > maxVal):
                maxVal = output
                maxSeq = seq
            maxVal = max(maxVal, output)
        print(f"result: {maxVal}, expected: {expected}, seq: {maxSeq}")


def runProgram(intcode, sequence):
    output = 0
    for i in sequence:
        print(f"running sequence {i} with input {output}")
        cx = computer.Computer(intcode)
        cx.input_add([i, output])
        while(cx.step()):
            if(len(cx.output_queue) > 0):
                op = cx.output_queue.popleft()
                print(f"\tfeeding output {op}")
                cx.input_add([op])
        output = cx.last_output
    return output

def getSequences(start,end):
    seq = []
    for a in range(start,end+1):
        for b in range(start,end+1):
            for c in range(start,end+1):
                for d in range(start,end+1):
                    for e in range(start,end+1):
                        v = [a,b,c,d,e]
                        if(is_valid(v, start)):
                            seq.append(v)
    return seq

def is_valid(value, m):
    flag = [0,0,0,0,0]
    flag[value[0]%m] += 1
    flag[value[1]%m] += 1
    flag[value[2]%m] += 1
    flag[value[3]%m] += 1
    flag[value[4]%m] += 1
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
