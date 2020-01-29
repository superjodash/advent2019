"""
    Draw the image
    Layers are top to bottom in the file
        0 is black
        1 is white
        2 is transparent

"""
width = 25
height = 6
dim = width * height


def main():
    img = load_file()

    layerCount = int(len(img) / dim)

    # initialize buffer to  all transparent [2,2,...2]
    buffer = [2 for x in range(0, dim)]

    for layerIndex in range(layerCount-1, -1, -1):
        for h in range(0, height):
            for w in range(0, width):
                bindex = h * width + w
                #bpixel = buffer[bindex]

                pindex = (layerIndex * dim) + (h * width) + w
                pixel = img[pindex]

                if(pixel == 2):
                    pass  # leave buffer pixel if transparent
                else:
                    buffer[bindex] = pixel  # overwrite pixel value

    write_img(buffer)


def write_img(data):
    f = open("Day08/Part02/puzzle_out.img", "w")
    for y in range(0, height):
        for x in range(0, width):
            val = data[y * width + x]
            if(val == 2):
                val = " "
            elif(val == 1):
                val = "X"
            else:
                val = " "
            f.write(val)
        f.write("\r")
    f.close()


def load_file():
    f = open('Day08/puzzle.img', 'r')
    lst = [int(x) for i, x in enumerate(f.read())]
    f.close()
    return lst


main()
