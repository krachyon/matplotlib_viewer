#! /usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib
import pickle
import sys
import glob
import os
import random
import numpy as np

import gzip
import bz2
import lzma
open_funcs = [open, gzip.open, bz2.open, lzma.open]
exceptions = [pickle.UnpicklingError, gzip.BadGzipFile, OSError, lzma.LZMAError]
try:
    import zstandard
    open_funcs.append(zstandard.open)
    exceptions.append(zstandard.ZstdError)
except ImportError:
    pass


def get_figure(fname):
    for f, ex in zip(open_funcs,exceptions):
        try:
            with f(fname, 'rb') as infile:
                fig = pickle.load(infile)
                return fig
        except ex:
            pass


def recurse_artists(artist_list, type):
    ret = []
    for artist in artist_list:
        if isinstance(artist, type):
            ret += [artist]
        else:
            ret += recurse_artists(artist.get_children(), type)
    return ret


def fontscale(key):
    artist_list = []
    fig = plt.gcf()

    all_text = recurse_artists(fig.get_children(), matplotlib.text.Text)
    
    inc = 1.1 if key=='+' else 0.9

    for text in all_text:
        text.set_fontsize(text.get_fontsize()*inc)

    plt.draw()

all_cmaps = [ cmap for i in dir(matplotlib.cm) if issubclass(type(cmap := getattr(matplotlib.cm, i)), matplotlib.colors.Colormap)]

def change_colormap(key):
    """TODO: Deduplicate x,v,c; transform all colormaps to ListedColormap immediately"""
    fig = plt.gcf()
    all_images = recurse_artists(fig.get_children(), matplotlib.image.AxesImage)
    all_colorbars = [cbar for img in all_images if (cbar:=img.colorbar) is not None]
    print(all_colorbars)
    if key == 'x':
        cmap = all_images[0].get_cmap()
        cmap = matplotlib.colors.ListedColormap(cmap.colors*2)
    elif key == 'v':
        cmap = all_images[0].get_cmap()
        cmap = matplotlib.colors.ListedColormap(cmap.colors[:int(len(cmap.colors)/2)])
    elif key == 'c':
        cmap = all_images[0].get_cmap()
        random_cmap = random.choice(all_cmaps)
        if hasattr(random_cmap, 'colors'):
            addition = list(random_cmap.colors)
        else:
            addition = list(random_cmap(np.linspace(0,1,75))[:,:3])
        cmap = matplotlib.colors.ListedColormap(cmap.colors + addition)
    elif key == 'r':
        cmap = all_images[0].get_cmap().copy()
        colors = cmap.colors.copy()
        np.random.shuffle(colors)
        cmap = matplotlib.colors.ListedColormap(colors)
    elif key == '6':
        cmap = random.choice(all_cmaps).copy()
    else:
        cmap = matplotlib.cm.get_cmap({
            '1': 'viridis',
            '2': 'plasma',
            '3': 'jet',
            '4': 'gnuplot',
            '5': 'prism'}[key]).copy()

    for image in all_images:
        image.set_cmap(cmap)
    for cbar in all_colorbars:
        cbar.cmap = cmap
        # just take the last image, lol.
        cbar.update_normal(image)
    plt.draw()

def press(event):
    global current_index
    print(f'press {event.key}')

    if event.key == 'left':
        current_index -= 1
    elif event.key == 'right':
        current_index += 1
    elif event.key in ['+','-']:
        fontscale(event.key)
        return
    elif event.key in ['1','2','3','4','5','6', 'x', 'v', 'c', 'r']:
        change_colormap(event.key)
        return
    else:
        return

    display(figure_files[current_index % len(figure_files)])


def display(figure_filename):
    # TODO this is really brittle and just kills the current figure window to open a new one
    #  with the same geometry. Would be nice to replace the content instead...
    old_fig = plt.gcf()
    geometry = plt.get_current_fig_manager().window.geometry()

    fig = get_figure(figure_filename)

    fig.show()
    plt.get_current_fig_manager().window.setGeometry(geometry)
    fig.canvas.set_window_title(figure_filename)
    plt.close(old_fig)
    plt.gcf().canvas.mpl_connect('key_press_event', press)


if __name__ == '__main__':
    file_to_open = os.path.abspath(sys.argv[1])

    working_dir = os.path.dirname(file_to_open)
    print(working_dir)
    figure_files = sorted(glob.glob(os.path.join(os.path.abspath(working_dir), '*.mplf')))

    current_index = figure_files.index(os.path.abspath(file_to_open))

    display(file_to_open)
    plt.show()
