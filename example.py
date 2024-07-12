import numpy as np
from functions import *

'''
200 iterations
c = -0.4 + 0.6i
graph limits:
x: {-1.5, 1.5}
y: {-1.5, 1.5}
500x500 matrix of points'''
x, y, color = fractal(200, JuliaSet, -0.4, 0.6, [-1.5, 1.5], [-1.5, 1.5], 500)
plot_set(x, y, color)


x, y, color = MandelbrotSet(100, [-1.5, 0.5], [-1.5, 1.5], 500)
plot_set(x, y, color, aspect_ratio=0.5)
