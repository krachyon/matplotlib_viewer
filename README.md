# matplotlib_viewer
View matplotlib pickle files

# Usage:

Save a matplotlib figure with something like this:

```python
with open(filename_base+'.mplf', 'wb') as outfile:
    pickle.dump(figure, outfile)
```

Put matplotlib_viewer.py somewhere in your path and configure your system to open `.mplf`-files with it.
Clicking on a mplf file should load and display it

You can use the left and right arrow keys to navigate between figures in the directory the original figure was in.
This probably only works with QT backend...

## fontsize
Pressing `+` and `-` will scale the fontsize. The funny ways it will mess up your figure are considered a feature.

## colors
only works on images for now.

- presing `1`-`5` will give you boring built-in colormaps
- pressing `6` will give you a random one
- pressing `x` (for 'Xtreme') will spice up the current colormap by doubling it; [1] 
- pressing `v` (for 'bvring) will despice the current colormap by halving it;
- pressing `c` (for 'order') will extent the colormap with a random one
- pressing `r` (for 'predictable') will shuffle the colormap

[1] ~~Holding down this key is a fun way to learn about exponential growth and a nice workout for your system~~ actually the new behaviour of re-interpolating the colormap just creates some weird temporal Moiré pattern 

# supported formats
`plain, gzip, bz2, lzma` : always

`zstandard`: install [zstandard](https://github.com/indygreg/python-zstandard)

in all cases: save figure like 
```python 
compression_lib.open(filename_base+'.mplf', 'wb') as f:
    pickle.dump(plt.gcf(), f)
```