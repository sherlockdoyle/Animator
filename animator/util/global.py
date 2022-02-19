"""Functions that exists across the whole library."""
import time


def set_random_seed(seed: int = 42) -> None:
    """Set the random *seed* for the library. This should be called just after importing **animator**.

    :param seed: The seed to use.
    """
    import random
    import numpy
    random.seed(seed)
    numpy.random.seed(seed)


__oldtime: float = 0


def delta_time() -> float:
    """Return the time in seconds since the last call to this function."""
    global __oldtime
    newtime = time.time()
    dt = newtime - __oldtime
    __oldtime = newtime
    return dt
