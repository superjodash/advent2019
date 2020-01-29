width = 25
height = 6
dim = width * height


def main():
    img = load_file()

    layerCount = int(len(img) / dim)

    fewestZeros = None
    layerData = {}
    for layerIndex in range(0, layerCount):
        layer = layerData.get(layerIndex)
        if(layer == None):
            layer = [0, 0, 0]
            layerData[layerIndex] = layer
        for h in range(0, height):
            for w in range(0, width):
                pindex = (layerIndex * dim) + (h * width) + w
                pixel = img[pindex]
                print(f"Index: {pindex}, Value: {pixel}")
                layer[pixel] += 1
        if(fewestZeros == None):
            fewestZeros = layer
        else:
            if(fewestZeros[0] > layer[0]):
                fewestZeros = layer

    print(f"{fewestZeros} with value of {fewestZeros[1] * fewestZeros[2]}")


def load_file():
    f = open('Day08/puzzle.img', 'r')
    lst = [int(x) for i, x in enumerate(f.read())]
    f.close()
    return lst


main()
