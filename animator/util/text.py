from animator import skia

FONT_COLLECTION = skia.textlayout.FontCollection()
FONT_COLLECTION.setDefaultFontManager(skia.FontMgr())


def get_char_width(text_style: skia.textlayout.TextStyle) -> float:
    return (
        skia.Font(
            FONT_COLLECTION.findTypefaces(text_style.getFontFamilies(), text_style.getFontStyle())[0],
            text_style.getFontSize(),
        )
        .getMetrics()[0]
        .fAvgCharWidth
    )
