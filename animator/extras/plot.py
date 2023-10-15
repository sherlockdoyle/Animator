from __future__ import annotations

import math
from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Callable

import numpy as np
from numpy.typing import ArrayLike

from animator import skia
from animator._common_types import ColorLike, PointLike
from animator.anim import Anim
from animator.entity import Entity
from animator.graphics import color as parse_color
from animator.scene import Scene

if TYPE_CHECKING:
    from animator.skia import _Rect


class _Artist:
    def __init__(self, parent: Plot, c: ColorLike | None = None, sw: float = 3) -> None:
        self._parent: Plot = parent
        self._color: skia.Color4f = skia.uniqueColor(50) if c is None else parse_color(c)
        self._stroke_width: float = sw

    @abstractmethod
    def _draw(self, canvas: skia.Canvas, matrix: skia.Matrix) -> None:
        pass


def _increase_size_if_needed(array: np.ndarray, size: int) -> np.ndarray:
    if array.shape[0] < size:
        array = np.vstack((array, array[::-1]))
        if array.shape[0] < size:
            return np.resize(array, (size, array.shape[1]))
        return array[:size]
    return array


class _Point_Anim(Anim):
    def __init__(self, artist: _PointArtist, data: np.ndarray, duration: float, **kwargs: Any) -> None:
        super().__init__(duration, **kwargs)
        self.__artist: _PointArtist = artist
        self.__target_data: np.ndarray = data
        self.__initial_common_data: np.ndarray = None  # type: ignore lateinit
        self.__diff_common_data: np.ndarray = None  # type: ignore lateinit

    def start(self) -> None:
        max_len = max(self.__artist._data.shape[0], self.__target_data.shape[0])
        self.__initial_common_data = _increase_size_if_needed(self.__artist._data, max_len)
        self.__diff_common_data = _increase_size_if_needed(self.__target_data, max_len) - self.__initial_common_data
        self.__artist._parent.ion()

    def update(self, t: float) -> None:
        self.__artist._data = self.__initial_common_data + self.__diff_common_data * t

    def end(self) -> None:
        self.__artist._data = self.__target_data
        self.__artist._parent.ioff()


def _sanitize_scatter_data(x_data: ArrayLike, y_data: ArrayLike) -> np.ndarray:
    x_data = np.array(x_data, dtype=np.float32)
    y_data = np.array(y_data, dtype=np.float32)
    if x_data.ndim != 1 or y_data.ndim != 1 or x_data.size != y_data.size:
        raise ValueError('Scatter requires 2 equal sized 1D arrays.')
    return np.vstack((x_data, y_data)).T


class _PointArtist(_Artist):
    def __init__(self, data: np.ndarray, *args: Any, **kwargs: Any) -> None:
        """
        :param data: Data to plot of shape (2, n).
        """
        super().__init__(*args, **kwargs)
        self._data: np.ndarray = data

    def _draw(self, canvas: skia.Canvas, matrix: skia.Matrix) -> None:
        self._parent.style.stroke_paint.setColor4f(self._color)
        self._parent.style.stroke_paint.setStrokeWidth(2 * self._stroke_width)
        skia.plot.Canvas_drawPoints(
            canvas, skia.Canvas.PointMode.kPoints_PointMode, self._data.copy(), matrix, self._parent.style.stroke_paint
        )

    def set_data(self, x_data: ArrayLike, y_data: ArrayLike) -> None:
        """Set data to plot. Takes the same data as :meth:`Plot.scatter`."""
        self._data = _sanitize_scatter_data(x_data, y_data)
        self._parent._mark_dirty()

    def animate_set_data(self, x_data: ArrayLike, y_data: ArrayLike, duration: float, **kwargs: Any) -> _Point_Anim:
        """
        Animate the points in the plot to a new set of points. Takes the same data as :meth:`set_data` and
        :class:`Anim`.
        """
        return _Point_Anim(self, _sanitize_scatter_data(x_data, y_data), duration, **kwargs)


class _Line_Anim(Anim):
    def __init__(self, artist: _LineArtist, data: np.ndarray, duration: float, **kwargs: Any) -> None:
        super().__init__(duration, **kwargs)
        self.__artist: _LineArtist = artist
        self.__target_path: skia.Path = skia.plot.Point_Polygon(data, False)
        self.__initial_aligned_path: skia.Path = None  # type: ignore lateinit
        self.__target_aligned_path: skia.Path = None  # type: ignore lateinit

    def start(self) -> None:
        matcher = skia.LinearSegment(self.__artist._path, self.__target_path)
        self.__initial_aligned_path = matcher.mPath0
        self.__target_aligned_path = matcher.mPath1
        self.__artist._parent.ion()

    def update(self, t: float) -> None:
        self.__artist._path = self.__target_aligned_path.interpolate(self.__initial_aligned_path, t)  # type: ignore aligned path will always be interpolatable

    def end(self) -> None:
        self.__artist._path = self.__target_path
        self.__artist._parent.ioff()


def _sanitize_plot_data(data: tuple[ArrayLike, ...]) -> np.ndarray:
    array = np.array(data, dtype=np.float32).squeeze()
    if array.ndim == 0:
        raise ValueError('Plot requires at least two points.')
    if array.ndim == 1:
        array = np.vstack((np.arange(len(array), dtype=np.float32), array))
    elif array.ndim > 2:
        raise ValueError('Plot requires at most two dimensions.')
    return array.T.copy()


class _LineArtist(_Artist):
    def __init__(self, data: np.ndarray, *args: Any, **kwargs: Any) -> None:
        """
        :param data: Data to plot of shape (2, n).
        """
        super().__init__(*args, **kwargs)
        self._path: skia.Path = skia.plot.Point_Polygon(data, False)

    def _draw(self, canvas: skia.Canvas, matrix: skia.Matrix) -> None:
        self._parent.style.stroke_paint.setColor4f(self._color)
        self._parent.style.stroke_paint.setStrokeWidth(self._stroke_width)
        canvas.drawPath(self._path.makeTransform(matrix), self._parent.style.stroke_paint)

    def set_data(self, *args: ArrayLike) -> None:
        """Set data to plot. Takes the same data as :meth:`Plot.plot`."""
        self._path = skia.plot.Point_Polygon(_sanitize_plot_data(args), False)
        self._parent._mark_dirty()

    def animate_set_data(self, args: tuple[ArrayLike, ...], duration: float, **kwargs: Any) -> _Line_Anim:
        """
        Animate the plot to a new plot. Takes the same data as :meth:`set_data` and :class:`Anim`. However, instead of
        just passing the data, a tuple of data needs to be passed. This is because of the *duration* parameter. So, if
        you call ``set_data(a, b, c, d)``, you need to call ``animate_set_data((a, b, c, d), duration, ...)`` instead.
        """
        return _Line_Anim(self, _sanitize_plot_data(args), duration, **kwargs)


class _FuncArtist(_Artist):
    def __init__(self, func: Callable[[float], float], *args: Any, **kwargs: Any) -> None:
        """
        :param func: Function to plot of type :math:`y = f(x)`.
        """
        super().__init__(*args, **kwargs)
        self.__func = np.vectorize(func, otypes=[np.float32])

    def _draw(self, canvas: skia.Canvas, matrix: skia.Matrix) -> None:
        origin = matrix.mapOrigin()
        scale = matrix.mapVector(1, -1)
        x = np.linspace(0, self._parent.width, math.ceil(self._parent.width) + 1, dtype=np.float32)
        y = origin.fY - self.__func((x - origin.fX) / scale.fX) * scale.fY
        self._parent.style.stroke_paint.setColor4f(self._color)
        self._parent.style.stroke_paint.setStrokeWidth(self._stroke_width)
        canvas.drawPath(skia.plot.Point_Polygon(np.vstack((x, y)).T.copy(), False), self._parent.style.stroke_paint)


class _ZoomAnim(Anim):
    def __init__(self, entity: Plot, bounds: skia.Rect, duration: float, **kwargs: Any) -> None:
        super().__init__(duration, **kwargs)
        self.__entity: Plot = entity
        self.__target_bounds: skia.Rect = bounds
        self.__initial_bounds: skia.Rect = None  # type: ignore lateinit
        self.__diff_l: float = None  # type: ignore lateinit
        self.__diff_t: float = None  # type: ignore lateinit
        self.__diff_r: float = None  # type: ignore lateinit
        self.__diff_b: float = None  # type: ignore lateinit

    def start(self) -> None:
        self.__initial_bounds = skia.Rect(*self.__entity.bounds)
        self.__diff_l = self.__target_bounds.fLeft - self.__initial_bounds.fLeft
        self.__diff_t = self.__target_bounds.fTop - self.__initial_bounds.fTop
        self.__diff_r = self.__target_bounds.fRight - self.__initial_bounds.fRight
        self.__diff_b = self.__target_bounds.fBottom - self.__initial_bounds.fBottom
        self.__entity.ion()

    def update(self, t: float) -> None:
        self.__entity.bounds.setLTRB(
            self.__initial_bounds.fLeft + self.__diff_l * t,
            self.__initial_bounds.fTop + self.__diff_t * t,
            self.__initial_bounds.fRight + self.__diff_r * t,
            self.__initial_bounds.fBottom + self.__diff_b * t,
        )

    def end(self) -> None:
        self.__entity.bounds.setLTRB(*self.__target_bounds)
        self.__entity.ioff()


def _clamp(value: float, min_value: float, max_value: float) -> float:
    return min_value if value < min_value else max_value if value > max_value else value


def _nice_number(value: float) -> float:
    exp = math.floor(math.log10(value))
    frac = value / (10**exp)
    if frac < 1.5:
        frac = 1
    elif frac < 3:
        frac = 2
    elif frac < 7:
        frac = 5
    else:
        frac = 10
    return frac * (10**exp)


_TEXT_FONT = skia.Font()


class Plot(Entity):
    """
    This provides a very basic matplotlib like interface for plotting and animating simple graphs. This entity does not
    draw anything by default. Call any of the plot methods to draw a graph. The ``stroke_paint`` is used for plotting
    and the ``fill_paint`` is used for drawing the grid.
    """

    def __init__(
        self,
        width: float | None = None,
        height: float | None = None,
        bounds: _Rect | None = None,
        padding: float = 25,
        tick_spacing: float | None = None,
        pos: PointLike = (0, 0),
        **kwargs: Any,
    ) -> None:
        super().__init__(pos=pos, **kwargs)
        self.width: float = width  # type: ignore set in set_scene
        self.height: float = height  # type: ignore set in set_scene
        self.bounds: skia.Rect = None if bounds is None else skia.Rect(*bounds)  # type: ignore set in set_scene
        self.__rebound: bool = bounds is None
        self.padding: float = padding
        self.tick_spacing: float = padding * 4 if tick_spacing is None else tick_spacing

        self.__is_interactive: bool = False
        self.__artists: list[_Artist] = []
        if 'fill_color' not in kwargs:
            self.style.fill_paint.setColor(skia.ColorLTGRAY)

        self.__grid_picture: skia.Picture | None = None
        self.__picture_recorder: skia.PictureRecorder = skia.PictureRecorder()
        self.__picture: skia.Picture | None = None

    def set_scene(self, scene: Scene) -> None:
        super().set_scene(scene)
        if self.width is None:
            self.width = scene.width
        if self.height is None:
            self.height = scene.height
        if self.bounds is None:
            self.bounds = skia.Rect(-scene.width / 2, -scene.height / 2, scene.width / 2, scene.height / 2)
            self.bounds.inset(self.padding, self.padding)

    def __build_grid(self, canvas: skia.Canvas, matrix: skia.Matrix) -> None:
        origin = matrix.mapOrigin()
        scale = matrix.mapVector(1, -1)
        tx = _nice_number(self.tick_spacing / scale.fX)
        ty = _nice_number(self.tick_spacing / scale.fY)
        dx = tx * scale.fX
        dy = ty * scale.fY

        self.style.fill_paint.setStrokeWidth(1)
        i = -math.floor(origin.fX / dx)
        l = (self.width - origin.fX) / dx
        while i < l:
            x = origin.fX + i * dx
            canvas.drawLine(x, 0, x, self.height, self.style.fill_paint)
            canvas.drawString(
                f'{i*tx:.5g}', x + 4, _clamp(origin.fY + 14, 12, self.height - 4), _TEXT_FONT, self.style.fill_paint
            )
            i += 1
        i = -math.floor(origin.fY / dy)
        l = (self.height - origin.fY) / dy
        while i < l:
            y = origin.fY + i * dy
            canvas.drawLine(0, y, self.width, y, self.style.fill_paint)
            text = f'{-i*ty:.5g}'
            canvas.drawString(
                text,
                _clamp(origin.fX + 4, 2, self.width - _TEXT_FONT.measureText(text)[0] - 2),
                y + 14,
                _TEXT_FONT,
                self.style.fill_paint,
            )
            i += 1

        self.style.fill_paint.setStrokeWidth(5)
        canvas.drawLine(0, origin.fY, self.width, origin.fY, self.style.fill_paint)
        canvas.drawLine(origin.fX, 0, origin.fX, self.height, self.style.fill_paint)

    def __build_plot(self, canvas: skia.Canvas) -> None:
        matrix = skia.Matrix.RectToRect(  # mathematical axis is flipped
            (self.bounds.fLeft, -self.bounds.fBottom, self.bounds.fRight, -self.bounds.fTop),
            (self.padding, self.padding, self.width - self.padding, self.height - self.padding),
        ).preScale(1, -1)
        if self.__is_interactive:
            self.__build_grid(canvas, matrix)
        else:
            if self.__grid_picture is None:
                grid_picture_recorder = skia.PictureRecorder()
                self.__build_grid(grid_picture_recorder.beginRecording(self.width, self.height), matrix)
                self.__grid_picture = grid_picture_recorder.finishRecordingAsPicture()
            canvas.drawPicture(self.__grid_picture)

        for artist in self.__artists:
            artist._draw(canvas, matrix)

    def on_draw(self, canvas: skia.Canvas) -> None:
        canvas.translate(self.offset.fX, self.offset.fY)
        if self.__is_interactive:
            self.__build_plot(canvas)
        else:
            if self._is_dirty or self.__picture is None:
                self.__build_plot(self.__picture_recorder.beginRecording(self.width, self.height))
                self.__picture = self.__picture_recorder.finishRecordingAsPicture()
                self._is_dirty = False
            canvas.drawPicture(self.__picture)

    def get_bounds(self, transformed: bool = False) -> skia.Rect:
        bounds = skia.Rect.MakeXYWH(self.offset.fX, self.offset.fY, self.width, self.height)
        if transformed:
            return self.mat.mapRect(bounds, skia.ApplyPerspectiveClip.kNo)
        return bounds

    def ion(self) -> None:
        """Enable interactive mode. Prepares for animations."""
        self.__is_interactive = True

    def ioff(self) -> None:
        """Disable interactive mode. Prepares for large number of plots."""
        self.__is_interactive = False
        self.__grid_picture = None  # clear the cache since contents may have changed during interactive mode
        self.__picture = None

    def clear_plots(self) -> None:
        """Clear all plots."""
        self.__artists.clear()

    def scatter(self, x_data: ArrayLike, y_data: ArrayLike, **kwargs: Any) -> _PointArtist:
        data = _sanitize_scatter_data(x_data, y_data)
        if self.__rebound:
            self.bounds = skia.Rect(*data.min(0), *data.max(0))
            self.__rebound = False

        artist = _PointArtist(data, self, **kwargs)
        self.__artists.append(artist)
        self._is_dirty = True
        return artist

    def plot(self, *args: ArrayLike, **kwargs: Any) -> _LineArtist:
        data = _sanitize_plot_data(args)
        if self.__rebound:
            self.bounds = skia.Rect(*data.min(0), *data.max(0))
            self.__rebound = False

        artist = _LineArtist(data, self, **kwargs)
        self.__artists.append(artist)
        self._is_dirty = True
        return artist

    def func_plot(self, func: Callable[[float], float], **kwargs: Any) -> _FuncArtist:
        artist = _FuncArtist(func, self, **kwargs)
        self.__artists.append(artist)
        self._is_dirty = True
        return artist

    def zoom(self, bounds: _Rect, duration: float, **kwargs: Any) -> _ZoomAnim:
        """Animate the bounds of the plot to a new bounds therby zooming in or out.

        :param bounds: Bounds to zoom to.
        :param duration: Duration of animation.
        """
        return _ZoomAnim(self, skia.Rect(*bounds), duration, **kwargs)
