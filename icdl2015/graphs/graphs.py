"""Graph class and code for bokeh graphs"""

import os
import struct
import binascii
import shapely.ops
import warnings

import numpy as np

import bokeh
import bokeh.plotting as bpl
import bokeh.io as bio
from bokeh.models import FixedTicker, FuncTickFormatter
from bokeh.models import LinearColorMapper, BasicTicker, ColorBar, Label
from bokeh.models import HoverTool

from . import utils_bokeh as ubkh



SIZE = 500
TOOLS = ()

def rgb2hex(rgb):
    return '#{0:02x}{1:02x}{2:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def hex2rgb(hexstr):
    return struct.unpack('BBB', binascii.unhexlify(hexstr[1:]))
#    return struct.unpack('BBB', binascii.unhexlify(hexstr[1:]))

def rgba2rgb(rgb, rgba):
    r,g,b,a = rgba
    return ((1-a)*rgb[0] + a * r,
            (1-a)*rgb[1] + a * g,
            (1-a)*rgb[2] + a * b)

def hexa(hex, alpha):
    rgb = hex2rgb(hex)
    return rgb2hex(rgba2rgb((255, 255, 255), rgb+(alpha,)))

C_COLOR   = rgb2hex((21, 152, 71))

class Figure:

    def __init__(self, x_range=None, y_range=None, title='', height=SIZE, width=SIZE,
                       tools=TOOLS):
        self.fig = ubkh.figure(title=title, plot_width=width, plot_height=height,
                               x_range=x_range, y_range=y_range,
                               tools=[])

    def set_x_ticks(self, fig, ticks=None):
        if ticks is None:
            ticks=(-500, 0, 500, 1000)
        fig.xaxis[0].ticker = FixedTicker(ticks=ticks)

    def set_y_ticks(self, fig, ticks=None):
        if ticks is not None: # no default value
            fig.yaxis[0].ticker = FixedTicker(ticks=ticks)

    def save(self, fig, title, ext='pdf'):
        full_title = '{}{}'.format(title, self.model_desc)
        ubkh.save_fig(fig, full_title, ext=ext, verbose=True)

    def line(self, x, y, alpha=0.5, color='black', **kwargs):
        """Just a line"""
        line = self.fig.line(x=x, y=y,
                             alpha=alpha, color=color, **kwargs)

    def rect(self, x, y, color='blue', alpha=0.5):
        """Just a line"""
        self.fig.quad(top=[y[1]], bottom=[y[0]], left=[x[0]], right=[x[1]],
                      color=color, alpha=alpha, line_color=None)

    def circle(self, x, y, alpha=0.5, label=None, swap_xy=True, **kwargs):
        """Just a line"""
        if swap_xy:
            x, y = y, x
        line = self.fig.circle(x=x, y=y, alpha=alpha,
                               line_color=None, **kwargs)

    def coverage(self, effects, τ, color=C_COLOR):
        ys, xs = zip(*effects)
        self.fig.circle(xs, ys, radius=τ, fill_color=hexa(color, 0.35),
                                        line_color=None)

        union = shapely.ops.unary_union([shapely.geometry.Point(x, y).buffer(τ)
                                         for x, y in zip(xs, ys)])
        boundary = union.boundary
        if isinstance(boundary, shapely.geometry.LineString):
            boundary = [boundary]

        for b in boundary:
            x, y = b.xy
            x, y = list(x), list(y)
            self.fig.patch(x, y, fill_color=None, line_color=hexa(color, 0.75))

    def display_posture(self, posture, alpha=0.75):
        xs, ys = zip(*posture)

        self.fig.line(xs, ys, line_width=1.0,               color='#666666', alpha=alpha)
        self.fig.circle(xs[  : 1], ys[  : 1], radius=0.015, color='#666666', alpha=alpha)
        self.fig.circle(xs[ 1:-1], ys[ 1:-1], radius=0.008, color='#666666', alpha=alpha)
        self.fig.circle(xs[-1:  ], ys[-1:  ], radius=0.01,  color='red',     alpha=alpha)

    def show(self):
        bpl.show(self.fig)
