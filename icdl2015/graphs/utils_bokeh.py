import os
import shutil
import warnings
import subprocess

from bokeh import io
from bokeh import plotting
from bokeh.layouts import row, column, gridplot
from bokeh.io import export_png, export_svgs


try:
    get_ipython() # checking if (it seems) we are in a notebook
    plotting.output_notebook(hide_banner=True)
    JUPYTER = True
except NameError:
    JUPYTER = False
    
def tweak_fig(fig):
    tight_layout(fig)
    disable_minor_ticks(fig)
    disable_grid(fig)
    fig.toolbar.logo = None

def tight_layout(fig):
    fig.min_border_top    = 35
    fig.min_border_bottom = 35
    fig.min_border_right  = 35
    fig.min_border_left   = 35

def disable_minor_ticks(fig):
    #fig.axis.major_label_text_font_size = value('8pt')
    fig.axis.minor_tick_line_color = None
    fig.axis.major_tick_in = 0

def disable_grid(fig):
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = None

def figure(*args, **kwargs):
    fig = plotting.figure(*args, **kwargs)
    tweak_fig(fig)
    transparent_background(fig)
    return fig

def transparent_background(fig):
    fig.background_fill_color = None
    fig.border_fill_color     = None


# saving figure

def save_fig(fig, title, ext='png', verbose=True):
    """Save files as png or pdf"""
    title = title.replace(' ', '_')
    filename = '{}s/{}'.format(ext, title, ext)
    if not os.path.exists(ext + 's'):
        os.mkdir(ext + 's')
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        if ext == 'png':
            export_png(fig, filename=filename+'.png')
        else: # svg or pdf
            fig.output_backend = 'svg'
            export_svgs(fig, filename=filename+'.svg')
            if ext == 'pdf':
                svg2pdf(filename+'.svg')
                #os.remove(filename+'.svg')
    if verbose:
        print('saving {}.{}'.format(filename, ext))

def svg2pdf(filename):
    """Convert a svg into a pdf.

    Use inkscape if available, else relies on `svglib`
    :param filename:  the path to the svg file, i.e. `path/to/file.svg`
    """
    abs_filename = os.path.abspath(os.path.expanduser(filename))
    pdf_filename = os.path.splitext(abs_filename)[0] + '.pdf'

    if shutil.which('inkscape') is not None:
        cmd = 'inkscape "{}" --export-pdf="{}"'.format(abs_filename, pdf_filename)
        subprocess.call(cmd, shell=True)
    else:
        try:
            import svglib
            import reportlab
            rlg_file = svglib.svglib.svg2rlg(abs_filename)
            reportlab.graphics.renderPDF.drawToFile(rlg_file, pdf_filename)
        except ImportError as e:
            print('Inkscape was not detected. Please install it, or svglib '
                  'using `pip install svglib reportlab`')
