"""
 starting coord for:
    sample1.map - (8,3)
    sample2.map - (11,13)
    puzzle.map - (20, 20)
 """
import math

def main():
    runTest("Day10/Part02/sample1.map", (8,3))
    #runTest("Day10/Part02/sample2.map", (11,13))
    #runTest("Day10/puzzle.map", (20,20))

def runTest(fileName, startPosition):
    amap = load_file(fileName)
    print(amap)
    amap = convertToCartisian(amap, startPosition)
    vectors = convertToVectors(amap, startPosition)
    print(amap)
    #result = analyze(amap, startPosition)
    #print(f"Best is {result[0]} with {result[1]} other asteroids detected")

def convertToCartisian(amap, startPosition):
    """
        make the startPosition == 0,0 and adjust all coords to that
        then calculcate angles for each point and rotate around that point
    """
    newmap = []
    for p in amap:
        newmap.append((p[0]-startPosition[0], p[1]-startPosition[1]))
    return newmap

def convertToVectors(amap, startPosition):
    vecs = {}
    for p in amap:
        angle = calcAngle(p)
        dist = calcDistance(0,0,p[0],p[1])
        coord = vecs.get(angle)
        if coord != None:
            print(f"Vector ({angle},{dist})")
        else:
            vecs[angle] = dist
    return vecs

def calcAngle(point):
    h = calcDistance(0, 0, point[0], point[1]) # always in first quadrant - need whole circle
    rads = math.radians(point[1] / h)
    v = 1/math.sin(rads)
    return v


def analyze(amap, startPosition):
    maxcount = 0
    maxcoord = None

    p = startPosition
    vals = {}
    for p2 in amap:
        if(p == p2):
            continue
        dy, dx = calcSlope(p[0], p[1], p2[0], p2[1])
        s = 0
        if(dy == 0 or dx == 0): 
            if(dy == 0):
                if(dx > 0):
                    key = f"0{dx}"
                else:
                    key = f"3{dx}"
            else:
                if(dy > 0):
                    key = f"4{dy}"
                else:
                    key = f"2{dy}"
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
    return math.sqrt((x2 - x1) ** 2  + (y2 - y1) ** 2)

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