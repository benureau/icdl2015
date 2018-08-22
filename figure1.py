import reproducible

from icdl2015 import arm2d, exploration, graphs
from icdl2015 import random2 as random


graphs.output_file('figures/figure1.html')


random.seed(0)

arm = arm2d.RoboticArm(20, 150)
explorer = exploration.RandomMotorExplorer(arm.M_bounds)

postures, effects = [], []
for t in range(5000):
    m_command = explorer.explore()
    s_effect  = arm.execute(m_command)
    effects.append(s_effect)
    postures.append(arm.posture)

x, y = zip(*effects)
fig = graphs.Figure(x_range=(-1, 1), y_range=(-1, 1), height=600, width=600,
                    title='random motor babbling')
fig.circle(x, y, size=2.5, alpha=0.75)
for posture in postures[-5:]:
    fig.display_posture(posture)

graphs.show(fig.fig)

reproducible.add_repo('.')
reproducible.add_file('figures/figure1.html', category='output')
reproducible.export_yaml('figures/figure1.context.yaml')
