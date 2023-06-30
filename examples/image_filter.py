import numpy as np

import animator as am

scene = am.Scene(1000, 800)

img1 = am.skia.Image.open('examples/images/colors.png')  # load an image from a file
img1 = img1.resize(
    width=200, height=img1.height() * 200 // img1.width()
)  # resize the image to 200 pixels wide keeping the aspect ratio

img2 = am.skia.Image.open('examples/images/Under the Wave.jpg')  # load another image
img2 = img2.resize(width=img1.width(), height=img1.height())  # resize the image to the same size as the first image

imgf = am.skia.ImageFilters.Image(img2)  # create an ImageFilter from the second image

grid_arr = np.zeros(shape=(img1.width(), img1.height(), 4), dtype=np.uint8)  # create numpy array for an image
grid = am.skia.Image.fromarray(grid_arr, copy=False)  # create an image from the numpy array (shared memory)
grid_arr[::10, :] = grid_arr[:, ::10] = 255  # set every 10th row and column to white to create a grid


image_and_filters: list[tuple[am.skia.Image, am.skia.ImageFilter, str]] = [
    (
        img2,
        am.skia.ImageFilters.ColorFilter(am.skia.ColorFilters.Lighting(am.color('lightgreen'), am.color('lightred'))),
        'ColorFilter-Lighting',
    ),  # apply a color filter to the image, result = image * lightgreen + lightred
    (
        img2,
        am.skia.ImageFilters.ColorFilter(
            am.skia.ColorFilters.Matrix(
                [0.393, 0.769, 0.189, 0, 0.349, 0.686, 0.168, 0, 0.272, 0.534, 0.131, 0, 0, 0, 0, 1, 0, 0, 0, 0]
            )
        ),
        'ColorFilter-ColorMatrix',
    ),  # apply a color matrix to the image by multiplying each pixel by the matrix
    (
        img2,
        am.skia.ImageFilters.ColorFilter(am.skia.ColorFilters.LinearToSRGBGamma()),
        'ColorFilter-LinearToSRGBGamma',
    ),  # apply a gamma correction to the image, assuming the image is in linear color space
    (
        img2,
        am.skia.ImageFilters.ColorFilter(am.skia.ColorFilters.SRGBToLinearGamma()),
        'ColorFilter-SRGBToLinearGamma',
    ),  # apply a gamma correction to the image, assuming the image is in sRGB color space
    (img2, am.skia.ImageFilters.Offset(25, 25), 'Offset'),  # offset the image by 25 pixels in x and y direction
    (
        img2,
        am.skia.ImageFilters.MatrixConvolution((3, 3), [0, -1, 0, -1, 5, -1, 0, -1, 0]),
        'MatrixConvolution',
    ),  # apply a sharpen convolution matrix to the image
    (
        img1,
        am.skia.ImageFilters.Arithmetic(0, 0.5, 0.5, 0, background=imgf),
        'Arithmetic',
    ),  # apply an arithmetic filter to the image, result = image * 0.5 + imgf * 0.5
    (img1, am.skia.ImageFilters.Blend(am.skia.BlendMode.kDarken, imgf), 'Blend'),  # blend the image with imgf
    (
        img1,
        am.skia.ImageFilters.DisplacementMap(
            am.skia.ColorChannel.kR,
            am.skia.ColorChannel.kG,
            10,
            am.skia.ImageFilters.Shader(am.skia.Shader.MakeFractalNoise(0.1, 0.1, 1, 0)),
        ),
        'DisplacementMap',
    ),  # apply a displacement map to the image using the red and green channels of a fractal noise shader along the x and y axis respectively
    (img1, am.skia.ImageFilters.MatrixTransform(am.skia.Matrix.Skew(0, 0.3)), 'MatrixTransform'),  # skew the image
    (
        img1,
        am.skia.ImageFilters.RuntimeShader(
            am.Shader(
                """
uniform shader image;  // input image,
half4 main(float2 xy) {
    return image.eval(xy).gbra;  // swap red and green channels
}
                """
            ).builder  # a single uniform is present, which is automatically picked up for the input
        ),
        'RuntimeShader',
    ),  # apply a runtime shader to the image
    (img1, am.skia.ImageFilters.Dilate(10, 10), 'Dilate'),  # dilate the image
    (
        img1,
        am.skia.ImageFilters.DropShadow(5, 5, 2, 2, am.color('red')),
        'DropShadow',
    ),  # add a drop shadow to the image
    (
        img1,
        am.skia.ImageFilters.DropShadowOnly(5, 5, 2, 2, am.color('yellow')),
        'DropShadowOnly',
    ),  # only show the drop shadow
    (img1, am.skia.ImageFilters.Blur(2, 2), 'Blur'),  # blur the image
    (img1, am.skia.ImageFilters.Erode(10, 10), 'Erode'),  # erode the image
    (
        grid,
        am.skia.ImageFilters.Magnifier((0, 0, 200, 200), 2, 25),
        'Magnifier',
    ),  # magnify the whole image by 2 with a 25px padding; everything inside the padding is magnified by 2, the padded area is squished
    (
        grid,
        am.skia.ImageFilters.DistantLitSpecular((100, 100, 100), am.color('black'), 3, 0.5, 0.5),
        'DistantLitSpecular',
    ),  # draws the result of a distant light source from the direction (100, 100, 100) falling on a heightmap defined by the image's alpha channel
    (
        grid,
        am.skia.ImageFilters.PointLitSpecular((0, 0, 100), am.color('black'), 3, 0.5, 0.5),
        'PointLitSpecular',
    ),  # same as above, but with a point light source at (0, 0, 100)
    (
        grid,
        am.skia.ImageFilters.SpotLitSpecular((0, 0, 100), (100, 100, 0), 2, 45, am.color('green'), 3, 0.5, 0.5),
        'SpotLitSpecular',
    ),  # same as above, but with a spot light source at (0, 0, 100) pointing at (100, 100, 0)
]

x = y = 0
for image, image_filter, name in image_and_filters:  # loop over all images and filters
    scene.add(am.Image(image, pos=(x, y), image_filter=image_filter))  # add the image with the filter applied
    scene.add(label := am.SimpleText(name, pos=(x + 2, y + 14)))  # add the label
    label.style.set_glow(2, 'black')  # add a glow to the label to make it more readable
    y += 200
    if y > scene.height - 200:
        y = 0
        x += 200


scene.update()
scene.show_frame()
