"""Entities are the basic objects that can be drawn on the screen."""
from __future__ import annotations

import math
from typing import TYPE_CHECKING, Any, Final, Generator, Literal, TypeVar, overload

from animator import skia
from animator._common_types import PointLike
from animator.entity.entity_list import EntityList
from animator.entity.relpos import RelativePosition
from animator.entity.transformation import Transformation
from animator.graphics import Style

if TYPE_CHECKING:
    from animator.anim import Anim
    from animator.scene import Scene

    ET = TypeVar('ET', bound='Entity')


class Entity:
    """The base entity class.

    :ivar pos: The position of the entity. This is the origin of the entity.
    :ivar mat: The transformation matrix of the entity.
    :ivar transformation: Convenience object for applying transformations to the entity.
    :ivar offset: The extra offset to draw the entity at after applying the entity's transformation.
    :ivar visible: Whether the entity is drawn. This does not affect the entity's children.
    :ivar style: The :class:`Style` of the entity.
    :ivar children: The children of this entity.
    :ivar _is_dirty: Entities may cache some values for performance. This flag is set to ``True`` when the entity needs
        to recalculate its cached values. Subclasses may implement methods to automatically detect when this flag needs
        to be set.
    """

    def __init__(self, pos: PointLike | None = None, **kwargs: Any) -> None:
        """
        :param pos: The position of the entity.
        :param kwargs: Arguments to pass to :attr:`transformation` and :attr:`style`. See their :meth:`set_from_args`
            method for more info.
        """
        self.pos: Final[skia.Point] = skia.Point(0, 0) if pos is None else skia.Point(*pos)
        self.__do_center: bool = pos is None
        self.mat: Final[skia.Matrix] = skia.Matrix()
        self.transformation: Final[Transformation] = Transformation(self.mat)
        self.offset: Final[skia.Point] = skia.Point(0, 0)
        self.__z_index: int = 0
        self.visible: bool = True
        self.style: Final[Style] = Style()

        self.transformation.set_from_kwargs(**kwargs)
        self.style.set_from_kwargs(**kwargs)

        self.children: Final[EntityList] = EntityList()
        self.__parent: Entity | None = None
        self._scene: Scene = None  # type: ignore lateinit
        self._is_dirty: bool = True

    @property
    def z_index(self) -> int:
        """
        The z-index of the entity. Entities with a higher z-index are drawn on top of entities with a lower z-index.
        """
        return self.__z_index

    @z_index.setter
    def z_index(self, value: int) -> None:
        if self.__z_index != value:
            self.__z_index = value
            if self.__parent is None:  # no parent, so maybe direct child of its scene
                self._scene.entities.sort()
            else:
                self.__parent.__sort_children()

    def __sort_children(self) -> None:
        self.children.sort()

    def set_scene(self, scene: Scene) -> None:
        """Set the scene of this entity and all its children."""
        self._scene = scene
        if self.__do_center and self.__parent is None:
            self.pos.offset(scene.width / 2, scene.height / 2)
        self.__do_center = False
        for child in self.children:
            child.set_scene(scene)

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
        if self.__parent is None:
            return skia.Matrix.Translate(self.pos).preConcat(self.mat)
        else:
            return self.__parent.total_transformation.preTranslate(*self.pos).preConcat(self.mat)

    @property
    def absolute_position(self) -> skia.Point:
        """The absolute position of this entity in the scene, after applying its parent's transformation."""
        if self.__parent is None:
            return skia.Point(*self.pos)
        return self.__parent.total_transformation.mapXY(*self.pos)

    def add(self, *children: Entity) -> None:
        """Add one or more children to this entity."""
        self.children.extend(children)
        for child in children:
            child.__parent = self
            if self._scene is not None:
                child.set_scene(self._scene)

    def clear(self) -> None:
        """Clear the children of this entity."""
        for child in self.children:
            child.__parent = None
        self.children.clear()

    def __getitem__(self: ET, children: Entity | tuple[Entity, ...] | Generator[Entity, None, None]) -> ET:
        """Clear the children of this entity and add the given children."""
        self.clear()
        if isinstance(children, Entity):
            self.add(children)
        else:
            self.add(*children)
        return self

    def __contains__(self, entity: Entity) -> bool:
        """Check if an entity is in this entity or in any of it's children, recursively.

        :param entity: The entity to check.
        """
        if entity in self.children:
            return True
        for child in self.children:
            if entity in child:
                return True
        return False

    def _add_sibling(self, entity: Entity) -> None:
        """Add a new *entity* at the same level as this entity."""
        if self.__parent is None:
            self._scene.entities.append(entity)
        else:
            self.__parent.children.append(entity)
            entity.__parent = self.__parent
        if self._scene is not None:
            entity.set_scene(self._scene)

    def _remove(self) -> None:
        """Remove itself from its parent, if it has one, or from the scene."""
        if self.__parent is None:
            self._scene.entities.remove(self)
        else:
            self.__parent.children.remove(self)

    def _replace(self, entity: Entity) -> None:
        """Replace this entity with another one."""
        if self.__parent is None:
            index = self._scene.entities.index(self)
            self._scene.entities[index] = entity
        else:
            index = self.__parent.children.index(self)
            self.__parent.children[index] = entity
            entity.__parent = self.__parent
        if self._scene is not None:
            entity.set_scene(self._scene)

    def _mark_dirty(self) -> None:
        """
        Manually mark this entity as dirty in case automatic cache invalidation fails. Maybe this should be called every
        time the entity is modified.
        """
        self._is_dirty = True

    def get_bounds(self, transformed: bool = False) -> skia.Rect:
        """Get the bounding box of this entity.

        :param transformed: Whether to apply the entity's transformation to the bounding box.
        """
        raise NotImplementedError('get_bounds() must be implemented by subclasses.')

    def get_dimensions(self, transformed: bool = False) -> skia.Size:
        """Get the width and height of this entity.

        :param transformed: Whether to apply the entity's transformation to the dimensions.
        """
        bounds = self.get_bounds(transformed)
        return skia.Size(bounds.width(), bounds.height())

    def set_relative_pos(
        self: ET, pos: RelativePosition, anchor: RelativePosition | None = None, padding: float = 25
    ) -> ET:
        """Set the position of this entity relative to its scene. Doesn't work for child entities.

        :param pos: The position of the entity relative to the scene, a 2 element numpy array [x, y]. The coordinates
            are between -1 and 1, where -1 is the left/top of the scene and 1 is the right/bottom of the scene.
        :param anchor: The anchor point of the entity in relative coordinates, which will be positioned at *pos*. If
            ``None``, it'll be same as *pos*.
        :param padding: The extra space around the scene, in pixels.
        """
        self.pos.set(*self._scene.r2a_bounds(self.get_bounds(True), pos, anchor, padding))
        return self

    def get_pos_relative_to_entity(
        self, other: Entity, pos: RelativePosition, anchor: RelativePosition | None = None, padding: float = 25
    ) -> skia.Point:
        """
        Get the position of this entity relative to another entity. Takes the same parameters as
        :meth:`set_relative_to_entity`. Doesn't work for child entities.
        """
        if anchor is None:
            anchor = -pos
        self_bounds = self.get_bounds(True)
        other_bounds = other.get_bounds(True)
        self_pos_x = anchor[0] * ((self_bounds.left() if anchor[0] < 0 else -self_bounds.right()) - padding)
        self_pos_y = anchor[1] * ((self_bounds.top() if anchor[1] < 0 else -self_bounds.bottom()) - padding)
        other_pos_x = pos[0] * (-other_bounds.left() if pos[0] < 0 else other_bounds.right())
        other_pos_y = pos[1] * (-other_bounds.top() if pos[1] < 0 else other_bounds.bottom())
        return skia.Point(other.pos.fX + self_pos_x + other_pos_x, other.pos.fY + self_pos_y + other_pos_y)

    def set_relative_to_entity(
        self: ET, other: Entity, pos: RelativePosition, anchor: RelativePosition | None = None, padding: float = 25
    ) -> ET:
        """Set the position of this entity relative to another entity. Doesn't work for child entities.

        :param other: The entity to which the position is relative.
        :param pos: The position of the entity relative to *other*, a 2 element numpy array [x, y]. The coordinates are
            between -1 and 1, where -1 is the left/top of the entity and 1 is the right/bottom of the entity.
        :param anchor: The anchor point of the entity in relative coordinates, which will be positioned at *pos*. If
            ``None``, it'll be same as -*pos*.
        :param padding: The extra space around the entity, in pixels.
        """
        self.pos.set(*self.get_pos_relative_to_entity(other, pos, anchor, padding))
        return self

    def move(self: ET, dx: float = 0, dy: float = 0) -> ET:
        """Move the entity by a given amount. This changes *pos*.

        :param dx: The amount to move in the x direction.
        :param dy: The amount to move in the y direction.
        """
        self.pos.offset(dx, dy)
        return self

    def translate(self: ET, dx: float = 0, dy: float = 0) -> ET:
        """Translate the entity by the given amount.

        :param dx: The amount to translate in the x direction.
        :param dy: The amount to translate in the y direction.
        """
        self.mat.preTranslate(dx, dy)
        return self

    def scale(self: ET, sx: float = 1, sy: float | None = None) -> ET:
        """Scale the entity by the given amount.

        :param sx: The amount to scale in the x direction.
        :param sy: The amount to scale in the y direction. If ``None``, *sx* is used.
        """
        self.mat.preScale(sx, sx if sy is None else sy)
        return self

    def rotate(self: ET, degrees: float = 0) -> ET:
        """Rotate the entity by the given amount.

        :param degrees: The amount to rotate in degrees.
        """
        self.mat.preRotate(degrees)
        return self

    def skew(self: ET, kx: float = 0, ky: float = 0) -> ET:
        """Skew the entity by the given amount.

        :param kx: The amount (in degrees) to skew in the x direction.
        :param ky: The amount (in degrees) to skew in the y direction.
        """
        self.mat.preSkew(math.tan(math.radians(kx)), math.tan(math.radians(ky)))
        return self

    def transform(self: ET, mat: skia.Matrix) -> ET:
        """Apply the given transformation matrix to the entity.

        :param mat: The transformation matrix.
        """
        self.mat.preConcat(mat)
        return self

    def reset_transform(self: ET) -> ET:
        """Reset the transformation matrix to the identity matrix."""
        self.mat.reset()
        return self

    def shift(self: ET, dx: float = 0, dy: float = 0) -> ET:
        """Shift the entity by the given amount. This changes *offset*.

        :param dx: The amount to shift in the x direction.
        :param dy: The amount to shift in the y direction.
        """
        self.offset.offset(dx, dy)
        return self

    def align(self: ET, pos: RelativePosition) -> ET:
        """Shifts the entity so that its *offset* is aligned with the relative *pos*.

        :param pos: The position relative to the entity, a 2 element numpy array [x, y]. The coordinates are between -1
            and 1, where -1 is the left/top of the entity and 1 is the right/bottom of the entity.
        """
        bounds = self.get_bounds(True)
        point = self.mat.makeInverse().mapVector(
            (pos[0] + 1) * bounds.width() / 2 + bounds.fLeft, (pos[1] + 1) * bounds.height() / 2 + bounds.fTop
        )
        self.offset.offset(-point.fX, -point.fY)
        return self

    def center(self: ET) -> ET:
        """Shifts the entity so that its *offset* is aligned with the center of the entity."""
        bounds = self.get_bounds(True)
        center = self.mat.makeInverse().mapVector(bounds.centerX(), bounds.centerY())
        self.offset.offset(-center.fX, -center.fY)
        return self

    def do_stroke(self, canvas: skia.Canvas) -> None:
        """Draw the stroke. This method can be overridden by subclasses to change the stroke behavior."""
        pass

    def do_fill(self, canvas: skia.Canvas) -> None:
        """Draw the fill. This method can be overridden by subclasses to change the fill behavior."""
        pass

    def on_draw(self, canvas: skia.Canvas) -> None:
        """Draw the entity. This method can be overridden by subclasses to change the drawing behavior."""
        if (
            self.style.paint_style == Style.PaintStyle.STROKE_ONLY
            or self.style.paint_style == Style.PaintStyle.STROKE_THEN_FILL
        ):
            self.do_stroke(canvas)
        if self.style.paint_style != Style.PaintStyle.STROKE_ONLY:
            self.do_fill(canvas)
        if self.style.paint_style == Style.PaintStyle.FILL_THEN_STROKE:
            self.do_stroke(canvas)

    def draw_self(self, canvas: skia.Canvas) -> None:
        """Draw the entity on the given *canvas*."""
        if self.style.nothing_to_draw():
            return
        save_count = canvas.save()
        self.style.apply_clip(canvas)
        self.style.apply_final_paint(canvas)

        self.on_draw(canvas)

        canvas.restoreToCount(save_count)

    def draw(self) -> None:
        """Draw the entity and its children."""
        canvas = self._scene.canvas
        save_count = canvas.save()
        if self.visible or self.children:
            canvas.translate(*self.pos)
            canvas.concat(self.mat)

        if self.visible:
            self.draw_self(self._scene.canvas if canvas is None else canvas)
        for child in self.children:
            child.draw()

        canvas.restoreToCount(save_count)

    @overload
    def animate(self, property: Literal['z_index'], target: int, duration: float, **kwargs: Any) -> Anim:
        pass

    @overload
    def animate(
        self,
        property: Literal[
            'transformation.originX',
            'transformation.originY',
            'transformation.translateX',
            'transformation.translateY',
            'transformation.scaleX',
            'transformation.scaleY',
            'transformation.scale',
            'transformation.rotation',
            'transformation.skewX',
            'transformation.skewY',
        ],
        target: float,
        duration: float,
        **kwargs: Any,
    ) -> Anim:
        pass

    @overload
    def animate(self, property: Literal['pos'], target: PointLike, duration: float, **kwargs: Any) -> Anim:
        pass

    def animate(self, property: str, target: Any, duration: float, **kwargs: Any) -> Anim:
        """Animates the entity.

        :param property: The property to animate.
        :param target: The target value.
        :param duration: The duration of the animation in seconds.
        """
        from animator.anim.property import PropertyAnim  # I don't like this, but this is to prevent circular imports

        return PropertyAnim(self, property, target, duration, **kwargs)


class Group(Entity):
    """
    An entity that doesn't draw anything of its own but draws its children. A :class:`Group` also applies its ``offset``
    to its children. The bounds of a group is the union of all of its children's bounds.
    """

    @property
    def total_transformation(self) -> skia.Matrix:
        return super().total_transformation.preTranslate(*self.offset)

    def get_bounds(self, transformed: bool = False) -> skia.Rect:
        if not self.children:
            return skia.Rect.MakeEmpty()

        bounds = self.children[0].get_bounds(True)
        bounds.offset(self.children[0].pos)
        mat = skia.Matrix.Translate(self.offset).postConcat(self.mat)
        points: list[skia.Point] = mat.mapRectToQuad(bounds) if transformed else []
        for i in range(1, len(self.children)):
            child = self.children[i]
            bound = child.get_bounds(True)
            bound.offset(child.pos)
            if transformed:
                points.extend(mat.mapRectToQuad(bound))
            else:
                bounds.join(bound)
        if transformed:
            bounds.setBounds(points)
        return bounds

    def draw(self) -> None:
        canvas = self._scene.canvas
        save_count = canvas.save()
        if self.children:
            canvas.translate(*self.pos)
            canvas.concat(self.mat)
            canvas.translate(*self.offset)

        for child in self.children:
            child.draw()

        canvas.restoreToCount(save_count)
