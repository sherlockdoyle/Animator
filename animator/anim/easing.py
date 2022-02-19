"""This module defines different types of interpolation and utility functions. There are three kinds of animations:

  - **in**: Starts slow, faster at the end.
  - **out**: Starts fast, slower at the end.
  - **inout**: Starts slow, ends slow, fast in the middle. Use this for the smoothest animations.

All the interpolator functions take a single parameter, *t*, a float usually between [0, 1] and returns a float in the
same range. Here are some of the functions, with x-axis as the input, and y-axis as the output.

.. plot::

    import animator as am
    plt.rcParams["figure.figsize"] = (9, 25)
    f = ['quad', 'cubic', 'quart', 'quint', 'exp', 'sin', 'circ', 'back', 'elastic', 'bounce']
    x = np.linspace(0, 1, 100)
    fig, axes = plt.subplots(nrows=len(f), ncols=3)
    for i in range(len(f)):
        axes[i][0].set_ylabel(f[i] + "          ", rotation=0, size='xx-large')
    axes[0][0].set_title("in", size='xx-large')
    axes[0][1].set_title("out", size='xx-large')
    axes[0][2].set_title("inout", size='xx-large')
    for i in range(len(f)):
        axes[i][0].plot(x, np.vectorize(getattr(am.interp, f[i] + "_in"))(x))
        axes[i][1].plot(x, np.vectorize(getattr(am.interp, f[i] + "_out"))(x))
        axes[i][2].plot(x, np.vectorize(getattr(am.interp, f[i] + "_inout"))(x))
    plt.tight_layout()
    plt.show()
"""
from __future__ import annotations
import math
import math as _math
from typing import Callable as _Callable

_HALF_PI = math.pi / 2
_TWO_PI = math.tau


def linear(t: float) -> float:
    """Linear interpolation, whatever is the input is the output. :math:`f(t) = t`"""
    return t


def sin_in(t: float) -> float:
    """Sinusoidal in. :math:`f(t) = \\sin(t)`"""
    return 1 - _math.cos(t * _HALF_PI)


def sin_out(t: float) -> float:
    """Sinusoidal out. :math:`f(t) = \\sin(t)`"""
    return _math.sin(t * _HALF_PI)


def sin_inout(t: float) -> float:
    """Sinusoidal inout. :math:`f(t) = \\sin(t)`"""
    return -0.5 * (_math.cos(_math.pi * t) - 1)


def circ_in(t: float) -> float:
    """Circular in. A quarter of a circle. :math:`f(t) = \\sqrt{1 - t^2}`"""
    return 1 - _math.sqrt(1 - t * t)


def circ_out(t: float) -> float:
    """Circular out. A quarter of a circle. :math:`f(t) = \\sqrt{1 - t^2}`"""
    return _math.sqrt(t * (2 - t))


def circ_inout(t: float) -> float:
    """Circular inout. Two quarters of a circle. :math:`f(t) = \\sqrt{1 - t^2}`"""
    t *= 2
    if t < 1:
        return 0.5 * (1 - _math.sqrt(1 - t * t))
    t -= 2
    return 0.5 * (_math.sqrt(1 - t * t) + 1)


def exp_in(t: float) -> float:
    """Exponential in. :math:`f(t) = 2^t`"""
    return pow(2, 10 * (t - 1))


def exp_out(t: float) -> float:
    """Exponential out. :math:`f(t) = 2^t`"""
    return 1 - pow(2, -10 * t)


def exp_inout(t: float) -> float:
    """Exponential inout. :math:`f(t) = 2^t`"""
    t *= 2
    return .5 * (pow(2, 10 * (t - 1)) if t < 1 else 2 - pow(2, 10 * (1 - t)))


def bounce_in(t: float) -> float:
    """Bounce in. Amplitude of bounce increases."""
    return 1 - bounce_out(1 - t)


def bounce_out(t: float) -> float:
    """Bounce out. Amplitude of bounce decreases."""
    if t < 0.36363636363636365:
        return 7.5625 * t * t
    elif t < 0.7272727272727273:
        return 7.5625 * (t - 0.5454545454545454) ** 2 + 0.75
    elif t < 0.9090909090909091:
        return 7.5625 * (t - 0.8181818181818182) ** 2 + 0.9375
    else:
        return 7.5625 * (t - 0.9545454545454546) ** 2 + 0.984375


def bounce_inout(t: float) -> float:
    """Bounce inout. Amplitude of bounce first increases, then decreases."""
    if t < 0.5:
        return (1 - bounce_out(1 - t * 2)) * .5
    return (bounce_out(t * 2 - 1) + 1) * .5


def bezier(p1x: float, p1y: float, p2x: float, p2y: float | None = None) -> _Callable[[float], float]:
    """Creates and returns an interpolating function for a bezier curve defined by one (*p1x*, *p1y*) or two (*p2x*,
    *p2y*) control points. The curve starts at (0, 0) and ends at (1, 1)."""
    if p2x is None or p2y is None:
        p1x *= 0.6666666666666666
        p1y *= 0.6666666666666666
        p2x, p2y = p1x + 0.3333333333333333, p1y + 0.3333333333333333
    e = 1e-6

    cx = 3 * p1x
    bx = 3 * (p2x - p1x) - cx
    ax = 1 - cx - bx
    cy = 3 * p1y
    by = 3 * (p2y - p1y) - cy
    ay = 1 - cy - by

    def X(t: float) -> float:
        return ((ax * t + bx) * t + cx) * t

    def X_inv(x: float) -> float:
        t2 = x
        for i in range(8):
            x2 = X(t2) - x
            if abs(x2) < e:
                return t2
            d2 = (3 * ax * t2 + 2 * bx) * t2 + cx
            if abs(d2) < e:
                break
            t2 -= x2 / d2
        t0, t1, t2 = 0.0, 1.0, x
        if t2 < t0:
            return t0
        if t2 > t1:
            return t1
        while t0 < t1:
            x2 = X(t2)
            if abs(x2 - x) < e:
                return t2
            if x > x2:
                t0 = t2
            else:
                t1 = t2
            t2 = (t1 - t0) * .5 + t0
        return t2

    def f(t: float) -> float:
        x = X_inv(t)
        return ((ay * x + by) * x + cy) * x

    return f


def get(amt: float) -> _Callable[[float], float]:
    """Creates and returns a quadratic easing interpolator with amount of easing (curvature of the function) *amt*. -1
    gives a **in** type interpolator, 1 gives a **out** type interpolator, 0 just returns the :func:`linear`
    interpolator. Other values returns something in between."""
    if amt < -1:
        amt = -1
    elif amt > 1:
        amt = 1
    return lambda t: t * (1 + (1 - t) * amt)


def get_pow_in(n: float) -> _Callable[[float], float]:
    """Returns a **in** type polynomial interpolator of power *n*."""
    return lambda t: pow(t, n)


def get_pow_out(n: float) -> _Callable[[float], float]:
    """Returns a **out** type polynomial interpolator of power *n*."""
    return lambda t: 1 - pow(1 - t, n)


def get_pow_inout(n: float) -> _Callable[[float], float]:
    """Returns a **inout** type polynomial interpolator of power *n*."""

    def f(t: float) -> float:
        t *= 2
        if t < 1:
            return 0.5 * pow(t, n)
        return 1 - 0.5 * abs(pow(2 - t, n))

    return f


def get_back_in(amt: float) -> _Callable[[float], float]:
    """Generates and returns interpolator functions like :func:`back_in`. *amt* defines the amount the function will go
    below 0."""
    return lambda t: t * t * ((amt + 1) * t - amt)


def get_back_out(amt: float) -> _Callable[[float], float]:
    """Generates and returns interpolator functions like :func:`back_out`. *amt* defines the amount the function will go
    above 1."""

    def f(t: float) -> float:
        t -= 1
        return t * t * ((amt + 1) * t + amt) + 1

    return f


def get_back_inout(amt: float) -> _Callable[[float], float]:
    """Generates and returns interpolator functions like :func:`back_inout`. *amt* defines the amount the function will
    go below 0 and above 1."""
    amt *= 1.525

    def f(t: float) -> float:
        t *= 2
        if t < 1:
            return 0.5 * (t * t * ((amt + 1) * t - amt))
        t -= 2
        return 0.5 * (t * t * ((amt + 1) * t + amt) + 2)

    return f


def get_elastic_in(amp: float, p: float) -> _Callable[[float], float]:
    """Creates and returns an **in** type interpolating function to simulate the behaviour of a oscillating spring with
    amplitude *amp* and period *p*."""

    def f(t: float) -> float:
        if t == 0 or t == 1:
            return t
        t -= 1
        return -amp * pow(2, 10 * t) * _math.sin(t * _TWO_PI / p - _math.asin(1 / amp))

    return f


def get_elastic_out(amp: float, p: float) -> _Callable[[float], float]:
    """Creates and returns an **out** type interpolating function to simulate the behaviour of a oscillating spring with
    amplitude *amp* and period *p*."""
    return lambda t: t if t == 0 or t == 1 else amp * pow(2, -10 * t) * _math.sin(
        t * _TWO_PI / p - _math.asin(1 / amp)) + 1


def get_elastic_inout(amp: float, p: float) -> _Callable[[float], float]:
    """Creates and returns an **inout** type interpolating function to simulate the behaviour of a oscillating spring
    with amplitude *amp* and period *p*."""

    def f(t: float) -> float:
        t = t * 2 - 1
        if t < 0:
            return -0.5 * amp * pow(2, 10 * t) * _math.sin(t * _TWO_PI / p - _math.asin(1 / amp))
        return amp * pow(2, -10 * t) * _math.sin(t * _TWO_PI / p - _math.asin(1 / amp)) * 0.5 + 1

    return f


def repeat(f: _Callable[[float], float]) -> _Callable[[float], float]:
    """Creates a new interpolating function by taking a interpolating function and repeating/appending it after itself.

    .. plot::

        import animator as am
        x = np.linspace(0, 1, 100)
        plt.plot(x, np.vectorize(am.interp.cubic_inout)(x), label="original")
        plt.plot(x, np.vectorize(am.interp.repeat(am.interp.cubic_inout))(x), label="repeated")
        plt.legend()
        plt.tight_layout()
        plt.show()
    """
    return lambda t: .5 * (f(2 * t) if t < .5 else 1 + f(2 * t - 1))


def mirror(f: _Callable[[float], float]) -> _Callable[[float], float]:
    """Creates a new interpolating function by taking a interpolating function, flipping it and placing the reflected
    version beside itself.

    .. plot::

        import animator as am
        x = np.linspace(0, 1, 100)
        plt.plot(x, np.vectorize(am.interp.cubic_inout)(x), label="original")
        plt.plot(x, np.vectorize(am.interp.mirror(am.interp.cubic_inout))(x), label="mirrored")
        plt.legend()
        plt.tight_layout()
        plt.show()
    """
    return lambda t: f(2 * (t if t < .5 else 1 - t))


def oscillate(f: _Callable[[float], float], n: float = 2) -> _Callable[[float], float]:
    """Creates a new interpolating function by taking a interpolating function and superimposing it with an oscillating
    curve with *n* oscillations.

    .. plot::

        import animator as am
        x = np.linspace(0, 1, 100)
        plt.plot(x, np.vectorize(am.interp.mirror(am.interp.cubic_inout))(x), label="original")
        plt.plot(x, np.vectorize(am.interp.oscillate(am.interp.mirror(am.interp.cubic_inout)))(x), label="oscillated")
        plt.legend()
        plt.tight_layout()
        plt.show()
    """
    return lambda t: f(t) * _math.sin(n * _math.pi * t)


def nested(*f: _Callable[[float], float]) -> _Callable[[float], float]:
    """Returns a function that nests all the specified functions.

    >>> nested(f1, f2, f3, ...)(t) == f3(f2(f1(t)))...
    """

    def nester(t: float) -> float:
        for i in f:
            t = i(t)
        return t

    return nester


quad_in = get_pow_in(2)
"""
Quadratic (degree 2) in. :math:`f(t) = t^2`
"""
quad_out = get_pow_out(2)
"""
Quadratic (degree 2) out. :math:`f(t) = t^2`
"""
quad_inout = get_pow_inout(2)
"""
Quadratic (degree 2) inout. :math:`f(t) = t^2`
"""
cubic_in = get_pow_in(3)
"""
Cubic (degree 3) in. :math:`f(t) = t^3`
"""
cubic_out = get_pow_out(3)
"""
Cubic (degree 3) out. :math:`f(t) = t^3`
"""
cubic_inout = get_pow_inout(3)
"""
Cubic (degree 3) inout. :math:`f(t) = t^3`
"""
quart_in = get_pow_in(4)
"""
Quartic (degree 4) in. :math:`f(t) = t^4`
"""
quart_out = get_pow_out(4)
"""
Quartic (degree 4) out. :math:`f(t) = t^4`
"""
quart_inout = get_pow_inout(4)
"""
Quartic (degree 4) inout. :math:`f(t) = t^4`
"""
quint_in = get_pow_in(5)
"""
Quintic (degree 5) in. :math:`f(t) = t^5`
"""
quint_out = get_pow_out(5)
"""
Quintic (degree 5) out. :math:`f(t) = t^5`
"""
quint_inout = get_pow_inout(5)
"""
Quintic (degree 5) inout. :math:`f(t) = t^5`
"""
back_in = get_back_in(1.7)
back_out = get_back_out(1.7)
back_inout = get_back_inout(1.7)
elastic_in = get_elastic_in(1, 0.3)
elastic_out = get_elastic_out(1, 0.3)
elastic_inout = get_elastic_inout(1, 0.45)


def plot_interpolator(f: _Callable[[float], float], start: float = 0, stop: float = 1, num: int = 1000) -> None:
    """Utility function to plot any interpolator from *start* to *stop* with *num* points."""
    import numpy as np
    import matplotlib.pyplot as plt
    x = np.linspace(start, stop, num)
    y = np.vectorize(f)(x)
    plt.plot(x, y)
    plt.show()
