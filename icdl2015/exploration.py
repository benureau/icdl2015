"""
Exploration strategy
"""
import math
import collections

import numpy as np
import shapely.geometry
import shapely.ops

from . import random2 as random
from .neighbors import NNSet


def draw(p):
    assert len(p) >= 1
    """Given a vector p, return index i with probability p_i/sum(p).

    :param p:    list of positive numbers
    """
    # this function is unecessary complicated to retain random compatibility
    sum_p = sum(p)
    dice = random.uniform(0, sum_p)
    if sum_p == 0.0:
        return random.randint(0, len(p)-1)
    s, i = p[0], 0
    while (i < len(p)-1 and dice >= s):
        i += 1
        assert p[i] >= 0, 'all elements of {} are not positive'.format(p)
        s += p[i]
    return i


def diversity_score(points, τ):
    areas = [shapely.geometry.Point(xy).buffer(τ) for xy in points]
    coverage = shapely.ops.unary_union(areas)
    return coverage.area


class DiversityMeasure:

    def __init__(self, τ, window):
        self.τ = τ
        self.window = window
        self.diversity_diffs = {'goal':  collections.deque([math.pi*self.τ**2], self.window),
                                'motor': collections.deque([math.pi*self.τ**2], self.window)}
        # coverage: area occupied by the points
        self.coverage = shapely.geometry.MultiPolygon([])

    def add_effect(self, name, effect):
        old_area = self.coverage.area
        new_point_area = shapely.geometry.Point(effect).buffer(self.τ)
        # adding the newly explored area to the past one.
        self.coverage = self.coverage.union(new_point_area)
        # attribution to the corresponding explorer of the difference (possibly 0)
        self.diversity_diffs[name].append(self.coverage.area - old_area)

    def diversity(self, name):
        divdiffs = self.diversity_diffs[name]
        return sum(divdiffs)/len(divdiffs)


class AdaptDiversity:
    """
    :param M_bounds:  motor space boundaries, as a list of (min, max) tuples.
    :param S_bounds:  sensory space boundaries, as a list of (min, max) tuples.
    :param d:         disturb parameter for the random goal babbling.
    :param α:         ratio of random choices, where a random strategy is
                      chosen, rather than one based on the diversity score.
    :param τ:         threshold value for hyperball diversity computation.
    :param window:    how many timesteps to consider when computing diversity.
    """

    def __init__(self, M_bounds, S_bounds, d, α, τ, window):
        self.random_motor = RandomMotorExplorer(M_bounds)
        self.random_goal = RandomGoalExplorer(M_bounds, S_bounds, d)
        self.diversity = DiversityMeasure(τ, window)
        self.α = α
        self.last_explorer = None

    def explore(self):
        # choosing the explorer
        a = random.random()
        if a < self.α: # randomly choosing a strategy
            explorer = random.choice([self.random_motor, self.random_goal])
        else: # choosing proportionally to past diversity
            i = draw(self.diversities())
            explorer = [self.random_motor, self.random_goal][i]
        self.last_explorer = explorer.name
        return explorer.explore()

    def diversities(self):
        return np.array([self.diversity.diversity('motor'),
                         self.diversity.diversity('goal')])

    def add_observation(self, command, effect):
        self.random_goal.add_observation(command, effect)
        self.diversity.add_effect(self.last_explorer, effect)


class FixedMixture:

    def __init__(self, M_bounds, S_bounds, d, motor_ratio):
        self.random_motor = RandomMotorExplorer(M_bounds)
        self.random_goal = RandomGoalExplorer(M_bounds, S_bounds, d)
        self.motor_ratio = motor_ratio

    def explore(self):
        if random.random() < self.motor_ratio:
            explorer = self.random_motor
        else:
            explorer = self.random_goal
        return explorer.explore()

    def add_observation(self, command, effect):
        self.random_goal.add_observation(command, effect)


class RandomMotorExplorer:
    name = 'motor'

    def __init__(self, M_bounds):
        self.M_bounds = M_bounds

    def explore(self):
        """Return a motor command to try"""
        return [random.uniform(a, b) for a, b in self.M_bounds]


class RandomGoalExplorer:
    name = 'goal'

    def __init__(self, M_bounds, S_bounds, d):
        self.inverse = InverseModel(d, M_bounds)
        self.M_bounds, self.S_bounds = M_bounds, S_bounds

    def explore(self):
        """Return a motor command to try"""
        # choose a random goal
        self.goal = [random.uniform(a, b) for a, b in self.S_bounds]

        # choose a corresponding motor command
        try:
            command = self.inverse.inverse(self.goal)
            return command
        except ValueError:
            random.choice([0]) # to keep random draw exactly similar
            return [random.uniform(a, b) for a, b in self.M_bounds]

    def add_observation(self, command, effect):
        self.inverse.add_observation(command, effect)


class InverseModel:

    def __init__(self, d, M_bounds):
        self.d        = d
        self.M_bounds = M_bounds
        self.nn       = NNSet()

    def add_observation(self, command, effect):
        """Add an observation, to be available for nearest neighbors requests"""
        self.nn.add(command, effect)

    def inverse(self, goal):
        """Inverse model: takes a goal; generate a corresponding motor command"""
        # find the nearest command
        nn_command, nn_effect = self.nn.nn_y(goal)

        # perturbate the command
        new_command_a, new_command = [], []
        for m_i, (m_i_min, m_i_max) in zip(nn_command, self.M_bounds):
            min_i = max(m_i_min, m_i - self.d * (m_i_max - m_i_min))
            max_i = min(m_i_max, m_i + self.d * (m_i_max - m_i_min))
            new_command.append(random.uniform(min_i, max_i))

        random.choice([0]) # to keep random draws exactly similar
        return new_command
