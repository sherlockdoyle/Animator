import animator as am

scene = am.Scene(720, 480)

path = am.skia.ParsePath.FromSVGString(
    "m183.5016 9.8064c-22.848 0-45.9516 24.0696-63.5052 46.6932-17.5644 22.6212-40.6848 46.692-63.498 46.692-25.7448 0-46.6896-20.9472-46.6896-46.6908 0-25.746 20.9448-46.692 46.6896-46.692 22.8132 0 45.9348 24.0744 63.498 46.6908 17.562 22.6116 40.6884 46.692 63.5052 46.692l46.6884-46.6908-46.6884-46.6944z"
)
center = path.getBounds().center()
small_path = path.makeTransform(am.skia.Matrix.Translate(-center.x(), -center.y()).postScale(0.07, 0.07))


path_effects: list[tuple[am.skia.PathEffect, str]] = [
    (am.skia.CornerPathEffect.Make(50), 'CornerPathEffect'),
    (am.skia.DiscretePathEffect.Make(10, 4), 'DiscretePathEffect'),
    (
        am.skia.PathEffect.MakeCompose(
            am.skia.DiscretePathEffect.Make(10, 4), am.skia.Line2DPathEffect.Make(2, am.skia.Matrix.Scale(1, 5))
        ),
        'Compose',
    ),
    (
        am.skia.Path1DPathEffect.Make(small_path, 20, 0, am.skia.Path1DPathEffect.Style.kTranslate_Style),
        'Path1DPathEffect-Translate',
    ),
    (am.skia.TrimPathEffect.Make(0.25, 0.75), 'TrimPathEffect'),
    (am.skia.DashPathEffect.Make([4, 8, 12, 20]), 'DashPathEffect'),
    (am.skia.PathEffect.MakeSum(am.skia.DashPathEffect.Make([4, 8]), am.skia.DiscretePathEffect.Make(10, 10)), 'Sum'),
    (
        am.skia.Path1DPathEffect.Make(small_path, 20, 0, am.skia.Path1DPathEffect.Style.kRotate_Style),
        'Path1DPathEffect-Rotate',
    ),
    (am.skia.TrimPathEffect.Make(0.25, 0.75, am.skia.TrimPathEffect.Mode.kInverted), 'TrimPathEffect-Inverted'),
    (am.skia.Line2DPathEffect.Make(2, am.skia.Matrix.Scale(1, 5).postRotate(30)), 'Line2DPathEffect'),
    (
        am.skia.Path2DPathEffect.Make(
            am.skia.Matrix.Scale(30, 10), small_path.makeTransform(am.skia.Matrix.Scale(2, 2))
        ),
        'Path2DPathEffect',
    ),
    (
        am.skia.Path1DPathEffect.Make(small_path, 20, 0, am.skia.Path1DPathEffect.Style.kMorph_Style),
        'Path1DPathEffect-Morph',
    ),
]

x = y = 0
for effect, name in path_effects:
    scene.add(entity := am.Path(path, pos=(x, y), path_effect=effect))
    entity.add(label := am.SimpleText(name, pos=(119.9964, 56.4996)))
    label.center()
    label.style.set_glow(2, 'black')
    y += 120
    if y > scene.height - 120:
        y = 0
        x += 240


scene.update()
scene.show_frame()
