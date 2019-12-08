import os
currentdir = os.path.dirname(os.path.abspath(__file__))

LAYER_WIDTH = 25
LAYER_HEIGHT = 6
LAYER_SIZE = LAYER_WIDTH * LAYER_HEIGHT

BLACK = "0"
WHITE = "1"
TRANSPARENT = "2"

def read_layers(inputfile, size):
    with open(inputfile) as f:
        data = f.read().splitlines()[0]

    layer_count = len(data) // size

    layers = []
    for l in range(layer_count):
        layer_start = l * size
        layer_end = layer_start + size
        layers.append(data[layer_start:layer_end])

    return layers

def part1(inputfile, width, height):
    layers = read_layers(inputfile, width * height)
    layer = min(layers, key=lambda l: l.count("0"))
    return layer.count("1") * layer.count("2")

def part2(inputfile, width, height, pretty=True):
    size = width * height
    layers = read_layers(inputfile, size)
    image = ""
    for p in range(size):
        for layer in layers:
            if layer[p] == TRANSPARENT:
                continue
            image = image + layer[p]
            break

    if pretty:
        image = image.replace(BLACK, " ")
        image = image.replace(WHITE, "#")

    rows = []
    for row in range(height):
        row_start = row * width
        row_end = row_start + width
        rows.append(image[row_start:row_end])
    
    return "\n".join(rows)

assert part1(os.path.join(currentdir, "testinput1.txt"), 3, 2) == 1

print("Part 1: %s" % part1(os.path.join(currentdir, "input.txt"), 25, 6))

assert part2(os.path.join(currentdir, "testinput2.txt"), 2, 2, False) == "01\n10"

print("Part 2:\n%s" % part2(os.path.join(currentdir, "input.txt"), 25, 6))
