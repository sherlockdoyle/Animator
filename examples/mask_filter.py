import animator as am

scene = am.Scene()

am.Style.FILL_COLOR = am.color('yellow900')  # set the default fill color to yellow900


scene.add(circle := am.Circle(100))  # add a circle to the scene
circle.set_relative_pos(am.relpos.TL)  # position the circle in the top left corner
circle.style.set_mask_filter(
    am.skia.MaskFilter.MakeBlur(am.skia.BlurStyle.kNormal_BlurStyle, 20)
)  # add a normal blur mask, everything is blurred
circle.add(am.SimpleText('Normal', font_size=40).center())  # add label

scene.add(circle := am.Circle(100))
circle.set_relative_pos(am.relpos.TR)
circle.style.set_mask_filter(
    am.skia.MaskFilter.MakeBlur(am.skia.BlurStyle.kSolid_BlurStyle, 20)
)  # add a solid blur mask, inside is kept, outside is blurred
circle.add(am.SimpleText('Solid', font_size=40).center())

scene.add(circle := am.Circle(100))
circle.set_relative_pos(am.relpos.BL)
circle.style.set_mask_filter(
    am.skia.MaskFilter.MakeBlur(am.skia.BlurStyle.kInner_BlurStyle, 20)
)  # add a inner blur mask, inside is blurred, outside is untouched
circle.add(am.SimpleText('Inner', font_size=40).center())

scene.add(circle := am.Circle(100))
circle.set_relative_pos(am.relpos.BR)
circle.style.set_mask_filter(
    am.skia.MaskFilter.MakeBlur(am.skia.BlurStyle.kOuter_BlurStyle, 20)
)  # add a outer blur mask, inside is removed, outside is blurred
circle.add(am.SimpleText('Outer', font_size=40).center())

scene.add(circle := am.Circle(100))
circle.set_relative_pos(am.relpos.TOP)
circle.style.set_mask_filter(
    am.Gradient.Linear(-100, 0, 100, 0).add_colors('black', 'transparent').build()
)  # add a linear gradient mask, inside fades to transparent from left to right
circle.add(am.SimpleText('Fade', font_size=40).center())

scene.add(circle := am.Circle(100))
circle.set_relative_pos(am.relpos.BOTTOM)
circle.style.set_mask_filter(
    am.Shader(
        """
float rand(vec2 co) {  // random number generator
    return fract(sin(dot(co.xy, vec2(12.9898, 78.233))) * 43758.5453);
}
half4 main(vec2 p) {
    return half4(0, 0, 0, rand(p) < (p.x + 100) / 200);  // only the value of the alpha channel is used for masking
}
"""
    ).build()
)  # add a shader mask, inside is randomly removed based on x position
circle.add(am.SimpleText('Shader', font_size=40).center())


scene.update()
scene.show_frame()
