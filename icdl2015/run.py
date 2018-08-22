import os
import pickle
import subprocess

import numpy as np
import reproducible

from . import random2 as random

from .exploration import AdaptDiversity, FixedMixture, diversity_score
from .arm2d import RoboticArm


def just_run(seed, # random seed
             T,    # number of trials
             ## arm
             dim,         # arm dimension,
             limit,       # arm angle limit
             ## exploration strategy
             d,           # disturb factor
             adapt_on,    # if False, diversity adaption is disabled
             motor_ratio=None, # if `adapt_on` is False, the (fixed) probability to
                               # choose the random motor babbling strategy
             τ=0.02,      # coverage threshold (will be used even if adapt_on is
                          # False to compute the total diversity
             α=None,      # if `adapt_on` is True, ratio of random choice of strategy
             window=None  # if `adapt_on` is True, number of past trials to consider
                          # when computing diversity.
            ):

    random.seed(seed)

    arm = RoboticArm(dim, limit)
    if adapt_on:
        explorer = AdaptDiversity(arm.M_bounds, arm.S_bounds, d, α, τ, window)
    else:
        explorer = FixedMixture(arm.M_bounds, arm.S_bounds, d, motor_ratio)

    effects     = []
    diversities = [] # for each timestep, current diversity of motor/goal
    use_goal    = [] # for each timestep, True if goal explorer is used.

    for t in range(T):
        m_command = explorer.explore()
        s_effect  = arm.execute(m_command)
        explorer.add_observation(m_command, s_effect)

        effects.append(s_effect)
        if adapt_on:
            diversities.append(explorer.diversities())
            use_goal.append(explorer.last_explorer == 'goal')

    return {'effects': np.array(effects),
            'diversities': np.array(diversities),
            'use_goal': np.array(use_goal),
            'total_diversity': diversity_score(effects, τ)}


def run(seed, T, dim, limit, adapt_on, d=None,
        motor_ratio=None, α=None, τ=0.02, window=None,
        force_run=False, verbose=True):
    """
    Run the algorithm and save the results. Will opportunistically load
    a previous run if a matching file is found.

    :param force_run:   will not load saved result, recompute instead.
    """
    if adapt_on:
        filepath = 'runs/run_{}_adapt_{}_{}_{}_s{}'.format(d, α, τ, window, seed)
    else:
        filepath = 'runs/run_{}_fixed_{}_s{}'.format(d, motor_ratio, seed)
    os.makedirs('runs', exist_ok=True)

    try:
        with open(filepath + '.pickle', 'rb') as fd:
            data = pickle.load(fd)
        if verbose:
            print('loaded {}'.format(filepath))
        return data
    except (FileNotFoundError, EOFError):
        context = reproducible.Context(repo_path='.', allow_dirty=True)
        try:
            cmd = ['geos-config','--version']
            geos_version = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
        except FileNotFoundError: # geos-config not available
            geos_version = 'could not be retrieved'
        context.add_data('geos_version', geos_version)

        params  = context.function_args()

        results = just_run(seed, T, dim, limit, d, adapt_on,
                           motor_ratio=motor_ratio, τ=τ, α=α, window=window)
        if verbose:
            print('saving {}'.format(filepath))
        data = {'params': params, 'results': results}
        with open(filepath + '.pickle', 'wb') as fd:
            pickle.dump(data, fd)
        context.add_file(filepath + '.pickle', category='output')
        context.export_yaml(filepath + '.context.yaml')
        return data
