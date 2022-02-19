from __future__ import annotations

__all__ = 'AnimationManager', 'Anim', 'AnimCollection'

import enum
from collections import deque
from typing import Callable, List, Type, TYPE_CHECKING, Dict, Any, Iterable

from .easing import cubic_inout

if TYPE_CHECKING:
    from ..scene.scene import Scene
    from ..entity.entity import Entity


class AnimationManager:
    """The :class:`AnimationManager` class handles and updates all animations. It keeps track of the animations,
    their duration, running time, etc. Every :class:`AnimationManager` is bound to a :class:`Scene` and tracks the
    animations for that *scene*.

    Animations can be added to the animation manager either at a specified time or automatically based on an internal
    marker. The marker can be updated with :meth:`wait`.

    >>> manager.add(Anim(1))  # add an animation of 1 second, anim1
    >>> manager.add(Anim(2), start_time=0.5) # add an animation of 2 seconds, anim2, from half a second
    >>> manager.wait(1)  # add an wait for 1 second and update internal marker
    >>> manager.add(Anim(1))  # add an animation of 1 second, anim3
    >>> manager.add(Anim(2))  # add an animation of 2 seconds, anim4
    >>> manager.wait()  # just update the internal marker without any wait (wait for 0 seconds)
    >>> manager.add(Anim(2), start_time=1.5)  # add an animation of 2 seconds, anim5, from 1.5 seconds
    >>> manager.add(Anim(1))  # anim6
    The above example will make the following animation sequence,
    |<-1 sec->|---------|---------|---------|---------|
    |--anim1--|--wait---|--anim3--|         |--anim6--|
                        |-------anim4-------|
         |-------anim2-------|              V
                   |-------anim5-------|   wait

    :ivar frame_count: Number of frames passed, number of times updated.
    :ivar running: Whether the animation manager is running or not, ie. if calling :meth:`update` will update the animations.
    """

    class After:
        """Convenience class for chaining animations one after another."""

        def __init__(self, manager: AnimationManager, frame: int):
            self.manager = manager
            self.start_frame = frame

        def then(self, *anims: Anim, end_time: float = None, end_frame: int = None) -> AnimationManager.After:
            """Add animations to the animation manager after this animation.

            :param anims: The animations to add.
            :param end_time: The time to end the animation at.
            :param end_frame: The frame to end the animation at.
            """
            if isinstance(anims[0], tuple):
                anims = anims[0]
            afters: List[AnimationManager.After] = [
                self.manager.add(anim, start_frame=self.start_frame, end_time=end_time, end_frame=end_frame) for anim in
                anims]
            return max(afters, key=lambda a: a.start_frame)

        __radd__ = __add__ = then

    def __init__(self, scene: Scene):
        """Initializes and binds the animation manager to a *scene*."""
        self.anims: Dict[Anim, int] = {}
        self.frame_count = 0
        self.running = False
        self.scene = scene
        self.__cur_start_frame = 0
        self.__max_frame_len = 0

    def add(self, anim: Anim, start_time: float | None = None, end_time: float | None = None,
            start_frame: int | None = None, end_frame: int | None = None) -> After | None:
        """Adds an animation *anim* to the animation manager which will start at *start_time* or *start_frame*. An
        optional *end_time* or *end_frame* can be specified to indicate the duration of the animation and will
        override the animation's original duration.

        The ``..._time`` parameters specifies the values in seconds, are irrespective of the scene's FPS,
        and will override the ``..._frame`` parameters, if provided. If neither is specified, the animation is added
        at a time specified by an internal marker. The marker can be changed with :meth:`wait`.

        :param anim: The animation to add.
        :param start_time: The time to start the animation at.
        :param start_frame: The frame to start the animation at.
        :param end_time: The time to end the animation at.
        :param end_frame: The frame to end the animation at.
        :return: The :class:`After` object which can be used to chain animations.
        """
        anim.scene = self.scene
        anim._manager = self
        if start_time is not None:
            start_frame = round(start_time * self.scene.fps)
        if end_time is not None:
            end_frame = round(end_time * self.scene.fps)
        update_max = False
        if start_frame is None:
            start_frame = self.__cur_start_frame
            update_max = True

        if isinstance(anim.duration, Anim.InfiniteDuration):
            self.anims[anim] = start_frame
            anim.n_frames = -1
            return None  # terminate early, chained animations are not supported

        if end_frame is None:
            anim.n_frames = round(anim.duration * self.scene.fps)
        else:
            anim.n_frames = end_frame - start_frame
            anim.duration = anim.n_frames / self.scene.fps

        if update_max:
            self.__max_frame_len = max(self.__max_frame_len, anim.n_frames)
        self.anims[anim] = start_frame
        return AnimationManager.After(self, start_frame + anim.n_frames)

    def wait(self, time: float, frame: int = 0) -> None:
        """Waits for *time* seconds or *frame* frames (*frame* is ignored if *time* is specified). If neither is
        specified, the wait is of 0 seconds.

        This updates an internal marker that is used to add un-timed animations. Originally the marker is at 0,
        and every time this method is called, the marker is moved forward by ``max(duration of all un-timed
        animations added since the last marker update) + time of this wait``.

        :param time: The time to wait in seconds.
        :param frame: The number of frames to wait.
        """
        if time is not None:
            frame = round(time * self.scene.fps)
        self.__cur_start_frame += self.__max_frame_len + frame
        self.__max_frame_len = 0

    def start(self) -> None:
        """Starts the animations. Called before :meth:`update`."""
        self.running = True

    def pause(self) -> None:
        """Pauses the animations. Can be resumed with :meth:`start`."""
        self.running = False

    def update(self) -> bool:
        """Starts (at the required time) and updates (by one frame) each of the animations. Returns ``True`` if more
        updates are possible. Finished animations are removed and ``False`` is returned when no more animations are
        left.

        :note: Infinite animations will never end and will never be removed. If any infinite animations are present,
            this method will never return ``False``.
        """
        num_alongside = 0  # number of animations that are running alongside others
        if self.running:
            finished = []
            for anim, start_frame in self.anims.items():
                if anim.duration == Anim.InfiniteDuration.ALONGSIDE:
                    num_alongside += 1

                if self.frame_count == start_frame:
                    anim.start()
                    anim.state = Anim.State.RUNNING

                if self.frame_count >= start_frame:
                    anim.update()
                    anim.frame_count += 1
                    if self.frame_count >= start_frame + anim.n_frames and not isinstance(anim.duration,
                                                                                          Anim.InfiniteDuration):
                        finished.append(anim)

            for anim in finished:  # remove finished animations
                anim.end()
                anim.state = Anim.State.FINISHED
                del self.anims[anim]

            self.frame_count += 1
        return len(self.anims) > num_alongside or self.frame_count <= self.__cur_start_frame

    def __contains__(self, anim: Anim) -> bool:
        """Returns whether the animation manager contains the animation *anim*."""
        return anim in self.anims


class AnimCollector:
    def __init__(self, *anim_classes: Type[Anim]):
        self.anim_classes: List[Type[Anim]] = list(anim_classes)

    def __add__(self, other: Type[Anim] | AnimCollector) -> AnimCollector:
        if isinstance(other, AnimCollector):
            self.anim_classes.extend(other.anim_classes)
        else:
            self.anim_classes.append(other)
        return self

    __iadd__ = __add__

    def __call__(self, *args: Any, duration: float = None, **kwargs: Any) -> AnimCollection:
        return AnimCollection(*(anim_class(*args, duration=duration, **kwargs) for anim_class in self.anim_classes),
                              duration=duration, delay_ratio=0)


class AnimAdder(type):
    def __add__(self, other: Type[Anim]) -> AnimCollector:
        return AnimCollector(self, other)

    __radd__ = __add__


class Anim(metaclass=AnimAdder):
    """:class:`Anim` is the base class for all animations. It defines an animation which runs for *duration* seconds
    and uses the *func* interpolation function. The *duration* can be an instance of :class:`Anim.Duration` for
    special behavior. For such cases ``Anim.t`` will be undefined.

    :ivar duration: The duration of the animation, in seconds.
    :ivar f: The interpolation function.
    :ivar frame_count: Number of frames (times) the animation has been updated.
    :ivar n_frames: Total number of frames (times) the animation must run.
    :ivar entities: Holds the entities which will be animated.
    """

    class State(enum.Enum):
        """The state of the animation."""
        NOT_STARTED = 0
        RUNNING = 1
        FINISHED = 2
        PAUSED = 3

    class InfiniteDuration(enum.IntEnum):
        """Special duration values which allow the animation to run indefinitely (:meth:`Anim.end` won't be called)."""
        INFINITE = -1
        """Runs indefinitely. This will cause the animation loop to never stop."""
        ALONGSIDE = -2
        """Runs the animation as long as other animations are running. Will stop when all animations are finished."""

    duration: float = 1
    """The default duration for animations."""

    def __init__(self, duration: float | InfiniteDuration | None = None,
                 ease_func: Callable[[float], float] = cubic_inout):
        """
        :param duration: The duration of the animation, in seconds. If ``None``, the default duration is used,
            which can be set by :attr:`Anim.duration`.
        :param ease_func: The interpolation function.
        """
        if duration is not None:
            self.duration: float | Anim.InfiniteDuration = duration
        self.f: Callable[[float], float] = ease_func
        self.frame_count: int = 0
        self.entities: List[Entity] = []
        self.n_frames: int = None
        self.state: Anim.State = Anim.State.NOT_STARTED
        self.scene: Scene = None
        self._manager: AnimationManager = None

    @property
    def t(self) -> float:
        """The current interpolation value. This is between 0 and 1."""
        return self.f(max(0.0, min(self.frame_count / self.n_frames, 1.0)))

    def start(self) -> None:
        """This method is called once, when the animation is started. Do necessary initialization here."""
        pass

    def update(self) -> None:
        """This method is called every frame, when the animation is running."""
        pass

    def end(self) -> None:
        """This method is called once, when the animation is finished. Do necessary cleanup here."""
        pass


class AnimCollection(Anim, AnimationManager):
    """Class to handle a collection of animations of same duration each, and all running at once, with some
    incremental delay, or one after another."""

    def __init__(self, *anims: Anim, duration: float | None = None, anim_duration: float | None = None,
                 delay_ratio: float | None = None):
        """
        :param anims: The animations to run.
        :param duration: The duration of the collection, in seconds. If ``None``, the default duration is used,
            which can be set by :attr:`Anim.duration`. If both ``duration`` and ``anim_duration`` are specified,
            ``duration`` takes precedence. If one of the two is ``None``, the other is used to calculate the value.
        :param anim_duration: The duration for each of the animations, in seconds.
        :param delay_ratio: The amount delay between the animations. A value of 0 means all animations start and end
            together, while a value of 1 means all animations start and end one after another. Values between 0 and 1
            will cause the animations to be overlapped with some offset.
        """
        if not anims:
            raise ValueError('No animations specified.')
        if delay_ratio is None:
            delay_ratio = 0.5 / len(anims)

        if duration is None:
            if anim_duration is None:
                duration = Anim.duration
                anim_duration = 1 / ((len(anims) - 1) * delay_ratio + 1)
            else:
                duration = anim_duration + (len(anims) - 1) * anim_duration * delay_ratio
        else:
            anim_duration = duration / ((len(anims) - 1) * delay_ratio + 1)

        Anim.__init__(self, duration=duration)
        AnimationManager.__init__(self, None)  # type: ignore
        del self.__max_frame_len
        self._anim_list = anims
        for a in anims:
            self.entities.extend(a.entities)
        self.anim_duration = anim_duration

    @classmethod
    def distributed(cls, anim_class: Type[Anim], entity: Entity, levels: int | slice | Iterable[int] = 1,
                    duration: float | None = None) -> AnimCollection:
        """Convenience method to create a collection of animations of type *anim_class* that applies to the children
        of the given *entity* (children in the specified *levels*), with the given *duration*.

        :param anim_class: The class of the animation to create.
        :param entity: The entity whose children to use.
        :param levels: The levels to use. 0 means the entity itself, 1 means its children, etc. A slice or iterable
            can be used to specify multiple levels.
        :param duration: The duration of the collective animation, in seconds. If ``None``, the default duration is
            used, which can be set by :attr:`Anim.duration`.
        """
        if isinstance(levels, int):
            levels = {levels}
        elif isinstance(levels, slice):
            levels = range(*levels.indices(1024))  # deep enough
        elif not isinstance(levels, range):  # range.__contains__() is fast
            levels = set(levels)

        anims: List[Anim] = []
        q = deque([(entity, 0)])
        while q:
            ent, level = q.pop()
            if level in levels:
                anims.append(anim_class(ent))
            for e in ent.entities:
                q.appendleft((e, level + 1))

        collection = cls(*anims, duration=duration, delay_ratio=0)
        collection.entities.clear()
        collection.entities.append(entity)
        return collection

    def add(self) -> None:
        raise NotImplementedError('Cannot add to a collection.')

    def wait(self) -> None:
        raise NotImplementedError('Cannot wait on a collection.')

    def pause(self) -> None:
        raise NotImplementedError('Cannot pause a collection.')

    def start(self) -> None:
        AnimationManager.start(self)
        delay = 0.0 if len(self._anim_list) == 1 else (self.duration - self.anim_duration) / (len(self._anim_list) - 1)
        for i, anim in enumerate(self._anim_list):
            anim.scene = self.scene
            anim._manager = self._manager
            anim.duration = self.anim_duration
            anim.n_frames = round(anim.duration * self.scene.fps)
            self.anims[anim] = round(delay * i * self.scene.fps)
        del self._anim_list

    def update(self) -> None:
        AnimationManager.update(self)
        self.frame_count -= 1  # frame_count is updated twice, once from the parent class and once from the manager

    def end(self) -> None:
        for anim in self.anims:
            anim.end()
            anim.state = Anim.State.FINISHED
        self.anims.clear()
