import animator as am

scene = am.Scene(1000, 600)

img = am.skia.Image.open('examples/images/Under the Wave.jpg').resize(200, 200)  # load and resize an image


def make_color_filter(sksl: str) -> am.skia.ColorFilter:
    result = am.skia.RuntimeEffect.MakeForColorFilter(sksl)  # create a custom color filter from sksl
    if not result.effect:
        raise RuntimeError(result.errorText)
    return am.skia.RuntimeColorFilterBuilder(result.effect).makeColorFilter()


TABLE = list(range(256))  # create a table with 256 entries
GREYSCALE = [0.2126, 0.7152, 0.0722, 0, 0]  # create a greyscale matrix
NeedWhiteBackground = bool
color_filters: list[tuple[am.skia.ColorFilter, str] | tuple[am.skia.ColorFilter, str, NeedWhiteBackground]] = [
    (am.skia.ColorFilters.Blend(am.color('red500'), am.skia.BlendMode.kColor), 'Blend'),  # blend with red
    (
        am.skia.ColorFilters.Matrix(
            [0.393, 0.768, 0.188, 0, 0, 0.349, 0.685, 0.167, 0, 0, 0.272, 0.533, 0.130, 0, 0, 0, 0, 0, 1, 0]
        ),
        'Matrix-Sepia',
    ),  # apply a sepia matrix
    (
        am.skia.HighContrastFilter.Make(am.skia.HighContrastConfig(grayscale=True)),
        'HighContrast-Grayscale',
    ),  # apply a grayscale filter
    (am.skia.ColorFilters.Lighting(am.color('red500'), am.color('blue500')), 'Lighting'),
    (
        am.skia.ColorFilters.HSLAMatrix(
            [0.393, 0.768, 0.188, 0, 0, 0.349, 0.685, 0.167, 0, 0, 0.272, 0.533, 0.130, 0, 0, 0, 0, 0, 1, 0]
        ),
        'HSLAMatrix',
    ),  # apply the sepia matrix on the HSLA color space
    (
        am.skia.HighContrastFilter.Make(
            am.skia.HighContrastConfig(invertStyle=am.skia.HighContrastConfig.InvertStyle.kInvertLightness)
        ),
        'HighContrast-InvertLightness',
    ),  # invert the lightness
    (am.skia.ColorFilters.LinearToSRGBGamma(), 'LinearToSRGBGamma'),  # convert from linear to srgb color space
    (
        am.skia.ColorFilters.TableARGB(
            TABLE, TABLE[64:] + TABLE[:64], TABLE[128:] + TABLE[:128], TABLE[192:] + TABLE[:192]
        ),
        'TableARGB',
    ),  # swap light and dark colors
    (
        am.skia.HighContrastFilter.Make(
            am.skia.HighContrastConfig(invertStyle=am.skia.HighContrastConfig.InvertStyle.kInvertBrightness)
        ),
        'HighContrast-InvertBrightness',
    ),  # invert the brightness
    (am.skia.ColorFilters.SRGBToLinearGamma(), 'SRGBToLinearGamma'),  # convert from srgb to linear color space
    (am.skia.LumaColorFilter.Make(), 'Luma', True),  # apply a luma color filter
    (
        am.skia.HighContrastFilter.Make(am.skia.HighContrastConfig(contrast=1)),
        'HighContrast-Contrast',
    ),  # increase the contrast
    (
        am.skia.ColorFilters.Lerp(
            0.5,
            am.skia.ColorFilters.Matrix(GREYSCALE + GREYSCALE + GREYSCALE + [0, 0, 0, 1, 0]),  # greyscale matrix
            am.skia.HighContrastFilter.Make(am.skia.HighContrastConfig(contrast=0.5)),  # highish contrast
        ),
        'Lerp',
    ),  # mix the greyscale matrix with the high contrast filter
    (
        am.skia.ColorFilters.Compose(
            am.skia.ColorFilters.HSLAMatrix(
                GREYSCALE + GREYSCALE + GREYSCALE + [0, 0, 0, 1, 0]
            ),  # greyscale matrix, but on the HSLA color space
            am.skia.HighContrastFilter.Make(
                am.skia.HighContrastConfig(invertStyle=am.skia.HighContrastConfig.InvertStyle.kInvertBrightness)
            ),  # invert the brightness
        ),
        'Compose',
    ),  # invert the brightness, then apply the greyscale matrix
    (
        make_color_filter(
            """
float rand(vec2 co) {  // create a random number generator
    return fract(sin(dot(co.xy, vec2(1, 7))) * 4);  // little random
}
half4 main(half4 color) {
    return half4(rand(color.xy), rand(color.yz), rand(color.zw), rand(color.wx));  // map each color to a random number
}
    """
        ),
        'RuntimeEffect',
    ),  # apply a custom color filter
]

x = y = 0
for i in range(len(color_filters)):  # for each color filter
    filter = color_filters[i][0]
    name = color_filters[i][1]
    need_white_background = color_filters[i][2] if len(color_filters[i]) > 2 else False  # type: ignore
    if need_white_background:  # the luma color filter only generates the alpha channel
        scene.add(
            am.PaintFill(fill_color='white', clip=am.skia.Rect.MakeXYWH(x, y, 200, 200))
        )  # so we need to add a white background
    scene.add(am.Image(img, pos=(x, y), clip=img.bounds(), color_filter=filter))  # add the image with the filter
    scene.add(label := am.SimpleText(name, pos=(x + 2, y + 14)))  # add the label
    label.style.set_glow(2, 'black')  # add a glow to the label to make it more readable
    y += 200
    if y > scene.height - 200:
        y = 0
        x += 200


scene.update()
scene.show_frame()
