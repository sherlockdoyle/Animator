"""General classes for animating any (numeric like) property of any object (although typed for :class:`Entity`).

These are not meant to be used directly, although you can. These are made available via several
:meth:`Entity.animate` methods. """
from __future__ import annotations

__all__ = 'PropertyAnimator',

import operator
from typing import Callable, Any, Union, Sequence, TYPE_CHECKING, Dict

import numpy

from .anim import Anim

if TYPE_CHECKING:
    from ..entity.entity import Entity

    PropType = Union[str, int]
    ValueType = Union[float, Sequence[float], numpy.ndarray]


class _PropAnim(Anim):
    """Animates a property *prop* of an object *obj*."""

    def __init__(self, obj: Entity, prop: PropType,
                 mod_func: Callable[[float | numpy.ndarray, float], float | numpy.ndarray], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.obj: Entity = obj
        self.prop: PropType = prop
        self.mod_func: Callable[[float | numpy.ndarray, float], float | numpy.ndarray] = mod_func
        self.entities.append(obj)

    def start(self) -> None:
        if isinstance(self.prop, str):
            old_val = operator.attrgetter(self.prop)(self.obj)

            def getter() -> ValueType:
                return operator.attrgetter(self.prop)(self.obj)

            *all_prop, last_prop = self.prop.split('.')

            def setter(value: ValueType) -> None:
                sub_val = self.obj
                for p in all_prop:
                    sub_val = getattr(sub_val, p)
                setattr(sub_val, last_prop, value)

        else:  # isinstance(self.prop, int)
            old_val = operator.itemgetter(self.prop)(self.obj)

            def getter() -> ValueType:
                return operator.itemgetter(self.prop)(self.obj)

            def setter(value: ValueType) -> None:
                self.obj[self.prop] = value

        if isinstance(old_val, (int, float)):
            self.updater: Callable[[float], None] = lambda t: setter(self.mod_func(old_val, t))
        elif isinstance(old_val, Sequence):
            old_val = numpy.array(old_val)
            self.updater: Callable[[float], None] = lambda t: getter().__setitem__(slice(None),
                                                                                   self.mod_func(old_val, self.t))
        elif isinstance(old_val, numpy.ndarray):
            self.updater: Callable[[float], None] = lambda t: numpy.copyto(getter(), self.mod_func(old_val, t))
        else:
            raise TypeError(f'PropertyAnimator can only animate scalar, sequence, or ndarray. Found {type(old_val)}.')

    def update(self) -> None:
        self.updater(self.t)

    def end(self) -> None:
        self.updater(1)


class _PropSetterAnim(_PropAnim):
    """Sets a property *prop* of an object *obj* to a value *val*."""
    # use mod_func to set the value
    mod_func: ValueType  # type: ignore

    def start(self) -> None:
        if isinstance(self.prop, str):
            old_val = operator.attrgetter(self.prop)(self.obj)

            def getter() -> ValueType:
                return operator.attrgetter(self.prop)(self.obj)

            *all_prop, last_prop = self.prop.split('.')

            def setter(value: ValueType) -> None:
                sub_val = self.obj
                for p in all_prop:
                    sub_val = getattr(sub_val, p)
                setattr(sub_val, last_prop, value)

        else:  # isinstance(self.prop, int)
            old_val = operator.itemgetter(self.prop)(self.obj)

            def getter() -> ValueType:
                return operator.itemgetter(self.prop)(self.obj)

            def setter(value: ValueType) -> None:
                self.obj[self.prop] = value

        if isinstance(old_val, (int, float)):
            diff = self.mod_func - old_val
            self.updater: Callable[[float], None] = lambda t: setter(old_val + diff * t)
        elif isinstance(old_val, Sequence):
            old_val = numpy.array(old_val)
            diff = self.mod_func - old_val
            self.updater: Callable[[float], None] = lambda t: getter().__setitem__(slice(None), old_val + diff * t)
        elif isinstance(old_val, numpy.ndarray):
            diff = self.mod_func - old_val
            self.updater: Callable[[float], None] = lambda t: numpy.copyto(getter(), old_val + diff * t)
        else:
            raise TypeError(f'PropertyAnimator can only animate scalar, sequence, or ndarray. Found {type(old_val)}.')


class PropertyAnimator:
    """Creates :class:`Anim` objects for animating any numeric or sequence of numeric properties of an object. The
    properties can chain. Except numeric properties, other properties are modified in place. It's the user's
    responsibility to pass compatible data types.

    Each of the methods also takes two additional keyword arguments:
        - *duration* (float): Duration of the animation in seconds.
        - *ease_func* (Callable[[float], float]): Easing function to use.
    """

    def __init__(self, obj: Entity, prop: PropType = ''):
        """
        :param obj: The object whose property is to be animated.
        :param prop: The property to be animated. Can be a string for attributes (``prop1.prop2...``) or an integer for
            list indices. This can be left empty and extended with :meth:`__getattr__`.
        """
        self.__obj: Entity = obj
        self.__prop: PropType = prop

    def __getattr__(self, prop: str) -> PropertyAnimator:
        """Extend the property (if possible, i.e. it's a string) to animate and return itself for chaining."""
        if isinstance(self.__prop, str):
            if self.__prop == '':
                self.__prop = prop
            else:
                self.__prop += '.' + prop
        return self

    def add(self, value: ValueType, **kwargs: Any) -> _PropAnim:
        """Returns an :class:`Anim` object that animates an addition to the property.

        :param value: The value to add to the property.
        """
        if isinstance(value, Sequence):
            value = numpy.array(value)
        return _PropAnim(self.__obj, self.__prop, lambda old, t: old + value * t, **kwargs)

    __add__ = add

    def sub(self, value: ValueType, **kwargs: Any) -> _PropAnim:
        """Returns an :class:`Anim` object that animates a subtraction from the property.

        :param value: The value to subtract from the property.
        """
        if isinstance(value, Sequence):
            value = numpy.array(value)
        return _PropAnim(self.__obj, self.__prop, lambda old, t: old - value * t, **kwargs)

    __sub__ = sub

    def mul(self, value: ValueType, **kwargs: Any) -> _PropAnim:
        """Returns an :class:`Anim` object that animates a multiplication with the property.

        :param value: The value to multiply the property with.
        """
        if isinstance(value, Sequence):
            value = numpy.array(value)
        return _PropAnim(self.__obj, self.__prop, lambda old, t: old * value ** t, **kwargs)

    __mul__ = mul

    def __setitem__(self, key: Dict[str, Any], value: ValueType) -> _PropAnim:
        """Returns an :class:`Anim` object that sets the property to the given *value* (with animation).

        :param key: The key represents the *kwargs* to pass to the :class:`Anim` object.
        :param value: The value to set the property to.
        """
        if isinstance(value, Sequence):
            value = numpy.array(value)
        return _PropSetterAnim(self.__obj, self.__prop, value, **key)  # type: ignore
