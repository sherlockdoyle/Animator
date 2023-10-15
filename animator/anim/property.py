from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, TypeVar

from animator import skia
from animator.anim.anim import Anim

if TYPE_CHECKING:
    from animator.entity import Entity

__DT = TypeVar('__DT', int, float, skia.Point)


class __Interpolator(Generic[__DT]):
    def interpolate(self, initial: __DT, diff: __DT, t: float) -> __DT:
        raise NotImplementedError


class __IntInterpolator(__Interpolator[int]):
    def interpolate(self, initial: int, diff: int, t: float) -> int:
        return round(initial + diff * t)


__FPT = TypeVar('__FPT', float, skia.Point)


class __FloatOrPointInterpolator(__Interpolator[__FPT]):
    def interpolate(self, initial: __FPT, diff: __FPT, t: float) -> __FPT:
        return initial + diff * t


class __PropertyAnim(Anim, Generic[__DT]):
    def __init__(self, entity: Entity, property: str, duration: float, **kwargs: Any):
        super().__init__(duration, **kwargs)
        self._entity: Entity = entity
        self._properties: list[str] = property.split('.')


class __UnitPropertyAnim(__PropertyAnim[__DT], __Interpolator[__DT]):
    def __init__(self, entity: Entity, property: str, target: __DT, *args: Any, **kwargs: Any):
        super().__init__(entity, property, *args, **kwargs)
        self._target: __DT = target
        self._base_obj: Any = None  # type: ignore lateinit
        self._final_attr: str = None  # type: ignore lateinit
        self._initial: __DT = None  # type: ignore lateinit
        self._diff: __DT = None  # type: ignore lateinit

    def start(self) -> None:
        base_obj = self._entity
        for prop in self._properties[:-1]:
            base_obj = getattr(base_obj, prop)
        self._base_obj = base_obj
        self._final_attr = self._properties[-1]
        self._initial = getattr(base_obj, self._final_attr)
        self._diff = self._target - self._initial

    def update(self, t: float) -> None:
        setattr(self._base_obj, self._final_attr, self.interpolate(self._initial, self._diff, t))

    def end(self) -> None:
        setattr(self._base_obj, self._final_attr, self._target)


class __ListPropertyAnim(__PropertyAnim[__DT], __Interpolator[__DT]):
    def __init__(self, entity: Entity, property: str, target: list[__DT], *args: Any, **kwargs: Any):
        super().__init__(entity, property, *args, **kwargs)
        self._target: list[__DT] = target
        self._initial_obj: list[__DT] = None  # type: ignore lateinit
        self._initial: list[__DT] = None  # type: ignore lateinit
        self._diff: list[__DT] = None  # type: ignore lateinit

    def start(self) -> None:
        initial_obj: list[__DT] = self._entity  # type: ignore start with the final type
        for prop in self._properties:
            initial_obj = getattr(initial_obj, prop)
        l_target = len(self._target)
        l_initial = len(initial_obj)
        if l_target != l_initial:
            raise ValueError(f'Length of target ({l_target}) does not match length of initial ({l_initial})')
        self._initial_obj = initial_obj
        self._initial = initial_obj.copy()
        self._diff = [t - i for i, t in zip(initial_obj, self._target)]

    def update(self, t: float) -> None:
        for i, d in enumerate(self._diff):
            self._initial_obj[i] = self.interpolate(self._initial[i], d, t)

    def end(self) -> None:
        self._initial_obj[:] = self._target


class __IntPropertyAnim(__UnitPropertyAnim[int], __IntInterpolator):
    pass


class __FloatPropertyAnim(__UnitPropertyAnim[float], __FloatOrPointInterpolator[float]):
    pass


class __PointPropertyAnim(__UnitPropertyAnim[skia.Point], __FloatOrPointInterpolator[skia.Point]):
    pass


class __IntListPropertyAnim(__ListPropertyAnim[int], __IntInterpolator):
    pass


class __FloatListPropertyAnim(__ListPropertyAnim[float], __FloatOrPointInterpolator[float]):
    pass


class __PointListPropertyAnim(__ListPropertyAnim[skia.Point], __FloatOrPointInterpolator[skia.Point]):
    pass


__Point = skia.Point | tuple[float, float]


def PropertyAnim(
    entity: Entity,
    property: str,
    target: __DT | __Point | list[int] | list[float] | list[__Point],
    duration: float,
    **kwargs: Any,
) -> __PropertyAnim:
    """
    Animates a property of an entity. This can animate any property of type `int`, `float`, :class:`skia.Point` or a
    list of these.

    :param entity: The entity to animate.
    :param property: The property to animate.
    :param target: The target value.
    :param duration: The duration of the animation.

    :note: The type of the animation depends on the type of the target.
    """
    if isinstance(target, list):
        t0 = target[0]
        if isinstance(t0, int):
            return __IntListPropertyAnim(entity, property, target, duration, **kwargs)  # type: ignore type was checked
        elif isinstance(t0, float):
            return __FloatListPropertyAnim(entity, property, target, duration, **kwargs)  # type: ignore type was checked
        elif isinstance(t0, (skia.Point, tuple)):
            return __PointListPropertyAnim(entity, property, [skia.Point(*p) for p in target], duration, **kwargs)
        else:
            raise TypeError(f'Unsupported type list[{type(t0)}]')
    else:
        if isinstance(target, int):
            return __IntPropertyAnim(entity, property, target, duration, **kwargs)
        elif isinstance(target, float):
            return __FloatPropertyAnim(entity, property, target, duration, **kwargs)
        elif isinstance(target, (skia.Point, tuple)):
            return __PointPropertyAnim(entity, property, skia.Point(*target), duration, **kwargs)
        else:
            raise TypeError(f'Unsupported type {type(target)}')
