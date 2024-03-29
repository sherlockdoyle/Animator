from __future__ import annotations

import re
from contextlib import contextmanager
from pathlib import Path
from typing import Callable, Iterator, TypeVar

import numpy as np

from animator import skia
from animator.display import DisplayManager
from animator.entity import Entity
from animator.entity.entity_list import EntityList
from animator.entity.relpos import RelativePosition
from animator.graphics import Context2d
from animator.util.env import inside_notebook

UpdateCallback = TypeVar('UpdateCallback', bound=Callable[[], bool | None])


_name2px: dict[str, tuple[int, int]] = {
    '144p': (256, 144),
    '240p': (426, 240),
    '360p': (640, 360),
    '480p': (854, 480),
    '720p': (1280, 720),
    'hd': (1280, 720),
    '1080p': (1920, 1080),
    'fhd': (1920, 1080),
    'fullhd': (1920, 1080),
    '1440p': (2560, 1440),
    '2k': (2560, 1440),
    '2160p': (3840, 2160),
    '4k': (3840, 2160),
    'uhd': (3840, 2160),
    'ultrahd': (3840, 2160),
}
_ext2format: dict[str, skia.EncodedImageFormat] = {
    'png': skia.EncodedImageFormat.kPNG,
    'jpg': skia.EncodedImageFormat.kJPEG,
    'jpeg': skia.EncodedImageFormat.kJPEG,
    'webp': skia.EncodedImageFormat.kWEBP,
}
_clear_paint: skia.Paint = skia.Paint(blendMode=skia.BlendMode.kClear)


class Scene:
    """The scene class. This is the main class for creating animations. It initializes a frame and a canvas to draw on,
    and provides methods for displaying and saving them.

    :ivar width: The width of the frame/scene.
    :ivar height: The height of the frame/scene.
    :ivar fps: The FPS used for animations.
    :ivar frame: The internal frame (array) used for drawing. The data type is in RGBA format.
    :ivar canvas: The :class:`skia.Canvas` used for drawing.
    :ivar bgcolor: The background color of the scene. This is used when clearing the scene after each frame.
    """

    def __init__(
        self, width: int | str = 854, height: int = 480, fps: float = 30, scale: float | tuple[int, int] | str = 1
    ) -> None:
        """
        :param width: The width of the frame/scene or a string representing a resolution. Resolutions can be one of
        '144p', '240p', '360p', '480p', '720p', 'hd', '1080p', 'fhd', 'fullhd', '1440p', '2k', '2160p', '4k', 'uhd',
        'ultrahd'. The resolution strings are case-insensitive and may contain whitespaces.
        :param height: The height of the frame/scene.
        :param fps: The FPS used for saving the animation. The FPS used for displaying the animation may be different.
        :param scale: Amount to scale the frame up or down. This can be a float, in which case the frame is scaled by
            that amount, or a tuple of two integers, in which case the frame is scaled to that size. This can also be a
            string representing a resolution (see `width` parameter). During displaying animations a large frame may
            cause lag or not fit on the screen. This factor is used to scale the frame down. By specifying a value >1,
            the frame can also be scaled up. If the aspect ratio of the frame is different from that of the scene, the
            frame will be centered.
        """
        if isinstance(width, str):
            width = re.sub(r'[\W+]+', '', width.lower())
            width, height = _name2px[width]
        self.width: int = width
        self.height: int = height

        if isinstance(scale, (str, tuple)):
            if isinstance(scale, str):
                scale = _name2px[re.sub(r'[\W+]+', '', scale.lower())]
            frame_width, frame_height = scale
        else:
            frame_width = int(width * scale)
            frame_height = int(height * scale)
        self.frame: np.ndarray = np.zeros(shape=(frame_height, frame_width, 4), dtype=np.uint8)
        self.canvas = skia.Canvas(self.frame)
        scale = min(frame_width / width, frame_height / height)
        self.canvas.translate((frame_width - width * scale) / 2, (frame_height - height * scale) / 2)
        self.canvas.scale(scale, scale)

        self.fps: float = fps

        self.entities: EntityList = EntityList()
        self.bgcolor: skia.Color4f = skia.Color4f.kBlack
        self.__context2d: Context2d | None = None

        self.__update_func: Callable[[], bool | None] | None = None

    def clear(self) -> None:
        """Clears the frame and fills it with transparency."""
        self.canvas.drawPaint(_clear_paint)

    def clear_with_bgcolor(self) -> None:
        """Clears the frame and fills it with the background color."""
        self.canvas.clear(self.bgcolor)

    def add(self, *entities: Entity) -> None:
        """Add one or more entities to the scene.

        :param entities: The entities to add.
        """
        self.entities.extend(entities)
        for entity in entities:
            entity.set_scene(self)

    def __matmul__(self, entity: Entity) -> Entity:
        """Sets the scene of an entity withouth adding it to the scene."""
        entity.set_scene(self)
        return entity

    __rmatmul__ = __matmul__

    @property
    def context2d(self) -> Context2d:
        """An instance of :class:`Context2d` wrapping the canvas. A :class:`Context2d` wraps a :class:`skia.Canvas` and
        provides additional methods for drawing. A scene contains a single :class:`Context2d` instance, which can be
        accessed through this method."""
        if self.__context2d is None:
            self.__context2d = Context2d(self.canvas)
        return self.__context2d

    def on_update(self, func: UpdateCallback) -> UpdateCallback:
        """Registers a function to be called before each frame is drawn. This function can be used to update the scene
        and its entities.

        :param func: The function to call. If the function returns ``True``, the animation will stop.
        """
        self.__update_func = func
        return func

    def update(self) -> bool:
        """Updates the scene. This method is called before each frame is drawn. It draws all entities in the scene.

        :return: ``False`` if the animation should stop, ``True`` otherwise.
        """
        self.clear_with_bgcolor()
        more = True if self.__update_func is None else not self.__update_func()
        for entity in self.entities:
            entity.draw()
        return more

    def show_frame(self) -> None:
        """Displays the current frame."""
        manager = DisplayManager.get_best()(self)
        while manager.show_frame():
            pass
        manager.close()

    def save_frame(self, path: str, quality: int = 100) -> None:
        """Saves the current frame to a file.

        :param path: The path to the file. The path may contain a ``{}`` placeholder, which will be replaced with the
            current frame number.
        :param quality: The quality of the image, between 0 and 100. Defaults to 100."""
        path_obj = Path(path.format(0)).expanduser().resolve()
        ext = path_obj.suffix[1:]
        try:
            skia.Image.fromarray(self.frame, copy=False).save(str(path_obj), _ext2format[ext], quality)
        except KeyError:
            raise ValueError(f'Unsupported file extension: {ext}')

    def play_frames(self, delay: float | None = None, keep_open: bool = True) -> None:
        """Plays the animation by displaying each frame in the scene.

        :param delay: The delay between frames in seconds. If ``None``, the delay is set to ``1 / fps``. If ``0``, the
            animation is played as fast as possible.
        :param keep_open: Whether to keep the animation open after playing. To close the animation, press ``Esc`` or
            close the window.
        """
        if delay is None:
            delay = 1 / self.fps
        manager = DisplayManager.get_best()(self, delay)
        while self.update() and manager.show_frame():
            pass
        if keep_open:
            while manager.show_frame():
                pass
        manager.close()

    @contextmanager
    def quickdraw(self) -> Iterator[Context2d]:
        """A simple way to quickly draw something on the scene. This method clears the scene and returns a
        :class:`Context2d` for drawing. When the context manager exits, the frame is displayed.

        >>> import animator as am
        >>> scene = am.Scene()
        >>> with scene.quickdraw() as ctx:
        ...     ctx.circle(scene.width / 2, scene.height / 2, 120)
        ...     ctx.fill()
        >>> # A circle is drawn at the center with a black background.
        """
        try:
            self.clear_with_bgcolor()
            yield self.context2d
        finally:
            if inside_notebook():
                from IPython.display import display

                display(self)
            else:
                self.show_frame()

    def r2a(self, pos: RelativePosition, padding: float = 25) -> skia.Point:
        """Convert a point from the scene's relative coordinate system to absolute coordinates.

        :param pos: The point in relative coordinates, a 2 element numpy array [x, y]. The coordinates are between -1
            and 1, where -1 is the left/top edge of the scene and 1 is the right/bottom edge.
        :param padding: The extra space around the scene, in pixels.
        :return: The point in absolute coordinates.
        """
        pos = (pos + 1) / 2
        return skia.Point(pos[0] * (self.width - 2 * padding) + padding, pos[1] * (self.height - 2 * padding) + padding)

    def r2a_bounds(
        self, bounds: skia.Rect, pos: RelativePosition, anchor: RelativePosition | None = None, padding: float = 25
    ) -> skia.Point:
        """Convert the position of a bounding box from the scene's relative coordinate system to absolute coordinates.

        :param bounds: The bounding box that is to be positioned.
        :param pos: The position of the bounding box in relative coordinates, a 2 element numpy array [x, y]. The
            coordinates are between -1 and 1, where -1 is the left/top edge of the scene and 1 is the right/bottom edge.
        :param anchor: The anchor point in the bounding box in relative coordinates, which will be positioned at *pos*.
            If ``None``, it'll be same as *pos*.
        :param padding: The extra space around the scene, in pixels.
        :return: The position of the bounding box in absolute coordinates.
        """
        if anchor is None:
            anchor = pos
        anchor_x = anchor[0] * (bounds.left() if anchor[0] < 0 else -bounds.right())
        anchor_y = anchor[1] * (bounds.top() if anchor[1] < 0 else -bounds.bottom())
        return self.r2a(pos, padding) + (anchor_x, anchor_y)

    def _repr_png_(self) -> bytes:
        """Returns the current frame as a PNG image. This method is called when the scene is displayed in a Jupyter
        notebook."""
        return skia.Image.fromarray(self.frame, copy=False).encodeToData().bytes()
