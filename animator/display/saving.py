"""Classes used to save the animator frames."""
from __future__ import annotations

import os
import subprocess as sp
from typing import List, TYPE_CHECKING, Any

from .DisplayManager import DisplayManager
from .. import skia
from ..util.env import get_path

if TYPE_CHECKING:
    from ..scene.scene import Scene


class DMS_ffmpeg(DisplayManager):
    def __init__(self, scene: Scene, path: str, codec: str = 'libx264', opts: List[str] = None,
                 command: List[str] = None, **kwargs: Any):
        """Saves the frames to *path* using ``ffmpeg``. The video *codec* and extra *opts* can be specified to pass
        to ``ffmpeg``. Alternately, a custom *command* for saving can also be specified. Both *opts* and *command*
        must be in the format as accepted by the :mod:`subprocess` module.

        :param scene: The scene which will be saved.
        :param path: The path to save the frames to.
        :param codec: The codec to use for the video.
        :param opts: Extra options to pass to ``ffmpeg``.
        :param command: A custom command to use for saving.
        """
        super().__init__(scene, **kwargs)
        if command is None:
            if opts is None:
                opts = []
            command = ['ffmpeg', '-y',  # overwrite output file
                       '-f', 'rawvideo',  # raw input (constant)
                       '-s', f'{self.width}x{self.height}',  # size of one frame (from scene)
                       '-pix_fmt', 'rgba',  # pixel format (constant)
                       '-r', str(self.scene.fps),  # frames per second (from scene)
                       '-i', '-',  # input from pipe (constant, from scene)
                       '-an',  # no audio (constant)
                       '-vcodec', codec,  # video codec (from user)
                       *opts,  # extra options (from user)
                       get_path(path)]  # output path (from user)
        self.proc = sp.Popen(command, stdin=sp.PIPE, stderr=sp.DEVNULL)

    def show_frame(self) -> bool:
        print(f'\rWriting frame {self.scene.frame_count}', end='')
        self.proc.stdin.write(self.scene.frame.tostring())
        return True

    def close(self) -> None:
        print(f'\rCompleted writing {self.scene.frame_count} frames.', end='')
        self.proc.stdin.close()
        self.proc.wait()


class DMS_imageSeq(DisplayManager):
    def __init__(self, scene: Scene, path: str, **kwargs: Any):
        """Saves the frames to the directory *path* as a sequence of images. The images are named
        ``frame_<frame_count>.png``.

        :param scene: The scene which will be saved.
        :param path: The directory path to save the frames to.
        """
        super().__init__(scene, **kwargs)
        self.path = get_path(path if path.endswith(os.sep) else (path + os.sep), True)
        self.img: skia.Image = skia.Image.fromarray(self.scene.frame, copy=False)

    def show_frame(self) -> bool:
        print(f'\rWriting frame {self.scene.frame_count}', end='')
        self.img.save(os.path.join(self.path, f'frame_{self.scene.frame_count}.png'))
        return True

    def close(self) -> None:
        print(f'\rCompleted writing {self.scene.frame_count} frames.', end='')
