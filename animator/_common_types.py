from typing import Sequence, Tuple

from animator import skia

PointLike = skia.Point | Tuple[float, float]
ColorLike = skia.Color4f | int | float | Sequence[float] | str
ClipLike = (
    skia.IRect
    | skia.Path
    | skia.RRect
    | skia.Rect
    | skia.Region
    | skia.Shader
    | tuple[()]
    | tuple[int, int]
    | tuple[int, int, int, int]
    | tuple[float, float]
    | tuple[float, float, float, float]
)
