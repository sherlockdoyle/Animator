#include "common.h"
#include "include/core/SkBlender.h"
#include "include/core/SkColorFilter.h"
#include "include/core/SkImage.h"
#include "include/core/SkMatrix.h"
#include "include/core/SkShader.h"
#include "include/effects/SkGradientShader.h"
#include "include/effects/SkPerlinNoiseShader.h"
#include <pybind11/stl.h>

template <typename T>
const SkScalar *validateColor_Pos(const std::vector<T> &colors, const std::optional<std::vector<SkScalar>> &pos)
{
    if (pos)
    {
        if (pos->size() == colors.size())
            return pos->data();
        throw py::value_error(
            "pos must have the same number of elements as in colors. Expected {} but got {}."_s.format(colors.size(),
                                                                                                       pos->size()));
    }
    return nullptr;
}

void initShader(py::module &m)
{
    py::class_<SkShader, sk_sp<SkShader>, SkFlattenable> Shader(
        m, "Shader", "Functions from the SkShaders namespace are also available here as static methods.");
    Shader.def("isOpaque", &SkShader::isOpaque)
        .def(
            "isAImage",
            [](const SkShader &self) -> std::optional<py::tuple>
            {
                SkMatrix localMatrix;
                SkTileMode xy[2];
                SkImage *image = self.isAImage(&localMatrix, xy);
                if (image)
                    return py::make_tuple(sk_ref_sp(image), localMatrix, py::make_tuple(xy[0], xy[1]));
                else
                    return std::nullopt;
            },
            R"doc(
                Iff this shader is backed by a single :py:class:`Image`, return it, the local matrix, and the tile mode.
                Else return ``None``.
            )doc")
        .def("makeWithLocalMatrix", &SkShader::makeWithLocalMatrix, "localMatrix"_a)
        .def("makeWithColorFilter", &SkShader::makeWithColorFilter, "filter"_a)
        .def_static("Empty", &SkShaders::Empty)
        .def_static("Color", py::overload_cast<SkColor>(&SkShaders::Color), "color"_a)
        .def_static("Color", py::overload_cast<const SkColor4f &, sk_sp<SkColorSpace>>(&SkShaders::Color), "color"_a,
                    "space"_a = nullptr)
        .def_static("Blend", py::overload_cast<SkBlendMode, sk_sp<SkShader>, sk_sp<SkShader>>(&SkShaders::Blend),
                    "mode"_a, "dst"_a, "src"_a)
        .def_static("Blend", py::overload_cast<sk_sp<SkBlender>, sk_sp<SkShader>, sk_sp<SkShader>>(&SkShaders::Blend),
                    "blender"_a, "dst"_a, "src"_a)
        .def_static("CoordClamp", &SkShaders::CoordClamp, "shader"_a, "subset"_a)
        .def_static("MakeFractalNoise", &SkShaders::MakeFractalNoise, "baseFrequencyX"_a, "baseFrequencyY"_a,
                    "numOctaves"_a, "seed"_a, "tileSize"_a = nullptr)
        .def_static("MakeTurbulence", &SkShaders::MakeTurbulence, "baseFrequencyX"_a, "baseFrequencyY"_a,
                    "numOctaves"_a, "seed"_a, "tileSize"_a = nullptr);

    py::class_<SkGradientShader> GradientShader(m, "GradientShader");

    py::enum_<SkGradientShader::Flags>(GradientShader, "Flags", py::arithmetic())
        .value("kInterpolateColorsInPremul_Flag", SkGradientShader::Flags::kInterpolateColorsInPremul_Flag);

    py::class_<SkGradientShader::Interpolation> Interpolation(GradientShader, "Interpolation");

    py::enum_<SkGradientShader::Interpolation::InPremul>(Interpolation, "InPremul")
        .value("kNo", SkGradientShader::Interpolation::InPremul::kNo)
        .value("kYes", SkGradientShader::Interpolation::InPremul::kYes);

    py::enum_<SkGradientShader::Interpolation::ColorSpace>(Interpolation, "ColorSpace", py::arithmetic())
        .value("kDestination", SkGradientShader::Interpolation::ColorSpace::kDestination)
        .value("kSRGBLinear", SkGradientShader::Interpolation::ColorSpace::kSRGBLinear)
        .value("kLab", SkGradientShader::Interpolation::ColorSpace::kLab)
        .value("kOKLab", SkGradientShader::Interpolation::ColorSpace::kOKLab)
        .value("kLCH", SkGradientShader::Interpolation::ColorSpace::kLCH)
        .value("kOKLCH", SkGradientShader::Interpolation::ColorSpace::kOKLCH)
        .value("kSRGB", SkGradientShader::Interpolation::ColorSpace::kSRGB)
        .value("kHSL", SkGradientShader::Interpolation::ColorSpace::kHSL)
        .value("kHWB", SkGradientShader::Interpolation::ColorSpace::kHWB)
        .value("kLastColorSpace", SkGradientShader::Interpolation::ColorSpace::kLastColorSpace);
    Interpolation.def_readonly_static("kColorSpaceCount", &SkGradientShader::Interpolation::kColorSpaceCount);

    py::enum_<SkGradientShader::Interpolation::HueMethod>(Interpolation, "HueMethod", py::arithmetic())
        .value("kShorter", SkGradientShader::Interpolation::HueMethod::kShorter)
        .value("kLonger", SkGradientShader::Interpolation::HueMethod::kLonger)
        .value("kIncreasing", SkGradientShader::Interpolation::HueMethod::kIncreasing)
        .value("kDecreasing", SkGradientShader::Interpolation::HueMethod::kDecreasing)
        .value("kLastHueMethod", SkGradientShader::Interpolation::HueMethod::kLastHueMethod);
    Interpolation.def_readonly_static("kHueMethodCount", &SkGradientShader::Interpolation::kHueMethodCount)
        .def_readwrite("fInPremul", &SkGradientShader::Interpolation::fInPremul)
        .def_readwrite("fColorSpace", &SkGradientShader::Interpolation::fColorSpace)
        .def_readwrite("fHueMethod", &SkGradientShader::Interpolation::fHueMethod)
        .def_static("FromFlags", &SkGradientShader::Interpolation::FromFlags, "flags"_a);

    static constexpr SkGradientShader::Interpolation di;

    GradientShader
        .def_static(
            "MakeLinear",
            [](const std::vector<SkPoint> &pts, const std::vector<SkColor> &colors,
               const std::optional<std::vector<SkScalar>> &pos, const SkTileMode &mode, const uint32_t &flags,
               const SkMatrix *localMatrix)
            {
                if (pts.size() != 2)
                    throw py::value_error("pts must have 2 elements.");
                return SkGradientShader::MakeLinear(pts.data(), colors.data(), validateColor_Pos(colors, pos),
                                                    colors.size(), mode, flags, localMatrix);
            },
            "Returns a linear gradient shader between the two specified *pts* with the specified *colors*.", "pts"_a,
            "colors"_a, "pos"_a = nullptr, "mode"_a = SkTileMode::kClamp, "flags"_a = 0, "localMatrix"_a = nullptr)
        .def_static(
            "MakeLinear",
            [](const std::vector<SkPoint> &pts, const std::vector<SkColor4f> &colors,
               const sk_sp<SkColorSpace> &colorSpace, const std::optional<std::vector<SkScalar>> &pos,
               const SkTileMode &mode, const SkGradientShader::Interpolation &interpolation,
               const SkMatrix *localMatrix)
            {
                if (pts.size() != 2)
                    throw py::value_error("pts must have 2 elements.");
                return SkGradientShader::MakeLinear(pts.data(), colors.data(), colorSpace,
                                                    validateColor_Pos(colors, pos), colors.size(), mode, interpolation,
                                                    localMatrix);
            },
            "Returns a linear gradient shader between the two specified *pts* with the specified *colors*.", "pts"_a,
            "colors"_a, "colorSpace"_a = nullptr, "pos"_a = nullptr, "mode"_a = SkTileMode::kClamp,
            "interpolation"_a = di, "localMatrix"_a = nullptr)
        .def_static(
            "MakeLinear",
            [](const std::vector<SkPoint> &pts, const std::vector<SkColor4f> &colors,
               const sk_sp<SkColorSpace> &colorSpace, const std::optional<std::vector<SkScalar>> &pos,
               const SkTileMode &mode, const uint32_t &flags, const SkMatrix *localMatrix)
            {
                if (pts.size() != 2)
                    throw py::value_error("pts must have 2 elements.");
                return SkGradientShader::MakeLinear(pts.data(), colors.data(), colorSpace,
                                                    validateColor_Pos(colors, pos), colors.size(), mode, flags,
                                                    localMatrix);
            },
            "Returns a linear gradient shader between the two specified *pts* with the specified *colors*.", "pts"_a,
            "colors"_a, "colorSpace"_a = nullptr, "pos"_a = nullptr, "mode"_a = SkTileMode::kClamp, "flags"_a = 0,
            "localMatrix"_a = nullptr)
        .def_static(
            "MakeRadial",
            [](const SkPoint &center, const SkScalar &radius, const std::vector<SkColor> &colors,
               const std::optional<std::vector<SkScalar>> &pos, const SkTileMode &mode, const uint32_t &flags,
               const SkMatrix *localMatrix)
            {
                return SkGradientShader::MakeRadial(center, radius, colors.data(), validateColor_Pos(colors, pos),
                                                    colors.size(), mode, flags, localMatrix);
            },
            "Returns a radial gradient shader with the specified *center*, *radius* and *colors*.", "center"_a,
            "radius"_a, "colors"_a, "pos"_a = nullptr, "mode"_a = SkTileMode::kClamp, "flags"_a = 0,
            "localMatrix"_a = nullptr)
        .def_static(
            "MakeRadial",
            [](const SkPoint &center, const SkScalar &radius, const std::vector<SkColor4f> &colors,
               const sk_sp<SkColorSpace> &colorSpace, const std::optional<std::vector<SkScalar>> &pos,
               const SkTileMode &mode, const SkGradientShader::Interpolation &interpolation,
               const SkMatrix *localMatrix)
            {
                return SkGradientShader::MakeRadial(center, radius, colors.data(), colorSpace,
                                                    validateColor_Pos(colors, pos), colors.size(), mode, interpolation,
                                                    localMatrix);
            },
            "Returns a radial gradient shader with the specified *center*, *radius* and *colors*.", "center"_a,
            "radius"_a, "colors"_a, "colorSpace"_a = nullptr, "pos"_a = nullptr, "mode"_a = SkTileMode::kClamp,
            "interpolation"_a = di, "localMatrix"_a = nullptr)
        .def_static(
            "MakeRadial",
            [](const SkPoint &center, const SkScalar &radius, const std::vector<SkColor4f> &colors,
               const sk_sp<SkColorSpace> &colorSpace, const std::optional<std::vector<SkScalar>> &pos,
               const SkTileMode &mode, const uint32_t &flags, const SkMatrix *localMatrix)
            {
                return SkGradientShader::MakeRadial(center, radius, colors.data(), colorSpace,
                                                    validateColor_Pos(colors, pos), colors.size(), mode, flags,
                                                    localMatrix);
            },
            "Returns a radial gradient shader with the specified *center*, *radius* and *colors*.", "center"_a,
            "radius"_a, "colors"_a, "colorSpace"_a = nullptr, "pos"_a = nullptr, "mode"_a = SkTileMode::kClamp,
            "flags"_a = 0, "localMatrix"_a = nullptr)
        .def_static(
            "MakeTwoPointConical",
            [](const SkPoint &start, const SkScalar &startRadius, const SkPoint &end, const SkScalar &endRadius,
               const std::vector<SkColor> &colors, const std::optional<std::vector<SkScalar>> &pos,
               const SkTileMode &mode, const uint32_t &flags, const SkMatrix *localMatrix)
            {
                return SkGradientShader::MakeTwoPointConical(start, startRadius, end, endRadius, colors.data(),
                                                             validateColor_Pos(colors, pos), colors.size(), mode, flags,
                                                             localMatrix);
            },
            R"doc(
                Returns a conical gradient shader with the specified *start* and *end* points, the *startRadius* and
                *endRadius*, and the *colors*.
            )doc",
            "start"_a, "startRadius"_a, "end"_a, "endRadius"_a, "colors"_a, "pos"_a = nullptr,
            "mode"_a = SkTileMode::kClamp, "flags"_a = 0, "localMatrix"_a = nullptr)
        .def_static(
            "MakeTwoPointConical",
            [](const SkPoint &start, const SkScalar &startRadius, const SkPoint &end, const SkScalar &endRadius,
               const std::vector<SkColor4f> &colors, const sk_sp<SkColorSpace> &colorSpace,
               const std::optional<std::vector<SkScalar>> &pos, const SkTileMode &mode,
               const SkGradientShader::Interpolation &interpolation, const SkMatrix *localMatrix)
            {
                return SkGradientShader::MakeTwoPointConical(start, startRadius, end, endRadius, colors.data(),
                                                             colorSpace, validateColor_Pos(colors, pos), colors.size(),
                                                             mode, interpolation, localMatrix);
            },
            R"doc(
                Returns a conical gradient shader with the specified *start* and *end* points, the *startRadius* and
                *endRadius*, and the *colors*.
            )doc",
            "start"_a, "startRadius"_a, "end"_a, "endRadius"_a, "colors"_a, "colorSpace"_a = nullptr, "pos"_a = nullptr,
            "mode"_a = SkTileMode::kClamp, "interpolation"_a = di, "localMatrix"_a = nullptr)
        .def_static(
            "MakeTwoPointConical",
            [](const SkPoint &start, const SkScalar &startRadius, const SkPoint &end, const SkScalar &endRadius,
               const std::vector<SkColor4f> &colors, const sk_sp<SkColorSpace> &colorSpace,
               const std::optional<std::vector<SkScalar>> &pos, const SkTileMode &mode, const uint32_t &flags,
               const SkMatrix *localMatrix)
            {
                return SkGradientShader::MakeTwoPointConical(start, startRadius, end, endRadius, colors.data(),
                                                             colorSpace, validateColor_Pos(colors, pos), colors.size(),
                                                             mode, flags, localMatrix);
            },
            R"doc(
                Returns a conical gradient shader with the specified *start* and *end* points, the *startRadius* and
                *endRadius*, and the *colors*.
            )doc",
            "start"_a, "startRadius"_a, "end"_a, "endRadius"_a, "colors"_a, "colorSpace"_a = nullptr, "pos"_a = nullptr,
            "mode"_a = SkTileMode::kClamp, "flags"_a = 0, "localMatrix"_a = nullptr)
        .def_static(
            "MakeSweep",
            [](const SkScalar &cx, const SkScalar &cy, const std::vector<SkColor> &colors,
               const std::optional<std::vector<SkScalar>> &pos, const SkTileMode &mode, const SkScalar &startAngle,
               const SkScalar &endAngle, const uint32_t &flags, const SkMatrix *localMatrix)
            {
                return SkGradientShader::MakeSweep(cx, cy, colors.data(), validateColor_Pos(colors, pos), colors.size(),
                                                   mode, startAngle, endAngle, flags, localMatrix);
            },
            "Returns a sweep gradient shader with the specified center (*cx*, *cy*) and *colors*.", "cx"_a, "cy"_a,
            "colors"_a, "pos"_a = nullptr, "mode"_a = SkTileMode::kClamp, "startAngle"_a = 0, "endAngle"_a = 360,
            "flags"_a = 0, "localMatrix"_a = nullptr)
        .def_static(
            "MakeSweep",
            [](const SkScalar &cx, const SkScalar &cy, const std::vector<SkColor4f> &colors,
               const sk_sp<SkColorSpace> &colorSpace, const std::optional<std::vector<SkScalar>> &pos,
               const SkTileMode &mode, const SkScalar &startAngle, const SkScalar &endAngle,
               const SkGradientShader::Interpolation &interpolation, const SkMatrix *localMatrix)
            {
                return SkGradientShader::MakeSweep(cx, cy, colors.data(), colorSpace, validateColor_Pos(colors, pos),
                                                   colors.size(), mode, startAngle, endAngle, interpolation,
                                                   localMatrix);
            },
            "Returns a sweep gradient shader with the specified center (*cx*, *cy*) and *colors*.", "cx"_a, "cy"_a,
            "colors"_a, "colorSpace"_a = nullptr, "pos"_a = nullptr, "mode"_a = SkTileMode::kClamp, "startAngle"_a = 0,
            "endAngle"_a = 360, "interpolation"_a = di, "localMatrix"_a = nullptr)
        .def_static(
            "MakeSweep",
            [](const SkScalar &cx, const SkScalar &cy, const std::vector<SkColor4f> &colors,
               const sk_sp<SkColorSpace> &colorSpace, const std::optional<std::vector<SkScalar>> &pos,
               const SkTileMode &mode, const SkScalar &startAngle, const SkScalar &endAngle, const uint32_t &flags,
               const SkMatrix *localMatrix)
            {
                return SkGradientShader::MakeSweep(cx, cy, colors.data(), colorSpace, validateColor_Pos(colors, pos),
                                                   colors.size(), mode, startAngle, endAngle, flags, localMatrix);
            },
            "Returns a sweep gradient shader with the specified center (*cx*, *cy*) and *colors*.", "cx"_a, "cy"_a,
            "colors"_a, "colorSpace"_a = nullptr, "pos"_a = nullptr, "mode"_a = SkTileMode::kClamp, "startAngle"_a = 0,
            "endAngle"_a = 360, "flags"_a = 0, "localMatrix"_a = nullptr);
}