# Sphinx is a complex piece of software that doesn't do anything you need to do easily. The code has a decent amount of
# documentations, but the numerous Sphinx extensions just can't extract them. So, I've decided to write docs in markdown
# and put them on GitHub wiki. This file is for adding some Animator specific demos.
from __future__ import annotations

import argparse
import io
import os
from contextlib import AbstractContextManager
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Literal

_CODE_IMPORT = '''import animator as am

'''
_CODE_SUFFIX = '''scene.play_frames()
'''
_CODE_SUFFIX_IMG = '''scene.show_frame()
'''


class DemoParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.__inside_demo: bool = False
        self.__attribs: dict[str, str | Literal[True]] = {}
        self.code: str = ''

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.__inside_demo = True
        for k, v in attrs:
            self.__attribs[k] = True if v is None else v

    def handle_endtag(self, tag: str) -> None:
        self.__inside_demo = False

    def handle_data(self, data: str) -> None:
        if self.__inside_demo:
            self.code = data.strip()

    @property
    def image(self) -> bool:
        return bool(self.__attribs.get('image', False))

    @property
    def no_update(self) -> bool:
        return bool(self.__attribs.get('noupdate', False))

    @property
    def alt(self) -> str:
        return str(self.__attribs.get('alt', ''))

    @property
    def code_prefix(self) -> str:
        return f'scene = am.Scene({self.__attribs.get("args", "")})\n'

    def write_code(self, writer: io.TextIOWrapper) -> None:
        writer.write('```python\n')
        if self.__attribs.get('appendimport', False):
            writer.write(_CODE_IMPORT)
        if self.__attribs.get('appendprefix', False):
            writer.write(self.code_prefix)
        writer.write(self.code)
        writer.write('\n')
        if self.__attribs.get('appendsuffix', False):
            writer.write(_CODE_SUFFIX_IMG if self.no_update else _CODE_SUFFIX)
        writer.write('```\n')

    def get_exec(self) -> str:
        return _CODE_IMPORT + self.code_prefix + self.code


def sdbm(str):
    hash = 0
    for c in str:
        hash = (ord(c) + (hash << 6) + (hash << 16) - hash) & 0xFFFFFFFF
    return hex(hash)[2:]


class Parser(AbstractContextManager):
    def __init__(self, read_path: Path, write_path: Path, base: Path, file_name: str, ffmpeg: str, force: bool):
        self.__base: Path = base
        self.__file_name: str = file_name
        self.__ffmpeg: str = ffmpeg
        self.__force: bool = force
        self.__reader: io.TextIOWrapper = read_path.open()
        self.__writer: io.TextIOWrapper = write_path.open('w')

        self.__cur_line: str = ''

    def __enter__(self) -> Parser:
        return super().__enter__()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.__writer.close()
        self.__reader.close()

    def __readline(self) -> str:
        self.__cur_line = self.__reader.readline()
        if not self.__cur_line:
            raise EOFError
        return self.__cur_line

    def __read_demo(self) -> str:
        lines = [self.__cur_line]
        while True:
            lines.append(self.__readline())
            if self.__cur_line.strip() == '</demo>':
                break
        return ''.join(lines)

    def process(self, image_path: Path) -> None:
        while True:
            try:
                if self.__readline().strip().startswith('<demo'):
                    demo = DemoParser()
                    demo.feed(self.__read_demo())
                    demo.write_code(self.__writer)

                    code = demo.get_exec()
                    file_name = f'{self.__file_name}-{sdbm(code)}'
                    png_path = f'{image_path/file_name}.png'
                    mp4_path = f'build/{file_name}.mp4'
                    gif_path = f'{image_path/file_name}.gif'
                    file_exists = False
                    if demo.image:
                        file_exists = Path(png_path).exists()
                        if not demo.no_update:
                            code += '\nscene.update()'
                        code += f'\nscene.save_frame("{png_path}")'
                    else:
                        file_exists = Path(gif_path).exists()
                        code += f'\nscene.save_frames("{mp4_path}", cmd="{self.__ffmpeg}", force=True)'
                    if not file_exists or self.__force:
                        with open('build/code.py', 'w') as f:
                            f.write(code)
                        if os.system('python build/code.py') != 0:
                            raise RuntimeError('Failed to run code.')
                        if not demo.image:
                            os.system(f'{self.__ffmpeg} -i {mp4_path} {gif_path} -y')

                    self.__writer.write(
                        f'\n**Output**\n\n![{demo.alt}]({Path(png_path if demo.image else gif_path).relative_to(self.__base)})\n'
                    )
                else:
                    self.__writer.write(self.__cur_line)
            except EOFError:
                break


parser = argparse.ArgumentParser()
parser.add_argument('dir', nargs='?', default='docs', help='Path to the docs directory')
parser.add_argument('out', nargs='?', default='Animator.wiki', help='Path to the output directory')
parser.add_argument('--force', action='store_true', help='Force generate all the docs')
parser.add_argument('--ffmpeg', default='ffmpeg' if os.system('ffmpeg') == 0 else 'ffmpeg.exe', help='Path to ffmpeg')
args = parser.parse_args()

read_path = Path(args.dir)
write_path = Path(args.out)
image_path = write_path / 'assets'
image_path.mkdir(parents=True, exist_ok=True)
for file in read_path.glob('**/*.md'):
    rel_path = file.relative_to(read_path)
    new_file = write_path / rel_path
    new_file.parent.mkdir(parents=True, exist_ok=True)
    if not new_file.exists() or new_file.lstat().st_mtime < file.lstat().st_mtime or args.force:
        print(f'Generating {rel_path}...')
        with Parser(file, new_file, write_path, file.stem, args.ffmpeg, args.force) as parser:
            parser.process(image_path)
