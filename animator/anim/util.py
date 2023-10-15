"""Animation utilities."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Generator

from animator.anim.anim import Anim
from animator.anim.manager import AnimationManager

if TYPE_CHECKING:
    from animator.entity import Entity

    EntityOrAnim = Entity | Anim
    YieldType = EntityOrAnim | tuple[EntityOrAnim, ...]
    ReturnType = Generator[YieldType, None, None]

FuncAnimFunc = Callable[[], bool | None]


class FuncAnim(Anim):
    """Animate by calling a function on each frame."""

    def __init__(self, func: FuncAnimFunc) -> None:
        """
        :param func: The function to call. If it returns ``True``, the animation will stop.
        """
        super().__init__(Anim.Duration.INDEFINITE)
        self.__func: FuncAnimFunc = func

    def start(self) -> None:
        if self.__func():
            self._state = Anim._State.FINISHED

    def update(self, t: float) -> None:
        if self.__func():
            self._state = Anim._State.FINISHED


SyncedAnimFunc = Callable[[], 'ReturnType']


class SyncedAnim(Anim):
    """
    Animate by calling a generator function which yields the animations. This can be used to create animations that may
    depend on the result of earlier animations. The generator may also yield entities, which will be added to the scene.

    ..example::
    def f():...
    """

    def __init__(self, func: SyncedAnimFunc, **kwargs: Any) -> None:
        super().__init__(Anim.Duration.INDEFINITE, **kwargs)
        self.__func: SyncedAnimFunc = func
        self.__generator: ReturnType = None  # type: ignore lateinit
        self.__animation_manager: AnimationManager = None  # type: ignore lateinit

    def start(self) -> None:
        self.__generator = self.__func()
        self.__animation_manager = AnimationManager(self._scene)
        self.step()

    def update(self, t: float) -> None:
        self.step()

    def step(self) -> None:
        self.__animation_manager._handle_end()
        if not self.__animation_manager._is_pending():
            try:
                objs = next(self.__generator)
            except StopIteration:
                self._state = Anim._State.FINISHED
                return
            if not isinstance(objs, tuple):
                objs = (objs,)
            self.__animation_manager._update_marker()  # update the internal marker to the current frame
            for obj in objs:
                if isinstance(obj, Anim):
                    self.__animation_manager.add(obj)
                else:
                    self._scene.add(obj)
        self.__animation_manager._handle_progress()


class Wait(Anim):
    """Simple do nothing animation that waits for the given *duration*."""

    pass


class Once(Anim):
    """Single frame animation that calls the given function."""

    def __init__(self, func: Callable, **kwargs: Any) -> None:
        super().__init__(0, **kwargs)
        self.__func: Callable = func

    def start(self) -> None:
        self.__func()
