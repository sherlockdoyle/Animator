import math
import re
from dataclasses import dataclass, fields
from typing import Literal

from animator import skia
from animator._common_types import ColorLike
from animator.graphics.color import color as parse_color

_NON_LETTER_REGEX = re.compile(r'[^a-zA-Z]+')
_AVAILABLE_FONT_NAME_CACHE: dict[str, str] = {name.lower().replace(' ', ''): name for name in skia.FontMgr.RefDefault()}


class FontStyle:
    """Font style for text entities."""

    class Weight:
        """Font weight."""

        INVISIBLE = skia.FontStyle.Weight.kInvisible_Weight
        THIN = skia.FontStyle.Weight.kThin_Weight
        EXTRA_LIGHT = skia.FontStyle.Weight.kExtraLight_Weight
        LIGHT = skia.FontStyle.Weight.kLight_Weight
        NORMAL = skia.FontStyle.Weight.kNormal_Weight
        MEDIUM = skia.FontStyle.Weight.kMedium_Weight
        SEMI_BOLD = skia.FontStyle.Weight.kSemiBold_Weight
        BOLD = skia.FontStyle.Weight.kBold_Weight
        EXTRA_BOLD = skia.FontStyle.Weight.kExtraBold_Weight
        BLACK = skia.FontStyle.Weight.kBlack_Weight
        EXTRA_BLACK = skia.FontStyle.Weight.kExtraBlack_Weight

    class Width:
        """Font width."""

        ULTRA_CONDENSED = skia.FontStyle.Width.kUltraCondensed_Width
        EXTRA_CONDENSED = skia.FontStyle.Width.kExtraCondensed_Width
        CONDENSED = skia.FontStyle.Width.kCondensed_Width
        SEMI_CONDENSED = skia.FontStyle.Width.kSemiCondensed_Width
        NORMAL = skia.FontStyle.Width.kNormal_Width
        SEMI_EXPANDED = skia.FontStyle.Width.kSemiExpanded_Width
        EXPANDED = skia.FontStyle.Width.kExpanded_Width
        EXTRA_EXPANDED = skia.FontStyle.Width.kExtraExpanded_Width
        ULTRA_EXPANDED = skia.FontStyle.Width.kUltraExpanded_Width

    class Slant:
        """Font slant."""

        UPRIGHT = skia.FontStyle.Slant.kUpright_Slant
        ITALIC = skia.FontStyle.Slant.kItalic_Slant
        OBLIQUE = skia.FontStyle.Slant.kOblique_Slant

    FAMILY_NAME: str | None = None
    SIZE: float | None = None
    STYLE: skia.FontStyle = skia.FontStyle()
    COLOR: skia.Color4f | skia.Shader = skia.Color4f.kWhite

    @staticmethod
    def get_available_fonts() -> list[str]:
        """Get a list of the names of available fonts."""
        return list(skia.FontMgr.RefDefault())  # type: ignore __getitem__ is defined

    @staticmethod
    def _parse_font_style(style: str) -> skia.FontStyle:
        """Parse a font style string."""
        style = _NON_LETTER_REGEX.sub(' ', style).strip().lower()
        font_style = [FontStyle.STYLE.weight(), FontStyle.STYLE.width(), FontStyle.STYLE.slant()]
        for i in range(3):
            for attr, value in _FONT_STYLE_COMPONENTS[i].__dict__.items():
                if not attr.startswith('_'):
                    attr = attr.lower().replace('_', ' ')
                    if attr in style or attr.replace(' ', '') in style:
                        font_style[i] = value
        return skia.FontStyle(*font_style)

    @staticmethod
    def get_closest_font_name(name: str) -> str | None:
        """Get the closest available font name to the given name."""
        return _AVAILABLE_FONT_NAME_CACHE.get(name.lower().replace(' ', ''))

    @staticmethod
    def get_font(name: str | None = FAMILY_NAME, style: skia.FontStyle | str = STYLE) -> skia.Typeface:
        """Get the best matching font.

        :param name: The name of the font to use. If ``None``, the default font is used.
        :param style: The font style to use.
        """
        if isinstance(style, str):
            style = FontStyle._parse_font_style(style)
        return skia.FontMgr.RefDefault().matchFamilyStyle(name, style)

    def __init__(
        self,
        name: str | skia.Typeface | None = FAMILY_NAME,
        size: float | None = SIZE,
        style: skia.FontStyle | str = STYLE,
    ) -> None:
        """Create a new font style.

        :param name: The name of the font or a ``skia.Typeface`` object to use. If ``None``, the default font is used.
        :param size: The font size to use. If ``None``, the default font size is used.
        :param style: The font style to use.
        """
        if not isinstance(name, skia.Typeface):
            name = FontStyle.get_font(name, style)
        self.font: skia.Font = skia.Font(name) if size is None else skia.Font(name, size)

    @property
    def size(self) -> float:
        """The font size."""
        return self.font.getSize()

    @size.setter
    def size(self, size: float) -> None:
        self.font.setSize(size)

    @property
    def style(self) -> skia.FontStyle:
        """The font style."""
        return self.font.getTypefaceOrDefault().fontStyle()

    @property
    def family_name(self) -> str:
        """The font family name."""
        return self.font.getTypefaceOrDefault().getFamilyName()

    def set_fake_width(self, width: float = 1) -> None:
        """Set a fake width for the font in case the font does not support width.

        :param width: The fake width to set. ``1`` means no change. Smaller values make the font narrower, larger values
            make it wider.
        """
        self.font.setScaleX(width)

    def set_fake_slant(self, slant: float = 0) -> None:
        """Set a fake slant for the font in case the font does not support slant.

        :param slant: The fake slant to set in degrees. ``0`` means no change. Positive values make the font slanted to
            the right, negative values make it slanted to the left.
        """
        self.font.setSkewX(math.tan(math.radians(slant)))


_FONT_STYLE_COMPONENTS = [FontStyle.Weight, FontStyle.Width, FontStyle.Slant]


class _Undefined:
    def __repr__(self) -> str:
        return 'undefined'


_undefined = _Undefined()
_Color = int | skia.Color4f
_ColorLike = ColorLike | skia.Color4f
_DecorationLiteral = Literal['line-through', 'overline', 'underline']
_Decoration = _DecorationLiteral | list[_DecorationLiteral]
_DecorationMode = Literal['gaps', 'through']
_DecorationStyle = Literal['dashed', 'dotted', 'double', 'solid', 'wavy']
_TextBaseline = Literal['alphabetic', 'ideographic']


def _parse_decoration(decoration: _Decoration) -> skia.textlayout.TextDecoration:
    text_decoration = skia.textlayout.TextDecoration.kNoDecoration
    decoration_set = set(decoration) if isinstance(decoration, list) else {decoration}
    if 'line-through' in decoration_set:
        text_decoration |= skia.textlayout.TextDecoration.kLineThrough
    if 'overline' in decoration_set:
        text_decoration |= skia.textlayout.TextDecoration.kOverline
    if 'underline' in decoration_set:
        text_decoration |= skia.textlayout.TextDecoration.kUnderline
    return skia.textlayout.TextDecoration(text_decoration)


def _parse_decoration_mode(decoration_mode: _DecorationMode) -> skia.textlayout.TextDecorationMode:
    return (
        skia.textlayout.TextDecorationMode.kGaps
        if decoration_mode == 'gaps'
        else skia.textlayout.TextDecorationMode.kThrough
    )


def _parse_decoration_style(decoration_style: _DecorationStyle) -> skia.textlayout.TextDecorationStyle:
    return (
        skia.textlayout.TextDecorationStyle.kDashed
        if decoration_style == 'dashed'
        else skia.textlayout.TextDecorationStyle.kDotted
        if decoration_style == 'dotted'
        else skia.textlayout.TextDecorationStyle.kDouble
        if decoration_style == 'double'
        else skia.textlayout.TextDecorationStyle.kSolid
        if decoration_style == 'solid'
        else skia.textlayout.TextDecorationStyle.kWavy
    )


def _parse_text_baseline(text_baseline: _TextBaseline) -> skia.textlayout.TextBaseline:
    return (
        skia.textlayout.TextBaseline.kAlphabetic
        if text_baseline == 'alphabetic'
        else skia.textlayout.TextBaseline.kIdeographic
    )


@dataclass(init=False, kw_only=True, slots=True)
class TextStyle:
    @dataclass(init=False, kw_only=True, slots=True)
    class FontStyle:
        weight: skia.FontStyle.Weight | _Undefined = _undefined
        width: skia.FontStyle.Width | _Undefined = _undefined
        slant: skia.FontStyle.Slant | _Undefined = _undefined

        def __init__(
            self,
            weight: str | skia.FontStyle | skia.FontStyle.Weight | _Undefined = _undefined,
            width: skia.FontStyle.Width | _Undefined = _undefined,
            slant: skia.FontStyle.Slant | _Undefined = _undefined,
        ) -> None:
            if isinstance(weight, str):
                self.weight = _undefined
                self.width = _undefined
                self.slant = _undefined
                weight = _NON_LETTER_REGEX.sub(' ', weight).strip().lower()
                for i in range(3):
                    component = _FONT_STYLE_COMPONENTS[i]
                    for attr, value in component.__dict__.items():
                        if not attr.startswith('_'):
                            attr = attr.lower().replace('_', ' ')
                            if attr in weight or attr.replace(' ', '') in weight:
                                setattr(self, component.__name__.lower(), value)
            elif isinstance(weight, skia.FontStyle):
                self.weight = weight.weight()  # type: ignore
                self.width = weight.width()  # type: ignore
                self.slant = weight.slant()
            else:
                self.weight = weight
                self.width = width
                self.slant = slant

        def set_in_font_style(self, style: skia.FontStyle) -> skia.FontStyle:
            return skia.FontStyle(
                style.weight() if self.weight is _undefined else self.weight,  # type: ignore
                style.width() if self.width is _undefined else self.width,  # type: ignore
                style.slant() if self.slant is _undefined else self.slant,  # type: ignore
            )

    color: _Color | _Undefined = _undefined
    foregroundPaint: skia.Paint | None | _Undefined = _undefined
    backgroundPaint: skia.Paint | None | _Undefined = _undefined
    decoration: skia.textlayout.TextDecoration | _Undefined = _undefined
    decorationMode: skia.textlayout.TextDecorationMode | _Undefined = _undefined
    decorationStyle: skia.textlayout.TextDecorationStyle | _Undefined = _undefined
    decorationColor: _Color | _Undefined = _undefined
    decorationThicknessMultiplier: float | _Undefined = _undefined
    fontStyle: FontStyle | _Undefined = _undefined
    shadows: list[skia.textlayout.TextShadow] | None | _Undefined = _undefined
    fontArguments: skia.FontArguments | _Undefined = _undefined
    fontSize: float | _Undefined = _undefined
    fontFamilies: list[str] | _Undefined = _undefined
    baselineShift: float | _Undefined = _undefined
    height: float | _Undefined = _undefined
    heightOverride: bool | _Undefined = _undefined
    halfLeading: bool | _Undefined = _undefined
    letterSpacing: float | _Undefined = _undefined
    wordSpacing: float | _Undefined = _undefined
    typeface: skia.Typeface | _Undefined = _undefined
    locale: str | _Undefined = _undefined
    textBaseline: skia.textlayout.TextBaseline | _Undefined = _undefined
    placeholder: bool | _Undefined = _undefined

    def __init__(
        self,
        color: _ColorLike | _Undefined = _undefined,
        foregroundPaint: skia.Paint | None | _Undefined = _undefined,
        backgroundPaint: skia.Paint | None | _Undefined = _undefined,
        decoration: _Decoration | skia.textlayout.TextDecoration | _Undefined = _undefined,
        decorationMode: _DecorationMode | skia.textlayout.TextDecorationMode | _Undefined = _undefined,
        decorationStyle: _DecorationStyle | skia.textlayout.TextDecorationStyle | _Undefined = _undefined,
        decorationColor: _ColorLike | _Undefined = _undefined,
        decorationThicknessMultiplier: float | _Undefined = _undefined,
        fontStyle: str | skia.FontStyle | FontStyle | _Undefined = _undefined,
        shadows: list[skia.textlayout.TextShadow] | None | _Undefined = _undefined,
        fontArguments: skia.FontArguments | _Undefined = _undefined,
        fontSize: float | _Undefined = _undefined,
        fontFamilies: str | list[str] | _Undefined = _undefined,
        baselineShift: float | _Undefined = _undefined,
        height: float | _Undefined = _undefined,
        heightOverride: bool | _Undefined = _undefined,
        halfLeading: bool | _Undefined = _undefined,
        letterSpacing: float | _Undefined = _undefined,
        wordSpacing: float | _Undefined = _undefined,
        typeface: skia.Typeface | _Undefined = _undefined,
        locale: str | _Undefined = _undefined,
        textBaseline: _TextBaseline | skia.textlayout.TextBaseline | _Undefined = _undefined,
        placeholder: bool | _Undefined = _undefined,
    ) -> None:
        self.color = color if isinstance(color, (int, skia.Color4f, _Undefined)) else skia.Color4f(parse_color(color))
        self.foregroundPaint = foregroundPaint
        self.backgroundPaint = backgroundPaint
        self.decoration = (
            decoration
            if isinstance(decoration, (skia.textlayout.TextDecoration, _Undefined))
            else _parse_decoration(decoration)
        )
        self.decorationMode = (
            decorationMode
            if isinstance(decorationMode, (skia.textlayout.TextDecorationMode, _Undefined))
            else _parse_decoration_mode(decorationMode)
        )
        self.decorationStyle = (
            decorationStyle
            if isinstance(decorationStyle, (skia.textlayout.TextDecorationStyle, _Undefined))
            else _parse_decoration_style(decorationStyle)
        )
        self.decorationColor = (
            decorationColor
            if isinstance(decorationColor, (int, skia.Color4f, _Undefined))
            else skia.Color4f(parse_color(decorationColor))
        )
        self.decorationThicknessMultiplier = decorationThicknessMultiplier
        self.fontStyle = (
            fontStyle if isinstance(fontStyle, (TextStyle.FontStyle, _Undefined)) else TextStyle.FontStyle(fontStyle)
        )
        self.shadows = shadows
        self.fontArguments = fontArguments
        self.fontSize = fontSize
        self.fontFamilies = fontFamilies.split(',') if isinstance(fontFamilies, str) else fontFamilies
        self.baselineShift = baselineShift
        self.height = height
        self.heightOverride = heightOverride
        self.halfLeading = halfLeading
        self.letterSpacing = letterSpacing
        self.wordSpacing = wordSpacing
        self.typeface = typeface
        self.locale = locale
        self.textBaseline = (
            textBaseline
            if isinstance(textBaseline, (skia.textlayout.TextBaseline, _Undefined))
            else _parse_text_baseline(textBaseline)
        )
        self.placeholder = placeholder

    def get_text_style(self) -> skia.textlayout.TextStyle:
        """Get the style as a :class:`skia.textlayout.TextStyle` object."""
        return self.set_in_text_style(skia.textlayout.TextStyle())

    def set_in_text_style(self, style: skia.textlayout.TextStyle) -> skia.textlayout.TextStyle:
        """Set the style in the given :class:`skia.textlayout.TextStyle` object."""
        for field in fields(self):
            value = getattr(self, field.name)
            if value is not _undefined:
                if field.name == 'foregroundPaint' and value is None:
                    style.clearForegroundColor()
                elif field.name == 'backgroundPaint' and value is None:
                    style.clearBackgroundColor()
                elif field.name == 'fontStyle':
                    style.setFontStyle(value.set_in_font_style(style.getFontStyle()))
                elif field.name == 'shadows':
                    style.resetShadows()
                    if value is not None:
                        for shadow in value:
                            style.addShadow(shadow)
                elif field.name == 'placeholder':
                    if value:
                        style.setPlaceholder()
                else:
                    getattr(style, f'set{field.name[0].upper()}{field.name[1:]}')(value)
        return style
