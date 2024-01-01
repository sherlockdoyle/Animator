"""Misceleaneous entities."""
from typing import Any

from animator import skia
from animator._common_types import ClipLike, ColorLike, PointLike
from animator.entity.entity import Entity
from animator.graphics import Style
from animator.graphics import color as parse_color


class Vertices(Entity):
    """A collection of vertices drawn as triangles with the ``fill_paint``."""

    def __init__(
        self,
        positions: list[PointLike],
        colors: list[ColorLike] | None = None,
        mode: skia.Vertices.VertexMode = skia.Vertices.VertexMode.kTriangles_VertexMode,
        textures: list[PointLike] | None = None,
        indices: list[int] | None = None,
        blend_mode: skia.BlendMode | None = None,
        **kwargs: Any
    ):
        """
        :param positions: The positions of the vertices.
        :param colors: The colors for each vertex. If not provided, the fill paint's color is used.
        :param mode: The vertex mode. The default is ``kTriangles``.
        :param textures: The texture coordinates in the fill paint's shader space for each vertex.
        :param indices: The indices of the vertices to use to draw the triangles.
        :param blend_mode: The blend mode to use to blend the *colors* (if provided) with the fill paint. If *colors* is
            not provided, the default is ``kSrcOver``. Otherwise, the default is ``kDstOver``.
        """
        super().__init__(**kwargs)
        self.positions: list[skia.Point] = [skia.Point(*point) for point in positions]
        self.colors: list[skia.Color4f] | None = (
            [skia.Color4f(parse_color(color)) for color in colors] if colors else None
        )
        self.mode: skia.Vertices.VertexMode = mode
        self.textures: list[skia.Point] | None = [skia.Point(*point) for point in textures] if textures else None
        self.indices: list[int] | None = indices
        self.blend_mode: skia.BlendMode = (
            (skia.BlendMode.kSrcOver if colors is None else skia.BlendMode.kDstOver)
            if blend_mode is None
            else blend_mode
        )

        self.__vertices: skia.Vertices = None  # type: ignore lateinit
        self.__old_offset: skia.Point = skia.Point(*self.offset)

    def __build_vertices(self):
        if self._is_dirty or self.__old_offset != self.offset:
            self.__vertices = skia.Vertices(
                self.mode, skia.Point.Offset(self.positions, self.offset), self.textures, self.colors, self.indices
            )
            self._is_dirty = False
            self.__old_offset.set(*self.offset)

    def on_draw(self, canvas: skia.Canvas) -> None:
        self.__build_vertices()
        canvas.drawVertices(self.__vertices, self.blend_mode, self.style.fill_paint)

    def get_bounds(self, transformed: bool = False) -> skia.Rect:
        self.__build_vertices()
        bounds = self.__vertices.bounds()
        if transformed:
            return self.mat.mapRect(bounds, skia.ApplyPerspectiveClip.kNo)
        return bounds


class Patch(Entity):
    """A [Coons patch](https://en.wikipedia.org/wiki/Coons_patch) drawn with the ``fill_paint``."""

    def __init__(
        self,
        cubics: list[PointLike],
        colors: list[ColorLike] | None = None,
        textures: list[PointLike] | None = None,
        blend_mode: skia.BlendMode | None = None,
        **kwargs: Any
    ):
        """
        :param cubics: A list of 12 points specifying the 4 cubic Bézier curves starting at the top-left corner, going
            clockwise.
        :param colors: A list of 4 colors for each corner of the patch. If not provided, the fill paint's color is used.
        :param textures: A list of 4 points specifying the texture coordinates in the fill paint's shader space for each
            corner of the patch.
        :param blend_mode: The blend mode to use to blend the *colors* (if provided) with the fill paint. If *colors* is
            not provided, the default is ``kSrcOver``. Otherwise, the default is ``kDstOver``.
        """
        super().__init__(**kwargs)
        self.cubics: list[skia.Point] = [skia.Point(*point) for point in cubics]
        self.colors: list[skia.Color4f] | None = (
            [skia.Color4f(parse_color(color)) for color in colors] if colors else None
        )
        self.textures: list[skia.Point] | None = [skia.Point(*point) for point in textures] if textures else None
        self.blend_mode: skia.BlendMode = (
            (skia.BlendMode.kSrcOver if colors is None else skia.BlendMode.kDstOver)
            if blend_mode is None
            else blend_mode
        )

    def on_draw(self, canvas: skia.Canvas) -> None:
        canvas.drawPatch(
            skia.Point.Offset(self.cubics, self.offset),
            self.colors,
            self.textures,
            self.blend_mode,
            self.style.fill_paint,
        )

    def get_bounds(self, transformed: bool = False) -> skia.Rect:
        path = skia.Path().moveTo(self.cubics[0])
        path.cubicTo(self.cubics[1], self.cubics[2], self.cubics[3])
        path.cubicTo(self.cubics[4], self.cubics[5], self.cubics[6])
        path.cubicTo(self.cubics[7], self.cubics[8], self.cubics[9])
        path.cubicTo(self.cubics[10], self.cubics[11], self.cubics[0])
        path.close()
        path.offset(*self.offset)
        if transformed:
            path.transform(self.mat, skia.ApplyPerspectiveClip.kNo)
        return path.computeTightBounds()


class BackDrop(Entity):
    """
    Applies a backdrop filter to the content behind the entity. The ``stroke_paint`` and ``fill_paint`` are ignored.
    """

    def __init__(self, filter: skia.ImageFilter, clip: ClipLike | None = None, **kwargs: Any):
        """
        :param filter: The image filter to apply.
        :param clip: The bounds of the filter. If not provided, the filter is applied to the entire canvas.
        """
        super().__init__(**kwargs)
        self.filter: skia.ImageFilter = filter
        self.style.clip = clip

    def draw_self(self, canvas: skia.Canvas) -> None:
        if self.style.nothing_to_draw():
            return
        save_count = canvas.save()
        canvas.translate(*self.offset)
        self.style.apply_clip(canvas)

        optimization = self.style.optimization
        final_paint = self.style.final_paint
        paint = None
        if optimization == Style.FinalPaintOptimization.OPACITY_ONLY and final_paint.getAlpha() < 255:
            paint = skia.Paint(alphaf=final_paint.getAlphaf())
        elif (
            optimization == Style.FinalPaintOptimization.ALL and not final_paint.nothingToDraw()
        ) or optimization == Style.FinalPaintOptimization.ALWAYS:
            paint = final_paint
        canvas.saveLayer(skia.Canvas.SaveLayerRec(paint=paint, backdrop=self.filter))

        canvas.restoreToCount(save_count)

    def get_bounds(self, transformed: bool = False) -> skia.Rect:
        clip = self.style.clip
        if isinstance(clip, (skia.Path, skia.Region)):
            if isinstance(clip, skia.Path):
                path = clip.makeOffset(*self.offset)
            else:
                path = skia.Path()
                clip.makeTranslate(*self.offset).getBoundaryPath(path)
            if transformed:
                path.transform(self.mat, skia.ApplyPerspectiveClip.kNo)
            return path.computeTightBounds()
        if isinstance(clip, skia.Rect):
            bounds = skia.Rect(*clip)
        elif isinstance(clip, (skia.IRect, tuple)):
            bounds = skia.Rect(clip)
        elif isinstance(clip, skia.RRect):
            bounds = clip.getBounds()
        else:
            bounds = skia.Rect.MakeEmpty()
        bounds.offset(self.offset)
        if transformed:
            return self.mat.mapRect(bounds, skia.ApplyPerspectiveClip.kNo)
        return bounds
