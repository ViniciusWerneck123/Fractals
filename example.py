import numpy as np
from functions import *

'''
200 iterations
c = 0.285 + 0.01i
graph limits:
x: {-1.5, 1.5}
y: {-1.5, 1.5}
750x750 matrix of points'''
a, b = -0.8, 0.156
c = complex(a, b)
#z, color = julia(c, clean_plot=True, zoom=1, center_x=None, center_y=None, dpi=100, converging_color=[1, 1, 1])


z, color = mandelbrot(clean_plot=True, cmap='binary_r', forced_stop=False, stop_step=50, converging_color=[1, 1, 1], zoom=1, center_x=None, center_y=None, dpi=100)
