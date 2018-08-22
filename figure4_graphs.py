import pickle

import numpy as np
import reproducible

from icdl2015 import graphs


graphs.output_file('figures/figure4.html')
color_motor, color_goal = '#2577b2', '#e84a5f'

with open('runs/fig4_diversities.pickle', 'rb') as fd:
    diversities_fixed, diversities_adapt = pickle.load(fd)

print(diversities_adapt)

div_meanstd = []
figs = []

y_ranges = [(0, 1.2), (0.5, 3), (0.9, 1.3)]
for d, y_range in zip([0.001, 0.05, 0.5], y_ranges):
    x = sorted(diversities_fixed[d].keys())
    y_fixed_mean = [np.nanmean(diversities_fixed[d][x_i]) for x_i in x]
    y_fixed_std  = [np.nanstd(diversities_fixed[d][x_i]) for x_i in x]
    y_adapt_mean = np.nanmean(diversities_adapt[d])
    y_adapt_std  = np.nanstd(diversities_adapt[d])

    fig = graphs.Figure(y_range=y_range, height=250, width=900,
                        title='d = {}'.format(d))
    # fixed
    fig.line(x, y_fixed_mean, color=color_motor)
    fig.circle(x, y_fixed_mean, color=color_motor, swap_xy=False)
    for x_i, y_mean_i, y_std_i in zip(x, y_fixed_mean, y_fixed_std):
        fig.rect([x_i-0.002, x_i+0.002], [y_mean_i - y_std_i, y_mean_i + y_std_i],
                 color=color_motor, alpha=0.25)

    # adapt
    fig.line([0, 1], [y_adapt_mean, y_adapt_mean], color=color_goal,
             line_width=1, line_dash=[3, 3], line_cap='round')
    fig.rect([0, 1], [y_adapt_mean - y_adapt_std, y_adapt_mean + y_adapt_std],
             color=color_goal, alpha=0.15)
    figs.append(fig.fig)

graphs.show(graphs.column(figs))

reproducible.add_repo('.')
reproducible.add_file('figures/figure4.html', category='output')
reproducible.export_yaml('figures/figure4.context.yaml')
