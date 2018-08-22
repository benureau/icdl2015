import pickle
import multiprocessing

import numpy as np
import tqdm

from icdl2015 import run


## Parameters
# note: not using `np.arange` or `np.linspace` to avoid `0.15000000000000002`
#       in filenames.
motor_ratios = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45,
                0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
ds = [0.001, 0.05, 0.5]
τ = 0.02
T = 10000
dim, limit = 20, 150
repetitions = 25

## Save
diversities_fixed = {d: {mr: repetitions*[np.nan] for mr in motor_ratios} for d in ds}
diversities_adapt = {d: repetitions*[np.nan] for d in ds}
def save():
    """The output of the save function is used by the `python4_graphs.py` script."""
    with open('runs/fig4_diversities.pickle', 'wb') as fd:
        pickle.dump((diversities_fixed, diversities_adapt), fd)

## Runs helpers
def run_fixed(args):
    d, motor_ratio, seed = args
    results = run(seed=seed, T=T, dim=dim, limit=limit, τ=τ, d=d,
                  adapt_on=False, motor_ratio=motor_ratio, verbose=False)['results']
    return d, motor_ratio, results['total_diversity'], seed

def run_adapt(args):
    d, seed = args
    results = run(seed=seed, T=T, dim=dim, limit=limit,
        d=d, adapt_on=True, τ=τ, α=0.1, window=50, verbose=False)['results']
    return d, results['total_diversity'], seed

## Create job args
fixed_runs, adapt_runs = [], []
for i in range(repetitions):
    for d in ds:
        for motor_ratio in motor_ratios:
            fixed_runs.append((d, motor_ratio, i))
        adapt_runs.append((d, i))

## Run with multiple workers
if __name__ == '__main__':
    pool = multiprocessing.Pool()
    for d, mr, diversity, i in tqdm.tqdm(pool.imap(run_fixed, fixed_runs),
                                         total=len(fixed_runs)):
        diversities_fixed[d][mr][i] = diversity
        save()
    for d, diversity, i in tqdm.tqdm(pool.imap(run_adapt, adapt_runs),
                                     total=len(adapt_runs)):
        diversities_adapt[d][i] = diversity
        save()
