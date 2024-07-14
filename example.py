import numpy as np
from functions import *

'''
200 iterations
c = 0.285 + 0.01i
graph limits:
x: {-1.5, 1.5}
y: {-1.5, 1.5}
750x750 matrix of points'''
a, b = 0.285, 0.01
c = complex(a, b)
z, color = fractal(c, n_points=750, clean_plot=False, zoom=15, center_x=-0.39, center_y=-0.30)


#z, color = MandelbrotSet(n_points=750, clean_plot=False, zoom=1, center_x=None, center_y=None)
