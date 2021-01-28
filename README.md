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
