import animator as am

scene = am.Scene(1050, 750)


def RectAndBars(x: float, y: float, side: float):  # create an entity that returns a complex entity
    return am.StyledGroup(pos=(x, y))[  # create a group; the square bracket syntax is a shortcut for adding children
        am.Rect(side, side / 2, fill_color='blue', style='fill'),  # add a blue filled rectangle
        am.Line(0, 6 * side / 10, side, 6 * side / 10, stroke_color='red500'),  # add a horizontal red line
        am.Line(0, 7 * side / 10, side, 7 * side / 10, stroke_color='blue500'),  # add a horizontal blue line
        am.Line(0, 8 * side / 10, side, 8 * side / 10, stroke_color='yellow500'),  # add a horizontal yellow line
        am.Line(0, 9 * side / 10, side, 9 * side / 10, stroke_color='green500'),  # add a horizontal green line
    ]


def EllipseAndBars(
    x: float, y: float, side: float, blend_mode: am.skia.BlendMode | am.skia.Blender
):  # create another complex entity with a blend mode
    # we also add a clip, otherwise the blend mode will be applied to the whole scene
    # the 5px offset is to account for the stroke width and round caps
    return am.StyledGroup(pos=(x, y), blend_mode=blend_mode, clip=(-5, -5, SIDE + 5, SIDE + 5))[  # create a group
        am.Ellipse(side / 4, side / 2, fill_color='red', style='fill').shift(
            side / 4, side / 2
        ),  # add a red ellipse, shift it to bring the origin to the top left corner
        am.Line(6 * side / 10, 0, 6 * side / 10, side, stroke_color='red500'),  # add a vertical red line
        am.Line(7 * side / 10, 0, 7 * side / 10, side, stroke_color='blue500'),  # add a vertical blue line
        am.Line(8 * side / 10, 0, 8 * side / 10, side, stroke_color='yellow500'),  # add a vertical yellow line
        am.Line(9 * side / 10, 0, 9 * side / 10, side, stroke_color='green500'),  # add a vertical green line
    ]


blend_modes = [  # create a list of all the blend modes
    am.skia.BlendMode.kClear,  # r = 0
    am.skia.BlendMode.kSrc,  # r = s
    am.skia.BlendMode.kDst,  # r = d
    am.skia.BlendMode.kSrcOver,  # r = s + (1-sa)*d
    am.skia.BlendMode.kDstOver,  # r = d + (1-da)*s
    am.skia.BlendMode.kSrcIn,  # r = s * da
    am.skia.BlendMode.kDstIn,  # r = d * sa
    am.skia.BlendMode.kSrcOut,  # r = s * (1-da)
    am.skia.BlendMode.kDstOut,  # r = d * (1-sa)
    am.skia.BlendMode.kSrcATop,  # r = s*da + d*(1-sa)
    am.skia.BlendMode.kDstATop,  # r = d*sa + s*(1-da)
    am.skia.BlendMode.kXor,  # r = s*(1-da) + d*(1-sa)
    am.skia.BlendMode.kPlus,  # r = min(s + d, 1)
    am.skia.BlendMode.kModulate,  # r = s*d
    am.skia.BlendMode.kScreen,  # r = s + d - s*d
    am.skia.BlendMode.kOverlay,  # multiply or screen, depending on destination
    am.skia.BlendMode.kDarken,  # rc = s + d - max(s*da, d*sa), ra = kSrcOver
    am.skia.BlendMode.kLighten,  # rc = s + d - min(s*da, d*sa), ra = kSrcOver
    am.skia.BlendMode.kColorDodge,  # brighten destination to reflect source
    am.skia.BlendMode.kColorBurn,  # darken destination to reflect source
    am.skia.BlendMode.kHardLight,  # multiply or screen, depending on source
    am.skia.BlendMode.kSoftLight,  # lighten or darken, depending on source
    am.skia.BlendMode.kDifference,  # rc = s + d - 2*(min(s*da, d*sa)), ra = kSrcOver
    am.skia.BlendMode.kExclusion,  # rc = s + d - two(s*d), ra = kSrcOver
    am.skia.BlendMode.kMultiply,  # r = s*(1-da) + d*(1-sa) + s*d
    am.skia.BlendMode.kHue,  # hue of source with saturation and luminosity of destination
    am.skia.BlendMode.kSaturation,  # saturation of source with hue and luminosity of destination
    am.skia.BlendMode.kColor,  # hue and saturation of source with luminosity of destination
    am.skia.BlendMode.kLuminosity,  # luminosity of source with hue and saturation of destination
]


x = y = 0
SIDE = 150
for mode in blend_modes:  # loop over the blend modes
    scene.add(RectAndBars(x + 5, y + 5, SIDE - 10))  # add the first layer
    scene.add(EllipseAndBars(x + 5, y + 5, SIDE - 10, mode))  # add the second layer with the blend mode
    scene.add(am.SimpleText(mode.name_(), pos=(x + 8, y + 18)))  # add the label
    x += SIDE
    if x > 900 - SIDE:
        x = 0
        y += SIDE
scene.add(RectAndBars(x + 5, y + 5, SIDE - 10))  # add the first layer
scene.add(
    EllipseAndBars(x + 5, y + 5, SIDE - 10, am.skia.Blenders.Arithmetic(1, 1, 1, 0))
)  # add the second layer with an arithmetic blend mode
scene.add(am.SimpleText('Arithmatic', pos=(x + 8, y + 18)))  # add the label

scene.add(
    # the child_blender property of a group will apply the blend mode to all its children
    am.StyledGroup(child_blender=am.skia.BlendMode.kExclusion, pos=(900, 5), clip=(-5, -5, 155, 155))[
        am.Circle(50, pos=(50, 50), fill_color=0xFFFF0000),
        am.Circle(50, pos=(100, 50), fill_color=0xFF00FF00),
        am.Circle(50, pos=(75, 86.6), fill_color=0xFF0000FF),
    ]
)
scene.add(am.SimpleText('Group', pos=(903, 18)))

scene.add(am.PaintFill(fill_color='white', clip=am.skia.Rect.MakeXYWH(900, 150, 150, 150)))  # add some background
scene.add(
    # the blender property can also be set by name
    am.StyledGroup(child_blender='multiply', pos=(900, 155), clip=(-5, -5, 155, 155))[
        am.Circle(50, pos=(50, 50), fill_color=0xFF00FFFF),
        am.Circle(50, pos=(100, 50), fill_color=0xFFFF00FF),
        am.Circle(50, pos=(75, 86.6), fill_color=0xFFFFFF00),
    ]
)
scene.add(label := am.SimpleText('Group-string', pos=(903, 168)))
label.style.set_glow(2, 'black')

scene.add(RectAndBars(905, 305, 140))
scene.add(EllipseAndBars(905, 305, 140, am.skia.Blenders.Arithmetic(0, 1, 1, -0.5)))  # grain merge
scene.add(am.SimpleText('Grain Merge', pos=(908, 318)))


def make_blender(sksl: str) -> am.skia.Blender:
    result = am.skia.RuntimeEffect.MakeForBlender(sksl)  # create a custom blender from sksl
    if not result.effect:
        raise RuntimeError(result.errorText)
    return am.skia.RuntimeBlendBuilder(result.effect).makeBlender()


blender = make_blender(
    """
half4 blend_porter_duff(half4 blendOp, half4 src, half4 dst) {  // taken from sksl_gpu.sksl from Skia
    half2 coeff = blendOp.xy + (blendOp.zw * (half2(dst.a, src.a) + min(blendOp.zw, 0)));
    return min(half4(1), src * coeff.x + dst * coeff.y);
}
half4 main(half4 c1, half4 c2) {
    return blend_porter_duff(half4(0,0,1,1), c1, c2);
}
"""
)  # porter duff blender
scene.add(RectAndBars(905, 455, 140))
scene.add(EllipseAndBars(905, 455, 140, blender))
scene.add(am.SimpleText('Porter Duff', pos=(908, 468)))

blender = make_blender(
    """
half4 main(half4 c1, half4 c2) {
    return c1.bgra;
}
"""
)  # also works as a color filter
scene.add(RectAndBars(905, 605, 140))
scene.add(EllipseAndBars(905, 605, 140, blender))
scene.add(am.SimpleText('Color Filter', pos=(908, 618)))


scene.update()
scene.show_frame()
