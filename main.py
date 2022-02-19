import animator as am

scene = am.Scene()
scene.wait()

circle = scene.add(am.Circle(100)).set_relative_pos(am.CENTER)
circle.add(am.SimpleText('hello world'))

# scene.add(am.PropertyAnimator(circle).w.mul(2))
i = 0


def f(t):
    global i
    circle.reset_transform()
    circle.transform(am.math.rotate_x(i))
    circle.rotate(i)
    circle.transform(am.math.rotate_y(i))
    i += 1


scene.add(am.FuncAnim(f, duration=am.Anim.InfiniteDuration.INFINITE))

scene.add(am.ShowFPS())
scene.play(0)
# scene.save_frames('/home/sherlock/Desktop/Projects/Python/Animator2/temp/3.mp4')
