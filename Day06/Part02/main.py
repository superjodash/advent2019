import sys
from anytree import Node, RenderTree, AsciiStyle, PostOrderIter


def main():
    runFile("Day06/map.txt")
    # runFile("Day06/Part02/sample_4.txt")


def runFile(filename):
    program = load_file(filename)
    list = create_tree_list(program)

    you = list["YOU"]
    san = list["SAN"]

    # alternate traversal from each end until depth is same?
    yd = you.parent  # start with item you is orbiting
    sd = san.parent  # start with item san is orbiting
    count = 0
    while yd.name != sd.name:
        if yd.depth > sd.depth:
            print(f"YOU at ({yd.name},{yd.depth}). Going down")
            yd = yd.parent
            count += 1
        else:
            print(f"SAN at ({sd.name},{sd.depth}). Going down")
            sd = sd.parent
            count += 1

    print(f"SAN at ({sd.name},{sd.depth}). SAN at ({sd.name},{sd.depth})")
    print(f"Transfers: {count}")

    #renderTreeToFile(filename, tree)
    #nodes = countNodes(tree)
    #print(f"Nodes: {nodes}")


def renderTreeToFile(filename, tree):
    f = open(filename + "_out.txt", "w")
    for pre, _, node in RenderTree(tree, style=AsciiStyle()):
        f.write("%s%s\r" % (pre, node.name))


def create_tree_list(program):
    list = {}
    for n in program:
        centerName = n[0]
        center = list.get(centerName)
        if(center == None):
            center = Node(centerName)
            list[centerName] = center

        orbiterName = n[1]
        orbiter = list.get(orbiterName)
        if(orbiter == None):
            orbiter = Node(orbiterName, parent=center)
            list[orbiterName] = orbiter
        elif orbiter.parent == None:
            orbiter.parent = center

    return list


def countNodes(tree):
    depth = 0
    for node in PostOrderIter(tree):
        depth += node.depth
    return depth


def load_file(fileName):
    f = open(fileName, 'r')
    lines = f.read().splitlines()
    orbits = []
    for l in lines:
        orbits.append(l.split(')'))
    f.close()
    return orbits


main()
