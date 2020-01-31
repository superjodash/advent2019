# Sample 1 - (3,4), 8 asteroids
# Sample 2 - (5,8), 33 asteroids
from search import SquareGrid


def main():

    w, h, amap = load_file("Day10/Part01/sample1.map")

    print(f"Width: {w}, Height: {h}")
    # renderMap(w, h, amap)
    # result = processMapA(w, h, amap)
    result = testing(w, h, amap)
    print(result)


def testing(width, height, amap):
    g = SquareGrid(width, height)
    g.walls = get_asteroid_coords(width, height, amap)
    # draw_grid(g)

    return ""


def draw_grid(graph):
    for y in range(graph.height):
        for x in range(graph.width):
            if((x, y) in graph.walls):
                print("#", end="")
            else:
                print(".", end="")
        print()


def get_asteroid_coords(width, height, amap):
    asteroids = []
    for y in range(height):
        for x in range(width):
            if(amap[y * width + x] == "#"):
                asteroids.append((x, y))
    return asteroids

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


# def slope(x1, y1, x2, y2):
#     return (y2 - y1) / (x2 - x2)


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
