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

def calc_angle(asteroid1, asteroid2):
    """Calculates the angle in degress from asteroid1 to asteroid2
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

def calc_distance(asteroid1, asteroid2):
    """Calculates the distance between two asteroids"""
    x1, y1 = asteroid1
    x2, y2 = asteroid2
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx * dx + dy * dy)

def detectable(asteroid1, asteroid2, asteroids):
    """Returns true if asteroid2 is detectable from asteroid1, considering all asteroids"""
    angle1 = calc_angle(asteroid1, asteroid2)
    dist1 = calc_distance(asteroid1, asteroid2)

    for asteroid in asteroids:
        if asteroid == asteroid1 or asteroid == asteroid2:
            continue

        dist2 = calc_distance(asteroid1, asteroid)
        if dist2 > dist1:
            continue

        angle2 = calc_angle(asteroid1, asteroid)
        if angle1 != angle2:
            continue

        return False

    return True

def calc_visibility(asteroid, asteroids):
    """Returns a list of asteroids that are visibible from one specific one"""
    visibilities = []
    for asteroid2 in asteroids:
        if asteroid == asteroid2:
            continue

        if detectable(asteroid, asteroid2, asteroids):
            visibilities.append(asteroid2)

    return visibilities

def calc_visibilities(asteroids):
    """Returns a list of all asteroid pairs that are visible from each other

    Parameters
    ----------

    asteroids : list<(int, int)>
        The coordinates of all asteroids
    """
    visibilities = []

    for a, asteroid in enumerate(asteroids):
        visibility = calc_visibility(asteroid, asteroids[(a+1):])
        for v in visibility:
            visibilities.append((asteroid, v))

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

def use_laser(filename, laser, destroys=200):
    """Uses the laser until the specified amount of asteroids are destroyed
    
    Returns x*100 + y of the last destroyed asteroid"""

    asteroids = read_asteroids(filename)
    visibilities = []
    while len(visibilities) < destroys:
        destroys = destroys - len(visibilities)
        asteroids = [asteroid for asteroid in asteroids if asteroid not in visibilities]
        visibilities = calc_visibility(laser, asteroids)

    visibilities.sort(key=lambda v: calc_angle(laser, v))
    return visibilities[destroys - 1][0] * 100 + visibilities[destroys - 1][1]

assert best_location(os.path.join(currentdir, "testinput1.txt")) == ((3, 4), 8)
assert best_location(os.path.join(currentdir, "testinput2.txt")) == ((5, 8), 33)
assert best_location(os.path.join(currentdir, "testinput3.txt")) == ((1, 2), 35)
assert best_location(os.path.join(currentdir, "testinput4.txt")) == ((6, 3), 41)
testresult = best_location(os.path.join(currentdir, "testinput5.txt"))
assert testresult == ((11, 13), 210)

result = best_location(os.path.join(currentdir, "input.txt"))
print("Part 1: %s %s" % result)

assert use_laser(os.path.join(currentdir, "testinput5.txt"), testresult[0], 1) == 1112
assert use_laser(os.path.join(currentdir, "testinput5.txt"), testresult[0], 2) == 1201
assert use_laser(os.path.join(currentdir, "testinput5.txt"), testresult[0], 3) == 1202
assert use_laser(os.path.join(currentdir, "testinput5.txt"), testresult[0], 10) == 1208
assert use_laser(os.path.join(currentdir, "testinput5.txt"), testresult[0], 20) == 1600
assert use_laser(os.path.join(currentdir, "testinput5.txt"), testresult[0], 50) == 1609
assert use_laser(os.path.join(currentdir, "testinput5.txt"), testresult[0], 100) == 1016
assert use_laser(os.path.join(currentdir, "testinput5.txt"), testresult[0], 199) == 906
assert use_laser(os.path.join(currentdir, "testinput5.txt"), testresult[0], 200) == 802
assert use_laser(os.path.join(currentdir, "testinput5.txt"), testresult[0], 201) == 1009
assert use_laser(os.path.join(currentdir, "testinput5.txt"), testresult[0], 299) == 1101

print("Part 2: %s" % use_laser(os.path.join(currentdir, "input.txt"), result[0]))
