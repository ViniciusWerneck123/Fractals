import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation
from itertools import product
from screeninfo import get_monitors

DEFAULT_XLIM = [-2, 2]
MANDELBROT_XLIM = [-2.55, 1.55]
DEFAULT_DPI = 100
CMAP = 'viridis'
CONVERGING_COLOR = [0, 0, 0] # [r, g, b]
MINIMUM_ITERATIONS = 25
MAXIMUM_ITERATIONS = 500


def nxtSequenceValue(func, z):
    return func(z)



def fractal(n_iter: int=None, fractal_type: str="mandelbrot", c: complex=complex(0, 0), dpi: int=DEFAULT_DPI, cmap: str=CMAP,
            converging_color: list=CONVERGING_COLOR, clean_plot: bool=True, zoom: int=1, center_x: float=None, center_y: float=None,
            xlim: list=None, animated: bool=False, filename: str='fractal.gif', frame_interval: int=100) -> None:
    '''Creates an image or animation of a specified fractal.                                    

    Parameters
    ----------
    n_iter: int, None
        number of iterations to generate the fractal. If ``n_iter`` is not given, then the fractal will exit when there is no
        more points diverging in one iteration. For some fractals, the iteration where this happens could be high, up to 500 iterations.                                                             
    fractal_type: {'julia', 'mandelbrot'} 
        the type of the fractal. Default is `'mandelbrot'`.                                   
    c: complex
        the constant `c` in the sequence. If `fractal_type='mandelbrot'`, this should not be used.                                               
    dpi: int
        dots per inches, number used for calculation of grid size. Default is 100.                                                     
    cmap: str
        matplotlib color map used to color the fractal. Default to `'viridis'`.                                                         
    converging_color: list([red, green, blue])
        the color of points that do not diverge until the last iteration. The values of each color are a float between 0 and 1.
        Default to [0, 0, 0] -> black
    clean_plot: bool
        If `clean_plot` is `True`, the plot will appears without labels and ticks. If `False`, they will appear in the image.
    zoom: int
        The zoom value of the fractal.
    center_x: float, None
        The x center value of the image. Default to `None`
    center_y: float, None
        The y center value of the image. Default to `None`
    xlim: list([xmin, xmax])
        The x limits of the image. If `fractal_type = 'julia'`, default to `[-2, 2]` and if `fractal_type = 'mandelbrot'`, default to `[-2.55, 1.55]`.
    animated: bool
        Controls the kind of output. If `True`, the program will generate a file with the name given by `filename` that is an animated
        version of the fractal with a number of frames equal to n_iter. If n_iter = None, then the program will raise and error. 
        If `False`, then the program will show the image after running as an image that can be saved using
        matplotlib controls. Default to `False`.
    filename: str
        The name and type of the animation that will be created. Default to `'fractal.gif'`.
    frame_interval: int
        The interval between frames in miliseconds. Default to 100'''
    # If animated = True, the number of frames (n_iter) must be different of None
    if animated and type(n_iter) == type(None):
        print('\nParameter error:')
        print('When \'animated\' = True, the parameter \'n_iter\' must be given to avoid a heavy gif with too many frames.\n')
        return None

    if fractal_type == "mandelbrot":
        xlim = MANDELBROT_XLIM
    elif fractal_type == "julia":
        xlim = DEFAULT_XLIM
    else:
        print("type parameter is incorrect. Should be either 'mandelbrot' or 'julia', review your code")
        exit(0)

    ### Creating the grid of points
    # Gets the value of inches of the monitor
    monitor = get_monitors()[0]
    width, height = round(monitor.width_mm/25.4, 1), round(monitor.height_mm/25.4, 1)

    aspect_ratio = height/width

    # Ask the user if the size of grid is ok
    check_dpi(width, height, dpi)

    # Getting the respective ylim using the aspect ratio of the monitor
    overall_y_height = np.sum(np.abs(np.array(xlim)))*aspect_ratio
    ylim = [-overall_y_height/2, overall_y_height/2]

    # Values of displacement in x and y of the limits of the axes to ensure the new center is in the middle of figure
    dx = center_displacement(xlim, center_x, zoom)
    dy = center_displacement(ylim, center_y, zoom)

    # Grid of points
    x = np.linspace(xlim[0]/zoom + dx, xlim[1]/zoom + dx, int(width*dpi), dtype=np.float64)
    y = np.linspace(ylim[0]/zoom + dy, ylim[1]/zoom + dy, int(height*dpi), dtype=np.float64)
    values = product(x, y)

    del x, y

    # Complex grid
    grid_points = np.array([complex(i[0], i[1]) for i in values]).reshape((int(width*dpi), int(height*dpi)))
    
    # Color of the converging points
    color = np.ones(grid_points.shape)*-1

    if fractal_type == 'mandelbrot':
        z = c
        c = grid_points
    else:
        z = grid_points

    # Creating the figure
    fig = plt.figure()
    # Add axes that occupies all the figure area
    ax = fig.add_axes([0, 0, 1, 1])
    # Leave the plot without lines and labels
    if clean_plot:
        ax.tick_params(labelbottom=False, bottom=False, labelleft=False, left=False)
        ax.axis('off')

    # Creation of img Artist, needs to use the transpose of color grid
    img = ax.imshow(color_points(color, cmap, converging_color))

    start_time = time.time()

    def update(n_iter, z, c, color):
        '''The loop that calculates the sequence'''
        global i
        i = 1
        while True:
            z = nxtSequenceValue(lambda x: x**2 + c, z)

            # Update color based on convergence:
            # if point diverge, the value, color = i -> the number of the iteration it took to diverge
            diverging = np.absolute(z) > 2

            if type(n_iter) != type(None):
                if i >= n_iter:
                    break
            else:
                # If there is no point diverging, leave the loop
                if np.all(~diverging) and i > MINIMUM_ITERATIONS:
                    break

            new_point = color == -1
            sn = 1 - np.log10(np.absolute(z))/np.log10(2)
            color[np.logical_and(diverging, new_point)] = i + sn[np.logical_and(diverging, new_point)]
            z[diverging] = np.nan

            i += 1
        
        color = color_points(color, cmap=cmap, converging_color=converging_color)
        img.set_data(color)

        return (img, )

    if not animated:
        update(n_iter, z, c, color)
        # Make figure occupy the whole screen
        mng = plt.get_current_fig_manager()
        mng.window.state('zoomed')

        plt.show()
    else:
        anim = animation.FuncAnimation(fig=fig, func=update, fargs=(z, c, color), frames=n_iter, repeat=False, interval=frame_interval,
                                       cache_frame_data=False)
        anim.save(filename, writer='pillow')
        # When frames in FuncAnimation is just a number, is equivalent to range(n_iter), so the last value
        # is not n_iter but n_iter - 1. This is to i = the number of iterations.
        i += 1
    

    end_time = time.time()
    evaluate_elapsed_time(start_time, end_time, i)



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

    if color.max() == 0:
        color = cmap(color)
    else:
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



def evaluate_elapsed_time(start, end, n_iter):
    elapsed_time = end - start
    print(f'\nNumber of iterations: {n_iter:.0f}\
          \nElapsed time: {elapsed_time/60:02.0f}:{round(elapsed_time%60, 0):02.0f} min\
          \n*******************************************************************')
