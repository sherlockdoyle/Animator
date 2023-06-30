import animator as am

scene = am.Scene()


shader = am.Shader(
    """
uniform shader image;  // the image to be drawn
uniform float2 div_mul;  // the multiplier for the wave effect
uniform float shift;  // the shift of the wave effect
layout(color) uniform vec4 tint;  // the tint of the image

half4 main(float2 xy) {  // the main function is called for each pixel
    xy.x += sin(xy.y / div_mul.x + shift) * div_mul.y;  // add a wave effect
    xy.y += sin(xy.x / div_mul.y + shift) * div_mul.x;  // add more wave effect
    return image.eval(xy).rgba * tint;  // return the color of the image at the given position multiplied by the tint
}
"""
)  # create a shader from the given sksl code
shader['image'] = (
    am.Image('examples/images/Under the Wave.jpg').scale_image(0.25).get_shader()
)  # set the image as a shader
shader['div_mul'] = (20, 30)  # set the div_mul uniform
shader['tint'] = am.color('green300')  # set the tint to whitish green

scene.add(background := am.PaintFill(fill_color=shader.build()))  # add a paint fill with the shader for the background

scene.add(image := am.Image('examples/images/colors.png'))  # add an image from the given path
image.center()  # center the image

r = (250, 200, 350, 300)
scene.add(
    am.Rect.from_ltrb(*r, paint_style=am.Style.PaintStyle.STROKE_ONLY, stroke_width=1)
)  # add a rect to show the bounds of the snapshot source
scene.add(snapshot := am.Snapshot(r))  # add a snapshot of the rect
snapshot.scale(2).set_relative_pos(am.relpos.BR)  # scale the snapshot and set it to the bottom right of the scene

scene.add(
    rect := am.Rect(  # add a rect for the blender
        200,
        200,
        style='fill',  # alternate of paint_style=am.Style.PaintStyle.FILL_ONLY
        fill_color=am.ShaderBlender('exclusion')[  # use the exclusion blend mode to mix
            am.Gradient.Conical(0, 0).add_colors('red', 'blue', 'yellow', 'green', 'red').build(),  # a conical gradient
            am.skia.Shader.MakeFractalNoise(0.01, 0.01, 1, 1),  # a fractal perlin noise shader
            am.skia.Shader.MakeTurbulence(0.02, 0.02, 2, 2),  # and a turbulence perlin noise shader
        ],
    )
)
rect.center().set_relative_pos(am.relpos.TR)  # center the rect so that the radial gradient is centered

scene.add(backdrop := am.BackDrop(am.skia.ImageFilters.Blur(5, 5), (200, 200)))  # add a blurry backdrop
backdrop.set_relative_pos(am.relpos.BL)  # set the backdrop to the bottom left of the scene

GREYSCALE = [0.2126, 0.7152, 0.0722, 0, 0]  # r*0.2126 + g*0.7152 + b*0.0722 + a*0 + 0
scene.add(
    greyscale := am.BackDrop(
        am.skia.ImageFilters.ColorFilter(
            am.skia.ColorFilters.Matrix(GREYSCALE + GREYSCALE + GREYSCALE + [0, 0, 0, 1, 0])
        ),
        (200, 200),
    )
)  # add a greyscale backdrop
greyscale.set_relative_pos(am.relpos.TL)  # set the backdrop to the top left of the scene


shift = 0  # the shift of the wave effect


@scene.on_update  # keep updating the scene indefinitely
def update() -> None:
    global shift
    shader['shift'] = shift  # set the shift
    background.style.set_fill_shader(shader.build())  # update the background's shader
    if shift % 2 > 1:  # after every 200 frames
        snapshot.sampling_options = am.skia.SamplingOptions(
            am.skia.CubicResampler.Mitchell()
        )  # make the snapshot smooth
    else:  # then
        snapshot.sampling_options = am.skia.SamplingOptions()  # make the snapshot pixelated
    shift += 0.01  # increase the shift


scene.play_frames()
