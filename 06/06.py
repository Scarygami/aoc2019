import os
currentdir = os.path.dirname(os.path.abspath(__file__))

class Tree:
    def __init__(self, id):
        self.id = id
        self.children = []
        self.parent = None

    def __repr__(self):
        return f"{self.id}"

def construct_tree(inputfile):
    root = None
    nodes = {}

    with open(inputfile, "r") as f:
        for line in f.read().splitlines():
            p, c = line.split(")")
            parent = nodes.get(p, Tree(p))
            nodes[p] = parent
            child = nodes.get(c, Tree(c))
            nodes[c] = child
            parent.children.append(child)
            child.parent = parent

    for node in nodes.values():
        if node.parent is None:
            root = node
            break

    you = nodes.get("YOU", None)
    santa = nodes.get("SAN", None)

    return (root, you, santa)

def count_orbits(node, depth = 0):
    orbits = depth
    for child in node.children:
        orbits = orbits + count_orbits(child, depth + 1)

    return orbits

def get_parents(node):
    if node.parent is None:
        return []
    parents = [node.parent.id]
    parents.extend(get_parents(node.parent))
    return parents

def find_path(node1, node2):
    """Finds the length of the path from node1 to node2

    This is done by looking at the list of parents
    and finding the first common parent.
    """

    parents1 = get_parents(node1)
    parents2 = get_parents(node2)
    for l1 in range(len(parents1)):
        if parents1[l1] in parents2:
            l2 = parents2.index(parents1[l1])
            return l1 + l2

    return 0

root, _ ,_ = construct_tree(os.path.join(currentdir, "testinput.txt"))
assert count_orbits(root) == 42

root, _, _ = construct_tree(os.path.join(currentdir, "input.txt"))
print("Part 1: %s" % count_orbits(root))

_, you, santa = construct_tree(os.path.join(currentdir, "testinput2.txt"))
assert find_path(you, santa) == 4

_, you, santa = construct_tree(os.path.join(currentdir, "input.txt"))
print("Part 2: %s" % find_path(you, santa))
