#include "common.h"

SkImageInfo ndarrayToImageInfo(const py::array &array, const SkColorType &ct, const SkAlphaType &at,
                               const sk_sp<SkColorSpace> &cs)
{
    if (!(array.flags() & py::array::c_style))
        throw py::value_error("Array must be c-style contiguous");
    if (array.ndim() < 2)
        throw py::value_error("Array must have at least 2 dimensions");
    if (array.shape(0) == 0 || array.shape(1) == 0)
        throw py::value_error("Array must have at least 1 element");
    SkImageInfo info = SkImageInfo::Make(array.shape(1), array.shape(0), ct, at, cs);
    const int pixelSize = array.ndim() == 2 ? array.strides(1) : array.strides(2) * array.shape(2);
    if (pixelSize != info.bytesPerPixel())
        throw py::value_error(
            "Incorrect number of channels (expected {} but got {})"_s.format(info.bytesPerPixel(), pixelSize));
    return info;
}

size_t validateImageInfo_Buffer(const SkImageInfo &imgInfo, const py::buffer_info &bufInfo, size_t rowBytes)
{
    if (rowBytes == 0)
        rowBytes = imgInfo.minRowBytes();
    else if (!imgInfo.validRowBytes(rowBytes))
        throw py::value_error(
            "rowBytes is too small (expected at least {} but got {})"_s.format(imgInfo.minRowBytes(), rowBytes));
    const size_t bufInfoSize = bufInfo.size * bufInfo.itemsize, imgInfoSize = imgInfo.computeByteSize(rowBytes);
    if (bufInfoSize < imgInfoSize)
        throw py::value_error(
            "buffer is too small (expected at least {} but got {})"_s.format(imgInfoSize, bufInfoSize));
    return rowBytes;
}

py::buffer_info imageInfoToBufferInfo(const SkImageInfo &imgInfo, void *data, py::ssize_t rowBytes, bool readonly)
{
    py::ssize_t width = imgInfo.width(), height = imgInfo.height(), bytesPerPixel = imgInfo.bytesPerPixel();
    if (!rowBytes)
        rowBytes = imgInfo.minRowBytes();
    switch (imgInfo.colorType())
    {
    case kAlpha_8_SkColorType:
    case kGray_8_SkColorType:
        return py::buffer_info(data, bytesPerPixel, "B", 2, {height, width}, {rowBytes, bytesPerPixel}, readonly);

    case kRGB_565_SkColorType:
    case kARGB_4444_SkColorType:
        return py::buffer_info(data, bytesPerPixel, "H", 2, {height, width}, {rowBytes, bytesPerPixel}, readonly);

    case kRGBA_8888_SkColorType:
    case kRGB_888x_SkColorType:
    case kBGRA_8888_SkColorType:
        return py::buffer_info(data, 1, "B", 3, {height, width, py::ssize_t(4)},
                               {rowBytes, bytesPerPixel, py::ssize_t(1)}, readonly);

    case kRGBA_1010102_SkColorType:
    case kBGRA_1010102_SkColorType:
    case kRGB_101010x_SkColorType:
    case kBGR_101010x_SkColorType:
        return py::buffer_info(data, bytesPerPixel, "I", 2, {height, width}, {rowBytes, bytesPerPixel}, readonly);

    case kRGBA_F16Norm_SkColorType:
    case kRGBA_F16_SkColorType:
        return py::buffer_info(data, 2, "e", 3, {height, width, py::ssize_t(4)},
                               {rowBytes, bytesPerPixel, py::ssize_t(2)}, readonly);

    case kRGBA_F32_SkColorType:
        return py::buffer_info(data, 4, "f", 3, {height, width, py::ssize_t(4)},
                               {rowBytes, bytesPerPixel, py::ssize_t(4)}, readonly);

    case kR8G8_unorm_SkColorType:
        return py::buffer_info(data, 1, "B", 3, {height, width, py::ssize_t(2)},
                               {rowBytes, bytesPerPixel, py::ssize_t(1)}, readonly);

    case kA16_float_SkColorType:
        return py::buffer_info(data, 2, "e", 2, {height, width}, {rowBytes, bytesPerPixel}, readonly);

    case kR16G16_float_SkColorType:
        return py::buffer_info(data, 2, "e", 3, {height, width, py::ssize_t(2)},
                               {rowBytes, bytesPerPixel, py::ssize_t(2)}, readonly);

    case kA16_unorm_SkColorType:
        return py::buffer_info(data, 2, "<H", 2, {height, width}, {rowBytes, bytesPerPixel}, readonly);

    case kR16G16_unorm_SkColorType:
        return py::buffer_info(data, 2, "<H", 3, {height, width, py::ssize_t(2)},
                               {rowBytes, bytesPerPixel, py::ssize_t(2)}, readonly);

    case kR16G16B16A16_unorm_SkColorType:
        return py::buffer_info(data, 2, "<H", 3, {height, width, py::ssize_t(4)},
                               {rowBytes, bytesPerPixel, py::ssize_t(2)}, readonly);

    case kUnknown_SkColorType:
    default:
        throw std::runtime_error("Unsupported color type.");
    }
}