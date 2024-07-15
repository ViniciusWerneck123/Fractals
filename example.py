import numpy as np
from functions import *

'''
200 iterations
c = 0.285 + 0.01i
graph limits:
x: {-1.5, 1.5}
y: {-1.5, 1.5}
750x750 matrix of points'''
a, b = -0.17, 0.8
c = complex(a, b)
z, color = juliaSet(c, n_points=750, clean_plot=False, zoom=1, center_x=None, center_y=None)


#z, color = mandelbrotSet(n_points=750, clean_plot=False, cmap='viridis', interior_color=[0, 0, 0], zoom=1, center_x=None, center_y=None)
