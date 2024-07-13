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
#z, color = fractal(100, c, [-1.5, 1.5], [-1.5, 1.5], 750, cmap='viridis')
#plot_set(z, color, s=0.5)


z, color = MandelbrotSet(25, [-2.2, 0.8], [-1.2, 1.2], 500)
plot_set(z, color)
