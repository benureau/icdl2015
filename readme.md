# Code for "Diversity-Driven Selection of Exploration Strategies in Multi-Armed Bandits"

This repository hosts the code for producing the figures of the following
paper, written by [Fabien C. Y. Benureau](https://fabien.benureau.com) and
[Pierre-Yves Oudeyer](http://www.pyoudeyer.com/):

Benureau, Oudeyer, "Diversity-Driven Selection of Exploration Strategies in
Multi-Armed Bandits" *ICDL-Epirob conference*, Providence, RI, USA, 2015.
https://doi.org/10.1109/devlrn.2015.7346130

The pdf is [available here](https://fabien.benureau.com/docs/icdl2015.pdf).

Precomputed figures can be found in the `figures_ref/` folder, if you don't wish
to rerun the code. Because randomness is controlled by seeds, you should obtain
the exact same figures, baring a change of behavior of one of the software or
hardware component.

This code tries to abide to the five Rs: [re-runnable, repeatable, reproducible,
reusable and replicable](https://doi.org/10.3389/fninf.2017.00069).

## Not the original code

The original code was integrated in a complex framework coded in Python 2, that
was difficult to install and run. This code was rewritten from scratch. Extra
care was made to reproduce the figures exactly, by recreating the random draw of
the original code. This meant using Python 2's random module in Python 3
(copying the `random` code from CPython 2), and adding a few extraneous calls to
random functions where the previous framework code did.

This code is simpler and faster. Figure 1, 2 and 3 are reproduced exactly.
The Figure 4 could not be reproduced exactly (the most probable explanation is
a difference of random seeds with the original code), although it remains
qualitatively identical.

This code is licensed under the
[Open Science License](http://fabien.benureau.com/openscience).


## Install

The `requirements.txt` file list the necessary packages. And additional,
`requirements_strict.txt` file—created with the `requirements_strict.py` script—
lists the specific version of each package that was installed when the
results and figures were computed. Furthermore Each produced result file or figure
is accompanied by a `*.context.yaml` file produced using the `reproducible`
library. This file details the Python version and OS version used to produce the
results, as well as the git hash commit of the code and the packages installed
and their version (the same information as `requirement_strict.txt`. This may
help you to recreate the original execution environment in a virtual machine,
even 10 or 20 years from now.

To install the required dependencies, either one of:
```bash
pip install -r requirements.txt
pip install -r requirements_strict.txt
```


## Run and Plot

To produce figure 1, 2 and 3, simply run:
```bash
python figure1.py
python figure2.py
python figure3.py
```
The figures should open in a web browser. They can also be found in the
`figures/` folder. Reference figures can be found in the `figures_ref/` folder.

Producing figure 4 takes a few hours (~2hours at 500GFLOPS). You should run:
```bash
python figure4_runs.py
python figure4_graphs.py
```


## Contact

This code is mainly an archive for the corresponding article, and no further
development is planned. However, do not hesitate to open of an issue or contact
me if you have a question or a problem. My contact on my website:
[fabien.benureau.com](https://fabien.benureau.com)
