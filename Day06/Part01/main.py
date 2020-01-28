import sys
from anytree import Node, RenderTree, AsciiStyle, PostOrderIter


def main():
    runFile("Day06/map.txt")
    # runFile("Day06/Part01/sample_42.txt")


def runFile(filename):
    program = load_file(filename)
    tree = create_tree(program)
    # for pre, _, node in RenderTree(tree, style=AsciiStyle()):
    #     print("%s%s" % (pre, node.name))
    #renderTreeToFile(filename, tree)
    nodes = countNodes(tree)
    print(f"Nodes: {nodes}")


def renderTreeToFile(filename, tree):
    f = open(filename + "_out.txt", "w")
    for pre, _, node in RenderTree(tree, style=AsciiStyle()):
        f.write("%s%s\r" % (pre, node.name))


def create_tree(program):
    list = {}
    for n in program:
        centerName = n[0]
        center = list.get(centerName)
        if(center == None):
            #print(f"C Miss: {centerName}")
            center = Node(centerName)
            list[centerName] = center

        orbiterName = n[1]
        orbiter = list.get(orbiterName)
        if(orbiter == None):
            #print(f"O Miss: {orbiterName}")
            orbiter = Node(orbiterName, parent=center)
            list[orbiterName] = orbiter
        elif orbiter.parent == None:
            orbiter.parent = center

    tree = list["COM"]

    return tree


# def countNodes(tree, list = {}, level = 0):
#     for c in tree.children:
#         level += 1
#         list[c.name] = level
#         countNodes(c, list, level)
#     return 0

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
