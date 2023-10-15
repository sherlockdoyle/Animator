from typing import Any, Callable, Sequence

from animator import skia
from animator._common_types import PointLike
from animator.entity.entity import Entity
from animator.graphics.shader import _BlenderLike, _to_blender


class Group(Entity):
    """
    A :class:`Group` does not draw anything itself, so it's ``stroke_paint`` and ``fill_paint`` are ignored. It is
    useful for grouping entities together, especially if you want to apply some style to all of them at once. While you
    can add children to any entity, a group behaves a bit differently on how it draws its children.

    Normally, an entity's ``clip`` and ``final_paint`` only apply to itself. However, a group will apply its ``clip``
    and ``final_paint`` to all of its children. The bounds of a group is the union of all of its children's bounds. The
    group can also be used to blend its children.
    """

    def __init__(self, child_blender: _BlenderLike | None = None, **kwargs: Any) -> None:
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


FuncEntityFunc = Callable[[], Entity | Sequence[Entity] | None]


class FuncEntity(Entity):
    """An entity that dynamically draws the return value of a provided function."""

    def __init__(self, func: FuncEntityFunc, pos: PointLike = (0, 0), **kwargs: Any) -> None:
        """
        :param func: A function that returns an entity or list of entities to draw. The function is called every time
            the entity is drawn and the returned entities are added as children temporarily.
        """
        super().__init__(pos, **kwargs)
        self.func: FuncEntityFunc = func

    def draw(self, canvas: skia.Canvas | None = None) -> None:
        entities = self.func()
        if entities is None:
            return
        if isinstance(entities, Entity):
            entities = [entities]

        self.add(*entities)
        super().draw(canvas)
        self.children.clear()
