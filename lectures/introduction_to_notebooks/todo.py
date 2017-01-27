# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors


def mandelbrot(X, Y, max_iterations=1000, verbose=True):
    """Computes the Mandelbrot set.

    Returns a matrix with the escape iteration number of the mandelbrot
    sequence. The matrix contains a cell for every (x, y) couple of the
    X and Y vectors elements given in input. Maximum max_iterations are
    performed for each point
    :param X: set of x coordinates
    :param Y: set of y coordinates
    :param max_iterations: maximum number of iterations to perform before
        forcing to stop the sequence
    :param show_out: flag indicating whether to print on console which line
        number is being computed
    :return: Matrix containing the escape iteration number for every point
        specified in input
    """

    # init the output array
    out_arr = np.zeros((len(Y), len(X)))

    # Iterate of the y coordinates
    for i, y in enumerate(Y):

        if verbose:
            print('\rProcessing line {} of {}'.format(i+1, len(Y)), end='')

        for j, x in enumerate(X):
            n = 0
            c = x + 1j*y
            z = c
            while (n < max_iterations) and (abs(z) <= 2):
                z = z*z + c
                n += 1
            out_arr[i, j] = n

    if verbose:
        print('\r', end='')
    return out_arr


def _mandelbrot_vectorized(X, Y, maxiter, horizon=2.0):
    C = X + Y[:, None]*1j
    N = np.zeros(C.shape, dtype=int)
    Z = np.zeros(C.shape, np.complex64)
    for n in range(maxiter):
        I = np.less(abs(Z), horizon)
        N[I] = n
        Z[I] = Z[I]**2 + C[I]
    N[N == maxiter-1] = 0
    return Z, N


def fractional_mandelbrot(X, Y, maxiter, horizon=2.0):
    Z, N = _mandelbrot_vectorized(X, Y, maxiter, horizon)

    log_horizon = np.log(np.log(horizon))/np.log(2)

    # This line will generate warnings for null values but it is faster to
    # process them afterwards using the nan_to_num
    with np.errstate(invalid='ignore'):
        M = np.nan_to_num(
            N + 1 - np.log(np.log(abs(Z))) / np.log(2) + log_horizon)
    return M


def pretty_plot(fractal_image):
    dpi = 72
    width = 10
    height = 10 * fractal_image.shape[1] / fractal_image.shape[0]
    fig = plt.figure(figsize=(width, height), dpi=dpi)
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0], frameon=False, aspect=1)

    light = colors.LightSource(azdeg=315, altdeg=10)
    fractal_image = light.shade(
        fractal_image, cmap=plt.cm.hot, vert_exag=1.5,
        norm=colors.PowerNorm(0.3), blend_mode='hsv')

    plt.imshow(fractal_image,
               interpolation="bicubic")
    ax.set_xticks([])
    ax.set_yticks([])

    plt.show()
