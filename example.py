import numpy as np
from functions import *

'''
200 iterations
c = 0.285 + 0.01i
graph limits:
x: {-1.5, 1.5}
y: {-1.5, 1.5}
750x750 matrix of points'''
a, b = -0.64, 0
c = complex(a, b)
z, color = fractal(c, [-1.5, 1.5], [-1.5, 1.5], 750, cmap='viridis')


z, color = MandelbrotSet([-2.2, 0.8], [-1.2, 1.2], 500)
