import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from typing import Tuple

'''Here is the file for all the functions necessary to create the image of a fractal.

fractal: main call function that receives the fractal law function and parameters for the graph limits and numeric calculation.

plot_set: main function to plot the fractal. Only needs the real and complex matrix of points as well as the color for each point.

MandelbrotSet: function that generates the Mandelbrot set. Similar to fractal function but the way to collect the points is different.

JuliaSet: an existing function that holds for creation of Julia sets. It uses the grid values of real and complex parts of the plane
and the real and complex values of the constant c.'''


def fractal(n: int, func, a: float, b: float, xlim: tuple, ylim: tuple, n_points: int, cmap='viridis') -> Tuple[np.array, np.array, np.array]:
    '''Return a tuple of matrices with x and y values of the mandelbrot set.\n
    n: number of iterations.\n
    func: the sequence law. This function should have 4 parameters in this order:
    x (real values), y (complex values), a (real constant part), b (complex constant part).
    The func also should return the new values of x and y.\n
    a: real part of added constant in the sequence\n
    b: complex part of added constant in the sequence.'''
    x, y = np.linspace(xlim[0], xlim[1], n_points, dtype=np.float64), np.linspace(ylim[0], ylim[1], n_points, dtype=np.float64)
    # matrices with real and complex part of z
    x_start, y_start = np.meshgrid(x, y)
    x, y = x_start, y_start

    # Color of the converging points
    color = x * 0
    for i in range(1, n + 1):
        x, y = func(x, y, a, b)
        # Update color based on convergence:
        # if point diverge, the value, color = i -> the number of the iteration it took to diverge
        diverging = np.sqrt(x**2 + y**2) > 2
        new_point = color == 0
        x[diverging] = np.nan
        y[diverging] = np.nan
        color = np.where(np.logical_and(diverging, new_point), np.zeros(color.shape) + i, color)
    
    # Flatten the color array for better utilization
    color = color.flatten()
    # Index of points that converge until the last iteration
    converging = color == 0

    # Merge colors
    cmap = cm.get_cmap(cmap)
    color = cmap(color/color.max())
    
    # Color of points that converge until last iteration will have a black color
    for i in range(3):
        color[converging, i] = 0
    
    return x_start, y_start, color



def plot_set(x, y, color, s=0.5, clean_plot=True, width=9):
    # Calculate aspect ratio based on the limits of the axes
    dx = x.max() - x.min()
    dy = y.max() - y.min()
    aspect_ratio = dx/dy

    f = plt.figure(figsize=(width, width/aspect_ratio))

    plt.scatter(x, y, s=s, c=color)

    # Leave the plot only with a black edge
    if clean_plot:
        plt.tick_params(labelbottom=False, bottom=False, labelleft=False, left=False)

    plt.show()

    return f, plt.gca()



def JuliaSet(x, y, a, b):
    '''Sequence: z(k) = z(k-1)^2 + c
    Where c = a + bi
    and z = x + yi'''
    xk = x**2 - y**2 + a
    yk = 2*x*y + b
    return xk, yk



def MandelbrotSet(n: int, xlim: tuple, ylim: tuple, n_points: int, cmap='viridis'):
    '''
    n: number of iterations.\n
    xlim/ylim: limits for the points.\n
    n_points: number of points of the n_points x n_points matrix.'''

    a, b = np.linspace(xlim[0], xlim[1], n_points, dtype=np.float64), np.linspace(ylim[0], ylim[1], n_points, dtype=np.float64)
    a, b = np.meshgrid(a, b)
    
    # Color matrix
    color = a * 0

    x, y = a, b
    for i in range(1, n+1):
        xk = x**2 - y**2 + a
        yk = 2*x*y + b
        diverging = np.sqrt(xk**2 + yk**2) > 2
        new_point = color == 0
        xk[diverging] = np.nan
        yk[diverging] = np.nan
        color = np.where(np.logical_and(diverging, new_point), np.zeros(color.shape) + i, color)
        x, y = xk, yk

    # Flatten the color array for better utilization
    color = color.flatten()
    # Index of points that converge until the last iteration
    converging = color == 0

    # Merge colors
    cmap = cm.get_cmap(cmap)
    color = cmap(color/color.max())
    
    # Color of points that converge until last iteration will have a black color
    for i in range(3):
        color[converging, i] = 0

    return a, b, color       
    
