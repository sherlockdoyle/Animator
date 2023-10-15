import animator as am

scene = am.Scene()  # create a scene, the base of everything


scene.add(circle := am.Circle(100))  # add a circle to the scene with hex and rgb colors

scene.add(
    ellipse := am.Ellipse(100, 50, fill_color=am.PURPLE, stroke_color=am.CYAN)
)  # add an ellipse with preset colors
ellipse.rotate(15).set_relative_pos(
    am.relpos.BL
)  # rotate and set the position of the ellipse to the bottom left of the scene

scene.add(
    am.Rect(200, 200, pos=(50, 50), fill_color=am.color(), stroke_color=am.color())
)  # add a rectangle at (50, 50) with unique colors

scene.add(
    square := am.Rect(100, fill_color=am.color('blue500'), stroke_color=am.color('redA200'))
)  # add a square (rect with only one parameter) with colors from material design
square.set_relative_pos(am.relpos.TR)

scene.add(
    rrect := am.RoundRect(100, 200, (10, 20, 30, 40, 50, 60, 70, 80), fill_color='khaki', stroke_color='lawngreen')
)  # add a round rectangle with upto 8 radii and web colors
rrect.set_relative_pos(am.relpos.BR)

scene.add(
    star := am.Star(5, 100, fill_color=am.color(hsb=(120, 100, 100)), stroke_color=am.color(hsl=(240, 100, 50)))
)  # add a 5 pointed star with hsb and hsl colors
star.set_relative_to_entity(circle, am.relpos.RIGHT)  # set the position of the star to the right of the circle

scene.add(
    am.Path(
        'M307 240c0-53-8-85-8-119-2-34-5-76-39-95-48-27-107-15-160-8-32 5-70 18-81 53-19 57 8 116 17 173 4 35 18 80 60 82 46-5 89 18 126 44 29 21 28 68 63 83 49 18 99-7 149-9 72-5 153 0 216-43 35-30 27-82 49-119 17-26 55-38 50-83-12-57-70-87-122-101-30-8-73-8-91 23-14 40 11 79 11 119a120 130 0 11-240 0z',
        pos=(0, 0),
        stroke_color=am.color(0xFFABCDEF),
        paint_style=am.Style.PaintStyle.STROKE_ONLY,
        dash=[20, 10],
    )
)  # add a dashed stroke only path from SVG path data with ARGB color

scene.add(
    vertices := am.Vertices([(0, 0), (100, 100), (200, 0)], ['#ef0000', '#008b00', '#6161ff'])
)  # add a triangle with multi-colored vertices
vertices.center().set_relative_pos(am.relpos.TOP)  # center the triangle and set it to the top of the scene

w = 100
scene.add(
    patch := am.Patch(
        [
            (0, 0),
            (w / 3, w / 2),
            (w * 2 / 3, -w / 2),
            (w, 0),
            (w - w / 2, w / 3),
            (w + w / 2, w * 2 / 3),
            (w, w),
            (w * 2 / 3, w - w / 2),
            (w / 3, w + w / 2),
            (0, w),
            (w / 2, w * 2 / 3),
            (-w / 2, w / 3),
        ],
        colors=['rgb(218, 0, 185)', 'hsv(190,100 61)', 'hsb(69 100,50%)', 'hsl(167 100 26)'],
    )
)  # add a patch with 4 colors; a wide variety of color formats are supported
patch.center().set_relative_to_entity(ellipse, am.relpos.TR, padding=-27).scale(0.9)  # guess what this does?


scene.update()  # update the scene, this will progress the animation by one frame and draw all entities
scene.show_frame()  # show the frame, this will open a window and show the current frame
# scene.save_frame('test.png')  # save the current frame to a file
