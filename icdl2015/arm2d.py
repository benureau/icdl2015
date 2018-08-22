import math


class RoboticArm(object):
    """A kinematic model of a robotic arm in 2D.

    Receives an array of angles (in degrees) as a motor commands.
    Return the position of the tip of the arm as a 2-tuple.
    """

    def __init__(self, dim=7, limit=150):
        """
        :param dim:    number of joints
        :param limit:  joints are able to move in (-limit, +limit)"""
        self.dim, self.limit = dim, limit
        # hold the last executed posture (x, y position of all joints).
        self.posture = [(0.0, 0.0)]*dim

    def execute(self, angles):
        """Return the position of the end effector. Accepts values in degrees."""
        u, v, sum_a, length = 0, 0, 0, 1.0/len(angles)
        self.posture = [(u, v)]
        for a in reversed(angles):
            sum_a += a
            # at zero pose, the tip is at x=0,y=1.
            sum_a_rad = math.radians(sum_a)
            u, v = u + length * math.sin(sum_a_rad), v + length * math.cos(sum_a_rad)
            self.posture.append((u, v))
        return v, u

    @property
    def M_bounds(self):
        return [(-self.limit, self.limit) for _ in range(self.dim)]

    @property
    def S_bounds(self):
        # should be 1.0, but previous code used this more general computation,
        # which yields 1.0000000000000002
        max_length = sum(self.dim*[1.0/self.dim])
        return [(-max_length, max_length), (-max_length, max_length)]
