from typing import TYPE_CHECKING

from animator.extras.more_path import Arrow as Arrow
from animator.extras.more_path import Ring as Ring
from animator.extras.plot import Plot as Plot


def __get_import_error_placeholder(err: ImportError) -> type:
    class __ImportErrorPlaceholder:
        def __init__(self, *args, **kwargs):
            raise err

    return __ImportErrorPlaceholder


try:
    from animator.extras.code import Code as Code
except ImportError as __err:
    if not TYPE_CHECKING:  # ignore dummy class from type checker
        Code = __get_import_error_placeholder(__err)

try:
    from animator.extras.mpl import Mpl as Mpl
except ImportError as __err:
    if not TYPE_CHECKING:
        Mpl = __get_import_error_placeholder(__err)
