"""This module keeps track of all the classes and functions required to set up the drawing operations. The
:class:`Scene` class provides an interface around a ``skia.Canvas`` and is the most important class used for all
kinds of drawings.

**Converters:** In case you want to use a different surface for drawing (say SVG), the converter functions can be
used to quickly change the surface. This, however, will break most of the :class:`Scene` methods (the reason for
providing them as separate functions). Generally, once the scene has been converted, the rendering functions will not
work."""
from __future__ import annotations

__all__ = 'Scene',

import contextlib
import os
import re
import warnings
from typing import Dict, Tuple, List, TypeVar, TYPE_CHECKING, Callable, ContextManager, Any

import numpy

from .Context2d import Context2d
from .. import skia
from ..anim.anim import AnimationManager, Anim
from ..anim.basic import Once
from ..display.DisplayManager import DisplayManager
from ..display.saving import DMS_ffmpeg
from ..entity.entity import Entity
from ..util.env import get_path, inside_ipython_notebook

if TYPE_CHECKING:
    from .._common_types import Color

    EntityOrAnim = TypeVar('EntityOrAnim', Entity, Anim)
    ET = TypeVar('ET', bound=Entity)

_name2px: Dict[str, Tuple[int, int]] = {
    '144p': (256, 144),
    '240p': (426, 240),
    '360p': (640, 360),
    '480p': (854, 480),
    '720p': (1280, 720),
    'hd': (1280, 720),
    '1080p': (1920, 1080),
    'fullhd': (1920, 1080),
    'fhd': (1920, 1080),
    '1440p': (2560, 1440),
    '2k': (2560, 1440),
    '2160p': (3840, 2160),
    '4k': (3840, 2160),
    'ultrahd': (3840, 2160),
    'uhd': (3840, 2160),
}
_ext2format: Dict[str, skia.EncodedImageFormat] = {
    'png': skia.EncodedImageFormat.kPNG,
    'jpg': skia.EncodedImageFormat.kJPEG,
    'jpeg': skia.EncodedImageFormat.kJPEG,
    'webp': skia.EncodedImageFormat.kWEBP
}
_clear_paint: skia.Paint = skia.Paint(BlendMode=skia.BlendMode.kClear)


class Scene:
    """Scene is the root of all renderings. This class keeps track of all the entities and animations and provides an
    easy to use interface for all drawings. It initializes a frame, and a :class:`skia.Canvas` to keep track of all
    the drawings and displays or saves them.

    :ivar width: The width of the frame/scene.
    :ivar height: The height of the frame/scene.
    :ivar fps: The FPS to be used when rendering.
    :ivar frame: The internal frame (array) used to save the drawings. The data is in RGBA format.
    :ivar canvas: The :class:`skia.Canvas` used for drawing.
    :ivar bgcolor: The background color for the drawings. This is used to clear and fill the scene after each frame.
    """

    def __init__(self, width: int | str = 854, height: int = 480, fps: float = 30,
                 scale: float | Tuple[int, int] | str = 1):
        """
        :param width: The width of the frame/scene or a string representing a common resolution. Resolutions can be
            one of '144p', '240p', '360p', '480p', '720p', '1080p', '1440p', '2160p', '2k', '4k', 'hd', 'fullhd', 'fhd',
            'ultrahd' or 'uhd', is case-insensitive and may contain whitespaces.
        :param height: The height of the frame/scene.
        :param fps: The FPS to be used while saving the animations. The FPS used during real time animations might vary.
        :param scale: During real time animations, a larger frame might cause delays and slow down the animation.
            This factor simply scales the frame to a smaller size. By specifying a value >1, this can also be used to
            render high-resolution (scaled up) images. It can also be one of the strings supported by *width*,
            or a tuple of (width, height), in which case the frame will be scaled to match the size. If the aspect
            ratio of the frame is different from the scene, the frame will be scaled and centered.
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
            frame_width, frame_height = int(width * scale), int(height * scale)
        self.frame: numpy.ndarray = numpy.zeros(shape=(frame_height, frame_width, 4), dtype=numpy.uint8)
        self.canvas = skia.Canvas(self.frame)
        scale = min(frame_width / width, frame_height / height)
        self.canvas.translate((frame_width - width * scale) / 2, (frame_height - height * scale) / 2)
        self.canvas.scale(scale, scale)

        self.fps: float = fps
        self.bgcolor: Color = (0, 0, 0, 1)
        self.entities: List[Entity] = []
        self.animation_manager: AnimationManager = AnimationManager(self)
        self.__context2d: Context2d = None  # lateinit

    def clear(self) -> None:
        """Clears the frame and fills it with transparency."""
        self.canvas.drawPaint(_clear_paint)

    def clear_with_bgcolor(self) -> None:
        """Clears the frame and fills it with the background color."""
        self.canvas.clear(skia.Color4f(self.bgcolor))

    def add(self, *child: EntityOrAnim) -> EntityOrAnim | Tuple[EntityOrAnim, ...]:
        """Add one or more entity or animation to the scene.

        :param child: The entity or animation to be added.
        :return: The added entity or animation.
        """
        for c in child:
            if isinstance(c, Entity):
                if c not in self:
                    self.entities.append(c)
                    c._set_scene(self)
            else:  # isinstance(c, Anim)
                self.animation_manager.add(c)
                for e in c.entities:
                    if e not in self:
                        self.entities.append(e)
                        e._set_scene(self)
        return child[0] if len(child) == 1 else child

    def __add__(self, anim: Anim | Tuple[Anim, ...]) -> Anim | Tuple[Anim, ...]:
        """Add one or more animations to the scene and return the added animation(s). Adds a single frame wait after
        the animations."""
        if isinstance(anim, Anim):
            self.add(anim)
        else:  # isinstance(anim, tuple)
            self.add(*anim)
        self.animation_manager.wait(frame=1)
        return anim

    __radd__ = __add__

    def wait(self, time: float = 1, frame: int = 0) -> None:
        """Add a wait of *time* seconds or *frame* frames to the scene (*time* overrides *frame*).

        :param time: The time to wait in seconds. 1 second is the default.
        :param frame: The number of frames to wait.
        """
        self.animation_manager.wait(time, frame)

    def hook(self, f: Callable[[], None]) -> Callable[[], None]:
        """Hook a function to be called at the current point in the animation timeline.

        :param f: The function to be called.
        """
        self.add(Once(f))
        return f

    def __matmul__(self, ent: ET) -> ET:
        """Utility method to set the scene of an entity without adding it to the scene.

        >>> ent1 = Entity()  # ent1 has no scene
        >>> scene.add(ent1)  # ent1 has a scene, it'll also be drawn
        >>> ent2 = Entity() @ scene  # ent2 has a scene, but won't be drawn

        :param ent: The entity to set the scene of.
        """
        ent._set_scene(self)
        return ent

    __rmatmul__ = __matmul__

    def __contains__(self, ent: Entity) -> bool:
        """Check if an entity is in the scene or in any of its entities, recursively.

        :param ent: The entity to check.

        :note: To check if an animation is in the scene, use ``scene.animation_manager.__contains__``.
        """
        if ent in self.entities:
            return True
        for e in self.entities:
            if ent in e:
                return True
        return False

    def remove(self, ent: Entity) -> bool:
        """Remove an entity from the scene.

        :param ent: The entity to remove.
        :return: ``True`` if the entity was removed, ``False`` otherwise.
        """
        try:
            self.entities.remove(ent)
            return True
        except ValueError:
            return False

    @property
    def frame_count(self) -> int:
        """The number of frames displayed."""
        return self.animation_manager.frame_count

    @property
    def context2d(self) -> Context2d:
        """An instance of :class:`Context2d` wrapping the current canvas. A :class:`Context2d` wraps around a
        :class:`skia.Canvas` instance and provides additional functionality. A scene contains only one instance of a
        :class:`Context2d`; multiple calls to this method will return the same instance. This method works with
        converted scenes."""
        if self.__context2d is None:
            self.__context2d = Context2d(self.canvas)
        return self.__context2d

    def update(self) -> bool:
        """Update a single frame of the animations, clears and draws the entities on the scene.

        :return: ``True`` if more updates are possible, ``False`` otherwise.
        """
        more: bool = self.animation_manager.update()
        for ent in self.entities:
            ent.update()
        self.clear_with_bgcolor()
        for ent in self.entities:
            ent.draw()
        return more

    def show_frame(self) -> None:
        """Show the current frame of the animation."""
        manager = DisplayManager.get_best()(self)
        while manager.show_frame():
            pass
        manager.close()

    def save_frame(self, path: str, quality: int = 100) -> None:
        """Save the current frame of the animation to a file.

        :param path: The path to the file to save to. If the path contains a ``{}`` format specifier, the current
            frame number will be added.
        :param quality: The quality of the image. 100 (the default) is the best quality.
        """
        path = path.format(self.animation_manager.frame_count)
        ext = os.path.splitext(path)[1][1:]
        try:
            skia.Image.fromarray(self.frame, copy=False).save(get_path(path), _ext2format[ext], quality)
        except KeyError:
            raise ValueError(f'Unsupported file extension: {ext}')

    def play_frames(self, delay: float | None = None, keep_open: bool = True) -> None:
        """Play the animations and display the frames using the best available :class:`DisplayManager`.

        :param delay: The delay between frames in seconds. If ``None``, the delay will be determined from the scene's
            fps. If ``0``, the animation will be played as fast as possible.
        :param keep_open: Whether to keep the window open after the animation is finished. To close the window,
            press the escape key or click on the close button.
        """
        if delay is None:
            delay = 1 / self.fps
        manager = DisplayManager.get_best()(self, delay)

        self.animation_manager.start()
        while self.update() and manager.show_frame():
            pass
        self.animation_manager.pause()
        if keep_open:
            while manager.show_frame():
                pass
        manager.close()

    play = play_frames

    def save_frames(self, path: str) -> None:
        """Save the animation frames to a single movie file.

        :param path: The path to the file to save to.
        """
        for anim in self.animation_manager.anims:
            if anim.duration == Anim.InfiniteDuration.INFINITE:
                warnings.warn(f'INFINITE duration animation {anim.__class__.__name__} in scene. Changing it to type '
                              f'ALONGSIDE.')
                anim.duration = Anim.InfiniteDuration.ALONGSIDE

        writer = DMS_ffmpeg(self, get_path(path))
        self.animation_manager.start()
        while self.update():
            writer.show_frame()  # will always return True
        self.animation_manager.pause()
        writer.close()

    render = save_frames

    @contextlib.contextmanager
    def synced_anim(self, keep_open: bool = True, save_path: str | None = None, **kwargs: Any) -> ContextManager[
        Callable[[Anim], None]]:
        """A context manager that plays the animation or saves it to a movie file, synchronously. Animations play as
        soon as added.

        :param keep_open: Whether to keep the window open after the animation is finished. To close the window,
            press the escape key or click on the close button.
        :param save_path: The path to the file to save to. If ``None``, the animation will not be saved, but played.
        :param kwargs: Additional keyword arguments to pass to the :class:`DisplayManager`.
        """
        if save_path is not None:
            keep_open = False
        helper = SyncedAnimHelper(self, save_path=save_path, **kwargs)
        try:
            yield helper.play
        finally:
            if keep_open:
                helper.keep_open()
            helper.close()

    @contextlib.contextmanager
    def quickdraw(self) -> ContextManager[Context2d]:
        """Used for quickly drawing on the scene. This method clears the scene and returs an instance of
        :class:`Context2d` for drawing. On exit, the scene is displayed with appropriate method.

        >>> import animator as am
        >>> scene = am.Scene()
        >>> with scene.quickdraw() as ctx:
        ...     ctx.circle(scene.width / 2, scene.height / 2, 120)
        ...     ctx.fill()
        >>> # This will show a circle at the center of a black background.
        """
        try:
            self.clear_with_bgcolor()
            yield self.context2d
        finally:
            if inside_ipython_notebook():
                from IPython.display import display
                display(self)
            else:
                self.show_frame()

    def r2a(self, pos: numpy.ndarray, padding: float = 25) -> skia.Point:
        """Convert a point from the scene's relative coordinates to absolute coordinates.

        :param pos: The point in relative coordinates, a 2 element numpy array [x, y]. The coordinates are between -1
            (left or top) and 1 (right or bottom).
        :param padding: The extra space to consider at the edges of the scene.
        :return: The point in absolute coordinates.
        """
        pos = (1 + pos) / 2
        return skia.Point((self.width - 2 * padding) * pos[0] + padding, (self.height - 2 * padding) * pos[1] + padding)

    def r2a_bounds(self, bounds: skia.Rect, pos: numpy.ndarray, anchor: numpy.ndarray | None = None,
                   padding: float = 25) -> skia.Point:
        """Convert a relative coordinates to absolute coordinates for a rectangular bounding box. This is used for
        the relative positioning of a bounding box in the scene.

        :param bounds: The bounding box that is to be positioned.
        :param pos: The relative position of the bounding box. A 2 element numpy array [x, y]. The coordinates are
            between -1 (left or top) and 1 (right or bottom).
        :param anchor: The relative position in the bounding box that will be aligned to the relative position. A 2
            element numpy array [x, y]. The coordinates are between -1 (left or top) and 1 (right or bottom). If
            ``None``, the anchor will be the same as *pos*.
        :param padding: The extra space to consider at the edges of the scene.
        :return: The absolute position for the bounding box.
        """
        if anchor is None:
            anchor = pos
        anchor_x = anchor[0] * (bounds.left() if anchor[0] < 0 else -bounds.right())
        anchor_y = anchor[1] * (bounds.top() if anchor[1] < 0 else -bounds.bottom())
        return self.r2a(pos, padding) + (anchor_x, anchor_y)

    def _repr_png_(self) -> bytes:
        """Return a png representation of the scene.

        This method is used by IPython notebooks.
        """
        return skia.Image.fromarray(self.frame, copy=False).encodeToData(skia.EncodedImageFormat.kPNG, 100).bytes()


class SyncedAnimHelper:
    """Helper class for playing an animation in sync.

    :note: This will add an extra frame between two animations.
    """

    def __init__(self, scene: Scene, save_path: str | None = None, **kwargs: Any):
        """
        :param scene: The scene to play the animation of.
        :param save_path: The path to the file to save to. If ``None``, the animation will not be saved, but played.
        :param kwargs: Additional keyword arguments to pass to the :class:`DisplayManager`.
        """
        self.scene = scene
        self.display_manager = DisplayManager.get_best()(scene, **kwargs) if save_path is None \
            else DMS_ffmpeg(scene, save_path, **kwargs)
        self.show_frame = True

    def play(self, *anims: Anim, wait: float = 0, display: bool | None = None) -> None:
        """Play the animations in sync followed by a wait of *wait* seconds. Execution will be blocked until the
        animations complete.

        :param anims: The animations to play.
        :param wait: The number of seconds to wait after the animations have completed. Use this without any
            animations to just wait for *wait* seconds.
        :param display: If specified, the scene will be displayed or not based on this value. If ``False``,
            the animations will execute, but nothing will be displayed.
        """
        if display is not None:
            self.show_frame = display
            return
        if self.scene.animation_manager.frame_count != 0:
            self.scene.animation_manager.frame_count -= 1
        self.scene.add(*anims)
        self.scene.animation_manager.wait(wait)
        self.scene.animation_manager.start()
        while self.scene.update():
            if self.show_frame and not self.display_manager.show_frame():
                break
        self.scene.animation_manager.pause()

    def keep_open(self) -> None:
        """Keep the animation window open."""
        while self.display_manager.show_frame():
            pass

    def close(self) -> None:
        """Close the animation window."""
        self.display_manager.show_frame()  # show the last frame
        self.display_manager.close()
