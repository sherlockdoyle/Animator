"""Entities for showing text."""
from __future__ import annotations

__all__ = 'SimpleText', 'KernedText'

import math
import re
from typing import Any, List, TYPE_CHECKING, Tuple, TypeVar

from .entity import Entity
from .. import skia

if TYPE_CHECKING:
    FontStyle = Tuple[int, int, skia.FontStyle.Slant]
    ET = TypeVar('ET', bound=Entity)

_NON_LETTER_REGEX = re.compile(r'[^a-zA-Z]+')
_DEFAULT_FONT_SIZE = skia.Font().getSize()


class TextCommon:
    """Common properties for text entities."""

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

    DEFAULT_SIZE = _DEFAULT_FONT_SIZE
    DEFAULT_STYLE: FontStyle = (Weight.NORMAL, Width.NORMAL, Slant.UPRIGHT)

    @staticmethod
    def get_available_fonts() -> List[str]:
        """Return a list of available system fonts."""
        return list(skia.FontMgr.RefDefault())

    @staticmethod
    def _parse_font_style(style: str) -> FontStyle:
        """Parse font style string."""
        style = _NON_LETTER_REGEX.sub(' ', style).strip().lower()
        font_style = list(TextCommon.DEFAULT_STYLE)
        components = [TextCommon.Weight, TextCommon.Width, TextCommon.Slant]
        for i in range(3):
            for attr, value in components[i].__dict__.items():
                if not attr.startswith('_'):
                    attr: str = attr.lower().replace('_', ' ')
                    if attr in style or attr.replace(' ', '') in style:
                        font_style[i] = value
        return tuple(font_style)

    @staticmethod
    def get_font(name: str | None = None, style: FontStyle | str = DEFAULT_STYLE) -> skia.Typeface:
        """Get best matching font for given *name*.

        :param name: Font name. If ``None``, returns default font.
        :param style: Font style, tuple of (weight, width, slant). Use ``TextCommon.Weight``, ``TextCommon.Width``,
            and ``TextCommon.Slant``.
        """
        if isinstance(style, str):
            style = TextCommon._parse_font_style(style)
        return skia.FontMgr.RefDefault().matchFamilyStyle(name, skia.FontStyle(*style))

    def __init__(self: Entity, font: str | None, size: float = DEFAULT_SIZE, style: FontStyle | str = DEFAULT_STYLE):
        self.font: skia.Font = skia.Font(TextCommon.get_font(font, style), size)
        # should have been initialized by a super call to Entity
        self.style.stroke_width = -1
        self.style.fill_color = (1, 1, 1, 1)

    def set_fake_width(self, width: float = 1) -> None:
        """Set fake width for text, for font which doesn't support width.

        :param width: Width in pixels. ``1`` means no change. Smaller values shrink text. Larger values expand text.
        """
        self.font.setScaleX(width)

    def set_fake_slant(self, slant: float = 0) -> None:
        """Set fake slant for text, for font which doesn't support slanting.

        :param slant: Angle of slant in degrees. ``0`` means no change. Positive values slant text to the left.
            Negative values slant text to the right.
        """
        self.font.setSkewX(math.tan(math.radians(slant)))

    def align_with_baseline(self: ET, x: float = 0) -> ET:
        """Align this entity by changing its *offset* to be at the relative *x* position of this entity while
        vertically aligning it with the baseline.

        This can be used for text alignment. ``-1`` is left, ``0`` is center, ``1`` is right.

        :param x: The relative horizontal position in the entity. The coordinate is between -1 (left) and 1 (right).
        :return: Itself for chaining.
        """
        bounds = self.get_bounds()
        self.offset.offset(-(x + 1) * bounds.width() / 2 - bounds.left(), self.offset.y())
        return self


class SimpleText(Entity, TextCommon):
    """Simple text, shown simply!"""

    def __init__(self, text: str, font: str | None = None, size: float = TextCommon.DEFAULT_SIZE,
                 style: FontStyle | str = TextCommon.DEFAULT_STYLE, *args: Any, **kwargs: Any):
        """
        :param text: The text to display.
        :param font: The font to use.
        :param size: The size of the font.
        :param style: The style of the font.
        """
        Entity.__init__(self, *args, **kwargs)
        TextCommon.__init__(self, font, size, style)
        self.text: str = text

    def on_draw(self) -> None:
        self.scene.canvas.save()
        self.scene.canvas.concat(self.total_transformation)
        fill_paint, stroke_paint, opacity = self.style.get_paints()
        if opacity:
            if opacity < 1:
                self.scene.canvas.saveLayerAlpha(None, round(opacity * 255))
            self.scene.canvas.drawString(self.text, *self.offset, self.font, fill_paint)
            self.scene.canvas.drawString(self.text, *self.offset, self.font, stroke_paint)
            if opacity < 1:
                self.scene.canvas.restore()
        self.scene.canvas.restore()

    def get_bounds(self, transformed: bool = False) -> skia.Rect:
        bounds = skia.Rect()
        self.font.measureText(self.text, bounds=bounds)
        bounds.offset(self.offset)
        if transformed:
            bounds = self.mat.mapRect(bounds, skia.ApplyPerspectiveClip.kNo)
        return bounds


class KernedText(Entity, TextCommon):
    """Text with kerning."""

    def __init__(self, text: str, font: str | None = None, size: float = TextCommon.DEFAULT_SIZE,
                 style: FontStyle | str = TextCommon.DEFAULT_STYLE, *args: Any, **kwargs: Any):
        """
        :param text: The text to display.
        :param font: The font to use.
        :param size: The size of the font.
        :param style: The style of the font.
        """
        Entity.__init__(self, *args, **kwargs)
        TextCommon.__init__(self, font, size, style)
        self.text: str = text
        self.text_blob: skia.TextBlob | None = None

        self._is_text_dirty: bool = True
        self.__kerning_sub: float = 0
        self.__builder: skia.TextBlobBuilder = skia.TextBlobBuilder()

    def __setattr__(self, key: str, value: Any) -> None:
        super().__setattr__(key, value)
        if key == 'text':
            self._is_text_dirty = True

    def update_text_blob(self) -> None:
        if self._is_text_dirty:
            glyphs = self.font.textToGlyphs(self.text)
            x_pos = self.font.getXPos(glyphs)
            typeface: skia.Typeface = self.font.getTypefaceOrDefault()
            kerning = typeface.getKerningPairAdjustments(glyphs)
            if kerning:
                multiplier = self.font.getSize() / typeface.getUnitsPerEm()
                kerning[0] *= multiplier
                x_pos[1] += kerning[0]
                for i in range(1, len(kerning)):
                    kerning[i] *= multiplier
                    kerning[i] += kerning[i - 1]
                    x_pos[i + 1] += kerning[i]
                self.__kerning_sub = kerning[-1]
            else:
                self.__kerning_sub = 0
            self.__builder.allocRunPosH(self.font, glyphs, x_pos, 0)
            self.text_blob = self.__builder.make()
            self._is_text_dirty = False

    def on_draw(self) -> None:
        self.update_text_blob()
        if self.text_blob is None:
            return

        self.scene.canvas.save()
        self.scene.canvas.concat(self.total_transformation)
        fill_paint, stroke_paint, opacity = self.style.get_paints()
        if opacity:
            if opacity < 1:
                self.scene.canvas.saveLayerAlpha(None, round(opacity * 255))
            self.scene.canvas.drawTextBlob(self.text_blob, *self.offset, fill_paint)
            self.scene.canvas.drawTextBlob(self.text_blob, *self.offset, stroke_paint)
            if opacity < 1:
                self.scene.canvas.restore()
        self.scene.canvas.restore()

    def get_bounds(self, transformed: bool = False) -> skia.Rect:
        self.update_text_blob()
        if self.text_blob is None:
            return skia.Rect()

        bounds = skia.Rect()
        self.font.measureText(self.text, bounds=bounds)
        bounds.fRight += self.__kerning_sub
        bounds.offset(self.offset)
        if transformed:
            bounds = self.mat.mapRect(bounds, skia.ApplyPerspectiveClip.kNo)
        return bounds
