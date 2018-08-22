import numpy as np
import reproducible

from icdl2015 import run, graphs


graphs.output_file('figures/figure3.html')
color_motor, color_goal = '#2577b2', '#e84a5f'

def means(v, window):
    ms = []
    for t in range(len(v)):
        t_min = max(     0, t - window//2)
        t_max = min(len(v), t + window//2)
        ms.append(np.mean(v[t_min:t_max]))
    return ms

figs = []
for d in [0.001, 0.05, 0.5]:
    results = run(seed=0, T=5000, dim=20, limit=150,
                                        d=d, adapt_on=True,
                                        τ=0.02, α=0.1, window=50)['results']

    x, y = zip(*results['effects'])
    fig = graphs.Figure(x_range=(-1, 1), y_range=(-1, 1), height=600, width=600,
                        title='d = {}'.format(d))
    fig.coverage(results['effects'], 0.02)
    fig.circle(x, y, size=2.5, alpha=0.75)
    figs.append(fig.fig)

    fig = graphs.Figure(y_range=(0, 1.3), height=250, width=900,
                        title='diversity'.format(d))
    y_motor, y_goal = zip(*results['diversities'])
    y_motor, y_goal = 1000*np.array(y_motor), 1000*np.array(y_goal)
    fig.line(range(len(y_motor)), y_motor, color=color_motor)
    fig.line(range(len(y_goal)), y_goal, color=color_goal)
    figs.append(fig.fig)

    fig = graphs.Figure(y_range=(0, 1), height=250, width=900,
                        title='usage'.format(d))
    goals  = 1.0 * results['use_goal']
    motors = 1.0 - results['use_goal']
    fig.line(range(len(motors)), means(motors, 100), color=color_motor)
    fig.line(range(len( goals)), means( goals, 100), color=color_goal)
    figs.append(fig.fig)


graphs.show(graphs.column(figs))

reproducible.add_repo('.')
reproducible.add_file('figures/figure3.html', category='output')
reproducible.export_yaml('figures/figure3.context.yaml')
