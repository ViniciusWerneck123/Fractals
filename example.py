import numpy as np
from functions import *

'''
200 iterations
−0.835 − 0.2321
c = 0.285 + 0.01i
graph limits:
x: {-1.5, 1.5}
y: {-1.5, 1.5}
750x750 matrix of points'''
a, b = -0.835, -0.2321
c = complex(a, b)
#julia(c, clean_plot=True, stop_iteration=None, zoom=1, center_x=None, center_y=None, dpi=200)


mandelbrot(clean_plot=True, cmap='binary_r', stop_iteration=100, converging_color=[1, 1, 1], zoom=1, center_x=None, center_y=None, dpi=200)
