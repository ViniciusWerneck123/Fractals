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
a, b = 0.285, 0.01
c = complex(a, b)
fractal(n_iter=100, fractal_type='julia', c=complex(a,b), cmap='viridis', animated=True)
