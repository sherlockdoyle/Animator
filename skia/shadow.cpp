#include "common.h"
#include "include/core/SkCanvas.h"
#include "include/core/SkMatrix.h"
#include "include/core/SkPath.h"
#include "include/core/SkPoint3.h"
#include "include/utils/SkShadowUtils.h"

void initShadow(py::module &m)
{
    py::enum_<SkShadowFlags>(m, "ShadowFlags", py::arithmetic())
        .value("kNone_ShadowFlag", SkShadowFlags::kNone_ShadowFlag)
        .value("kTransparentOccluder_ShadowFlag", SkShadowFlags::kTransparentOccluder_ShadowFlag)
        .value("kGeometricOnly_ShadowFlag", SkShadowFlags::kGeometricOnly_ShadowFlag)
        .value("kDirectionalLight_ShadowFlag", SkShadowFlags::kDirectionalLight_ShadowFlag)
        .value("kConcaveBlurOnly_ShadowFlag", SkShadowFlags::kConcaveBlurOnly_ShadowFlag)
        .value("kAll_ShadowFlag", SkShadowFlags::kAll_ShadowFlag);

    py::class_<SkShadowUtils>(m, "ShadowUtils")
        .def_static("DrawShadow", &SkShadowUtils::DrawShadow, "canvas"_a, "path"_a, "zPlaneParams"_a, "lightPos"_a,
                    "lightRadius"_a, "ambientColor"_a, "spotColor"_a, "flags"_a = SkShadowFlags::kNone_ShadowFlag)
        .def_static(
            "GetLocalBounds",
            [](const SkMatrix &ctm, const SkPath &path, const SkPoint3 &zPlaneParams, const SkPoint3 &lightPos,
               const SkScalar &lightRadius, const uint32_t &flags)
            {
                SkRect bounds;
                if (SkShadowUtils::GetLocalBounds(ctm, path, zPlaneParams, lightPos, lightRadius, flags, &bounds))
                    return bounds;
                throw std::runtime_error("Failed to get local bounds.");
            },
            "Return bounding box for shadows relative to path. Includes both the ambient and spot shadow bounds.",
            "ctm"_a, "path"_a, "zPlaneParams"_a, "lightPos"_a, "lightRadius"_a,
            "flags"_a = SkShadowFlags::kNone_ShadowFlag)
        .def_static(
            "ComputeTonalColors",
            [](const SkColor &inAmbientColor, const SkColor &inSpotColor)
            {
                SkColor outAmbientColor, outSpotColor;
                SkShadowUtils::ComputeTonalColors(inAmbientColor, inSpotColor, &outAmbientColor, &outSpotColor);
                return std::make_tuple(outAmbientColor, outSpotColor);
            },
            "Compute and return color values for one-pass tonal alpha.", "inAmbientColor"_a, "inSpotColor"_a);
}