"""Environment related utilities."""


def inside_ipython() -> bool:
    """Return ``True`` if the code is running inside IPython."""
    try:
        __IPYTHON__
        return True
    except NameError:
        return False


def inside_notebook() -> bool:
    """Return ``True`` if the code is running inside IPython/Jupyter notebook."""
    try:
        return 'zmqshell' in str(type(get_ipython()))
    except NameError:
        return False
