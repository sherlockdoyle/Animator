#include "modules/skparagraph/include/ParagraphStyle.h"
#include "common.h"
#include <pybind11/operators.h>
#include <pybind11/stl.h>

using namespace skia::textlayout;

void initParagraphStyle(py::module &m)
{
    py::class_<StrutStyle, std::unique_ptr<StrutStyle>>(m, "StrutStyle")
        .def(py::init())
        .def(py::init(
                 [](const std::optional<const std::vector<std::string>> &fontFamilies,
                    const std::optional<const SkFontStyle> &fontStyle, const std::optional<const SkScalar> &fontSize,
                    const std::optional<const SkScalar> &height, const std::optional<const SkScalar> &leading,
                    const std::optional<const bool> &strutEnabled, const std::optional<const bool> &forceStrutHeight,
                    const std::optional<const bool> &heightOverride, const std::optional<const bool> &halfLeading)
                 {
                     std::unique_ptr<StrutStyle> self = std::make_unique<StrutStyle>();
                     if (fontFamilies)
                         self->setFontFamilies(std::vector<SkString>(fontFamilies->begin(), fontFamilies->end()));
                     if (fontStyle)
                         self->setFontStyle(*fontStyle);
                     if (fontSize)
                         self->setFontSize(*fontSize);
                     if (height)
                         self->setHeight(*height);
                     if (leading)
                         self->setLeading(*leading);
                     if (strutEnabled)
                         self->setStrutEnabled(*strutEnabled);
                     if (forceStrutHeight)
                         self->setForceStrutHeight(*forceStrutHeight);
                     if (heightOverride)
                         self->setHeightOverride(*heightOverride);
                     if (halfLeading)
                         self->setHalfLeading(*halfLeading);
                     return self;
                 }),
             R"doc(
                 Construct a new strut style from keyword arguments. This creates a new :py:class:`StrutStyle` object
                 and calls the respective setters for each keyword argument.
             )doc",
             "fontFamilies"_a = py::none(), "fontStyle"_a = py::none(), "fontSize"_a = py::none(),
             "height"_a = py::none(), "leading"_a = py::none(), "strutEnabled"_a = py::none(),
             "forceStrutHeight"_a = py::none(), "heightOverride"_a = py::none(), "halfLeading"_a = py::none())
        .def("getFontFamilies",
             [](const StrutStyle &self)
             {
                 const std::vector<SkString> &fontFamilies = self.getFontFamilies();
                 py::list families;
                 for (const SkString &family : fontFamilies)
                     families.append(SkString2pyStr(family));
                 return families;
             })
        .def(
            "setFontFamilies",
            [](StrutStyle &self, const std::vector<std::string> &families)
            { self.setFontFamilies(std::vector<SkString>(families.begin(), families.end())); },
            "families"_a)
        .def("getFontStyle", &StrutStyle::getFontStyle)
        .def("setFontStyle", &StrutStyle::setFontStyle, "fontStyle"_a)
        .def("getFontSize", &StrutStyle::getFontSize)
        .def("setFontSize", &StrutStyle::setFontSize, "size"_a)
        .def("setHeight", &StrutStyle::setHeight, "height"_a)
        .def("getHeight", &StrutStyle::getHeight)
        .def("setLeading", &StrutStyle::setLeading, "Leading"_a)
        .def("getLeading", &StrutStyle::getLeading)
        .def("getStrutEnabled", &StrutStyle::getStrutEnabled)
        .def("setStrutEnabled", &StrutStyle::setStrutEnabled, "v"_a)
        .def("getForceStrutHeight", &StrutStyle::getForceStrutHeight)
        .def("setForceStrutHeight", &StrutStyle::setForceStrutHeight, "v"_a)
        .def("getHeightOverride", &StrutStyle::getHeightOverride)
        .def("setHeightOverride", &StrutStyle::setHeightOverride, "v"_a)
        .def("setHalfLeading", &StrutStyle::setHalfLeading, "halfLeading"_a)
        .def("getHalfLeading", &StrutStyle::getHalfLeading)
        .def(py::self == py::self)
        .def("__str__",
             [](const StrutStyle &self)
             {
                 return "StrutStyle(fontStyle={}, fontSize={}, height={}, leading={}{}{}{}{})"_s.format(
                     self.getFontStyle(), self.getFontSize(), self.getHeight(), self.getLeading(),
                     self.getStrutEnabled() ? ", strut enabled" : "",
                     self.getForceStrutHeight() ? ", force strut height" : "",
                     self.getHeightOverride() ? ", height override" : "",
                     self.getHalfLeading() ? ", half leading" : "");
             });

    py::class_<ParagraphStyle>(m, "ParagraphStyle")
        .def(py::init())
        .def(py::init(
                 [](const std::optional<const StrutStyle> &strutStyle, const std::optional<const TextStyle> &textStyle,
                    const std::optional<const TextDirection> &textDirection,
                    const std::optional<const TextAlign> &textAlign, const std::optional<const size_t> &maxLines,
                    const std::optional<const std::string> &ellipsis, const std::optional<const SkScalar> &height,
                    const std::optional<const TextHeightBehavior> &textHeightBehavior,
                    const std::optional<const bool> &replaceTabCharacters,
                    const std::optional<const bool> &applyRoundingHack)
                 {
                     std::unique_ptr<ParagraphStyle> self = std::make_unique<ParagraphStyle>();
                     if (strutStyle)
                         self->setStrutStyle(*strutStyle);
                     if (textStyle)
                         self->setTextStyle(*textStyle);
                     if (textDirection)
                         self->setTextDirection(*textDirection);
                     if (textAlign)
                         self->setTextAlign(*textAlign);
                     if (maxLines)
                         self->setMaxLines(*maxLines);
                     if (ellipsis)
                         self->setEllipsis(SkString(*ellipsis));
                     if (height)
                         self->setHeight(*height);
                     if (textHeightBehavior)
                         self->setTextHeightBehavior(*textHeightBehavior);
                     if (replaceTabCharacters)
                         self->setReplaceTabCharacters(*replaceTabCharacters);
                     if (applyRoundingHack)
                         self->setApplyRoundingHack(*applyRoundingHack);
                     return self;
                 }),
             R"doc(
                 Construct a new paragraph style from keyword arguments. This creates a new :py:class:`ParagraphStyle`
                 object and calls the respective setters for each keyword argument.
             )doc",
             "strutStyle"_a = py::none(), "textStyle"_a = py::none(), "textDirection"_a = py::none(),
             "textAlign"_a = py::none(), "maxLines"_a = py::none(), "ellipsis"_a = py::none(), "height"_a = py::none(),
             "textHeightBehavior"_a = py::none(), "replaceTabCharacters"_a = py::none(),
             "applyRoundingHack"_a = py::none())
        .def(py::self == py::self)
        .def("getStrutStyle", &ParagraphStyle::getStrutStyle, py::return_value_policy::reference_internal)
        .def("setStrutStyle", &ParagraphStyle::setStrutStyle, "strutStyle"_a)
        .def("getTextStyle", &ParagraphStyle::getTextStyle, py::return_value_policy::reference_internal)
        .def("setTextStyle", &ParagraphStyle::setTextStyle, "textStyle"_a)
        .def("getTextDirection", &ParagraphStyle::getTextDirection)
        .def("setTextDirection", &ParagraphStyle::setTextDirection, "direction"_a)
        .def("getTextAlign", &ParagraphStyle::getTextAlign)
        .def("setTextAlign", &ParagraphStyle::setTextAlign, "align"_a)
        .def("getMaxLines", &ParagraphStyle::getMaxLines)
        .def("setMaxLines", &ParagraphStyle::setMaxLines, "maxLines"_a)
        .def("getEllipsis", [](const ParagraphStyle &self) { return SkString2pyStr(self.getEllipsis()); })
        .def("getEllipsisUtf16", &ParagraphStyle::getEllipsisUtf16)
        .def(
            "setEllipsis",
            [](ParagraphStyle &self, const std::string &ellipsis) { self.setEllipsis(SkString(ellipsis)); },
            "ellipsis"_a)
        .def("getHeight", &ParagraphStyle::getHeight)
        .def("setHeight", &ParagraphStyle::setHeight, "height"_a)
        .def("getTextHeightBehavior", &ParagraphStyle::getTextHeightBehavior)
        .def("setTextHeightBehavior", &ParagraphStyle::setTextHeightBehavior, "v"_a)
        .def("unlimited_lines", &ParagraphStyle::unlimited_lines)
        .def("ellipsized", &ParagraphStyle::ellipsized)
        .def("effective_align", &ParagraphStyle::effective_align)
        .def("hintingIsOn", &ParagraphStyle::hintingIsOn)
        .def("turnHintingOff", &ParagraphStyle::turnHintingOff)
        .def("getReplaceTabCharacters", &ParagraphStyle::getReplaceTabCharacters)
        .def("setReplaceTabCharacters", &ParagraphStyle::setReplaceTabCharacters, "value"_a)
        .def("getApplyRoundingHack", &ParagraphStyle::getApplyRoundingHack)
        .def("setApplyRoundingHack", &ParagraphStyle::setApplyRoundingHack, "value"_a)
        .def(
            "__str__",
            [](const ParagraphStyle &self)
            {
                return "ParagraphStyle(strutStyle={}, textStyle={}, textDirection={}, textAlign={}, maxLines={}, height={}, textHeightBehavior={}{}{}, effectiveAlign={}{}{}{})"_s
                    .format(self.getStrutStyle(), self.getTextStyle(), self.getTextDirection(), self.getTextAlign(),
                            self.getMaxLines(), self.getHeight(), self.getTextHeightBehavior(),
                            self.unlimited_lines() ? ", unlimited lines" : "",
                            self.ellipsized() ? ", ellipsized, ellipsis={}"_s.format(SkString2pyStr(self.getEllipsis()))
                                              : "",
                            self.effective_align(), self.hintingIsOn() ? ", hinting is on" : "",
                            self.getReplaceTabCharacters() ? ", replace tab characters" : "",
                            self.getApplyRoundingHack() ? ", apply rounding hack" : "");
            });
}