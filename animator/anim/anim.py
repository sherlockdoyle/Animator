"""Animations!"""
from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from animator.anim.easing import EaseFunc, cubic_inout

if TYPE_CHECKING:
    from animator.scene import Scene


class Anim:
    class Duration:
        """Special duration values."""

        INFINITE = -1  #: The animation will run indefinitely.
        INDEFINITE = -2  #: The animation will run indefinitely until explicitly stopped.

    class _State(Enum):
        """The state of an animation."""

        IDLE = 0  #: The animation has not started.
        RUNNING = 1  #: The animation is running.
        FINISHED = 2  #: The animation has finished.
        # PAUSED = 3  #: The animation is paused.

    def __init__(self, duration: float, ease: EaseFunc = cubic_inout) -> None:
        """
        :param duration: The duration of the animation in seconds. Negative values have
        :param ease_func: The easing function to use for the animation.
        """
        self._duration: float = duration
        self.ease_func: EaseFunc = ease

        # self._reversing: bool = False
        self._start_frame: int = 0
        self._num_frames: int = 0
        self._state: Anim._State = Anim._State.IDLE
        self._scene: Scene = None  # type: ignore lateinit

    def _mount(self, scene: Scene, start_frame: int) -> None:
        self._scene = scene
        self._start_frame = start_frame
        self._num_frames = -1 if self._duration < 0 else round(self._duration * self._scene.fps)

    def start(self) -> None:
        """Called once before the animation starts. Do any setup here."""
        pass

    def update(self, t: float) -> None:
        """Called every frame with the time since the animation started.

        :param t: Interpolated time since the animation started. This will be 0 at the start of the animation and 1 at
          the end. Undefined behavior if the animation is infinite.
        """
        pass

    def end(self) -> None:
        """Called once after the animation ends. Do any cleanup here and make sure to set the final state."""
        pass

    def stop(self) -> None:
        """Stop the animation manually."""
        self._state = Anim._State.FINISHED
