from __future__ import annotations

from functools import lru_cache
from typing import Any, Final, Literal, TypeVar

import matplotlib.style
import numpy as np
from matplotlib import font_manager
from matplotlib.axes import Axes
from matplotlib.backend_bases import FigureCanvasBase, GraphicsContextBase, RendererBase
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from matplotlib.path import Path
from matplotlib.text import Text
from matplotlib.textpath import TextToPath
from matplotlib.transforms import Affine2D, Affine2DBase, Bbox, Transform, TransformedPath
from matplotlib.typing import CapStyleType, ColorType, JoinStyleType
from numpy.typing import ArrayLike

from animator import skia
from animator._common_types import PointLike
from animator.entity import Entity
from animator.scene import Scene

_CAP_STYLE_2_SKIA: dict[CapStyleType, skia.Paint.Cap] = {
    'butt': skia.Paint.Cap.kButt_Cap,
    'projecting': skia.Paint.Cap.kSquare_Cap,
    'round': skia.Paint.Cap.kRound_Cap,
}
_JOIN_STYLE_2_SKIA: dict[JoinStyleType, skia.Paint.Join] = {
    'bevel': skia.Paint.Join.kBevel_Join,
    'miter': skia.Paint.Join.kMiter_Join,
    'round': skia.Paint.Join.kRound_Join,
}
_FONT_SLANT_2_SKIA: dict[str, skia.FontStyle.Slant] = {
    'normal': skia.FontStyle.Slant.kUpright_Slant,
    'italic': skia.FontStyle.Slant.kItalic_Slant,
    'oblique': skia.FontStyle.Slant.kOblique_Slant,
}


class _GraphicsContext(GraphicsContextBase):
    def __init__(self, renderer: _Renderer) -> None:
        super().__init__()
        self.__renderer = renderer

        self.paint: skia.Paint = skia.Paint(antiAlias=True)

    def restore(self) -> None:
        self.__renderer.canvas.restore()

    def get_antialiased(self) -> bool:
        return self.paint.isAntiAlias()

    def get_rgb(self) -> skia.Color4f:
        return self.paint.getColor4f()

    def set_alpha(self, alpha: float) -> None:
        super().set_alpha(alpha)
        self.paint.setAlphaf(1 if alpha is None else alpha)

    def set_antialiased(self, b: bool) -> None:
        self.paint.setAntiAlias(b)

    def set_capstyle(self, cs: CapStyleType) -> None:
        super().set_capstyle(cs)
        self.paint.setStrokeCap(_CAP_STYLE_2_SKIA[cs])

    def set_clip_rectangle(self, rectangle: Bbox | None) -> None:
        super().set_clip_rectangle(rectangle)
        if rectangle is not None:
            self.__renderer.canvas.clipRect(
                skia.Rect.MakeXYWH(rectangle.x0, rectangle.y0, rectangle.width, rectangle.height)
            )

    def set_clip_path(self, path: TransformedPath | None) -> None:
        super().set_clip_path(path)
        if path is not None:
            self.__renderer.canvas.clipPath(_make_path(*path.get_transformed_path_and_affine()))

    def set_dashes(self, dash_offset: float, dash_list: ArrayLike | None) -> None:
        super().set_dashes(dash_offset, dash_list)
        if dash_list is None:
            self.paint.setPathEffect(None)
        else:
            self.paint.setPathEffect(
                skia.DashPathEffect.Make(list(self.__renderer.points_to_pixels(dash_list)), dash_offset)  # type: ignore dash_list is numeric
            )

    def set_foreground(self, fg: ColorType, isRGBA: bool = False) -> None:
        super().set_foreground(fg, isRGBA)
        self.paint.setColor4f(skia.Color4f(self._rgb))  # type: ignore _rgb is present

    def set_joinstyle(self, js: JoinStyleType) -> None:
        super().set_joinstyle(js)
        self.paint.setStrokeJoin(_JOIN_STYLE_2_SKIA[js])

    def set_linewidth(self, w: float) -> None:
        super().set_linewidth(w)
        self.paint.setStrokeWidth(self.__renderer.points_to_pixels(w))


def _make_path(
    path: Path,
    transform: Transform,
    clip: skia.Rect | None = None,
    snap: bool | None = False,
    stroke_width: float = 1.0,
    sketch: tuple[float, float, float] | None = None,
) -> skia.Path:
    skia_path = skia.Path()
    for points, code in path.iter_segments(
        transform=transform,
        remove_nans=True,
        clip=None if clip is None else (clip.fLeft, clip.fTop, clip.fRight, clip.fBottom),
        snap=snap,
        stroke_width=stroke_width,
        sketch=sketch,
    ):
        if code == Path.MOVETO:
            skia_path.moveTo(*points)
        elif code == Path.CLOSEPOLY:
            skia_path.close()
        elif code == Path.LINETO:
            skia_path.lineTo(*points)
        elif code == Path.CURVE3:
            skia_path.quadTo(*points)
        elif code == Path.CURVE4:
            skia_path.cubicTo(*points)
    return skia_path


T = TypeVar('T', bound=ArrayLike)


class _Renderer(RendererBase):
    def __init__(self, canvas: skia.Canvas, size: tuple[float, float], dpi: float) -> None:
        super().__init__()
        self.canvas = canvas
        self.width, self.height = size
        self.dpi = dpi

        self.__group_stack: list[str] = []

    def get_canvas_width_height(self) -> tuple[float, float]:
        return self.width, self.height

    def points_to_pixels(self, points: T) -> T:
        return np.array(points) * self.dpi / 72  # type: ignore points will be numeric

    def new_gc(self) -> GraphicsContextBase:
        self.canvas.save()
        return _GraphicsContext(self)

    def __fill_and_stroke(self, path: skia.Path, gc: _GraphicsContext, fill_c: ColorType | None):
        if fill_c is not None:
            paint = skia.Paint(gc.paint)
            if len(fill_c) == 3 or gc.get_forced_alpha():
                paint.setColor4f(skia.Color4f(fill_c[0], fill_c[1], fill_c[2], gc.get_alpha()))  # type: ignore fill_c is a tuple
            else:
                paint.setColor4f(skia.Color4f(fill_c[0], fill_c[1], fill_c[2], fill_c[3]))  # type: ignore fill_c is a tuple
            paint.setStroke(False)
            self.canvas.drawPath(path, paint)

        if hatch := gc.get_hatch_path():
            self.canvas.save()
            self.canvas.clipPath(path)
            rect = skia.Rect.MakeWH(self.width, self.height)
            rect.outset(self.dpi, self.dpi)
            self.canvas.drawRect(
                rect,
                skia.Paint(
                    antiAlias=True,
                    color4f=skia.Color4f(*gc.get_hatch_color()),  # type: ignore hatch_color is a tuple
                    style=skia.Paint.Style.kStrokeAndFill_Style,
                    strokeWidth=gc.get_hatch_linewidth(),
                    pathEffect=skia.Path2DPathEffect.Make(
                        skia.Matrix.Scale(self.dpi, self.dpi), _make_path(hatch, Affine2D().scale(self.dpi))
                    ),
                ),
            )
            self.canvas.restore()

        if gc.paint.getStrokeWidth() > 0:
            gc.paint.setStroke(True)
            self.canvas.drawPath(path, gc.paint)

    def draw_path(
        self, gc: _GraphicsContext, path: Path, transform: Transform, rgbFace: ColorType | None = None
    ) -> None:
        clip = self.canvas.getLocalClipBounds() if rgbFace is None and gc.get_hatch() is None else None
        self.__fill_and_stroke(
            _make_path(path, transform, clip, gc.get_snap(), gc.get_linewidth(), gc.get_sketch_params()), gc, rgbFace
        )

    def draw_markers(
        self,
        gc: _GraphicsContext,
        marker_path: Path,
        marker_trans: Transform,
        path: Path,
        trans: Transform,
        rgbFace: ColorType | None = None,
    ) -> None:
        skia_marker_path = _make_path(marker_path, marker_trans)
        skia_path = skia.Path()
        for i, (vertices, _) in enumerate(path.iter_segments(trans, simplify=False)):
            x, y = vertices[-2:]
            skia_path.addPath(skia_marker_path, x, y)
            if i % 1000 == 999:
                self.__fill_and_stroke(skia_path, gc, rgbFace)
                skia_path.reset()
        self.__fill_and_stroke(skia_path, gc, rgbFace)

    def draw_image(
        self, gc: _GraphicsContext, x: float, y: float, im: np.ndarray, transform: Affine2DBase | None = None
    ) -> None:
        image = skia.Image.fromarray(im, copy=False)
        self.canvas.drawImage(image, x, y)

    def draw_gouraud_triangles(
        self, gc: _GraphicsContext, triangles_array: np.ndarray, colors_array: np.ndarray, transform: Transform
    ) -> None:
        vertices = skia.plot.Vertices__init__(
            transform.transform(triangles_array.reshape(-1, 2)).astype(np.float32),
            colors_array.reshape(-1, 4).astype(np.float32),
        )
        self.canvas.drawVertices(vertices, skia.BlendMode.kDstOver, skia.Paint(gc.paint))

    @lru_cache
    def __make_font_from_fname(self, fname: str, size: float) -> skia.Font:
        return skia.Font(skia.Typeface.MakeFromFile(fname), self.points_to_pixels(size))

    @lru_cache
    def __make_font_from_prop(self, prop: FontProperties) -> skia.Font:
        weight = prop.get_weight()
        width = prop.get_stretch()
        return skia.Font(
            skia.Typeface(
                prop.get_name(),
                skia.FontStyle(
                    weight=font_manager.weight_dict.get(weight, weight),  # type: ignore return will always be int
                    width=round(font_manager.stretch_dict.get(width, width) / 100),  # type: ignore return will always be int
                    slant=_FONT_SLANT_2_SKIA[prop.get_slant()],
                ),
            ),
            self.points_to_pixels(prop.get_size()),
        )

    def draw_text(
        self,
        gc: _GraphicsContext,
        x: float,
        y: float,
        s: str,
        prop: FontProperties,
        angle: float,
        ismath: bool | Literal['TeX'] = False,
        mtext: Text | None = None,
    ) -> None:
        self.canvas.save()
        self.canvas.scale(1, -1)
        self.canvas.translate(0, -self.height)
        self.canvas.rotate(-angle, x, y)

        if ismath:  # this may be slower, but it looks better
            text2path: TextToPath = self._text2path  # type: ignore _text2path exists
            _, _, _, glyphs, rects = text2path.mathtext_parser.parse(s, self.dpi, prop)

            for font, fontsize, glyph, ox, oy in glyphs:
                self.canvas.drawText(
                    chr(glyph), x + ox, y - oy, self.__make_font_from_fname(font.fname, fontsize), gc.paint
                )

            for ox, oy, w, h in rects:
                self.canvas.drawRect(
                    skia.Rect.MakeXYWH(x + ox, y - oy - h * 1.15, w, h),  # extra 0.15 shift to make it look nicer
                    gc.paint,
                )
        else:
            self.canvas.drawText(s, x, y, self.__make_font_from_prop(prop), gc.paint)

        self.canvas.restore()

    def get_text_width_height_descent(
        self, s: str, prop: FontProperties, ismath: bool | Literal['TeX']
    ) -> tuple[float, float, float]:
        if ismath:
            return super().get_text_width_height_descent(s, prop, ismath)

        width, rect = self.__make_font_from_prop(prop).measureText(s)
        return width, rect.height(), rect.fBottom


class _Canvas(FigureCanvasBase):
    def draw(self, canvas: skia.Canvas) -> None:
        save_count = canvas.save()
        canvas.translate(0, self.figure.bbox.height)
        canvas.scale(1, -1)
        self.figure.draw(_Renderer(canvas, self.figure.bbox.size, self.figure.dpi))
        canvas.restore()
        # kept for debugging this experiemental entity
        assert save_count == canvas.getSaveCount(), 'unbalanced save/restore, should not happen'


class Mpl(Entity):
    """Matplotlib wrapper for Animator.

    :ivar figure: The internal figure object. Use this to draw.
    """

    @staticmethod
    def set_dark_mode() -> None:
        """Sets the matplotlib style to dark mode.

        :note: This sets the style globally.
        """
        matplotlib.style.use('dark_background')

    def __init__(
        self,
        figsize: tuple[float, float] | None = None,
        dpi: float | None = None,
        figure_kw: dict[str, Any] = {},
        pos: PointLike = (0, 0),
        **kwargs: Any,
    ) -> None:
        """
        :param figsize: The size of the figure in **inches** (not pixels). Defaults to the size of the scene.
        :param dpi: The resolution of the figure.
        :param figure_kw: Keyword arguments to pass to :meth:`matplotlib.figure.Figure.__init__`.
        """
        super().__init__(pos=pos, **kwargs)
        self.figure: Final[Figure] = Figure(figsize=figsize, dpi=dpi, **figure_kw)
        self.__canvas: _Canvas = _Canvas(self.figure)
        self.__do_set_figsize = figsize is None

    def set_scene(self, scene: Scene) -> None:
        super().set_scene(scene)
        if self.__do_set_figsize:
            self.figure.set_size_inches(scene.width / self.figure.dpi, scene.height / self.figure.dpi)
            self.__do_set_figsize = False

    @property
    def ax(self) -> Axes:
        """
        The current axes. Use this to draw. Calls :meth:`matplotlib.figure.Figure.gca`. Alternatively, create your own
        axes from the ``figure`` attribute.
        """
        return self.figure.gca()

    def on_draw(self, canvas: skia.Canvas) -> None:
        self.__canvas.draw(canvas)

    def get_bounds(self, transformed: bool = False) -> skia.Rect:
        bounds = skia.Rect.MakeXYWH(*self.figure.bbox.bounds)
        if transformed:
            return self.mat.mapRect(bounds, skia.ApplyPerspectiveClip.kNo)
        return bounds
