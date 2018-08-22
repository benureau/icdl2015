from .graphs import Figure

from bokeh import plotting as _plotting
from bokeh import io as _io
from bokeh import layouts as _layouts
output_file = _plotting.output_file
show = _io.show
column = _layouts.column


# remove LAPACK/scipy harmless warning (see https://github.com/scipy/scipy/issues/5998)
import warnings
warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")
