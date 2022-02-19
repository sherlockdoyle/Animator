"""Entities are the basic objects that can be drawn on the screen."""
from __future__ import annotations

__all__ = 'Entity', 'Drawer', 'PathEntity'

import copy
import math
from typing import Dict, TYPE_CHECKING, List, Any, Tuple, TypeVar

import numpy

from ._transformation import Transformation
from .style import Style
from .. import skia
from ..anim.anim import Anim

if TYPE_CHECKING:
    from .._common_types import Point
    from ..scene.scene import Scene

    ET = TypeVar('ET', bound='Entity')

_PROJ_PAINT = skia.Paint(Color=0xffff0000, Style=skia.Paint.Style.kStroke_Style)
_BOUNDS_PAINT = skia.Paint(Color=0xff00ff00, Style=skia.Paint.Style.kStroke_Style)
_CROSS_PAINT = skia.Paint(Color=0xffffff00, Style=skia.Paint.Style.kStroke_Style)


class Entity:
    """The base entity class.

    :ivar pos: The position of the entity. This is the origin of the entity.
    :ivar offset: The extra offset to draw the entity at after applying the entity's transformation.
    :ivar mat: The transformation matrix of the entity.
    :ivar transformation: Convenience object for applying transformations to the entity.
    :ivar style: The :class:`Style` of the entity.
    :ivar visible: Whether the entity is drawn. This does not affect the entity's children.
    :ivar children: The children of this entity.
    :ivar update_animations: Animations to apply on each frame.
    :ivar scene: The scene this entity is in.
    """

    def __init__(self, pos: Point | skia.Point = (0, 0)):
        """
        :param pos: The position of the entity.
        """
        self.pos: skia.Point = skia.Point(*pos)
        self.offset: skia.Point = skia.Point(0, 0)
        self.mat: skia.Matrix = skia.Matrix()
        self.transformation = Transformation(self)
        self.style = Style(self)
        self.visible: bool = True

        self.children: List[Entity] = []
        self.update_animations: List[Anim] = []

        self.scene: Scene = None  # lateinit
        self._parent: Entity | None = None
        self._debug: bool = False

    def _set_scene(self, scene: Scene) -> None:
        """Set the scene of this entity and all its children."""
        self.scene = scene
        for child in self.children:
            child._set_scene(scene)

    def attr(self: ET, **kwargs: Any) -> ET:
        """Set attributes of this entity, its style, or its transformation.

        :param kwargs: The attributes to set.
        :return: This entity.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            elif hasattr(self.style, key):
                if key == 'fill_color':
                    self.style.set_color(value, None)
                elif key == 'stroke_color':
                    self.style.set_color(None, value)
                else:
                    setattr(self.style, key, value)
            elif hasattr(self.transformation, key):
                setattr(self.transformation, key, value)
        return self

    def set_visibility(self, visible: bool | None = None) -> None:
        """Set the visibility of this entity and all its children. To change the visibility without affecting the
        children, set :attr:`Entity.visible` instead.

        :param visible: Whether the entity is visible. If ``None``, the entity's visibility is toggled.
        """
        self.visible = (not self.visible) if visible is None else visible
        for child in self.children:
            child.set_visibility(visible)

    @property
    def total_transformation(self) -> skia.Matrix:
        """The total transformation of this entity, including its parent's transformation."""
        if self._parent is None:
            return skia.Matrix.Translate(self.pos).preConcat(self.mat)
        else:
            return self._parent.total_transformation.preTranslate(*self.pos).preConcat(self.mat)

    @property
    def absolute_position(self) -> skia.Point:
        """The absolute position of this entity in the scene, after applying its parent's transformation."""
        if self._parent is None:
            return skia.Point(*self.pos)
        return self._parent.total_transformation.mapXY(*self.pos)

    def add(self, *child: ET) -> ET | Tuple[ET, ...]:
        """Add one or more child entity to this entity."""
        for c in child:
            self.children.append(c)
            if self.scene is not None:
                c._set_scene(self.scene)
            c._parent = self
        return child[0] if len(child) == 1 else child

    def __contains__(self, ent: Entity) -> bool:
        """Check if an entity is in this entity or in any of its children, recursively.

        :param ent: The entity to check.
        """
        if ent in self.children:
            return True
        for child in self.children:
            if ent in child:
                return True
        return False

    def eject(self, child: ET) -> ET:
        """Remove and return a child entity from this entity, and sets the child's *pos* and *mat* such that the
        visual position and size of the child on the scene doesn't change."""
        self.children.remove(child)
        mat = self.total_transformation.preTranslate(*child.pos)
        child.pos = mat.mapXY(0, 0)
        child.mat.postConcat(mat.postTranslate(-child.pos.fX, -child.pos.fY))
        child._parent = None
        return child

    def __deepcopy__(self: ET, memo: Dict[int, Any]) -> ET:
        """Return a deep copy of this entity."""
        ent: ET = object.__new__(type(self))
        memo[id(self)] = ent
        for k, v in self.__dict__.items():
            if k == 'style':
                ent.__dict__[k] = copy.copy(self.style)
            elif k == 'mat':
                ent.__dict__[k] = skia.Matrix().set9(self.mat.get9())
            elif k in {'pos', 'offset'}:
                ent.__dict__[k] = skia.Point(*v)
            elif k in {'scene', '_parent'}:
                ent.__dict__[k] = None
            else:
                ent.__dict__[k] = copy.deepcopy(v, memo)
        ent._parent = self._parent

        stack: List[Entity] = [ent]
        while stack:
            top = stack.pop()
            for child in top.children:
                child._parent = top
                stack.append(child)
        return ent

    def copy(self: ET, eject: bool = False) -> ET:
        """Return a copy of this entity.

        :param eject: Whether to eject the copy from its parent.
        :return: The copy.
        """
        ent: ET = copy.deepcopy(self)
        if eject and self._parent is not None:
            mat = self._parent.total_transformation.preTranslate(*ent.pos)
            ent.pos = mat.mapXY(0, 0)
            ent.mat.postConcat(mat.postTranslate(-ent.pos.fX, -ent.pos.fY))
            ent._parent = None
        return ent

    def get_bounds(self, transformed: bool = False) -> skia.Rect:
        """Get the bounding box of this entity.

        :param transformed: Whether to return the bounds after applying the entity's transformation.
        :return: The bounding box of this entity.
        """
        raise NotImplementedError('This method must be implemented by subclasses.')

    def get_dimensions(self, transformed: bool = False) -> skia.Size:
        """Get the width and height of this entity.

        :param transformed: Whether to return the dimensions after applying the entity's transformation.
        :return: The width and height of this entity.
        """
        bounds = self.get_bounds(transformed)
        return skia.Size(bounds.width(), bounds.height())

    def set_relative_pos(self: ET, pos: numpy.ndarray, anchor: numpy.ndarray | None = None, padding: float = 25) -> ET:
        """Set the position of this entity relative to its scene.

        :param pos: The relative position in the scene. A 2 element numpy array [x, y]. The coordinates are between
            -1 (left or top) and 1 (right or bottom).
        :param anchor: The relative position in this entity that will be aligned to the relative position. A 2 element
            numpy array [x, y]. The coordinates are between -1 (left or top) and 1 (right or bottom). If ``None``,
            the anchor will be the same as *pos*.
        :param padding: The extra space to consider at the edges of the scene.
        :return: Itself for chaining.

        .. seealso:: :mod:`rel_pos`
        """
        self.pos.set(*self.scene.r2a_bounds(self.get_bounds(True), pos, anchor, padding))
        return self

    def set_relative_to_entity(self: ET, other: Entity, pos: numpy.ndarray, anchor: numpy.ndarray | None = None,
                               padding: float = 25) -> ET:
        """Set the position of this entity relative to another entity.

        :param other: The entity to which the position will be relative.
        :param pos: The relative position in the *other* entity. A 2 element numpy array [x, y]. The coordinates are
            between -1 (left or top) and 1 (right or bottom).
        :param anchor: The relative position in the entity that will be aligned to the relative position in the *other*
            entity. A 2 element numpy array [x, y]. The coordinates are between -1 (left or top) and 1 (right or
            bottom). If ``None``, the anchor will be the same as *pos*.
        :param padding: The extra space to consider at the edges of the scene.
        :return: Itself for chaining.

        .. seealso:: :mod:`rel_pos`
        """
        if anchor is None:
            anchor = -pos
        self_bounds = self.get_bounds(True)
        other_bounds = other.get_bounds(True)
        self_pos_x = anchor[0] * ((self_bounds.left() if anchor[0] < 0 else -self_bounds.right()) - padding)
        self_pos_y = anchor[1] * ((self_bounds.top() if anchor[1] < 0 else -self_bounds.bottom()) - padding)
        other_pos_x = pos[0] * (-other_bounds.left() if pos[0] < 0 else other_bounds.right())
        other_pos_y = pos[1] * (-other_bounds.top() if pos[1] < 0 else other_bounds.bottom())
        self.pos.set(other.pos.fX + self_pos_x + other_pos_x, other.pos.fY + self_pos_y + other_pos_y)
        return self

    def move(self: ET, dx: float = 0, dy: float = 0) -> ET:
        """Move this entity by the given amount. This changes the *pos* of this entity, but not its *mat*.

        :param dx: The amount to move in the x-axis.
        :param dy: The amount to move in the y-axis.
        :return: This entity for chaining.
        """
        self.pos += (dx, dy)
        return self

    def translate(self: ET, dx: float = 0, dy: float = 0) -> ET:
        """Translate this entity by the given amount.

        :param dx: The amount to translate in the x-axis.
        :param dy: The amount to translate in the y-axis.
        :return: This entity for chaining.
        """
        self.mat.preTranslate(dx, dy)
        return self

    def scale(self: ET, sx: float = 1, sy: float | None = None) -> ET:
        """Scale this entity by the given amount.

        :param sx: The amount to scale in the x-axis.
        :param sy: The amount to scale in the y-axis. If ``None``, the same amount is used in both axes.
        :return: This entity for chaining.
        """
        if sy is None:
            sy = sx
        self.mat.preScale(sx, sy)
        return self

    def rotate(self: ET, degrees: float = 0) -> ET:
        """Rotate this entity by the given amount.

        :param degrees: The angle to rotate in degrees.
        :return: This entity for chaining.
        """
        self.mat.preRotate(degrees)
        return self

    def skew(self: ET, kx: float = 0, ky: float = 0) -> ET:
        """Skew this entity by the given amount.

        :param kx: The angle (in degrees) to skew in the x-axis.
        :param ky: The angle (in degrees) to skew in the y-axis.
        :return: This entity for chaining.
        """
        kx, ky = math.tan(math.radians(kx)), math.tan(math.radians(ky))
        self.mat.preSkew(kx, ky)
        return self

    def transform(self: ET, mat: skia.Matrix) -> ET:
        """Transform this entity by the given matrix.

        :param mat: The matrix to transform by.
        :return: This entity for chaining.
        """
        self.mat.preConcat(mat)
        return self

    def reset_transform(self: ET) -> ET:
        """Reset the transform of this entity."""
        self.mat.reset()
        return self

    def align(self: ET, pos: numpy.ndarray) -> ET:
        """Align this entity by changing its *offset* to be at the relative *pos* of this entity.

        :param pos: The relative position in the entity. A 2 element numpy array [x, y]. The coordinates are between
            -1 (left or top) and 1 (right or bottom).
        :return: Itself for chaining.
        """
        bounds = self.get_bounds()
        self.offset.offset(-(pos[0] + 1) * bounds.width() / 2 - bounds.left(),
                           -(pos[1] + 1) * bounds.height() / 2 - bounds.top())
        return self

    def center(self: ET) -> ET:
        """Center this entity by changing its *offset* to be the center of the entity."""
        bounds = self.get_bounds()
        self.offset.offset(-bounds.centerX(), -bounds.centerY())
        return self

    def shift(self: ET, dx: float = 0, dy: float = 0) -> ET:
        """Shift this entity by the given amount. This changes the *offset* of this entity, but not its *mat*.

        :param dx: The amount to move in the x-axis.
        :param dy: The amount to move in the y-axis.
        :return: This entity for chaining.
        """
        self.offset += (dx, dy)
        return self

    def update(self) -> None:
        """Update the animations of this entity."""
        for anim in self.update_animations:
            if anim.state == Anim.State.NOT_STARTED:
                anim.start()
            anim.update()
        for child in self.children:
            child.update()

    def debug_draw(self) -> None:
        """Draw debug information for this entity."""
        transformation: skia.Matrix = skia.Matrix.Translate(self.pos) if self._parent is None else \
            self._parent.total_transformation.preTranslate(*self.pos)
        self_pos = transformation.mapXY(0, 0)
        bounds = transformation.mapRect(self.get_bounds(True))
        self_offset = transformation.preConcat(self.mat).mapXY(0, 0)

        self.scene.canvas.save()
        self.scene.canvas.drawPath(
            skia.Path().moveTo(bounds.left(), bounds.top()).lineTo(self_pos).lineTo(bounds.right(), bounds.bottom())
                .moveTo(bounds.right(), bounds.top()).lineTo(self_pos).lineTo(bounds.left(), bounds.bottom()),
            _PROJ_PAINT
        )
        self.scene.canvas.drawRect(bounds, _BOUNDS_PAINT)
        self.scene.canvas.drawPath(
            skia.Path().moveTo(bounds.left(), bounds.top()).lineTo(self_offset).lineTo(bounds.right(), bounds.bottom())
                .moveTo(bounds.right(), bounds.top()).lineTo(self_offset).lineTo(bounds.left(), bounds.bottom()),
            _CROSS_PAINT
        )
        self.scene.canvas.restore()

    def draw(self) -> None:
        """Draw this entity and its children."""
        if self.visible:
            self.on_draw()
        for child in self.children:
            child.draw()
        if self._debug:
            self.debug_draw()

    def on_draw(self) -> None:
        """Called to draw this entity. Override this in subclass."""
        pass


class Drawer:
    """A drawer draws on a path. This class is handled by a :class:`PathEntity`.

    Use this to draw around the origin. The container entity will handle positioning; although you can do extra
    positioning and transformations here too. Set the attributes of the drawer which effect the path (usually all the
    parameters of ``__init__``) in *__slots__*. This is necessary for the container entity to be able to track changes.
    """
    __slots__: Tuple[str, ...] = ()  #: attributes to look for to track changes
    # TODO: Implement fill_type
    fill_type: skia.PathFillType  #: the fill type of the path (currently unused)

    def __init__(self, **kwargs: Any):
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))  # should specify all attributes

    def draw(self, path: skia.Path) -> None:
        """Draw on the given *path*. Override this in subclass.

        This method is called only if the entity thinks that a redraw is necessary. Assume that the path is empty.
        """
        raise NotImplementedError('This method must be overridden in subclass.')


class PathEntity(Entity):
    """The base class for entities that are drawn with a path. These are the most common entities. The drawable's
    attributes are also accessible and modifiable from this entity.

    :ivar drawer: The drawable to draw on the path. We use a separate object so that it can be changed without
        changing the entity.
    :ivar preserve_stroke: Whether the stroke of the entity should be preserved from transformations.
    :ivar scale_stroke_width: When the stroke is preserved, whether the stroke width should still be scaled (uniformly).
    """

    def __init__(self, drawer: Drawer, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.drawer: Drawer = drawer
        self.preserve_stroke: bool = False
        self.scale_stroke_width: bool = False

        self._path: skia.Path = skia.Path()
        self._is_path_dirty: bool = True

    def __setattr__(self, key: str, value: Any) -> None:
        if 'drawer' in self.__dict__ and key in self.drawer.__slots__:
            setattr(self.drawer, key, value)
            self._is_path_dirty = True
        else:
            super().__setattr__(key, value)
            if key in {'drawer', 'offset'}:
                self._is_path_dirty = True

    def __getattribute__(self, key: str) -> Any:
        if key == 'offset':  # offset accessed, maybe will change
            self._is_path_dirty = True
        return super().__getattribute__(key)

    def __getattr__(self, key: str) -> Any:
        self._is_path_dirty = True  # access to attributes, maybe will change
        return getattr(self.drawer, key)  # this should work

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({", ".join(map(lambda x: f"{x}={getattr(self, x)}", self.drawer.__slots__))})'

    def dirty_path(self) -> None:
        """An attribute change might not always be detected. This method asks for a path recalculation."""
        self._is_path_dirty = True

    def update_path(self) -> None:
        """Update the path of this entity if necessary."""
        if self._is_path_dirty:
            self._path.rewind()
            self.drawer.draw(self._path)
            self._path.offset(*self.offset)
            self._is_path_dirty = False

    def do_fill_stroke(self) -> None:
        """Draw the path with the current style."""
        fill_paint, stroke_paint, opacity = self.style.get_paints()
        if opacity == 0:
            return  # if opacity is 0, we don't need to draw anything
        if opacity < 1:
            self.scene.canvas.saveLayerAlpha(None, round(opacity * 255))

        self.scene.canvas.drawPath(self._path, fill_paint)
        if self.preserve_stroke:
            transformation: skia.Matrix = self.scene.canvas.getTotalMatrix()
            transformed_path: skia.Path = skia.Path()
            self._path.transform(transformation, transformed_path, skia.ApplyPerspectiveClip.kNo)
            fill_path: skia.Path = skia.Path()
            if self.scale_stroke_width:
                stroke_paint.setStrokeWidth(transformation.mapRadius(stroke_paint.getStrokeWidth()))
            # TODO: Is the following okay?
            if stroke_paint.getFillPath(transformed_path, fill_path):  # don't draw if hairline
                transformation.invert(transformation)
                fill_path.transform(transformation, pc=skia.ApplyPerspectiveClip.kNo)
                stroke_paint.setStyle(skia.Paint.kFill_Style)
                self.scene.canvas.drawPath(fill_path, stroke_paint)
        else:
            self.scene.canvas.drawPath(self._path, stroke_paint)

        if opacity < 1:
            self.scene.canvas.restore()

    def on_draw(self) -> None:
        self.update_path()
        self.scene.canvas.save()
        self.scene.canvas.concat(self.total_transformation)
        self.do_fill_stroke()
        self.scene.canvas.restore()

    def get_bounds(self, transformed: bool = False) -> skia.Rect:
        """Get the bounds of this entity.

        :param transformed: If True, return the bounds of the transformed path.
        """
        self.update_path()
        if transformed:
            path = self._path.makeTransform(self.mat, skia.ApplyPerspectiveClip.kNo)
            return path.computeTightBounds()
        else:
            return self._path.computeTightBounds()
