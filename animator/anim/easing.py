"""Different types of interpolation functions and related utilities. There are three main types of easing functions:

  - **in**: The animation starts slowly and speeds up towards the end.
  - **out**: The animation starts quickly and slows down towards the end.
  - **inout**: The animation starts slowly, speeds up in the middle, and slows down towards the end. This is the
      smoothest type of animation.

All easing functions take a single argument, `t`, which is usually a value between 0 and 1. The function returns a float
between 0 and 1, which is the progress of the animation. Some easing functions may return values outside of this range,
for example, `bounce`.

.. plot::

    import animator as am
    plt.rcParams["figure.figsize"] = (9, 25)
    funcs = ['quad', 'cubic', 'quart', 'quint', 'exp', 'sin', 'circ', 'back', 'elastic', 'bounce']
    x = np.linspace(0, 1, 100)
    fig, axs = plt.subplots(nrows=len(funcs), ncols=3)
    for i, func in enumerate(funcs):
        axs[i, 0].set_ylabel(func + "          ", rotation=0, size='xx-large')
    axs[0, 0].set_title("in", size='xx-large')
    axs[0, 1].set_title("out", size='xx-large')
    axs[0, 2].set_title("inout", size='xx-large')
    for i, func in enumerate(funcs):
        axs[i, 0].plot(x, np.vectorize(getattr(am.easing, func + "_in"))(x))
        axs[i, 1].plot(x, np.vectorize(getattr(am.easing, func + "_out"))(x))
        axs[i, 2].plot(x, np.vectorize(getattr(am.easing, func + "_inout"))(x))
    plt.tight_layout()
    plt.show()
"""
import math
from typing import Callable

from animator import skia

_HALF_PI = math.pi / 2
_PI = math.pi
_TWO_PI = math.tau

EaseFunc = Callable[[float], float]


def linear(t: float) -> float:
    """Linear easing function, the input is the output. :math:`f(t) = t`"""
    return t


def sin_in(t: float) -> float:
    """Sinusoidal in. :math:`f(t) = \\sin(t)`"""
    return 1 - math.cos(t * _HALF_PI)


def sin_out(t: float) -> float:
    """Sinusoidal out. :math:`f(t) = \\sin(t)`"""
    return math.sin(t * _HALF_PI)


def sin_inout(t: float) -> float:
    """Sinusoidal in-out. :math:`f(t) = \\sin(t)`"""
    return (1 - math.cos(t * _PI)) * 0.5


def circ_in(t: float) -> float:
    """Circular in for a quarter circle. :math:`f(t) = \\sqrt{1 - t^2}`"""
    return 1 - math.sqrt(1 - t * t)


def circ_out(t: float) -> float:
    """Circular out for a quarter circle. :math:`f(t) = \\sqrt{1 - t^2}`"""
    return math.sqrt(t * (2 - t))


def circ_inout(t: float) -> float:
    """Circular in-out for a semi-circle. :math:`f(t) = \\sqrt{1 - t^2}`"""
    t *= 2
    if t < 1:
        return (1 - math.sqrt(1 - t * t)) * 0.5
    t -= 2
    return (1 + math.sqrt(1 - t * t)) * 0.5


def exp_in(t: float) -> float:
    """Exponential in. :math:`f(t) = 2^t`"""
    return 2 ** (10 * (t - 1))


def exp_out(t: float) -> float:
    """Exponential out. :math:`f(t) = 2^t`"""
    return 1 - 2 ** (-10 * t)


def exp_inout(t: float) -> float:
    """Exponential in-out. :math:`f(t) = 2^t`"""
    t *= 2
    if t < 1:
        return 2 ** (10 * t - 11)
    return 1 - 2 ** (9 - 10 * t)


def bounce_in(t: float) -> float:
    """Bounce in, amplitude of bounce increases."""
    return 1 - bounce_out(1 - t)


def bounce_out(t: float) -> float:
    """Bounce out, amplitude of bounce decreases."""
    if t < 1 / 2.75:
        return 7.5625 * t * t
    if t < 2 / 2.75:
        return 7.5625 * (t - 1.5 / 2.75) ** 2 + 0.75
    if t < 2.5 / 2.75:
        return 7.5625 * (t - 2.25 / 2.75) ** 2 + 0.9375
    return 7.5625 * (t - 2.625 / 2.75) ** 2 + 0.984375


def bounce_inout(t: float) -> float:
    """Bounce in-out, amplitude of bounce increases and then decreases."""
    if t < 0.5:
        return (1 - bounce_out(1 - 2 * t)) * 0.5
    return (1 + bounce_out(2 * t - 1)) * 0.5


def bezier(x1: float, y1: float, x2: float | None = None, y2: float | None = None, /) -> Callable[[float], float]:
    """
    Create a cubic bezier easing function from one or two control points. The curve starts at (0, 0) and ends at (1, 1).
    """
    if x2 is None:
        x1 *= 2 / 3
        y1 *= 2 / 3
        x2 = x1 + 1 / 3
        y2 = y1 + 1 / 3
    cubic = skia.CubicMap((x1, y1), (x2, y2))  # type: ignore y2 should never be None
    return cubic.computeYFromX


def get_quadish(amount: float) -> Callable[[float], float]:
    """
    Create a quadratic easing function with a given amount of ease. -1 is ease in, 0 is linear, 1 is ease out. Other
    values gives something in between.
    """
    if amount < -1:
        amount = -1
    if amount > 1:
        amount = 1
    return lambda t: t * (1 + (1 - t) * amount)


def get_pow_in(n: float) -> Callable[[float], float]:
    """Create a power in easing function with power *n*. :math:`f(t) = t^n`"""
    return lambda t: t**n


def get_pow_out(n: float) -> Callable[[float], float]:
    """Create a power out easing function with power *n*. :math:`f(t) = t^n`"""
    return lambda t: 1 - (1 - t) ** n


def get_pow_inout(n: float) -> Callable[[float], float]:
    """Create a power in-out easing function with power *n*. :math:`f(t) = t^n`"""

    def f(t: float) -> float:
        t *= 2
        if t < 1:
            return t**n * 0.5
        return 1 - abs((2 - t) ** n) * 0.5

    return f


def get_back_in(amount: float) -> Callable[[float], float]:
    """Create a back in easing function with a given amount of overshoot."""
    return lambda t: t * t * ((amount + 1) * t - amount)


def get_back_out(amount: float) -> Callable[[float], float]:
    """Create a back out easing function with a given amount of overshoot."""

    def f(t: float) -> float:
        t -= 1
        return t * t * ((amount + 1) * t + amount) + 1

    return f


def get_back_inout(amount: float) -> Callable[[float], float]:
    """Create a back in-out easing function with a given amount of overshoot."""

    def f(t: float) -> float:
        t *= 2
        if t < 1:
            return t * t * ((amount + 1) * t - amount) * 0.5
        t -= 2
        return t * t * ((amount + 1) * t + amount) * 0.5 + 1

    return f


def get_elastic_in(amplitude: float, period: float) -> Callable[[float], float]:
    """Create an elastic in easing function with a given amplitude and period."""
    asin = math.asin(1 / amplitude)
    period = _TWO_PI / period

    def f(t: float) -> float:
        if t == 0 or t == 1:
            return t
        t -= 1
        return -amplitude * 2 ** (10 * t) * math.sin(t * period - asin)

    return f


def get_elastic_out(amplitude: float, period: float) -> Callable[[float], float]:
    """Create an elastic out easing function with a given amplitude and period."""
    asin = math.asin(1 / amplitude)
    period = _TWO_PI / period

    def f(t: float) -> float:
        if t == 0 or t == 1:
            return t
        return amplitude * 2 ** (-10 * t) * math.sin(t * period - asin) + 1

    return f


def get_elastic_inout(amplitude: float, period: float) -> Callable[[float], float]:
    """Create an elastic in-out easing function with a given amplitude and period."""
    asin = math.asin(1 / amplitude)
    period = _TWO_PI / period

    def f(t: float) -> float:
        t = t * 2 - 1
        if t < 0:
            return -0.5 * amplitude * 2 ** (10 * t) * math.sin(t * period - asin)
        return amplitude * 2 ** (-10 * t) * math.sin(t * period - asin) * 0.5 + 1

    return f


def repeat(f: Callable[[float], float]) -> Callable[[float], float]:
    """Create an easing function that repeats/appends the given function.

    .. plot::

        import animator as am
        x = np.linspace(0, 1, 100)
        plt.plot(x, np.vectorize(am.easing.cubic_inout)(x), label="original")
        plt.plot(x, np.vectorize(am.easing.repeat(am.easing.cubic_inout))(x), label="repeated")
        plt.legend()
        plt.tight_layout()
        plt.show()
    """
    return lambda t: (f(2 * t) if t < 0.5 else f(2 * t - 1) + 1) * 0.5


def reflect(f: Callable[[float], float]) -> Callable[[float], float]:
    """Create an easing function that reflects the given function.

    .. plot::

        import animator as am
        x = np.linspace(0, 1, 100)
        plt.plot(x, np.vectorize(am.easing.cubic_inout)(x), label="original")
        plt.plot(x, np.vectorize(am.easing.reflect(am.easing.cubic_inout))(x), label="reflected")
        plt.legend()
        plt.tight_layout()
        plt.show()
    """
    return lambda t: f(2 * (t if t < 0.5 else 1 - t))


def nested(*f: Callable[[float], float]) -> Callable[[float], float]:
    """Create an easing function that applies the given functions in sequence.

    >>> nested(f1, f2, f3, ...)(t) == f3(f2(f1(t)))...
    """

    def nester(t: float) -> float:
        for f_ in f:
            t = f_(t)
        return t

    return nester


quad_in = get_pow_in(2)  #: Quadratic (degree 2) in easing function. :math:`f(t) = t^2`
quad_out = get_pow_out(2)  #: Quadratic (degree 2) out easing function. :math:`f(t) = t^2`
quad_inout = get_pow_inout(2)  #: Quadratic (degree 2) in-out easing function. :math:`f(t) = t^2`
cubic_in = get_pow_in(3)  #: Cubic (degree 3) in easing function. :math:`f(t) = t^3`
cubic_out = get_pow_out(3)  #: Cubic (degree 3) out easing function. :math:`f(t) = t^3`
cubic_inout = get_pow_inout(3)  #: Cubic (degree 3) in-out easing function. :math:`f(t) = t^3`
quart_in = get_pow_in(4)  #: Quartic (degree 4) in easing function. :math:`f(t) = t^4`
quart_out = get_pow_out(4)  #: Quartic (degree 4) out easing function. :math:`f(t) = t^4`
quart_inout = get_pow_inout(4)  #: Quartic (degree 4) in-out easing function. :math:`f(t) = t^4`
quint_in = get_pow_in(5)  #: Quintic (degree 5) in easing function. :math:`f(t) = t^5`
quint_out = get_pow_out(5)  #: Quintic (degree 5) out easing function. :math:`f(t) = t^5`
quint_inout = get_pow_inout(5)  #: Quintic (degree 5) in-out easing function. :math:`f(t) = t^5`
back_in = get_back_in(1.70158)  #: Back in easing function.
back_out = get_back_out(1.70158)  #: Back out easing function.
back_inout = get_back_inout(1.70158)  #: Back in-out easing function.
elastic_in = get_elastic_in(1, 0.3)  #: Elastic in easing function.
elastic_out = get_elastic_out(1, 0.3)  #: Elastic out easing function.
elastic_inout = get_elastic_inout(1, 0.45)  #: Elastic in-out easing function.


def _plot_easing_functions(f: Callable[[float], float], start: float = 0, end: float = 1, num: int = 1000) -> None:
    """Plot the given easing function from *start* to *end* with *num* points."""
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.linspace(start, end, num)
    plt.plot(x, np.vectorize(f)(x))
    plt.show()
