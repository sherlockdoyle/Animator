"""Entities for images."""
from __future__ import annotations

from typing import Any, BinaryIO, Literal, TypeVar

import numpy as np

from animator import skia
from animator._common_types import PointLike
from animator.entity.entity import Entity

IT = TypeVar('IT', bound='Image')


class Image(Entity):
    """Image entity only uses ``fill_paint``."""

    def __init__(
        self,
        path: str | BinaryIO | skia.Image,
        width: int | None = None,
        height: int | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Create an image entity from the given *path*. If both *width* and *height* are ``None``, they will be set to the
        image's original dimensions. If both are given, the image will be scaled to fit.

        :param path: Path to image, a file-like object, or a :class:`skia.Image` object.
        :param width: Width of image. If ``None``, will be calculated from *height* to preserve aspect ratio.
        :param height: Height of image. If ``None``, will be calculated from *width* to preserve aspect ratio.
        """
        super().__init__(**kwargs)
        self.__image = path if isinstance(path, skia.Image) else skia.Image.open(path)

        self.width = self.__image.width() if width is None else width
        self.height = self.__image.height() if height is None else height
        if width is None and height is not None:
            self.width = self.__image.width() * height // self.__image.height()
        if height is None and width is not None:
            self.height = self.__image.height() * width // self.__image.width()

        self.sampling_options = skia.SamplingOptions(skia.CubicResampler.Mitchell())
        self.__ndarray: np.ndarray | None = None

    def get_shader(
        self,
        tmx: skia.TileMode = skia.TileMode.kDecal,
        tmy: skia.TileMode = skia.TileMode.kDecal,
        sampling: skia.SamplingOptions | None = None,
        localMatrix: Literal['current'] | skia.Matrix | None = None,
    ) -> skia.Shader:
        """Get the shader representation of the image.

        :param tmx: Tile mode in the x direction.
        :param tmy: Tile mode in the y direction.
        :param sampling: Sampling options. If ``None``, the default sampling options will be used.
        :param localMatrix: Local matrix to apply to the shader. If ``'current'``, the entity's current transformation
            matrix will be used.
        """
        return self.__image.makeShader(
            tmx,
            tmy,
            self.sampling_options if sampling is None else sampling,
            self.total_transformation if localMatrix == 'current' else localMatrix,
        )

    @property
    def ndarray(self) -> np.ndarray:
        """
        Numpy array representation of the image. Calling this property will convert the internal image to a raster
        image. The returned array is a view of the image's pixels, so modifying it will modify the image.
        """
        if self.__ndarray is None:
            self.__image = self.__image.makeRasterImage()
            self.__ndarray = np.array(self.__image, copy=False)
        return self.__ndarray

    def scale_image(self: IT, sx: float = 1, sy: float | None = None) -> IT:
        """
        Scale the image inline by the given factors. Calling this method will convert the internal image to a raster
        image.
        """
        if sy is None:
            sy = sx
        self.width = round(self.__image.width() * sx)
        self.height = round(self.__image.height() * sy)
        self.__image = self.__image.resize(self.width, self.height, self.sampling_options)

        self.__ndarray = None
        return self

    def resize(self: IT, width: int | None = None, height: int | None = None) -> IT:
        """
        Resize the image inline to the given dimensions. Calling this method will convert the internal image to a raster
        image.
        """
        if width is None and height is None:
            raise ValueError('At least one of width and height must be given.')
        self.width = self.__image.width() * height // self.__image.height() if width is None else width  # type: ignore height is not None
        self.height = self.__image.height() * width // self.__image.width() if height is None else height  # type: ignore width is not None
        self.__image = self.__image.resize(self.width, self.height, self.sampling_options)
        self.__ndarray = None
        return self

    def on_draw(self, canvas: skia.Canvas) -> None:
        canvas.drawImageRect(
            self.__image,
            skia.Rect.MakeXYWH(self.offset.fX, self.offset.fY, self.width, self.height),
            self.sampling_options,
            self.style.fill_paint,
        )

    def get_bounds(self, transformed: bool = False) -> skia.Rect:
        bounds = skia.Rect.MakeXYWH(self.offset.fX, self.offset.fY, self.width, self.height)
        if transformed:
            return self.mat.mapRect(bounds, skia.ApplyPerspectiveClip.kNo)
        return bounds


class Snapshot(Entity):
    """
    Snapshot of a part of the scene that has already been drawn by entities before this one. This entity neither uses
    ``fill_paint`` nor ``stroke_paint``.
    """

    def __init__(self, bounds: skia.IRect | tuple[int, int, int, int], **kwargs: Any) -> None:
        """
        :param bounds: Bounds of the snapshot.
        """
        super().__init__(**kwargs)
        self.bounds: skia.IRect = skia.IRect(*bounds)
        self.sampling_options = skia.SamplingOptions()

    def on_draw(self, canvas: skia.Canvas) -> None:
        bitmap = skia.Bitmap()
        bitmap.allocN32Pixels(self.bounds.width(), self.bounds.height())
        canvas.readPixels(bitmap, self.bounds.left(), self.bounds.top())
        canvas.drawImage(bitmap.asImage(), self.offset.fX, self.offset.fY, self.sampling_options)

    def get_bounds(self, transformed: bool = False) -> skia.Rect:
        bounds = skia.Rect.MakeXYWH(self.offset.fX, self.offset.fY, self.bounds.width(), self.bounds.height())
        if transformed:
            return self.mat.mapRect(bounds, skia.ApplyPerspectiveClip.kNo)
        return bounds


class PaintFill(Entity):
    """Fills the whole scene with the ``fill_paint``."""

    def __init__(self, pos: PointLike = (0, 0), **kwargs: Any) -> None:
        super().__init__(pos=pos, **kwargs)

    def on_draw(self, canvas: skia.Canvas) -> None:
        canvas.drawPaint(self.style.fill_paint)

    def get_bounds(self, transformed: bool = False) -> skia.Rect:
        return skia.Rect.MakeEmpty()
