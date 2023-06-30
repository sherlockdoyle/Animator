"""Display manager manages the display of a scene. Multiple display managers are available, and the scene can
automatically choose the best one."""
from __future__ import annotations

from abc import abstractmethod
from contextlib import AbstractContextManager
from time import time
from typing import TYPE_CHECKING, Any, Type

if TYPE_CHECKING:
    from animator.scene import Scene


class DisplayManager(AbstractContextManager):
    """Base class for display managers. A display manager manages the display of a scene."""

    display_method: str | None = None

    def __init__(self, scene: Scene, delay: float | None = None) -> None:
        """Manages the display of a scene.

        :param scene: The scene to display.
        :param delay: The delay between frames. If ``None``, the delay will be calculated from the scene's fps.
        """
        self.scene: Scene = scene
        self.width: int = scene.frame.shape[1]
        self.height: int = scene.frame.shape[0]
        self.delay: float = delay or 1 / scene.fps

        self.winname: str = f'Scene_{id(scene)}'
        self.running: bool = True
        self.__oldtime: float = time()

    def waittime(self) -> float:
        """Returns the time to wait until the next frame should be displayed in seconds. This will be at least 0.001
        seconds."""
        newtime = time()
        waittime = max(self.__oldtime + self.delay - newtime, 0.001)
        self.__oldtime = newtime
        return waittime

    @abstractmethod
    def show_frame(self) -> bool:
        """Displays the current frame and returns ``True``. If the window was closed, returns ``False``."""
        pass

    def close(self) -> None:
        """Closes the :class:`DisplayManager`."""
        pass

    def __exit__(self, __exc_type: Any, __exc_value: Any, __traceback: Any) -> None:
        self.close()

    @classmethod
    def get_best(cls) -> Type[DisplayManager]:
        """Returns the best available :class:`DisplayManager`."""
        if cls.display_method:
            for subclass in cls.__subclasses__():
                if subclass.__name__.endswith(cls.display_method):
                    return subclass
        raise RuntimeError('No display method available.')
