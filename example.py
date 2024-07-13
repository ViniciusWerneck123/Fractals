import numpy as np
from functions import *

'''
200 iterations
c = 0.285 + 0.01i
graph limits:
x: {-1.5, 1.5}
y: {-1.5, 1.5}
750x750 matrix of points'''
x, y, color = fractal(150, JuliaSet, 0.285, 0.01, [-1.5, 1.5], [-1.5, 1.5], 750, cmap='viridis_r')
plot_set(x, y, color, s=0.5)


#x, y, color = MandelbrotSet(100, [-1.5, 0.5], [-1.5, 1.5], 500)
#plot_set(x, y, color, aspect_ratio=0.5)
