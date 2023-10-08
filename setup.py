from glob import glob
import os
from setuptools import setup, find_packages
from pybind11.setup_helpers import Pybind11Extension, build_ext, ParallelCompile, naive_recompile

os.environ['CC'] = os.environ['CXX'] = 'clang++-17'

ParallelCompile(default=2, max=4, needs_recompile=naive_recompile).install()

ext_modules = [
    Pybind11Extension(
        'animator.skia',
        sources=sorted(glob('skia/*.cpp') + glob('skia/extras/*.cpp') + glob('skia/textlayout/*.cpp')),
        include_dirs=['skia'],
        libraries=['png', 'fontconfig', 'icuuc'],
        extra_objects=sorted(glob('skia/lib/*.a')),
        extra_compile_args=['-Wall', '-Wextra', '-O3'],
        extra_link_args=['-Wall', '-Wextra', '-O3'],
    )
]

setup(
    name='animator',
    author='sherlock',
    packages=find_packages(),
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext},
)
