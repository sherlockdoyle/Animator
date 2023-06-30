#include "common.h"
#include "include/core/SkBitmap.h"
#include "include/core/SkCanvas.h"
#include "include/core/SkColorSpace.h"
#include "include/core/SkSurface.h"
#include <pybind11/operators.h>

void initSurface(py::module &m)
{
    py::class_<SkSurface, sk_sp<SkSurface>> Surface(m, "Surface", py::buffer_protocol(), R"doc(
        :py:class:`Surface` is responsible for managing the pixels that a canvas draws into. Functions from the
        SkShaders namespace are also available here as static methods.

        Example::
            surface = skia.Surface(640, 480)
            with surface as canvas:
                draw(canvas)
            image = surface.makeImageSnapshot()
    )doc");
    Surface
        .def_buffer(
            [](SkSurface &self)
            {
                SkPixmap pixmap;
                if (self.peekPixels(&pixmap))
                    return imageInfoToBufferInfo(pixmap.info(), pixmap.writable_addr(), pixmap.rowBytes(), false);
                throw std::runtime_error("Surface does not have pixels.");
            })
        .def(py::init(
                 [](py::array &array, const SkColorType &ct, const SkAlphaType &at, const sk_sp<SkColorSpace> &cs,
                    const SkSurfaceProps *surfaceProps)
                 {
                     return SkSurfaces::WrapPixels(ndarrayToImageInfo(array, ct, at, cs), array.mutable_data(),
                                                   array.strides(0), surfaceProps);
                 }),
             "Creates :py:class:`Surface` backed by numpy array.", "array"_a,
             "colorType"_a = SkColorType::kN32_SkColorType, "alphaType"_a = SkAlphaType::kUnpremul_SkAlphaType,
             "colorSpace"_a = nullptr, "surfaceProps"_a = nullptr, py::keep_alive<1, 2>())
        .def("toarray", &readToNumpy<SkSurface>, "Returns a ``ndarray`` of the image's pixels.", "srcX"_a = 0,
             "srcY"_a = 0, "colorType"_a = SkColorType::kN32_SkColorType,
             "alphaType"_a = SkAlphaType::kUnpremul_SkAlphaType, "colorSpace"_a = nullptr)
        .def(py::init([](const int &width, const int &height, const SkSurfaceProps *surfaceProps)
                      { return SkSurfaces::Raster(SkImageInfo::MakeN32Premul(width, height), surfaceProps); }),
             "width"_a, "height"_a, "surfaceProps"_a = nullptr)
        .def("width", &SkSurface::width)
        .def("height", &SkSurface::height)
        .def("imageInfo", &SkSurface::imageInfo)
        .def("generationID", &SkSurface::generationID)
        .def_static("Null", &SkSurfaces::Null, "width"_a, "height"_a)
        .def_static("Raster",
                    py::overload_cast<const SkImageInfo &, size_t, const SkSurfaceProps *>(&SkSurfaces::Raster),
                    "imageInfo"_a, "rowBytes"_a = 0, "surfaceProps"_a = nullptr)
        .def_static(
            "WrapPixels",
            [](const SkImageInfo &imageInfo, const py::buffer &pixels, const size_t &rowBytes,
               const SkSurfaceProps *surfaceProps)
            {
                py::buffer_info bufInfo = pixels.request();
                return SkSurfaces::WrapPixels(imageInfo, bufInfo.ptr,
                                              validateImageInfo_Buffer(imageInfo, bufInfo, rowBytes), surfaceProps);
            },
            "Allocates raster :py:class:`Surface` with the specified *pixels*.", "imageInfo"_a, "pixels"_a,
            "rowBytes"_a = 0, "surfaceProps"_a = nullptr)
        .def_static("WrapPixels", py::overload_cast<const SkPixmap &, const SkSurfaceProps *>(&SkSurfaces::WrapPixels),
                    "pixmap"_a, "props"_a = nullptr);

    py::enum_<SkSurface::ContentChangeMode>(Surface, "ContentChangeMode")
        .value("kDiscard_ContentChangeMode", SkSurface::ContentChangeMode::kDiscard_ContentChangeMode)
        .value("kRetain_ContentChangeMode", SkSurface::ContentChangeMode::kRetain_ContentChangeMode);
    Surface.def("notifyContentWillChange", &SkSurface::notifyContentWillChange, "mode"_a)
        .def("getCanvas", &SkSurface::getCanvas, py::return_value_policy::reference_internal)
        .def("makeSurface", py::overload_cast<const SkImageInfo &>(&SkSurface::makeSurface), "imageInfo"_a)
        .def("makeSurface", py::overload_cast<int, int>(&SkSurface::makeSurface), "width"_a, "height"_a)
        .def("makeImageSnapshot", py::overload_cast<>(&SkSurface::makeImageSnapshot))
        .def("makeImageSnapshot", py::overload_cast<const SkIRect &>(&SkSurface::makeImageSnapshot), "bounds"_a)
        .def("draw",
             py::overload_cast<SkCanvas *, SkScalar, SkScalar, const SkSamplingOptions &, const SkPaint *>(
                 &SkSurface::draw),
             "canvas"_a, "x"_a, "y"_a, "sampling"_a = SkSamplingOptions(), "paint"_a = nullptr)
        .def(
            "peekPixels",
            [](SkSurface &self)
            {
                SkPixmap pixmap;
                if (self.peekPixels(&pixmap))
                    return pixmap;
                throw std::runtime_error("Failed to peek pixels.");
            },
            "Returns a :py:class:`Pixmap` describing the pixel data.")
        .def("readPixels", py::overload_cast<const SkPixmap &, int, int>(&SkSurface::readPixels), "dst"_a, "srcX"_a = 0,
             "srcY"_a = 0)
        .def("readPixels", &readPixels<SkSurface>,
             "Copies *dstInfo* pixels starting from (*srcX*, *srcY*) to *dstPixels* buffer.", "dstInfo"_a,
             "dstPixels"_a, "dstRowBytes"_a = 0, "srcX"_a = 0, "srcY"_a = 0)
        .def("readPixels", py::overload_cast<const SkBitmap &, int, int>(&SkSurface::readPixels), "dst"_a, "srcX"_a = 0,
             "srcY"_a = 0)
        .def("writePixels", py::overload_cast<const SkPixmap &, int, int>(&SkSurface::writePixels), "src"_a,
             "dstX"_a = 0, "dstY"_a = 0)
        .def("writePixels", py::overload_cast<const SkBitmap &, int, int>(&SkSurface::writePixels), "src"_a,
             "dstX"_a = 0, "dstY"_a = 0)
        .def("props", &SkSurface::props)
        .def(
            "__enter__", [](SkSurface &self) { return self.getCanvas(); },
            "Returns a :py:class:`Canvas` object that can be used to draw on the surface.",
            py::return_value_policy::reference_internal)
        .def("__exit__", [](const SkSurface &, const py::object &, const py::object &, const py::object &) {})
        .def("__str__", [](const SkSurface &self) { return "Surface({} x {})"_s.format(self.width(), self.height()); });
}