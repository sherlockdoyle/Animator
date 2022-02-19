"""Environment related utilities."""
import os
import sys


def inside_ipython() -> bool:
    """Check if we are running inside IPython."""
    try:
        get_ipython()
        return True
    except NameError:
        return False


def inside_ipython_notebook() -> bool:
    """Check if we are running inside IPython/Jupyter notebook."""
    try:
        return 'zmqshell' in str(type(get_ipython()))
    except NameError:
        return False


def get_path(path: str, mkdir: bool = False) -> str:
    """Takes a relative or absolute *path* and returns the absolute path. If the path is relative, it will be
    resolved relative to the current working directory. If the path is absolute, it will be returned as is. If
    *mkdir* is ``True``, and the directory in the path does not exist, it will be created.

    :param path: The path to resolve.
    :param mkdir: If ``True``, and the directory in the path does not exist, it will be created.
    """
    path = os.path.normpath(os.path.join(os.getcwd() if inside_ipython() else os.path.dirname(sys.argv[0]), path)) + (
        os.sep if path.endswith(os.sep) else '')
    if mkdir:
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)
    return path
