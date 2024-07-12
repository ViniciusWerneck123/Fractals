import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from typing import Tuple

def fractal(n: int, func, a: float, b: float, xlim: tuple, ylim: tuple, n_points: int) -> Tuple[np.array, np.array, np.array]:
    '''Return a tuple of matrices with x and y values of the mandelbrot set.\n
    n: number of iterations.\n
    func: the sequence law. This function should have 4 parameters in this order:
    x (real values), y (complex values), a (real constant part), b (complex constant part).
    The func also should return the new values of x and y.\n
    a: real part of added constant in the sequence\n
    b: complex part of added constant in the sequence.'''
    x, y = np.linspace(xlim[0], xlim[1], n_points), np.linspace(ylim[0], ylim[1], n_points)
    # matrices with real and complex part of z
    x_start, y_start = np.meshgrid(x, y)
    x, y = x_start, y_start

    # Color of the converging points
    color = x * 0
    for i in range(n):
        x, y = func(x, y, a, b)
        # Update color based on convergence
        condition = np.sqrt(x**2 + y**2) > 2
        color[condition] += i
    
    color = (color/n).flatten()
    
    return x_start, y_start, color


def JuliaSet(x, y, a, b):
    '''Sequence: z(k) = z(k-1)^2 + c
    Where c = a + bi
    and z = x + yi'''
    xk = x**2 - y**2 + a
    yk = 2*x*y + b
    return xk, yk


def plot_set(x, y, color, cmap='viridis', s=0.5, clean_plot=True, aspect_ratio=1):
    f = plt.figure(figsize=(9, 9/aspect_ratio))
    plt.scatter(x, y, s=s, c=color, cmap=cmap)
    if clean_plot:
        plt.tick_params(labelbottom=False, bottom=False, labelleft=False, left=False)
    plt.show()
    return f, plt.gca()


def MandelbrotSet(n: int, xlim: tuple, ylim: tuple, n_points: int):
    '''
    n: number of iterations.\n
    xlim/ylim: limits for the points.\n
    n_points: number of points of the n_points x n_points matrix.'''

    a, b = np.linspace(xlim[0], xlim[1], n_points), np.linspace(ylim[0], ylim[1], n_points)
    a, b = np.meshgrid(a, b)
    
    # Color matrix
    color = a * 0

    x, y = a, b
    for i in range(n):
        xk = x**2 - y**2 + a
        yk = 2*x*y + b
        x, y = xk, yk
        color[np.sqrt(x**2 + y**2) > 2] += i

    return a, b, color        
    
