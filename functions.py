import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation
from itertools import product
from screeninfo import get_monitors

DEFAULT_XLIM = [-2, 2]
MANDELBROT_XLIM = [-2.5, 1.5]
DEFAULT_DPI = 100
CMAP = 'viridis'
CONVERGING_COLOR = [0, 0, 0] # [r, g, b]
MINIMUM_ITERATIONS = 25
MAXIMUM_ITERATIONS = 500


def nxtSequenceValue(func, z):
    return func(z)



def fractal(n_iter=None, fractal_type="mandelbrot", c=complex(0, 0), dpi=DEFAULT_DPI, cmap=CMAP, converging_color=CONVERGING_COLOR,
            clean_plot=True, zoom=1, center_x=None, center_y=None, xlim=None, animated=False):
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
    # Creation of img Artist, needs to use the transpose of color grid
    img = ax.imshow((color + 1).T, cmap=cmap)

    start_time = time.time()

    def update(n_iter, z, c, color):
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
    else:
        anim = animation.FuncAnimation(fig=fig, func=update, fargs=(z, c, color), frames=n_iter, repeat=False, interval=30, cache_frame_data=False)
    
    # Leave the plot without lines and labels
    if clean_plot:
        ax.tick_params(labelbottom=False, bottom=False, labelleft=False, left=False)
        ax.axis('off')
    # Make figure occupy the whole screen
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')

    plt.show()

    end_time = time.time()
    evaluate_elapsed_time(start_time, end_time)



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



def evaluate_elapsed_time(start, end):
    elapsed_time = end - start
    print(f'\nElapsed time: {elapsed_time:.2f} s\
          \n*******************************************************************')
