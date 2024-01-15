import math
from enum import IntFlag
from typing import Literal, TypeVar

from animator import skia
from animator.entity import relpos
from animator.entity.entity import Group
from animator.entity.relpos import RelativePosition

ET = TypeVar('ET', bound='Container')


def _reverse_pairs(lst: list[float]) -> None:
    """Reverse a list of even length with two elements at a time, inplace.

    >>> _reverse_pairs([1, 2, 3, 4, 5, 6])
    [2, 1, 4, 3, 6, 5]
    """
    for i in range(0, len(lst), 2):
        lst[i], lst[i + 1] = lst[i + 1], lst[i]


TextAlign = Literal['left', 'right', 'center', 'justify']
text_aligns: dict[TextAlign, skia.textlayout.TextAlign] = {
    'left': skia.textlayout.TextAlign.kLeft,
    'right': skia.textlayout.TextAlign.kRight,
    'center': skia.textlayout.TextAlign.kCenter,
    'justify': skia.textlayout.TextAlign.kJustify,
}


class Container(Group):
    def arrange_in_line(self: ET, dir: RelativePosition = relpos.RIGHT, gap: float = 25) -> ET:
        """Arrange the children in a line along the given *dir*ection and *gap* between them."""
        num_children = len(self.children)
        if not num_children:
            return self

        bounds = [c.get_bounds() for c in self.children]
        widths: list[float] = []
        heights: list[float] = []
        for b in bounds:
            widths.append(-b.fLeft)
            widths.append(b.fRight)
            heights.append(-b.fTop)
            heights.append(b.fBottom)
        if dir[0] < 0:
            _reverse_pairs(widths)
        if dir[1] < 0:
            _reverse_pairs(heights)

        padding_extra = gap * (num_children - 1)
        widths[0] -= (sum(widths) + padding_extra) / 2
        heights[0] -= (sum(heights) + padding_extra) / 2
        for i in range(2, num_children * 2, 2):
            widths[i] += widths[i - 2] + widths[i - 1] + gap
            heights[i] += heights[i - 2] + heights[i - 1] + gap
        for i in range(num_children):
            self.children[i].pos.set(widths[i * 2] * dir[0], heights[i * 2] * dir[1])

        return self

    class GridDirection(IntFlag):
        """Useful flag for :meth:`arrange_in_grid` direction."""

        LEFT = 0b000
        RIGHT = 0b100
        TOP = 0b000
        BOTTOM = 0b010
        HORIZONTAL = 0b000
        VERTICAL = 0b001

    def arrange_in_grid(
        self: ET, rows: int | None = None, cols: int | None = None, dir: int = 0b000, gap: float = 25
    ) -> ET:
        """
        Arrange the children in a grid of *rows* and *cols* with the given *dir*ection and *gap* between them. The
        direction is a 3-bit integer with bits 1, 2, and 3 (where 1 is the MSB) representing:

        1. x-pos: 0 = left, 1 = right
        2. y-pos: 0 = top, 1 = bottom
        3. main direction: 0 = first horizontally then vertically, 1 = first vertically then horizontally

        For instance, ``dir=0b101`` means start from right top corner and first go down then left.

        If neither *rows* nor *cols* is provided, the grid will be as close to a square as possible.
        """
        num_children = len(self.children)
        if not num_children:
            return self
        if cols is None:
            if rows is None:
                rows = math.floor(math.sqrt(num_children))
            cols = num_children // rows + bool(num_children % rows)
        elif rows is None:
            rows = num_children // cols + bool(num_children % cols)
        if rows * cols < num_children:
            raise ValueError(f'Cannot arrange {num_children} children in a {rows}x{cols} grid')

        x = cols - 1 if dir & 0b100 else 0
        y = rows - 1 if dir & 0b010 else 0
        dx = -1 if dir & 0b100 else 1
        dy = -1 if dir & 0b010 else 1
        vertical = dir & 0b001
        widths: list[float] = [0.0] * cols * 2
        heights: list[float] = [0.0] * rows * 2
        idx: list[tuple[int, int]] = []
        for c in self.children:
            bounds = c.get_bounds()
            widths[x * 2] = max(widths[x * 2], -bounds.fLeft)
            widths[x * 2 + 1] = max(widths[x * 2 + 1], bounds.fRight)
            heights[y * 2] = max(heights[y * 2], -bounds.fTop)
            heights[y * 2 + 1] = max(heights[y * 2 + 1], bounds.fBottom)
            idx.append((x, y))
            if vertical:
                y += dy
                if y < 0 or y >= rows:
                    x += dx
                    y %= rows
            else:
                x += dx
                if x < 0 or x >= cols:
                    y += dy
                    x %= cols

        widths[0] -= (sum(widths) + gap * (cols - 1)) / 2
        heights[0] -= (sum(heights) + gap * (rows - 1)) / 2
        for i in range(2, cols * 2, 2):
            widths[i] += widths[i - 2] + widths[i - 1] + gap
        for i in range(2, rows * 2, 2):
            heights[i] += heights[i - 2] + heights[i - 1] + gap
        for i in range(num_children):
            self.children[i].pos.set(widths[idx[i][0] * 2], heights[idx[i][1] * 2])
        return self

    def arrange_as_text(self: ET, width: float, align: TextAlign = 'left') -> ET:
        """
        Arrange the children as text, with the given *width* and *align*ment (one of 'left', 'right', 'center', or
        'justify').
        """
        builder = skia.textlayout.ParagraphBuilder(
            skia.textlayout.ParagraphStyle(
                textStyle=skia.textlayout.TextStyle(fontSize=0.1),  # apparently 0 resets to 1
                textAlign=text_aligns[align],
                # we don't use the height parameter, instead we use the fontSize since that also hides the spaces
            ),
            skia.FontMgr.RefDefault(),  # we need some fonts to get the spaces working
        )
        for c in self.children:
            bounds = c.get_bounds()
            builder.addPlaceholder(
                skia.textlayout.PlaceholderStyle(width=bounds.width(), height=bounds.height(), offset=-bounds.fTop)
            )
            # space is required for dynamic gaps between placeholders (say, during justification)
            builder.addText(' ')  # zwsp doesn't work
        paragraph = builder.Build()
        paragraph.layout(width)
        for i, box in enumerate(paragraph.getRectsForPlaceholders()):
            child = self.children[i]
            bounds = child.get_bounds()
            child.pos.set(box.rect.fLeft - bounds.fLeft, box.rect.fTop - bounds.fTop)

        return self
