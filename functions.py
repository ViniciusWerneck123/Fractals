import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from itertools import product
from screeninfo import get_monitors

DEFAULT_XLIM = [-2, 2]
MANDELBROT_XLIM = [-2.5, 1.5]
DEFAULT_DPI = 100
STOP_STEP = 100
CMAP = 'viridis'
INTERIOR_COLOR = [0, 0, 0] # [r, g, b]
MINIMUM_ITERATIONS = 25
MAXIMUM_ITERATIONS = 500

def julia(c: complex, forced_stop=False, stop_step=STOP_STEP, cmap=CMAP,
            converging_color=INTERIOR_COLOR, clean_plot=True, dpi=DEFAULT_DPI,
            zoom=1, center_x=None, center_y=None, xlim=DEFAULT_XLIM):
    '''Function that return the points and colors for each point for the fractal.
    Return a tuple of matrices with x and y values of the mandelbrot set.\n                                                  
    c: the complex constant value of the sequence.                                               
    forced_stop: if the user wants to run the fractal faster but in a incomplete way. Sometimes the fractals take long to calculate, this can be used
    to end the convergence loop before the stop condition.                                                                          
    stop_step: the value of the iteration the user wants to force the calculation to stop.                                                      
    cmap: cmap used for coloring the fractal. Default to viridis.                                                       
    converging_color: [r, g, b] - list color in RGB of points that converge. Default to last color in cmap                                                              
    clean_plot: if the image is displayed without the axis labels. Default True                                                                 
    dpi: dots per inches of figure                                                                          
    zoom: the amount of zoom. If specified, the values for center_x and center_y should be specified also.
            If not, the center_x value will be the resultant one using default value of xlim and
            center_y will be 0.                                                                                             
    center_x: x coordinate of the center point of the figure                                                        
    center_y: y coordinate of the center point of the figure                                                    
    xlim: x limits for the fractal. Default: [-2, 2]'''
    # Gets the value of inches of the monitor
    monitor = get_monitors()[0]
    width, height = round(monitor.width_mm/25.4, 1), round(monitor.height_mm/25.4, 1)

    aspect_ratio = height/width

    check_dpi(width, height, dpi)

    overall_y_height = np.sum(np.abs(np.array(xlim)))*aspect_ratio
    ylim = [-overall_y_height/2, overall_y_height/2]

    start_time = time.time()

    # Values of displacement in x and y of the limits of the axes to ensure the new center is in the middle of figure
    dx = center_displacement(xlim, center_x, zoom)
    dy = center_displacement(ylim, center_y, zoom)

    # Grid of points
    x = np.linspace(xlim[0]/zoom + dx, xlim[1]/zoom + dx, int(width*dpi), dtype=np.float64)
    y = np.linspace(ylim[0]/zoom + dy, ylim[1]/zoom + dy, int(height*dpi), dtype=np.float64)
    values = product(x, y)

    del x, y

    # Complex grid
    z_start = np.array([complex(i[0], i[1]) for i in values]).reshape((int(width*dpi), int(height*dpi)))

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
        sn = 1 - np.log10(np.absolute(z))/np.log10(2)
        color[np.logical_and(diverging, new_point)] = i + sn[np.logical_and(diverging, new_point)]
        z[diverging] = np.nan
        
        i += 1

    del diverging, new_point

    end_time = time.time()
    evaluate_elapsed_time(start_time, end_time, i)
    
    color = color_points(color, cmap, converging_color)

    plot_set(color, clean_plot=clean_plot)





def mandelbrot(forced_stop = False, stop_step=STOP_STEP, cmap=CMAP,
                converging_color=INTERIOR_COLOR, clean_plot=True, dpi=DEFAULT_DPI,
                zoom=1, center_x=None, center_y=None, xlim=MANDELBROT_XLIM):
    '''Generate the points and color of the Mandelbrot set                                                      
    Return the values z of the plane and the colors of each point

    forced_stop: if the user wants to run the fractal faster but in a incomplete way. Sometimes the fractals take long to calculate, this can be used
    to end the convergence loop before the stop condition.                                                                          
    stop_step: the value of the iteration the user wants to force the calculation to stop.                                                  
    cmap: cmap used for coloring the fractal. Default to viridis.                                                   
    converging_color: color in RGB of points that converge. Default to black ([0, 0, 0])                                                          
    clean_plot: if the image is displayed without the axis labels. Default True                                                                 
    dpi: dots per inches of figure                                                                      
    zoom: the amount of zoom. If specified, the values for center_x and center_y should be specified also.
            If not, the center_x value will be the resultant one using default value of xlim and
            center_y will be 0.                                                                              
    center_x: x coordinate of the center point of the figure.                                                        
    center_y: y coordinate of the center point of the figure                                                                            
    xlim: x limits for the fractal. Default: [-2.5, 1.5]'''
    # Gets the value of inches of the monitor
    monitor = get_monitors()[0]
    width, height = round(monitor.width_mm/25.4, 1), round(monitor.height_mm/25.4, 1)

    aspect_ratio = height/width
    
    check_dpi(width, height, dpi)

    # Calculates respective ylim with xlim and calculated aspect_ratio
    overall_y_height = np.sum(np.abs(np.array(xlim)))*aspect_ratio
    ylim = [-overall_y_height/2, overall_y_height/2]

    start_time = time.time()

    # Values of displacement in x and y of the limits of the axes to ensure the new center is in the middle of figure
    dx = center_displacement(xlim, center_x, zoom)
    dy = center_displacement(ylim, center_y, zoom)
    
    a = np.linspace(xlim[0]/zoom + dx, xlim[1]/zoom + dx, int(width*dpi), dtype=np.float64)
    b = np.linspace(ylim[0]/zoom + dy, ylim[1]/zoom + dy, int(height*dpi), dtype=np.float64)
    
    # Complex grid
    c_start = np.array([complex(i[0], i[1]) for i in product(a, b)]).reshape((int(width*dpi), int(height*dpi)))

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
        sn = 1 - np.log10(np.absolute(z))/np.log10(2)
        color[np.logical_and(diverging, new_point)] = i + sn[np.logical_and(diverging, new_point)]
        z[diverging] = np.nan

        i += 1
    
    del diverging

    end_time = time.time()
    evaluate_elapsed_time(start_time, end_time, i)
    
    color = color_points(color, cmap, converging_color)

    plot_set(color, clean_plot=clean_plot)
       
    



def plot_set(color, clean_plot=True):
    f = plt.figure()
    
    # Add axes with the size of the figure
    ax = f.add_axes([0, 0, 1, 1])

    ax.imshow(color)

    # Leave the plot without lines and labels
    if clean_plot:
        ax.tick_params(labelbottom=False, bottom=False, labelleft=False, left=False)
        ax.axis('off')

    # Make figure occupy the whole screen
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')

    plt.show()

    return f, ax



def color_points(color, cmap, converging_color):
    cmap = cm.get_cmap(cmap)
    
    # Necessary in order for the orientation to be right
    color = color.T

    # Save the final shape of colors grid
    shape = tuple([*color.shape, 4])

    # Flattening makes easy to change the color of converging points
    color = color.flatten()
    converging = color == -1

    # Sets converging points to zero just for cmap method does not raises any error
    # because the values should be between 0 and 1
    color[converging] = 0

    color = cmap(color/color.max())

    # Change the color of converging points to the specified color
    for i in range(3):
        color[converging, i] = converging_color[i]

    # Reshape the flattened array for the correct shape
    color = color.reshape(shape)
    return color



def center_displacement(limits, center, zoom):
    if type(center) == type(None):
        displ = (sum(limits))/2 - (sum(limits)/zoom)/2
    else:
        displ = center - (sum(limits)/zoom)/2

    return displ



def check_dpi(width, height, dpi):
    value = input(f'\n************************ Fractal generator ************************\
                  \n\nUsing a dpi of {dpi}, the grid has {width*dpi:.0f}x{height*dpi:.0f} = {(width*dpi)*(height*dpi)} points.\
                  \nDo you want to continue?\n\n(y/n)\n')

    if value == 'y':
        return
    elif value == 'n':
        quit()
    else:
        print('Incorrect value!')
        check_dpi(width, dpi)



def evaluate_elapsed_time(start, end, n_iterations):
    elapsed_time = end - start
    print(f'\nElapsed time: {elapsed_time:.2f} s\
          \nNumber of iterations: {n_iterations}\
          \n*******************************************************************')
