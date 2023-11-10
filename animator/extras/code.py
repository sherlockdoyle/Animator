from html.parser import HTMLParser
from typing import Any

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.formatters.html import _get_ttype_class  # type: ignore symbol is defined
from pygments.lexer import Lexer
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.style import Style

from animator import skia
from animator.entity import Entity
from animator.graphics import FontStyle

_HEIGHT_OVERRIDE = True
_HEIGHT = 1.25


def _parse_hex(c: str) -> skia.Color4f:
    return skia.Color4f(0xFF000000 | int(c, 16))


def _style_to_class(
    style: type[Style], default_style: skia.textlayout.TextStyle
) -> dict[str, skia.textlayout.TextStyle]:
    classes: dict[str, skia.textlayout.TextStyle] = {}
    for tk, st in style:
        if name := _get_ttype_class(tk):
            text_style = classes[name] = skia.textlayout.TextStyle(default_style)
            if st['color']:
                text_style.setColor(_parse_hex(st['color']))
            if st['bold']:
                text_style.setFontStyle(skia.FontStyle.BoldItalic() if st['italic'] else skia.FontStyle.Bold())
            elif st['italic']:
                text_style.setFontStyle(skia.FontStyle.Italic())
            if st['underline']:
                text_style.setDecoration(skia.textlayout.TextDecoration.kUnderline)
            if st['bgcolor']:
                text_style.setBackgroundPaint(skia.Paint(color=_parse_hex(st['bgcolor'])))
    return classes


class CodeParser(HTMLParser):
    def __init__(
        self,
        builder: skia.textlayout.ParagraphBuilder,
        style: type[Style],
        font_names: list[str],
        font_size: float,
        no_err: bool,
    ) -> None:
        super().__init__()
        self.builder: skia.textlayout.ParagraphBuilder = builder
        self.classes: dict[str, skia.textlayout.TextStyle] = _style_to_class(
            style,
            skia.textlayout.TextStyle(
                fontFamilies=font_names, fontSize=font_size, heightOverride=_HEIGHT_OVERRIDE, height=_HEIGHT
            ),
        )
        self.no_err: bool = no_err

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        class_ = attrs[0][1]
        if not (self.no_err and class_ == 'err') and class_ in self.classes:
            self.builder.pushStyle(skia.textlayout.TextStyle(self.classes[class_]))

    def handle_endtag(self, tag: str) -> None:
        self.builder.pop()

    def handle_data(self, data: str) -> None:
        self.builder.addText(data)


class Code(Entity):
    """A code entity."""

    def __init__(
        self,
        code: str,
        lexer: str | Lexer | None = None,
        style: str | type[Style] = 'bw',
        font_name: str = 'monospace',
        font_size: float | None = FontStyle.SIZE,
        width: float | None = None,
        no_err: bool = False,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        if lexer is None:
            lexer = guess_lexer(code, stripall=True)
        elif isinstance(lexer, str):
            lexer = get_lexer_by_name(lexer, stripall=True)
        formatter = HtmlFormatter(nowrap=True, style=style)
        self.bgcolor: skia.Color4f = _parse_hex(formatter.style.background_color[1:])

        font_names = font_name.split(',')
        font_names.append('monospace')
        text_style = skia.textlayout.TextStyle(fontFamilies=font_names, heightOverride=_HEIGHT_OVERRIDE, height=_HEIGHT)
        if font_size is None:
            font_size = text_style.getFontSize()
        else:
            text_style.setFontSize(font_size)
        builder = skia.textlayout.ParagraphBuilder(skia.textlayout.ParagraphStyle(textStyle=text_style), skia.FontMgr())
        parser = CodeParser(builder, formatter.style, font_names, font_size, no_err)
        parser.feed(highlight(code, lexer, formatter).strip('\n'))
        parser.close()

        self.__paragraph = builder.Build()
        self.__paragraph.layout(text_style.getFontMetrics().fAvgCharWidth * 100 if width is None else width)

    def on_draw(self, canvas: skia.Canvas) -> None:
        self.__paragraph.paint(canvas, self.offset.fX, self.offset.fY)

    def get_bounds(self, transformed: bool = False) -> skia.Rect:
        bounds = skia.Rect.MakeXYWH(
            self.offset.fX, self.offset.fY, self.__paragraph.getMaxIntrinsicWidth(), self.__paragraph.getHeight()
        )
        if transformed:
            return self.mat.mapRect(bounds, skia.ApplyPerspectiveClip.kNo)
        return bounds
