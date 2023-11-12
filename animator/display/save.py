"""Display managers for saving frames."""
from __future__ import annotations

import subprocess as sp
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from animator.scene import Scene


class SaveManager:
    def __init__(self, scene: Scene, path: str) -> None:
        self.scene: Scene = scene
        self.frame = scene.frame
        self.path: str = path

    @property
    def frame_count(self) -> int:
        return self.scene.animation_manager._current_frame

    def save_frame(self) -> None:
        print(f'\rWriting frame {self.frame_count}', end='')

    def close(self) -> None:
        print()


class SM_ffmpeg(SaveManager):
    """
    Saves frames using FFmpeg to *path*.

    TODO: Currently works only for mp4, why?
    """

    def __init__(self, scene: Scene, path: str, cmd: str = 'ffmpeg', force: bool = False) -> None:
        super().__init__(scene, path)
        args = f'{cmd} {"-y" if force else "-n"} -f rawvideo -s {self.frame.shape[1]}x{self.frame.shape[0]} -pix_fmt rgba -r {self.scene.fps} -i - -an {self.path}'.split()
        self.proc = sp.Popen(args, stdin=sp.PIPE, stderr=sp.DEVNULL)

    def save_frame(self) -> None:
        super().save_frame()
        if self.proc.stdin:
            try:
                self.proc.stdin.write(self.frame.tobytes())
            except BrokenPipeError:
                raise RuntimeError(
                    'FFmpeg exited unexpectedly. Hint: If the file already exists, try setting `force=True` to overwrite it.'
                )

    def close(self) -> None:
        super().close()
        if self.proc.stdin:
            self.proc.stdin.close()
        self.proc.wait()
