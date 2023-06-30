"""Entities for showing text."""
from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

from animator import skia
from animator.entity.entity import Entity
from animator.graphics import FontStyle, Style, TextStyle
from animator.util.html import ParagraphHTMLParser

if TYPE_CHECKING:
    from animator.scene import Scene

    _TextStyle = TextStyle | skia.textlayout.TextStyle


class TextEntity(Entity):
    """Base class for entities that show text."""

    def __init__(
        self,
        font_name: str | None = FontStyle.FAMILY_NAME,
        font_size: float | None = FontStyle.SIZE,
        font_style: skia.FontStyle | str = FontStyle.STYLE,
        **kwargs: Any,
    ) -> None:
        """
        :param font_name: The name of the font family to use. If ``None``, the default font family is used.
        :param font_size: The font size to use. If ``None``, the default font size is used.
        :param font_style: The font style to use.
        """
        super().__init__(**kwargs)
        self.font_style: FontStyle = FontStyle(font_name, font_size, font_style)
        if 'paint_style' not in kwargs:
            self.style.paint_style = Style.PaintStyle.FILL_ONLY
        if 'fill_color' not in kwargs:
            self.style.set_fill_color_or_shader(FontStyle.COLOR)


class SimpleText(TextEntity):
    """Simple text, shown simply!"""

    def __init__(self, text: str, **kwargs: Any):
        """
        :param text: The text to display.
        """
        super().__init__(**kwargs)
        self.text: str = text

    def do_stroke(self, canvas: skia.Canvas) -> None:
        canvas.drawString(self.text, self.offset.fX, self.offset.fY, self.font_style.font, self.style.stroke_paint)

    def do_fill(self, canvas: skia.Canvas) -> None:
        canvas.drawString(self.text, self.offset.fX, self.offset.fY, self.font_style.font, self.style.fill_paint)

    def get_bounds(self, transformed: bool = False) -> skia.Rect:
        _, bounds = self.font_style.font.measureText(self.text)
        bounds.offset(self.offset)
        if transformed:
            bounds = self.mat.mapRect(bounds, skia.ApplyPerspectiveClip.kNo)
        return bounds


class TextOnPath(TextEntity):
    """Text on a path."""

    def __init__(self, text: str, path: skia.Path, text_offset: float = 0, **kwargs: Any):
        """
        :param text: The text to display.
        :param path: The path on which to display the text.
        :param text_offset: The offset of the text along the path in pixels. ``0`` means the start of the path.
        """
        super().__init__(**kwargs)
        self.text: str = text
        self.__path: skia.Path = path
        self.text_offset: float = text_offset

        self.__blob: skia.TextBlob = None  # type: ignore lateinit

    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)
        if __name in {'text', 'text_offset'}:
            self._is_dirty = True

    def __build_blob(self) -> None:
        if self._is_dirty:
            self.__blob = skia.TextBlob.MakeOnPath(self.text, self.__path, self.font_style.font, self.text_offset)
            self._is_dirty = False

    def do_stroke(self, canvas: skia.Canvas) -> None:
        canvas.drawTextBlob(self.__blob, self.offset.fX, self.offset.fY, self.style.stroke_paint)

    def do_fill(self, canvas: skia.Canvas) -> None:
        canvas.drawTextBlob(self.__blob, self.offset.fX, self.offset.fY, self.style.fill_paint)

    def _transform_and_draw(self, canvas: skia.Canvas) -> None:
        self.__build_blob()
        super()._transform_and_draw(canvas)

    def get_bounds(self, transformed: bool = False) -> skia.Rect:
        self.__build_blob()
        bounds = self.__blob.bounds()
        bounds.offset(self.offset)
        if transformed:
            return self.mat.mapRect(bounds, skia.ApplyPerspectiveClip.kNo)
        return bounds


_TEXT_STYLE_KWARGS = {
    'color',
    'foregroundPaint',
    'backgroundPaint',
    'decoration',
    'decorationMode',
    'decorationStyle',
    'decorationColor',
    'decorationThicknessMultiplier',
    'shadows',
    'fontArguments',
    'baselineShift',
    'height',
    'heightOverride',
    'halfLeading',
    'letterSpacing',
    'wordSpacing',
    'typeface',
    'locale',
    'textBaseline',
    'placeholder',
}
_WHITE_SPACE_RE = re.compile(r'\s+')


def _text_style_kwargs(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Extracts the text style kwargs from the given kwargs."""
    text_style_kwargs = {}
    for key in list(kwargs.keys()):
        if key in _TEXT_STYLE_KWARGS:
            text_style_kwargs[key] = kwargs.pop(key)
    return text_style_kwargs


class Text(Entity):
    """The best kind of text with lots of formatting options!

    :note: For a :class:`Text` there is no concept of stroke, just fill. The ``fill_paint`` and ``stroke_paint`` of the
        :class:`Style` are not used. Instead, you can change the style of the text while adding text.
    """

    def __init__(
        self,
        text: str | None = None,
        font_name: str | None = FontStyle.FAMILY_NAME,
        font_size: float | None = FontStyle.SIZE,
        font_style: skia.FontStyle | str = FontStyle.STYLE,
        width: float | None = None,
        **kwargs: Any,
    ):
        """
        :param text: The text to display.
        :param font_name: The name of the font family to use. If ``None``, the default font family is used. This can be
            a comma-separated string of font names, in which case the first available font will be used.
        :param font_size: The font size to use. If ``None``, the default font size is used.
        :param font_style: The font style to use.
        :param width: The width of the text box. If ``None``, the width is automatically set to the width of the scene.
        :param kwargs: Additional keyword arguments passed to :class:`Entity` and the default :class:`TextStyle`.
        """
        super().__init__(**kwargs)

        text_style = skia.textlayout.TextStyle(
            fontStyle=FontStyle._parse_font_style(font_style) if isinstance(font_style, str) else font_style,
            **_text_style_kwargs(kwargs),
        )
        if font_name is not None:
            text_style.setFontFamilies(font_name.split(','))
        if font_size is not None:
            text_style.setFontSize(font_size)
        self.width: float = text_style.getFontMetrics().fAvgCharWidth * 80 if width is None else width
        self.__set_width_from_scene = width is None

        self.__builder = skia.textlayout.ParagraphBuilder(
            skia.textlayout.ParagraphStyle(textStyle=text_style), skia.FontMgr()
        )
        if text is not None:
            self.__builder.addText(text)
        self.__paragraph: skia.textlayout.Paragraph = None  # type: ignore lateinit
        self.__placeholders_and_margins: list[tuple[Entity, float]] = []

    @classmethod
    def from_htmlish(
        cls, html: str, classes: dict[str, TextStyle] = {}, objs: dict[str, Entity] = {}, **kwargs: Any
    ) -> Text:
        """Create a :class:`Text` from the given *html* string.

        :param html: The html string to parse.
        :param classes: A mapping of class names to :class:`TextStyle` instances.
        """
        text = cls(**kwargs)
        parser = ParagraphHTMLParser(text.__builder, classes, objs)
        parser.feed(re.sub(_WHITE_SPACE_RE, ' ', html.strip()))
        parser.close()
        text.__placeholders_and_margins.extend(parser.ordered_placeholders_and_margins)
        text.add(*(obj for obj, _ in parser.ordered_placeholders_and_margins))
        return text

    def set_scene(self, scene: Scene) -> None:
        super().set_scene(scene)
        if self.__set_width_from_scene:
            self.width = scene.width

    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)
        if __name == 'width':
            self._is_dirty = True

    def push_style(self, style: _TextStyle) -> None:
        """Push the given *style* onto the stack."""
        self.__builder.pushStyle(style.get_text_style() if isinstance(style, TextStyle) else style)

    def append_style(self, style: TextStyle) -> None:
        """Append the given *style* to the current style."""
        self.__builder.pushStyle(style.set_in_text_style(self.__builder.peekStyle()))

    def pop_style(self) -> None:
        """Pop the top style from the stack."""
        self.__builder.pop()

    def add_text(self, text: str, style: _TextStyle | None = None, **kwargs: Any) -> None:
        """
        Add *text* with the given *style*. If *style* is ``None``, but *kwargs* are given, a new :class:`TextStyle` is
        created with the given *kwargs* and used as the style. If *style* is ``None`` and *kwargs* are not given, the
        current style is used.
        """
        if style is None and kwargs:
            style = TextStyle(**kwargs)
        if style is not None:
            self.__builder.pushStyle(style.get_text_style() if isinstance(style, TextStyle) else style)
        self.__builder.addText(text)
        if style is not None:
            self.__builder.pop()
        self._is_dirty = True

    def append_text(self, text: str, style: TextStyle | None = None, **kwargs: Any) -> None:
        """
        Append *text* with the given *style* appended to the current style. If *style* is ``None``, a new
        :class:`TextStyle` is created with the given *kwargs* and used as the style.
        """
        if style is None:
            style = TextStyle(**kwargs)
        self.__builder.pushStyle(style.set_in_text_style(self.__builder.peekStyle()))
        self.__builder.addText(text)
        self.__builder.pop()
        self._is_dirty = True

    def __build_paragraph(self) -> None:
        if self._is_dirty:
            self.__paragraph = self.__builder.Build()
            self.__paragraph.layout(self.width)
            for i, box in enumerate(self.__paragraph.getRectsForPlaceholders()):
                obj, margin = self.__placeholders_and_margins[i]
                bounds = obj.get_bounds()
                bounds.outset(margin, margin)
                obj.pos.set(box.rect.fLeft - bounds.fLeft, box.rect.fTop - bounds.fTop)
            self._is_dirty = False

    def on_draw(self, canvas: skia.Canvas) -> None:
        self.__build_paragraph()
        self.__paragraph.paint(canvas, self.offset.fX, self.offset.fY)

    def get_bounds(self, transformed: bool = False) -> skia.Rect:
        """Get the (approximate) bounds of the text."""
        self.__build_paragraph()
        bounds = skia.Rect.MakeXYWH(
            self.offset.fX, self.offset.fY, self.__paragraph.getMaxIntrinsicWidth(), self.__paragraph.getHeight()
        )
        if transformed:
            return self.mat.mapRect(bounds, skia.ApplyPerspectiveClip.kNo)
        return bounds
