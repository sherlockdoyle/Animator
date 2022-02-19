"""Basic and utility animations."""
from __future__ import annotations

__all__ = 'ShowFPS',

import sys
import time
from typing import TYPE_CHECKING

from .. import skia

from .anim import Anim
from ..entity.entity import Entity

if TYPE_CHECKING:
    from ..scene.scene import Scene


class ShowFPS(Anim):
    """Show the current FPS."""

    class Helper(Entity):
        font: skia.Font = skia.Font()
        paint: skia.Paint = skia.Paint(Color=0xFFFFFFFF)

        def __init__(self):
            super().__init__()
            self.real_fps: float = 0

        def _set_scene(self, scene: Scene) -> None:
            super()._set_scene(scene)
            self.real_fps = scene.fps

        def draw(self) -> None:
            self.scene.canvas.drawString(f'FPS: {self.real_fps:.2f}', 5, 20, self.font, self.paint)

    def __init__(self):
        frame = sys._getframe(1)
        print(f'Debugging with ShowFPS from {frame.f_code.co_filename}:{frame.f_lineno}')

        super().__init__(Anim.InfiniteDuration.ALONGSIDE)
        self.old_time: float = 0

        self.helper: ShowFPS.Helper = ShowFPS.Helper()
        self.entities.append(self.helper)

    def start(self) -> None:
        self.old_time = time.time()

    def update(self) -> None:
        newtime = time.time()
        # Exponential moving average (https://github.com/processing/processing/blob/8e86389c7e017d0e4d61f81fb942c25e3ed348c7/core/src/processing/core/PApplet.java#L2460-L2470)
        self.helper.real_fps /= 0.95 + 0.05 * (newtime - self.old_time) * self.helper.real_fps
        self.old_time = newtime
