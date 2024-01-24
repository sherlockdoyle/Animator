#include "modules/skparagraph/include/Paragraph.h"
#include "common.h"
#include "include/core/SkCanvas.h"
#include "modules/skparagraph/include/FontCollection.h"
#include "modules/skparagraph/src/ParagraphBuilderImpl.h"
#include <pybind11/iostream.h>
#include <pybind11/stl.h>
#include <unordered_set>

using namespace skia::textlayout;

class PyParagraph : public Paragraph
{
public:
    using Paragraph::Paragraph;
    void layout(SkScalar width) override { PYBIND11_OVERLOAD_PURE(void, Paragraph, layout, width); }
    void paint(SkCanvas *canvas, SkScalar x, SkScalar y) override
    {
        PYBIND11_OVERLOAD_PURE(void, Paragraph, paint, canvas, x, y);
    }
    void paint(ParagraphPainter *painter, SkScalar x, SkScalar y) override
    {
        PYBIND11_OVERLOAD_PURE(void, Paragraph, paint, painter, x, y);
    }
    std::vector<TextBox> getRectsForRange(unsigned start, unsigned end, RectHeightStyle rectHeightStyle,
                                          RectWidthStyle rectWidthStyle) override
    {
        PYBIND11_OVERLOAD_PURE(std::vector<TextBox>, Paragraph, getRectsForRange, start, end, rectHeightStyle,
                               rectWidthStyle);
    }
    std::vector<TextBox> getRectsForPlaceholders() override
    {
        PYBIND11_OVERLOAD_PURE(std::vector<TextBox>, Paragraph, getRectsForPlaceholders);
    }
    PositionWithAffinity getGlyphPositionAtCoordinate(SkScalar dx, SkScalar dy) override
    {
        PYBIND11_OVERLOAD_PURE(PositionWithAffinity, Paragraph, getGlyphPositionAtCoordinate, dx, dy);
    }
    SkRange<size_t> getWordBoundary(unsigned offset) override
    {
        PYBIND11_OVERLOAD_PURE(SkRange<size_t>, Paragraph, getWordBoundary, offset);
    }
    void getLineMetrics(std::vector<LineMetrics> &metrics) override
    {
        PYBIND11_OVERLOAD_PURE(void, Paragraph, getLineMetrics, metrics);
    }
    size_t lineNumber() override { PYBIND11_OVERLOAD_PURE(size_t, Paragraph, lineNumber); }
    void markDirty() override { PYBIND11_OVERLOAD_PURE(void, Paragraph, markDirty); }
    int32_t unresolvedGlyphs() override { PYBIND11_OVERLOAD_PURE(int32_t, Paragraph, unresolvedGlyphs); }
    std::unordered_set<SkUnichar> unresolvedCodepoints() override
    {
        PYBIND11_OVERLOAD_PURE(std::unordered_set<SkUnichar>, Paragraph, unresolvedCodepoints);
    }
    void updateTextAlign(TextAlign align) override { PYBIND11_OVERLOAD_PURE(void, Paragraph, updateTextAlign, align); }
    void updateFontSize(size_t from, size_t to, SkScalar fontSize) override
    {
        PYBIND11_OVERLOAD_PURE(void, Paragraph, updateFontSize, from, to, fontSize);
    }
    void updateForegroundPaint(size_t from, size_t to, SkPaint paint) override
    {
        PYBIND11_OVERLOAD_PURE(void, Paragraph, updateForegroundPaint, from, to, paint);
    }
    void updateBackgroundPaint(size_t from, size_t to, SkPaint paint) override
    {
        PYBIND11_OVERLOAD_PURE(void, Paragraph, updateBackgroundPaint, from, to, paint);
    }
    void visit(const Visitor &visitor) override { PYBIND11_OVERLOAD_PURE(void, Paragraph, visit, visitor); }
    void extendedVisit(const ExtendedVisitor &visitor) override
    {
        PYBIND11_OVERLOAD_PURE(void, Paragraph, extendedVisit, visitor);
    }
    int getPath(int lineNumber, SkPath *dest) override
    {
        PYBIND11_OVERLOAD_PURE(int, Paragraph, getPath, lineNumber, dest);
    }
    bool containsEmoji(SkTextBlob *textBlob) override
    {
        PYBIND11_OVERLOAD_PURE(bool, Paragraph, containsEmoji, textBlob);
    }
    bool containsColorFontOrBitmap(SkTextBlob *textBlob) override
    {
        PYBIND11_OVERLOAD_PURE(bool, Paragraph, containsColorFontOrBitmap, textBlob);
    }
    int getLineNumberAt(TextIndex codeUnitIndex) const override
    {
        PYBIND11_OVERLOAD_PURE(int, Paragraph, getLineNumberAt, codeUnitIndex);
    }
    int getLineNumberAtUTF16Offset(size_t codeUnitIndex) override
    {
        PYBIND11_OVERLOAD_PURE(int, Paragraph, getLineNumberAtUTF16Offset, codeUnitIndex);
    }
    bool getLineMetricsAt(int lineNumber, LineMetrics *lineMetrics) const override
    {
        PYBIND11_OVERLOAD_PURE(bool, Paragraph, getLineMetricsAt, lineNumber, lineMetrics);
    }
    TextRange getActualTextRange(int lineNumber, bool includeSpaces) const override
    {
        PYBIND11_OVERLOAD_PURE(TextRange, Paragraph, getActualTextRange, lineNumber, includeSpaces);
    }
    bool getGlyphClusterAt(TextIndex codeUnitIndex, GlyphClusterInfo *glyphInfo) override
    {
        PYBIND11_OVERLOAD_PURE(bool, Paragraph, getGlyphClusterAt, codeUnitIndex, glyphInfo);
    }
    bool getClosestGlyphClusterAt(SkScalar dx, SkScalar dy, GlyphClusterInfo *glyphInfo) override
    {
        PYBIND11_OVERLOAD_PURE(bool, Paragraph, getClosestGlyphClusterAt, dx, dy, glyphInfo);
    }
    bool getGlyphInfoAtUTF16Offset(size_t codeUnitIndex, GlyphInfo *glyphInfo) override
    {
        PYBIND11_OVERLOAD_PURE(bool, Paragraph, getGlyphInfoAtUTF16Offset, codeUnitIndex, glyphInfo);
    }
    bool getClosestUTF16GlyphInfoAt(SkScalar dx, SkScalar dy, GlyphInfo *glyphInfo) override
    {
        PYBIND11_OVERLOAD_PURE(bool, Paragraph, getClosestUTF16GlyphInfoAt, dx, dy, glyphInfo);
    }
    SkFont getFontAt(TextIndex codeUnitIndex) const override
    {
        PYBIND11_OVERLOAD_PURE(SkFont, Paragraph, getFontAt, codeUnitIndex);
    }
    SkFont getFontAtUTF16Offset(size_t codeUnitIndex) override
    {
        PYBIND11_OVERLOAD_PURE(SkFont, Paragraph, getFontAtUTF16Offset, codeUnitIndex);
    }
    std::vector<FontInfo> getFonts() const override
    {
        PYBIND11_OVERLOAD_PURE(std::vector<FontInfo>, Paragraph, getFonts);
    }
};

void initParagraph(py::module &m)
{
    py::class_<FontCollection, sk_sp<FontCollection>>(m, "FontCollection")
        .def(py::init())
        .def("getFontManagersCount", &FontCollection::getFontManagersCount)
        .def("setAssetFontManager", &FontCollection::setAssetFontManager, "fontManager"_a)
        .def("setDynamicFontManager", &FontCollection::setDynamicFontManager, "fontManager"_a)
        .def("setTestFontManager", &FontCollection::setTestFontManager, "fontManager"_a)
        .def("setDefaultFontManager", py::overload_cast<sk_sp<SkFontMgr>>(&FontCollection::setDefaultFontManager),
             "fontManager"_a)
        .def("setDefaultFontManager",
             py::overload_cast<sk_sp<SkFontMgr>, const char *>(&FontCollection::setDefaultFontManager), "fontManager"_a,
             "defaultFamilyName"_a)
        .def(
            "setDefaultFontManager",
            [](FontCollection &self, const sk_sp<SkFontMgr> &fontManager,
               const std::vector<std::string> &defaultFamilyNames)
            {
                self.setDefaultFontManager(fontManager,
                                           std::vector<SkString>(defaultFamilyNames.begin(), defaultFamilyNames.end()));
            },
            "fontManager"_a, "defaultFamilyNames"_a)
        .def("getFallbackManager", &FontCollection::getFallbackManager)
        .def(
            "findTypefaces",
            [](FontCollection &self, const std::vector<std::string> &familyNames, const SkFontStyle &fontStyle)
            { return self.findTypefaces(std::vector<SkString>(familyNames.begin(), familyNames.end()), fontStyle); },
            "familyNames"_a, "fontStyle"_a)
        .def(
            "findTypefaces",
            [](FontCollection &self, const std::vector<std::string> &familyNames, const SkFontStyle &fontStyle,
               const std::optional<const FontArguments> &fontArgs) {
                return self.findTypefaces(std::vector<SkString>(familyNames.begin(), familyNames.end()), fontStyle,
                                          fontArgs);
            },
            "familyNames"_a, "fontStyle"_a, "fontArgs"_a)
        .def(
            "defaultFallback",
            [](FontCollection &self, const SkUnichar &unicode, const SkFontStyle &fontStyle, const std::string &locale)
            { return self.defaultFallback(unicode, fontStyle, SkString(locale)); },
            "unicode"_a, "fontStyle"_a, "locale"_a)
        .def(
            "defaultEmojiFallback",
            [](FontCollection &self, const SkUnichar &emojiStart, const SkFontStyle &fontStyle,
               const std::string &locale)
            { return self.defaultEmojiFallback(emojiStart, fontStyle, SkString(locale)); },
            "emojiStart"_a, "fontStyle"_a, "locale"_a)
        .def("defaultFallback", py::overload_cast<>(&FontCollection::defaultFallback))
        .def("disableFontFallback", &FontCollection::disableFontFallback)
        .def("enableFontFallback", &FontCollection::enableFontFallback)
        .def("fontFallbackEnabled", &FontCollection::fontFallbackEnabled)
        .def("clearCaches", &FontCollection::clearCaches)
        .def("__str__",
             [](FontCollection &self)
             {
                 const size_t count = self.getFontManagersCount();
                 return "FontCollection({} font manager{}{})"_s.format(
                     count, count == 1 ? "" : "s", self.fontFallbackEnabled() ? ", fallback enabled" : "");
             });

    py::class_<StyleMetrics>(m, "StyleMetrics")
        .def(py::init<const TextStyle *>(), "style"_a, py::keep_alive<1, 2>())
        .def(py::init<const TextStyle *, SkFontMetrics &>(), "style"_a, "fontMetrics"_a)
        .def_readonly("text_style", &StyleMetrics::text_style)
        .def_readwrite("font_metrics", &StyleMetrics::font_metrics)
        .def("__str__", [](const StyleMetrics &self)
             { return "StyleMetrics(text_style={}, font_metrics={})"_s.format(self.text_style, self.font_metrics); });

    py::class_<LineMetrics>(m, "LineMetrics")
        .def(py::init())
        .def(py::init<size_t, size_t, size_t, size_t, bool>(), "start"_a = 0, "end"_a = 0,
             "end_excluding_whitespaces"_a = 0, "end_including_newline"_a = 0, "hard_break"_a = false)
        .def_readwrite("fStartIndex", &LineMetrics::fStartIndex)
        .def_readwrite("fEndIndex", &LineMetrics::fEndIndex)
        .def_readwrite("fEndExcludingWhitespaces", &LineMetrics::fEndExcludingWhitespaces)
        .def_readwrite("fEndIncludingNewline", &LineMetrics::fEndIncludingNewline)
        .def_readwrite("fHardBreak", &LineMetrics::fHardBreak)
        .def_readwrite("fAscent", &LineMetrics::fAscent)
        .def_readwrite("fDescent", &LineMetrics::fDescent)
        .def_readwrite("fUnscaledAscent", &LineMetrics::fUnscaledAscent)
        .def_readwrite("fHeight", &LineMetrics::fHeight)
        .def_readwrite("fWidth", &LineMetrics::fWidth)
        .def_readwrite("fLeft", &LineMetrics::fLeft)
        .def_readwrite("fBaseline", &LineMetrics::fBaseline)
        .def_readwrite("fLineNumber", &LineMetrics::fLineNumber)
        .def_readwrite("fLineMetrics", &LineMetrics::fLineMetrics)
        .def(
            "__str__",
            [](const LineMetrics &self)
            {
                return "LineMetrics(startIndex={}, endIndex={}, endExcludingWhitespaces={}, endIncludingNewline={}, hardBreak={}, ascent={}, descent={}, unscaledAscent={}, height={}, width={}, left={}, baseline={}, lineNumber={}, lineMetrics={})"_s
                    .format(self.fStartIndex, self.fEndIndex, self.fEndExcludingWhitespaces, self.fEndIncludingNewline,
                            self.fHardBreak, self.fAscent, self.fDescent, self.fUnscaledAscent, self.fHeight,
                            self.fWidth, self.fLeft, self.fBaseline, self.fLineNumber, self.fLineMetrics);
            });

    py::class_<Paragraph, PyParagraph> ParagraphClass(m, "Paragraph");
    ParagraphClass.def(py::init<ParagraphStyle, sk_sp<FontCollection>>(), "style"_a, "fonts"_a)
        .def("getMaxWidth", &Paragraph::getMaxWidth)
        .def("getHeight", &Paragraph::getHeight)
        .def("getMinIntrinsicWidth", &Paragraph::getMinIntrinsicWidth)
        .def("getMaxIntrinsicWidth", &Paragraph::getMaxIntrinsicWidth)
        .def("getAlphabeticBaseline", &Paragraph::getAlphabeticBaseline)
        .def("getIdeographicBaseline", &Paragraph::getIdeographicBaseline)
        .def("getLongestLine", &Paragraph::getLongestLine)
        .def("didExceedMaxLines", &Paragraph::didExceedMaxLines)
        .def("layout", &Paragraph::layout, "width"_a)
        .def("paint", py::overload_cast<SkCanvas *, SkScalar, SkScalar>(&Paragraph::paint), "canvas"_a, "x"_a, "y"_a)
        .def("getRectsForRange", &Paragraph::getRectsForRange, "start"_a, "end"_a, "rectHeightStyle"_a,
             "rectWidthStyle"_a)
        .def("getRectsForPlaceholders", &Paragraph::getRectsForPlaceholders)
        .def("getGlyphPositionAtCoordinate", &Paragraph::getGlyphPositionAtCoordinate, "dx"_a, "dy"_a)
        .def("getWordBoundary", &Paragraph::getWordBoundary, "offset"_a)
        .def("getLineMetrics",
             [](Paragraph &self)
             {
                 std::vector<LineMetrics> metrics;
                 self.getLineMetrics(metrics);
                 return metrics;
             })
        .def("lineNumber", &Paragraph::lineNumber)
        .def("markDirty", &Paragraph::markDirty)
        .def("unresolvedGlyphs", &Paragraph::unresolvedGlyphs)
        .def("updateTextAlign", &Paragraph::updateTextAlign, "textAlign"_a)
        .def("updateFontSize", &Paragraph::updateFontSize, "from_"_a, "to"_a, "fontSize"_a)
        .def("updateForegroundPaint", &Paragraph::updateForegroundPaint, "from_"_a, "to"_a, "paint"_a)
        .def("updateBackgroundPaint", &Paragraph::updateBackgroundPaint, "from_"_a, "to"_a, "paint"_a);

    py::enum_<Paragraph::VisitorFlags>(ParagraphClass, "VisitorFlags", py::arithmetic())
        .value("kWhiteSpace_VisitorFlag", Paragraph::VisitorFlags::kWhiteSpace_VisitorFlag);
    py::class_<Paragraph::VisitorInfo>(ParagraphClass, "VisitorInfo")
        .def_property_readonly(
            "font", [](const Paragraph::VisitorInfo &self) { return self.font; }, py::return_value_policy::reference,
            "TODO: How to bind reference fields? There's probably some memory leak here.")
        .def_readonly("origin", &Paragraph::VisitorInfo::origin)
        .def_readonly("advanceX", &Paragraph::VisitorInfo::advanceX)
        .def_readonly("count", &Paragraph::VisitorInfo::count)
        .def_property_readonly("glyphs", [](const Paragraph::VisitorInfo &self)
                               { return std::vector<uint16_t>(self.glyphs, self.glyphs + self.count); })
        .def_property_readonly("positions", [](const Paragraph::VisitorInfo &self)
                               { return std::vector<SkPoint>(self.positions, self.positions + self.count); })
        .def_property_readonly("utf8Starts", [](const Paragraph::VisitorInfo &self)
                               { return std::vector<uint32_t>(self.utf8Starts, self.utf8Starts + self.count + 1); })
        .def_property_readonly("flags", [](const Paragraph::VisitorInfo &self)
                               { return static_cast<Paragraph::VisitorFlags>(self.flags); })
        .def("__str__",
             [](const Paragraph::VisitorInfo &self)
             {
                 return "VisitorInfo(origin={}, advanceX={}, {} glyph{}, flags={})"_s.format(
                     self.origin, self.advanceX, self.count, self.count == 1 ? "" : "s", self.flags);
             });
    ParagraphClass.def(
        "visit",
        [](Paragraph &self)
        {
            py::list result;
            self.visit([&result](int lineNumber, const Paragraph::VisitorInfo *info)
                       { result.append(py::make_tuple(lineNumber, info ? py::cast(*info) : py::none())); });
            return result;
        },
        "Returns a list of (lineNumber, visitorInfo) tuples.");

    py::class_<Paragraph::ExtendedVisitorInfo>(ParagraphClass, "ExtendedVisitorInfo")
        .def_property_readonly(
            "font", [](const Paragraph::ExtendedVisitorInfo &self) { return self.font; },
            py::return_value_policy::reference,
            "TODO: How to bind reference fields? There's probably some memory leak here.")
        .def_readonly("origin", &Paragraph::ExtendedVisitorInfo::origin)
        .def_readonly("advance", &Paragraph::ExtendedVisitorInfo::advance)
        .def_readonly("count", &Paragraph::ExtendedVisitorInfo::count)
        .def_property_readonly("glyphs", [](const Paragraph::ExtendedVisitorInfo &self)
                               { return std::vector<uint16_t>(self.glyphs, self.glyphs + self.count); })
        .def_property_readonly("positions", [](const Paragraph::ExtendedVisitorInfo &self)
                               { return std::vector<SkPoint>(self.positions, self.positions + self.count); })
        .def_property_readonly("bounds", [](const Paragraph::ExtendedVisitorInfo &self)
                               { return std::vector<SkRect>(self.bounds, self.bounds + self.count); })
        .def_property_readonly("utf8Starts", [](const Paragraph::ExtendedVisitorInfo &self)
                               { return std::vector<uint32_t>(self.utf8Starts, self.utf8Starts + self.count + 1); })
        .def_property_readonly("flags", [](const Paragraph::ExtendedVisitorInfo &self)
                               { return static_cast<Paragraph::VisitorFlags>(self.flags); })
        .def("__str__",
             [](const Paragraph::ExtendedVisitorInfo &self)
             {
                 return "ExtendedVisitorInfo(origin={}, advance={}, {} glyph{}, flags={})"_s.format(
                     self.origin, self.advance, self.count, self.count == 1 ? "" : "s", self.flags);
             });
    ParagraphClass
        .def(
            "extendVisit",
            [&](Paragraph &self)
            {
                py::list result;
                self.extendedVisit([&result](int lineNumber, const Paragraph::ExtendedVisitorInfo *info)
                                   { result.append(py::make_tuple(lineNumber, info ? py::cast(*info) : py::none())); });
                return result;
            },
            "Returns a list of (lineNumber, extendedVisitorInfo) tuples.")
        .def(
            "getPath",
            [](Paragraph &self, const int &lineNumber)
            {
                SkPath dest;
                const int count = self.getPath(lineNumber, &dest);
                return py::make_tuple(dest, count);
            },
            "Returns a tuple of (path, number of glyphs that could not be converted).", "lineNumber"_a)
        .def_static("GetPath", &Paragraph::GetPath, "textBlob"_a)
        .def("containsEmoji", &Paragraph::containsEmoji, "textBlob"_a)
        .def("containsColorFontOrBitmap", &Paragraph::containsColorFontOrBitmap, "textBlob"_a)
        .def("getLineNumberAt", &Paragraph::getLineNumberAt, "codeUnitIndex"_a)
        .def("getLineNumberAtUTF16Offset", &Paragraph::getLineNumberAtUTF16Offset, "codeUnitIndex"_a)
        .def(
            "getLineMetricsAt",
            [](const Paragraph &self, int lineNumber) -> std::optional<LineMetrics>
            {
                LineMetrics lineMetrics;
                if (self.getLineMetricsAt(lineNumber, &lineMetrics))
                    return lineMetrics;
                return std::nullopt;
            },
            "Returns line metrics info for the line, or `None` if the line is not found.", "lineNumber"_a)
        .def("getActualTextRange", &Paragraph::getActualTextRange, "lineNumber"_a, "includeSpaces"_a);

    py::class_<Paragraph::GlyphClusterInfo>(ParagraphClass, "GlyphClusterInfo")
        .def_readonly("fBounds", &Paragraph::GlyphClusterInfo::fBounds)
        .def_readonly("fClusterTextRange", &Paragraph::GlyphClusterInfo::fClusterTextRange)
        .def_readonly("fGlyphClusterPosition", &Paragraph::GlyphClusterInfo::fGlyphClusterPosition)
        .def("__str__",
             [](const Paragraph::GlyphClusterInfo &self)
             {
                 return "GlyphClusterInfo(fBounds={}, fClusterTextRange={}, fGlyphClusterPosition={})"_s.format(
                     self.fBounds, self.fClusterTextRange, self.fGlyphClusterPosition);
             });
    ParagraphClass
        .def(
            "getGlyphClusterAt",
            [](Paragraph &self, TextIndex codeUnitIndex) -> std::optional<Paragraph::GlyphClusterInfo>
            {
                Paragraph::GlyphClusterInfo glyphInfo;
                if (self.getGlyphClusterAt(codeUnitIndex, &glyphInfo))
                    return glyphInfo;
                return std::nullopt;
            },
            "codeUnitIndex"_a)
        .def(
            "getClosestGlyphClusterAt",
            [](Paragraph &self, SkScalar dx, SkScalar dy) -> std::optional<Paragraph::GlyphClusterInfo>
            {
                Paragraph::GlyphClusterInfo glyphInfo;
                if (self.getClosestGlyphClusterAt(dx, dy, &glyphInfo))
                    return glyphInfo;
                return std::nullopt;
            },
            "dx"_a, "dy"_a);

    py::class_<Paragraph::GlyphInfo>(ParagraphClass, "GlyphInfo")
        .def_readonly("fGraphemeLayoutBounds", &Paragraph::GlyphInfo::fGraphemeLayoutBounds)
        .def_readonly("fGraphemeClusterTextRange", &Paragraph::GlyphInfo::fGraphemeClusterTextRange)
        .def_readonly("fDirection", &Paragraph::GlyphInfo::fDirection)
        .def_readonly("fIsEllipsis", &Paragraph::GlyphInfo::fIsEllipsis)
        .def(
            "__str__",
            [](const Paragraph::GlyphInfo &self)
            {
                return "GlyphInfo(fGraphemeLayoutBounds={}, fGraphemeClusterTextRange={}, fDirection={}, fIsEllipsis={})"_s
                    .format(self.fGraphemeLayoutBounds, self.fGraphemeClusterTextRange, self.fDirection,
                            self.fIsEllipsis);
            });
    ParagraphClass
        .def("getGlyphInfoAtUTF16Offset",
             [](Paragraph &self, const size_t &codeUnitIndex) -> std::optional<Paragraph::GlyphInfo>
             {
                 Paragraph::GlyphInfo glyphInfo;
                 if (self.getGlyphInfoAtUTF16Offset(codeUnitIndex, &glyphInfo))
                     return glyphInfo;
                 return std::nullopt;
             })
        .def("getClosestUTF16GlyphInfoAt",
             [](Paragraph &self, const SkScalar &dx, const SkScalar &dy) -> std::optional<Paragraph::GlyphInfo>
             {
                 Paragraph::GlyphInfo glyphInfo;
                 if (self.getClosestUTF16GlyphInfoAt(dx, dy, &glyphInfo))
                     return glyphInfo;
                 return std::nullopt;
             });

    py::class_<Paragraph::FontInfo>(ParagraphClass, "FontInfo")
        .def(py::init<const SkFont &, const TextRange &>(), "font"_a, "textRange"_a)
        .def(py::init<const Paragraph::FontInfo &>(), "other"_a)
        .def_readwrite("fFont", &Paragraph::FontInfo::fFont)
        .def_readwrite("fTextRange", &Paragraph::FontInfo::fTextRange)
        .def("__str__", [](const Paragraph::FontInfo &self)
             { return "FontInfo(fFont={}, fTextRange={})"_s.format(self.fFont, self.fTextRange); });
    ParagraphClass.def("getFontAt", &Paragraph::getFontAt, "codeUnitIndex"_a)
        .def("getFontAtUTF16Offset", &Paragraph::getFontAtUTF16Offset, "codeUnitIndex"_a)
        .def("getFonts", &Paragraph::getFonts)
        .def(
            "__str__",
            [](Paragraph &self)
            {
                return "Paragraph(maxWidth={}, height={}, minIntrinsicWidth={}, maxIntrinsicWidth={}, alphabeticBaseline={}, ideographicBaseline={}, longestLine={}, didExceedMaxLines={})"_s
                    .format(self.getMaxWidth(), self.getHeight(), self.getMinIntrinsicWidth(),
                            self.getMaxIntrinsicWidth(), self.getAlphabeticBaseline(), self.getIdeographicBaseline(),
                            self.getLongestLine(), self.didExceedMaxLines());
            });

    py::class_<ParagraphBuilderImpl, std::unique_ptr<ParagraphBuilderImpl>>(m, "ParagraphBuilder")
        .def(py::init<ParagraphStyle, sk_sp<FontCollection>>(), "style"_a, "fontCollection"_a)
        .def(py::init(
                 [](const ParagraphStyle &style, const sk_sp<SkFontMgr> &fontMgr)
                 {
                     const sk_sp<FontCollection> fontCollection = sk_make_sp<FontCollection>();
                     fontCollection->setDefaultFontManager(fontMgr);
                     fontCollection->enableFontFallback();
                     return std::make_unique<ParagraphBuilderImpl>(style, fontCollection);
                 }),
             "style"_a, "fontMgr"_a)
        .def("pushStyle", &ParagraphBuilderImpl::pushStyle, "style"_a)
        .def("pop", &ParagraphBuilderImpl::pop)
        .def("peekStyle", &ParagraphBuilderImpl::peekStyle)
        .def(
            "addText",
            [](ParagraphBuilderImpl &self, const std::string &text) { self.addText(text.c_str(), text.size()); },
            "text"_a)
        .def("addPlaceholder", py::overload_cast<const PlaceholderStyle &>(&ParagraphBuilderImpl::addPlaceholder),
             "placeholderStyle"_a)
        .def("Build", &ParagraphBuilderImpl::Build)
        .def("getText",
             [](ParagraphBuilderImpl &self)
             {
                 auto text = self.getText();
                 return py::str(text.data(), text.size());
             })
        .def("getParagraphStyle", &ParagraphBuilderImpl::getParagraphStyle)
        .def("Reset", &ParagraphBuilderImpl::Reset)
        .def_static("make",
                    py::overload_cast<const ParagraphStyle &, sk_sp<FontCollection>>(&ParagraphBuilderImpl::make),
                    "style"_a, "fontCollection"_a)
        .def("__str__",
             [](ParagraphBuilderImpl &self)
             {
                 const auto &text = self.getText();
                 return "ParagraphBuilder({})"_s.format(py::repr(py::str(text.data(), text.size())));
             });
}