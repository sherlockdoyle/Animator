"""This module contains some simple animations."""
from __future__ import annotations

__all__ = 'Wait', 'FuncAnim', 'Once'

from typing import Callable, Any

from .anim import Anim


class Wait(Anim):
    """Wait for a given amount of time."""

    def __init__(self, duration: float):
        """
        :param duration: The amount of time to wait in seconds.
        """
        super().__init__(duration)


class FuncAnim(Anim):
    """Uses a function to do the updates for the animation."""

    def __init__(self, f: Callable[[float], bool | None], start_func: Callable[[], None] | None = None,
                 end_func: Callable[[], None] | None = None, *args: Any, **kwargs: Any):
        """
        :param f: The function to use to update the animation. The function takes a single float argument,
            the current interpolation value. The fight might return an optional boolean value, which can be used to
            keep the animation running as long as it returns ``True``. In this, the *duration* of the animation is
            ignored.
        :param start_func: The function to call when the animation starts.
        :param end_func: The function to call when the animation ends.
        """
        super().__init__(*args, **kwargs)
        self.update_func: Callable[[float], bool | None] = f
        self.start_func: Callable[[], None] | None = start_func
        self.end_func: Callable[[], None] | None = end_func

    def start(self) -> None:
        if self.start_func is not None:
            self.start_func()

    def update(self) -> None:
        if self.update_func(self.t):
            self.n_frames = self.duration = 0

    def end(self) -> None:
        if self.end_func is not None:
            self.end_func()


class Once(Anim):
    """An animation that runs a function once."""

    def __init__(self, f: Callable[[], None]):
        """
        :param f: The function to call when the animation starts.
        """
        super().__init__(duration=0)
        self.func: Callable[[], None] = f

    def start(self) -> None:
        self.func()
