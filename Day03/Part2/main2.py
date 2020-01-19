mat = []
file = "Day03/Part2/sample0_30"

def main():
    global mat
    wires = load_file()
    ewires = []
    for w in wires:
        ewires.append(expand(w))
    print(ewires)
    
    #mat = [0 for x in range(dim * dim)]

    

def load_file():
    f = open(file + ".txt", 'r')
    lines = f.read().splitlines()
    wires = []
    for l in lines:
        wires.append(l.split(','))
    f.close()
    return wires

def expand(wire):
    exp = []
    for point in wire:
        d = point[0] # direction
        v = int(point[1:]) # vector
        for r in range(0, v):
            exp.append(d+"1")
    return exp

main()