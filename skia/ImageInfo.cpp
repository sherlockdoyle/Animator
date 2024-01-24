#include "common.h"
#include "include/core/SkColorSpace.h"
#include "include/core/SkImageInfo.h"
#include <pybind11/operators.h>
#include <pybind11/stl.h>

void initImageInfo(py::module &m)
{
    py::enum_<SkAlphaType>(m, "AlphaType")
        .value("kUnknown_AlphaType", SkAlphaType::kUnknown_SkAlphaType)
        .value("kOpaque_AlphaType", SkAlphaType::kOpaque_SkAlphaType)
        .value("kPremul_AlphaType", SkAlphaType::kPremul_SkAlphaType)
        .value("kUnpremul_AlphaType", SkAlphaType::kUnpremul_SkAlphaType)
        .value("kLastEnum_AlphaType", SkAlphaType::kLastEnum_SkAlphaType)
        .def("isOpaque", &SkAlphaTypeIsOpaque,
             R"doc(
                Returns true if this alpha type is opaque (*kOpaque_AlphaType*).

                *kOpaque_AlphaType* is a hint that the ColorType is opaque, or that all alpha values are set to their
                1.0 equivalent. If :py:class:`AlphaType` is *kOpaque_AlphaType*, and :py:class:`ColorType` is not
                opaque, then the result of drawing any pixel with a alpha value less than 1.0 is undefined.
            )doc");

    py::enum_<SkColorType>(m, "ColorType")
        .value("kUnknown_ColorType", SkColorType::kUnknown_SkColorType)
        .value("kAlpha_8_ColorType", SkColorType::kAlpha_8_SkColorType)
        .value("kRGB_565_ColorType", SkColorType::kRGB_565_SkColorType)
        .value("kARGB_4444_ColorType", SkColorType::kARGB_4444_SkColorType)
        .value("kRGBA_8888_ColorType", SkColorType::kRGBA_8888_SkColorType)
        .value("kRGB_888x_ColorType", SkColorType::kRGB_888x_SkColorType)
        .value("kBGRA_8888_ColorType", SkColorType::kBGRA_8888_SkColorType)
        .value("kRGBA_1010102_ColorType", SkColorType::kRGBA_1010102_SkColorType)
        .value("kBGRA_1010102_ColorType", SkColorType::kBGRA_1010102_SkColorType)
        .value("kRGB_101010x_ColorType", SkColorType::kRGB_101010x_SkColorType)
        .value("kBGR_101010x_ColorType", SkColorType::kBGR_101010x_SkColorType)
        .value("kBGR_101010x_XR_ColorType", SkColorType::kBGR_101010x_XR_SkColorType)
        .value("kRGBA_10x6_ColorType", SkColorType::kRGBA_10x6_SkColorType)
        .value("kGray_8_ColorType", SkColorType::kGray_8_SkColorType)
        .value("kRGBA_F16Norm_ColorType", SkColorType::kRGBA_F16Norm_SkColorType)
        .value("kRGBA_F16_ColorType", SkColorType::kRGBA_F16_SkColorType)
        .value("kRGBA_F32_ColorType", SkColorType::kRGBA_F32_SkColorType)
        .value("kR8G8_unorm_ColorType", SkColorType::kR8G8_unorm_SkColorType)
        .value("kA16_float_ColorType", SkColorType::kA16_float_SkColorType)
        .value("kR16G16_float_ColorType", SkColorType::kR16G16_float_SkColorType)
        .value("kA16_unorm_ColorType", SkColorType::kA16_unorm_SkColorType)
        .value("kR16G16_unorm_ColorType", SkColorType::kR16G16_unorm_SkColorType)
        .value("kR16G16B16A16_unorm_ColorType", SkColorType::kR16G16B16A16_unorm_SkColorType)
        .value("kSRGBA_8888_ColorType", SkColorType::kSRGBA_8888_SkColorType)
        .value("kR8_unorm_ColorType", SkColorType::kR8_unorm_SkColorType)
        .value("kLastEnum_ColorType", SkColorType::kLastEnum_SkColorType)
        .value("kN32_ColorType", SkColorType::kN32_SkColorType)
        .def("bytesPerPixel", &SkColorTypeBytesPerPixel,
             R"doc(
                Returns the number of bytes required to store a pixel, including unused padding. Returns zero if this
                is *kUnknown_ColorType* or invalid.

                :return: bytes per pixel
            )doc")
        .def("isAlwaysOpaque", &SkColorTypeIsAlwaysOpaque,
             R"doc(
                Returns true if :py:class:`ColorType` always decodes alpha to 1.0, making the pixel fully opaque. If
                ``True``, :py:class:`ColorType` does not reserve bits to encode alpha.

                :return: true if alpha is always set to 1.0
            )doc")
        .def(
            "validateAlphaType",
            [](const SkColorType &colorType, const SkAlphaType &alphaType) -> std::optional<SkAlphaType>
            {
                SkAlphaType canonical;
                if (SkColorTypeValidateAlphaType(colorType, alphaType, &canonical))
                    return canonical;
                return std::nullopt;
            },
            R"doc(
                Returns a :py:class:`AlphaType` if this *colorType* has a valid :py:class:`AlphaType`.

                Returns ``None`` only if *alphaType* is :py:attr:`~skia.Type.kUnknown_AlphaType`, color type is not
                :py:attr:`~skia.ColorType.kUnknown_ColorType`, and :py:class:`ColorType` is not always opaque.

                :param alphaType: alpha type
                :return: alpha type for this color type, or ``None``
                :rtype: :py:class:`AlphaType` | None
            )doc",
            "alphaType"_a);

    py::enum_<SkYUVColorSpace>(m, "YUVColorSpace")
        .value("kJPEG_Full_YUVColorSpace", SkYUVColorSpace::kJPEG_Full_SkYUVColorSpace)
        .value("kRec601_Limited_YUVColorSpace", SkYUVColorSpace::kRec601_Limited_SkYUVColorSpace)
        .value("kRec709_Full_YUVColorSpace", SkYUVColorSpace::kRec709_Full_SkYUVColorSpace)
        .value("kRec709_Limited_YUVColorSpace", SkYUVColorSpace::kRec709_Limited_SkYUVColorSpace)
        .value("kBT2020_8bit_Full_YUVColorSpace", SkYUVColorSpace::kBT2020_8bit_Full_SkYUVColorSpace)
        .value("kBT2020_8bit_Limited_YUVColorSpace", SkYUVColorSpace::kBT2020_8bit_Limited_SkYUVColorSpace)
        .value("kBT2020_10bit_Full_YUVColorSpace", SkYUVColorSpace::kBT2020_10bit_Full_SkYUVColorSpace)
        .value("kBT2020_10bit_Limited_YUVColorSpace", SkYUVColorSpace::kBT2020_10bit_Limited_SkYUVColorSpace)
        .value("kBT2020_12bit_Full_YUVColorSpace", SkYUVColorSpace::kBT2020_12bit_Full_SkYUVColorSpace)
        .value("kBT2020_12bit_Limited_YUVColorSpace", SkYUVColorSpace::kBT2020_12bit_Limited_SkYUVColorSpace)
        .value("kIdentity_YUVColorSpace", SkYUVColorSpace::kIdentity_SkYUVColorSpace)
        .value("kLastEnum_YUVColorSpace", SkYUVColorSpace::kLastEnum_SkYUVColorSpace)
        .value("kJPEG_YUVColorSpace", SkYUVColorSpace::kJPEG_SkYUVColorSpace)
        .value("kRec601_YUVColorSpace", SkYUVColorSpace::kRec601_SkYUVColorSpace)
        .value("kRec709_YUVColorSpace", SkYUVColorSpace::kRec709_SkYUVColorSpace)
        .value("kBT2020_YUVColorSpace", SkYUVColorSpace::kBT2020_SkYUVColorSpace);

    py::class_<SkColorInfo>(m, "ColorInfo")
        .def(py::init())
        .def(py::init<SkColorType, SkAlphaType, sk_sp<SkColorSpace>>(), "ct"_a, "at"_a, "cs"_a = py::none())
        .def(py::init<const SkColorInfo &>())
        .def("colorSpace", &SkColorInfo::colorSpace, py::return_value_policy::reference_internal)
        .def("refColorSpace", &SkColorInfo::refColorSpace)
        .def("colorType", &SkColorInfo::colorType)
        .def("alphaType", &SkColorInfo::alphaType)
        .def("isOpaque", &SkColorInfo::isOpaque)
        .def("gammaCloseToSRGB", &SkColorInfo::gammaCloseToSRGB)
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def("makeAlphaType", &SkColorInfo::makeAlphaType, "newAlphaType"_a)
        .def("makeColorType", &SkColorInfo::makeColorType, "newColorType"_a)
        .def("makeColorSpace", &SkColorInfo::makeColorSpace, "cs"_a)
        .def("bytesPerPixel", &SkColorInfo::bytesPerPixel)
        .def("shiftPerPixel", &SkColorInfo::shiftPerPixel)
        .def("__str__",
             [](const SkColorInfo &info)
             {
                 return "ColorInfo(colorType={}, alphaType={}, colorSpace={})"_s.format(
                     info.colorType(), info.alphaType(), info.colorSpace());
             });

    py::class_<SkImageInfo>(m, "ImageInfo",
                            ":note: The :py:meth:`~ImageInfo.Make` methods are also available as constructors.")
        .def(py::init())
        .def_static("Make",
                    py::overload_cast<int, int, SkColorType, SkAlphaType, sk_sp<SkColorSpace>>(&SkImageInfo::Make),
                    "width"_a, "height"_a, "ct"_a, "at"_a, "cs"_a = nullptr)
        .def(py::init(py::overload_cast<int, int, SkColorType, SkAlphaType, sk_sp<SkColorSpace>>(&SkImageInfo::Make)),
             "width"_a, "height"_a, "ct"_a, "at"_a, "cs"_a = py::none())
        .def_static("Make",
                    py::overload_cast<SkISize, SkColorType, SkAlphaType, sk_sp<SkColorSpace>>(&SkImageInfo::Make),
                    "dimensions"_a, "ct"_a, "at"_a, "cs"_a = py::none())
        .def(py::init(py::overload_cast<SkISize, SkColorType, SkAlphaType, sk_sp<SkColorSpace>>(&SkImageInfo::Make)),
             "dimensions"_a, "ct"_a, "at"_a, "cs"_a = py::none())
        .def_static("Make", py::overload_cast<SkISize, const SkColorInfo &>(&SkImageInfo::Make), "dimensions"_a,
                    "colorInfo"_a)
        .def(py::init(py::overload_cast<SkISize, const SkColorInfo &>(&SkImageInfo::Make)), "dimensions"_a,
             "colorInfo"_a)
        .def_static("MakeN32", py::overload_cast<int, int, SkAlphaType, sk_sp<SkColorSpace>>(&SkImageInfo::MakeN32),
                    "width"_a, "height"_a, "at"_a, "cs"_a = py::none())
        .def_static("MakeS32", &SkImageInfo::MakeS32, "width"_a, "height"_a, "at"_a)
        .def_static("MakeN32Premul", py::overload_cast<int, int, sk_sp<SkColorSpace>>(&SkImageInfo::MakeN32Premul),
                    "width"_a, "height"_a, "cs"_a = py::none())
        .def_static("MakeN32Premul", py::overload_cast<SkISize, sk_sp<SkColorSpace>>(&SkImageInfo::MakeN32Premul),
                    "dimensions"_a, "cs"_a = nullptr)
        .def_static("MakeA8", py::overload_cast<int, int>(&SkImageInfo::MakeA8), "width"_a, "height"_a)
        .def_static("MakeA8", py::overload_cast<SkISize>(&SkImageInfo::MakeA8), "dimensions"_a)
        .def_static("MakeUnknown", py::overload_cast<int, int>(&SkImageInfo::MakeUnknown), "width"_a, "height"_a)
        .def_static("MakeUnknown", py::overload_cast<>(&SkImageInfo::MakeUnknown))
        .def("width", &SkImageInfo::width)
        .def("height", &SkImageInfo::height)
        .def("colorType", &SkImageInfo::colorType)
        .def("alphaType", &SkImageInfo::alphaType)
        .def("colorSpace", &SkImageInfo::colorSpace, py::return_value_policy::reference_internal)
        .def("refColorSpace", &SkImageInfo::refColorSpace)
        .def("isEmpty", &SkImageInfo::isEmpty)
        .def("colorInfo", &SkImageInfo::colorInfo, py::return_value_policy::reference_internal)
        .def("isOpaque", &SkImageInfo::isOpaque)
        .def("dimensions", &SkImageInfo::dimensions)
        .def("bounds", &SkImageInfo::bounds)
        .def("gammaCloseToSRGB", &SkImageInfo::gammaCloseToSRGB)
        .def("makeWH", &SkImageInfo::makeWH, "newWidth"_a, "newHeight"_a)
        .def("makeDimensions", &SkImageInfo::makeDimensions, "newSize"_a)
        .def("makeAlphaType", &SkImageInfo::makeAlphaType, "newAlphaType"_a)
        .def("makeColorType", &SkImageInfo::makeColorType, "newColorType"_a)
        .def("makeColorSpace", &SkImageInfo::makeColorSpace, "cs"_a)
        .def("bytesPerPixel", &SkImageInfo::bytesPerPixel)
        .def("shiftPerPixel", &SkImageInfo::shiftPerPixel)
        .def("minRowBytes64", &SkImageInfo::minRowBytes64)
        .def("minRowBytes", &SkImageInfo::minRowBytes)
        .def("computeOffset", &SkImageInfo::computeOffset, "x"_a, "y"_a, "rowBytes"_a)
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def("computeByteSize", &SkImageInfo::computeByteSize, "rowBytes"_a)
        .def("computeMinByteSize", &SkImageInfo::computeMinByteSize)
        .def_static("ByteSizeOverflowed", &SkImageInfo::ByteSizeOverflowed, "byteSize"_a)
        .def("validRowBytes", &SkImageInfo::validRowBytes, "rowBytes"_a)
        .def("reset", &SkImageInfo::reset)
        .def("__str__",
             [](const SkImageInfo &info)
             {
                 return "ImageInfo(width={}, height={}, colorType={}, alphaType={}, colorSpace={})"_s.format(
                     info.width(), info.height(), info.colorType(), info.alphaType(), info.colorSpace());
             });
}