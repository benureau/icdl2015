import reproducible

from icdl2015 import arm2d, exploration, graphs
from icdl2015 import random2 as random


graphs.output_file('figures/figure2.html')
figs = []

for d in [0.001, 0.05, 0.5]:
    random.seed(0)
    arm = arm2d.RoboticArm(20, 150)
    explorer_motor = exploration.RandomMotorExplorer(arm.M_bounds)
    explorer_goal = exploration.RandomGoalExplorer(arm.M_bounds, arm.S_bounds, d)

    postures, effects = [], []
    for t in range(5000):
        random.uniform(0, 1) # keeping random draw as original code.
        explorer = explorer_motor if t < 10 else explorer_goal
        m_command = explorer.explore()
        s_effect  = arm.execute(m_command)
        explorer_goal.add_observation(m_command, s_effect)

        effects.append(s_effect)
        postures.append(arm.posture)

    x, y = zip(*effects)
    fig = graphs.Figure(x_range=(-1, 1), y_range=(-1, 1), height=600, width=600,
                        title='random motor babbling')
    fig.circle(x, y, size=2.5, alpha=0.75)

    for posture in postures[-5:]:
        fig.display_posture(posture)

    figs.append(fig.fig)

graphs.show(graphs.column(figs))

reproducible.add_repo('.')
reproducible.add_file('figures/figure2.html', category='output')
reproducible.export_yaml('figures/figure2.context.yaml')
