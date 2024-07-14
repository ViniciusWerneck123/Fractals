import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from itertools import product
from typing import Tuple

DEFAULT_XLIM = [-1.5, 1.5]
DEFAULT_YLIM = [-1.5, 1.5]
MANDELBROT_XLIM = [-2, 0.5]
MANDELBROT_YLIM = [-1.2, 1.2]
N_POINTS = 750
STOP_STEP = 100
CMAP = 'viridis'
INTERIOR_COLOR = [0, 0, 0] # RGB
GRAPH_WIDTH = 9

def fractal(c: complex, xlim: tuple = DEFAULT_XLIM, ylim: tuple = DEFAULT_YLIM, n_points: int = N_POINTS, forced_stop=False, stop_step=STOP_STEP, cmap=CMAP,
            interior_color=INTERIOR_COLOR, clean_plot=True, width=GRAPH_WIDTH) -> Tuple[np.array, np.array, np.array]:
    '''Function that return the points and colors for each point for the fractal.
    Return a tuple of matrices with x and y values of the mandelbrot set.\n                                                                                                                                                     
    xlim: tuple with lower and upper limit for x axes.                                                         
    ylim: tuple with lower and upper limit for y axes.                                                  
    n_points: number of lines and columns in the square grid of points.                                                     
    forced_stop: if the user wants to run the fractal faster but in a incomplete way. Sometimes the fractals take long to calculate, this can be used
    to end the convergence loop before the stop condition.                                                                          
    stop_step: the value of the iteration the user wants to force the calculation to stop.                                                      
    cmap: cmap used for coloring the fractal. Default to viridis.                                                       
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
    i = 1
    while True:
        if forced_stop:
            if stop_step == i:
                break

        z = z**2 + c
        # Update color based on convergence:
        # if point diverge, the value, color = i -> the number of the iteration it took to diverge
        diverging = np.absolute(z) > 2

        # If there is no point diverging, leave the loop
        if np.all(~diverging):
            break

        new_point = color == -1
        z[diverging] = np.nan
        color = np.where(np.logical_and(diverging, new_point), np.zeros(color.shape) + np.log(i), color)
        
        i += 1

    # Index of points that converge until the last iteration
    converging = color == -1

    # Merge colors
    cmap_ = cm.get_cmap(cmap)
    color = cmap_(color/color.max())
    
    # Color of points that converge until last iteration will have a black color
    for i in range(3):
        color[converging, i] = interior_color[i]

    plot_set(z_start, color, clean_plot=clean_plot, width=width)
    return z_start, color



def plot_set(z, color, s=0.5, clean_plot=True, width=GRAPH_WIDTH):
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
        plt.axis('off')

    plt.tight_layout()
    plt.show()

    return f, plt.gca()



def newtonIteration(x, y, a, b):
    '''Newton iteration formula for root calculation
    z = z - P(z)/P'(z)
    where P(z) = z³ - 1'''
    xk = (x**3 - 3*x*y**2) / (3*(x**2 + y**2)**3) + 2/3
    yk = (3*x**2 * y - y**3) / (3*(x**2 + y**2)**3)
    return xk, yk



def MandelbrotSet(xlim: tuple = MANDELBROT_XLIM, ylim: tuple = MANDELBROT_YLIM, n_points: int = N_POINTS, forced_stop = False, stop_step=STOP_STEP, cmap=CMAP,
                  interior_color=INTERIOR_COLOR, clean_plot=True, width=GRAPH_WIDTH):
    '''Generate the points and color of the Mandelbrot set                                                      
    Return the values z of the plane and the colors of each point

    xlim/ylim: limits for the points.                                                       
    n_points: number of points of the n_points x n_points matrix.                                                               
    forced_stop: if the user wants to run the fractal faster but in a incomplete way. Sometimes the fractals take long to calculate, this can be used
    to end the convergence loop before the stop condition.                                                                          
    stop_step: the value of the iteration the user wants to force the calculation to stop.                                                  
    cmap: cmap used for coloring the fractal. Default to viridis.                                                   
    interior_color: color in RGB of points that converge. Default to black'''
    a, b = np.linspace(xlim[0], xlim[1], n_points, dtype=np.float64), np.linspace(ylim[0], ylim[1], n_points, dtype=np.float64)
    
    # Complex grid
    c_start = np.array([complex(i[0], i[1]) for i in product(a, b)])
    
    # Color matrix
    color = np.ones(c_start.shape)*-1

    z = c_start
    c = c_start
    i = 1
    while True:
        if forced_stop:
            if stop_step == i:
                break

        z = z**2 + c
        diverging = np.absolute(z) > 2

        # If there is no point diverging, leave the loop
        if np.all(~diverging):
            break

        new_point = color == -1
        z[diverging] = np.nan
        color = np.where(np.logical_and(diverging, new_point), np.zeros(color.shape) + np.log(i), color)

        i += 1

    # Index of points that converge until the last iteration
    converging = color == -1

    # Merge colors
    cmap = cm.get_cmap(cmap)
    color = cmap(color/color.max())
    
    # Color of points that converge until last iteration
    for i in range(3):
        color[converging, i] = interior_color[i]

    plot_set(c_start, color, clean_plot=clean_plot, width=width)
    return c_start, color       
    

