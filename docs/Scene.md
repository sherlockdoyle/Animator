# Scene

A `Scene` is the main component of Animator. It holds the entities and the animations that you want to display or save. To use Animator, you need to create a scene first.

```python
import animator as am

scene = am.Scene()
# add your code here
scene.play_frames()
```

The rest of the documentation assumes that you have this code snippet at the beginning and that you add your code where the comment is.

## Customizing your scene

### Resolution

You can set the resolution of your scene by specifying the `width: int` and `height: int` of your scene in pixels. The default values are 854 and 480, respectively.

```python
scene = am.Scene(1920, 1080)
```

Alternatively, you can use a predefined resolution string to create your scene. The available resolutions and their corresponding dimensions are:

| Resolution                      | Width | Height |
| ------------------------------- | ----- | ------ |
| `144p`                          | 256   | 144    |
| `240p`                          | 426   | 240    |
| `360p`                          | 640   | 360    |
| `480p`                          | 854   | 480    |
| `720p`, `hd`                    | 1280  | 720    |
| `1080p`, `fhd`, `fullhd`        | 1920  | 1080   |
| `1440p`, `2k`                   | 2560  | 1440   |
| `2160p`, `4k`, `uhd`, `ultrahd` | 3840  | 2160   |

```python
scene = am.Scene('fhd')
```

The width and height of your scene can be accessed as `scene.width` and `scene.height`.

Say you want to render the same scene at different resolutions. If you just change the `width` or `height` of your scene, the entities in your scene will not be scaled automatically, and they may appear too large or too small. For example:

##### Original scene

<demo appendprefix image args='200, 200'>
scene.add(am.Circle(100))
</demo>

##### Resized

<demo appendprefix image args='400, 400'>
scene.add(am.Circle(100))
</demo>

The scene is resized, but the circle stays the same size, so it looks smaller. To fix this, you can use the `scale` argument to scale the scene and its entities by a given factor. You can use a float value to scale your scene proportionally, or a tuple of two integers to scale your scene to width and height separately. You can also use a resolution string to scale your scene to match that resolution. These options are equivalent to the first two arguments of the constructor (`width`/`resolution`, `height`).

##### Scaled

<demo appendprefix image args='200, 200, scale=2'>
scene.add(am.Circle(100))
</demo>

The scene and the circle are both scaled up, so they look the same.

If the aspect ratio of the scale (remember, scale can be a tuple or a string) is different from the aspect ratio of the scene, the scene will be padded with empty space to fit the scale. This may reveal some content that is outside the original scene boundaries. To avoid this, you can call `scene.clip()` to trim the excess content.

Note that, scaling a scene does not change the width or height of the scene. It only creates a scaled frame.

### FPS

You can set the frames per second of your animation by specifying the `fps: int` argument. The default value is 30. This argument affects the duration and quality of your animation when you save it. When you play your animation, the actual fps may vary depending on your system resources.

```python
scene = am.Scene('2k', fps=60)
```

The FPS can be accessed as `scene.fps`.

### Background color

You can set the background color of your scene by setting `scene.bgcolor` to a skia Color4f object. You can use the `am.color()` function to parse a color string. The default background color is opaque black. Note that, most default colors used across Animator assumes a black background.

```python
scene = am.Scene()
scene.bgcolor = am.color('white')
```

### The frame and canvas

The scene uses an internal frame to store the pixel values of its content. You can access this frame by calling `scene.frame`. The frame is a numpy array with the shape `(height, width, 4)`, where the last dimension represents the RGBA values of each pixel. The frame may contain random values when the scene is created. Ideally, the scene will clear the frame before drawing anything on it.

The scene also uses a skia canvas to draw on the frame. You can access this canvas by calling `scene.canvas`.

### Clipping

When a scene is scaled to fit a different aspect ratio, it may have empty space on the sides as padding. However, this does not prevent the scene from drawing anything outside its original boundaries. To avoid this, you can use the `scene.clip()` method to clip out the extra space. This method will also clear the scene before clipping to remove any random values.

##### Original scene

<demo appendprefix image args='200, 100'>
scene.add(am.Circle(100))
</demo>

##### Without clip

<demo appendprefix image args='200, 100, scale=(200, 200)'>
scene.add(am.Circle(100))
</demo>

A 200x100 scene is scaled to fit a 200x200 frame, but the original aspect ratio is not preserved. The scene is padded with empty space at the top and bottom. The circle is fully visible in the padded area.

##### With clip

<demo appendprefix image args='200, 100, scale=(200, 200)'>
scene.clip()
scene.add(am.Circle(100))
</demo>

A 200x100 scene is scaled to fit a 200x200 frame, but the original aspect ratio is not preserved. The circle is not visible in the padded area.

## Cleaning the scene

Before drawing anything on the scene, it is necessary to clear the scene, either to eliminate any garbage values or the previous drawing. This can be achieved by invoking either `scene.clear()` or `scene.clear_with_bgcolor()`.

The `scene.clear()` method erases the scene by setting all the pixels in the frame to 0. Although slightly slower than `scene.clear_with_bgcolor()`, it functions regardless of the clip status.

On the other hand, the `scene.clear_with_bgcolor()` method erases the scene by filling it with the background color (`bgcolor`). It is faster than `scene.clear()`, but it only affects the clipped area of the scene. This method is used internally by the scene to erase the frame before any drawing occurs.

## Drawing

### The canvas

The scene utilizes a Skia canvas to draw on the frame, which can be accessed through `scene.canvas`. This allows for drawing on the scene in a primitive manner and supports anything the Skia canvas offers. For further details about the Skia canvas, refer to the [Skia documentation](https://skia.org/docs/user/api/skcanvas_overview/). Here's an example:

<demo appendsuffix image noupdate>
scene.canvas.drawCircle(
    (scene.width / 2, scene.height / 2), 100, am.skia.Paint(color=am.skia.ColorRED)
)
</demo>

### Context2D

[`Context2d`]() serves as a wrapper around a Skia canvas, providing methods similar to the HTML canvas element. It offers a more convenient way to draw using the canvas and can be accessed through `scene.context2d`. For additional information about `Context2d`, consult its documentation. Here's an example:

<demo appendsuffix image noupdate>
ctx = scene.context2d
ctx.circle(scene.width / 2, scene.height / 2, 100)
ctx.fillStyle = am.skia.ColorGREEN
ctx.fill()
</demo>

### Quick draw

The `scene.quickdraw()` method offers a quick means to draw and visualize the scene. This method serves as a context manager, returning a `Context2d` object that can be utilized for drawing on the scene. Once the context is exited, the scene is displayed in a new window or in the Jupyter notebook output, depending on the environment.

```python
import animator as am

scene = am.Scene()
with scene.quickdraw() as ctx:
    ctx.circle(scene.width / 2, scene.height / 2, 100)
    ctx.fill()
```

The above code will display a circle in the center of the scene.

### Entities

Entities are the preferred way to draw in Animator. Entities are objects that can draw on the scene and transform their appearance as needed. You can read more about the [`Entity`]() class and its methods in its documentation. To add an entity to the scene, you can use the `scene.add()` method, which takes one or more entities as arguments. Animator comes with a number of predefined entities that you can use to create various graphics and animations. You can also create your own custom entities by subclassing the `Entity` class.

<demo image>
scene.add(am.Circle(100), am.Rect(200, 100, fill_color='red'))  # add two entities
scene.add(
    rect := am.Rect(
        200,
        fill_color=am.Gradient.Linear(0, 0, 200, 200)
        .add_colors('green', 'blue')
        .build(),
    ).rotate(45)
)
rect.set_relative_pos(am.relpos.TL)  # set the relative position of the rectangle to the top left of the scene
</demo>

While entities can be created by themselves, some of the methods of the `Entity` class require a scene to work properly. For example, the `set_relative_pos()` method in the above example needs to know the dimensions of the scene to position the entity correctly. That's why we add the entity to the scene first before calling the method. We use the walrus operator to assign the entity to a variable, so that we can access its methods later.

However, you may not need to add the entity to the scene always. In some cases, you may just want to attach the entity to the scene without adding it to the scene's list of entities. You can do this by using the `@` operator, which attaches the entity to the scene and returns the entity itself. This allows you to chain the entity's methods after the operator.

```python
circle = am.Circle(100)
circle.set_relative_pos(am.relpos.TOP)  # This will fail because the circle does not have a scene to refer to.
(circle @ scene).set_relative_pos(am.relpos.TOP)  # This will work because the circle is attached to the scene and positioned at the top of the scene.
```

### Drawing on each frame

Another way of drawing on the scene is by using the `scene.on_draw(func)` method, which allows you to add callbacks that are called every time the scene is drawn. The `on_draw` function takes a callback function as an argument, which is called on each frame. You can use this function to control animations manually or run code on each frame. The function may also return one or more entities. These entities will then be temporarily added to the scene, drawn on the frame, and then removed. Internally, this method just adds a `FuncEntity` to the scene. This method can also be used as a decorator, as shown in the following example:

<demo>
t = 0

@scene.on_draw
def draw():
    global t
    t += 1
    return am.Circle(100, pos=(t / 60 * scene.width, t / 60 * scene.height))

scene.wait(2)  # wait for 2 seconds to see the animation
</demo>

## Animations

Animations is what Animator is made for. You can learn more about [animation]() in its documentation, but here's a gist.

### The timeline

Internally, all animations reside on a timeline. They start at a point in the timeline and goes on for a certain duration. To add an animation to the timeline, the most primitive method, `scene.animation_manager.add(anim, start_time)` can be used. The duration for the animation is specified in the animation itself. Everything is in seconds.

<demo>
scene.animation_manager.add(am.DrawIn(am.Circle(100), 2), 0)
</demo>

An animation which creates a circle in the scene with a duration of 2 seconds. The animation will start at the beginning of the timeline, ie. at time 0.

### Predefined linear animations

Instead of adding each animations at a specific time, you can instead use `scene.animate(anim)` which will add the animations using a internal marker. The marker starts at time 0. Calling `scene.wait()` will update the marker to the end of all the added animations.

This method adds one or more animations to the scene at a point in time marked by an internal marker. Calling [`scene.wait()`](#scene.wait) will update the marker to the current time. See the [`AnimationManager`]() class for more information. The animations will be played in order.

<demo>
scene.animate(am.SlideIn(circle := am.Circle(100), 2))  # store the circle in a variable
scene.wait(1)  # wait for 1 second and update the marker
scene.animate(am.SlideOut(circle, 2, dir=am.relpos.BOTTOM))  # refer to the circle entity
</demo>

## `scene.once(func)`

Calls a callback function once at a point in time marked by an internal marker. This method can also be used as a decorator, as shown in the following example:

<demo>
scene.wait(1)  # wait for 1 second
@scene.once
def func():
    scene.add(am.Circle(100))  # then add a circle
scene.wait(1)
</demo>

## `scene.wait(seconds: float = 0)`

Wait for the given number of `seconds` and update the internal marker for further animations. If no `seconds` are given, just update the marker.