import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from itertools import product
from typing import Tuple


def fractal(n: int, c: complex, xlim: tuple, ylim: tuple, n_points: int, cmap='viridis', interior_color=[0, 0, 0]) -> Tuple[np.array, np.array, np.array]:
    '''Function that return the points and colors for each point for the fractal.
    Return a tuple of matrices with x and y values of the mandelbrot set.\n
    n: number of iterations.                                                                                                                                                       
    xlim: tuple with lower and upper limit for x axes.                                                         
    ylim: tuple with lower and upper limit for y axes.                                                  
    n_points: number of lines and columns in the square grid of points.
    cmap: cmap used for coloring the fractal. Default to viridis
    interior_color: color in RGB of points that converge. Default to black'''
    # Grid of points
    x, y = np.linspace(xlim[0], xlim[1], n_points, dtype=np.float64), np.linspace(ylim[0], ylim[1], n_points, dtype=np.float64)
    values = product(x, y)

    del x, y

    # Complex grid
    z_start = np.array([complex(i[0], i[1]) for i in values])

    # Color of the converging points
    color = np.ones(z_start.shape)*-1
    z = z_start
    for i in range(1, n + 1):
        z = z**2 + c
        # Update color based on convergence:
        # if point diverge, the value, color = i -> the number of the iteration it took to diverge
        diverging = np.absolute(z) > 2
        new_point = color == -1
        z[diverging] = np.nan
        color = np.where(np.logical_and(diverging, new_point), np.zeros(color.shape) + np.log(i), color)

    # Index of points that converge until the last iteration
    converging = color == -1

    # Merge colors
    cmap_ = cm.get_cmap(cmap)
    color = cmap_(color/color.max())
    
    # Color of points that converge until last iteration will have a black color
    for i in range(3):
        color[converging, i] = interior_color[i]

    return z_start, color



def plot_set(z, color, s=0.5, clean_plot=True, width=9):
    x = np.real(z)
    y = np.imag(z)

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



def newtonIteration(x, y, a, b):
    '''Newton iteration formula for root calculation
    z = z - P(z)/P'(z)
    where P(z) = z³ - 1'''
    xk = (x**3 - 3*x*y**2) / (3*(x**2 + y**2)**3) + 2/3
    yk = (3*x**2 * y - y**3) / (3*(x**2 + y**2)**3)
    return xk, yk



def MandelbrotSet(n: int, xlim: tuple, ylim: tuple, n_points: int, cmap='viridis'):
    '''
    n: number of iterations.\n
    xlim/ylim: limits for the points.\n
    n_points: number of points of the n_points x n_points matrix.'''
    a, b = np.linspace(xlim[0], xlim[1], n_points, dtype=np.float64), np.linspace(ylim[0], ylim[1], n_points, dtype=np.float64)
    
    # Complex grid
    c_start = np.array([complex(i[0], i[1]) for i in product(a, b)])
    
    # Color matrix
    color = np.zeros(c_start.shape)

    z = c_start
    c = c_start
    for i in range(1, n+1):
        z = z**2 + c
        diverging = np.absolute(z) > 2
        new_point = color == 0
        z[diverging] = np.nan
        color = np.where(np.logical_and(diverging, new_point), np.zeros(color.shape) + i, color)

    # Index of points that converge until the last iteration
    converging = color == 0

    # Merge colors
    cmap = cm.get_cmap(cmap)
    color = cmap(color/color.max())
    
    # Color of points that converge until last iteration will have a black color
    for i in range(3):
        color[converging, i] = 0

    return c_start, color       
    

