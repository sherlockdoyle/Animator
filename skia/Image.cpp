#include "common.h"
#include "include/core/SkBitmap.h"
#include "include/core/SkColorSpace.h"
#include "include/core/SkData.h"
#include "include/core/SkEncodedImageFormat.h"
#include "include/core/SkImage.h"
#include "include/core/SkImageFilter.h"
#include "include/core/SkPaint.h"
#include "include/core/SkPicture.h"
#include "include/core/SkStream.h"
#include "include/core/SkSurfaceProps.h"
#include "include/core/SkTextureCompressionType.h"
#include "include/encode/SkJpegEncoder.h"
#include "include/encode/SkPngEncoder.h"
#include "include/encode/SkWebpEncoder.h"
#include <pybind11/operators.h>
#include <pybind11/stl.h>

sk_sp<SkData> encodeToData(const SkImage *self, const SkEncodedImageFormat &format = SkEncodedImageFormat::kPNG,
                           const int &quality = 100)
{ // taken from old SkImageEncoder.cpp
    switch (format)
    {
    case SkEncodedImageFormat::kJPEG:
    {
        SkJpegEncoder::Options opts;
        opts.fQuality = quality;
        return SkJpegEncoder::Encode(nullptr, self, opts);
    }
    case SkEncodedImageFormat::kPNG:
    {
        SkPngEncoder::Options opts;
        return SkPngEncoder::Encode(nullptr, self, opts);
    }
    case SkEncodedImageFormat::kWEBP:
    {
        SkWebpEncoder::Options opts;
        if (quality == 100)
        {
            opts.fCompression = SkWebpEncoder::Compression::kLossless;
            opts.fQuality = 75;
        }
        else
        {
            opts.fCompression = SkWebpEncoder::Compression::kLossy;
            opts.fQuality = quality;
        }
        return SkWebpEncoder::Encode(nullptr, self, opts);
    }
    default:
        return nullptr;
    }
}

void initImage(py::module &m)
{
    py::enum_<SkFilterMode>(m, "FilterMode")
        .value("kNearest", SkFilterMode::kNearest)
        .value("kLinear", SkFilterMode::kLinear)
        .value("kLast", SkFilterMode::kLast);

    py::enum_<SkMipmapMode>(m, "MipmapMode")
        .value("kNone", SkMipmapMode::kNone)
        .value("kNearest", SkMipmapMode::kNearest)
        .value("kLinear", SkMipmapMode::kLinear)
        .value("kLast", SkMipmapMode::kLast);

    py::class_<SkCubicResampler>(m, "CubicResampler")
        .def(py::init(
                 [](const float &B, const float &C) {
                     return SkCubicResampler{B, C};
                 }),
             "B"_a, "C"_a)
        .def_readwrite("B", &SkCubicResampler::B)
        .def_readwrite("C", &SkCubicResampler::C)
        .def_static("Mitchell", &SkCubicResampler::Mitchell)
        .def_static("CatmullRom", &SkCubicResampler::CatmullRom)
        .def("__str__",
             [](const SkCubicResampler &self) { return "CubicResampler(B={:g}, C={:g})"_s.format(self.B, self.C); });

    py::class_<SkSamplingOptions>(m, "SamplingOptions")
        .def_readonly("maxAniso", &SkSamplingOptions::maxAniso)
        .def_readonly("useCubic", &SkSamplingOptions::useCubic)
        .def_readonly("cubic", &SkSamplingOptions::cubic)
        .def_readonly("filter", &SkSamplingOptions::filter)
        .def_readonly("mipmap", &SkSamplingOptions::mipmap)
        .def(py::init())
        .def(py::init<const SkSamplingOptions &>(), "other"_a)
        .def(py::init<SkFilterMode, SkMipmapMode>(), "fm"_a, "mm"_a)
        .def(py::init<SkFilterMode>(), "fm"_a)
        .def(py::init<const SkCubicResampler &>(), "c"_a)
        .def_static("Aniso", &SkSamplingOptions::Aniso, "maxAniso"_a)
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def("isAniso", &SkSamplingOptions::isAniso)
        .def("__str__",
             [](const SkSamplingOptions &self)
             {
                 return "SamplingOptions({})"_s.format(self.isAniso() ? "maxAniso={}"_s.format(self.maxAniso)
                                                       : self.useCubic
                                                           ? "cubic={}"_s.format(self.cubic)
                                                           : "filter={}, mipmap={}"_s.format(self.filter, self.mipmap));
             });

    py::enum_<SkTileMode>(m, "TileMode")
        .value("kClamp", SkTileMode::kClamp)
        .value("kRepeat", SkTileMode::kRepeat)
        .value("kMirror", SkTileMode::kMirror)
        .value("kDecal", SkTileMode::kDecal)
        .value("kLastTileMode", SkTileMode::kLastTileMode);
    m.attr("kTileModeCount") = kSkTileModeCount;

    py::enum_<SkEncodedImageFormat>(m, "EncodedImageFormat")
        .value("kBMP", SkEncodedImageFormat::kBMP)
        .value("kGIF", SkEncodedImageFormat::kGIF)
        .value("kICO", SkEncodedImageFormat::kICO)
        .value("kJPEG", SkEncodedImageFormat::kJPEG)
        .value("kPNG", SkEncodedImageFormat::kPNG)
        .value("kWBMP", SkEncodedImageFormat::kWBMP)
        .value("kWEBP", SkEncodedImageFormat::kWEBP)
        .value("kPKM", SkEncodedImageFormat::kPKM)
        .value("kKTX", SkEncodedImageFormat::kKTX)
        .value("kASTC", SkEncodedImageFormat::kASTC)
        .value("kDNG", SkEncodedImageFormat::kDNG)
        .value("kHEIF", SkEncodedImageFormat::kHEIF)
        .value("kAVIF", SkEncodedImageFormat::kAVIF)
        .value("kJPEGXL", SkEncodedImageFormat::kJPEGXL);

    py::enum_<SkPixelGeometry>(m, "PixelGeometry")
        .value("kUnknown_PixelGeometry", SkPixelGeometry::kUnknown_SkPixelGeometry)
        .value("kRGB_H_PixelGeometry", SkPixelGeometry::kRGB_H_SkPixelGeometry)
        .value("kBGR_H_PixelGeometry", SkPixelGeometry::kBGR_H_SkPixelGeometry)
        .value("kRGB_V_PixelGeometry", SkPixelGeometry::kRGB_V_SkPixelGeometry)
        .value("kBGR_V_PixelGeometry", SkPixelGeometry::kBGR_V_SkPixelGeometry)
        .def("pixelGeometryIsRGB", &SkPixelGeometryIsRGB)
        .def("pixelGeometryIsBGR", &SkPixelGeometryIsBGR)
        .def("pixelGeometryIsH", &SkPixelGeometryIsH)
        .def("pixelGeometryIsV", &SkPixelGeometryIsV);

    py::class_<SkSurfaceProps> SurfaceProps(m, "SurfaceProps");

    py::enum_<SkSurfaceProps::Flags>(SurfaceProps, "Flags", py::arithmetic())
        .value("kUseDeviceIndependentFonts_Flag", SkSurfaceProps::Flags::kUseDeviceIndependentFonts_Flag)
        .value("kDynamicMSAA_Flag", SkSurfaceProps::Flags::kDynamicMSAA_Flag)
        .value("kAlwaysDither_Flag", SkSurfaceProps::Flags::kAlwaysDither_Flag);
    SurfaceProps.def(py::init())
        .def(py::init<uint32_t, SkPixelGeometry>(), "flags"_a, "pg"_a)
        .def(py::init<const SkSurfaceProps &>(), "props"_a)
        .def("cloneWithPixelGeometry", &SkSurfaceProps::cloneWithPixelGeometry, "newPixelGeometry"_a)
        .def("flags", &SkSurfaceProps::flags)
        .def("pixelGeometry", &SkSurfaceProps::pixelGeometry)
        .def("isUseDeviceIndependentFonts", &SkSurfaceProps::isUseDeviceIndependentFonts)
        .def("isAlwaysDither", &SkSurfaceProps::isAlwaysDither)
        .def(py::self == py::self)
        .def(py::self != py::self);

    py::class_<SkImage, sk_sp<SkImage>> Image(m, "Image", py::buffer_protocol(), R"doc(
        :py:class:`Image` describes a two dimensional array of pixels to draw.

        A few high-level methods in addition to C++ API::

            image = skia.Image.open('/path/to/image.png')
            image = image.resize(120, 120)
            image = image.convert(alphaType=skia.kUnpremul_AlphaType)
            image.save('/path/to/output.jpg', skia.kJPEG)

        NumPy arrays can be directly imported or exported::

            image = skia.Image.fromarray(array)
            array = image.toarray()

        General pixel buffers can be exchanged in the following approach::

            image = skia.Image.frombytes(pixels, (100, 100))
            pixels = image.tobytes()
    )doc");
    Image
        .def_buffer(
            [](const SkImage &self)
            {
                SkPixmap pixmap;
                if (self.peekPixels(&pixmap))
                    return imageInfoToBufferInfo(pixmap.info(), pixmap.writable_addr(), pixmap.rowBytes(), false);
                throw std::runtime_error("Image is not backed by pixels. Hint: call makeRasterImage() first.");
            })
        .def_static(
            "frombytes",
            [](const py::buffer &buffer, const SkISize &dimensions, const SkColorType &ct, const SkAlphaType &at,
               const sk_sp<SkColorSpace> &cs, const bool &copy)
            {
                py::buffer_info bufInfo = buffer.request();
                SkImageInfo imgInfo = SkImageInfo::Make(dimensions, ct, at, cs);
                size_t rowBytes = validateImageInfo_Buffer(imgInfo, bufInfo, 0);
                size_t size = imgInfo.computeByteSize(rowBytes);
                return SkImages::RasterFromData(imgInfo,
                                                copy ? SkData::MakeWithCopy(bufInfo.ptr, size)
                                                     : SkData::MakeWithoutCopy(bufInfo.ptr, size),
                                                rowBytes);
            },
            R"doc(
                Creates a new :py:class:`Image` from bytes.

                :param buffer: A Python buffer object.
                :param dimensions: The dimensions of the image.
                :param ct: The color type of the image.
                :param at: The alpha type of the image.
                :param cs: The color space of the image.
                :param copy: Whether to copy the data from the buffer.
                :return: A new :py:class:`Image` sharing the data in the buffer if copy is ``False``, or a new
                    :py:class:`Image` with a copy of the data if copy is ``True``.
            )doc",
            "buffer"_a, "dimensions"_a, "ct"_a = kN32_SkColorType, "at"_a = SkAlphaType::kUnpremul_SkAlphaType,
            "cs"_a = py::none(), "copy"_a = true)
        .def(
            "tobytes",
            [](const SkImage &self)
            {
                SkPixmap pixmap;
                if (self.peekPixels(&pixmap))
                    return py::bytes(reinterpret_cast<const char *>(pixmap.addr()), pixmap.computeByteSize());
                else
                {
                    SkImageInfo imgInfo = self.imageInfo();
                    py::bytes bytes(nullptr, imgInfo.computeMinByteSize());
                    void *ptr = reinterpret_cast<void *>(PyBytes_AS_STRING(bytes.ptr()));
                    if (self.readPixels(imgInfo, ptr, imgInfo.minRowBytes(), 0, 0))
                        return bytes;
                    throw std::runtime_error("Failed to read pixels.");
                }
            },
            "Returns python ``bytes`` object from internal pixels.")
        .def_static(
            "fromarray",
            [](const py::array &array, const SkColorType &ct, const SkAlphaType &at, const sk_sp<SkColorSpace> &cs,
               const bool &copy)
            {
                py::ssize_t rowBytes = array.strides(0);
                size_t size = array.shape(0) * rowBytes;
                return SkImages::RasterFromData(ndarrayToImageInfo(array, ct, at, cs),
                                                copy ? SkData::MakeWithCopy(array.data(), size)
                                                     : SkData::MakeWithoutCopy(array.data(), size),
                                                rowBytes);
            },
            R"doc(
                Creates a new :py:class:`Image` from numpy array.

                :param array: A numpy array of shape ``(height, width, channels)`` and appropriate dtype.
                :param ct: The color type of the image.
                :param at: The alpha type of the image.
                :param cs: The color space of the image.
                :param copy: Whether to copy the data from the array.
                :return: A new :py:class:`Image` sharing the data in the array if copy is ``False``, or a new
                    :py:class:`Image` with a copy of the data if copy is ``True``.
            )doc",
            "array"_a, "ct"_a = kN32_SkColorType, "at"_a = SkAlphaType::kUnpremul_SkAlphaType, "cs"_a = nullptr,
            "copy"_a = true)
        .def("toarray", &readToNumpy<SkImage>, "Returns a ``ndarray`` of the image's pixels.", "srcX"_a = 0,
             "srcY"_a = 0, "ct"_a = SkColorType::kN32_SkColorType, "at"_a = SkAlphaType::kUnpremul_SkAlphaType,
             "cs"_a = nullptr)
        .def_static(
            "open",
            [](const py::object &fp)
            {
                sk_sp<SkData> data;
                if (py::hasattr(fp, "seek") && py::hasattr(fp, "read"))
                {
                    fp.attr("seek")(0);
                    py::buffer_info bufInfo = fp.attr("read")().cast<py::buffer>().request();
                    data = SkData::MakeWithCopy(bufInfo.ptr, bufInfo.size);
                    if (!data)
                        throw py::value_error("Failed to read data from file.");
                }
                else
                {
                    std::string path = fp.cast<std::string>();
                    data = SkData::MakeFromFileName(path.c_str());
                    if (!data)
                        throw py::value_error("Failed to open file {}"_s.format(path));
                }

                sk_sp<SkImage> image = SkImages::DeferredFromEncodedData(data);
                if (image)
                    return image;
                throw py::value_error("Failed to decode image.");
            },
            "Opens an image from a file like object or a path.", "fp"_a)
        .def(
            "save",
            [](const SkImage &self, const py::object &fp, const SkEncodedImageFormat &encodedImageFormat,
               const int &quality)
            {
                sk_sp<SkData> data = encodeToData(&self, encodedImageFormat, quality);
                if (!data)
                    throw py::value_error("Failed to encode image.");
                if (py::hasattr(fp, "write"))
                    fp.attr("write")(data);
                else
                {
                    std::string path = fp.cast<std::string>();
                    SkFILEWStream stream(path.c_str());
                    if (!stream.write(data->data(), data->size()))
                        throw py::value_error("Failed to write data to file {}"_s.format(path));
                }
            },
            R"doc(
                Saves the image to a file like object or a path.

                :param fp: A file like object or a path.
                :param format: The format of the image. Should be one of :py:attr:`EncodedImageFormat.kJPEG`,
                    :py:attr:`EncodedImageFormat.kPNG`, :py:attr:`EncodedImageFormat.kWEBP`.
                :param quality: The quality of the image. 100 is the best quality.
            )doc",
            "fp"_a, "encodedImageFormat"_a = SkEncodedImageFormat::kPNG, "quality"_a = 100)
        .def_static("RasterFromBitmap", &SkImages::RasterFromBitmap, "bitmap"_a);

    py::enum_<SkTextureCompressionType>(Image, "TextureCompressionType")
        .value("kNone", SkTextureCompressionType::kNone)
        .value("kETC2_RGB8_UNORM", SkTextureCompressionType::kETC2_RGB8_UNORM)
        .value("kBC1_RGB8_UNORM", SkTextureCompressionType::kBC1_RGB8_UNORM)
        .value("kBC1_RGBA8_UNORM", SkTextureCompressionType::kBC1_RGBA8_UNORM)
        .value("kLast", SkTextureCompressionType::kLast)
        .value("kETC1_RGB8", SkTextureCompressionType::kETC1_RGB8);
    Image
        .def_static("RasterFromCompressedTextureData", &SkImages::RasterFromCompressedTextureData, "data"_a, "width"_a,
                    "height"_a, "type"_a)
        .def_static("DeferredFromEncodedData", &SkImages::DeferredFromEncodedData, "encoded"_a,
                    "alphaType"_a = std::nullopt);

    py::enum_<SkImages::BitDepth>(Image, "BitDepth")
        .value("kU8", SkImages::BitDepth::kU8)
        .value("kF16", SkImages::BitDepth::kF16);
    Image
        .def_static(
            "DeferredFromPicture",
            py::overload_cast<sk_sp<SkPicture>, const SkISize &, const SkMatrix *, const SkPaint *, SkImages::BitDepth,
                              sk_sp<SkColorSpace>, SkSurfaceProps>(&SkImages::DeferredFromPicture),
            "picture"_a, "dimensions"_a, "matrix"_a = nullptr, "paint"_a = nullptr,
            "bitDepth"_a = SkImages::BitDepth::kU8, "colorSpace"_a = nullptr, "props"_a = SkSurfaceProps{})
        .def_static("RasterFromPixmapCopy", &SkImages::RasterFromPixmapCopy, "pixmap"_a)
        .def_static(
            "RasterFromPixmap",
            [](const SkPixmap &pixmap) { return SkImages::RasterFromPixmap(pixmap, nullptr, nullptr); },
            "Creates :py:class:`Image` from *pixmap*, sharing :py:class:`Pixmap` pixels.", "pixmap"_a,
            py::keep_alive<0, 1>())
        .def_static("RasterFromData", &SkImages::RasterFromData, "info"_a, "pixels"_a, "rowBytes"_a);

    static constexpr SkSamplingOptions dso;

    Image.def("imageInfo", &SkImage::imageInfo)
        .def("width", &SkImage::width)
        .def("height", &SkImage::height)
        .def("dimensions", &SkImage::dimensions)
        .def("bounds", &SkImage::bounds)
        .def("uniqueID", &SkImage::uniqueID)
        .def("alphaType", &SkImage::alphaType)
        .def("colorType", &SkImage::colorType)
        .def("colorSpace", &SkImage::colorSpace, py::return_value_policy::reference_internal)
        .def("refColorSpace", &SkImage::refColorSpace)
        .def("isAlphaOnly", &SkImage::isAlphaOnly)
        .def("isOpaque", &SkImage::isOpaque)
        .def("makeShader",
             py::overload_cast<SkTileMode, SkTileMode, const SkSamplingOptions &, const SkMatrix *>(
                 &SkImage::makeShader, py::const_),
             "tmx"_a = SkTileMode::kClamp, "tmy"_a = SkTileMode::kClamp, "sampling"_a = dso, "localMatrix"_a = nullptr)
        .def("makeRawShader",
             py::overload_cast<SkTileMode, SkTileMode, const SkSamplingOptions &, const SkMatrix *>(
                 &SkImage::makeRawShader, py::const_),
             "tmx"_a = SkTileMode::kClamp, "tmy"_a = SkTileMode::kClamp, "sampling"_a = dso, "localMatrix"_a = nullptr)
        .def(
            "peekPixels",
            [](const SkImage &self)
            {
                SkPixmap pixmap;
                if (self.peekPixels(&pixmap))
                    return pixmap;
                throw std::runtime_error("Pixel address is not available.");
            },
            "Returns a :py:class:`Pixmap` describing the pixel data.")
        .def(
            "isValid", [](const SkImage &self) { return self.isValid(nullptr); },
            "Returns ``True`` if :py:class:`Image` can be drawn on raster surface.");

    py::enum_<SkImage::CachingHint>(Image, "CachingHint")
        .value("kAllow_CachingHint", SkImage::CachingHint::kAllow_CachingHint)
        .value("kDisallow_CachingHint", SkImage::CachingHint::kDisallow_CachingHint);
    Image
        .def(
            "readPixels",
            [](const SkImage &self, const SkImageInfo &dstInfo, const py::buffer &dstPixels, const size_t &dstRowBytes,
               const int &srcX, const int &srcY, const SkImage::CachingHint &cachingHint)
            {
                const py::buffer_info bufInfo = dstPixels.request();
                return self.readPixels(nullptr, dstInfo, bufInfo.ptr,
                                       validateImageInfo_Buffer(dstInfo, bufInfo, dstRowBytes), srcX, srcY,
                                       cachingHint);
            },
            "Copies *dstInfo* pixels starting from (*srcX*, *srcY*) to *dstPixels* buffer.", "dstInfo"_a, "dstPixels"_a,
            "dstRowBytes"_a = 0, "srcX"_a = 0, "srcY"_a = 0, "cachingHint"_a = SkImage::CachingHint::kAllow_CachingHint)
        .def(
            "readPixels",
            [](const SkImage &self, const SkPixmap &dst, const int &srcX, const int &srcY,
               const SkImage::CachingHint &cachingHint)
            { return self.readPixels(nullptr, dst, srcX, srcY, cachingHint); },
            "Copies pixels starting from (*srcX*, *srcY*) to *dst* :py:class:`Pixmap`.", "dst"_a, "srcX"_a = 0,
            "srcY"_a = 0, "cachingHint"_a = SkImage::CachingHint::kAllow_CachingHint)
        .def("scalePixels", &SkImage::scalePixels, "dst"_a, "sampling"_a = dso,
             "cachingHint"_a = SkImage::kAllow_CachingHint)
        .def("encodeToData", &encodeToData, "encodedImageFormat"_a = SkEncodedImageFormat::kPNG, "quality"_a = 100)
        .def("refEncodedData", &SkImage::refEncodedData)
        .def(
            "makeSubset", [](const SkImage &self, const SkIRect &subset) { return self.makeSubset(nullptr, subset); },
            "Returns subset of :py:class:`Image` with *subset* bounds.", "subset"_a)
        .def("hasMipmaps", &SkImage::hasMipmaps)
        .def("withDefaultMipmaps", &SkImage::withDefaultMipmaps)
        .def("makeNonTextureImage", [](const SkImage &self) { return self.makeNonTextureImage(nullptr); })
        .def(
            "makeRasterImage",
            [](const SkImage &self, const SkImage::CachingHint &cachingHint)
            { return self.makeRasterImage(nullptr, cachingHint); },
            "cachingHint"_a = SkImage::CachingHint::kDisallow_CachingHint)
        .def(
            "makeWithFilter",
            [](const SkImage &self, const SkImageFilter *filter, const SkIRect *subset, const SkIRect *clipBounds)
            {
                SkIRect outSubset;
                SkIPoint offset;
                const SkIRect &selfBounds = self.bounds();
                sk_sp<SkImage> result = self.makeWithFilter(nullptr, filter, subset ? *subset : selfBounds,
                                                            clipBounds ? *clipBounds : selfBounds, &outSubset, &offset);
                if (result)
                    return py::make_tuple(result, outSubset, offset);
                throw std::runtime_error("Image filtering failed.");
            },
            "Creates filtered :py:class:`Image` and returns ``(filteredImage, outSubset, offset)``.", "filter"_a,
            "subset"_a = py::none(), "clipBounds"_a = py::none())
        .def("isLazyGenerated", &SkImage::isLazyGenerated)
        .def(
            "makeColorSpace",
            [](const SkImage &self, const sk_sp<SkColorSpace> &target) { return self.makeColorSpace(nullptr, target); },
            "Creates :py:class:`Image` in *target* colorspace.", "target"_a)
        .def(
            "makeColorTypeAndColorSpace",
            [](const SkImage &self, const SkColorType &targetColorType, const sk_sp<SkColorSpace> &targetColorSpace)
            { return self.makeColorTypeAndColorSpace(nullptr, targetColorType, targetColorSpace); },
            "Creates :py:class:`Image` in *targetColorType* and *targetColorSpace*.", "targetColorType"_a,
            "targetColorSpace"_a)
        .def("reinterpretColorSpace", &SkImage::reinterpretColorSpace, "newColorSpace"_a)
        .def(
            "bitmap",
            [](const SkImage &self, const SkColorType &colorType, const SkAlphaType &alphaType,
               const sk_sp<SkColorSpace> &colorSpace)
            {
                std::unique_ptr<SkBitmap> bitmap(new SkBitmap());
                if (!bitmap)
                    throw std::bad_alloc();
                const SkImageInfo imageInfo = SkImageInfo::Make(
                    self.width(), self.height(),
                    colorType == SkColorType::kUnknown_SkColorType ? self.colorType() : colorType,
                    alphaType == SkAlphaType::kUnknown_SkAlphaType ? self.alphaType() : alphaType, colorSpace);
                if (!bitmap->tryAllocPixels(imageInfo))
                    throw std::bad_alloc();
                if (self.readPixels(bitmap->pixmap(), 0, 0))
                    return bitmap;
                throw std::runtime_error("Failed to read pixels.");
            },
            "Creates a new :py:class:`Bitmap` from :py:class:`Image` with a copy of pixels.",
            "colorType"_a = SkColorType::kUnknown_SkColorType, "alphaType"_a = SkAlphaType::kUnknown_SkAlphaType,
            "colorSpace"_a = py::none())
        .def(
            "resize",
            [](const SkImage &self, const int &width, const int &height, const SkSamplingOptions &sampling,
               const SkImage::CachingHint &cachingHint)
            {
                const SkImageInfo imageInfo = self.imageInfo().makeWH(width, height);
                const sk_sp<SkData> buffer = SkData::MakeUninitialized(imageInfo.computeMinByteSize());
                if (!buffer)
                    throw std::bad_alloc();
                const size_t rowBytes = imageInfo.minRowBytes();
                const SkPixmap pixmap = SkPixmap(imageInfo, buffer->writable_data(), rowBytes);
                if (self.scalePixels(pixmap, sampling, cachingHint))
                    return SkImages::RasterFromData(imageInfo, buffer, rowBytes);
                throw std::runtime_error("Failed to resize image.");
            },
            "Creates a new :py:class:`Image` by scaling pixels to fit *width* and *height*.", "width"_a, "height"_a,
            "sampling"_a = dso, "cachingHint"_a = SkImage::kAllow_CachingHint)
        .def("_repr_png_",
             [](const SkImage &self)
             {
                 sk_sp<SkData> data = encodeToData(&self);
                 if (!data)
                     throw std::runtime_error("Failed to encode image.");
                 return py::bytes(static_cast<const char *>(data->data()), data->size());
             })
        .def("__str__",
             [](const SkImage &self)
             {
                 return "Image({} x {}, colorType={}, alphaType={}, colorSpace={})"_s.format(
                     self.width(), self.height(), self.colorType(), self.alphaType(), self.colorSpace());
             });
}