"""Animations!"""
from __future__ import annotations

from typing import TYPE_CHECKING

from animator.anim.anim import Anim

if TYPE_CHECKING:
    from animator.scene import Scene


class AnimationManager:
    """
    An :class:`AnimationManager` manages a collection of :class:`Anim`ations. It handles the starting, stopping and
    progressing of the animations.

    1. Ideally, the manager will call :meth:`Anim.start` when it is ready to start the animation. For animations with 0
       duration, the :meth:`Anim.start` and :meth:`Anim.end` will be called during the same frame after all other ends
       have been called; :meth:`Anim.update` will never be called.
    2. Then it will call :meth:`Anim.update` with the appropriate interpolated time. The time will already be eased with
       the animation's easing function. Note that :meth:`Anim.update` will not be called for the first (usually with 0)
       and last (usually with 1) frames of the animation. This is because the first frame is the default and should not
       be updated. The last frame is the final frame and should be handled by :meth:`Anim.end`.
    3. The manager will also call :meth:`Anim.end` when the animation is done. All :meth:`Anim.end` for a certain frame
       will be called before any :meth:`Anim.start` for that frame. This is to ensure that any consecutive animations
       that depends on the same resource will receive the updated resource. Note that, :meth:`Anim.end` will not be
       called for infinite animations. Infinite animations may set their ``_state`` to ``FINISHED`` to end the animation
       or call :meth:`Anim.stop`.
    """

    def __init__(self, scene: Scene) -> None:
        self._scene: Scene = scene
        self._animations: set[Anim] = set()
        self._current_frame: int = 0

        self.__current_start_frame: int = 0
        self.__max_num_frames: int = 0

    def add(self, anim: Anim, start_time: float | None = None, start_frame: int | None = None) -> None:
        """
        Add an *anim*ation from the given *start_time* or *start_frame*. If neither are given, the animation will start
        time will be determined by an internal marker. Multiple call to this method without the time or frame will add
        the animations at the same marker. To progress the marker, call :meth:`wait`.
        """
        self._animations.add(anim)
        if start_frame is None:
            if start_time is None:
                anim._mount(self._scene, self.__current_start_frame)
                # max will handle negative num_frames
                self.__max_num_frames = max(self.__max_num_frames, anim._num_frames)
                return
            else:
                start_frame = round(start_time * self._scene.fps)
        anim._mount(self._scene, start_frame)

    def wait(self, time: float | None = None, frames: int | None = None) -> None:
        """
        Wait for the given *time* or *frames*. This method will also progress the internal marker so that any new
        animations added will start after this wait. If neither *time* nor *frames* are given, just the marker will be
        progressed.
        """
        if frames is None:
            frames = 0 if time is None else round(time * self._scene.fps)
        self.__current_start_frame += self.__max_num_frames + frames
        self.__max_num_frames = 0

    def _update_marker(self) -> None:
        """Update the internal marker to the current frame so that new animations will start after this."""
        self.__current_start_frame = self._current_frame
        self.__max_num_frames = 0

    def __contains__(self, anim: Anim) -> bool:
        return anim in self._animations

    def _handle_end(self) -> None:
        """Handle animations that are going to end."""
        duration_0: set[Anim] = set()
        to_remove: set[Anim] = set()
        for anim in self._animations:
            if anim._num_frames == 0 and anim._start_frame == self._current_frame:  # 0 duration, handle later
                duration_0.add(anim)
            elif (
                anim._num_frames > 0 and anim._start_frame + anim._num_frames == self._current_frame
            ) or anim._state == Anim._State.FINISHED:  # also end if already marked as finished
                anim._state = Anim._State.FINISHED
                anim.end()
                to_remove.add(anim)
        self._animations -= to_remove

        for anim in duration_0:
            anim.start()
            anim._state = Anim._State.FINISHED
            anim.end()
        self._animations -= duration_0

    def _handle_progress(self) -> None:
        """Start or update animations that are going to progress."""
        for anim in self._animations:
            if anim._start_frame == self._current_frame:
                anim.start()
                anim._state = Anim._State.RUNNING
            elif anim._start_frame < self._current_frame:
                if anim._num_frames < 0:  # infinite
                    anim.update(-1)
                else:
                    anim.update(anim.ease_func((self._current_frame - anim._start_frame) / anim._num_frames))
        self._current_frame += 1

    def _is_pending(self) -> bool:
        """Check if any animations are left to run."""
        return (
            any(a._duration != Anim.Duration.INFINITE for a in self._animations)
            or self._current_frame < self.__current_start_frame + self.__max_num_frames  # internal marker is pending
        )

    def update(self) -> bool:
        """
        Update the animation manager. The scene will call this method once every frame. Returns ``True`` if animations
        are left to run, ``False`` otherwise.
        """
        if self._animations:
            self._handle_end()
            self._handle_progress()
            return self._is_pending()
        return False
