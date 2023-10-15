from html.parser import HTMLParser
from typing import Any, TypedDict

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexer import Lexer
from pygments.lexers import get_lexer_by_name, guess_lexer

from animator import skia
from animator.entity import Entity
from animator.graphics import FontStyle

_TS = skia.textlayout.TextStyle
_C = skia.Color4f
_I = skia.FontStyle.Italic()
_B = skia.FontStyle.Bold()


class _Classes(TypedDict):
    err: _TS
    c: _TS
    k: _TS
    o: _TS
    ch: _TS
    cm: _TS
    cp: _TS
    cpf: _TS
    c1: _TS
    cs: _TS
    gd: _TS
    ge: _TS
    gr: _TS
    gh: _TS
    gi: _TS
    go: _TS
    gp: _TS
    gs: _TS
    gu: _TS
    gt: _TS
    kc: _TS
    kd: _TS
    kn: _TS
    kp: _TS
    kr: _TS
    kt: _TS
    m: _TS
    s: _TS
    na: _TS
    nb: _TS
    nc: _TS
    no: _TS
    nd: _TS
    ni: _TS
    ne: _TS
    nf: _TS
    nl: _TS
    nn: _TS
    nt: _TS
    nv: _TS
    ow: _TS
    w: _TS
    mb: _TS
    mf: _TS
    mh: _TS
    mi: _TS
    mo: _TS
    sa: _TS
    sb: _TS
    sc: _TS
    dl: _TS
    sd: _TS
    s2: _TS
    se: _TS
    sh: _TS
    si: _TS
    sx: _TS
    sr: _TS
    s1: _TS
    ss: _TS
    bp: _TS
    fm: _TS
    vc: _TS
    vg: _TS
    vi: _TS
    vm: _TS
    il: _TS


_HEIGHT_OVERRIDE = True
_HEIGHT = 1.25


class CodeParser(HTMLParser):
    def __init__(
        self,
        builder: skia.textlayout.ParagraphBuilder,
        classes: _Classes,
        font_names: list[str],
        font_size: float,
        no_err: bool,
    ) -> None:
        super().__init__()
        self.builder: skia.textlayout.ParagraphBuilder = builder
        self.classes: _Classes = classes
        self.font_names: list[str] = font_names
        self.font_size: float = font_size
        self.no_err: bool = no_err

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        class_ = attrs[0][1]
        if not (self.no_err and class_ == 'err') and class_ in self.classes:
            style = _TS(self.classes[class_])  # type: ignore class_ is in self.classes
            style.setFontFamilies(self.font_names)
            style.setFontSize(self.font_size)
            style.setHeightOverride(_HEIGHT_OVERRIDE)
            style.setHeight(_HEIGHT)
            self.builder.pushStyle(style)

    def handle_endtag(self, tag: str) -> None:
        self.builder.pop()

    def handle_data(self, data: str) -> None:
        self.builder.addText(data)


class Code(Entity):
    """A code entity."""

    CLASSES: _Classes = {
        'err': _TS(
            decoration=skia.textlayout.TextDecoration.kUnderline,
            decorationStyle=skia.textlayout.TextDecorationStyle.kWavy,
            decorationColor=_C(1, 0, 0, 1),
            decorationThicknessMultiplier=2,
        ),
        'c': _TS(color=_C(0.3615528144, 0.7057883958, 0.7057883958, 1), fontStyle=_I),
        'k': _TS(color=_C(-0.0, 0.7696582935, -0.0, 1), fontStyle=_B),
        'o': _TS(color=_C(0.683512039, 0.683512039, 0.683512039, 1)),
        'ch': _TS(color=_C(0.3615528144, 0.7057883958, 0.7057883958, 1), fontStyle=_I),
        'cm': _TS(color=_C(0.3615528144, 0.7057883958, 0.7057883958, 1), fontStyle=_I),
        'cp': _TS(color=_C(0.8966217719, 0.5887894093, -0.0, 1)),
        'cpf': _TS(color=_C(0.3615528144, 0.7057883958, 0.7057883958, 1), fontStyle=_I),
        'c1': _TS(color=_C(0.3615528144, 0.7057883958, 0.7057883958, 1), fontStyle=_I),
        'cs': _TS(color=_C(0.3615528144, 0.7057883958, 0.7057883958, 1), fontStyle=_I),
        'gd': _TS(color=_C(1.0, 0.6709375557, 0.6709375557, 1)),
        'ge': _TS(fontStyle=_I),
        'gr': _TS(color=_C(1.0, 0.5027355801, 0.5027355801, 1)),
        'gh': _TS(color=_C(0.8944277125, 0.8944277125, 1.0, 1), fontStyle=_B),
        'gi': _TS(color=_C(-0.0, 0.7583938151, -0.0, 1)),
        'go': _TS(color=_C(0.652252888, 0.652252888, 0.652252888, 1)),
        'gp': _TS(color=_C(0.8944277125, 0.8944277125, 1.0, 1), fontStyle=_B),
        'gs': _TS(fontStyle=_B),
        'gu': _TS(color=_C(1.0, 0.663578935, 1.0, 1), fontStyle=_B),
        'gt': _TS(color=_C(0.6772447007, 0.7103929725, 1.0, 1)),
        'kc': _TS(color=_C(-0.0, 0.7696582935, -0.0, 1), fontStyle=_B),
        'kd': _TS(color=_C(-0.0, 0.7696582935, -0.0, 1), fontStyle=_B),
        'kn': _TS(color=_C(-0.0, 0.7696582935, -0.0, 1), fontStyle=_B),
        'kp': _TS(color=_C(-0.0, 0.7696582935, -0.0, 1)),
        'kr': _TS(color=_C(-0.0, 0.7696582935, -0.0, 1), fontStyle=_B),
        'kt': _TS(color=_C(1.0, 0.6189562326, 0.6791946664, 1)),
        'm': _TS(color=_C(0.683512039, 0.683512039, 0.683512039, 1)),
        's': _TS(color=_C(0.9655142438, 0.6033823499, 0.6033823499, 1)),
        'na': _TS(color=_C(0.6026862442, 0.6918451505, 0.2126160295, 1)),
        'nb': _TS(color=_C(-0.0, 0.7696582935, -0.0, 1)),
        'nc': _TS(color=_C(0.7381741855, 0.7381741855, 1.0, 1), fontStyle=_B),
        'no': _TS(color=_C(1.0, 0.7284719892, 0.7284719892, 1)),
        'nd': _TS(color=_C(0.7689956723, 0.5505431256, 1.0, 1)),
        'ni': _TS(color=_C(0.652252888, 0.652252888, 0.652252888, 1), fontStyle=_B),
        'ne': _TS(color=_C(0.9286480767, 0.5456316436, 0.5349705356, 1), fontStyle=_B),
        'nf': _TS(color=_C(0.7381741855, 0.7381741855, 1.0, 1)),
        'nl': _TS(color=_C(0.6719609845, 0.6719609845, -0.0, 1)),
        'nn': _TS(color=_C(0.7381741855, 0.7381741855, 1.0, 1), fontStyle=_B),
        'nt': _TS(color=_C(-0.0, 0.7696582935, -0.0, 1), fontStyle=_B),
        'nv': _TS(color=_C(0.865418268, 0.8646751225, 0.9790105915, 1)),
        'ow': _TS(color=_C(0.7689956723, 0.5505431256, 1.0, 1), fontStyle=_B),
        'w': _TS(color=_C(0.7333333333, 0.7333333333, 0.7333333333, 1)),
        'mb': _TS(color=_C(0.683512039, 0.683512039, 0.683512039, 1)),
        'mf': _TS(color=_C(0.683512039, 0.683512039, 0.683512039, 1)),
        'mh': _TS(color=_C(0.683512039, 0.683512039, 0.683512039, 1)),
        'mi': _TS(color=_C(0.683512039, 0.683512039, 0.683512039, 1)),
        'mo': _TS(color=_C(0.683512039, 0.683512039, 0.683512039, 1)),
        'sa': _TS(color=_C(0.9655142438, 0.6033823499, 0.6033823499, 1)),
        'sb': _TS(color=_C(0.9655142438, 0.6033823499, 0.6033823499, 1)),
        'sc': _TS(color=_C(0.9655142438, 0.6033823499, 0.6033823499, 1)),
        'dl': _TS(color=_C(0.9655142438, 0.6033823499, 0.6033823499, 1)),
        'sd': _TS(color=_C(0.9655142438, 0.6033823499, 0.6033823499, 1), fontStyle=_I),
        's2': _TS(color=_C(0.9655142438, 0.6033823499, 0.6033823499, 1)),
        'se': _TS(color=_C(0.9711113372, 0.5417643845, 0.1960564486, 1), fontStyle=_B),
        'sh': _TS(color=_C(0.9655142438, 0.6033823499, 0.6033823499, 1)),
        'si': _TS(color=_C(0.8121463594, 0.591306641, 0.66902311, 1), fontStyle=_B),
        'sx': _TS(color=_C(-0.0, 0.7696582935, -0.0, 1)),
        'sr': _TS(color=_C(0.8121463594, 0.591306641, 0.66902311, 1)),
        's1': _TS(color=_C(0.9655142438, 0.6033823499, 0.6033823499, 1)),
        'ss': _TS(color=_C(0.865418268, 0.8646751225, 0.9790105915, 1)),
        'bp': _TS(color=_C(-0.0, 0.7696582935, -0.0, 1)),
        'fm': _TS(color=_C(0.7381741855, 0.7381741855, 1.0, 1)),
        'vc': _TS(color=_C(0.865418268, 0.8646751225, 0.9790105915, 1)),
        'vg': _TS(color=_C(0.865418268, 0.8646751225, 0.9790105915, 1)),
        'vi': _TS(color=_C(0.865418268, 0.8646751225, 0.9790105915, 1)),
        'vm': _TS(color=_C(0.865418268, 0.8646751225, 0.9790105915, 1)),
        'il': _TS(color=_C(0.683512039, 0.683512039, 0.683512039, 1)),
    }

    def __init__(
        self,
        code: str,
        lexer: str | Lexer | None = None,
        classes: _Classes = CLASSES,
        font_name: str = 'monospace',
        font_size: float | None = FontStyle.SIZE,
        width: float | None = None,
        no_err: bool = False,
        **kwargs: Any
    ):
        super().__init__(**kwargs)
        if lexer is None:
            lexer = guess_lexer(code, stripall=True)
        elif isinstance(lexer, str):
            lexer = get_lexer_by_name(lexer, stripall=True)
        code_html = highlight(code, lexer, HtmlFormatter(nowrap=True))

        font_names = font_name.split(',')
        font_names.append('monospace')
        text_style = skia.textlayout.TextStyle(fontFamilies=font_names, heightOverride=_HEIGHT_OVERRIDE, height=_HEIGHT)
        if font_size is None:
            font_size = text_style.getFontSize()
        else:
            text_style.setFontSize(font_size)
        builder = skia.textlayout.ParagraphBuilder(skia.textlayout.ParagraphStyle(textStyle=text_style), skia.FontMgr())
        parser = CodeParser(builder, classes, font_names, font_size, no_err)
        parser.feed(code_html)
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
