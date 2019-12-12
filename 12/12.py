import math


def sign(number):
    if number > 0:
        return 1
    if number < 0:
        return -1
    return 0


def lcm(a, b):
    return int(a * b / math.gcd(a, b))


class Moon(object):

    def __init__(self, position, velocity=(0, 0, 0)):
        self.position = position
        self.velocity = velocity

    def __repr__(self):
        x, y, z = self.position
        dx, dy, dz = self.velocity
        return "(%s,%s,%s),(%s,%s,%s)" % (x, y, z, dx, dy, dz)

    def apply_gravity(self, other):
        self.velocity = tuple(self.velocity[i] + sign(other.position[i] - self.position[i]) for i in range(3))

    def apply_velocity(self):
        self.position = tuple(self.position[i] + self.velocity[i] for i in range(3))

    def energy(self):
        return sum(abs(p) for p in self.position) * sum(abs(v) for v in self.velocity)


def move_moons(moons, steps):
    for _ in range(steps):
        for a in range(len(moons) - 1):
            for b in range(a + 1, len(moons)):
                moons[a].apply_gravity(moons[b])
                moons[b].apply_gravity(moons[a])

        for moon in moons:
            moon.apply_velocity()


def total_energy(moons):
    return sum(moon.energy() for moon in moons)


def state(moons, axis):
    return tuple((moon.position[axis], moon.velocity[axis]) for moon in moons)


def find_repetition(moons):
    steps = 0
    loops = [0, 0, 0]
    states = [{}, {}, {}]
    while True:
        for a in range(3):
            if loops[a] == 0:
                axis_state = state(moons, a)
                if axis_state in states[a]:
                    loops[a] = steps
                else:
                    states[a][axis_state] = True

        if loops[0] > 0 and loops[1] > 0 and loops[2] > 0:
            break

        move_moons(moons, 1)
        steps = steps + 1

    return lcm(lcm(loops[0], loops[1]), loops[2])


"""
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
"""
moons = [
  Moon((-1, 0, 2)),
  Moon((2, -10, -7)),
  Moon((4, -8, 8)),
  Moon((3, 5, -1))
]

move_moons(moons, 10)
assert total_energy(moons) == 179

"""
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
"""
moons = [
  Moon((-8, -10, 0)),
  Moon((5, 5, 10)),
  Moon((2, -7, 3)),
  Moon((9, -8, -3))
]

move_moons(moons, 100)
assert total_energy(moons) == 1940

"""
<x=-7, y=-8, z=9>
<x=-12, y=-3, z=-4>
<x=6, y=-17, z=-9>
<x=4, y=-10, z=-6>
"""
moons = [
  Moon((-7, -8, 9)),
  Moon((-12, -3, -4)),
  Moon((6, -17, -9)),
  Moon((4, -10, -6))
]

move_moons(moons, 1000)
print("Part 1: %s" % total_energy(moons))


moons = [
  Moon((-1, 0, 2)),
  Moon((2, -10, -7)),
  Moon((4, -8, 8)),
  Moon((3, 5, -1))
]
assert find_repetition(moons) == 2772

moons = [
  Moon((-8, -10, 0)),
  Moon((5, 5, 10)),
  Moon((2, -7, 3)),
  Moon((9, -8, -3))
]
assert find_repetition(moons) == 4686774924

moons = [
  Moon((-7, -8, 9)),
  Moon((-12, -3, -4)),
  Moon((6, -17, -9)),
  Moon((4, -10, -6))
]
print("Part 2: %s" % find_repetition(moons))
