"""
Animations to transition one entity to another. These animations changes one entity, which is already on the scene, to
another entity, which is not in the scene. After the animation is finished, the old entity is removed from the scene and
the new entity is added to the scene. The final state of the old entity is undefined. The new entity is added to the
same level as the old entity (same parent, if present, otherwise the scene). These animations may or may not affect the
children of either entity.
"""
from __future__ import annotations

import copy
from typing import Any, Generic, TypeVar

from animator import skia
from animator.anim.anim import Anim
from animator.anim.graphics import StyleAnim
from animator.anim.transformation import Transform, Transform_Pow
from animator.entity.entity import Entity
from animator.entity.path import PathEntity


class _PointChange:
    def __init__(self, point: skia.Point, from_: skia.Point, to: skia.Point) -> None:
        self._point: skia.Point = point
        self._from: skia.Point = from_
        self._to: skia.Point = to
        self._diff: skia.Point = to - from_


class _ZIndexChange:
    def __init__(self, entity: Entity, from_: int, to: int) -> None:
        self._entity: Entity = entity
        self._from: int = from_
        self._to: int = to
        self._diff: int = to - from_


T = TypeVar('T', bound=Entity)


class __SwapAnim(Anim, Generic[T]):
    """Swaps an entity with another entity."""

    def __init__(
        self,
        from_: T,
        to: T,
        duration: float,
        animate_pos: bool = True,
        animate_mat: type[Transform] | type[Transform_Pow] | None = Transform,
        animate_z_index: bool = True,
        **kwargs: Any,
    ) -> None:
        """
        :param from_: The entity to be swapped.
        :param to: The entity to be swapped with.
        :param duration: The duration of the animation.
        :param animate_pos: If ``True``, the position of the entity will be animated.
        :param animate_mat: If not ``None``, the matrix of the entity will be animated with the given transformation
            animation (:class:`Transform` or :class:`Transform_Pow`).
        :param animate_z_index: If ``True``, the z-index of the entity will be animated.
        """
        super().__init__(duration, **kwargs)
        self._initial_entity: T = from_
        self._target_entity: T = to

        self.__animate_pos: bool = animate_pos
        self.__animate_mat: type[Transform] | type[Transform_Pow] | None = animate_mat
        self.__animate_z_index: bool = animate_z_index
        self.__point_anims: list[_PointChange] = []
        self.__mat_anims: list[Transform | Transform_Pow] = []
        self.__z_index_anims: list[_ZIndexChange] = []

    def _add_pos_anim(self, entity: Entity, from_: skia.Point, to: skia.Point) -> None:
        entity.pos.set(*from_)
        if self.__animate_pos:
            self.__point_anims.append(_PointChange(entity.pos, from_, to))

    def _add_mat_anim(self, entity: Entity, from_: skia.Matrix, to: skia.Matrix) -> None:
        entity.mat.setFromMatrix(from_)
        if self.__animate_mat:
            anim = self.__animate_mat(entity, to, self._duration, ease=self.ease_func)
            self.__mat_anims.append(anim)
            anim._mount(self._scene, self._start_frame)
            anim.start()

    def _add_offset_anim(self, entity: Entity, from_: skia.Point, to: skia.Point) -> None:
        entity.offset.set(*from_)
        self.__point_anims.append(_PointChange(entity.offset, from_, to))

    def _add_z_index_anim(self, entity: Entity, from_: int, to: int) -> None:
        entity.z_index = to
        if self.__animate_z_index:
            self.__z_index_anims.append(_ZIndexChange(entity, from_, to))

    def update(self, t: float) -> None:
        for p in self.__point_anims:
            p._point.set(*p._from + p._diff * t)
        for m in self.__mat_anims:
            m.update(t)
        for z in self.__z_index_anims:
            z._entity.z_index = round(z._from + z._diff * t)

    def end(self) -> None:
        for p in self.__point_anims:
            p._point.set(*p._to)
        for m in self.__mat_anims:
            m.end()
        for z in self.__z_index_anims:
            z._entity.z_index = z._to


class Dissolve(__SwapAnim[Entity]):
    class __Entity(Entity):
        def __init__(self, width: float, height: float) -> None:
            super().__init__()
            self.__clip = skia.Rect.MakeWH(width, height)
            self._paint = skia.Paint()

        def on_draw(self, canvas: skia.Canvas) -> None:
            canvas.translate(self.offset.fX, self.offset.fY)
            canvas.clipRect(self.__clip)
            canvas.drawPaint(self._paint)

    def __init__(self, from_: Entity, to: Entity, duration: float, padding: float = 25, **kwargs: Any) -> None:
        super().__init__(from_, to, duration, **kwargs)
        self.__padding = padding
        self.__anim_entity: Dissolve.__Entity = None  # type: ignore lateinit
        self.__builder: skia.RuntimeShaderBuilder = None  # type: ignore lateinit

    def start(self) -> None:
        self._target_entity.set_scene(self._initial_entity._scene)
        initial_bounds = self._initial_entity.get_bounds()
        target_bounds = self._target_entity.get_bounds()
        initial_bounds.outset(self.__padding, self.__padding)
        target_bounds.outset(self.__padding, self.__padding)
        max_width = max(initial_bounds.width(), target_bounds.width())
        max_height = max(initial_bounds.height(), target_bounds.height())

        recorder = skia.PictureRecorder()
        canvas = recorder.beginRecording(initial_bounds.width(), initial_bounds.height())
        canvas.translate(-initial_bounds.fLeft, -initial_bounds.fTop)
        self._initial_entity.on_draw(canvas)
        initial_shader = recorder.finishRecordingAsPicture().makeShader(
            skia.TileMode.kDecal, skia.TileMode.kDecal, skia.FilterMode.kNearest
        )

        canvas = recorder.beginRecording(target_bounds.width(), target_bounds.height())
        canvas.translate(-target_bounds.fLeft, -target_bounds.fTop)
        self._target_entity.on_draw(canvas)
        target_shader = recorder.finishRecordingAsPicture().makeShader(
            skia.TileMode.kDecal, skia.TileMode.kDecal, skia.FilterMode.kNearest
        )

        result = skia.RuntimeEffect.MakeForShader(
            'uniform shader p,s,d;uniform float t;vec4 main(vec2 c){return mix(s.eval(c*(vec2('
            + f'{initial_bounds.width()/target_bounds.width()-1},{initial_bounds.height()/target_bounds.height()-1})*t+1)),d.eval(c*(vec2({target_bounds.width()/initial_bounds.width()},{target_bounds.height()/initial_bounds.height()}'
            + ')*(1-t)+t)),p.eval(c).r<t*.55+.05?1:0);}'
        )
        if result.effect is None:
            raise ValueError(result.errorText)
        self.__builder = skia.RuntimeShaderBuilder(result.effect)
        self.__builder.child('p').set(
            skia.Shader.MakeFractalNoise(
                max_width / 5000,
                max_height / 5000,
                1,
                len(self._initial_entity.__class__.__name__) + len(self._target_entity.__class__.__name__),
            )
        )
        self.__builder.child('s').set(initial_shader)
        self.__builder.child('d').set(target_shader)
        self.__builder.uniform('t').set(0)

        self.__anim_entity = Dissolve.__Entity(max_width, max_height)
        self.__anim_entity._paint.setShader(self.__builder.makeShader())
        self._initial_entity._replace(self.__anim_entity)
        self._add_pos_anim(self.__anim_entity, self._initial_entity.pos, self._target_entity.pos)
        self._add_mat_anim(self.__anim_entity, self._initial_entity.mat, self._target_entity.mat)
        self._add_offset_anim(
            self.__anim_entity,
            skia.Point(initial_bounds.fLeft, initial_bounds.fTop),
            skia.Point(target_bounds.fLeft, target_bounds.fTop),
        )
        self._add_z_index_anim(self.__anim_entity, self._initial_entity.z_index, self._target_entity.z_index)

    def update(self, t: float) -> None:
        self.__builder.uniform('t').set(t)
        self.__anim_entity._paint.setShader(self.__builder.makeShader())
        super().update(t)

    def end(self) -> None:
        self.__anim_entity._replace(self._target_entity)


class FadeInOut(__SwapAnim[Entity]):
    def __init__(self, from_: Entity, to: Entity, duration: float, **kwargs: Any) -> None:
        super().__init__(from_, to, duration, **kwargs)
        self.__initial_opacity: float = None  # type: ignore lateinit
        self.__target_opacity: float = None  # type: ignore lateinit

    def start(self) -> None:
        self._initial_entity._add_sibling(self._target_entity)
        self.__initial_opacity = self._initial_entity.style.opacity
        self.__target_opacity = self._target_entity.style.opacity
        self._target_entity.style.opacity = 0

        initial_pos = skia.Point(*self._initial_entity.pos)
        target_pos = skia.Point(*self._target_entity.pos)
        initial_mat = skia.Matrix()
        initial_mat.setFromMatrix(self._initial_entity.mat)
        target_mat = skia.Matrix()
        target_mat.setFromMatrix(self._target_entity.mat)
        self._add_pos_anim(self._initial_entity, initial_pos, target_pos)
        self._add_pos_anim(self._target_entity, initial_pos, target_pos)
        self._add_mat_anim(self._initial_entity, initial_mat, target_mat)
        self._add_mat_anim(self._target_entity, initial_mat, target_mat)
        self._add_z_index_anim(self._initial_entity, self._initial_entity.z_index, self._target_entity.z_index)
        self._add_z_index_anim(self._target_entity, self._initial_entity.z_index, self._target_entity.z_index)

    def update(self, t: float) -> None:
        self._initial_entity.style.opacity = self.__initial_opacity * (1 - t)
        self._target_entity.style.opacity = self.__target_opacity * t
        super().update(t)

    def end(self) -> None:
        self._target_entity.style.opacity = self.__target_opacity
        super().end()
        self._initial_entity._remove()


class Morph(__SwapAnim[PathEntity]):
    class __Entity(PathEntity):
        def __init__(self, entity: PathEntity) -> None:
            super().__init__()
            self._path = entity.built_path
            self.style = copy.copy(entity.style)  # type: ignore initialize style for animation

        def on_build_path(self, path: skia.Path) -> None:
            path.addPath(self._path)

    def __init__(
        self,
        from_: PathEntity,
        to: PathEntity,
        duration: float,
        dist_factor: float = 1.0,
        match_type: skia.PathMatcher.MatchType = skia.PathMatcher.MatchType.split,
        **kwargs: Any,
    ) -> None:
        super().__init__(from_, to, duration, **kwargs)
        self.__anim_entity: PathEntity = None  # type: ignore lateinit
        self.__dist_factor: float = dist_factor
        self.__match_type: skia.PathMatcher.MatchType = match_type
        self.__matcher: skia.PathMatcher = None  # type: ignore lateinit
        self.__style_anim: StyleAnim = None  # type: ignore lateinit

    def start(self) -> None:
        self._target_entity.set_scene(self._initial_entity._scene)

        self.__matcher = skia.PathMatcher(
            self._initial_entity.built_path, self._target_entity.built_path, self.__dist_factor, self.__match_type
        )

        self.__anim_entity = Morph.__Entity(self._initial_entity)
        self._initial_entity._replace(self.__anim_entity)
        self._add_pos_anim(self.__anim_entity, self._initial_entity.pos, self._target_entity.pos)
        self._add_mat_anim(self.__anim_entity, self._initial_entity.mat, self._target_entity.mat)
        self._add_z_index_anim(self.__anim_entity, self._initial_entity.z_index, self._target_entity.z_index)
        self.__style_anim = StyleAnim(
            self.__anim_entity, self._target_entity.style, self._duration, ease=self.ease_func
        )
        self.__style_anim.start()

    def update(self, t: float) -> None:
        self.__matcher.interpolate(t, self.__anim_entity.path)
        super().update(t)
        self.__style_anim.update(t)

    def end(self) -> None:
        self.__anim_entity._replace(self._target_entity)
