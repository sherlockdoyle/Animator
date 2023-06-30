"""Entities are the basic objects that can be drawn on the screen."""
from __future__ import annotations

import math
from typing import TYPE_CHECKING, Any, TypeVar

from animator import skia
from animator._common_types import PointLike
from animator.entity.entity_list import EntityList
from animator.entity.relpos import RelativePosition
from animator.entity.transformation import Transformation
from animator.graphics import Style
from animator.graphics.shader import _BlenderLike, _to_blender

if TYPE_CHECKING:
    from animator.scene import Scene

    ET = TypeVar('ET', bound='Entity')


class Entity:
    """The base entity class.

    :ivar pos: The position of the entity. This is the origin of the entity.
    :ivar transformation: Convenience object for applying transformations to the entity.
    :ivar offset: The extra offset to draw the entity at after applying the entity's transformation.
    :ivar z_index: The z-index of the entity. Entities with a higher z-index are drawn on top of entities with a lower
        z-index.
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
        self.pos: skia.Point = skia.Point(0, 0) if pos is None else skia.Point(*pos)
        self.__do_center: bool = pos is None
        self.__mat: skia.Matrix = skia.Matrix()
        self.transformation = Transformation(self.__mat)
        self.offset: skia.Point = skia.Point(0, 0)
        self.z_index: int = 0
        self.visible: bool = True
        self.style: Style = Style()

        self.transformation.set_from_kwargs(**kwargs)
        self.style.set_from_kwargs(**kwargs)

        self.children: EntityList = EntityList()
        self.__parent: Entity | None = None
        self._scene: Scene = None  # type: ignore lateinit
        self._is_dirty: bool = True

    @property
    def mat(self) -> skia.Matrix:
        """The transformation matrix of the entity."""
        return self.__mat

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
            return skia.Matrix.Translate(self.pos).preConcat(self.__mat)
        else:
            return self.__parent.total_transformation.preTranslate(*self.pos).preConcat(self.__mat)

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

    def __getitem__(self: ET, children: Entity | tuple[Entity, ...]) -> ET:
        """Clear the children of this entity and add the given children."""
        self.clear()
        if isinstance(children, tuple):
            self.add(*children)
        else:
            self.add(children)
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
        """Set the position of this entity relative to its scene.

        :param pos: The position of the entity relative to the scene, a 2 element numpy array [x, y]. The coordinates
            are between -1 and 1, where -1 is the left/top of the scene and 1 is the right/bottom of the scene.
        :param anchor: The anchor point of the entity in relative coordinates, which will be positioned at *pos*. If
            ``None``, it'll be same as *pos*.
        :param padding: The extra space around the scene, in pixels.
        """
        self.pos.set(*self._scene.r2a_bounds(self.get_bounds(True), pos, anchor, padding))
        return self

    def set_relative_to_entity(
        self: ET, other: Entity, pos: RelativePosition, anchor: RelativePosition | None = None, padding: float = 25
    ) -> ET:
        """Set the position of this entity relative to another entity.

        :param other: The entity to which the position is relative.
        :param pos: The position of the entity relative to *other*, a 2 element numpy array [x, y]. The coordinates are
            between -1 and 1, where -1 is the left/top of the entity and 1 is the right/bottom of the entity.
        :param anchor: The anchor point of the entity in relative coordinates, which will be positioned at *pos*. If
            ``None``, it'll be same as *pos*.
        :param padding: The extra space around the entity, in pixels.
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
        self.__mat.preTranslate(dx, dy)
        return self

    def scale(self: ET, sx: float = 1, sy: float | None = None) -> ET:
        """Scale the entity by the given amount.

        :param sx: The amount to scale in the x direction.
        :param sy: The amount to scale in the y direction. If ``None``, *sx* is used.
        """
        self.__mat.preScale(sx, sx if sy is None else sy)
        return self

    def rotate(self: ET, degrees: float = 0) -> ET:
        """Rotate the entity by the given amount.

        :param degrees: The amount to rotate in degrees.
        """
        self.__mat.preRotate(degrees)
        return self

    def skew(self: ET, kx: float = 0, ky: float = 0) -> ET:
        """Skew the entity by the given amount.

        :param kx: The amount (in degrees) to skew in the x direction.
        :param ky: The amount (in degrees) to skew in the y direction.
        """
        kx = math.tan(math.radians(kx))
        ky = math.tan(math.radians(ky))
        self.__mat.preSkew(kx, ky)
        return self

    def transform(self: ET, mat: skia.Matrix) -> ET:
        """Apply the given transformation matrix to the entity.

        :param mat: The transformation matrix.
        """
        self.__mat.preConcat(mat)
        return self

    def reset_transform(self: ET) -> ET:
        """Reset the transformation matrix to the identity matrix."""
        self.__mat.reset()
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
        self.offset.offset(
            -(pos[0] + 1) * bounds.width() / 2 - bounds.left(), -(pos[1] + 1) * bounds.height() / 2 - bounds.top()
        )
        return self

    def center(self: ET) -> ET:
        """Shifts the entity so that its *offset* is aligned with the center of the entity."""
        bounds = self.get_bounds(True)
        self.offset.offset(-bounds.centerX(), -bounds.centerY())
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

    def _transform_and_draw(self, canvas: skia.Canvas) -> None:
        """Draw the entity on the given *canvas*."""
        if self.style.nothing_to_draw():
            return
        save_count = canvas.save()
        canvas.concat(self.total_transformation)
        self.style.apply_clip(canvas)
        self.style.apply_final_paint(canvas)

        self.on_draw(canvas)

        canvas.restoreToCount(save_count)

    def draw(self, canvas: skia.Canvas | None = None) -> None:
        """Draw the entity and its children."""
        if self.visible:
            self._transform_and_draw(self._scene.canvas if canvas is None else canvas)
        for child in self.children:
            child.draw()


class Group(Entity):
    """
    A :class:`Group` does not draw anything itself, so it's ``stroke_paint`` and ``fill_paint`` are ignored. It is
    useful for grouping entities together, especially if you want to apply some style to all of them at once. While you
    can add children to any entity, a group behaves a bit differently on how it draws its children.

    Normally, an entity's ``clip`` and ``final_paint`` only apply to itself. However, a group will apply its ``clip``
    and ``final_paint`` to all of its children. The bounds of a group is the union of all of its children's bounds. The
    group can also be used to blend its children.
    """

    def __init__(self, child_blender: _BlenderLike | None = None, **kwargs):
        """
        :param child_blender: If not ``None``, the blender is used for all children on top of their own blend mode.
        """
        super().__init__(**kwargs)
        self.child_blender = child_blender if child_blender is None else _to_blender(child_blender)

    def draw(self, canvas: skia.Canvas | None = None) -> None:
        if self.style.nothing_to_draw():
            return
        canvas = self._scene.canvas if canvas is None else canvas
        save_count = canvas.save()
        if self.style.clip is not None:
            total_matrix = canvas.getTotalMatrix()  # local stack for matrix
            canvas.concat(self.total_transformation)
            self.style.apply_clip(canvas)
            canvas.setMatrix(total_matrix)
        self.style.apply_final_paint(canvas)

        canvas.translate(self.offset.fX, self.offset.fY)
        for child in self.children:
            if self.child_blender is not None:
                canvas.saveLayer(None, skia.Paint(blender=self.child_blender))
            child.draw()
            if self.child_blender is not None:
                canvas.restore()

        canvas.restoreToCount(save_count)

    def get_bounds(self, transformed: bool = False) -> skia.Rect:
        bounds = skia.Rect.MakeEmpty()
        for child in self.children:
            bound = child.get_bounds()
            bound.offset(child.pos)
            bounds.join(self.mat.mapRect(bound, skia.ApplyPerspectiveClip.kNo) if transformed else bound)
        return bounds
