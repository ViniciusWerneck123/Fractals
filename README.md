# Fractals
Fractals is a program to create images of fractals. Until this stage, the ones available are the julia and mandelbrot fractals.
There is a parameter available to create animated fractals like ones given below.

Requirements:
```
matplotlib
numpy
```

Here are some examples:

## Julia set for c = 1 - golden ratio:

```
fractal(fractal_type='julia', c=complex(-0.64, 0), size='800x450')
```

![c=-0 64](https://github.com/user-attachments/assets/47892e7f-b9c3-4328-9362-872dd87fa347)


## Julia set for c = 0.285 - 0.01i

```
fractal(fractal_type='julia', c=complex(0.285, -0.01), size='800x450')
```

![Fig1](https://github.com/user-attachments/assets/d0c1899d-4938-4525-9ffb-63d824ebfbff)


## Animated version
```
fractal(n_iter=100, fractal_type='julia', c=complex(0.285, -0.01), size='800x450', animated=True)
```
```
#Output
************************ Fractal generator ************************
Generating fractal...

Number of iterations: 100
Elapsed time: 01:35 s
*******************************************************************
```

![Anim1](https://github.com/user-attachments/assets/a0a55af1-b26e-46dc-84f7-5dcb5e4e8b63)


## Plotting the Mandelbrot set:

```
fractal(fractal_type='mandelbrot', cmap='binary_r', size='800x450', converging_color=[1, 1, 1])
```
```
#Output
************************ Fractal generator ************************
Generating fractal...

Number of iterations: 130
Elapsed time: 00:05 s
*******************************************************************
```

![mandelbrot](https://github.com/user-attachments/assets/227b0a31-3367-4d81-8dd6-53c68de56b5b)


## Animated version:

```
fractal(n_iter=50, fractal_type='mandelbrot', cmap='binary', animated=True)
```
```
#Output
************************ Fractal generator ************************
Generating fractal...

Number of iterations: 50
Elapsed time: 00:13 s
*******************************************************************
```

![mandelbrot](https://github.com/user-attachments/assets/f0698a6c-f81c-40f1-a31c-0ffd75582a06)


## License

License is MIT.
