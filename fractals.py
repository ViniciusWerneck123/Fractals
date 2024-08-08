import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation
from itertools import product

DEFAULT_XLIM = [-2, 2]
MANDELBROT_XLIM = [-2.55, 1.55]
DEFAULT_DPI = 100
CMAP = 'viridis'
CONVERGING_COLOR = [0, 0, 0] # [r, g, b]
MINIMUM_ITERATIONS = 25
MAXIMUM_ITERATIONS = 500


def nxtSequenceValue(func, z):
    return func(z)



def fractal(n_iter: int=MAXIMUM_ITERATIONS, fractal_type: str="mandelbrot", c: complex=complex(0, 0), size: str='1600x900', dpi: int=DEFAULT_DPI, sampling: int=4,
            cmap: str=CMAP, converging_color: list=CONVERGING_COLOR, zoom: int=1, center_x: float=None, center_y: float=None,
            animated: bool=False, filename: str='fractal', file_type: str='gif', frame_interval: int=100) -> None:
    '''Creates an image or animation of a specified fractal.                                    

    Parameters
    ----------
    n_iter: int, None
        number of iterations to generate the fractal. If ``n_iter`` is not given, then the fractal will be contructed with 500 iterations.                                                             
    fractal_type: {'julia', 'mandelbrot'} 
        the type of the fractal. Default is `'mandelbrot'`.                                   
    c: complex
        the constant `c` in the sequence. If `fractal_type='mandelbrot'`, this should not be used.
    size: str
        The size of the respective image/animation in pixels. Default to `'1600x900`'.                                               
    dpi: int
        dots per inches. Default is 100.   
    sampling: int
        The sampling rate of points per pixel, Default to 4.                                                
    cmap: str
        matplotlib color map used to color the fractal. Default to `'viridis'`.                                                         
    converging_color: list([red, green, blue])
        the color of points that do not diverge until the last iteration. The values of each color are a float between 0 and 1.
        Default to [0, 0, 0] -> black
    zoom: int
        The zoom value of the fractal.
    center_x: float, None
        The x center value of the image. Default to `None`
    center_y: float, None
        The y center value of the image. Default to `None`
    animated: bool
        Controls the kind of output. If `True`, the program will generate a file with the name given by `filename` that is an animated
        version of the fractal with a number of frames equal to n_iter. If n_iter = None, then the program will raise and error. 
        If `False`, then the program will show the image after running as an image that can be saved using
        matplotlib controls. Default to `False`.
    filename: str
        The name and type of the animation that will be created. Default to `'fractal'`.
    file_type: str
        The file extension that the animated file will have. Default to `'gif'`.
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
        print("The 'type' parameter is incorrect. Should be either 'mandelbrot' or 'julia', review your code")
        exit(0)

    ### Creating the grid of points
    size = size.split('x')
    width, height = int(size[0]), int(size[1])

    aspect_ratio = height/width

    # Getting the respective ylim using the aspect ratio of the monitor
    overall_y_height = np.sum(np.abs(np.array(xlim)))*aspect_ratio
    ylim = [-overall_y_height/2, overall_y_height/2]

    # Values of displacement in x and y of the limits of the axes to ensure the new center is in the middle of figure
    dx = center_displacement(xlim, center_x, zoom)
    dy = center_displacement(ylim, center_y, zoom)

    n_x = int(width*sampling/2)
    n_y = int(height*sampling/2)

    # Grid of points
    x = np.linspace(xlim[0]/zoom + dx, xlim[1]/zoom + dx, n_x, dtype=np.float64)
    y = np.linspace(ylim[0]/zoom + dy, ylim[1]/zoom + dy, n_y, dtype=np.float64)
    values = product(x, y)

    del x, y

    # Complex grid
    grid_points = np.array([complex(i[0], i[1]) for i in values]).reshape((n_x, n_y))
    
    # z and color needs to be global in order to the inner function 'update()' below can access them
    global z, color

    # Color of the converging points
    color = np.ones(grid_points.shape)*-1

    if fractal_type == 'mandelbrot':
        z = c
        c = grid_points
    else:
        z = grid_points

    # Creating the figure and adding an axes that ocuppies the whole figure area
    fig = plt.figure(figsize=(width/dpi, height/dpi), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])

    # Leaves the plot without lines and labels
    ax.tick_params(labelbottom=False, bottom=False, labelleft=False, left=False)
    ax.axis('off')

    # Creation of img Artist, needs to use the transpose of color grid
    img = ax.imshow(color_points(color, cmap, converging_color), interpolation='antialiased')
    
    print('\n************************ Fractal generator ************************\
          \nGenerating fractal...')
    start_time = time.time()

    def calculate_color(row, row_id):
        '''The loop that calculates the sequence for an row of the grid'''
        iteration = 0
        row_color = -np.ones(row.shape)
        while iteration <= n_iter:
            row = nxtSequenceValue(lambda x: x**2 + c, row)
            diverging = np.absolute(row) > 2

            # Calculates the color of the row if diverging points exists
            row_color[diverging] = iteration + 1 - np.log10(np.absolute(row[diverging]))/np.log10(2)
            row[diverging] = np.nan
            
            # If all points diverges, then the loop does not need to continue
            if np.all(np.isnan(row)):
                break
            iteration += 1
        
        color[row_id] = row_color

    # Run the loop for each row
    for ix in range(n_x):
        calculate_color(grid_points[ix], ix)

    # Creates the color grid with RGBA values
    color_map = color_points(color, cmap, converging_color)
    img.set_data(color_map)
    plt.savefig(filename + '.png', dpi=dpi)

    end_time = time.time()
    evaluate_elapsed_time(start_time, end_time, n_iter)




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



def evaluate_elapsed_time(start, end, n_iter):
    elapsed_time = end - start
    print(f'\nNumber of iterations: {n_iter:.0f}\
          \nElapsed time: {elapsed_time/60:02.0f}:{round(elapsed_time%60, 0):02.0f} s\
          \n*******************************************************************')
