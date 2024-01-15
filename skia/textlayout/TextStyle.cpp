#include "modules/skparagraph/include/TextStyle.h"
#include "common.h"
#include <pybind11/operators.h>
#include <pybind11/stl.h>

using namespace skia::textlayout;

void initTextStyle(py::module &m)
{
    py::class_<TextShadow>(m, "TextShadow")
        .def_readwrite("fColor", &TextShadow::fColor)
        .def_readwrite("fOffset", &TextShadow::fOffset)
        .def_readwrite("fBlurSigma", &TextShadow::fBlurSigma)
        .def(py::init())
        .def(py::init<SkColor, SkPoint, double>(), "color"_a = SK_ColorBLACK, "offset"_a = SkPoint{0, 0},
             "blurSigma"_a = 0)
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def("hasShadow", &TextShadow::hasShadow);

    py::class_<FontArguments>(m, "FontArguments")
        .def(py::init<const SkFontArguments &>())
        .def(py::init<const FontArguments &>())
        .def("CloneTypeface", &FontArguments::CloneTypeface, "typeface"_a)
        .def(py::self == py::self)
        .def(py::self != py::self);

    py::implicitly_convertible<SkFontArguments, FontArguments>();

    py::enum_<TextDecoration>(m, "TextDecoration", py::arithmetic())
        .value("kNoDecoration", TextDecoration::kNoDecoration)
        .value("kUnderline", TextDecoration::kUnderline)
        .value("kOverline", TextDecoration::kOverline)
        .value("kLineThrough", TextDecoration::kLineThrough);

    py::enum_<TextDecorationStyle>(m, "TextDecorationStyle")
        .value("kSolid", TextDecorationStyle::kSolid)
        .value("kDouble", TextDecorationStyle::kDouble)
        .value("kDotted", TextDecorationStyle::kDotted)
        .value("kDashed", TextDecorationStyle::kDashed)
        .value("kWavy", TextDecorationStyle::kWavy);

    py::enum_<TextDecorationMode>(m, "TextDecorationMode")
        .value("kGaps", TextDecorationMode::kGaps)
        .value("kThrough", TextDecorationMode::kThrough);

    py::enum_<StyleType>(m, "StyleType")
        .value("kNone", StyleType::kNone)
        .value("kAllAttributes", StyleType::kAllAttributes)
        .value("kFont", StyleType::kFont)
        .value("kForeground", StyleType::kForeground)
        .value("kBackground", StyleType::kBackground)
        .value("kShadow", StyleType::kShadow)
        .value("kDecorations", StyleType::kDecorations)
        .value("kLetterSpacing", StyleType::kLetterSpacing)
        .value("kWordSpacing", StyleType::kWordSpacing);

    py::class_<Decoration>(m, "Decoration")
        .def(py::init())
        .def(py::init(
                 [](const TextDecoration &type, const TextDecorationMode &mode, const SkColor &color,
                    const TextDecorationStyle &style, const SkScalar &thicknessMultiplier) {
                     return Decoration{type, mode, color, style, thicknessMultiplier};
                 }),
             "type"_a = TextDecoration::kNoDecoration, "mode"_a = TextDecorationMode::kGaps, "color"_a = 0,
             "style"_a = TextDecorationStyle::kSolid, "thicknessMultiplier"_a = 0)
        .def_readwrite("fType", &Decoration::fType)
        .def_readwrite("fMode", &Decoration::fMode)
        .def_readwrite("fColor", &Decoration::fColor)
        .def_readwrite("fStyle", &Decoration::fStyle)
        .def_readwrite("fThicknessMultiplier", &Decoration::fThicknessMultiplier)
        .def(py::self == py::self)
        .def("__str__",
             [](const Decoration &self)
             {
                 return "Decoration(type={}, mode={}, color={:x}, style={}, thicknessMultiplier={})"_s.format(
                     self.fType, self.fMode, self.fColor, self.fStyle, self.fThicknessMultiplier);
             });

    py::enum_<PlaceholderAlignment>(m, "PlaceholderAlignment")
        .value("kBaseline", PlaceholderAlignment::kBaseline)
        .value("kAboveBaseline", PlaceholderAlignment::kAboveBaseline)
        .value("kBelowBaseline", PlaceholderAlignment::kBelowBaseline)
        .value("kTop", PlaceholderAlignment::kTop)
        .value("kBottom", PlaceholderAlignment::kBottom)
        .value("kMiddle", PlaceholderAlignment::kMiddle);

    py::class_<FontFeature>(m, "FontFeature")
        .def(py::init([](const std::string &name, const int &value) { return FontFeature(SkString(name), value); }),
             "name"_a, "value"_a)
        .def(py::self == py::self)
        .def_property(
            "fName", [](const FontFeature &self) { return SkString2pyStr(self.fName); },
            [](FontFeature &self, const std::string &name) { self.fName = SkString(name); })
        .def_readwrite("fValue", &FontFeature::fValue)
        .def("__str__", [](const FontFeature &self)
             { return "FontFeature(name={}, value={})"_s.format(SkString2pyStr(self.fName), self.fValue); });

    py::class_<PlaceholderStyle>(m, "PlaceholderStyle")
        .def(py::init())
        .def(py::init<SkScalar, SkScalar, PlaceholderAlignment, TextBaseline, SkScalar>(), "width"_a = 0,
             "height"_a = 0, "alignment"_a = PlaceholderAlignment::kBaseline, "baseline"_a = TextBaseline::kAlphabetic,
             "offset"_a = 0)
        .def("equals", &PlaceholderStyle::equals, "other"_a)
        .def("__eq__", &PlaceholderStyle::equals, py::is_operator())
        .def_readwrite("fWidth", &PlaceholderStyle::fWidth)
        .def_readwrite("fHeight", &PlaceholderStyle::fHeight)
        .def_readwrite("fAlignment", &PlaceholderStyle::fAlignment)
        .def_readwrite("fBaseline", &PlaceholderStyle::fBaseline)
        .def_readwrite("fBaselineOffset", &PlaceholderStyle::fBaselineOffset)
        .def("__str__",
             [](const PlaceholderStyle &self)
             {
                 return "PlaceholderStyle(width={}, height={}, alignment={}, baseline={}, baselineOffset={})"_s.format(
                     self.fWidth, self.fHeight, self.fAlignment, self.fBaseline, self.fBaselineOffset);
             });

    py::class_<TextStyle>(m, "TextStyle")
        .def(py::init())
        .def(py::init<const TextStyle &>())
        .def(py::init(
                 [](const py::kwargs &kwargs)
                 {
                     std::unique_ptr<TextStyle> self = std::make_unique<TextStyle>();
                     for (auto item : kwargs)
                     {
                         std::string key(py::str(item.first));
                         auto value = item.second;
                         if (key == "color")
                             self->setColor(value.cast<SkColor>());
                         else if (key == "foregroundPaint")
                             self->setForegroundPaint(value.cast<SkPaint>());
                         else if (key == "backgroundPaint")
                             self->setBackgroundPaint(value.cast<SkPaint>());
                         else if (key == "decoration")
                             self->setDecoration(value.cast<TextDecoration>());
                         else if (key == "decorationMode")
                             self->setDecorationMode(value.cast<TextDecorationMode>());
                         else if (key == "decorationStyle")
                             self->setDecorationStyle(value.cast<TextDecorationStyle>());
                         else if (key == "decorationColor")
                             self->setDecorationColor(value.cast<SkColor>());
                         else if (key == "decorationThicknessMultiplier")
                             self->setDecorationThicknessMultiplier(value.cast<SkScalar>());
                         else if (key == "fontStyle")
                             self->setFontStyle(value.cast<SkFontStyle>());
                         else if (key == "shadows")
                             for (const TextShadow &shadow : value.cast<std::vector<TextShadow>>())
                                 self->addShadow(shadow);
                         else if (key == "fontArguments")
                             self->setFontArguments(value.cast<SkFontArguments>());
                         else if (key == "fontSize")
                             self->setFontSize(value.cast<SkScalar>());
                         else if (key == "fontFamilies")
                         {
                             const std::vector<std::string> &fontFamilies = value.cast<std::vector<std::string>>();
                             self->setFontFamilies(std::vector<SkString>(fontFamilies.begin(), fontFamilies.end()));
                         }
                         else if (key == "baselineShift")
                             self->setBaselineShift(value.cast<SkScalar>());
                         else if (key == "height")
                             self->setHeight(value.cast<SkScalar>());
                         else if (key == "heightOverride")
                             self->setHeightOverride(value.cast<bool>());
                         else if (key == "halfLeading")
                             self->setHalfLeading(value.cast<bool>());
                         else if (key == "letterSpacing")
                             self->setLetterSpacing(value.cast<SkScalar>());
                         else if (key == "wordSpacing")
                             self->setWordSpacing(value.cast<SkScalar>());
                         else if (key == "typeface")
                             self->setTypeface(value.cast<sk_sp<SkTypeface>>());
                         else if (key == "locale")
                             self->setLocale(SkString(value.cast<std::string>()));
                         else if (key == "textBaseline")
                             self->setTextBaseline(value.cast<TextBaseline>());
                         else if (key == "placeholder")
                         {
                             if (value.cast<bool>())
                                 self->setPlaceholder();
                         }
                         else
                             throw py::key_error(key);
                     }
                     return self;
                 }),
             R"doc(
                 Construct a new text style from keyword arguments. This creates a new :py:class:`TextStyle` object and
                 calls the respective setters for each keyword argument.

                 Supported keyword arguments: ``color``, ``foregroundPaint``, ``backgroundPaint``, ``decoration``,
                 ``decorationMode``, ``decorationStyle``, ``decorationColor``, ``decorationThicknessMultiplier``,
                 ``fontStyle``, ``shadows``, ``fontArguments``, ``fontSize``, ``fontFamilies``, ``baselineShift``,
                 ``height``, ``heightOverride``, ``halfLeading``, ``letterSpacing``, ``wordSpacing``, ``typeface``,
                 ``locale``, ``textBaseline``, ``placeholder``.
             )doc")
        .def("cloneForPlaceholder", &TextStyle::cloneForPlaceholder)
        .def("equals", &TextStyle::equals, "other"_a)
        .def("equalsByFonts", &TextStyle::equalsByFonts, "that"_a)
        .def("matchOneAttribute", &TextStyle::matchOneAttribute, "styleType"_a, "other"_a)
        .def(py::self == py::self)
        .def("getColor", &TextStyle::getColor)
        .def("setColor", &TextStyle::setColor, "color"_a)
        .def("hasForeground", &TextStyle::hasForeground)
        .def("getForeground", &TextStyle::getForeground)
        .def("setForegroundPaint", &TextStyle::setForegroundPaint, "paint"_a)
        .def("clearForegroundColor", &TextStyle::clearForegroundColor)
        .def("hasBackground", &TextStyle::hasBackground)
        .def("getBackground", &TextStyle::getBackground)
        .def("setBackgroundPaint", &TextStyle::setBackgroundPaint, "paint"_a)
        .def("clearBackgroundColor", &TextStyle::clearBackgroundColor)
        .def("getDecoration", &TextStyle::getDecoration)
        .def("getDecorationType", &TextStyle::getDecorationType)
        .def("getDecorationMode", &TextStyle::getDecorationMode)
        .def("getDecorationColor", &TextStyle::getDecorationColor)
        .def("getDecorationStyle", &TextStyle::getDecorationStyle)
        .def("getDecorationThicknessMultiplier", &TextStyle::getDecorationThicknessMultiplier)
        .def("setDecoration", &TextStyle::setDecoration, "decoration"_a)
        .def("setDecorationMode", &TextStyle::setDecorationMode, "mode"_a)
        .def("setDecorationStyle", &TextStyle::setDecorationStyle, "style"_a)
        .def("setDecorationColor", &TextStyle::setDecorationColor, "color"_a)
        .def("setDecorationThicknessMultiplier", &TextStyle::setDecorationThicknessMultiplier, "m"_a)
        .def("getFontStyle", &TextStyle::getFontStyle)
        .def("setFontStyle", &TextStyle::setFontStyle, "style"_a)
        .def("getShadowNumber", &TextStyle::getShadowNumber)
        .def("getShadows", &TextStyle::getShadows)
        .def("addShadow", &TextStyle::addShadow, "shadow"_a)
        .def("resetShadows", &TextStyle::resetShadows)
        .def("getFontFeatureNumber", &TextStyle::getFontFeatureNumber)
        .def("getFontFeatures", &TextStyle::getFontFeatures)
        .def(
            "addFontFeature",
            [](TextStyle &self, const std::string &fontFeature, const int &value)
            { self.addFontFeature(SkString(fontFeature), value); },
            "fontFeature"_a, "value"_a)
        .def("resetFontFeatures", &TextStyle::resetFontFeatures)
        .def("getFontArguments", &TextStyle::getFontArguments, py::return_value_policy::reference_internal)
        .def("setFontArguments", &TextStyle::setFontArguments, "args"_a)
        .def("getFontSize", &TextStyle::getFontSize)
        .def("setFontSize", &TextStyle::setFontSize, "size"_a)
        .def("getFontFamilies",
             [](const TextStyle &self)
             {
                 const std::vector<SkString> &fontFamilies = self.getFontFamilies();
                 py::list families;
                 for (const SkString &family : fontFamilies)
                     families.append(SkString2pyStr(family));
                 return families;
             })
        .def(
            "setFontFamilies",
            [](TextStyle &self, const std::vector<std::string> &families)
            { self.setFontFamilies(std::vector<SkString>(families.begin(), families.end())); },
            "families"_a)
        .def("getBaselineShift", &TextStyle::getBaselineShift)
        .def("setBaselineShift", &TextStyle::setBaselineShift, "shift"_a)
        .def("setHeight", &TextStyle::setHeight, "height"_a)
        .def("getHeight", &TextStyle::getHeight)
        .def("setHeightOverride", &TextStyle::setHeightOverride, "heightOverride"_a)
        .def("getHeightOverride", &TextStyle::getHeightOverride)
        .def("setHalfLeading", &TextStyle::setHalfLeading, "halfLeading"_a)
        .def("getHalfLeading", &TextStyle::getHalfLeading)
        .def("setLetterSpacing", &TextStyle::setLetterSpacing, "letterSpacing"_a)
        .def("getLetterSpacing", &TextStyle::getLetterSpacing)
        .def("setWordSpacing", &TextStyle::setWordSpacing, "wordSpacing"_a)
        .def("getWordSpacing", &TextStyle::getWordSpacing)
        .def("getTypeface", &TextStyle::getTypeface, py::return_value_policy::reference)
        .def("refTypeface", &TextStyle::refTypeface)
        .def("setTypeface", &TextStyle::setTypeface, "typeface"_a)
        .def("getLocale", [](const TextStyle &self) { return SkString2pyStr(self.getLocale()); })
        .def(
            "setLocale", [](TextStyle &self, const std::string &locale) { self.setLocale(SkString(locale)); },
            "locale"_a)
        .def("getTextBaseline", &TextStyle::getTextBaseline)
        .def("setTextBaseline", &TextStyle::setTextBaseline, "baseline"_a)
        .def(
            "getFontMetrics",
            [](const TextStyle &self)
            {
                SkFontMetrics metrics;
                self.getFontMetrics(&metrics);
                return metrics;
            },
            "Returns the font metrics for the current font.")
        .def("isPlaceholder", &TextStyle::isPlaceholder)
        .def("setPlaceholder", &TextStyle::setPlaceholder)
        .def(
            "__str__",
            [](const TextStyle &self)
            {
                const size_t shadowNumber = self.getShadowNumber(), fontFeatureNumber = self.getFontFeatureNumber();
                return "TextStyle(color={:x}{}{}, decoration={}, fontStyle={}, {} shadow{}, {} font feature{}, fontSize={}, baselineShift={}, height={}, heightOverride={}, halfLeading={}, letterSpacing={}, wordSpacing={}, typeface={}, locale={}, textBaseline={}{})"_s
                    .format(self.getColor(),
                            self.hasForeground() ? ", foreground={}"_s.format(self.getForeground()) : "",
                            self.hasBackground() ? ", background={}"_s.format(self.getBackground()) : "",
                            self.getDecoration(), self.getFontStyle(), shadowNumber, shadowNumber == 1 ? "" : "s",
                            fontFeatureNumber, fontFeatureNumber == 1 ? "" : "s", self.getFontSize(),
                            self.getBaselineShift(), self.getHeight(), self.getHeightOverride(), self.getHalfLeading(),
                            self.getLetterSpacing(), self.getWordSpacing(), self.getTypeface(),
                            SkString2pyStr(self.getLocale()), self.getTextBaseline(),
                            self.isPlaceholder() ? ", placeholder"_s : "");
            });

    py::class_<Block>(m, "Block")
        .def(py::init())
        .def(py::init<size_t, size_t, const TextStyle &>(), "start"_a, "end"_a, "style"_a)
        .def(py::init<TextRange, const TextStyle &>(), "range"_a, "style"_a)
        .def("add", &Block::add, "tail"_a)
        .def_readwrite("fRange", &Block::fRange)
        .def_readwrite("fStyle", &Block::fStyle)
        .def("__str__",
             [](const Block &self) { return "Block(range={}, style={})"_s.format(self.fRange, self.fStyle); });

    py::class_<Placeholder>(m, "Placeholder")
        .def(py::init())
        .def(py::init<size_t, size_t, const PlaceholderStyle &, const TextStyle &, BlockRange, TextRange>(), "start"_a,
             "end"_a, "style"_a, "textStyle"_a, "blocksBefore"_a, "textBefore"_a)
        .def_readwrite("fRange", &Placeholder::fRange)
        .def_readwrite("fStyle", &Placeholder::fStyle)
        .def_readwrite("fTextStyle", &Placeholder::fTextStyle)
        .def_readwrite("fBlocksBefore", &Placeholder::fBlocksBefore)
        .def_readwrite("fTextBefore", &Placeholder::fTextBefore)
        .def("__str__",
             [](const Placeholder &self)
             {
                 return "Placeholder(range={}, style={}, textStyle={}, blocksBefore={}, textBefore={})"_s.format(
                     self.fRange, self.fStyle, self.fTextStyle, self.fBlocksBefore, self.fTextBefore);
             });
}