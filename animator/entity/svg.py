"""SVGs! More complex graphics"""
from __future__ import annotations

__all__ = 'SimpleSVG',

from typing import Any, TYPE_CHECKING

from .entity import Entity
from .. import skia

if TYPE_CHECKING:
    from .._common_types import Point


class SimpleSVG(Entity):
    """Simplest way to display SVG. Not much control - can't change the elements, etc."""

    def __init__(self, path: str, size: Point | None = None, *args: Any, **kwargs: Any):
        """
        :param path: Path to the SVG file.
        :param size: Sometimes the SVG might not show up correctly because of incorrect size. In such cases,
            specify the size (width, height) manually.
        """
        super().__init__(*args, **kwargs)
        self.path: str = path

        with skia.FILEStream(path) as stream:
            self.__svgdom: skia.SVGDOM = skia.SVGDOM.MakeFromStream(stream)
        if size is not None:
            self.__svgdom.setContainerSize(size)

    def on_draw(self) -> None:
        self.scene.canvas.save()
        self.scene.canvas.concat(self.total_transformation.preTranslate(*self.offset))
        self.__svgdom.render(self.scene.canvas)
        self.scene.canvas.restore()

    def get_bounds(self, transformed: bool = False) -> skia.Rect:
        bounds = skia.Rect(*self.__svgdom.containerSize())
        bounds.offset(self.offset)
        if transformed:
            bounds = self.mat.mapRect(bounds, skia.ApplyPerspectiveClip.kNo)
        return bounds
