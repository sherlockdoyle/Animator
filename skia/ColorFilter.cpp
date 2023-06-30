#include "common.h"
#include "include/core/SkColorFilter.h"
#include "include/core/SkColorSpace.h"
#include "include/core/SkColorTable.h"
#include "include/effects/SkColorMatrix.h"
#include "include/effects/SkColorMatrixFilter.h"
#include "include/effects/SkHighContrastFilter.h"
#include "include/effects/SkLumaColorFilter.h"
#include "include/effects/SkOverdrawColorFilter.h"
#include <pybind11/stl.h>

void validateTableARGB(const std::optional<std::vector<uint8_t>> &tableA,
                       const std::optional<std::vector<uint8_t>> &tableR,
                       const std::optional<std::vector<uint8_t>> &tableG,
                       const std::optional<std::vector<uint8_t>> &tableB)
{
    if (!tableA && !tableR && !tableG && !tableB)
        throw py::value_error("At least one table must be specified.");
    if (tableA && tableA->size() != 256)
        throw py::value_error("tableA must have 256 elements.");
    if (tableR && tableR->size() != 256)
        throw py::value_error("tableR must have 256 elements.");
    if (tableG && tableG->size() != 256)
        throw py::value_error("tableG must have 256 elements.");
    if (tableB && tableB->size() != 256)
        throw py::value_error("tableB must have 256 elements.");
}

void initColorFilter(py::module &m)
{
    py::class_<SkColorFilter, sk_sp<SkColorFilter>, SkFlattenable>(m, "ColorFilter")
        .def(
            "asAColorMode",
            [](SkColorFilter &colorFilter) -> std::optional<py::tuple>
            {
                SkColor color;
                SkBlendMode mode;
                if (colorFilter.asAColorMode(&color, &mode))
                    return py::make_tuple(color, mode);
                return std::nullopt;
            },
            R"doc(
                If the filter can be represented by a source color plus Mode, this returns (color, mode) appropriately.
                If not, this returns ``None``.

                :return: (color, mode) or None
                :rtype: Tuple[int, skia.BlendMode] | None
            )doc")
        .def(
            "asAColorMatrix",
            [](SkColorFilter &colorFilter) -> std::optional<std::vector<float>>
            {
                std::vector<float> matrix(20);
                if (colorFilter.asAColorMatrix(matrix.data()))
                    return matrix;
                return std::nullopt;
            },
            R"doc(
                If the filter can be represented by a 5x4 matrix, this returns list of floats appropriately. If not,
                this returns ``None``.

                :return: list of floats or None
                :rtype: List[float] | None
            )doc")
        .def("isAlphaUnchanged", &SkColorFilter::isAlphaUnchanged)
        .def("filterColor", &SkColorFilter::filterColor, "color"_a)
        .def("filterColor4f", &SkColorFilter::filterColor4f, "srcColor"_a, "srcCS"_a, "dstCS"_a)
        .def("makeComposed", &SkColorFilter::makeComposed, "inner"_a)
        .def_static(
            "Deserialize",
            [](const py::buffer &b)
            {
                py::buffer_info info = b.request();
                return SkColorFilter::Deserialize(info.ptr, info.size * info.itemsize);
            },
            "Deserialize a color filter from a buffer.", "buffer"_a);

    py::class_<SkColorMatrix>(m, "ColorMatrix")
        .def(py::init<>())
        .def(py::init<float, float, float, float, float, float, float, float, float, float, float, float, float, float,
                      float, float, float, float, float, float>(),
             "m00"_a, "m01"_a, "m02"_a, "m03"_a, "m04"_a, "m10"_a, "m11"_a, "m12"_a, "m13"_a, "m14"_a, "m20"_a, "m21"_a,
             "m22"_a, "m23"_a, "m24"_a, "m30"_a, "m31"_a, "m32"_a, "m33"_a, "m34"_a)
        .def(py::init(
                 [](const std::vector<float> &m)
                 {
                     if (m.size() != 20)
                         throw py::value_error("ColorMatrix must have 20 elements");
                     return SkColorMatrix{m[0],  m[1],  m[2],  m[3],  m[4],  m[5],  m[6],  m[7],  m[8],  m[9],
                                          m[10], m[11], m[12], m[13], m[14], m[15], m[16], m[17], m[18], m[19]};
                 }),
             "Construct a color matrix from a list of 20 floats.", "m"_a)
        .def_static("RGBtoYUV", &SkColorMatrix::RGBtoYUV, "cs"_a)
        .def_static("YUVtoRGB", &SkColorMatrix::YUVtoRGB, "cs"_a)
        .def("setIdentity", &SkColorMatrix::setIdentity)
        .def("setScale", &SkColorMatrix::setScale, "rScale"_a, "gScale"_a, "bScale"_a, "aScale"_a = 1)
        .def("postTranslate", &SkColorMatrix::postTranslate, "dr"_a, "dg"_a, "db"_a, "da"_a)
        .def("setConcat", &SkColorMatrix::setConcat, "a"_a, "b"_a)
        .def("preConcat", &SkColorMatrix::preConcat, "mat"_a)
        .def("postConcat", &SkColorMatrix::postConcat, "mat"_a)
        .def("setSaturation", &SkColorMatrix::setSaturation, "sat"_a)
        .def(
            "setRowMajor",
            [](SkColorMatrix &mat, const std::vector<float> &src)
            {
                if (src.size() != 20)
                    throw py::value_error("src must be 20 floats");
                mat.setRowMajor(src.data());
            },
            "src"_a)
        .def(
            "getRowMajor",
            [](const SkColorMatrix &mat)
            {
                std::vector<float> dst(20);
                mat.getRowMajor(dst.data());
                return dst;
            },
            "Returns a list of 20 floats representing the row-major matrix.")
        .def("__str__",
             [](const SkColorMatrix &mat)
             {
                 std::stringstream s;
                 float m[20];
                 mat.getRowMajor(m);
                 s << "ColorMatrix(";
                 for (int i = 0; i < 4; ++i)
                 {
                     s << "(";
                     for (int j = 0; j < 5; ++j)
                     {
                         s << m[i * 5 + j];
                         if (j < 4)
                             s << ", ";
                     }
                     s << (i < 3 ? "), " : ")");
                 }
                 s << ")";
                 return s.str();
             });

    py::implicitly_convertible<std::vector<float>, SkColorMatrix>();

    py::class_<SkColorTable, sk_sp<SkColorTable>>(m, "ColorTable")
        .def_static(
            "Make",
            [](const std::vector<uint8_t> &table)
            {
                if (table.size() != 256)
                    throw std::runtime_error("Table must have 256 elements.");
                return SkColorTable::Make(table.data());
            },
            "table"_a)
        .def_static(
            "Make",
            [](const std::optional<std::vector<uint8_t>> &tableA, const std::optional<std::vector<uint8_t>> &tableR,
               const std::optional<std::vector<uint8_t>> &tableG, const std::optional<std::vector<uint8_t>> &tableB)
            {
                validateTableARGB(tableA, tableR, tableG, tableB);
                return SkColorTable::Make(tableA ? tableA->data() : nullptr, tableR ? tableR->data() : nullptr,
                                          tableG ? tableG->data() : nullptr, tableB ? tableB->data() : nullptr);
            },
            "tableA"_a, "tableR"_a, "tableG"_a, "tableB"_a)
        .def(py::init(
                 [](const std::vector<uint8_t> &table)
                 {
                     if (table.size() != 256)
                         throw std::runtime_error("Table must have 256 elements.");
                     return SkColorTable::Make(table.data());
                 }),
             "table"_a)
        .def(
            py::init(
                [](const std::optional<std::vector<uint8_t>> &tableA, const std::optional<std::vector<uint8_t>> &tableR,
                   const std::optional<std::vector<uint8_t>> &tableG, const std::optional<std::vector<uint8_t>> &tableB)
                {
                    validateTableARGB(tableA, tableR, tableG, tableB);
                    return SkColorTable::Make(tableA ? tableA->data() : nullptr, tableR ? tableR->data() : nullptr,
                                              tableG ? tableG->data() : nullptr, tableB ? tableB->data() : nullptr);
                }),
            "tableA"_a, "tableR"_a, "tableG"_a, "tableB"_a)
        .def("alphaTable",
             [](const SkColorTable &self)
             {
                 return py::memoryview::from_buffer(self.alphaTable(), sizeof(uint8_t),
                                                    py::format_descriptor<uint8_t>::value, {256}, {sizeof(uint8_t)});
             })
        .def("redTable",
             [](const SkColorTable &self)
             {
                 return py::memoryview::from_buffer(self.redTable(), sizeof(uint8_t),
                                                    py::format_descriptor<uint8_t>::value, {256}, {sizeof(uint8_t)});
             })
        .def("greenTable",
             [](const SkColorTable &self)
             {
                 return py::memoryview::from_buffer(self.greenTable(), sizeof(uint8_t),
                                                    py::format_descriptor<uint8_t>::value, {256}, {sizeof(uint8_t)});
             })
        .def("blueTable",
             [](const SkColorTable &self)
             {
                 return py::memoryview::from_buffer(self.blueTable(), sizeof(uint8_t),
                                                    py::format_descriptor<uint8_t>::value, {256}, {sizeof(uint8_t)});
             });

    py::class_<SkColorFilters>(m, "ColorFilters")
        .def_static("Compose", &SkColorFilters::Compose, "outer"_a, "inner"_a)
        .def_static("Blend",
                    py::overload_cast<const SkColor4f &, sk_sp<SkColorSpace>, SkBlendMode>(&SkColorFilters::Blend),
                    "c"_a, "cs"_a, "mode"_a)
        .def_static("Blend", py::overload_cast<SkColor, SkBlendMode>(&SkColorFilters::Blend), "c"_a, "mode"_a)
        .def_static("Matrix", py::overload_cast<const SkColorMatrix &>(&SkColorFilters::Matrix), "cm"_a)
        .def_static(
            "Matrix",
            [](const std::vector<float> &rowMajor)
            {
                if (rowMajor.size() != 20)
                    throw std::runtime_error("Input must have 20 elements.");
                return SkColorFilters::Matrix(rowMajor.data());
            },
            "rowMajor"_a)
        .def_static("HSLAMatrix", py::overload_cast<const SkColorMatrix &>(&SkColorFilters::HSLAMatrix), "cm"_a)
        .def_static(
            "HSLAMatrix",
            [](const std::vector<float> &rowMajor)
            {
                if (rowMajor.size() != 20)
                    throw std::runtime_error("Input must have 20 elements.");
                return SkColorFilters::HSLAMatrix(rowMajor.data());
            },
            "rowMajor"_a)
        .def_static("LinearToSRGBGamma", &SkColorFilters::LinearToSRGBGamma)
        .def_static("SRGBToLinearGamma", &SkColorFilters::SRGBToLinearGamma)
        .def_static("Lerp", &SkColorFilters::Lerp, "t"_a, "dst"_a, "src"_a)
        .def_static(
            "Table",
            [](const std::vector<uint8_t> &table)
            {
                if (table.size() != 256)
                    throw std::runtime_error("Expected 256 entries in table.");
                return SkColorFilters::Table(table.data());
            },
            "table"_a)
        .def_static(
            "TableARGB",
            [](const std::optional<std::vector<uint8_t>> &tableA, const std::optional<std::vector<uint8_t>> &tableR,
               const std::optional<std::vector<uint8_t>> &tableG, const std::optional<std::vector<uint8_t>> &tableB)
            {
                validateTableARGB(tableA, tableR, tableG, tableB);
                return SkColorFilters::TableARGB(tableA ? tableA->data() : nullptr, tableR ? tableR->data() : nullptr,
                                                 tableG ? tableG->data() : nullptr, tableB ? tableB->data() : nullptr);
            },
            "tableA"_a, "tableR"_a, "tableG"_a, "tableB"_a)
        .def_static("Table", py::overload_cast<sk_sp<SkColorTable>>(&SkColorFilters::Table), "table"_a)
        .def_static("Lighting", &SkColorFilters::Lighting, "mul"_a, "add"_a);

    py::class_<SkColorMatrixFilter, sk_sp<SkColorMatrixFilter>, SkColorFilter>(m, "ColorMatrixFilter")
        .def_static("MakeLightingFilter", &SkColorMatrixFilter::MakeLightingFilter, "mul"_a, "add"_a);

    py::class_<SkHighContrastConfig> HighContrastConfig(m, "HighContrastConfig");

    py::enum_<SkHighContrastConfig::InvertStyle>(HighContrastConfig, "InvertStyle")
        .value("kNoInvert", SkHighContrastConfig::InvertStyle::kNoInvert)
        .value("kInvertBrightness", SkHighContrastConfig::InvertStyle::kInvertBrightness)
        .value("kInvertLightness", SkHighContrastConfig::InvertStyle::kInvertLightness)
        .value("kLast", SkHighContrastConfig::InvertStyle::kLast);
    HighContrastConfig
        .def(py::init([](const bool &grayscale, const SkHighContrastConfig::InvertStyle &invertStyle,
                         const SkScalar &contrast) { return SkHighContrastConfig(grayscale, invertStyle, contrast); }),
             "grayscale"_a = false, "invertStyle"_a = SkHighContrastConfig::InvertStyle::kNoInvert, "contrast"_a = 0)
        .def("isValid", &SkHighContrastConfig::isValid)
        .def_readwrite("fGrayscale", &SkHighContrastConfig::fGrayscale)
        .def_readwrite("fInvertStyle", &SkHighContrastConfig::fInvertStyle)
        .def_readwrite("fContrast", &SkHighContrastConfig::fContrast);

    py::class_<SkHighContrastFilter>(m, "HighContrastFilter")
        .def_static("Make", &SkHighContrastFilter::Make, "config"_a);

    py::class_<SkLumaColorFilter>(m, "LumaColorFilter").def_static("Make", &SkLumaColorFilter::Make);

    py::class_<SkOverdrawColorFilter>(m, "OverdrawColorFilter")
        .def_readonly_static("kNumColors", &SkOverdrawColorFilter::kNumColors)
        .def_static(
            "MakeWithColors",
            [](const std::vector<SkColor> &colors)
            {
                if (colors.size() != SkOverdrawColorFilter::kNumColors)
                {
                    std::stringstream s;
                    s << "Expected " << SkOverdrawColorFilter::kNumColors << " colors, got " << colors.size();
                    throw py::value_error(s.str());
                }
                return SkOverdrawColorFilter::MakeWithSkColors(colors.data());
            },
            "colors"_a);
}