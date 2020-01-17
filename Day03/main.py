
def load_file():
    f = open('day03/sample1_159.txt', 'r')
    lines = f.read().splitlines()
    wires = []
    for l in lines:
        wires.append(l.split(','))
    f.close()
    return wires


def build_matrix(wire):
    pt = 0
    w = 0
    wmin = 0
    wmax = 0
    h = 0
    hmin = 0
    hmax = 0
    for p in wire:
        d = p[0]
        v = int(p[1:])
        if d == "U":
            h += v
            hmax = max(hmax, h)
        elif d == "D":
            h -= v
            hmin = min(hmin, h)
        elif d == "R":
            w += v
            wmax = max(wmax, w)
        elif d == "L":
            w -= v
            wmin = min(wmin, w)
    print(f"hmin: {hmin}, hmax: {hmax}, wmin: {wmin}, wmax: {wmax}")


wires = load_file()
for wire in wires:
    build_matrix(wire)
    print(wire)
