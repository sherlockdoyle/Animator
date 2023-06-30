"""This module provides an interface to the Skia text layout library."""
from __future__ import annotations

import typing
from enum import IntEnum

import animator.skia
import animator.skia.textlayout
from animator.skia import _Color, _Point

__all__ = [
    "Affinity",
    "Block",
    "Decoration",
    "FontArguments",
    "FontCollection",
    "FontFeature",
    "LineMetricStyle",
    "LineMetrics",
    "Paragraph",
    "ParagraphBuilder",
    "ParagraphStyle",
    "Placeholder",
    "PlaceholderAlignment",
    "PlaceholderStyle",
    "PositionWithAffinity",
    "Range",
    "RectHeightStyle",
    "RectWidthStyle",
    "StrutStyle",
    "StyleMetrics",
    "StyleType",
    "TextAlign",
    "TextBaseline",
    "TextBox",
    "TextDecoration",
    "TextDecorationMode",
    "TextDecorationStyle",
    "TextDirection",
    "TextHeightBehavior",
    "TextShadow",
    "TextStyle",
]

class Affinity:
    """
    Members:

      kUpstream

      kDownstream
    """

    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    __members__: dict  # value = {'kUpstream': <Affinity.kUpstream: 0>, 'kDownstream': <Affinity.kDownstream: 1>}
    kDownstream: animator.skia.textlayout.Affinity  # value = <Affinity.kDownstream: 1>
    kUpstream: animator.skia.textlayout.Affinity  # value = <Affinity.kUpstream: 0>
    pass

class Block:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, range: Range, style: TextStyle) -> None: ...
    @typing.overload
    def __init__(self, start: int, end: int, style: TextStyle) -> None: ...
    def __str__(self) -> str: ...
    def add(self, tail: Range) -> None: ...
    @property
    def fRange(self) -> Range:
        """
        :type: Range
        """
    @fRange.setter
    def fRange(self, arg0: Range) -> None:
        pass
    @property
    def fStyle(self) -> TextStyle:
        """
        :type: TextStyle
        """
    @fStyle.setter
    def fStyle(self, arg0: TextStyle) -> None:
        pass
    pass

class Decoration:
    def __eq__(self, arg0: Decoration) -> bool: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(
        self,
        type: TextDecoration = TextDecoration.kNoDecoration,
        mode: TextDecorationMode = TextDecorationMode.kGaps,
        color: _Color = animator.skia.ColorTRANSPARENT,
        style: TextDecorationStyle = TextDecorationStyle.kSolid,
        thicknessMultiplier: float = 0,
    ) -> None: ...
    def __str__(self) -> str: ...
    @property
    def fColor(self) -> int:
        """
        :type: int
        """
    @fColor.setter
    def fColor(self, arg0: int) -> None:
        pass
    @property
    def fMode(self) -> TextDecorationMode:
        """
        :type: TextDecorationMode
        """
    @fMode.setter
    def fMode(self, arg0: TextDecorationMode) -> None:
        pass
    @property
    def fStyle(self) -> TextDecorationStyle:
        """
        :type: TextDecorationStyle
        """
    @fStyle.setter
    def fStyle(self, arg0: TextDecorationStyle) -> None:
        pass
    @property
    def fThicknessMultiplier(self) -> float:
        """
        :type: float
        """
    @fThicknessMultiplier.setter
    def fThicknessMultiplier(self, arg0: float) -> None:
        pass
    @property
    def fType(self) -> TextDecoration:
        """
        :type: TextDecoration
        """
    @fType.setter
    def fType(self, arg0: TextDecoration) -> None:
        pass
    pass

class FontArguments:
    def CloneTypeface(self, typeface: animator.skia.Typeface) -> animator.skia.Typeface: ...
    def __eq__(self, arg0: FontArguments) -> bool: ...
    @typing.overload
    def __init__(self, arg0: FontArguments) -> None: ...
    @typing.overload
    def __init__(self, arg0: animator.skia.FontArguments) -> None: ...
    def __ne__(self, arg0: FontArguments) -> bool: ...
    pass

class FontCollection:
    def __init__(self) -> None: ...
    def __str__(self) -> str: ...
    def clearCaches(self) -> None: ...
    @typing.overload
    def defaultFallback(self) -> animator.skia.Typeface: ...
    @typing.overload
    def defaultFallback(
        self, unicode: int, fontStyle: animator.skia.FontStyle, locale: str
    ) -> animator.skia.Typeface: ...
    def disableFontFallback(self) -> None: ...
    def enableFontFallback(self) -> None: ...
    @typing.overload
    def findTypefaces(
        self, familyNames: list[str], fontStyle: animator.skia.FontStyle
    ) -> list[animator.skia.Typeface]: ...
    @typing.overload
    def findTypefaces(
        self,
        familyNames: list[str],
        fontStyle: animator.skia.FontStyle,
        fontArgs: FontArguments | None,
    ) -> list[animator.skia.Typeface]: ...
    def fontFallbackEnabled(self) -> bool: ...
    def getFallbackManager(self) -> animator.skia.FontMgr: ...
    def getFontManagersCount(self) -> int: ...
    def setAssetFontManager(self, fontManager: animator.skia.FontMgr) -> None: ...
    @typing.overload
    def setDefaultFontManager(self, fontManager: animator.skia.FontMgr) -> None: ...
    @typing.overload
    def setDefaultFontManager(self, fontManager: animator.skia.FontMgr, defaultFamilyName: str) -> None: ...
    @typing.overload
    def setDefaultFontManager(self, fontManager: animator.skia.FontMgr, defaultFamilyNames: list[str]) -> None: ...
    def setDynamicFontManager(self, fontManager: animator.skia.FontMgr) -> None: ...
    def setTestFontManager(self, fontManager: animator.skia.FontMgr) -> None: ...
    pass

class FontFeature:
    def __eq__(self, arg0: FontFeature) -> bool: ...
    def __init__(self, name: str, value: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def fName(self) -> str:
        """
        :type: str
        """
    @fName.setter
    def fName(self, arg1: str) -> None:
        pass
    @property
    def fValue(self) -> int:
        """
        :type: int
        """
    @fValue.setter
    def fValue(self, arg0: int) -> None:
        pass
    pass

class LineMetricStyle:
    """
    Members:

      Typographic

      CSS
    """

    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    CSS: animator.skia.textlayout.LineMetricStyle  # value = <LineMetricStyle.CSS: 1>
    Typographic: animator.skia.textlayout.LineMetricStyle  # value = <LineMetricStyle.Typographic: 0>
    __members__: dict  # value = {'Typographic': <LineMetricStyle.Typographic: 0>, 'CSS': <LineMetricStyle.CSS: 1>}
    pass

class LineMetrics:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(
        self,
        start: int = 0,
        end: int = 0,
        end_excluding_whitespaces: int = 0,
        end_including_newline: int = 0,
        hard_break: bool = False,
    ) -> None: ...
    def __str__(self) -> str: ...
    @property
    def fAscent(self) -> float:
        """
        :type: float
        """
    @fAscent.setter
    def fAscent(self, arg0: float) -> None:
        pass
    @property
    def fBaseline(self) -> float:
        """
        :type: float
        """
    @fBaseline.setter
    def fBaseline(self, arg0: float) -> None:
        pass
    @property
    def fDescent(self) -> float:
        """
        :type: float
        """
    @fDescent.setter
    def fDescent(self, arg0: float) -> None:
        pass
    @property
    def fEndExcludingWhitespaces(self) -> int:
        """
        :type: int
        """
    @fEndExcludingWhitespaces.setter
    def fEndExcludingWhitespaces(self, arg0: int) -> None:
        pass
    @property
    def fEndIncludingNewline(self) -> int:
        """
        :type: int
        """
    @fEndIncludingNewline.setter
    def fEndIncludingNewline(self, arg0: int) -> None:
        pass
    @property
    def fEndIndex(self) -> int:
        """
        :type: int
        """
    @fEndIndex.setter
    def fEndIndex(self, arg0: int) -> None:
        pass
    @property
    def fHardBreak(self) -> bool:
        """
        :type: bool
        """
    @fHardBreak.setter
    def fHardBreak(self, arg0: bool) -> None:
        pass
    @property
    def fHeight(self) -> float:
        """
        :type: float
        """
    @fHeight.setter
    def fHeight(self, arg0: float) -> None:
        pass
    @property
    def fLeft(self) -> float:
        """
        :type: float
        """
    @fLeft.setter
    def fLeft(self, arg0: float) -> None:
        pass
    @property
    def fLineMetrics(self) -> typing.Dict[int, StyleMetrics]:
        """
        :type: typing.Dict[int, StyleMetrics]
        """
    @fLineMetrics.setter
    def fLineMetrics(self, arg0: typing.Dict[int, StyleMetrics]) -> None:
        pass
    @property
    def fLineNumber(self) -> int:
        """
        :type: int
        """
    @fLineNumber.setter
    def fLineNumber(self, arg0: int) -> None:
        pass
    @property
    def fStartIndex(self) -> int:
        """
        :type: int
        """
    @fStartIndex.setter
    def fStartIndex(self, arg0: int) -> None:
        pass
    @property
    def fUnscaledAscent(self) -> float:
        """
        :type: float
        """
    @fUnscaledAscent.setter
    def fUnscaledAscent(self, arg0: float) -> None:
        pass
    @property
    def fWidth(self) -> float:
        """
        :type: float
        """
    @fWidth.setter
    def fWidth(self, arg0: float) -> None:
        pass
    pass

class Paragraph:
    class FontInfo:
        @typing.overload
        def __init__(self, font: animator.skia.Font, textRange: Range) -> None: ...
        @typing.overload
        def __init__(self, other: Paragraph.FontInfo) -> None: ...
        def __str__(self) -> str: ...
        @property
        def fFont(self) -> animator.skia.Font:
            """
            :type: animator.skia.Font
            """
        @fFont.setter
        def fFont(self, arg0: animator.skia.Font) -> None:
            pass
        @property
        def fTextRange(self) -> Range:
            """
            :type: Range
            """
        @fTextRange.setter
        def fTextRange(self, arg0: Range) -> None:
            pass
        pass

    class GlyphClusterInfo:
        def __str__(self) -> str: ...
        @property
        def fBounds(self) -> animator.skia.Rect:
            """
            :type: animator.skia.Rect
            """
        @property
        def fClusterTextRange(self) -> Range:
            """
            :type: Range
            """
        @property
        def fGlyphClusterPosition(self) -> TextDirection:
            """
            :type: TextDirection
            """

    class VisitorFlags(IntEnum):
        """
        Members:

          kWhiteSpace_VisitorFlag
        """

        def __and__(self, other: object) -> object: ...
        def __eq__(self, other: object) -> bool: ...
        def __ge__(self, other: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __gt__(self, other: object) -> bool: ...
        def __hash__(self) -> int: ...
        def __index__(self) -> int: ...
        def __init__(self, value: int) -> None: ...
        def __int__(self) -> int: ...
        def __invert__(self) -> object: ...
        def __le__(self, other: object) -> bool: ...
        def __lt__(self, other: object) -> bool: ...
        def __ne__(self, other: object) -> bool: ...
        def __or__(self, other: object) -> object: ...
        def __rand__(self, other: object) -> object: ...
        def __repr__(self) -> str: ...
        def __ror__(self, other: object) -> object: ...
        def __rxor__(self, other: object) -> object: ...
        def __setstate__(self, state: int) -> None: ...
        def __xor__(self, other: object) -> object: ...
        @property
        def name(self) -> str:
            """
            :type: str
            """
        @property
        def value(self) -> int:
            """
            :type: int
            """
        __members__: dict  # value = {'kWhiteSpace_VisitorFlag': <VisitorFlags.kWhiteSpace_VisitorFlag: 1>}
        kWhiteSpace_VisitorFlag: animator.skia.textlayout.Paragraph.VisitorFlags  # value = <VisitorFlags.kWhiteSpace_VisitorFlag: 1>
        pass

    class VisitorInfo:
        def __str__(self) -> str: ...
        @property
        def advanceX(self) -> float:
            """
            :type: float
            """
        @property
        def count(self) -> int:
            """
            :type: int
            """
        @property
        def flags(self) -> Paragraph.VisitorFlags:
            """
            :type: Paragraph.VisitorFlags
            """
        @property
        def font(self) -> animator.skia.Font:
            """
            TODO: How to bind reference fields? There's probably some memory leak here.

            :type: animator.skia.Font
            """
        @property
        def glyphs(self) -> list[int]:
            """
            :type: list[int]
            """
        @property
        def origin(self) -> animator.skia.Point:
            """
            :type: animator.skia.Point
            """
        @property
        def positions(self) -> list[animator.skia.Point]:
            """
            :type: list[animator.skia.Point]
            """
        @property
        def utf8Starts(self) -> list[int]:
            """
            :type: list[int]
            """
    def __init__(self, style: ParagraphStyle, fonts: FontCollection) -> None: ...
    def __str__(self) -> str: ...
    def didExceedMaxLines(self) -> bool: ...
    def getActualTextRange(self, lineNumber: int, includeSpaces: bool) -> Range: ...
    def getAlphabeticBaseline(self) -> float: ...
    def getClosestGlyphClusterAt(self, dx: float, dy: float) -> Paragraph.GlyphClusterInfo | None: ...
    def getFontAt(self, codeUnitIndex: int) -> animator.skia.Font: ...
    def getFonts(self) -> list[Paragraph.FontInfo]: ...
    def getGlyphClusterAt(self, codeUnitIndex: int) -> Paragraph.GlyphClusterInfo | None: ...
    def getGlyphPositionAtCoordinate(self, dx: float, dy: float) -> PositionWithAffinity: ...
    def getHeight(self) -> float: ...
    def getIdeographicBaseline(self) -> float: ...
    def getLineMetrics(self) -> list[LineMetrics]: ...
    def getLineMetricsAt(self, lineNumber: int) -> LineMetrics | None:
        """
        Returns line metrics info for the line, or `None` if the line is not found.
        """
    def getLineNumberAt(self, codeUnitIndex: int) -> int: ...
    def getLongestLine(self) -> float: ...
    def getMaxIntrinsicWidth(self) -> float: ...
    def getMaxWidth(self) -> float: ...
    def getMinIntrinsicWidth(self) -> float: ...
    def getRectsForPlaceholders(self) -> list[TextBox]: ...
    def getRectsForRange(
        self, start: int, end: int, rectHeightStyle: RectHeightStyle, rectWidthStyle: RectWidthStyle
    ) -> list[TextBox]: ...
    def getWordBoundary(self, offset: int) -> Range: ...
    def layout(self, width: float) -> None: ...
    def lineNumber(self) -> int: ...
    def markDirty(self) -> None: ...
    def paint(self, canvas: animator.skia.Canvas, x: float, y: float) -> None: ...
    def unresolvedGlyphs(self) -> int: ...
    def updateBackgroundPaint(self, from_: int, to: int, paint: animator.skia.Paint) -> None: ...
    def updateFontSize(self, from_: int, to: int, fontSize: float) -> None: ...
    def updateForegroundPaint(self, from_: int, to: int, paint: animator.skia.Paint) -> None: ...
    def updateTextAlign(self, textAlign: TextAlign) -> None: ...
    def visit(self) -> list: ...
    pass

class ParagraphBuilder:
    def Build(self) -> Paragraph: ...
    def Reset(self) -> None: ...
    @typing.overload
    def __init__(self, style: ParagraphStyle, fontCollection: FontCollection) -> None: ...
    @typing.overload
    def __init__(self, style: ParagraphStyle, fontMgr: animator.skia.FontMgr) -> None: ...
    def __str__(self) -> str: ...
    def addPlaceholder(self, placeholderStyle: PlaceholderStyle) -> None: ...
    def addText(self, text: str) -> None: ...
    def getParagraphStyle(self) -> ParagraphStyle: ...
    def getText(self) -> str: ...
    @staticmethod
    def make(style: ParagraphStyle, fontCollection: FontCollection) -> ParagraphBuilder: ...
    def peekStyle(self) -> TextStyle: ...
    def pop(self) -> None: ...
    def pushStyle(self, style: TextStyle) -> None: ...
    pass

class ParagraphStyle:
    def __eq__(self, arg0: ParagraphStyle) -> bool: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(
        self,
        strutStyle: StrutStyle | None = None,
        textStyle: TextStyle | None = None,
        textDirection: TextDirection | None = None,
        textAlign: TextAlign | None = None,
        maxLines: int | None = None,
        ellipsis: str | None = None,
        height: float | None = None,
        textHeightBehavior: TextHeightBehavior | None = None,
        replaceTabCharacters: bool | None = None,
    ) -> None:
        """
        Construct a new paragraph style from keyword arguments. This creates a new :py:class:`ParagraphStyle`
        object and calls the respective setters for each keyword argument.
        """
    def __str__(self) -> str: ...
    def effective_align(self) -> TextAlign: ...
    def ellipsized(self) -> bool: ...
    def getEllipsis(self) -> str: ...
    def getEllipsisUtf16(self) -> str: ...
    def getHeight(self) -> float: ...
    def getMaxLines(self) -> int: ...
    def getReplaceTabCharacters(self) -> bool: ...
    def getStrutStyle(self) -> StrutStyle: ...
    def getTextAlign(self) -> TextAlign: ...
    def getTextDirection(self) -> TextDirection: ...
    def getTextHeightBehavior(self) -> TextHeightBehavior: ...
    def getTextStyle(self) -> TextStyle: ...
    def hintingIsOn(self) -> bool: ...
    def setEllipsis(self, ellipsis: str) -> None: ...
    def setHeight(self, height: float) -> None: ...
    def setMaxLines(self, maxLines: int) -> None: ...
    def setReplaceTabCharacters(self, value: bool) -> None: ...
    def setStrutStyle(self, strutStyle: StrutStyle) -> None: ...
    def setTextAlign(self, align: TextAlign) -> None: ...
    def setTextDirection(self, direction: TextDirection) -> None: ...
    def setTextHeightBehavior(self, v: TextHeightBehavior) -> None: ...
    def setTextStyle(self, textStyle: TextStyle) -> None: ...
    def turnHintingOff(self) -> None: ...
    def unlimited_lines(self) -> bool: ...
    pass

class Placeholder:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(
        self,
        start: int,
        end: int,
        style: PlaceholderStyle,
        textStyle: TextStyle,
        blocksBefore: Range,
        textBefore: Range,
    ) -> None: ...
    def __str__(self) -> str: ...
    @property
    def fBlocksBefore(self) -> Range:
        """
        :type: Range
        """
    @fBlocksBefore.setter
    def fBlocksBefore(self, arg0: Range) -> None:
        pass
    @property
    def fRange(self) -> Range:
        """
        :type: Range
        """
    @fRange.setter
    def fRange(self, arg0: Range) -> None:
        pass
    @property
    def fStyle(self) -> PlaceholderStyle:
        """
        :type: PlaceholderStyle
        """
    @fStyle.setter
    def fStyle(self, arg0: PlaceholderStyle) -> None:
        pass
    @property
    def fTextBefore(self) -> Range:
        """
        :type: Range
        """
    @fTextBefore.setter
    def fTextBefore(self, arg0: Range) -> None:
        pass
    @property
    def fTextStyle(self) -> TextStyle:
        """
        :type: TextStyle
        """
    @fTextStyle.setter
    def fTextStyle(self, arg0: TextStyle) -> None:
        pass
    pass

class PlaceholderAlignment:
    """
    Members:

      kBaseline

      kAboveBaseline

      kBelowBaseline

      kTop

      kBottom

      kMiddle
    """

    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    __members__: dict  # value = {'kBaseline': <PlaceholderAlignment.kBaseline: 0>, 'kAboveBaseline': <PlaceholderAlignment.kAboveBaseline: 1>, 'kBelowBaseline': <PlaceholderAlignment.kBelowBaseline: 2>, 'kTop': <PlaceholderAlignment.kTop: 3>, 'kBottom': <PlaceholderAlignment.kBottom: 4>, 'kMiddle': <PlaceholderAlignment.kMiddle: 5>}
    kAboveBaseline: animator.skia.textlayout.PlaceholderAlignment  # value = <PlaceholderAlignment.kAboveBaseline: 1>
    kBaseline: animator.skia.textlayout.PlaceholderAlignment  # value = <PlaceholderAlignment.kBaseline: 0>
    kBelowBaseline: animator.skia.textlayout.PlaceholderAlignment  # value = <PlaceholderAlignment.kBelowBaseline: 2>
    kBottom: animator.skia.textlayout.PlaceholderAlignment  # value = <PlaceholderAlignment.kBottom: 4>
    kMiddle: animator.skia.textlayout.PlaceholderAlignment  # value = <PlaceholderAlignment.kMiddle: 5>
    kTop: animator.skia.textlayout.PlaceholderAlignment  # value = <PlaceholderAlignment.kTop: 3>
    pass

class PlaceholderStyle:
    def __eq__(self, arg0: PlaceholderStyle) -> bool: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(
        self,
        width: float = 0,
        height: float = 0,
        alignment: PlaceholderAlignment = PlaceholderAlignment.kBaseline,
        baseline: TextBaseline = TextBaseline.kAlphabetic,
        offset: float = 0,
    ) -> None: ...
    def __str__(self) -> str: ...
    def equals(self, other: PlaceholderStyle) -> bool: ...
    @property
    def fAlignment(self) -> PlaceholderAlignment:
        """
        :type: PlaceholderAlignment
        """
    @fAlignment.setter
    def fAlignment(self, arg0: PlaceholderAlignment) -> None:
        pass
    @property
    def fBaseline(self) -> TextBaseline:
        """
        :type: TextBaseline
        """
    @fBaseline.setter
    def fBaseline(self, arg0: TextBaseline) -> None:
        pass
    @property
    def fBaselineOffset(self) -> float:
        """
        :type: float
        """
    @fBaselineOffset.setter
    def fBaselineOffset(self, arg0: float) -> None:
        pass
    @property
    def fHeight(self) -> float:
        """
        :type: float
        """
    @fHeight.setter
    def fHeight(self, arg0: float) -> None:
        pass
    @property
    def fWidth(self) -> float:
        """
        :type: float
        """
    @fWidth.setter
    def fWidth(self, arg0: float) -> None:
        pass
    pass

class PositionWithAffinity:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, position: int = 0, affinity: Affinity = Affinity.kDownstream) -> None: ...
    def __str__(self) -> str: ...
    @property
    def affinity(self) -> Affinity:
        """
        :type: Affinity
        """
    @affinity.setter
    def affinity(self, arg0: Affinity) -> None:
        pass
    @property
    def position(self) -> int:
        """
        :type: int
        """
    @position.setter
    def position(self, arg0: int) -> None:
        pass
    pass

class Range:
    def Shift(self, arg0: int) -> None: ...
    def __and__(self, arg0: Range) -> Range: ...
    def __contains__(self, arg0: Range) -> bool: ...
    def __eq__(self, arg0: Range) -> bool: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: tuple) -> None: ...
    @typing.overload
    def __init__(self, start: int, end: int) -> None: ...
    def __str__(self) -> str: ...
    def contains(self, other: Range) -> bool: ...
    def empty(self) -> bool: ...
    def intersection(self, other: Range) -> Range: ...
    def intersects(self, other: Range) -> bool: ...
    def width(self) -> int: ...
    @property
    def end(self) -> int:
        """
        :type: int
        """
    @end.setter
    def end(self, arg0: int) -> None:
        pass
    @property
    def start(self) -> int:
        """
        :type: int
        """
    @start.setter
    def start(self, arg0: int) -> None:
        pass
    pass

class RectHeightStyle:
    """
    Members:

      kTight

      kMax

      kIncludeLineSpacingMiddle

      kIncludeLineSpacingTop

      kIncludeLineSpacingBottom

      kStrut
    """

    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    __members__: dict  # value = {'kTight': <RectHeightStyle.kTight: 0>, 'kMax': <RectHeightStyle.kMax: 1>, 'kIncludeLineSpacingMiddle': <RectHeightStyle.kIncludeLineSpacingMiddle: 2>, 'kIncludeLineSpacingTop': <RectHeightStyle.kIncludeLineSpacingTop: 3>, 'kIncludeLineSpacingBottom': <RectHeightStyle.kIncludeLineSpacingBottom: 4>, 'kStrut': <RectHeightStyle.kStrut: 5>}
    kIncludeLineSpacingBottom: animator.skia.textlayout.RectHeightStyle  # value = <RectHeightStyle.kIncludeLineSpacingBottom: 4>
    kIncludeLineSpacingMiddle: animator.skia.textlayout.RectHeightStyle  # value = <RectHeightStyle.kIncludeLineSpacingMiddle: 2>
    kIncludeLineSpacingTop: animator.skia.textlayout.RectHeightStyle  # value = <RectHeightStyle.kIncludeLineSpacingTop: 3>
    kMax: animator.skia.textlayout.RectHeightStyle  # value = <RectHeightStyle.kMax: 1>
    kStrut: animator.skia.textlayout.RectHeightStyle  # value = <RectHeightStyle.kStrut: 5>
    kTight: animator.skia.textlayout.RectHeightStyle  # value = <RectHeightStyle.kTight: 0>
    pass

class RectWidthStyle:
    """
    Members:

      kTight

      kMax
    """

    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    __members__: dict  # value = {'kTight': <RectWidthStyle.kTight: 0>, 'kMax': <RectWidthStyle.kMax: 1>}
    kMax: animator.skia.textlayout.RectWidthStyle  # value = <RectWidthStyle.kMax: 1>
    kTight: animator.skia.textlayout.RectWidthStyle  # value = <RectWidthStyle.kTight: 0>
    pass

class StrutStyle:
    def __eq__(self, arg0: StrutStyle) -> bool: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(
        self,
        fontFamilies: list[str] | None = None,
        fontStyle: animator.skia.FontStyle | None = None,
        fontSize: float | None = None,
        height: float | None = None,
        leading: float | None = None,
        strutEnabled: bool | None = None,
        forceStrutHeight: bool | None = None,
        heightOverride: bool | None = None,
        halfLeading: bool | None = None,
    ) -> None:
        """
        Construct a new strut style from keyword arguments. This creates a new :py:class:`StrutStyle` object
        and calls the respective setters for each keyword argument.
        """
    def __str__(self) -> str: ...
    def getFontFamilies(self) -> list: ...
    def getFontSize(self) -> float: ...
    def getFontStyle(self) -> animator.skia.FontStyle: ...
    def getForceStrutHeight(self) -> bool: ...
    def getHalfLeading(self) -> bool: ...
    def getHeight(self) -> float: ...
    def getHeightOverride(self) -> bool: ...
    def getLeading(self) -> float: ...
    def getStrutEnabled(self) -> bool: ...
    def setFontFamilies(self, families: list[str]) -> None: ...
    def setFontSize(self, size: float) -> None: ...
    def setFontStyle(self, fontStyle: animator.skia.FontStyle) -> None: ...
    def setForceStrutHeight(self, v: bool) -> None: ...
    def setHalfLeading(self, halfLeading: bool) -> None: ...
    def setHeight(self, height: float) -> None: ...
    def setHeightOverride(self, v: bool) -> None: ...
    def setLeading(self, Leading: float) -> None: ...
    def setStrutEnabled(self, v: bool) -> None: ...
    pass

class StyleMetrics:
    @typing.overload
    def __init__(self, style: TextStyle) -> None: ...
    @typing.overload
    def __init__(self, style: TextStyle, fontMetrics: animator.skia.FontMetrics) -> None: ...
    def __str__(self) -> str: ...
    @property
    def font_metrics(self) -> animator.skia.FontMetrics:
        """
        :type: animator.skia.FontMetrics
        """
    @font_metrics.setter
    def font_metrics(self, arg0: animator.skia.FontMetrics) -> None:
        pass
    @property
    def text_style(self) -> TextStyle:
        """
        :type: TextStyle
        """

class StyleType:
    """
    Members:

      kNone

      kAllAttributes

      kFont

      kForeground

      kBackground

      kShadow

      kDecorations

      kLetterSpacing

      kWordSpacing
    """

    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    __members__: dict  # value = {'kNone': <StyleType.kNone: 0>, 'kAllAttributes': <StyleType.kAllAttributes: 1>, 'kFont': <StyleType.kFont: 2>, 'kForeground': <StyleType.kForeground: 3>, 'kBackground': <StyleType.kBackground: 4>, 'kShadow': <StyleType.kShadow: 5>, 'kDecorations': <StyleType.kDecorations: 6>, 'kLetterSpacing': <StyleType.kLetterSpacing: 7>, 'kWordSpacing': <StyleType.kWordSpacing: 8>}
    kAllAttributes: animator.skia.textlayout.StyleType  # value = <StyleType.kAllAttributes: 1>
    kBackground: animator.skia.textlayout.StyleType  # value = <StyleType.kBackground: 4>
    kDecorations: animator.skia.textlayout.StyleType  # value = <StyleType.kDecorations: 6>
    kFont: animator.skia.textlayout.StyleType  # value = <StyleType.kFont: 2>
    kForeground: animator.skia.textlayout.StyleType  # value = <StyleType.kForeground: 3>
    kLetterSpacing: animator.skia.textlayout.StyleType  # value = <StyleType.kLetterSpacing: 7>
    kNone: animator.skia.textlayout.StyleType  # value = <StyleType.kNone: 0>
    kShadow: animator.skia.textlayout.StyleType  # value = <StyleType.kShadow: 5>
    kWordSpacing: animator.skia.textlayout.StyleType  # value = <StyleType.kWordSpacing: 8>
    pass

class TextAlign:
    """
    Members:

      kLeft

      kRight

      kCenter

      kJustify

      kStart

      kEnd
    """

    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    __members__: dict  # value = {'kLeft': <TextAlign.kLeft: 0>, 'kRight': <TextAlign.kRight: 1>, 'kCenter': <TextAlign.kCenter: 2>, 'kJustify': <TextAlign.kJustify: 3>, 'kStart': <TextAlign.kStart: 4>, 'kEnd': <TextAlign.kEnd: 5>}
    kCenter: animator.skia.textlayout.TextAlign  # value = <TextAlign.kCenter: 2>
    kEnd: animator.skia.textlayout.TextAlign  # value = <TextAlign.kEnd: 5>
    kJustify: animator.skia.textlayout.TextAlign  # value = <TextAlign.kJustify: 3>
    kLeft: animator.skia.textlayout.TextAlign  # value = <TextAlign.kLeft: 0>
    kRight: animator.skia.textlayout.TextAlign  # value = <TextAlign.kRight: 1>
    kStart: animator.skia.textlayout.TextAlign  # value = <TextAlign.kStart: 4>
    pass

class TextBaseline:
    """
    Members:

      kAlphabetic

      kIdeographic
    """

    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    __members__: dict  # value = {'kAlphabetic': <TextBaseline.kAlphabetic: 0>, 'kIdeographic': <TextBaseline.kIdeographic: 1>}
    kAlphabetic: animator.skia.textlayout.TextBaseline  # value = <TextBaseline.kAlphabetic: 0>
    kIdeographic: animator.skia.textlayout.TextBaseline  # value = <TextBaseline.kIdeographic: 1>
    pass

class TextBox:
    def __init__(self, rect: animator.skia.Rect, direction: TextDirection) -> None: ...
    def __str__(self) -> str: ...
    @property
    def direction(self) -> TextDirection:
        """
        :type: TextDirection
        """
    @direction.setter
    def direction(self, arg0: TextDirection) -> None:
        pass
    @property
    def rect(self) -> animator.skia.Rect:
        """
        :type: animator.skia.Rect
        """
    @rect.setter
    def rect(self, arg0: animator.skia.Rect) -> None:
        pass
    pass

class TextDecoration(IntEnum):
    """
    Members:

      kNoDecoration

      kUnderline

      kOverline

      kLineThrough
    """

    def __and__(self, other: object) -> object: ...
    def __eq__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __gt__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __invert__(self) -> object: ...
    def __le__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __or__(self, other: object) -> object: ...
    def __rand__(self, other: object) -> object: ...
    def __repr__(self) -> str: ...
    def __ror__(self, other: object) -> object: ...
    def __rxor__(self, other: object) -> object: ...
    def __setstate__(self, state: int) -> None: ...
    def __xor__(self, other: object) -> object: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    __members__: dict  # value = {'kNoDecoration': <TextDecoration.kNoDecoration: 0>, 'kUnderline': <TextDecoration.kUnderline: 1>, 'kOverline': <TextDecoration.kOverline: 2>, 'kLineThrough': <TextDecoration.kLineThrough: 4>}
    kLineThrough: animator.skia.textlayout.TextDecoration  # value = <TextDecoration.kLineThrough: 4>
    kNoDecoration: animator.skia.textlayout.TextDecoration  # value = <TextDecoration.kNoDecoration: 0>
    kOverline: animator.skia.textlayout.TextDecoration  # value = <TextDecoration.kOverline: 2>
    kUnderline: animator.skia.textlayout.TextDecoration  # value = <TextDecoration.kUnderline: 1>
    pass

class TextDecorationMode:
    """
    Members:

      kGaps

      kThrough
    """

    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    __members__: dict  # value = {'kGaps': <TextDecorationMode.kGaps: 0>, 'kThrough': <TextDecorationMode.kThrough: 1>}
    kGaps: animator.skia.textlayout.TextDecorationMode  # value = <TextDecorationMode.kGaps: 0>
    kThrough: animator.skia.textlayout.TextDecorationMode  # value = <TextDecorationMode.kThrough: 1>
    pass

class TextDecorationStyle:
    """
    Members:

      kSolid

      kDouble

      kDotted

      kDashed

      kWavy
    """

    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    __members__: dict  # value = {'kSolid': <TextDecorationStyle.kSolid: 0>, 'kDouble': <TextDecorationStyle.kDouble: 1>, 'kDotted': <TextDecorationStyle.kDotted: 2>, 'kDashed': <TextDecorationStyle.kDashed: 3>, 'kWavy': <TextDecorationStyle.kWavy: 4>}
    kDashed: animator.skia.textlayout.TextDecorationStyle  # value = <TextDecorationStyle.kDashed: 3>
    kDotted: animator.skia.textlayout.TextDecorationStyle  # value = <TextDecorationStyle.kDotted: 2>
    kDouble: animator.skia.textlayout.TextDecorationStyle  # value = <TextDecorationStyle.kDouble: 1>
    kSolid: animator.skia.textlayout.TextDecorationStyle  # value = <TextDecorationStyle.kSolid: 0>
    kWavy: animator.skia.textlayout.TextDecorationStyle  # value = <TextDecorationStyle.kWavy: 4>
    pass

class TextDirection:
    """
    Members:

      kRtl

      kLtr
    """

    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    __members__: dict  # value = {'kRtl': <TextDirection.kRtl: 0>, 'kLtr': <TextDirection.kLtr: 1>}
    kLtr: animator.skia.textlayout.TextDirection  # value = <TextDirection.kLtr: 1>
    kRtl: animator.skia.textlayout.TextDirection  # value = <TextDirection.kRtl: 0>
    pass

class TextHeightBehavior(IntEnum):
    """
    Members:

      kAll

      kDisableFirstAscent

      kDisableLastDescent

      kDisableAll
    """

    def __and__(self, other: object) -> object: ...
    def __eq__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __gt__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __invert__(self) -> object: ...
    def __le__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __or__(self, other: object) -> object: ...
    def __rand__(self, other: object) -> object: ...
    def __repr__(self) -> str: ...
    def __ror__(self, other: object) -> object: ...
    def __rxor__(self, other: object) -> object: ...
    def __setstate__(self, state: int) -> None: ...
    def __xor__(self, other: object) -> object: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    __members__: dict  # value = {'kAll': <TextHeightBehavior.kAll: 0>, 'kDisableFirstAscent': <TextHeightBehavior.kDisableFirstAscent: 1>, 'kDisableLastDescent': <TextHeightBehavior.kDisableLastDescent: 2>, 'kDisableAll': <TextHeightBehavior.kDisableAll: 3>}
    kAll: animator.skia.textlayout.TextHeightBehavior  # value = <TextHeightBehavior.kAll: 0>
    kDisableAll: animator.skia.textlayout.TextHeightBehavior  # value = <TextHeightBehavior.kDisableAll: 3>
    kDisableFirstAscent: animator.skia.textlayout.TextHeightBehavior  # value = <TextHeightBehavior.kDisableFirstAscent: 1>
    kDisableLastDescent: animator.skia.textlayout.TextHeightBehavior  # value = <TextHeightBehavior.kDisableLastDescent: 2>
    pass

class TextShadow:
    def __eq__(self, arg0: TextShadow) -> bool: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(
        self, color: _Color = animator.skia.ColorBLACK, offset: _Point = ..., blurSigma: float = 0
    ) -> None: ...
    def __ne__(self, arg0: TextShadow) -> bool: ...
    def hasShadow(self) -> bool: ...
    @property
    def fBlurSigma(self) -> float:
        """
        :type: float
        """
    @fBlurSigma.setter
    def fBlurSigma(self, arg0: float) -> None:
        pass
    @property
    def fColor(self) -> int:
        """
        :type: int
        """
    @fColor.setter
    def fColor(self, arg0: int) -> None:
        pass
    @property
    def fOffset(self) -> animator.skia.Point:
        """
        :type: animator.skia.Point
        """
    @fOffset.setter
    def fOffset(self, arg0: animator.skia.Point) -> None:
        pass
    pass

class TextStyle:
    def __eq__(self, arg0: TextStyle) -> bool: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(
        self,
        color: _Color = ...,
        foregroundPaint: animator.skia.Paint = ...,
        backgroundPaint: animator.skia.Paint = ...,
        decoration: TextDecoration = ...,
        decorationMode: TextDecorationMode = ...,
        decorationStyle: TextDecorationStyle = ...,
        decorationColor: _Color = ...,
        decorationThicknessMultiplier: float = ...,
        fontStyle: animator.skia.FontStyle = ...,
        shadows: list[TextShadow] = ...,
        fontArguments: animator.skia.FontArguments = ...,
        fontSize: float = ...,
        fontFamilies: list[str] = ...,
        baselineShift: float = ...,
        height: float = ...,
        heightOverride: bool = ...,
        halfLeading: bool = ...,
        letterSpacing: float = ...,
        wordSpacing: float = ...,
        typeface: animator.skia.Typeface = ...,
        locale: str = ...,
        textBaseline: TextBaseline = ...,
        placeholder: bool = ...,
    ) -> None:
        """
        Construct a new text style from keyword arguments. This creates a new :py:class:`TextStyle` object and calls the
        respective setters for each keyword argument.

        Supported keyword arguments: ``color``, ``foregroundPaint``, ``backgroundPaint``, ``decoration``,
        ``decorationMode``, ``decorationStyle``, ``decorationColor``, ``decorationThicknessMultiplier``, ``fontStyle``,
        ``shadows``, ``fontArguments``, ``fontSize``, ``fontFamilies``, ``baselineShift``, ``height``,
        ``heightOverride``, ``halfLeading``, ``letterSpacing``, ``wordSpacing``, ``typeface``, ``locale``,
        ``textBaseline``, ``placeholder``.
        """
    @typing.overload
    def __init__(self, arg0: TextStyle) -> None: ...
    def __str__(self) -> str: ...
    def addFontFeature(self, fontFeature: str, value: int) -> None: ...
    def addShadow(self, shadow: TextShadow) -> None: ...
    def clearBackgroundColor(self) -> None: ...
    def clearForegroundColor(self) -> None: ...
    def cloneForPlaceholder(self) -> TextStyle: ...
    def equals(self, other: TextStyle) -> bool: ...
    def equalsByFonts(self, that: TextStyle) -> bool: ...
    def getBackground(self) -> animator.skia.Paint: ...
    def getBaselineShift(self) -> float: ...
    def getColor(self) -> int: ...
    def getDecoration(self) -> Decoration: ...
    def getDecorationColor(self) -> int: ...
    def getDecorationMode(self) -> TextDecorationMode: ...
    def getDecorationStyle(self) -> TextDecorationStyle: ...
    def getDecorationThicknessMultiplier(self) -> float: ...
    def getDecorationType(self) -> TextDecoration: ...
    def getFontArguments(self) -> FontArguments | None: ...
    def getFontFamilies(self) -> list: ...
    def getFontFeatureNumber(self) -> int: ...
    def getFontFeatures(self) -> list[FontFeature]: ...
    def getFontMetrics(self) -> animator.skia.FontMetrics:
        """
        Returns the font metrics for the current font.
        """
    def getFontSize(self) -> float: ...
    def getFontStyle(self) -> animator.skia.FontStyle: ...
    def getForeground(self) -> animator.skia.Paint: ...
    def getHalfLeading(self) -> bool: ...
    def getHeight(self) -> float: ...
    def getHeightOverride(self) -> bool: ...
    def getLetterSpacing(self) -> float: ...
    def getLocale(self) -> str: ...
    def getShadowNumber(self) -> int: ...
    def getShadows(self) -> list[TextShadow]: ...
    def getTextBaseline(self) -> TextBaseline: ...
    def getTypeface(self) -> animator.skia.Typeface: ...
    def getWordSpacing(self) -> float: ...
    def hasBackground(self) -> bool: ...
    def hasForeground(self) -> bool: ...
    def isPlaceholder(self) -> bool: ...
    def matchOneAttribute(self, styleType: StyleType, other: TextStyle) -> bool: ...
    def refTypeface(self) -> animator.skia.Typeface: ...
    def resetFontFeatures(self) -> None: ...
    def resetShadows(self) -> None: ...
    def setBackgroundPaint(self, paint: animator.skia.Paint) -> None: ...
    def setBaselineShift(self, shift: float) -> None: ...
    def setColor(self, color: _Color) -> None: ...
    def setDecoration(self, decoration: TextDecoration) -> None: ...
    def setDecorationColor(self, color: _Color) -> None: ...
    def setDecorationMode(self, mode: TextDecorationMode) -> None: ...
    def setDecorationStyle(self, style: TextDecorationStyle) -> None: ...
    def setDecorationThicknessMultiplier(self, m: float) -> None: ...
    def setFontArguments(self, args: animator.skia.FontArguments | None) -> None: ...
    def setFontFamilies(self, families: list[str]) -> None: ...
    def setFontSize(self, size: float) -> None: ...
    def setFontStyle(self, style: animator.skia.FontStyle) -> None: ...
    def setForegroundPaint(self, paint: animator.skia.Paint) -> None: ...
    def setHalfLeading(self, halfLeading: bool) -> None: ...
    def setHeight(self, height: float) -> None: ...
    def setHeightOverride(self, heightOverride: bool) -> None: ...
    def setLetterSpacing(self, letterSpacing: float) -> None: ...
    def setLocale(self, locale: str) -> None: ...
    def setPlaceholder(self) -> None: ...
    def setTextBaseline(self, baseline: TextBaseline) -> None: ...
    def setTypeface(self, typeface: animator.skia.Typeface) -> None: ...
    def setWordSpacing(self, wordSpacing: float) -> None: ...
    pass
