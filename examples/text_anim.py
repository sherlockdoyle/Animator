import animator as am

scene = am.Scene()


scene.add(
    simple_text := am.SimpleText(  # change SimpleText to PathText for a different animation
        'Hello, world!',
        font_name='serif',
        font_size=100,
        paint_style=am.Style.PaintStyle.STROKE_ONLY,
        stroke_width=2,
    )
)  # add some simple text to the scene
simple_text.center()  # center the text
simple_text.style.set_fill_shader(
    am.Gradient.Linear(*simple_text.get_bounds())
    .add_color_stop(0, 'SpringGreen')
    .add_color_stop(1, 'DodgerBlue')
    .build()
)  # set the fill to a linear gradient from the top left to the bottom right

scene.add(line := am.Line(0, 0, 200, 0))  # add a line to the scene
line.center().set_relative_pos(am.relpos.TOP).move(0, 50)  # center the line and position it a bit below the top
text_on_path = line.add_text_on_path(
    'Hello, world!', font_name='serif', font_size=30, font_style='italic'
)  # add some italic text on the line

scene.add(
    emoji := am.SimpleText('🌲🐻🐰🐿️⛺️🌳🌞💧🌈🍔🍿🎥📚🔥💤', font_name='Noto Color Emoji', font_size=20)
)  # add some colorful emoji
emoji.set_relative_pos(am.relpos.TL)  # position the emoji in the top left corner


scene.add(
    text := am.Text.from_htmlish(
        """
Here's some <b>bold</b> and <i>italic</i> text. <b><i>This is both!</i></b> <u>Underline</u> and <s>strikethrough</s>
and <o>overline</o> and <mark>highlight</mark>, oh my! This is <span class='red italic'>red and italic</span>.<br/>
Math too: (<i>x</i> + <i>y</i>)<sup><small>2</small></sup> = <i>x</i><sup><small>2</small></sup> + 2<i>xy</i> +
                                                             <i>y</i><sup><small>2</small></sup>
<br/>
Margined circle: <obj margin=5>circle</obj>, that was inline!<br/>
Some code: <code>print('Hello, world!')</code>
        """,
        classes={
            'red': am.TextStyle(color='red'),  # define a style for red text
            'italic': am.TextStyle(fontStyle='italic'),  # define a style for italic text
        },
        objs={'circle': am.Circle(20)},  # define an entity to be used within the text
        font_name='Libre Baskerville,serif',  # use Libre Baskerville if available, otherwise use serif
        font_size=20,
        width=scene.width - 50,
    )
)  # add some text with html-like formatting
text.set_relative_pos(am.relpos.BL)  # position the text in the bottom left corner


t = 0  # a variable to keep track of the time


@scene.on_update  # call the decorated function every frame to update the scene
def update():
    global t

    if t < 100:
        simple_text.style.set_trim(0, (t - 10) / 80)  # trim the end of the text for the first 100 frames
    elif t == 100:
        simple_text.style.paint_style = (
            am.Style.PaintStyle.FILL_THEN_STROKE
        )  # change the paint style to fill then stroke
        simple_text.style.fill_paint.setAlphaf(0)  # set the alpha of the fill paint to 0
    elif t < 200:
        simple_text.style.fill_paint.setAlphaf((t - 110) / 80)  # fade in the fill paint for 80 frames
        simple_text.style.stroke_paint.setAlphaf(1 - (t - 110) / 80)  # fade out the stroke paint for 80 frames
    elif t == 200:
        simple_text.style.paint_style = am.Style.PaintStyle.FILL_ONLY  # change the paint style to fill only

    text_on_path.text_offset = t / 200 * line.path_length  # move the text along the path
    line.points[1].fY = t / 2  # move the end of the line down
    line._mark_dirty()  # mark the line as dirty so it recalculates its path

    t += 1
    return t > 200  # return True to stop the scene from updating after 200 frames


scene.play_frames()  # play the scene
