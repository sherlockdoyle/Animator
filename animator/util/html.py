from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from typing import TYPE_CHECKING, Any

from animator import skia
from animator.graphics import TextStyle, color

if TYPE_CHECKING:
    from animator.entity import Entity

_BASIC_TAG_STYLES: dict[str, TextStyle] = {
    'b': TextStyle(fontStyle=TextStyle.FontStyle(weight=skia.FontStyle.Bold().weight())),  # type: ignore
    'i': TextStyle(fontStyle=TextStyle.FontStyle(slant=skia.FontStyle.Italic().slant())),
    'u': TextStyle(decoration=skia.textlayout.TextDecoration.kUnderline),
    's': TextStyle(decoration=skia.textlayout.TextDecoration.kLineThrough),
    'o': TextStyle(decoration=skia.textlayout.TextDecoration.kOverline),
    'mark': TextStyle(color=skia.ColorBLACK, backgroundPaint=skia.Paint(color=skia.ColorYELLOW)),
    'code': TextStyle(fontFamilies=['monospace']),
}


@dataclass(kw_only=True, slots=True)
class PlaceholderStyle:
    alignment: skia.textlayout.PlaceholderAlignment | None = None
    baseline: skia.textlayout.TextBaseline | None = None
    margin: float | None = None


def _attrs_to_styles(attrs: list[tuple[str, str | None]]) -> tuple[dict[str, Any], list[str]]:
    styles: dict[str, Any] = {}
    classes: list[str] = []
    for attr, value in attrs:
        if value is None:
            if attr in {'heightOverride', 'halfLeading', 'placeholder'}:
                styles[attr] = True
                continue
            raise ValueError(f'Attribute {attr} has no value')
        if attr == 'class':
            classes = value.split()
        elif attr in {'foregroundPaint', 'backgroundPaint'}:
            styles[attr] = skia.Paint(color4f=skia.Color4f(color(value)))
        elif attr == 'decoration':
            styles[attr] = value.split()
        elif attr in {
            'decorationThicknessMultiplier',
            'fontSize',
            'baselineShift',
            'height',
            'letterSpacing',
            'wordSpacing',
        }:
            styles[attr] = float(value)
        elif attr == 'fontFamilies':
            styles[attr] = value.split(',')
        elif attr in {
            'color',
            'decorationMode',
            'decorationStyle',
            'decorationColor',
            'fontStyle',
            'locale',
            'textBaseline',
        }:
            styles[attr] = value
        else:
            raise ValueError(f'Unknown attribute: {attr}')
    return styles, classes


class ParagraphHTMLParser(HTMLParser):
    def __init__(
        self, builder: skia.textlayout.ParagraphBuilder, classes: dict[str, TextStyle], objs: dict[str, Entity]
    ):
        super().__init__()
        self.builder: skia.textlayout.ParagraphBuilder = builder
        self.classes: dict[str, TextStyle] = classes
        self.placeholders: dict[str, Entity] = objs
        self.ordered_placeholders_and_margins: list[tuple[Entity, float]] = []
        self.__tag_stack: list[str] = []
        self.__last_tag_was_br = False
        self.__visited_placeholders: set[str] = set()
        self.__last_placeholder_style: PlaceholderStyle = PlaceholderStyle()

    def __set_placeholder_style(self, attrs: list[tuple[str, str | None]]) -> None:
        for attr, value in attrs:
            if value is None:
                raise ValueError(f'Attribute {attr} has no value')
            if attr == 'alignment':
                self.__last_placeholder_style.alignment = (
                    skia.textlayout.PlaceholderAlignment.kAboveBaseline
                    if value == 'above-baseline'
                    else skia.textlayout.PlaceholderAlignment.kBaseline
                    if value == 'baseline'
                    else skia.textlayout.PlaceholderAlignment.kBelowBaseline
                    if value == 'below-baseline'
                    else skia.textlayout.PlaceholderAlignment.kBottom
                    if value == 'bottom'
                    else skia.textlayout.PlaceholderAlignment.kMiddle
                    if value == 'middle'
                    else skia.textlayout.PlaceholderAlignment.kTop
                    if value == 'top'
                    else None
                )
                if self.__last_placeholder_style.alignment is None:
                    raise ValueError(f'Unknown alignment: {value}')
            elif attr == 'baseline':
                self.__last_placeholder_style.baseline = (
                    skia.textlayout.TextBaseline.kAlphabetic
                    if value == 'alphabetic'
                    else skia.textlayout.TextBaseline.kIdeographic
                    if value == 'ideographic'
                    else None
                )
                if self.__last_placeholder_style.baseline is None:
                    raise ValueError(f'Unknown baseline: {value}')
            elif attr == 'margin':
                self.__last_placeholder_style.margin = float(value)
            else:
                raise ValueError(f'Unknown attribute: {attr}')

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.__tag_stack.append(tag)
        self.__last_tag_was_br = False
        if tag == 'obj':
            self.__set_placeholder_style(attrs)
            return

        styles, classes = _attrs_to_styles(attrs)
        current_style = self.builder.peekStyle()
        if tag in _BASIC_TAG_STYLES:
            new_style = _BASIC_TAG_STYLES[tag]
        elif tag == 'sup':
            new_style = TextStyle(baselineShift=-current_style.getFontSize() / 2)
        elif tag == 'sub':
            new_style = TextStyle(baselineShift=current_style.getFontSize() / 2)
        elif tag == 'small':
            new_style = TextStyle(fontSize=current_style.getFontSize() * 0.8)
        elif tag == 'big':
            new_style = TextStyle(fontSize=current_style.getFontSize() * 1.2)
        elif tag == 'span':
            new_style = None
        else:
            raise ValueError(f'Unknown tag: {tag}')

        new_text_style = current_style if new_style is None else new_style.set_in_text_style(current_style)
        for class_ in classes:
            if class_ in self.classes:
                new_text_style = self.classes[class_].set_in_text_style(new_text_style)
            else:
                raise ValueError(f'Unknown class: {class_}')
        self.builder.pushStyle(TextStyle(**styles).set_in_text_style(new_text_style))

    def handle_endtag(self, tag: str) -> None:
        current_tag = self.__tag_stack.pop()
        if current_tag != tag:
            raise ValueError(f'Unexpected closing tag: {tag}, expected {current_tag}')
        self.builder.pop()

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == 'br':
            self.builder.addText('\n')
            self.__last_tag_was_br = True
        else:
            raise ValueError(f'Unexpected self-closing tag: {tag}')

    def handle_data(self, data: str) -> None:
        if self.__tag_stack and self.__tag_stack[-1] == 'obj':
            data = data.strip()
            if data not in self.placeholders:
                raise ValueError(f'Unknown object: {data}')
            if data in self.__visited_placeholders:
                raise ValueError(f'Object {data} already visited')
            bounds = self.placeholders[data].get_bounds()
            if self.__last_placeholder_style.margin is not None:
                bounds.outset(self.__last_placeholder_style.margin, self.__last_placeholder_style.margin)
            placeholder = skia.textlayout.PlaceholderStyle(
                width=bounds.width(),
                height=bounds.height(),
                offset=self.builder.peekStyle().getFontSize() / 3 - bounds.fTop
                if self.__last_placeholder_style.alignment is None
                else -bounds.fTop,
            )
            if self.__last_placeholder_style.alignment is not None:
                placeholder.fAlignment = self.__last_placeholder_style.alignment
            if self.__last_placeholder_style.baseline is not None:
                placeholder.fBaseline = self.__last_placeholder_style.baseline
            self.builder.addPlaceholder(placeholder)
            self.ordered_placeholders_and_margins.append(
                (
                    self.placeholders[data],
                    0 if self.__last_placeholder_style.margin is None else self.__last_placeholder_style.margin,
                )
            )
            self.__visited_placeholders.add(data)
            return

        if self.__last_tag_was_br:
            data = data.lstrip()
        self.builder.addText(data.replace('\n', ' '))
