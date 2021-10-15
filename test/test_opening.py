import pathlib
import sys

from ..matplotlib_viewer import get_figure
import matplotlib.figure

fignames_standard = ['fig.'+end for end in ['bz2', 'gz', 'pkl', 'xz']]
directory = pathlib.Path(__file__).parent


def test_standard():
    for figname in fignames_standard:
        fig = get_figure(directory/figname)
        assert type(fig) == matplotlib.figure.Figure


def test_zstd():
    if 'zstandard' in sys.modules:
        fig = get_figure(directory/'fig.zstd')
        assert type(fig) == matplotlib.figure.Figure