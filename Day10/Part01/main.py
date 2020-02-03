# Sample 1 - (3,4), 8 asteroids
# Sample 2 - (5,8), 33 asteroids
from grid import Grid


def main():

    w, h, amap = load_file("Day10/Part01/sample1.map")

    print(f"Width: {w}, Height: {h}")
    # renderMap(w, h, amap)
    # result = processMapA(w, h, amap)
    testing(w, h, amap)
#    print(result)


def testing(width, height, amap):
    g = Grid(width, height)
    get_asteroid_coords(g, amap)

    for ix in range(g.length()):
        runIteration(ix, g)

    # draw_grid(g)

    return ""

def runIteration(index, grid):
    slopes = {}
    astCount = 0
    for y in range(grid.height):
        for x in range(grid.width):
            x2, y2 = grid.indexToCoordinate(index)
            if grid.coordinateToIndex(x, y) == index:
                continue
            if grid.get(x, y) == 1:
                s = calcSlope(x, y, x2, y2)
                if slopes.get((x,y)) != None:                  
                    pass
                    # this slope is already in the collection; collision?
                else:
                    slopes[(x,y)] = calcSlope(x, y, x2, y2)
                    astCount += 1

                # calc slope and keep

def get_asteroid_coords(grid, amap):
    for y in range(grid.height):
        for x in range(grid.width):
            if(amap[y * grid.width + x] == "#"):
                grid.add(x, y, 1)

def draw_grid(grid):
    for y in range(grid.height):
        for x in range(grid.width):
            if((x, y) in grid.walls):
                print("#", end="")
            else:
                print(".", end="")
        print()




# def processMapA(width, height, amap):
#     for y in range(0, height):
#         for x in range(0, width):
#             count = runIteration(x, y, width, height, amap)

#     return ""

# def runIteration(cx,cy,width,height,amap):
#     curr = cy * width + cx
#     for y in range(0, height):
#         for x in range(0, width):
#             tindex = y * width + x
#             if(curr == tindex):
#                 continue
#             test = amap[tindex]
#             slope = calcSlope(cx, cy, x, y)


def calcSlope(x1, y1, x2, y2):
    y = y2 - y1
    x = x2 - x1
    return [x, y, y / x]


# def renderMap(width, height, amap):
#     for h in range(height):
#         line = ""
#         for w in range(width):
#             line += amap[h * width + w]
#         print(line)


def load_file(filename):
    f = open(filename, 'r')
    w = 0
    h = 0
    amap = []
    for l in f.read().splitlines():
        w = len(l)
        amap.extend(list(l))
        h += 1
    f.close()
    return [w, h, amap]


main()
