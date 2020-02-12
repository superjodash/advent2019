import math

def main():
    runTest("Day10/Part01/sample1_8.map", [(3,4), 8])
    runTest("Day10/Part01/sample2_33.map", [(5,8), 33])
    runTest("Day10/Part01/sample3_35.map", [(1,2), 35])
    runTest("Day10/Part01/sample4_41.map", [(6,3), 41])
    runTest("Day10/Part01/sample5_210.map", [(11,13), 210])
    runTest("Day10/puzzle.map", None)

def runTest(fileName, expected):
    amap = load_file(fileName)
    result = analyze(amap)
    print(f"Best is {result[0]} with {result[1]} other asteroids detected")
    if(expected != None):
        assert result == expected, f"result should be {expected}"

def analyze(amap):
    maxcount = 0
    maxcoord = None

    for p in amap:
        vals = {}
        for p2 in amap:
            if(p == p2):
                continue
            dy, dx = calcSlope(p[0], p[1], p2[0], p2[1])
            s = 0
            if(dy == 0 or dx == 0): 
                if(dy == 0):
                    if(dx > 0):
                        key = "x0"
                    else:
                        key = "-x0"
                else:
                    if(dy > 0):
                        key = "y0"
                    else:
                        key = "-y0"
                vv = vals.get(key)
                if(vv == None):
                    vals[key] = [p2]
                else:
                    vv.append(p2)
                    vals[key] = vv
            else:
                s = dy / dx
                q = getQuad(dx, dy)
                s2 = f"{q}{s}"
                vv = vals.get(s2)
                if(vv == None):
                    vals[s2] = [p2]
                else:
                    vv.append(p2)
                    vals[s2] = vv
        lv = len(vals)
        if(lv > maxcount):
            maxcount = lv
            maxcoord = p
    
    return [maxcoord, maxcount]


def calcSlope(x1, y1, x2, y2):
    dy = y2 - y1
    dx = x2 - x1
    return [dy, dx]

def calcDistance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 ) + ((y2 - y1) ** 2)

def getQuad(x, y):
    if(x > 0 and y > 0):
        return 0
    elif(x > 0 and y < 0):
        return 1
    elif(x < 0 and y > 0):
        return 2
    elif(x < 0 and y < 0):
        return 4

def load_file(filename):
    f = open(filename, 'r')
    y = 0
    amap = []
    for l in f.read().splitlines():
        x = 0
        for v in l:
            if(v == "#"):
                amap.append((x,y))
            x += 1
        y += 1
    f.close()
    return amap

main()