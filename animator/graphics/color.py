"""
Colors make the world go round. In animator, colors are represented as :class:`skia.Color4f` objects from the underlying
Skia library. The :class:`skia.Color4f` class provides an object-oriented interface to a color's red, green, blue, and
alpha channels, each with a value between 0 and 1. It can also be used as a list of 4 floats representing the same
channels. You can also use a tuple of 4 floats in most places where a :class:`skia.Color4f` is expected.

Some colors are predefined:

======= ====== ==== ===== ====== ===========
BLACK   BLUE   CYAN GRAY  GREEN  LIME
MAGENTA MAROON NAVY OLIVE ORANGE PURPLE
RED     SILVER TEAL WHITE YELLOW TRANSPARENT
======= ====== ==== ===== ====== ===========

Some examples and possible mistakes to avoid:

>>> color(127.5, 255, 0, 1)  # simplest way to create a color, red[0, 255], green[0, 255], blue[0, 255], alpha[0, 1]
Color4f(0.5, 1, 0, 1)
>>> color(255.0)  # grayscale, if a single float is given
Color4f(1, 1, 1, 1)
>>> color(255)  # if an int is given, it is passed as a packed 32-bit ARGB value
Color4f(0, 0, 1, 0)
>>> color('MarOon')  # case-insensitive color name
Color4f(0.501961, 0, 0, 1)
>>> color('red50')  # material color shade
Color4f(1, 0.921569, 0.933333, 1)
>>> color('limeA700')  # material color accent
Color4f(0.682353, 0.917647, 0, 1)
>>> color(r'r G b ( 50% 0, 0.0\\0.5)')  # strangely formatted CSS functional notation
Color4f(0.5, 0, 0, 0.5)
>>> color('420, 42, 3.14, max=(420, 42, 3.14), a=0.123)  # white, but with a custom max value and alpha
Color4f(1, 1, 1, 0.123)
"""
import colorsys
import re
from typing import Literal, Sequence

from animator import skia
from animator._common_types import ColorLike

__WHITESPACE_RE = re.compile(r'\s+')
__NUMBER_RE = re.compile(r'[-+]?[0-9]+[.]?[0-9]*([eE][-+]?[0-9]+)?%?')
__MATERIAL_COLOR_RE = re.compile(
    r'^(red|p(ink|urple)|deep_(purple|orange)|indigo|b(lue(|_gr[ae]y)|rown)|li(ght_(blue|green)|me)|cyan|teal|gr(e(en|y)|ay)|yellow|amber|orange)(50|[1-9]00|a[1247]00)$'
)

BLACK = skia.Color4f.kBlack
BLUE = skia.Color4f.kBlue
CYAN = skia.Color4f.kCyan
GRAY = skia.Color4f.kGray
GREEN = skia.Color4f(0, 0.5, 0, 1)
LIME = skia.Color4f.kGreen
MAGENTA = skia.Color4f.kMagenta
MAROON = skia.Color4f(0.5, 0, 0, 1)
NAVY = skia.Color4f(0, 0, 0.5, 1)
OLIVE = skia.Color4f(0.5, 0.5, 0, 1)
ORANGE = skia.Color4f(1, 0.5, 0, 1)
PURPLE = skia.Color4f(0.5, 0, 0.5, 1)
RED = skia.Color4f.kRed
SILVER = skia.Color4f.kLtGray
TEAL = skia.Color4f(0, 0.5, 0.5, 1)
WHITE = skia.Color4f.kWhite
YELLOW = skia.Color4f.kYellow
TRANSPARENT = skia.Color4f.kTransparent

ColorType = Literal['rgb', 'hsb', 'hsl']
ColorTuple = tuple[float, float, float, float]
ColorTuple3 = tuple[float, float, float]

__default_max: dict[ColorType, ColorTuple] = {
    'rgb': (255, 255, 255, 1),
    'hsb': (360, 100, 100, 1),
    'hsl': (360, 100, 100, 1),
}
__css_colors: dict[str, tuple[int, int, int]] = {
    'black': (0, 0, 0),
    'silver': (192, 192, 192),
    'gray': (128, 128, 128),
    'white': (255, 255, 255),
    'maroon': (128, 0, 0),
    'red': (255, 0, 0),
    'purple': (128, 0, 128),
    'fuchsia': (255, 0, 255),
    'green': (0, 128, 0),
    'lime': (0, 255, 0),
    'olive': (128, 128, 0),
    'yellow': (255, 255, 0),
    'navy': (0, 0, 128),
    'blue': (0, 0, 255),
    'teal': (0, 128, 128),
    'aqua': (0, 255, 255),
    'orange': (255, 165, 0),
    'aliceblue': (240, 248, 255),
    'antiquewhite': (250, 235, 215),
    'aquamarine': (127, 255, 212),
    'azure': (240, 255, 255),
    'beige': (245, 245, 220),
    'bisque': (255, 228, 196),
    'blanchedalmond': (255, 235, 205),
    'blueviolet': (138, 43, 226),
    'brown': (165, 42, 42),
    'burlywood': (222, 184, 135),
    'cadetblue': (95, 158, 160),
    'chartreuse': (127, 255, 0),
    'chocolate': (210, 105, 30),
    'coral': (255, 127, 80),
    'cornflowerblue': (100, 149, 237),
    'cornsilk': (255, 248, 220),
    'crimson': (220, 20, 60),
    'cyan': (0, 255, 255),
    'darkblue': (0, 0, 139),
    'darkcyan': (0, 139, 139),
    'darkgoldenrod': (184, 134, 11),
    'darkgray': (169, 169, 169),
    'darkgreen': (0, 100, 0),
    'darkgrey': (169, 169, 169),
    'darkkhaki': (189, 183, 107),
    'darkmagenta': (139, 0, 139),
    'darkolivegreen': (85, 107, 47),
    'darkorange': (255, 140, 0),
    'darkorchid': (153, 50, 204),
    'darkred': (139, 0, 0),
    'darksalmon': (233, 150, 122),
    'darkseagreen': (143, 188, 143),
    'darkslateblue': (72, 61, 139),
    'darkslategray': (47, 79, 79),
    'darkslategrey': (47, 79, 79),
    'darkturquoise': (0, 206, 209),
    'darkviolet': (148, 0, 211),
    'deeppink': (255, 20, 147),
    'deepskyblue': (0, 191, 255),
    'dimgray': (105, 105, 105),
    'dimgrey': (105, 105, 105),
    'dodgerblue': (30, 144, 255),
    'firebrick': (178, 34, 34),
    'floralwhite': (255, 250, 240),
    'forestgreen': (34, 139, 34),
    'gainsboro': (220, 220, 220),
    'ghostwhite': (248, 248, 255),
    'gold': (255, 215, 0),
    'goldenrod': (218, 165, 32),
    'greenyellow': (173, 255, 47),
    'grey': (128, 128, 128),
    'honeydew': (240, 255, 240),
    'hotpink': (255, 105, 180),
    'indianred': (205, 92, 92),
    'indigo': (75, 0, 130),
    'ivory': (255, 255, 240),
    'khaki': (240, 230, 140),
    'lavender': (230, 230, 250),
    'lavenderblush': (255, 240, 245),
    'lawngreen': (124, 252, 0),
    'lemonchiffon': (255, 250, 205),
    'lightblue': (173, 216, 230),
    'lightcoral': (240, 128, 128),
    'lightcyan': (224, 255, 255),
    'lightgoldenrodyellow': (250, 250, 210),
    'lightgray': (211, 211, 211),
    'lightgreen': (144, 238, 144),
    'lightgrey': (211, 211, 211),
    'lightpink': (255, 182, 193),
    'lightsalmon': (255, 160, 122),
    'lightseagreen': (32, 178, 170),
    'lightskyblue': (135, 206, 250),
    'lightslategray': (119, 136, 153),
    'lightslategrey': (119, 136, 153),
    'lightsteelblue': (176, 196, 222),
    'lightyellow': (255, 255, 224),
    'limegreen': (50, 205, 50),
    'linen': (250, 240, 230),
    'magenta': (255, 0, 255),
    'mediumaquamarine': (102, 205, 170),
    'mediumblue': (0, 0, 205),
    'mediumorchid': (186, 85, 211),
    'mediumpurple': (147, 112, 219),
    'mediumseagreen': (60, 179, 113),
    'mediumslateblue': (123, 104, 238),
    'mediumspringgreen': (0, 250, 154),
    'mediumturquoise': (72, 209, 204),
    'mediumvioletred': (199, 21, 133),
    'midnightblue': (25, 25, 112),
    'mintcream': (245, 255, 250),
    'mistyrose': (255, 228, 225),
    'moccasin': (255, 228, 181),
    'navajowhite': (255, 222, 173),
    'oldlace': (253, 245, 230),
    'olivedrab': (107, 142, 35),
    'orangered': (255, 69, 0),
    'orchid': (218, 112, 214),
    'palegoldenrod': (238, 232, 170),
    'palegreen': (152, 251, 152),
    'paleturquoise': (175, 238, 238),
    'palevioletred': (219, 112, 147),
    'papayawhip': (255, 239, 213),
    'peachpuff': (255, 218, 185),
    'peru': (205, 133, 63),
    'pink': (255, 192, 203),
    'plum': (221, 160, 221),
    'powderblue': (176, 224, 230),
    'rosybrown': (188, 143, 143),
    'royalblue': (65, 105, 225),
    'saddlebrown': (139, 69, 19),
    'salmon': (250, 128, 114),
    'sandybrown': (244, 164, 96),
    'seagreen': (46, 139, 87),
    'seashell': (255, 245, 238),
    'sienna': (160, 82, 45),
    'skyblue': (135, 206, 235),
    'slateblue': (106, 90, 205),
    'slategray': (112, 128, 144),
    'slategrey': (112, 128, 144),
    'snow': (255, 250, 250),
    'springgreen': (0, 255, 127),
    'steelblue': (70, 130, 180),
    'tan': (210, 180, 140),
    'thistle': (216, 191, 216),
    'tomato': (255, 99, 71),
    'turquoise': (64, 224, 208),
    'violet': (238, 130, 238),
    'wheat': (245, 222, 179),
    'whitesmoke': (245, 245, 245),
    'yellowgreen': (154, 205, 50),
    'rebeccapurple': (102, 51, 153),
}
__material_colors: dict[str, dict[int, tuple[int, int, int]]] = {
    'red': {
        50: (255, 235, 238),
        100: (255, 205, 210),
        200: (239, 154, 154),
        300: (229, 115, 115),
        400: (239, 83, 80),
        500: (244, 67, 54),
        600: (229, 57, 53),
        700: (211, 47, 47),
        800: (198, 40, 40),
        900: (183, 28, 28),
        -100: (255, 138, 128),
        -200: (255, 82, 82),
        -400: (255, 23, 68),
        -700: (213, 0, 0),
    },
    'pink': {
        50: (252, 228, 236),
        100: (248, 187, 208),
        200: (244, 143, 177),
        300: (240, 98, 146),
        400: (236, 64, 122),
        500: (233, 30, 99),
        600: (216, 27, 96),
        700: (194, 24, 91),
        800: (173, 20, 87),
        900: (136, 14, 79),
        -100: (255, 128, 171),
        -200: (255, 64, 129),
        -400: (245, 0, 87),
        -700: (197, 17, 98),
    },
    'purple': {
        50: (243, 229, 245),
        100: (225, 190, 231),
        200: (206, 147, 216),
        300: (186, 104, 200),
        400: (171, 71, 188),
        500: (156, 39, 176),
        600: (142, 36, 170),
        700: (123, 31, 162),
        800: (106, 27, 154),
        900: (74, 20, 140),
        -100: (234, 128, 252),
        -200: (224, 64, 251),
        -400: (213, 0, 249),
        -700: (170, 0, 255),
    },
    'deep_purple': {
        50: (237, 231, 246),
        100: (209, 196, 233),
        200: (179, 157, 219),
        300: (149, 117, 205),
        400: (126, 87, 194),
        500: (103, 58, 183),
        600: (94, 53, 177),
        700: (81, 45, 168),
        800: (69, 39, 160),
        900: (49, 27, 146),
        -100: (179, 136, 255),
        -200: (124, 77, 255),
        -400: (101, 31, 255),
        -700: (98, 0, 234),
    },
    'indigo': {
        50: (232, 234, 246),
        100: (197, 202, 233),
        200: (159, 168, 218),
        300: (121, 134, 203),
        400: (92, 107, 192),
        500: (63, 81, 181),
        600: (57, 73, 171),
        700: (48, 63, 159),
        800: (40, 53, 147),
        900: (26, 35, 126),
        -100: (140, 158, 255),
        -200: (83, 109, 254),
        -400: (61, 90, 254),
        -700: (48, 79, 254),
    },
    'blue': {
        50: (227, 242, 253),
        100: (187, 222, 251),
        200: (144, 202, 249),
        300: (100, 181, 246),
        400: (66, 165, 245),
        500: (33, 150, 243),
        600: (30, 136, 229),
        700: (25, 118, 210),
        800: (21, 101, 192),
        900: (13, 71, 161),
        -100: (130, 177, 255),
        -200: (68, 138, 255),
        -400: (41, 121, 255),
        -700: (41, 98, 255),
    },
    'light_blue': {
        50: (225, 245, 254),
        100: (179, 229, 252),
        200: (129, 212, 250),
        300: (79, 195, 247),
        400: (41, 182, 246),
        500: (3, 169, 244),
        600: (3, 155, 229),
        700: (2, 136, 209),
        800: (2, 119, 189),
        900: (1, 87, 155),
        -100: (128, 216, 255),
        -200: (64, 196, 255),
        -400: (0, 176, 255),
        -700: (0, 145, 234),
    },
    'cyan': {
        50: (224, 247, 250),
        100: (178, 235, 242),
        200: (128, 222, 234),
        300: (77, 208, 225),
        400: (38, 198, 218),
        500: (0, 188, 212),
        600: (0, 172, 193),
        700: (0, 151, 167),
        800: (0, 131, 143),
        900: (0, 96, 100),
        -100: (132, 255, 255),
        -200: (24, 255, 255),
        -400: (0, 229, 255),
        -700: (0, 184, 212),
    },
    'teal': {
        50: (224, 242, 241),
        100: (178, 223, 219),
        200: (128, 203, 196),
        300: (77, 182, 172),
        400: (38, 166, 154),
        500: (0, 150, 136),
        600: (0, 137, 123),
        700: (0, 121, 107),
        800: (0, 105, 92),
        900: (0, 77, 64),
        -100: (167, 255, 235),
        -200: (100, 255, 218),
        -400: (29, 233, 182),
        -700: (0, 191, 165),
    },
    'green': {
        50: (232, 245, 233),
        100: (200, 230, 201),
        200: (165, 214, 167),
        300: (129, 199, 132),
        400: (102, 187, 106),
        500: (76, 175, 80),
        600: (67, 160, 71),
        700: (56, 142, 60),
        800: (46, 125, 50),
        900: (27, 94, 32),
        -100: (185, 246, 202),
        -200: (105, 240, 174),
        -400: (0, 230, 118),
        -700: (0, 200, 83),
    },
    'light_green': {
        50: (241, 248, 233),
        100: (220, 237, 200),
        200: (197, 225, 165),
        300: (174, 213, 129),
        400: (156, 204, 101),
        500: (139, 195, 74),
        600: (124, 179, 66),
        700: (104, 159, 56),
        800: (85, 139, 47),
        900: (51, 105, 30),
        -100: (204, 255, 144),
        -200: (178, 255, 89),
        -400: (118, 255, 3),
        -700: (100, 221, 23),
    },
    'lime': {
        50: (249, 251, 231),
        100: (240, 244, 195),
        200: (230, 238, 156),
        300: (220, 231, 117),
        400: (212, 225, 87),
        500: (205, 220, 57),
        600: (192, 202, 51),
        700: (175, 180, 43),
        800: (158, 157, 36),
        900: (130, 119, 23),
        -100: (244, 255, 129),
        -200: (238, 255, 65),
        -400: (198, 255, 0),
        -700: (174, 234, 0),
    },
    'yellow': {
        50: (255, 253, 231),
        100: (255, 249, 196),
        200: (255, 245, 157),
        300: (255, 241, 118),
        400: (255, 238, 88),
        500: (255, 235, 59),
        600: (253, 216, 53),
        700: (251, 192, 45),
        800: (249, 168, 37),
        900: (245, 127, 23),
        -100: (255, 255, 141),
        -200: (255, 255, 0),
        -400: (255, 234, 0),
        -700: (255, 214, 0),
    },
    'amber': {
        50: (255, 248, 225),
        100: (255, 236, 179),
        200: (255, 224, 130),
        300: (255, 213, 79),
        400: (255, 202, 40),
        500: (255, 193, 7),
        600: (255, 179, 0),
        700: (255, 160, 0),
        800: (255, 143, 0),
        900: (255, 111, 0),
        -100: (255, 229, 127),
        -200: (255, 215, 64),
        -400: (255, 196, 0),
        -700: (255, 171, 0),
    },
    'orange': {
        50: (255, 243, 224),
        100: (255, 224, 178),
        200: (255, 204, 128),
        300: (255, 183, 77),
        400: (255, 167, 38),
        500: (255, 152, 0),
        600: (251, 140, 0),
        700: (245, 124, 0),
        800: (239, 108, 0),
        900: (230, 81, 0),
        -100: (255, 209, 128),
        -200: (255, 171, 64),
        -400: (255, 145, 0),
        -700: (255, 109, 0),
    },
    'deep_orange': {
        50: (251, 233, 231),
        100: (255, 204, 188),
        200: (255, 171, 145),
        300: (255, 138, 101),
        400: (255, 112, 67),
        500: (255, 87, 34),
        600: (244, 81, 30),
        700: (230, 74, 25),
        800: (216, 67, 21),
        900: (191, 54, 12),
        -100: (255, 158, 128),
        -200: (255, 110, 64),
        -400: (255, 61, 0),
        -700: (221, 44, 0),
    },
    'brown': {
        50: (239, 235, 233),
        100: (215, 204, 200),
        200: (188, 170, 164),
        300: (161, 136, 127),
        400: (141, 110, 99),
        500: (121, 85, 72),
        600: (109, 76, 65),
        700: (93, 64, 55),
        800: (78, 52, 46),
        900: (62, 39, 35),
        -100: (215, 204, 200),
        -200: (188, 170, 164),
        -400: (141, 110, 99),
        -700: (93, 64, 55),
    },
    'grey': {
        50: (250, 250, 250),
        100: (245, 245, 245),
        200: (238, 238, 238),
        300: (224, 224, 224),
        400: (189, 189, 189),
        500: (158, 158, 158),
        600: (117, 117, 117),
        700: (97, 97, 97),
        800: (66, 66, 66),
        900: (33, 33, 33),
        -100: (245, 245, 245),
        -200: (238, 238, 238),
        -400: (189, 189, 189),
        -700: (97, 97, 97),
    },
    'blue_grey': {
        50: (236, 239, 241),
        100: (207, 216, 220),
        200: (176, 190, 197),
        300: (144, 164, 174),
        400: (120, 144, 156),
        500: (96, 125, 139),
        600: (84, 110, 122),
        700: (69, 90, 100),
        800: (55, 71, 79),
        900: (38, 50, 56),
        -100: (207, 216, 220),
        -200: (176, 190, 197),
        -400: (120, 144, 156),
        -700: (69, 90, 100),
    },
}
__material_colors['gray'] = __material_colors['grey']
__material_colors['blue_gray'] = __material_colors['blue_grey']


def __parse_max(max: float | Sequence[float] | None, type: ColorType) -> ColorTuple:
    if max is None:
        return __default_max[type]
    if isinstance(max, Sequence):
        l = len(max)
        if l == 1:  # gray
            return max[0], max[0], max[0], 1
        if l == 2:  # gray, alpha
            return max[0], max[0], max[0], max[1]
        if l == 3:  # r, g, b
            return max[0], max[1], max[2], 1
        return max[0], max[1], max[2], max[3]  # r, g, b, alpha
    return max, max, max, max  # same for all


def __parse_num(n: str, max: float) -> float:
    """Parse a number, either as a percentage or a float."""
    if n.endswith('%'):
        return float(n[:-1]) / 100
    return float(n) / max


def __parse_csslike(css: str, a: float = 1, max: float | Sequence[float] | None = None) -> skia.Color4f:
    # TODO: use skia's color parsing?
    css = css.strip().lower()
    css_nospace = __WHITESPACE_RE.sub('', css)
    if css_nospace in __css_colors:  # css color name
        r, g, b = __css_colors[css_nospace]
        return skia.Color4f(r / 255, g / 255, b / 255, a)

    matches = __MATERIAL_COLOR_RE.findall(css_nospace)
    if matches:  # material color name
        color_name = matches[0][0]
        shade = matches[0][9]
        r, g, b = __material_colors[color_name][-int(shade[1:]) if shade.startswith('a') else int(shade)]
        return skia.Color4f(r / 255, g / 255, b / 255, a)

    if css_nospace.startswith('#'):  # hex
        css_nospace = css_nospace[1:]
        l = len(css_nospace)
        if l == 1:  # #g
            g = int(css_nospace, 16) / 15
            return skia.Color4f(g, g, g, a)
        if l == 2:  # #ga
            g = int(css_nospace[0], 16) / 15
            a = int(css_nospace[1], 16) / 15
            return skia.Color4f(g, g, g, a)
        if l == 3:  # #rgb
            rrggbb = int(css_nospace, 16)
            return skia.Color4f((rrggbb >> 8) / 15, ((rrggbb >> 4) & 0xF) / 15, (rrggbb & 0xF) / 15, a)
        if l == 4:  # #rgba
            rgba = int(css_nospace, 16)
            return skia.Color4f(
                (rgba >> 12) / 15, ((rgba >> 8) & 0xF) / 15, ((rgba >> 4) & 0xF) / 15, (rgba & 0xF) / 15
            )
        if l == 6:  # #rrggbb
            rrggbb = int(css_nospace, 16)
            return skia.Color4f((rrggbb >> 16) / 255, ((rrggbb >> 8) & 0xFF) / 255, (rrggbb & 0xFF) / 255, a)
        if l == 8:  # #rrggbbaa
            rrggbbaa = int(css_nospace, 16)
            return skia.Color4f(
                (rrggbbaa >> 24) / 255,
                ((rrggbbaa >> 16) & 0xFF) / 255,
                ((rrggbbaa >> 8) & 0xFF) / 255,
                (rrggbbaa & 0xFF) / 255,
            )

    # function notation
    left_paren = css.find('(')
    right_paren = css.rfind(')')
    func = __WHITESPACE_RE.sub('', css[:left_paren])
    components = [m.group() for m in __NUMBER_RE.finditer(css[left_paren + 1 : right_paren])]
    if func in {'rgb', 'rgba'}:
        max = __parse_max(max, 'rgb')
        components = [__parse_num(c, max[i]) for i, c in enumerate(components)]
        if len(components) == 3:
            components.append(a / max[3])
        return skia.Color4f(*components)
    if func in {'hsb', 'hsba', 'hsv', 'hsva'}:
        max = __parse_max(max, 'hsb')
        components = [__parse_num(c, max[i]) for i, c in enumerate(components)]
        if len(components) == 3:
            components.append(a / max[3])
        return color(hsba=components, max=(1, 1, 1, 1))  # type: ignore hsba has 4 components
    if func in {'hsl', 'hsla'}:
        max = __parse_max(max, 'hsl')
        components = [__parse_num(c, max[i]) for i, c in enumerate(components)]
        if len(components) == 3:
            components.append(a / max[3])
        return color(hsla=components, max=(1, 1, 1, 1))  # type: ignore hsla has 4 components
    return TRANSPARENT


def color(
    r: ColorLike | None = None,
    g: float | None = None,
    b: float | None = None,
    a: float = 1,
    packed: int | None = None,
    argb: int | None = None,
    rgb: ColorTuple3 | None = None,
    rgba: ColorTuple | None = None,
    hsb: ColorTuple3 | None = None,
    hsba: ColorTuple | None = None,
    hsv: ColorTuple3 | None = None,
    hsva: ColorTuple | None = None,
    hsl: ColorTuple3 | None = None,
    hsla: ColorTuple | None = None,
    max: float | Sequence[float] | None = None,
) -> skia.Color4f:
    """
    Create a color from a variety of formats. If multiple formats are specified, they will be parsed in the order
    specified below and the first successful parse will be returned. If conflicting values are specified, the result is
    undefined. A :class:`skia.Color4f` containing the red, green, blue, and alpha values is returned.

    - ``color(skia.Color4f)``: Return the color as is.
    - ``color(r, g, b)`` or ``color(r, g, b, a)``: Create a color from red, green, blue, and optional alpha values.
    - ``color(g, a)``: Create a gray color with given alpha.
    - If a single argument is given, it will be parsed based on its type:
        - ``color(g: float)``: Create a gray color with given value.
        - ``color(packed: int)``: Create a color from a 32-bit packed integer in ARGB format. This is same as calling
          with the *packed* or *argb* keyword argument.
        - ``color(rgba: Sequence[float])``: Create a color from the given sequence. The values are returned as is
          without any scaling (see below). The sequence may have 1, 2, 3, or 4 components, which will be parsed the way
          *max* is parsed for a sequence (see below).
        - ``color(css: str, a: float)``: Create a color from a CSS-like case-insensitive string. An optional alpha value
          and *max* may be specified. The string may be one of the following:
            - ``'color'``: A color name from the CSS3 list of colors.
            - ``'material'``: A color name from the Material Design list of colors. For example, ``'red50'`` or
              ``'blueA700'``.
            - ``'#hex'``: A hexadecimal color. Several formats are supported:
                - 1 digit (G): Grayscale, where G is the gray value.
                - 2 digits (GA): Grayscale with alpha, where G is the gray value and A is the alpha value.
                - 3 digits (RGB): RGB, where R, G, and B are the red, green, and blue values.
                - 4 digits (RGBA): RGBA, where R, G, B, and A are the red, green, blue, and alpha values.
                - 6 digits (RRGGBB): RGB, where RR, GG, and BB are the red, green, and blue values.
                - 8 digits (RRGGBBAA): RGBA, where RR, GG, BB, and AA are the red, green, blue, and alpha values.
            - ``'rgba(r, g, b, a)'``: Functional notation with red, green, blue, and alpha values. Some things to note:
                - The function name can be 'rgb', 'rgba', 'hsb', 'hsba', 'hsv', 'hsva', 'hsl', or 'hsla'.
                - The 'a' (alpha) in the function names is optional. The presence of an alpha value is determined by the
                  number of arguments.
                - The arguments can be anything that can be parsed by :func:`float`. They may follow an optional
                  ``%`` sign, which will be interpreted as a percentage.
                - The arguments may be separated by anyting that does not parse as a number.
    - ``color(packed=0xAARRGGBB)`` or ``color(argb=0xAARRGGBB)``: Create a color from a 32-bit packed integer in ARGB
      format.
    - ``color(rgb=(r, g, b))``: Create a color from a tuple of red, green, and blue values.
    - ``color(rgba=(r, g, b, a))``: Create a color from a tuple of red, green, blue, and alpha values. Note that this is
      different from *argb*.
    - ``color(hsb=(h, s, b))``: Create a color from a tuple of hue, saturation, and brightness values.
    - ``color(hsba=(h, s, b, a))``: Create a color from a tuple of hue, saturation, brightness, and alpha values.
    - ``color(hsv=(h, s, v))``: Create a color from a tuple of hue, saturation, and value values.
    - ``color(hsva=(h, s, v, a))``: Create a color from a tuple of hue, saturation, value, and alpha values.
    - ``color(hsl=(h, s, l))``: Create a color from a tuple of hue, saturation, and lightness values.
    - ``color(hsla=(h, s, l, a))``: Create a color from a tuple of hue, saturation, lightness, and alpha values.
    - ``color()``: Each time this is called, a unique color is returned with constant saturation and lightness.

    The function also takes an optional *max* argument, which specifies the maximum value for each component. This can
    be used to scale the components to the range [0, 1]. The *max* argument should ideally be a sequence of 4 values,
    one for each component (R, G, B, A for RGB colors, or H, S, B, A for HSB colors, etc.). Several formats are
    supported:

    - ``max=None``: If *max* is not specified, it defaults to ``(255, 255, 255, 1)`` for RGB colors and ``(360, 100,
      100, 1)`` for HSB, HSV, and HSL colors.
    - ``max=[g]``: If a sequence with a single value is specified, it is used for the first 3 components and 1 is used
      for the alpha component. ``(g, g, g, 1)``.
    - ``max=[g, a]``: If a sequence with 2 values is specified, the first value is used for the first 3 components and
      the second value is used for the alpha component. ``(g, g, g, a)``.
    - ``max=[r, g, b]``: If a sequence with 3 values is specified, the values are used for the first 3 components and 1
      is used for the alpha component. ``(r, g, b, 1)``.
    - ``max=[r, g, b, a]``: If a sequence with 4 values is specified, the values are used for the first 4 components.
      ``(r, g, b, a)``.
    - ``max=n``: If a single value is specified, it is used for all components. ``(n, n, n, n)``.

    :note: It is not guaranteed that the components of the returned color will be in the range [0, 1] depending on the
        values of the input.
    """
    if isinstance(r, skia.Color4f):
        return r
    mr, mg, mb, ma = __parse_max(max, 'rgb')
    if b is not None:  # r, g, b
        return skia.Color4f(r / mr, g / mg, b / mb, a / ma)  # type: ignore assume all args are floats
    if g is not None:  # g, a
        r /= mr  # type: ignore assume all args are floats
        return skia.Color4f(r, r, r, g / ma)  # type: ignore assume all args are floats
    if r is not None:
        if isinstance(r, float):  # g
            r /= mr
            return skia.Color4f(r, r, r, a / ma)
        if isinstance(r, int):  # packed
            return color(packed=r)
        if isinstance(r, str):  # css
            return __parse_csslike(r, a, max)
        if isinstance(r, Sequence):  # rgba
            return skia.Color4f(__parse_max(r, 'rgb'))  # same format

    if not (packed is None and argb is None):
        if argb is None:
            argb = packed
        return skia.Color4f.FromColor(argb)  # type: ignore argb will not be None

    if not (rgb is None and rgba is None):
        if rgb is None:
            r, g, b, a = rgba  # type: ignore rgba will not be None
        else:
            r, g, b = rgb
        return skia.Color4f(r / mr, g / mg, b / mb, a / ma)

    if not (hsb is None and hsba is None and hsv is None and hsva is None):
        if hsb is not None:
            h, s, b = hsb
        elif hsba is not None:
            h, s, b, a = hsba
        elif hsv is not None:
            h, s, b = hsv
        else:
            h, s, b, a = hsva  # type: ignore hsva will not be None
        mh, ms, mb, ma = __parse_max(max, 'hsb')
        return skia.Color4f(*colorsys.hsv_to_rgb(h / mh, s / ms, b / mb), a / ma)

    if not (hsl is None and hsla is None):
        if hsl is None:
            h, s, l, a = hsla  # type: ignore hsla will not be None
        else:
            h, s, l = hsl
        mh, ms, ml, ma = __parse_max(max, 'hsl')
        return skia.Color4f(*colorsys.hls_to_rgb(h / mh, l / ml, s / ms), a / ma)

    return skia.uniqueColor()


def lerp_color(c1: skia.Color4f, c2: skia.Color4f, t: float) -> skia.Color4f:
    """Linearly interpolate between two colors by a given factor."""
    t1 = 1 - t
    return skia.Color4f(c1.fR * t1 + c2.fR * t, c1.fG * t1 + c2.fG * t, c1.fB * t1 + c2.fB * t, c1.fA * t1 + c2.fA * t)
