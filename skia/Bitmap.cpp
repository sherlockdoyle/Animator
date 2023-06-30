#include "common.h"
#include "include/core/SkBitmap.h"
#include "include/core/SkColorSpace.h"
#include "include/core/SkImage.h"
#include "include/core/SkMatrix.h"
#include "include/core/SkPaint.h"
#include "include/core/SkShader.h"
#include "include/core/SkTileMode.h"
#include <pybind11/stl.h>

void initBitmap(py::module &m)
{
    py::class_<SkBitmap, std::unique_ptr<SkBitmap>> Bitmap(m, "Bitmap", py::buffer_protocol(), R"doc(
        :py:class:`Bitmap` describes a two-dimensional raster pixel array.

        :py:class:`Bitmap` supports buffer protocol. It is possible to mount :py:class:`Bitmap` as array::

            array = np.array(pixmap, copy=False)

        Or mount array as :py:class:`Bitmap` with :py:class:`ImageInfo`::

            buffer = np.zeros((100, 100, 4), np.uint8)
            bitmap = skia.Bitmap()
            bitmap.setInfo(skia.ImageInfo.MakeN32Premul(100, 100))
            bitmap.setPixels(buffer)
    )doc");
    Bitmap
        .def_buffer(
            [](const SkBitmap &bitmap)
            {
                if (bitmap.isNull() || bitmap.getPixels() == nullptr)
                    throw std::runtime_error("Bitmap has no pixels.");
                return imageInfoToBufferInfo(bitmap.info(), bitmap.getPixels(), bitmap.rowBytes(), false);
            })
        .def(
            "tobytes",
            [](const SkBitmap &self)
            { return py::bytes(reinterpret_cast<char *>(self.getPixels()), self.computeByteSize()); },
            "Convert :py:class:`Bitmap` to bytes.")
        .def(py::init())
        .def(py::init<const SkBitmap &>(), "src"_a)
        .def("swap", &SkBitmap::swap, "other"_a)
        .def("pixmap", &SkBitmap::pixmap, py::return_value_policy::reference_internal)
        .def("info", &SkBitmap::info, py::return_value_policy::reference_internal)
        .def("width", &SkBitmap::width)
        .def("height", &SkBitmap::height)
        .def("colorType", &SkBitmap::colorType)
        .def("alphaType", &SkBitmap::alphaType)
        .def("colorSpace", &SkBitmap::colorSpace, py::return_value_policy::reference_internal)
        .def("refColorSpace", &SkBitmap::refColorSpace)
        .def("bytesPerPixel", &SkBitmap::bytesPerPixel)
        .def("rowBytesAsPixels", &SkBitmap::rowBytesAsPixels)
        .def("shiftPerPixel", &SkBitmap::shiftPerPixel)
        .def("empty", &SkBitmap::empty)
        .def("isNull", &SkBitmap::isNull)
        .def("drawsNothing", &SkBitmap::drawsNothing)
        .def("rowBytes", &SkBitmap::rowBytes)
        .def("setAlphaType", &SkBitmap::setAlphaType, "alphaType"_a)
        .def(
            "getPixels",
            [](const SkBitmap &self)
            {
                if (self.getPixels() == nullptr)
                    throw std::runtime_error("Bitmap has no pixels.");
                return py::memoryview::from_memory(self.getPixels(), self.computeByteSize());
            },
            "Return a ``memoryview`` object of the pixel data.")
        .def("computeByteSize", &SkBitmap::computeByteSize)
        .def("isImmutable", &SkBitmap::isImmutable)
        .def("setImmutable", &SkBitmap::setImmutable)
        .def("isOpaque", &SkBitmap::isOpaque)
        .def("reset", &SkBitmap::reset)
        .def("computeIsOpaque", &SkBitmap::ComputeIsOpaque, "Returns ``True`` if all pixels are opaque.")
        .def(
            "getBounds",
            [](const SkBitmap &self)
            {
                SkIRect bounds;
                self.getBounds(&bounds);
                return bounds;
            },
            "Returns :py:class:`IRect` { 0, 0, :py:meth:`width`, :py:meth:`height` }.")
        .def("bounds", &SkBitmap::bounds)
        .def("dimensions", &SkBitmap::dimensions)
        .def("getSubset", &SkBitmap::getSubset)
        .def("setInfo", &SkBitmap::setInfo, "imageInfo"_a, "rowBytes"_a = 0);

    py::enum_<SkBitmap::AllocFlags>(Bitmap, "AllocFlags", py::arithmetic())
        .value("kZeroPixels_AllocFlag", SkBitmap::kZeroPixels_AllocFlag);
    Bitmap.def("tryAllocPixelsFlags", &SkBitmap::tryAllocPixelsFlags, "info"_a, "flags"_a = 0)
        .def("allocPixelsFlags", &SkBitmap::allocPixelsFlags, "info"_a, "flags"_a = 0)
        .def("tryAllocPixels", py::overload_cast<const SkImageInfo &, size_t>(&SkBitmap::tryAllocPixels), "info"_a,
             "rowBytes"_a)
        .def("allocPixels", py::overload_cast<const SkImageInfo &, size_t>(&SkBitmap::allocPixels), "info"_a,
             "rowBytes"_a)
        .def("tryAllocPixels", py::overload_cast<const SkImageInfo &>(&SkBitmap::tryAllocPixels), "info"_a)
        .def("allocPixels", py::overload_cast<const SkImageInfo &>(&SkBitmap::allocPixels), "info"_a)
        .def("tryAllocN32Pixels", &SkBitmap::tryAllocN32Pixels, "width"_a, "height"_a, "isOpaque"_a = false)
        .def("allocN32Pixels", &SkBitmap::allocN32Pixels, "width"_a, "height"_a, "isOpaque"_a = false)
        .def(
            "installPixels",
            [](SkBitmap &self, const SkImageInfo &info, std::optional<py::buffer> &pixels, const size_t &rowBytes)
            {
                if (pixels)
                {
                    const py::buffer_info bufInfo = pixels->request();
                    return self.installPixels(info, bufInfo.ptr, validateImageInfo_Buffer(info, bufInfo, rowBytes));
                }
                return self.installPixels(info, nullptr, rowBytes == 0 ? info.minRowBytes() : rowBytes);
            },
            R"doc(
                Sets :py:class:`ImageInfo` *info* and pixel data from the buffer *pixels*.

                :warning: Keep a reference to the buffer until the bitmap is no longer needed.
            )doc",
            "info"_a, "pixels"_a, "rowBytes"_a = 0)
        .def("installPixels", py::overload_cast<const SkPixmap &>(&SkBitmap::installPixels), "pixmap"_a)
        .def(
            "setPixels",
            [](SkBitmap &self, const std::optional<py::buffer> &pixels)
            {
                if (pixels)
                {
                    const py::buffer_info bufInfo = pixels->request();
                    validateImageInfo_Buffer(self.info(), bufInfo, self.rowBytes());
                    return self.setPixels(bufInfo.ptr);
                }
                return self.setPixels(nullptr);
            },
            R"doc(
                Sets pixel data from the buffer *pixels*.

                :warning: Keep a reference to the buffer until the bitmap is no longer needed.
            )doc",
            "pixels"_a)
        .def("tryAllocPixels", py::overload_cast<>(&SkBitmap::tryAllocPixels))
        .def("allocPixels", py::overload_cast<>(&SkBitmap::allocPixels))
        .def("pixelRefOrigin", &SkBitmap::pixelRefOrigin)
        .def("readyToDraw", &SkBitmap::readyToDraw)
        .def("getGenerationID", &SkBitmap::getGenerationID)
        .def("notifyPixelsChanged", &SkBitmap::notifyPixelsChanged)
        .def("eraseColor", py::overload_cast<SkColor4f>(&SkBitmap::eraseColor, py::const_), "c"_a)
        .def("eraseColor", py::overload_cast<SkColor>(&SkBitmap::eraseColor, py::const_), "c"_a)
        .def("eraseARGB", &SkBitmap::eraseARGB, "a"_a, "r"_a, "g"_a, "b"_a)
        .def("erase", py::overload_cast<SkColor4f, const SkIRect &>(&SkBitmap::erase, py::const_), "c"_a, "area"_a)
        .def("erase", py::overload_cast<SkColor, const SkIRect &>(&SkBitmap::erase, py::const_), "c"_a, "area"_a)
        .def("getColor", &SkBitmap::getColor, "x"_a, "y"_a)
        .def("getColor4f", &SkBitmap::getColor4f, "x"_a, "y"_a)
        .def("getAlphaf", &SkBitmap::getAlphaf, "x"_a, "y"_a)
        .def(
            "extractSubset",
            [](const SkBitmap &self, const SkIRect &subset)
            {
                SkBitmap dst;
                if (self.extractSubset(&dst, subset))
                    return dst;
                throw std::runtime_error("Resulting subset is empty");
            },
            "subset"_a)
        .def("readPixels", &readPixels<SkBitmap>,
             "Copies *dstInfo* pixels starting from (*srcX*, *srcY*) to *dstPixels* buffer.", "dstInfo"_a,
             "dstPixels"_a, "dstRowBytes"_a = 0, "srcX"_a = 0, "srcY"_a = 0)
        .def("readPixels", py::overload_cast<const SkPixmap &, int, int>(&SkBitmap::readPixels, py::const_), "dst"_a,
             "srcX"_a = 0, "srcY"_a = 0)
        .def("writePixels", py::overload_cast<const SkPixmap &, int, int>(&SkBitmap::writePixels), "src"_a,
             "dstX"_a = 0, "dstY"_a = 0)
        .def(
            "extractAlpha",
            [](const SkBitmap &self, const SkPaint *paint)
            {
                SkBitmap dst;
                SkIPoint offset;
                if (self.extractAlpha(&dst, paint, &offset))
                    return std::make_tuple(dst, offset);
                throw std::runtime_error("Failed to extract alpha");
            },
            "Returns a tuple of (bitmap describing the alpha values, top-left position of the alpha values).",
            "paint"_a = nullptr)
        .def(
            "peekPixels",
            [](const SkBitmap &self)
            {
                SkPixmap pixmap;
                if (self.peekPixels(&pixmap))
                    return pixmap;
                throw std::runtime_error("Failed to peek pixels");
            },
            "Returns a :py:class:`Pixmap` describing the pixel data.")
        .def("makeShader",
             py::overload_cast<SkTileMode, SkTileMode, const SkSamplingOptions &, const SkMatrix *>(
                 &SkBitmap::makeShader, py::const_),
             "tmx"_a = SkTileMode::kClamp, "tmy"_a = SkTileMode::kClamp, "sampling"_a = SkSamplingOptions(),
             "localMatrix"_a = nullptr)
        .def("asImage", &SkBitmap::asImage)
        .def("__str__",
             [](const SkBitmap &self)
             {
                 return "Bitmap({} x {}, colorType={}, alphaType={}, colorSpace={})"_s.format(
                     self.width(), self.height(), self.colorType(), self.alphaType(), self.colorSpace());
             });
}