#! /usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib
import pickle
import sys
import glob
import os

def recurse_artists(artist_list):
    ret = []
    for artist in artist_list:
        if isinstance(artist, matplotlib.text.Text):
            ret += [artist]
        else:
            ret += recurse_artists(artist.get_children())
    return ret

def fontscale(key):
    artist_list = []
    fig = plt.gcf()

    all_text = recurse_artists(fig.get_children())
    
    inc = 1.1 if key=='+' else 0.9

    for text in all_text:
        text.set_fontsize(text.get_fontsize()*inc)

    plt.draw()   

def press(event):
    global current_index
    print('press')

    if event.key == 'left':
        current_index -= 1
    elif event.key == 'right':
        current_index += 1
    elif event.key in ['+','-']:
        fontscale(event.key)
        return
    else:
        return

    display(figure_files[current_index % len(figure_files)])


def display(figure_file):
    # TODO this is really brittle and just kills the current figure window to open a new one
    #  with the same geometry. Would be nice to replace the content instead...
    old_fig = plt.gcf()
    geometry = plt.get_current_fig_manager().window.geometry()

    with open(figure_file, 'rb') as f:
        fig = pickle.load(f)

    fig.show()
    plt.get_current_fig_manager().window.setGeometry(geometry)
    fig.canvas.set_window_title(figure_file)
    plt.close(old_fig)
    plt.gcf().canvas.mpl_connect('key_press_event', press)


file_to_open = sys.argv[1]

working_dir = os.path.dirname(file_to_open)
figure_files = sorted(glob.glob(os.path.join(os.path.abspath(working_dir), '*.mplf')))

current_index = figure_files.index(file_to_open)

display(file_to_open)
plt.show()
