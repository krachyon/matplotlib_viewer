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

Pressing `+` and `-` will scale the fontsize. The funny ways it will mess up your figure are considered a feature.

## supported formats
`plain, gzip, bz2, lzma` : always

`zstandard`: install [zstandard](https://github.com/indygreg/python-zstandard)

in all cases: save figure like 
```python 
compression_lib.open(filename_base+'.mplf', 'wb')
```