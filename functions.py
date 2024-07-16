import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from itertools import product
from typing import Tuple

DEFAULT_XLIM = [-1.5, 1.5]
DEFAULT_YLIM = [-1.5, 1.5]
MANDELBROT_XLIM = [-2, 0.5]
MANDELBROT_YLIM = [-1.2, 1.2]
STOP_STEP = 100
CMAP = 'viridis'
INTERIOR_COLOR = None # [r, g, b]
GRAPH_WIDTH = 9
MINIMUM_ITERATIONS = 25

def julia(c: complex, forced_stop=False, stop_step=STOP_STEP, cmap=CMAP,
            converging_color=INTERIOR_COLOR, clean_plot=True, width=GRAPH_WIDTH, dpi=100,
            zoom=1, center_x=None, center_y=None) -> Tuple[np.array, np.array, np.array]:
    '''Function that return the points and colors for each point for the fractal.
    Return a tuple of matrices with x and y values of the mandelbrot set.\n                                                  
    c: the complex constant value of the sequence.                                               
    forced_stop: if the user wants to run the fractal faster but in a incomplete way. Sometimes the fractals take long to calculate, this can be used
    to end the convergence loop before the stop condition.                                                                          
    stop_step: the value of the iteration the user wants to force the calculation to stop.                                                      
    cmap: cmap used for coloring the fractal. Default to viridis.                                                       
    converging_color: [r, g, b] - list color in RGB of points that converge. Default to last color in cmap                                                              
    clean_plot: if the image is displayed without the axis labels. Default True                                                                 
    width: width of the figure                                                                              
    dpi: dots per inches of figure
    zoom: the amount of zoom                                                                        
    center_x: x coordinate of the center point of the figure                                                        
    center_y: y coordinate of the center point of the figure'''
    check_dpi(width, dpi)

    # Values of displacement in x and y of the limits of the axes to ensure the new center is in the middle of figure
    dx = center_displacement(DEFAULT_XLIM, center_x, zoom)
    dy = center_displacement(DEFAULT_YLIM, center_y, zoom)

    # Grid of points
    x = np.linspace(DEFAULT_XLIM[0]/zoom + dx, DEFAULT_XLIM[1]/zoom + dx, width*dpi, dtype=np.float64)
    y = np.linspace(DEFAULT_YLIM[0]/zoom + dy, DEFAULT_YLIM[1]/zoom + dy, width*dpi, dtype=np.float64)
    values = product(x, y)

    del x, y

    # Complex grid
    z_start = np.array([complex(i[0], i[1]) for i in values])

    # Color of the converging points
    color = np.ones(z_start.shape)*-1
    z = z_start
    i = 1
    while True:
        z = z**2 + c
        # Update color based on convergence:
        # if point diverge, the value, color = i -> the number of the iteration it took to diverge
        diverging = np.absolute(z) > 2

        if forced_stop:
            if stop_step == i:
                break
        else:
            # If there is no point diverging, leave the loop
            if np.all(~diverging) and i > MINIMUM_ITERATIONS * zoom:
                break

        new_point = color == -1
        z[diverging] = np.nan
        color = np.where(np.logical_and(diverging, new_point), np.zeros(color.shape) + i, color)
        
        i += 1

    del diverging, new_point

    color = color_points(color, cmap, converging_color)
    plot_set(z_start, color, clean_plot=clean_plot, width=width)

    return z_start, color




def mandelbrot(forced_stop = False, stop_step=STOP_STEP, cmap=CMAP,
                converging_color=INTERIOR_COLOR, clean_plot=True, width=GRAPH_WIDTH, dpi=100,
                zoom=1, center_x=None, center_y=None):
    '''Generate the points and color of the Mandelbrot set                                                      
    Return the values z of the plane and the colors of each point

    forced_stop: if the user wants to run the fractal faster but in a incomplete way. Sometimes the fractals take long to calculate, this can be used
    to end the convergence loop before the stop condition.                                                                          
    stop_step: the value of the iteration the user wants to force the calculation to stop.                                                  
    cmap: cmap used for coloring the fractal. Default to viridis.                                                   
    converging_color: color in RGB of points that converge. Default to black ([0, 0, 0])                                                          
    clean_plot: if the image is displayed without the axis labels. Default True                                                                 
    width: width of the figure                                                                              
    dpi: dots per inches of figure
    zoom: the amount of zoom                                                                        
    center_x: x coordinate of the center point of the figure                                                        
    center_y: y coordinate of the center point of the figure'''
    check_dpi(width, dpi)

    # Values of displacement in x and y of the limits of the axes to ensure the new center is in the middle of figure
    dx = center_displacement(MANDELBROT_XLIM, center_x, zoom)
    dy = center_displacement(MANDELBROT_YLIM, center_y, zoom)
    
    a = np.linspace(MANDELBROT_XLIM[0]/zoom + dx, MANDELBROT_XLIM[1]/zoom + dx, width*dpi, dtype=np.float64)
    b = np.linspace(MANDELBROT_YLIM[0]/zoom + dy, MANDELBROT_YLIM[1]/zoom + dy, width*dpi, dtype=np.float64)
    
    # Complex grid
    c_start = np.array([complex(i[0], i[1]) for i in product(a, b)])

    del a, b

    # Color matrix
    color = -np.ones(c_start.shape)

    z = c_start
    c = c_start
    i = 1
    while True:
        z = z**2 + c
        diverging = np.absolute(z) > 2

        if forced_stop:
            if stop_step == i:
                break
        else:
            # If there is no point diverging, leave the loop
            if np.all(~diverging) and i > MINIMUM_ITERATIONS * zoom:
                break

        new_point = color == -1
        z[diverging] = np.nan
        color = np.where(np.logical_and(diverging, new_point), np.zeros(color.shape) + i, color)

        i += 1
    
    del diverging

    color = color_points(color, cmap, converging_color)
    plot_set(c_start, color, clean_plot=clean_plot, width=width)

    return c_start, color       
    



def plot_set(z, color, s=0.5, clean_plot=True, width=GRAPH_WIDTH, ax: plt.Axes=None):
    x = np.real(z)
    y = np.imag(z)

    # Calculate aspect ratio based on the limits of the axes
    dx = x.max() - x.min()
    dy = y.max() - y.min()
    aspect_ratio = dx/dy

    if ax == None:
        f = plt.figure(figsize=(width, width/aspect_ratio))
        ax = plt.gca()

    ax.scatter(x, y, s=s, c=color)

    # Leave the plot only with a black edge
    if clean_plot:
        ax.tick_params(labelbottom=False, bottom=False, labelleft=False, left=False)
        ax.axis('off')

    plt.tight_layout()
    plt.show()

    return f, ax




def center_displacement(limits, center, zoom):
    if type(center) == type(None):
        displ = (sum(limits))/2 - (sum(limits)/zoom)/2
    else:
        displ = center - (sum(limits)/zoom)/2

    return displ




def color_points(color, cmap, converging_color):
    # Index of points that converge until the last iteration
    converging = color == -1
    
    # Apply color banding
    color[converging] = color.max()
    color = np.log(color)/np.log(color.max())

    # Merge colors
    cmap = cm.get_cmap(cmap)
    color = cmap(color)
    
    # Color of points that converge until last iteration
    if converging_color != None:
        for i in range(3):
            color[converging, i] = converging_color[i]
    
    return color


def check_dpi(width, dpi):
    value = input(f'\n\nFractal generator\n\nUsing a dpi of {dpi}, the grid points have {width*dpi}x{width*dpi} = {(width*dpi)**2} points.\
                  \nDo you want to continue?\n\n(y/n)\n')

    if value == 'y':
        return
    elif value == 'n':
        quit()
    else:
        print('Incorrect value!')
        check_dpi(width, dpi)
