#include "common.h"
#include "include/core/SkMaskFilter.h"
#include "include/core/SkShader.h"
#include "include/effects/SkShaderMaskFilter.h"
#include "include/effects/SkTableMaskFilter.h"
#include <pybind11/stl.h>

void initMaskFilter(py::module &m)
{
    py::enum_<SkBlurStyle>(m, "BlurStyle", py::arithmetic())
        .value("kNormal_BlurStyle", SkBlurStyle::kNormal_SkBlurStyle)
        .value("kSolid_BlurStyle", SkBlurStyle::kSolid_SkBlurStyle)
        .value("kOuter_BlurStyle", SkBlurStyle::kOuter_SkBlurStyle)
        .value("kInner_BlurStyle", SkBlurStyle::kInner_SkBlurStyle)
        .value("kLastEnum_BlurStyle", SkBlurStyle::kLastEnum_SkBlurStyle);

    py::class_<SkMaskFilter, sk_sp<SkMaskFilter>, SkFlattenable>(m, "MaskFilter")
        .def_static("MakeBlur", &SkMaskFilter::MakeBlur, "style"_a, "sigma"_a, "respectCTM"_a = true)
        .def("approximateFilteredBounds", &SkMaskFilter::approximateFilteredBounds, "src"_a)
        .def_static(
            "Deserialize",
            [](const py::buffer &data)
            {
                py::buffer_info bufInfo = data.request();
                return SkMaskFilter::Deserialize(bufInfo.ptr, bufInfo.size * bufInfo.itemsize, nullptr);
            },
            "data"_a);

    py::class_<SkShaderMaskFilter>(m, "ShaderMaskFilter").def_static("Make", &SkShaderMaskFilter::Make, "shader"_a);

    py::class_<SkTableMaskFilter>(m, "TableMaskFilter")
        .def_static(
            "MakeGammaTable",
            [](const SkScalar &gamma)
            {
                std::vector<uint8_t> table(256);
                SkTableMaskFilter::MakeGammaTable(table.data(), gamma);
                return table;
            },
            "Utility that returns the *gamma* table.", "gamma"_a)
        .def_static(
            "MakeClipTable",
            [](const uint8_t &min, const uint8_t &max)
            {
                std::vector<uint8_t> table(256);
                SkTableMaskFilter::MakeClipTable(table.data(), min, max);
                return table;
            },
            "Utility that returns a clipping table.", "min"_a, "max"_a)
        .def_static(
            "Create",
            [](const std::vector<uint8_t> &table)
            {
                if (table.size() != 256)
                    throw py::value_error("Table must have 256 entries.");
                return SkTableMaskFilter::Create(table.data());
            },
            "table"_a)
        .def_static("CreateGamma", &SkTableMaskFilter::CreateGamma, "gamma"_a)
        .def_static("CreateClip", &SkTableMaskFilter::CreateClip, "min"_a, "max"_a);
}