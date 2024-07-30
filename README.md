# Fractals
Fractals is a program to create images of fractals. Until this stage, the ones available are the julia and mandelbrot fractals.
There is a parameter available to create animated fractals like ones given below.

Requirements:
```
matplotlib
numpy
itertools
time
```

Here are some examples:

## Julia set for c = 1 - golden ratio:

```
fractal(fractal_type='julia', c=complex(-0.64, 0), size='800x450')
```

![juliaset_1](https://github.com/user-attachments/assets/65bbea49-0965-4a32-a916-2dcb21b16dd9)


## Julia set for c = 0.285 - 0.01i

```
fractal(fractal_type='julia', c=complex(0.285, -0.01), size='800x450')
```

![juliaset_2](https://github.com/user-attachments/assets/2c68e7ae-0265-4da3-8d7e-006ff189c9ba)

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

![julia_anim](https://github.com/user-attachments/assets/8b13d854-a01f-40a8-8cec-dbfcec4b8c78)


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

![mandelbrot](https://github.com/user-attachments/assets/c34ced51-6260-4227-8f32-ad2de2587ef9)

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

![mandelbrot_anim](https://github.com/user-attachments/assets/162903be-0627-44f6-8b14-a88ecdb5ea1f)


