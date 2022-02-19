#include "common.h"
#include "include/core/SkColorSpace.h"
#include "include/core/SkData.h"
#include <pybind11/stl.h>

void initColorSpace(py::module &m)
{
    py::class_<SkColorSpacePrimaries>(m, "ColorSpacePrimaries")
        .def(py::init())
        .def(py::init([](const float &fRX, const float &fRY, const float &fGX, const float &fGY, const float &fBX,
                         const float &fBY, const float &fWX, const float &fWY)
                      { return SkColorSpacePrimaries{fRX, fRY, fGX, fGY, fBX, fBY, fWX, fWY}; }),
             "fRX"_a, "fRY"_a, "fGX"_a, "fGY"_a, "fBX"_a, "fBY"_a, "fWX"_a, "fWY"_a)
        .def_readwrite("fRX", &SkColorSpacePrimaries::fRX)
        .def_readwrite("fRY", &SkColorSpacePrimaries::fRY)
        .def_readwrite("fGX", &SkColorSpacePrimaries::fGX)
        .def_readwrite("fGY", &SkColorSpacePrimaries::fGY)
        .def_readwrite("fBX", &SkColorSpacePrimaries::fBX)
        .def_readwrite("fBY", &SkColorSpacePrimaries::fBY)
        .def_readwrite("fWX", &SkColorSpacePrimaries::fWX)
        .def_readwrite("fWY", &SkColorSpacePrimaries::fWY)
        .def("toXYZD50",
             [](const SkColorSpacePrimaries &primaries)
             {
                 skcms_Matrix3x3 toXYZD50;
                 primaries.toXYZD50(&toXYZD50);
                 return toXYZD50;
             });

    py::module NamedTransferFn = m.def_submodule("NamedTransferFn", "Try not to write to these attributes! :)");
    NamedTransferFn.attr("kSRGB") = &SkNamedTransferFn::kSRGB;
    NamedTransferFn.attr("k2Dot2") = &SkNamedTransferFn::k2Dot2;
    NamedTransferFn.attr("kLinear") = &SkNamedTransferFn::kLinear;
    NamedTransferFn.attr("kRec2020") = &SkNamedTransferFn::kRec2020;
    NamedTransferFn.attr("kPQ") = &SkNamedTransferFn::kPQ;
    NamedTransferFn.attr("kHLG") = &SkNamedTransferFn::kHLG;

    py::module NamedGamut = m.def_submodule("NamedGamut", "Try not to write to these attributes! :)");
    NamedGamut.attr("kSRGB") = &SkNamedGamut::kSRGB;
    NamedGamut.attr("kAdobeRGB") = &SkNamedGamut::kAdobeRGB;
    NamedGamut.attr("kDisplayP3") = &SkNamedGamut::kDisplayP3;
    NamedGamut.attr("kRec2020") = &SkNamedGamut::kRec2020;
    NamedGamut.attr("kXYZ") = &SkNamedGamut::kXYZ;

    py::class_<SkColorSpace, sk_sp<SkColorSpace>>(m, "ColorSpace")
        .def(py::init(&SkColorSpace::Make), "profile"_a)
        .def_static("MakeSRGB", &SkColorSpace::MakeSRGB)
        .def_static("MakeSRGBLinear", &SkColorSpace::MakeSRGBLinear)
        .def_static("MakeRGB", &SkColorSpace::MakeRGB, "transferFn"_a, "toXYZ"_a)
        .def_static("Make", &SkColorSpace::Make, "profile"_a)
        .def(
            "toProfile",
            [](const SkColorSpace &colorspace)
            {
                std::unique_ptr<skcms_ICCProfile> profile(new skcms_ICCProfile());
                colorspace.toProfile(profile.get());
                return profile;
            },
            "Convert this color space to an skcms ICC profile struct and return it.")
        .def("gammaCloseToSRGB", &SkColorSpace::gammaCloseToSRGB)
        .def("gammaIsLinear", &SkColorSpace::gammaIsLinear)
        .def(
            "isNumericalTransferFn",
            [](const SkColorSpace &colorspace) -> std::optional<skcms_TransferFunction>
            {
                skcms_TransferFunction tf;
                if (colorspace.isNumericalTransferFn(&tf))
                    return tf;
                return std::nullopt;
            },
            R"doc(
                Returns the transfer function from this color space if the transfer function can be represented as
                coefficients to the standard ICC 7-parameter equation. Returns ``None`` otherwise (eg, PQ, HLG).

                :return: The transfer function from this color space.
                :rtype: skia.cms.TransferFunction | None
           )doc")
        .def(
            "toXYZD50",
            [](const SkColorSpace &colorspace) -> std::optional<skcms_Matrix3x3>
            {
                skcms_Matrix3x3 toXYZD50;
                if (colorspace.toXYZD50(&toXYZD50))
                    return toXYZD50;
                return std::nullopt;
            },
            R"doc(
                Returns the matrix if the color gamut can be described as a matrix. Returns ``None`` otherwise.

                :return: The matrix describing this color space.
                :rtype: skia.cms.Matrix3x3 | None
           )doc")
        .def("toXYZD50Hash", &SkColorSpace::toXYZD50Hash)
        .def("makeLinearGamma", &SkColorSpace::makeLinearGamma)
        .def("makeSRGBGamma", &SkColorSpace::makeSRGBGamma)
        .def("makeColorSpin", &SkColorSpace::makeColorSpin)
        .def("isSRGB", &SkColorSpace::isSRGB)
        .def("serialize", &SkColorSpace::serialize)
        .def_static(
            "Deserialize",
            [](const py::buffer &buffer)
            {
                py::buffer_info info = buffer.request();
                return SkColorSpace::Deserialize(info.ptr, info.size * info.itemsize);
            },
            "Deserialize a color space from a buffer.", "buffer"_a)
        .def_static("Equals", &SkColorSpace::Equals, "x"_a, "y"_a)
        .def("__eq__", &SkColorSpace::Equals, py::is_operator())
        .def(
            "transferFn",
            [](const SkColorSpace &colorspace)
            {
                skcms_TransferFunction tf;
                colorspace.transferFn(&tf);
                return tf;
            },
            "Returns the transfer function from this color space.")
        .def(
            "invTransferFn",
            [](const SkColorSpace &colorspace)
            {
                skcms_TransferFunction tf;
                colorspace.invTransferFn(&tf);
                return tf;
            },
            R"doc(
                Returns the inverse transfer function from this color space.
            )doc")
        .def(
            "gamutTransformTo",
            [](const SkColorSpace &colorspace, const SkColorSpace &dst)
            {
                skcms_Matrix3x3 src_to_dst;
                colorspace.gamutTransformTo(&dst, &src_to_dst);
                return src_to_dst;
            },
            R"doc(
                Returns the matrix that transforms from this color space to the destination color space.

                :param skia.ColorSpace dst: The destination color space.
                :return: The matrix that transforms from this color space to the destination color space.
                :rtype: skia.cms.Matrix3x3
            )doc",
            "dst"_a)
        .def("transferFnHash", &SkColorSpace::transferFnHash)
        .def("hash", &SkColorSpace::hash)
        .def("__hash__", &SkColorSpace::hash)
        .def("__str__",
             [](const SkColorSpace &colorspace)
             {
                 std::stringstream s;
                 s << "ColorSpace(";
                 skcms_TransferFunction tf;
                 colorspace.transferFn(&tf);
                 s << "transferFn=" << py::cast(tf).attr("__str__")();
                 skcms_Matrix3x3 toXYZD50;
                 if (colorspace.toXYZD50(&toXYZD50))
                     s << ", XYZD50=" << py::cast(toXYZD50).attr("__str__")();
                 s << ")";
                 return s.str();
             });
}