#define SK_ENABLE_SKSL
#include "common.h"
#include "include/core/SkBlender.h"
#include "include/core/SkColorFilter.h"
#include "include/core/SkImageFilter.h"
#include "include/core/SkMatrix.h"
#include "include/core/SkPoint3.h"
#include "include/core/SkSamplingOptions.h"
#include "include/effects/SkImageFilters.h"
#include "include/effects/SkRuntimeEffect.h"
#include <pybind11/stl.h>

void initImageFilter(py::module &m)
{
    py::class_<SkImageFilter, sk_sp<SkImageFilter>, SkFlattenable> ImageFilter(m, "ImageFilter");

    py::enum_<SkImageFilter::MapDirection>(ImageFilter, "MapDirection")
        .value("kForward_MapDirection", SkImageFilter::kForward_MapDirection)
        .value("kReverse_MapDirection", SkImageFilter::kReverse_MapDirection);
    ImageFilter
        .def("filterBounds", &SkImageFilter::filterBounds, "src"_a, "ctm"_a, "direction"_a, "inputRect"_a = py::none())
        .def("isColorFilterNode",
             [](const SkImageFilter &self) -> std::optional<sk_sp<SkColorFilter>>
             {
                 SkColorFilter *colorFilter;
                 if (self.isColorFilterNode(&colorFilter))
                     return sk_sp<SkColorFilter>(colorFilter);
                 return std::nullopt;
             })
        .def("asAColorFilter",
             [](const SkImageFilter &self) -> std::optional<sk_sp<SkColorFilter>>
             {
                 SkColorFilter *colorFilter;
                 if (self.asAColorFilter(&colorFilter))
                     return sk_sp<SkColorFilter>(colorFilter);
                 return std::nullopt;
             })
        .def("countInputs", &SkImageFilter::countInputs)
        .def("getInput", &SkImageFilter::getInput, "i"_a, py::return_value_policy::reference_internal)
        .def("computeFastBounds", &SkImageFilter::computeFastBounds, "bounds"_a)
        .def("canComputeFastBounds", &SkImageFilter::canComputeFastBounds)
        .def("makeWithLocalMatrix", &SkImageFilter::makeWithLocalMatrix, "matrix"_a)
        .def_static(
            "Deserialize",
            [](const py::buffer &data)
            {
                const py::buffer_info bufInfo = data.request();
                return SkImageFilter::Deserialize(bufInfo.ptr, bufInfo.size * bufInfo.itemsize, nullptr);
            },
            "data"_a);

    py::class_<SkImageFilters> ImageFilters(m, "ImageFilters");

    py::class_<SkImageFilters::CropRect>(ImageFilters, "CropRect")
        .def(py::init())
        .def(py::init<std::nullptr_t>(), "crop"_a)
        .def(py::init<const SkIRect &>(), "crop"_a)
        .def(py::init<const SkRect &>(), "crop"_a)
        .def_readwrite("fCropRect", &SkImageFilters::CropRect::fCropRect)
        .def("__str__",
             [](const SkImageFilters::CropRect &self)
             {
                 return "CropRect({}, {}, {}, {})"_s.format(self.fCropRect.fLeft, self.fCropRect.fTop,
                                                            self.fCropRect.fRight, self.fCropRect.fBottom);
             });
    py::implicitly_convertible<py::tuple, SkImageFilters::CropRect>();

    static const SkImageFilters::CropRect dcr = {};                   // default crop rect
    static const SkSamplingOptions dso(SkCubicResampler::Mitchell()); // default sampling options
    ImageFilters
        .def_static("Arithmetic", &SkImageFilters::Arithmetic, "k1"_a, "k2"_a, "k3"_a, "k4"_a,
                    "enforcePMColor"_a = false, "background"_a = py::none(), "foreground"_a = py::none(),
                    "cropRect"_a = dcr)
        .def_static("Blend",
                    py::overload_cast<SkBlendMode, sk_sp<SkImageFilter>, sk_sp<SkImageFilter>,
                                      const SkImageFilters::CropRect &>(&SkImageFilters::Blend),
                    "mode"_a, "background"_a, "foreground"_a = py::none(), "cropRect"_a = dcr)
        .def_static("Blend",
                    py::overload_cast<sk_sp<SkBlender>, sk_sp<SkImageFilter>, sk_sp<SkImageFilter>,
                                      const SkImageFilters::CropRect &>(&SkImageFilters::Blend),
                    "blender"_a, "background"_a, "foreground"_a = py::none(), "cropRect"_a = dcr)
        .def_static(
            "Blur",
            py::overload_cast<SkScalar, SkScalar, SkTileMode, sk_sp<SkImageFilter>, const SkImageFilters::CropRect &>(
                &SkImageFilters::Blur),
            "sigmaX"_a, "sigmaY"_a, "tileMode"_a = SkTileMode::kDecal, "input"_a = py::none(), "cropRect"_a = dcr)
        .def_static("ColorFilter", &SkImageFilters::ColorFilter, "cf"_a, "input"_a = py::none(), "cropRect"_a = dcr)
        .def_static("Compose", &SkImageFilters::Compose, "outer"_a, "inner"_a)
        .def_static("DisplacementMap", &SkImageFilters::DisplacementMap, "xChannelSelector"_a, "yChannelSelector"_a,
                    "scale"_a, "displacement"_a, "color"_a = py::none(), "cropRect"_a = dcr)
        .def_static("DropShadow", &SkImageFilters::DropShadow, "dx"_a, "dy"_a, "sigmaX"_a, "sigmaY"_a, "color"_a,
                    "input"_a = py::none(), "cropRect"_a = dcr)
        .def_static("DropShadowOnly", &SkImageFilters::DropShadowOnly, "dx"_a, "dy"_a, "sigmaX"_a, "sigmaY"_a,
                    "color"_a, "input"_a = py::none(), "cropRect"_a = dcr)
        .def_static("Empty", &SkImageFilters::Empty)
        .def_static(
            "Image",
            [](const sk_sp<SkImage> &image, const std::optional<SkRect> &srcRect, const std::optional<SkRect> &dstRect,
               const SkSamplingOptions &sampling)
            {
                if (!(srcRect && dstRect))
                    return SkImageFilters::Image(image, sampling);
                return SkImageFilters::Image(image, *srcRect, *dstRect, sampling);
            },
            "image"_a, "srcRect"_a = py::none(), "dstRect"_a = py::none(), "sampling"_a = dso)
        .def_static("Magnifier", &SkImageFilters::Magnifier, "lensBounds"_a, "zoomAmount"_a, "inset"_a,
                    "sampling"_a = dso, "input"_a = nullptr, "cropRect"_a = dcr)
        .def_static(
            "MatrixConvolution",
            [](const SkISize &kernelSize, const std::vector<SkScalar> &kernel, const SkScalar &gain,
               const SkScalar &bias, const std::optional<const SkIPoint> &kernelOffset, const SkTileMode &tileMode,
               const bool &convolveAlpha, const sk_sp<SkImageFilter> &input, const SkImageFilters::CropRect &cropRect)
            {
                const int width = kernelSize.width(), height = kernelSize.height();
                const size_t requiredSize = width * height, actualSize = kernel.size();
                if (requiredSize != actualSize)
                    throw py::value_error("kernel size must be {}, got {}"_s.format(requiredSize, actualSize));
                return SkImageFilters::MatrixConvolution(kernelSize, kernel.data(), gain, bias,
                                                         kernelOffset ? *kernelOffset : SkIPoint{width / 2, height / 2},
                                                         tileMode, convolveAlpha, input, cropRect);
            },
            "If *kernelOffset* is not specified, it is assumed to be half the kernel width and height.", "kernelSize"_a,
            "kernel"_a, "gain"_a = 1, "bias"_a = 0, "kernelOffset"_a = std::nullopt, "tileMode"_a = SkTileMode::kClamp,
            "convolveAlpha"_a = false, "input"_a = py::none(), "cropRect"_a = dcr)
        .def_static("MatrixTransform", &SkImageFilters::MatrixTransform, "matrix"_a, "sampling"_a = dso,
                    "input"_a = nullptr)
        .def_static(
            "Merge",
            [](const py::list &filters, const SkImageFilters::CropRect &cropRect)
            {
                const size_t size = filters.size();
                std::vector<sk_sp<SkImageFilter>> filters_(size);
                for (size_t i = 0; i < size; ++i)
                {
                    const auto filter = filters[i];
                    filters_[i] = filter.is_none() ? nullptr : filter.cast<sk_sp<SkImageFilter>>();
                }
                return SkImageFilters::Merge(filters_.data(), size, cropRect);
            },
            R"doc(
                Create a filter that merges the *filters* together by drawing their results in order with src-over
                blending. If any of the filters is ``None``, the source bitmap is used.
            )doc",
            "filters"_a, "cropRect"_a = dcr)
        .def_static("Merge",
                    py::overload_cast<sk_sp<SkImageFilter>, sk_sp<SkImageFilter>, const SkImageFilters::CropRect &>(
                        &SkImageFilters::Merge),
                    "first"_a, "second"_a, "cropRect"_a = dcr)
        .def_static("Offset", &SkImageFilters::Offset, "dx"_a, "dy"_a, "input"_a = py::none(), "cropRect"_a = dcr)
        .def_static("Picture", py::overload_cast<sk_sp<SkPicture>, const SkRect &>(&SkImageFilters::Picture), "pic"_a,
                    "targetRect"_a)
        .def_static("Picture", py::overload_cast<sk_sp<SkPicture>>(&SkImageFilters::Picture), "pic"_a)
        .def_static(
            "RuntimeShader",
            [](const SkRuntimeShaderBuilder &builder, const SkScalar &sampleRadius,
               const std::string_view &childShaderName, const sk_sp<SkImageFilter> &input)
            { return SkImageFilters::RuntimeShader(builder, sampleRadius, childShaderName, input); },
            "builder"_a, "sampleRadius"_a = 0, "childShaderName"_a = "", "input"_a = nullptr)
        .def_static(
            "RuntimeShader",
            [](const SkRuntimeShaderBuilder &builder, std::vector<std::string_view> &childShaderNames,
               const std::vector<sk_sp<SkImageFilter>> &inputs, const SkScalar &maxSampleRadius)
            {
                const size_t size = childShaderNames.size();
                if (inputs.size() != size)
                    throw py::value_error("childShaderNames and inputs must be the same length");
                return SkImageFilters::RuntimeShader(builder, maxSampleRadius, childShaderNames.data(), inputs.data(),
                                                     size);
            },
            "Note that the *maxSampleRadius* parameter is at the end of the argument list, unlike the C++ API.",
            "builder"_a, "childShaderNames"_a, "inputs"_a, "maxSampleRadius"_a = 0);

    py::enum_<SkImageFilters::Dither>(ImageFilters, "Dither")
        .value("kNo", SkImageFilters::Dither::kNo)
        .value("kYes", SkImageFilters::Dither::kYes);
    ImageFilters
        .def_static("Shader",
                    py::overload_cast<sk_sp<SkShader>, SkImageFilters::Dither, const SkImageFilters::CropRect &>(
                        &SkImageFilters::Shader),
                    "shader"_a, "dither"_a = SkImageFilters::Dither::kNo, "cropRect"_a = dcr)
        .def_static("Tile", &SkImageFilters::Tile, "src"_a, "dst"_a, "input"_a = py::none())
        .def_static("Dilate", &SkImageFilters::Dilate, "radiusX"_a, "radiusY"_a, "input"_a = py::none(),
                    "cropRect"_a = dcr)
        .def_static("Erode", &SkImageFilters::Erode, "radiusX"_a, "radiusY"_a, "input"_a = py::none(),
                    "cropRect"_a = dcr)
        .def_static("DistantLitDiffuse", &SkImageFilters::DistantLitDiffuse, "direction"_a, "lightColor"_a,
                    "surfaceScale"_a, "kd"_a, "input"_a = py::none(), "cropRect"_a = dcr)
        .def_static("PointLitDiffuse", &SkImageFilters::PointLitDiffuse, "location"_a, "lightColor"_a, "surfaceScale"_a,
                    "kd"_a, "input"_a = py::none(), "cropRect"_a = dcr)
        .def_static("SpotLitDiffuse", &SkImageFilters::SpotLitDiffuse, "location"_a, "target"_a, "falloffExponent"_a,
                    "cutoffAngle"_a, "lightColor"_a, "surfaceScale"_a, "kd"_a, "input"_a = py::none(),
                    "cropRect"_a = dcr)
        .def_static("DistantLitSpecular", &SkImageFilters::DistantLitSpecular, "direction"_a, "lightColor"_a,
                    "surfaceScale"_a, "ks"_a, "shininess"_a, "input"_a = py::none(), "cropRect"_a = dcr)
        .def_static("PointLitSpecular", &SkImageFilters::PointLitSpecular, "location"_a, "lightColor"_a,
                    "surfaceScale"_a, "ks"_a, "shininess"_a, "input"_a = py::none(), "cropRect"_a = dcr)
        .def_static("SpotLitSpecular", &SkImageFilters::SpotLitSpecular, "location"_a, "target"_a, "falloffExponent"_a,
                    "cutoffAngle"_a, "lightColor"_a, "surfaceScale"_a, "ks"_a, "shininess"_a, "input"_a = py::none(),
                    "cropRect"_a = dcr);
}