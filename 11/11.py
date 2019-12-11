import os
import sys
currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from lib.intcode import IntcodeVM

BLACK = 0
WHITE = 1

LEFT = 0
RIGHT = 1

# current_dir: ((dir_after_left_turn), (dir_after_right_turn))
TURNS = {
  ( 0, -1): ((-1,  0),( 1,  0)),
  (-1,  0): (( 0,  1),( 0, -1)),
  ( 0,  1): (( 1,  0),(-1,  0)),
  ( 1,  0): (( 0, -1),( 0,  1)),
}

def print_hull(hull):
    """Outputs the hull to stdout"""
    minx = min(hull, key=lambda panel: panel[0])[0]
    maxx = max(hull, key=lambda panel: panel[0])[0]
    miny = min(hull, key=lambda panel: panel[1])[1]
    maxy = max(hull, key=lambda panel: panel[1])[1]
    for y in range(miny, maxy + 1):
        row = ""
        for x in range(minx, maxx + 1):
            if hull.get((x, y), BLACK) == WHITE:
                row = row + "#"
            else:
                row = row + " "
        print(row)

def paint_hull(inputfile, hull={}):
    """Launches the emergency hull painting robot with the specified Intcode source file

    Parameters
    ----------

    inputfile: str
        Path/Filename of Intcode source code

    hull : dict<(int,int): int>
        Initial state of the hull
    """

    robot_pos = (0, 0)
    robot_dir = (0, -1)
    machine = IntcodeVM(inputfile, silent=True)
    machine.run()

    while machine.waiting:
        color, turn = machine.resume([hull.get(robot_pos, BLACK)])
        hull[robot_pos] = color
        robot_dir = TURNS[robot_dir][turn]
        robot_pos = (robot_pos[0] + robot_dir[0], robot_pos[1] + robot_dir[1])

    return hull

hull = paint_hull(IntcodeVM.read_intcode(os.path.join(currentdir, "input.txt")))
print("Part 1: %s" % len(hull.keys()))
print_hull(hull)

hull = paint_hull(IntcodeVM.read_intcode(os.path.join(currentdir, "input.txt")), {(0, 0): WHITE})
print("Part 2:")
print_hull(hull)
