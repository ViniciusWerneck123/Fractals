# Fractals
Fractals is a program to create images of fractals. Until this stage, the ones available are the julia and mandelbrot fractals.
There is an parameter available to create animations but is too heavy at this stage of development and one should use a number of iterations below 100 (this number already takes up to 2 min or more depending on which fractal).

Here are some examples:

Julia set for c = 1 - golden ratio:

`fractal(fractal_type='julia', c=complex(-0.64, 0), converging_color=[0, 0, 0], dpi=100)`

![juliaset_1](https://github.com/user-attachments/assets/65bbea49-0965-4a32-a916-2dcb21b16dd9)


Julia set for c = 0.285 - 0.01i

`fractal(fractal_type='julia', c=complex(0.285, -0.01), converging_color=[0, 0, 0], dpi=100)`

![juliaset_2](https://github.com/user-attachments/assets/2c68e7ae-0265-4da3-8d7e-006ff189c9ba)

Animated version
`fractal(n_iter=100, fractal_type='julia', c=complex(0.285, -0.01), animated=True)`
`#Output`
`************************ Fractal generator ************************`

`Using a dpi of 100, the grid has 1500x840 = 1260000.0 points.`
`Do you want to continue?`

`(y/n)`
`y`

`Elapsed time: 227.13 s`
`*******************************************************************`


Plotting the Mandelbrot set:

`fractal(fractal_type='mandelbrot', cmap='binary_r', dpi=100)`
`#Output`
`************************ Fractal generator ************************`

`Using a dpi of 100, the grid has 1500x840 = 1260000.0 points.`
`Do you want to continue?`

`(y/n)`
`y`

`Elapsed time: 15.31 s`
`*******************************************************************`

![mandelbrot](https://github.com/user-attachments/assets/c34ced51-6260-4227-8f32-ad2de2587ef9)

Animated version:

`#Output`
`************************ Fractal generator ************************`

`Using a dpi of 100, the grid has 1500x840 = 1260000.0 points.`
`Do you want to continue?`

`(y/n)`
`y`

`Elapsed time: 61.39 s`
`*******************************************************************`

