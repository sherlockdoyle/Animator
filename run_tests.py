# Run visual tests on the examples.

import os
from pathlib import Path

import numpy as np

from animator import skia

EXAMPLES_PATH = Path('examples')
IMAGES_PATH = EXAMPLES_PATH / 'out'
IMAGES_PATH.mkdir(exist_ok=True)

BUILD_PATH = Path('build')
BUILD_CODE_FILE = BUILD_PATH / 'code.py'
BUILD_IMAGE_FILE = BUILD_PATH / 'image.png'


def replace_and_copy(p: Path, output_file: Path):
    with open(p, 'r') as f:
        lines = f.readlines()
    save_code = f"scene.save_frame('{output_file}')\n"
    with open(BUILD_CODE_FILE, 'w') as f:
        for line in lines:
            if line.startswith('scene.show_frame()'):
                f.write(save_code)
            elif line.startswith('scene.play_frames()'):
                f.write('scene.update()\n')
                f.write(save_code)
            else:
                f.write(line)


def run_file():
    os.system(f'python {BUILD_CODE_FILE}')


def generate_output_file(p: Path, output_file: Path):
    replace_and_copy(p, output_file)
    run_file()
    print(f'\033[94m{p.stem} generated.\033[0m')


def run_test(p: Path, output_file: Path):
    replace_and_copy(p, BUILD_IMAGE_FILE)
    run_file()

    with open(output_file, 'rb') as f:
        original_image = np.array(skia.Image.open(f).makeRasterImage(), copy=False)
    with open(BUILD_IMAGE_FILE, 'rb') as f:
        new_image = np.array(skia.Image.open(f).makeRasterImage(), copy=False)
    if original_image.shape != new_image.shape:
        print(f'\033[93m{p.stem} failed, image shape changed.\033[0m')
        return

    diff_pixels = np.any(original_image != new_image, axis=-1).sum()
    if diff_pixels == 0:
        print(f'\033[92m{p.stem} passed.\033[0m')
    else:
        print(f'\033[91m{p.stem} failed, {diff_pixels} pixels differ.\033[0m')
        diff_image = (np.abs(original_image.astype(np.int16) - new_image.astype(np.int16)) != 0).astype(np.uint8) * 255
        diff_image[:, :, 3] = 255
        skia.Image.fromarray(diff_image, copy=False).save(f'{p.stem}-diff.png')


for p in EXAMPLES_PATH.glob('*.py'):
    output_file = IMAGES_PATH / f'{p.stem}.png'
    if output_file.exists():
        run_test(p, output_file)
    else:
        generate_output_file(p, output_file)
