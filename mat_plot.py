import matplotlib
matplotlib.use("Agg")

import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
import numpy as np 

import pylab

def plot_line(frame_num, data,figsize= [4,2.5]):
    fig = pylab.figure(figsize=figsize, # Inches
                   dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                   )
    ax = fig.gca()
    l = list(range(frame_num))
    ax.plot(l, data[0], '-r')
    ax.plot(l, data[1], '-y')
    ax.plot(l, data[2], '-g')
    ax.legend(['Infection', 'Incubation', 'Health'])
    ax.grid(linestyle="--", alpha=0.6)
    canvas = agg.FigureCanvasAgg(fig)
    plt.close()
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    return raw_data, size

def plot_hist(data, data_str=('Dorm', 'Class', 'Canteen', 'Play'), figsize= [4,2.5]):
    fig = pylab.figure(figsize=figsize, # Inches
                   dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                   )
    x = np.arange(len(data))
    ax = fig.gca()
    ax.bar(x, height=data, width=0.5, label="Infection number", tick_label=data_str)
    for a, b in zip(x, data):
        ax.text(a, b + 0.05, '%.0f' %b, ha='center', va='bottom', fontsize=10)
    ax.legend()
    ax.grid(linestyle="--", alpha=0.6)
    canvas = agg.FigureCanvasAgg(fig)
    plt.close()
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    return raw_data, size
