#include "common.h"
#include "include/core/SkBlender.h"
#include "include/core/SkColorFilter.h"
#include "include/core/SkImage.h"
#include "include/core/SkShader.h"
#include "include/effects/SkGradientShader.h"
#include "include/effects/SkPerlinNoiseShader.h"
#include <pybind11/stl.h>

struct PyGradientInfo : public SkShader::GradientInfo
{
    SkShader::GradientType fType;
    void alloc()
    {
        fColors = new SkColor[fColorCount];
        fColorOffsets = new SkScalar[fColorCount];
    }
    ~PyGradientInfo()
    {
        delete[] fColors;
        delete[] fColorOffsets;
    }
};

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
    py::class_<SkShader, sk_sp<SkShader>, SkFlattenable> Shader(m, "Shader");
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
            )doc");

    py::enum_<SkShader::GradientType>(Shader, "GradientType")
        .value("kNone_GradientType", SkShader::GradientType::kNone_GradientType)
        .value("kColor_GradientType", SkShader::GradientType::kColor_GradientType)
        .value("kLinear_GradientType", SkShader::GradientType::kLinear_GradientType)
        .value("kRadial_GradientType", SkShader::GradientType::kRadial_GradientType)
        .value("kSweep_GradientType", SkShader::GradientType::kSweep_GradientType)
        .value("kConical_GradientType", SkShader::GradientType::kConical_GradientType)
        .value("kLast_GradientType", SkShader::GradientType::kLast_GradientType);

    py::class_<PyGradientInfo>(
        Shader, "GradientInfo",
        "Contains information about a gradient. This also contains an extra field ``fType`` for the gradient type.")
        .def(py::init(
                 [](const int &colorCount)
                 {
                     PyGradientInfo *info = new PyGradientInfo();
                     info->fColorCount = colorCount;
                     info->alloc();
                     return info;
                 }),
             "Construct a GradientInfo with the given number of colors.", "colorCount"_a = 0)
        .def_readwrite("fColorCount", &PyGradientInfo::fColorCount)
        .def_property_readonly("fColors", [](const PyGradientInfo &self)
                               { return std::vector<SkColor>(self.fColors, self.fColors + self.fColorCount); })
        .def_property_readonly(
            "fColorOffsets", [](const PyGradientInfo &self)
            { return std::vector<SkScalar>(self.fColorOffsets, self.fColorOffsets + self.fColorCount); })
        .def_property_readonly("fPoint", [](const PyGradientInfo &self)
                               { return py::make_tuple(self.fPoint[0], self.fPoint[1]); })
        .def_property_readonly("fRadius", [](const PyGradientInfo &self)
                               { return py::make_tuple(self.fRadius[0], self.fRadius[1]); })
        .def_readonly("fTileMode", &PyGradientInfo::fTileMode)
        .def_readonly("fGradientFlags", &PyGradientInfo::fGradientFlags)
        .def_readonly("fType", &PyGradientInfo::fType, "The :py:class:`skia.Shader.GradientType` of this gradient.")
        .def("__str__",
             [](const PyGradientInfo &self)
             {
                 std::stringstream s;
                 s << "GradientInfo({}"_s.format(self.fType);

                 if (self.fType != SkShader::GradientType::kNone_GradientType)
                 {
                     s << ", colorCount=" << self.fColorCount << ", colors=[";
                     for (int i = 0; i < self.fColorCount; ++i)
                     {
                         if (i > 0)
                             s << ", ";
                         s << "0x{:08x}"_s.format(self.fColors[i]);
                     }
                     s << "]";

                     if (self.fType != SkShader::GradientType::kColor_GradientType)
                     {
                         s << ", colorOffsets=[";
                         for (int i = 0; i < self.fColorCount; ++i)
                         {
                             if (i > 0)
                                 s << ", ";
                             s << self.fColorOffsets[i];
                         }
                         s << "]";
                     }

                     if (self.fType == SkShader::GradientType::kRadial_GradientType ||
                         self.fType == SkShader::GradientType::kSweep_GradientType)
                         s << ", point={}"_s.format(self.fPoint[0]);
                     else if (self.fType == SkShader::GradientType::kLinear_GradientType ||
                              self.fType == SkShader::GradientType::kConical_GradientType)
                         s << ", point=[{}, {}]"_s.format(self.fPoint[0], self.fPoint[1]);

                     if (self.fType == SkShader::GradientType::kRadial_GradientType)
                         s << ", radius=" << self.fRadius[0];
                     else if (self.fType == SkShader::GradientType::kConical_GradientType)
                         s << ", radius=[" << self.fRadius[0] << ", " << self.fRadius[1] << "]";

                     s << ", tileMode={}"_s.format(self.fTileMode);
                     if (self.fGradientFlags)
                         s << ", gradientFlags=" << self.fGradientFlags;
                 }

                 s << ")";
                 return s.str();
             });
    Shader
        .def(
            "asAGradient",
            [](const SkShader &self)
            {
                std::unique_ptr<PyGradientInfo> info = std::make_unique<PyGradientInfo>();
                info->fType = self.asAGradient(info.get());
                if (info->fColorCount)
                {
                    info->alloc();
                    info->fType = self.asAGradient(info.get());
                }
                return info;
            },
            R"doc(
                Return a :py:class:`skia.Shader.GradientInfo` object with the gradient information. The returned object
                also contains an extra field ``fType`` for the gradient type.
            )doc")
        .def("makeWithLocalMatrix", &SkShader::makeWithLocalMatrix, "localMatrix"_a)
        .def("makeWithColorFilter", &SkShader::makeWithColorFilter, "filter"_a);

    py::class_<SkShaders>(m, "Shaders")
        .def_static("Empty", &SkShaders::Empty)
        .def_static("Color", py::overload_cast<SkColor>(&SkShaders::Color), "color"_a)
        .def_static("Color", py::overload_cast<const SkColor4f &, sk_sp<SkColorSpace>>(&SkShaders::Color), "color"_a,
                    "space"_a = py::none())
        .def_static("Blend", py::overload_cast<SkBlendMode, sk_sp<SkShader>, sk_sp<SkShader>>(&SkShaders::Blend),
                    "mode"_a, "dst"_a, "src"_a)
        .def_static("Blend", py::overload_cast<sk_sp<SkBlender>, sk_sp<SkShader>, sk_sp<SkShader>>(&SkShaders::Blend),
                    "blender"_a, "dst"_a, "src"_a);

    py::class_<SkGradientShader> GradientShader(m, "GradientShader");

    py::enum_<SkGradientShader::Flags>(GradientShader, "Flags", py::arithmetic())
        .value("kInterpolateColorsInPremul_Flag", SkGradientShader::Flags::kInterpolateColorsInPremul_Flag);

    GradientShader
        .def_static(
            "MakeLinear",
            [](const std::vector<SkPoint> &pts, const std::vector<SkColor> &colors,
               const std::optional<std::vector<SkScalar>> &pos, const SkTileMode &mode, const uint32_t &flags,
               const SkMatrix *localMatrix)
            {
                if (pts.size() != 2)
                    throw py::value_error("pts must have 2 elements");
                return SkGradientShader::MakeLinear(pts.data(), colors.data(), validateColor_Pos(colors, pos),
                                                    colors.size(), mode, flags, localMatrix);
            },
            "Returns a linear gradient shader between the two specified *pts* with the specified *colors*.", "pts"_a,
            "colors"_a, "pos"_a = py::none(), "mode"_a = SkTileMode::kClamp, "flags"_a = 0,
            "localMatrix"_a = py::none())
        .def_static(
            "MakeLinear",
            [](const std::vector<SkPoint> &pts, const std::vector<SkColor4f> &colors,
               const sk_sp<SkColorSpace> &colorSpace, const std::optional<std::vector<SkScalar>> &pos,
               const SkTileMode &mode, const uint32_t &flags, const SkMatrix *localMatrix)
            {
                if (pts.size() != 2)
                    throw py::value_error("pts must have 2 elements");
                return SkGradientShader::MakeLinear(pts.data(), colors.data(), colorSpace,
                                                    validateColor_Pos(colors, pos), colors.size(), mode, flags,
                                                    localMatrix);
            },
            "Returns a linear gradient shader between the two specified *pts* with the specified *colors*.", "pts"_a,
            "colors"_a, "colorSpace"_a = py::none(), "pos"_a = py::none(), "mode"_a = SkTileMode::kClamp, "flags"_a = 0,
            "localMatrix"_a = py::none())
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
            "radius"_a, "colors"_a, "pos"_a = py::none(), "mode"_a = SkTileMode::kClamp, "flags"_a = 0,
            "localMatrix"_a = py::none())
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
            "radius"_a, "colors"_a, "colorSpace"_a = py::none(), "pos"_a = py::none(), "mode"_a = SkTileMode::kClamp,
            "flags"_a = 0, "localMatrix"_a = py::none())
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
            "start"_a, "startRadius"_a, "end"_a, "endRadius"_a, "colors"_a, "pos"_a = py::none(),
            "mode"_a = SkTileMode::kClamp, "flags"_a = 0, "localMatrix"_a = py::none())
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
            "start"_a, "startRadius"_a, "end"_a, "endRadius"_a, "colors"_a, "colorSpace"_a = py::none(),
            "pos"_a = py::none(), "mode"_a = SkTileMode::kClamp, "flags"_a = 0, "localMatrix"_a = py::none())
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
            "colors"_a, "pos"_a = py::none(), "mode"_a = SkTileMode::kClamp, "startAngle"_a = 0, "endAngle"_a = 360,
            "flags"_a = 0, "localMatrix"_a = py::none())
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
            "colors"_a, "colorSpace"_a = py::none(), "pos"_a = py::none(), "mode"_a = SkTileMode::kClamp,
            "startAngle"_a = 0, "endAngle"_a = 360, "flags"_a = 0, "localMatrix"_a = py::none());

    py::class_<SkPerlinNoiseShader>(m, "PerlinNoiseShader")
        .def_static("MakeFractalNoise", &SkPerlinNoiseShader::MakeFractalNoise, "baseFrequencyX"_a, "baseFrequencyY"_a,
                    "numOctaves"_a, "seed"_a, "tileSize"_a = py::none())
        .def_static("MakeTurbulence", &SkPerlinNoiseShader::MakeTurbulence, "baseFrequencyX"_a, "baseFrequencyY"_a,
                    "numOctaves"_a, "seed"_a, "tileSize"_a = py::none());
}