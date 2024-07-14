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
z, color = fractal(c, n_points=1000, clean_plot=False)


#z, color = MandelbrotSet(n_points=750, clean_plot=False)
