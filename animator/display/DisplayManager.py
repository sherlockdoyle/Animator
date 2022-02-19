"""The base class that handle the display and saving for animator. These display classes are automatically generated
by a :class:`Scene` as necessary. """
from __future__ import annotations

import contextlib
import time
from typing import TYPE_CHECKING, Any, Type

if TYPE_CHECKING:
    from ..scene.scene import Scene


class DisplayManager(contextlib.AbstractContextManager):
    """Base class for managing windows for displaying scenes."""
    display_method: str | None = None

    def __init__(self, scene: Scene, delay: float | None = None):
        """Attach the display manager to the *scene*, with an optional *delay* in seconds.

        :param scene: The scene to display.
        :param delay: The delay between frames. The default is to calculate the delay from the scene's fps.
        """
        self.scene: Scene = scene
        self.width: int = scene.frame.shape[1]
        self.height: int = scene.frame.shape[0]
        self.delay: float = 1 / scene.fps if delay is None else delay
        self.winname: str = f'Scene_{id(scene)}'
        self.running: bool = True
        self.__oldtime: float = time.time()

    def waittime(self) -> float:
        """Returns the time to wait for the next frame. Will be at least 0.001 (1ms)."""
        newtime = time.time()
        waittime = max(self.delay + self.__oldtime - newtime, 0.001)
        self.__oldtime = newtime
        return waittime

    def show_frame(self) -> bool:
        """Displays the current frame and returns ``True``. Returns ``False`` if the window was closed."""
        pass

    def close(self) -> None:
        """Closes the :class:`DisplayManager`."""
        pass

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    @classmethod
    def get_best(cls) -> Type[DisplayManager]:
        """Returns the best :class:`DisplayManager` for the current system."""
        for manager in cls.__subclasses__():
            if manager.__name__.endswith(cls.display_method):
                return manager
        raise RuntimeError('No suitable display method available.')
