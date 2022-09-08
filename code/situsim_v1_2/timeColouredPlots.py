import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d.art3d import Line3DCollection

# a function to produce a plot where the line colour varies over its length
#   -   i originally wrote this for indicating time by colour, but the colour
#       can actually determined according to any variable
def doColourVaryingPlot2d(x, y, t, fig, ax, map='plasma', showBar=True, barlabel='time'):
    segments = []
    x = np.array(x)
    y = np.array(y)
    t = np.array(t)
    for i in range(y.shape[0] - 1):
        pair = np.array([[x[i], y[i]], [x[i + 1], y[i + 1]]])
        segments.append(pair)
    segments = np.array(segments)

    # Create a continuous norm to map from data points to colors
    norm = plt.Normalize(t.min(), t.max())
    lc = LineCollection(segments, cmap=map, norm=norm)
    # Set the values used for colormapping
    lc.set_array(t)
    lc.set_linewidth(2)
    line = ax.add_collection(lc)
    if showBar:
        col = fig.colorbar(line, ax=ax)
        col.set_label(barlabel)

    ax.set_xlim([np.min(x), np.max(x)])
    ax.set_ylim([np.min(y), np.max(y)])

def doColourVaryingPlot3d(x, y, z, t, fig, ax, map='plasma', showBar=True, barlabel='time'):
    segments = []
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    t = np.array(t)
    for i in range(y.shape[0] - 1):
        trip = np.array([[x[i], y[i], z[i]], [x[i + 1], y[i + 1], z[i+1]]])
        segments.append(trip)
    segments = np.array(segments)

    # Create a continuous norm to map from data points to colors
    norm = plt.Normalize(t.min(), t.max())
    lc = Line3DCollection(segments, cmap=map, norm=norm)
    # Set the values used for colormapping
    lc.set_array(t)
    lc.set_linewidth(2)
    line = ax.add_collection(lc)
    if showBar:
        col = fig.colorbar(line, ax=ax)
        col.set_label(barlabel)

    ax.set_xlim(x.min(), x.max())
    ax.set_ylim(y.min(), y.max())
    ax.set_zlim(z.min(), z.max())
