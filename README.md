# Animator

Animator is a Python library that allows you to easily create 2D animations and visualizations. I started this as a hobby project a long time back to learn more about Python and graphics programming. I've went through many iterations of this project, but I think I'll stick with this one for a while. I'm still working on the actual animation part in this version, but you can create some simple animations still.

Animator uses [Skia](https://skia.org/) as its graphics backend, so it's fast and supports a wide range of platforms. I used to use [skia-python](https://github.com/kyamagu/skia-python) for this project, but I decided to create my own bindings for Skia to make it easier to add new features and fix bugs. The earlier versions of Animator even used [pycairo](https://github.com/pygobject/pycairo) as the graphics backend, but I switched to Skia since it provides more features.

## Installation

Installation is kind of a pain right now. I'll work on making it easier. You'll need to build Skia from source and then install Animator using pip. Clone this repository. Visit the Skia website to [download](https://skia.org/docs/user/download) and [build](https://skia.org/docs/user/build) Skia.

Current Skia commit used: `c56f38d79fe0f3bcf36abf20953848f35390cc2f`

These are the basic steps I use to build:

```bash
export PATH="${PWD}/depot_tools:${PATH}"
cd skia
python3 tools/git-sync-deps
bin/gn gen out/StaticMin --args='is_debug=false is_official_build=true skia_enable_tools=true skia_use_system_harfbuzz=false skia_use_libfuzzer_defaults=false skia_use_gl=false text_tests_enabled=false skia_enable_pdf=false skia_enable_gpu=false skia_use_dng_sdk=false skia_enable_skvm_jit_when_possible=true skia_enable_skgpu_v1=false skia_enable_fontmgr_android=false skia_enable_discrete_gpu=false skia_build_fuzzers=false paragraph_tests_enabled=false cc="clang-14" cxx="clang++-14" extra_cflags_cc=["-frtti"] extra_ldflags=["-lrt"]'
ninja -C out/StaticMin/
```

### Explanation of some build flags

- `skia_use_system_harfbuzz=false`: Use Skia's internal HarfBuzz library. I didn't have the system HarfBuzz library installed, so I had to use Skia's internal one. You might not need this flag or need similar flags for other libraries.
- `skia_use_gl=false`: Disable OpenGL. No GPU support in Animator yet.
- `text_tests_enabled=false`: Disable tests.
- `skia_enable_pdf=false`: No PDF support.
- `skia_use_dng_sdk=false`: No DNG support, whatever that is.
- `skia_enable_fontmgr_android=false`: Not building for Android.
- `extra_cflags_cc=["-frtti"]`: Enable RTTI for pybind11.

After running `ninja`, you should have 12 `*.a` (or your platform's equivalent) files in `out/StaticMin`. These should be `libharfbuzz.a`, `libpathkit.a`, `libskcms.a`, `libskia.a`, `libskottie.a`, `libskparagraph.a`, `libskresources.a`, `libsksg.a`, `libskshaper.a`, `libsktext.a`, `libskunicode.a`, `libsvg.a`. They might be different depending on the build flags you used. Copy these files to `animator/skia/lib`. Required header files are already included.

After this, you can build and install Animator using pip:

```bash
pip setup.py install
```

## Getting Started

Here's a quick example to help you get started with Animator:

```python
import animator as am

scene = am.Scene()
scene.add(am.Circle(100))
scene.play_frames()
```

There are more examples in the [`examples`](/examples) directory.

## Testing

No tests. Animator is a visual library, so tests are visual! I'll add some tests later.

## Contributing

Contributions to Animator are welcome! If you find any bugs, have feature requests, or want to contribute code, please open an issue or pull request.

## License

Why is licensing so complicated? I'm not a lawyer, so I'll try to explain this as best as I can. Animator is licensed under the [MIT License](/LICENSE). However, Skia is licensed under the [BSD 3-Clause "New" or "Revised" License](https://github.com/google/skia/blob/main/LICENSE). This means that you can use Animator for any purpose, but you must include the Skia license too.