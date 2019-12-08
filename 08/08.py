import os
currentdir = os.path.dirname(os.path.abspath(__file__))

LAYER_WIDTH = 25
LAYER_HEIGHT = 6
LAYER_SIZE = LAYER_WIDTH * LAYER_HEIGHT

BLACK = "0"
WHITE = "1"
TRANSPARENT = "2"

def read_layers(inputfile):
    with open(inputfile) as f:
        data = f.read().splitlines()[0]

    layer_count = len(data) // LAYER_SIZE

    layers = []
    for l in range(layer_count):
        layer_start = l * LAYER_SIZE
        layer_end = layer_start + LAYER_SIZE
        layers.append(data[layer_start:layer_end])

    return layers

def part1(inputfile):
    layers = read_layers(inputfile)
    layer = min(layers, key=lambda l: l.count("0"))
    return layer.count("1") * layer.count("2")

def part2(inputfile, pretty=True):
    layers = read_layers(inputfile)
    image = ""
    for p in range(LAYER_SIZE):
        for layer in layers:
            if layer[p] == TRANSPARENT:
                continue
            image = image + layer[p]
            break

    if pretty:
        image = image.replace(BLACK, " ")
        image = image.replace(WHITE, "#")

    rows = []
    for row in range(LAYER_HEIGHT):
        row_start = row * LAYER_WIDTH
        row_end = row_start + LAYER_WIDTH
        rows.append(image[row_start:row_end])
    
    return "\n".join(rows)

print("Part 1: %s" % part1(os.path.join(currentdir, "input.txt")))
print("Part 2:\n%s" % part2(os.path.join(currentdir, "input.txt")))
