#include "common.h"
#include "include/core/SkBlendMode.h"
#include "include/core/SkBlender.h"
#include "include/effects/SkBlenders.h"

void initBlendMode(py::module &m)
{
    py::enum_<SkBlendMode> BlendMode(m, "BlendMode");
    BlendMode.value("kClear", SkBlendMode::kClear)
        .value("kSrc", SkBlendMode::kSrc)
        .value("kDst", SkBlendMode::kDst)
        .value("kSrcOver", SkBlendMode::kSrcOver)
        .value("kDstOver", SkBlendMode::kDstOver)
        .value("kSrcIn", SkBlendMode::kSrcIn)
        .value("kDstIn", SkBlendMode::kDstIn)
        .value("kSrcOut", SkBlendMode::kSrcOut)
        .value("kDstOut", SkBlendMode::kDstOut)
        .value("kSrcATop", SkBlendMode::kSrcATop)
        .value("kDstATop", SkBlendMode::kDstATop)
        .value("kXor", SkBlendMode::kXor)
        .value("kPlus", SkBlendMode::kPlus)
        .value("kModulate", SkBlendMode::kModulate)
        .value("kScreen", SkBlendMode::kScreen)
        .value("kOverlay", SkBlendMode::kOverlay)
        .value("kDarken", SkBlendMode::kDarken)
        .value("kLighten", SkBlendMode::kLighten)
        .value("kColorDodge", SkBlendMode::kColorDodge)
        .value("kColorBurn", SkBlendMode::kColorBurn)
        .value("kHardLight", SkBlendMode::kHardLight)
        .value("kSoftLight", SkBlendMode::kSoftLight)
        .value("kDifference", SkBlendMode::kDifference)
        .value("kExclusion", SkBlendMode::kExclusion)
        .value("kMultiply", SkBlendMode::kMultiply)
        .value("kHue", SkBlendMode::kHue)
        .value("kSaturation", SkBlendMode::kSaturation)
        .value("kColor", SkBlendMode::kColor)
        .value("kLuminosity", SkBlendMode::kLuminosity)
        .value("kLastCoeffMode", SkBlendMode::kLastCoeffMode)
        .value("kLastSeparableMode", SkBlendMode::kLastSeparableMode)
        .value("kLastMode", SkBlendMode::kLastMode);

    py::enum_<SkBlendModeCoeff>(m, "BlendModeCoeff")
        .value("kZero", SkBlendModeCoeff::kZero)
        .value("kOne", SkBlendModeCoeff::kOne)
        .value("kSC", SkBlendModeCoeff::kSC)
        .value("kISC", SkBlendModeCoeff::kISC)
        .value("kDC", SkBlendModeCoeff::kDC)
        .value("kIDC", SkBlendModeCoeff::kIDC)
        .value("kSA", SkBlendModeCoeff::kSA)
        .value("kISA", SkBlendModeCoeff::kISA)
        .value("kDA", SkBlendModeCoeff::kDA)
        .value("kIDA", SkBlendModeCoeff::kIDA)
        .value("kCoeffCount", SkBlendModeCoeff::kCoeffCount);

    BlendMode
        .def(
            "asCoeff",
            [](const SkBlendMode &self) -> std::optional<py::tuple>
            {
                SkBlendModeCoeff src, dst;
                if (SkBlendMode_AsCoeff(self, &src, &dst))
                    return py::make_tuple(src, dst);
                else
                    return py::none();
            },
            "Returns the source and destination coefficients for the coeffient-based blend mode, or None otherwise.")
        .def("name_", &SkBlendMode_Name, "Returns name of blend mode as returned by the C++ API.");

    py::class_<SkBlender, sk_sp<SkBlender>, SkFlattenable>(m, "Blender").def_static("Mode", &SkBlender::Mode, "mode"_a);

    py::class_<SkBlenders>(m, "Blenders")
        .def_static("Arithmetic", &SkBlenders::Arithmetic, "k1"_a, "k2"_a, "k3"_a, "k4"_a, "enforcePremul"_a = false);
}