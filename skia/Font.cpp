#include "common.h"
#include "include/core/SkData.h"
#include "include/core/SkFont.h"
#include "include/core/SkFontMetrics.h"
#include "include/core/SkFontMgr.h"
#include "include/core/SkPaint.h"
#include "include/core/SkPath.h"
#include "include/core/SkStream.h"
#include "include/ports/SkFontMgr_data.h"
#include <optional>
#include <pybind11/iostream.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>

using CoordinateVector = std::vector<SkFontArguments::VariationPosition::Coordinate>;
PYBIND11_MAKE_OPAQUE(CoordinateVector);
void FontArguments_VariationPosition_coordinates(SkFontArguments::VariationPosition &vp,
                                                 const CoordinateVector &coordinates)
{
    vp.coordinates = coordinates.data();
    vp.coordinateCount = coordinates.size();
}

using OverrideVector = std::vector<SkFontArguments::Palette::Override>;
PYBIND11_MAKE_OPAQUE(OverrideVector);
void FontArguments_Palette_overrides(SkFontArguments::Palette &p, const OverrideVector &overrides)
{
    p.overrides = overrides.data();
    p.overrideCount = overrides.size();
}

sk_sp<SkTypeface> Typeface_MakeFromName(const std::optional<std::string> &familyName, const SkFontStyle &fontStyle)
{
    return SkTypeface::MakeFromName(familyName ? familyName->c_str() : nullptr, fontStyle);
}

py::tuple FontStyleSet_getStyle(SkFontStyleSet *self, int index)
{
    SkFontStyle style;
    SkString name;
    if (index < 0 || index >= self->count())
        throw py::index_error("Index out of range.");
    self->getStyle(index, &style, &name);
    return py::make_tuple(style, py::str(name.c_str(), name.size()));
}

py::str FontMgr_getFamilyName(const SkFontMgr &fontmgr, int index)
{
    SkString familyName;
    if (index < 0 || index >= fontmgr.countFamilies())
        throw py::index_error("Index out of range.");
    fontmgr.getFamilyName(index, &familyName);
    return SkString2pyStr(familyName);
}

void initFont(py::module &m)
{
    py::class_<SkFontStyle> FontStyle(m, "FontStyle");
    py::enum_<SkFontStyle::Weight>(FontStyle, "Weight")
        .value("kInvisible_Weight", SkFontStyle::Weight::kInvisible_Weight)
        .value("kThin_Weight", SkFontStyle::Weight::kThin_Weight)
        .value("kExtraLight_Weight", SkFontStyle::Weight::kExtraLight_Weight)
        .value("kLight_Weight", SkFontStyle::Weight::kLight_Weight)
        .value("kNormal_Weight", SkFontStyle::Weight::kNormal_Weight)
        .value("kMedium_Weight", SkFontStyle::Weight::kMedium_Weight)
        .value("kSemiBold_Weight", SkFontStyle::Weight::kSemiBold_Weight)
        .value("kBold_Weight", SkFontStyle::Weight::kBold_Weight)
        .value("kExtraBold_Weight", SkFontStyle::Weight::kExtraBold_Weight)
        .value("kBlack_Weight", SkFontStyle::Weight::kBlack_Weight)
        .value("kExtraBlack_Weight", SkFontStyle::Weight::kExtraBlack_Weight);
    py::enum_<SkFontStyle::Width>(FontStyle, "Width")
        .value("kUltraCondensed_Width", SkFontStyle::Width::kUltraCondensed_Width)
        .value("kExtraCondensed_Width", SkFontStyle::Width::kExtraCondensed_Width)
        .value("kCondensed_Width", SkFontStyle::Width::kCondensed_Width)
        .value("kSemiCondensed_Width", SkFontStyle::Width::kSemiCondensed_Width)
        .value("kNormal_Width", SkFontStyle::Width::kNormal_Width)
        .value("kSemiExpanded_Width", SkFontStyle::Width::kSemiExpanded_Width)
        .value("kExpanded_Width", SkFontStyle::Width::kExpanded_Width)
        .value("kExtraExpanded_Width", SkFontStyle::Width::kExtraExpanded_Width)
        .value("kUltraExpanded_Width", SkFontStyle::Width::kUltraExpanded_Width);
    py::enum_<SkFontStyle::Slant>(FontStyle, "Slant")
        .value("kUpright_Slant", SkFontStyle::Slant::kUpright_Slant)
        .value("kItalic_Slant", SkFontStyle::Slant::kItalic_Slant)
        .value("kOblique_Slant", SkFontStyle::Slant::kOblique_Slant);
    FontStyle
        .def(py::init<int, int, SkFontStyle::Slant>(), "weight"_a = SkFontStyle::Weight::kNormal_Weight,
             "width"_a = SkFontStyle::Width::kNormal_Width, "slant"_a = SkFontStyle::Slant::kUpright_Slant)
        .def(py::init<>())
        .def(py::self == py::self)
        .def("weight", &SkFontStyle::weight)
        .def("width", &SkFontStyle::width)
        .def("slant", &SkFontStyle::slant)
        .def_static("Normal", &SkFontStyle::Normal)
        .def_static("Bold", &SkFontStyle::Bold)
        .def_static("Italic", &SkFontStyle::Italic)
        .def_static("BoldItalic", &SkFontStyle::BoldItalic)
        .def("__str__",
             [](const SkFontStyle &self) {
                 return "FontStyle(weight={}, width={}, slant={})"_s.format(self.weight(), self.width(), self.slant());
             });

    py::class_<SkFontArguments> FontArguments(m, "FontArguments");

    py::class_<SkFontArguments::VariationPosition> VariationPosition(FontArguments, "VariationPosition");
    py::class_<SkFontArguments::VariationPosition::Coordinate>(VariationPosition, "Coordinate")
        .def(py::init(
                 [](const SkFourByteTag &axis, const float &value) -> SkFontArguments::VariationPosition::Coordinate {
                     return {axis, value};
                 }),
             "axis"_a, "value"_a)
        .def_readwrite("axis", &SkFontArguments::VariationPosition::Coordinate::axis)
        .def_readwrite("value", &SkFontArguments::VariationPosition::Coordinate::value)
        .def("__str__", [](const SkFontArguments::VariationPosition::Coordinate &self)
             { return "Coordinate(axis={:x}, value={})"_s.format(self.axis, self.value); });
    py::bind_vector<CoordinateVector>(VariationPosition, "CoordinateVector");
    VariationPosition
        .def(py::init(
                 [](const CoordinateVector &coordinates)
                 {
                     SkFontArguments::VariationPosition vp;
                     FontArguments_VariationPosition_coordinates(vp, coordinates);
                     return vp;
                 }),
             "coordinates"_a)
        .def_property(
            "coordinates",
            [](const SkFontArguments::VariationPosition &self)
            { return CoordinateVector(self.coordinates, self.coordinates + self.coordinateCount); },
            &FontArguments_VariationPosition_coordinates)
        .def_readonly("coordinateCount", &SkFontArguments::VariationPosition::coordinateCount)
        .def("__str__",
             [](const SkFontArguments::VariationPosition &self) {
                 return "VariationPosition({} coordinate{})"_s.format(self.coordinateCount,
                                                                      self.coordinateCount == 1 ? "" : "s");
             });

    py::class_<SkFontArguments::Palette> Palette(FontArguments, "Palette");
    py::class_<SkFontArguments::Palette::Override>(Palette, "Override")
        .def(py::init(
                 [](const int &index, const SkColor &color) -> SkFontArguments::Palette::Override {
                     return {index, color};
                 }),
             "index"_a, "color"_a)
        .def_readwrite("index", &SkFontArguments::Palette::Override::index)
        .def_readwrite("color", &SkFontArguments::Palette::Override::color)
        .def("__str__", [](const SkFontArguments::Palette::Override &self)
             { return "Override(index={}, color={:x})"_s.format(self.index, self.color); });
    py::bind_vector<OverrideVector>(Palette, "OverrideVector");
    Palette
        .def(py::init(
                 [](const int &index, const OverrideVector &overrides)
                 {
                     SkFontArguments::Palette p;
                     p.index = index;
                     FontArguments_Palette_overrides(p, overrides);
                     return p;
                 }),
             "index"_a, "overrides"_a)
        .def_readwrite("index", &SkFontArguments::Palette::index)
        .def_property(
            "overrides",
            [](const SkFontArguments::Palette &self)
            { return OverrideVector(self.overrides, self.overrides + self.overrideCount); },
            &FontArguments_Palette_overrides)
        .def_readonly("overrideCount", &SkFontArguments::Palette::overrideCount)
        .def("__str__",
             [](const SkFontArguments::Palette &self)
             {
                 return "Palette(index={}, {} override{})"_s.format(self.index, self.overrideCount,
                                                                    self.overrideCount == 1 ? "" : "s");
             });

    FontArguments.def(py::init())
        .def("setCollectionIndex", &SkFontArguments::setCollectionIndex, "collectionIndex"_a)
        .def("setVariationDesignPosition", &SkFontArguments::setVariationDesignPosition, "position"_a)
        .def("getCollectionIndex", &SkFontArguments::getCollectionIndex)
        .def("getVariationDesignPosition", &SkFontArguments::getVariationDesignPosition)
        .def("setPalette", &SkFontArguments::setPalette, "palette"_a)
        .def("getPalette", &SkFontArguments::getPalette);

    py::class_<SkFontParameters> FontParameters(m, "FontParameters");
    py::class_<SkFontParameters::Variation> Variation(FontParameters, "Variation");
    py::class_<SkFontParameters::Variation::Axis>(Variation, "Axis")
        .def(py::init())
        .def(py::init<SkFourByteTag, float, float, float, bool>())
        .def_readwrite("tag", &SkFontParameters::Variation::Axis::tag)
        .def_readwrite("min", &SkFontParameters::Variation::Axis::min)
        .def_readwrite("def_", &SkFontParameters::Variation::Axis::def)
        .def_readwrite("max", &SkFontParameters::Variation::Axis::max)
        .def("isHidden", &SkFontParameters::Variation::Axis::isHidden)
        .def("setHidden", &SkFontParameters::Variation::Axis::setHidden, "hidden"_a)
        .def("__str__",
             [](const SkFontParameters::Variation::Axis &self)
             {
                 return "Axis(tag={:x}, min={}, def={}, max={}{})"_s.format(self.tag, self.min, self.def, self.max,
                                                                            self.isHidden() ? ", hidden" : "");
             });

    py::enum_<SkTextEncoding>(m, "TextEncoding")
        .value("kUTF8", SkTextEncoding::kUTF8)
        .value("kUTF16", SkTextEncoding::kUTF16)
        .value("kUTF32", SkTextEncoding::kUTF32)
        .value("kGlyphID", SkTextEncoding::kGlyphID);
    py::enum_<SkFontHinting>(m, "FontHinting")
        .value("kNone", SkFontHinting::kNone)
        .value("kSlight", SkFontHinting::kSlight)
        .value("kNormal", SkFontHinting::kNormal)
        .value("kFull", SkFontHinting::kFull);

    py::class_<SkTypeface, sk_sp<SkTypeface>> Typeface(m, "Typeface");
    Typeface.def("fontStyle", &SkTypeface::fontStyle)
        .def("isBold", &SkTypeface::isBold)
        .def("isItalic", &SkTypeface::isItalic)
        .def("isFixedPitch", &SkTypeface::isFixedPitch)
        .def(
            "getVariationDesignPosition",
            [](const SkTypeface &self)
            {
                int coordinateCount = self.getVariationDesignPosition(nullptr, 0);
                if (coordinateCount == -1)
                    throw std::runtime_error("Failed to get number of axes.");
                CoordinateVector coordinates(coordinateCount);
                if (self.getVariationDesignPosition(coordinates.data(), coordinates.size()) == -1)
                    throw std::runtime_error("Failed to get positions.");
                return coordinates;
            },
            "Returns the design variation coordinates.")
        .def(
            "getVariationDesignParameters",
            [](const SkTypeface &self)
            {
                int parameterCount = self.getVariationDesignParameters(nullptr, 0);
                if (parameterCount == -1)
                    throw std::runtime_error("Failed to get number of axes.");
                std::vector<SkFontParameters::Variation::Axis> parameters(parameterCount);
                if (self.getVariationDesignParameters(parameters.data(), parameters.size()) == -1)
                    throw std::runtime_error("Failed to get parameters.");
                return parameters;
            },
            "Returns the design variation parameters.")
        .def("uniqueID", &SkTypeface::uniqueID)
        .def_static("UniqueID", &SkTypeface::UniqueID, "face"_a)
        .def_static("Equal", &SkTypeface::Equal, "facea"_a, "faceb"_a)
        .def("__eq__", &SkTypeface::Equal, py::is_operator())
        .def_static("MakeDefault", &SkTypeface::MakeDefault)
        .def(py::init(&SkTypeface::MakeDefault), "Returns the default normal typeface.")
        .def_static("MakeFromName", &Typeface_MakeFromName, "familyName"_a, "fontStyle"_a = SkFontStyle())
        .def(
            py::init(&Typeface_MakeFromName),
            "Creates a new reference to the typeface that most closely matches the requested familyName and fontStyle.",
            "familyName"_a, "fontStyle"_a = SkFontStyle())
        .def_static(
            "MakeFromFile",
            [](const std::string &path, const int &index) { return SkTypeface::MakeFromFile(path.c_str(), index); },
            "path"_a, "index"_a = 0)
        .def_static("MakeFromData", &SkTypeface::MakeFromData, "data"_a, "index"_a = 0)
        .def("makeClone", &SkTypeface::makeClone, "fontArguments"_a);
    py::enum_<SkTypeface::SerializeBehavior>(Typeface, "SerializeBehavior")
        .value("kDoIncludeData", SkTypeface::SerializeBehavior::kDoIncludeData)
        .value("kDontIncludeData", SkTypeface::SerializeBehavior::kDontIncludeData)
        .value("kIncludeDataIfLocal", SkTypeface::SerializeBehavior::kIncludeDataIfLocal);
    Typeface
        .def("serialize", py::overload_cast<SkTypeface::SerializeBehavior>(&SkTypeface::serialize, py::const_),
             "behavior"_a = SkTypeface::SerializeBehavior::kIncludeDataIfLocal)
        .def_static(
            "MakeDeserialize",
            [](const sk_sp<SkData> &data)
            {
                SkMemoryStream stream(data);
                return SkTypeface::MakeDeserialize(&stream);
            },
            R"doc(
                Given the data previously written by :py:meth:`serialize`, return a new instance of a typeface referring
                to the same font.
            )doc",
            "data"_a)
        .def(
            "unicharsToGlyphs",
            [](const SkTypeface &self, const std::vector<SkUnichar> &uni)
            {
                std::vector<SkGlyphID> glyphs(uni.size());
                self.unicharsToGlyphs(uni.data(), uni.size(), glyphs.data());
                return glyphs;
            },
            R"doc(
                Given an array of UTF32 character codes, return their corresponding glyph IDs.

                :param chars: the array of UTF32 chars.
                :return: the corresponding glyph IDs for each character.
            )doc",
            "uni"_a)
        .def(
            "textToGlyphs",
            [](const SkTypeface &self, const std::string &text, const SkTextEncoding &encoding)
            {
                int maxGlyphCount = self.textToGlyphs(text.c_str(), text.size(), encoding, nullptr, 0);
                std::vector<SkGlyphID> glyphs(maxGlyphCount);
                self.textToGlyphs(text.c_str(), text.size(), encoding, glyphs.data(), glyphs.size());
                return glyphs;
            },
            R"doc(
                Given a string, return its corresponding glyph IDs.

                :param text: the text string.
                :param encoding: the text encoding.
                :return: the corresponding glyph IDs for each character.
            )doc",
            "text"_a, "encoding"_a = SkTextEncoding::kUTF8)
        .def("unicharToGlyph", &SkTypeface::unicharToGlyph, "unichar"_a)
        .def("countGlyphs", &SkTypeface::countGlyphs)
        .def("countTables", &SkTypeface::countTables)
        .def(
            "getTableTags",
            [](const SkTypeface &self)
            {
                int tableCount = self.countTables();
                std::vector<SkFontTableTag> tags(tableCount);
                if (self.getTableTags(tags.data()) != tableCount)
                    throw std::runtime_error("Failed to get table tags.");
                return tags;
            },
            "Returns the list of table tags in the font.")
        .def("getTableSize", &SkTypeface::getTableSize, "tag"_a)
        .def(
            "getTableData",
            [](const SkTypeface &self, const SkFontTableTag &tag, const size_t &offset, const int &length)
            {
                size_t tableSize = self.getTableSize(tag);
                if (offset > tableSize)
                    throw py::value_error("Offset is out of range.");
                size_t numBytes = length < 0 ? tableSize - offset : std::min((size_t)length, tableSize - offset);
                std::vector<char> data(numBytes);
                if (self.getTableData(tag, offset, numBytes, data.data()) == 0)
                    throw py::value_error("Not a valid tag.");
                return py::bytes(data.data(), numBytes);
            },
            R"doc(
                Returns the contents of a table.

                :param tag: The table tag whose contents are to be copied.
                :param offset: The offset into the table at which to start copying.
                :param length: The number of bytes to copy. If this is negative, the entire table is copied.
                :return: table contents
            )doc",
            "tag"_a, "offset"_a = 0, "length"_a = -1)
        .def("copyTableData", &SkTypeface::copyTableData, "tag"_a)
        .def("getUnitsPerEm", &SkTypeface::getUnitsPerEm)
        .def(
            "getKerningPairAdjustments",
            [](const SkTypeface &self, const std::vector<SkGlyphID> &glyphs) -> std::optional<std::vector<int32_t>>
            {
                std::vector<int32_t> adjustments(glyphs.size() - 1);
                if (self.getKerningPairAdjustments(glyphs.data(), glyphs.size(), adjustments.data()))
                    return adjustments;
                return std::nullopt;
            },
            "Given a run of *glyphs*, return the associated horizontal adjustments.", "glyphs"_a);
    py::class_<SkTypeface::LocalizedStrings>(Typeface, "LocalizedStrings")
        .def(
            "__iter__", [](const SkTypeface::LocalizedStrings *self) { return self; }, py::keep_alive<0, 1>())
        .def("__next__",
             [](SkTypeface::LocalizedStrings &self)
             {
                 SkTypeface::LocalizedString localizedString;
                 if (self.next(&localizedString))
                     return py::make_tuple(
                         py::str(localizedString.fString.c_str(), localizedString.fString.size()),
                         py::str(localizedString.fLanguage.c_str(), localizedString.fLanguage.size()));
                 self.unref();
                 throw py::stop_iteration();
             });
    Typeface
        .def("createFamilyNameIterator", &SkTypeface::createFamilyNameIterator,
             R"doc(
                Returns an iterator which returns tuple of (family name, language) specified by the font.

                :warning: Please use :py:meth:`~Typeface.getFamilyNames` instead which returns a list instead of
                    an iterator. There's probably a memory leak in this method, but I don't know how to fix it.
            )doc")
        .def(
            "getFamilyNames",
            [](const SkTypeface &self)
            {
                SkTypeface::LocalizedStrings *it = self.createFamilyNameIterator();
                if (!it)
                    throw std::runtime_error("Failed to create family name iterator.");
                py::list results;
                SkTypeface::LocalizedString name;
                while (it->next(&name))
                    results.append(py::make_tuple(py::str(name.fString.c_str(), name.fString.size()),
                                                  py::str(name.fLanguage.c_str(), name.fLanguage.size())));
                it->unref();
                return results;
            },
            "Returns a list of tuple of (family name, language) specified by the font.")
        .def(
            "getFamilyName",
            [](const SkTypeface &self)
            {
                SkString name;
                self.getFamilyName(&name);
                return py::str(name.c_str(), name.size());
            },
            "Returns the family name for this typeface.")
        .def(
            "getPostScriptName",
            [](const SkTypeface &self)
            {
                SkString name;
                self.getPostScriptName(&name);
                return py::str(name.c_str(), name.size());
            },
            "Returns the PostScript name for this typeface.")
        .def("getBounds", &SkTypeface::getBounds)
        .def("__str__",
             [](const SkTypeface &self)
             {
                 SkString name;
                 self.getFamilyName(&name);
                 return "Typeface('{}', {})"_s.format(name.c_str(), self.fontStyle());
             });

    py::class_<SkFontMetrics> FontMetrics(m, "FontMetrics");
    FontMetrics.def(py::init()).def("__eq__", &SkFontMetrics::operator==, py::is_operator(), "other"_a);
    py::enum_<SkFontMetrics::FontMetricsFlags>(FontMetrics, "FontMetricsFlags", py::arithmetic())
        .value("kUnderlineThicknessIsValid_Flag", SkFontMetrics::FontMetricsFlags::kUnderlineThicknessIsValid_Flag)
        .value("kUnderlinePositionIsValid_Flag", SkFontMetrics::FontMetricsFlags::kUnderlinePositionIsValid_Flag)
        .value("kStrikeoutThicknessIsValid_Flag", SkFontMetrics::FontMetricsFlags::kStrikeoutThicknessIsValid_Flag)
        .value("kStrikeoutPositionIsValid_Flag", SkFontMetrics::FontMetricsFlags::kStrikeoutPositionIsValid_Flag)
        .value("kBoundsInvalid_Flag", SkFontMetrics::FontMetricsFlags::kBoundsInvalid_Flag);
    FontMetrics.def_readwrite("fFlags", &SkFontMetrics::fFlags)
        .def_readwrite("fTop", &SkFontMetrics::fTop)
        .def_readwrite("fAscent", &SkFontMetrics::fAscent)
        .def_readwrite("fDescent", &SkFontMetrics::fDescent)
        .def_readwrite("fBottom", &SkFontMetrics::fBottom)
        .def_readwrite("fLeading", &SkFontMetrics::fLeading)
        .def_readwrite("fAvgCharWidth", &SkFontMetrics::fAvgCharWidth)
        .def_readwrite("fMaxCharWidth", &SkFontMetrics::fMaxCharWidth)
        .def_readwrite("fXMin", &SkFontMetrics::fXMin)
        .def_readwrite("fXMax", &SkFontMetrics::fXMax)
        .def_readwrite("fXHeight", &SkFontMetrics::fXHeight)
        .def_readwrite("fCapHeight", &SkFontMetrics::fCapHeight)
        .def_readwrite("fUnderlineThickness", &SkFontMetrics::fUnderlineThickness)
        .def_readwrite("fUnderlinePosition", &SkFontMetrics::fUnderlinePosition)
        .def_readwrite("fStrikeoutThickness", &SkFontMetrics::fStrikeoutThickness)
        .def_readwrite("fStrikeoutPosition", &SkFontMetrics::fStrikeoutPosition)
        .def(
            "hasUnderlineThickness",
            [](const SkFontMetrics &self) -> std::optional<SkScalar>
            {
                SkScalar thickness;
                if (self.hasUnderlineThickness(&thickness))
                    return thickness;
                return std::nullopt;
            },
            "Returns the underline thickness if it is valid, otherwise ``None``.")
        .def(
            "hasUnderlinePosition",
            [](const SkFontMetrics &self) -> std::optional<SkScalar>
            {
                SkScalar position;
                if (self.hasUnderlinePosition(&position))
                    return position;
                return std::nullopt;
            },
            "Returns the underline position if it is valid, otherwise ``None``.")
        .def(
            "hasStrikeoutThickness",
            [](const SkFontMetrics &self) -> std::optional<SkScalar>
            {
                SkScalar thickness;
                if (self.hasStrikeoutThickness(&thickness))
                    return thickness;
                return std::nullopt;
            },
            "Returns the strikeout thickness if it is valid, otherwise ``None``.")
        .def(
            "hasStrikeoutPosition",
            [](const SkFontMetrics &self) -> std::optional<SkScalar>
            {
                SkScalar position;
                if (self.hasStrikeoutPosition(&position))
                    return position;
                return std::nullopt;
            },
            "Returns the strikeout position if it is valid, otherwise ``None``.")
        .def("hasBounds", &SkFontMetrics::hasBounds)
        .def("__str__",
             [](const SkFontMetrics &self)
             {
                 std::stringstream s;
                 s << "FontMetrics("
                   << "flags=" << self.fFlags << ", "
                   << "top=" << self.fTop << ", "
                   << "ascent=" << self.fAscent << ", "
                   << "descent=" << self.fDescent << ", "
                   << "bottom=" << self.fBottom << ", "
                   << "leading=" << self.fLeading << ", "
                   << "avgCharWidth=" << self.fAvgCharWidth << ", "
                   << "maxCharWidth=" << self.fMaxCharWidth << ", "
                   << "xMin=" << self.fXMin << ", "
                   << "xMax=" << self.fXMax << ", "
                   << "xHeight=" << self.fXHeight << ", "
                   << "capHeight=" << self.fCapHeight << ", "
                   << "underlineThickness=" << self.fUnderlineThickness << ", "
                   << "underlinePosition=" << self.fUnderlinePosition << ", "
                   << "strikeoutThickness=" << self.fStrikeoutThickness << ", "
                   << "strikeoutPosition=" << self.fStrikeoutPosition << ")";
                 return s.str();
             });

    py::class_<SkFont> Font(m, "Font");
    py::enum_<SkFont::Edging>(Font, "Edging")
        .value("kAlias", SkFont::Edging::kAlias)
        .value("kAntiAlias", SkFont::Edging::kAntiAlias)
        .value("kSubpixelAntiAlias", SkFont::Edging::kSubpixelAntiAlias);
    Font.def(py::init())
        .def(py::init<sk_sp<SkTypeface>, SkScalar>(), "typeface"_a, "size"_a)
        .def(py::init<sk_sp<SkTypeface>>(), "typeface"_a)
        .def(py::init<sk_sp<SkTypeface>, SkScalar, SkScalar, SkScalar>(), "typeface"_a, "size"_a, "scaleX"_a, "skewX"_a)
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def("isForceAutoHinting", &SkFont::isForceAutoHinting)
        .def("isEmbeddedBitmaps", &SkFont::isEmbeddedBitmaps)
        .def("isSubpixel", &SkFont::isSubpixel)
        .def("isLinearMetrics", &SkFont::isLinearMetrics)
        .def("isEmbolden", &SkFont::isEmbolden)
        .def("isBaselineSnap", &SkFont::isBaselineSnap)
        .def("setForceAutoHinting", &SkFont::setForceAutoHinting, "forceAutoHinting"_a)
        .def("setEmbeddedBitmaps", &SkFont::setEmbeddedBitmaps, "embeddedBitmaps"_a)
        .def("setSubpixel", &SkFont::setSubpixel, "subpixel"_a)
        .def("setLinearMetrics", &SkFont::setLinearMetrics, "linearMetrics"_a)
        .def("setEmbolden", &SkFont::setEmbolden, "embolden"_a)
        .def("setBaselineSnap", &SkFont::setBaselineSnap, "baselineSnap"_a)
        .def("getEdging", &SkFont::getEdging)
        .def("setEdging", &SkFont::setEdging, "edging"_a)
        .def("setHinting", &SkFont::setHinting, "hintingLevel"_a)
        .def("getHinting", &SkFont::getHinting)
        .def("makeWithSize", &SkFont::makeWithSize, "size"_a)
        .def("getTypeface", &SkFont::getTypeface, py::return_value_policy::reference)
        .def("getTypefaceOrDefault", &SkFont::getTypefaceOrDefault, py::return_value_policy::reference)
        .def("getSize", &SkFont::getSize)
        .def("getScaleX", &SkFont::getScaleX)
        .def("getSkewX", &SkFont::getSkewX)
        .def("refTypeface", &SkFont::refTypeface)
        .def("refTypefaceOrDefault", &SkFont::refTypefaceOrDefault)
        .def("setTypeface", &SkFont::setTypeface, "tf"_a)
        .def("setSize", &SkFont::setSize, "textSize"_a)
        .def("setScaleX", &SkFont::setScaleX, "scaleX"_a)
        .def("setSkewX", &SkFont::setSkewX, "skewX"_a)
        .def(
            "textToGlyphs",
            [](const SkFont &self, const std::string &text, const SkTextEncoding &encoding)
            {
                int numGlyphs = self.textToGlyphs(text.c_str(), text.size(), encoding, nullptr, 0);
                std::vector<SkGlyphID> glyphs(numGlyphs);
                self.textToGlyphs(text.c_str(), text.size(), encoding, glyphs.data(), numGlyphs);
                return glyphs;
            },
            "Converts text into glyph indices and returns them.", "text"_a, "encoding"_a = SkTextEncoding::kUTF8)
        .def("unicharToGlyph", &SkFont::unicharToGlyph, "uni"_a)
        .def(
            "unicharsToGlyphs",
            [](const SkFont &self, const std::vector<SkUnichar> &uni)
            {
                std::vector<SkGlyphID> glyphs(uni.size());
                self.unicharsToGlyphs(uni.data(), uni.size(), glyphs.data());
                return glyphs;
            },
            "uni"_a)
        .def(
            "countText",
            [](const SkFont &self, const std::string &text, const SkTextEncoding &encoding)
            { return self.countText(text.c_str(), text.size(), encoding); },
            "Returns number of glyphs represented by text.", "text"_a, "encoding"_a = SkTextEncoding::kUTF8)
        .def(
            "measureText",
            [](const SkFont &self, const std::string &text, const SkTextEncoding &encoding, const SkPaint *paint)
            {
                SkRect bounds;
                SkScalar width = self.measureText(text.c_str(), text.size(), encoding, &bounds, paint);
                return py::make_tuple(width, bounds);
            },
            R"doc(
                Returns a tuple of (advance width of text, bounding box relative to (0, 0)).

                :param text: The text to measure.
                :param encoding: The encoding of the text.
                :param paint: The paint to use for the text.
                :rtpye: Tuple[float, :py:class:`Rect`]
            )doc",
            "text"_a, "encoding"_a = SkTextEncoding::kUTF8, "paint"_a = py::none())
        .def(
            "getWidths",
            [](const SkFont &self, const std::vector<SkGlyphID> &glyphs)
            {
                std::vector<SkScalar> width(glyphs.size());
                self.getWidths(glyphs.data(), glyphs.size(), width.data());
                return width;
            },
            "Returns the advance for each glyph in *glyphs*.", "glyphs"_a)
        .def(
            "getWidthsBounds",
            [](const SkFont &self, const std::vector<SkGlyphID> &glyphs, const SkPaint *paint)
            {
                std::vector<SkScalar> width(glyphs.size());
                std::vector<SkRect> bounds(glyphs.size());
                self.getWidthsBounds(glyphs.data(), glyphs.size(), width.data(), bounds.data(), paint);
                return py::make_tuple(width, bounds);
            },
            R"doc(
                Returns the advance and bounds for each glyph in *glyphs* with optional *paint*.

                :rtpye: Tuple[List[float], List[:py:class:`Rect`]]
            )doc",
            "glyphs"_a, "paint"_a = py::none())
        .def(
            "getBounds",
            [](const SkFont &self, const std::vector<SkGlyphID> &glyphs, const SkPaint *paint)
            {
                std::vector<SkRect> bounds(glyphs.size());
                self.getBounds(glyphs.data(), glyphs.size(), bounds.data(), paint);
                return bounds;
            },
            "Returns the bounds for each glyph in *glyphs* with optional *paint*.", "glyphs"_a, "paint"_a = nullptr)
        .def(
            "getPos",
            [](const SkFont &self, const std::vector<SkGlyphID> &glyphs, const SkPoint &origin)
            {
                std::vector<SkPoint> pos(glyphs.size());
                self.getPos(glyphs.data(), glyphs.size(), pos.data(), origin);
                return pos;
            },
            "Returns the positions for each glyph, beginning at the specified *origin*.", "glyphs"_a,
            "origin"_a = SkPoint::Make(0, 0))
        .def(
            "getXPos",
            [](const SkFont &self, const std::vector<SkGlyphID> &glyphs, const SkScalar &origin)
            {
                std::vector<SkScalar> xpos(glyphs.size());
                self.getXPos(glyphs.data(), glyphs.size(), xpos.data(), origin);
                return xpos;
            },
            "Returns the x-positions for each glyph, beginning at the specified *origin*.", "glyphs"_a, "origin"_a = 0)
        .def(
            "getIntercepts",
            [](const SkFont &self, const std::vector<SkGlyphID> &glyphs, const std::vector<SkPoint> &pos,
               const SkScalar &top, const SkScalar &bottom, const SkPaint *paint)
            {
                std::size_t count = glyphs.size();
                if (count != pos.size())
                    throw py::value_error("glyphs and pos must have the same size.");
                return self.getIntercepts(glyphs.data(), count, pos.data(), top, bottom, paint);
            },
            "Returns intervals [start, end] describing lines parallel to the advance that intersect with the *glyphs*.",
            "glyphs"_a, "pos"_a, "top"_a, "bottom"_a, "paint"_a = py::none())
        .def(
            "getPath",
            [](const SkFont &self, const SkGlyphID &glyphID) -> std::optional<SkPath>
            {
                SkPath path;
                if (self.getPath(glyphID, &path))
                    return path;
                return std::nullopt;
            },
            R"doc(
                Returns path to be the outline of the glyph or None if the glyph has no outline.

                :rtpye: :py:class:`Path` | None
            )doc",
            "glyphID"_a)
        .def(
            "getPaths",
            [](const SkFont &self, const std::vector<SkGlyphID> &glyphIDs)
            {
                py::list paths;
                self.getPaths(
                    glyphIDs.data(), glyphIDs.size(),
                    [](const SkPath *pathOrNull, const SkMatrix &mx, void *ctx)
                    {
                        py::list *paths = static_cast<py::list *>(ctx);
                        if (pathOrNull)
                        {
                            SkPath path;
                            pathOrNull->transform(mx, &path);
                            paths->append(path);
                        }
                        else
                            paths->append(py::none());
                    },
                    &paths);
                return paths;
            },
            R"doc(
                Returns a list of paths to be the outlines of the glyphs. Some elements may be None if the glyph has no
                outline.
            )doc",
            "glyphIDs"_a)
        .def(
            "getMetrics",
            [](const SkFont &self)
            {
                SkFontMetrics metrics;
                SkScalar spacing = self.getMetrics(&metrics);
                return py::make_tuple(metrics, spacing);
            },
            R"doc(
                Returns a tuple of (font metrics, line spacing).

                :rtype: Tuple[FontMetrics, float]
            )doc")
        .def("getSpacing", &SkFont::getSpacing)
        .def("dump",
             [](const SkFont &self)
             {
                 py::scoped_ostream_redirect stream;
                 self.dump();
             })
        .def_property_readonly_static(
            "defaultSize",
            [](py::object)
            {
                static SkScalar size = SkFont().getSize();
                return size;
            },
            "The default font size used internally.")
        .def("__str__",
             [](const SkFont &self)
             {
                 return "Font({}, size={:g}, scale={:g}, skew={:g})"_s.format(
                     self.getTypefaceOrDefault(), self.getSize(), self.getScaleX(), self.getSkewX());
             });

    py::class_<SkFontStyleSet, sk_sp<SkFontStyleSet>>(m, "FontStyleSet")
        .def("count", &SkFontStyleSet::count)
        .def("__len__", &SkFontStyleSet::count)
        .def("getStyle", &FontStyleSet_getStyle, "Return a tuple of (font style, style name) for the given *index*.",
             "index"_a)
        .def("__getitem__", &FontStyleSet_getStyle, "Same as :py:meth:`getStyle`.", "index"_a)
        .def("createTypeface", &SkFontStyleSet::createTypeface, "index"_a)
        .def("matchStyle", &SkFontStyleSet::matchStyle, "pattern"_a)
        .def_static("CreateEmpty", &SkFontStyleSet::CreateEmpty)
        .def("__str__",
             [](SkFontStyleSet &self)
             {
                 const int count = self.count();
                 return "FontStyleSet({} style{})"_s.format(count, count == 1 ? "" : "s");
             });

    py::class_<SkFontMgr, sk_sp<SkFontMgr>>(m, "FontMgr")
        .def("countFamilies", &SkFontMgr::countFamilies)
        .def("__len__", &SkFontMgr::countFamilies)
        .def("getFamilyName", &FontMgr_getFamilyName, "Return the name of the font family at the given *index*.",
             "index"_a)
        .def("__getitem__", &FontMgr_getFamilyName, "Same as :py:meth:`getFamilyName`.", "index"_a)
        .def("createStyleSet", &SkFontMgr::createStyleSet, "index"_a)
        .def(
            "matchFamily",
            [](const SkFontMgr &self, const std::optional<std::string> &familyName)
            { return self.matchFamily(familyName ? familyName->c_str() : nullptr); },
            "familyName"_a)
        .def(
            "matchFamilyStyle",
            [](const SkFontMgr &self, const std::optional<std::string> &familyName, const SkFontStyle &style)
            { return self.matchFamilyStyle(familyName ? familyName->c_str() : nullptr, style); },
            "familyName"_a, "style"_a)
        .def(
            "matchFamilyStyleCharacter",
            [](const SkFontMgr &self, const std::optional<std::string> &familyName, const SkFontStyle &style,
               const std::vector<std::string> &bcp47, const SkUnichar &character)
            {
                std::vector<const char *> bcp47_cstr(bcp47.size());
                std::transform(bcp47.begin(), bcp47.end(), bcp47_cstr.begin(),
                               [](const std::string &s) { return s.c_str(); });
                return self.matchFamilyStyleCharacter(familyName ? familyName->c_str() : nullptr, style,
                                                      bcp47_cstr.data(), bcp47_cstr.size(), character);
            },
            R"doc(
                Use the system fallback to find a typeface for the given character. ``bcp47Count`` is automatically set
                to the number of strings in *bcp47*.
            )doc",
            "familyName"_a, "style"_a, "bcp47"_a, "character"_a)
        .def("makeFromData", &SkFontMgr::makeFromData, "data"_a, "ttcIndex"_a = 0)
        .def("makeFromFile", &SkFontMgr::makeFromFile, "path"_a, "ttcIndex"_a = 0)
        .def("legacyMakeTypeface", &SkFontMgr::legacyMakeTypeface, "familyName"_a, "style"_a)
        .def_static("RefDefault", &SkFontMgr::RefDefault)
        .def_static("RefEmpty", &SkFontMgr::RefEmpty)
        .def(py::init(&SkFontMgr::RefDefault))
        .def_static("New_Custom_Data", [](std::vector<sk_sp<SkData>> &datas)
                    { return SkFontMgr_New_Custom_Data(SkSpan(datas.data(), datas.size())); })
        .def("__str__",
             [](const SkFontMgr &self)
             {
                 const int count = self.countFamilies();
                 return "FontMgr({} famil{})"_s.format(count, count == 1 ? "y" : "ies");
             });
}