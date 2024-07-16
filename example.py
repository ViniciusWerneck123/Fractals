import numpy as np
from functions import *

'''
200 iterations
c = 0.285 + 0.01i
graph limits:
x: {-1.5, 1.5}
y: {-1.5, 1.5}
750x750 matrix of points'''
a, b = -0.71, 0.28
c = complex(a, b)
#z, color = julia(c, clean_plot=True, zoom=1, center_x=None, center_y=None, dpi=100)


z, color = mandelbrot(clean_plot=True, cmap='binary_r', forced_stop=True, stop_step=25, converging_color=None, zoom=1, center_x=None, center_y=None, dpi=100)
