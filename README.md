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

![c=0 285 _0 01i](https://github.com/user-attachments/assets/bc6d865e-8569-47eb-90e8-6d6f2ec04dee)


## Animated version
```
fractal(n_iter=100, fractal_type='julia', c=complex(0.285, -0.01), size='800x450', animated=True)
```
```
#Output
************************ Fractal generator ************************
Generating fractal...

Number of iterations: 100
Elapsed time: 00:10 s
*******************************************************************
```

![julia1](https://github.com/user-attachments/assets/7e8714fc-eeb7-473a-8f34-f88373b59838)


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
