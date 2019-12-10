import os
import math
currentdir = os.path.dirname(os.path.abspath(__file__))

def read_asteroids(filename):
    """Returns a list of asteroid locations in the map provided in the file

    Parameters
    ----------

    filename : str
        path/name of file that contains the asteroid map
    """
    asteroids = []
    with open(filename, "r") as f:
        lines = f.read().splitlines()
        for y in range(len(lines)):
            for x in range(len(lines[y])):
                if lines[y][x] == "#":
                    asteroids.append((x, y))

    return asteroids

def prefilter_blocks(asteroids, asteroid1, asteroid2):
    """Returns all asteroids that are potentially between asteroid1 and asteroid2"""

    blocks = []
    x1 = min(asteroid1[0], asteroid2[0])
    x2 = max(asteroid1[0], asteroid2[0])
    y1 = min(asteroid1[1], asteroid2[1])
    y2 = max(asteroid1[1], asteroid2[1])

    for (x, y) in asteroids:
        if (x, y) == asteroid1 or (x, y) == asteroid2:
            continue
        if x < x1 or x > x2 or y < y1 or y > y2:
            continue
        if x1 != x2 and (x == x1 or x == x2):
            continue
        if y1 != y2 and (y == y1 or y == y2):
            continue
        blocks.append((x, y))

    return blocks

def calc_angle(asteroid1, asteroid2):
    """Calculates the angle from asteroid1 to asteroid2
    up = 0, angle increases clockwise
    """
    x1, y1 = asteroid1
    x2, y2 = asteroid2
    if x1 == x2:
        if y2 < y1:
            return 0
        return 180
    dx = x2 - x1
    dy = y1 - y2
    angle = math.degrees(math.atan2(dy, dx)) - 90
    angle = 360 - angle
    if angle >= 360:
        angle = angle - 360
    return angle

def calc_visibility(asteroid, asteroids):
    """Returns a list of asteroids that are visibible from one specific one"""
    x1, y1 = asteroid
    visibilities = []
    for (x2, y2) in asteroids:
        if (x1, y1) == (x2, y2):
            continue

        angle1 = calc_angle((x1, y1), (x2, y2))

        free_sight = True
        for (x3, y3) in prefilter_blocks(asteroids, (x1, y1), (x2, y2)):
            angle2 = calc_angle((x1, y1), (x3, y3))
            if angle1 == angle2:
                free_sight = False
                break

        if free_sight:
            visibilities.append((x2, y2))

    return visibilities

def calc_visibilities(asteroids):
    """Returns a list of all asteroid pairs that are visible from each other

    Parameters
    ----------

    asteroids : list<(int, int)>
        The coordinates of all asteroids
    """
    visibilities = []

    for a, (x1, y1) in enumerate(asteroids):
        visibility = calc_visibility((x1, y1), asteroids[(a+1):])
        for v in visibility:
            visibilities.append(((x1, y1), v))

    return visibilities

def best_location(filename):
    """Returns the asteroid with the most visible asteroids, and the according number

    Parameters
    ----------

    filename : str
        path/name of file that contains the asteroid map
    """

    asteroids = read_asteroids(filename)
    visibilities = calc_visibilities(asteroids)

    best_asteroid = None
    best_visibility = 0
    for asteroid in asteroids:
        visibility = len([v for v in visibilities if v[0] == asteroid or v[1] == asteroid])
        if visibility > best_visibility:
            best_asteroid = asteroid
            best_visibility = visibility

    return (best_asteroid, best_visibility)

def destroy_200(filename, laser):
    """Part 2 of the challenge"""
    asteroids = read_asteroids(filename)
    visibilities = calc_visibility(laser, asteroids)
    visibilities.sort(key=lambda v: calc_angle(laser, v))
    return visibilities[199][0] * 100 + visibilities[199][1]

assert best_location(os.path.join(currentdir, "testinput1.txt")) == ((3, 4), 8)
assert best_location(os.path.join(currentdir, "testinput2.txt")) == ((5, 8), 33)
assert best_location(os.path.join(currentdir, "testinput3.txt")) == ((1, 2), 35)
assert best_location(os.path.join(currentdir, "testinput4.txt")) == ((6, 3), 41)
testresult = best_location(os.path.join(currentdir, "testinput5.txt"))
assert testresult == ((11, 13), 210)

result = best_location(os.path.join(currentdir, "input.txt"))
print("Part 1: %s %s" % result)

assert destroy_200(os.path.join(currentdir, "testinput5.txt"), testresult[0]) == 802
print("Part 2: %s" % destroy_200(os.path.join(currentdir, "input.txt"), result[0]))
