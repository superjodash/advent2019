mat = []
dim = 25000
center = [int(dim / 2), int(dim / 2)]
file = "Day03/input"

def main():
    global mat
    wires = load_file()
    wnum = 1
    mat = [0 for x in range(dim * dim)]
    for wire in wires:
        plot(wire, wnum)
        wnum *= 2

    points = mat_filter()
    closest = get_closest_point(points)
    print(f"Closes point {closest}")
    #mat_dump()


def load_file():
    f = open(file + ".txt", 'r')
    lines = f.read().splitlines()
    wires = []
    for l in lines:
        wires.append(l.split(','))
    f.close()
    return wires

def mat_dump():
    global dim
    global mat
    f = open(file + "_out.txt", "w")
    for y in range(0, dim):
        for x in range(0, dim):
            val = str(mat_read(x, y))
            if(val == "0"):
                val = "."
            f.write(val)
        f.write("\r")
    f.close()

def plot(wire, wirenum):
    global dim
    global mat
    global center

    x = center[0]
    y = center[1]
    mat_write(x, y, 9)
    for point in wire:
        d = point[0] # direction
        v = int(point[1:]) # vector
        vert = True if d == "U" or d == "D" else False
        dx = x
        dy = y
        if d == "U":     # -y
            dy -= v
            v *= -1
        elif d == "D":   # +y
            dy += v
        elif d == "R":   # x
            dx += v
        else:            # -x
            dx -= v
            v *= -1

        draw_line(x, y, vert, v, wirenum)
        x = dx
        y = dy

def draw_line(x, y, vert, l, value):
    # x,y - start position
    # vert(ical) - if true, inc y, else inc x
    # l(ength) - if negative, go opposite direction
    # value = tracking value
    mag = abs(l)
    rev = True if l < 0 else False
    
    if(vert == True):
        dy = y
        if(rev):
            dy -= mag+1 # go up and draw down
        for m in range(1, mag + 1, 1):
            dy += 1
            val = mat_read(x, dy)
            if(val == 0):
                #print(f"0)writing ({x},{dy}): {value}")
                mat_write(x, dy, value)
            elif(val == value):
                pass
            else:
                #print(f"+)writing ({x},{dy}): {8}")
                mat_write(x, dy, 8)

    else:
        dx = x
        if(rev):
            dx -= mag+1 # go left and draw right
        for m in range(1, mag + 1, 1):
            dx += 1
            val = mat_read(dx, y)
            if(val == 0):
                #print(f"0)writing ({dx},{y}): {value}")
                mat_write(dx, y, value)
            elif(val == value):
                pass
            else:
                #print(f"+)writing ({dx},{y}): {8}")
                mat_write(dx, y, 8)

def mat_filter():
    global dim
    global mat

    points = []

    for y in range(0, dim):
        for x in range(0, dim):
            val = mat_read(x, y)
            if(val == 8):
                points.append([x,y])
    
    return points

def get_closest_point(points):
    global center
    closest = None
    for p in points:
        dist = get_man_dist(center, p)
        print(f"Manhattan Distance for point {p}: {dist}")
        if(closest == None or dist < closest):
            closest = dist
    return closest

def get_man_dist(a,b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def mat_write(x, y, value):
    global dim
    global mat
    mat[y * dim + x] = value

def mat_read(x, y):
    global dim
    global mat
    return mat[y * dim + x]

main()