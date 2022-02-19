#include "common.h"
#include "include/core/SkCanvas.h"
#include "include/core/SkSurface.h"
#include "include/core/SkSurfaceProps.h"
// #include <pybind11/numpy.h>
#include <pybind11/operators.h>

void initSurface(py::module &m)
{
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
        .value("kDynamicMSAA_Flag", SkSurfaceProps::Flags::kDynamicMSAA_Flag);
    SurfaceProps.def(py::init())
        .def(py::init<uint32_t, SkPixelGeometry>(), "flags"_a, "pg"_a)
        .def(py::init<const SkSurfaceProps &>(), "props"_a)
        .def("cloneWithPixelGeometry", &SkSurfaceProps::cloneWithPixelGeometry, "newPixelGeometry"_a)
        .def("flags", &SkSurfaceProps::flags)
        .def("pixelGeometry", &SkSurfaceProps::pixelGeometry)
        .def("isUseDeviceIndependentFonts", &SkSurfaceProps::isUseDeviceIndependentFonts)
        .def(py::self == py::self)
        .def(py::self != py::self);

    py::class_<SkSurface, sk_sp<SkSurface>> Surface(m, "Surface", py::buffer_protocol(), R"doc(
        :py:class:`Surface` is responsible for managing the pixels that a canvas draws into.

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
                throw std::runtime_error("Surface does not have pixels");
            })
        .def(py::init(&SkSurface::MakeRasterN32Premul), "width"_a, "height"_a, "surfaceProps"_a = py::none())
        .def(py::init(
                 [](py::array &array, const SkColorType &ct, const SkAlphaType &at, const sk_sp<SkColorSpace> &cs,
                    const SkSurfaceProps *surfaceProps)
                 {
                     return SkSurface::MakeRasterDirect(ndarrayToImageInfo(array, ct, at, cs), array.mutable_data(),
                                                        array.strides(0), surfaceProps);
                 }),
             "Creates :py:class:`Surface` backed by numpy array.", "array"_a,
             "colorType"_a = SkColorType::kN32_SkColorType, "alphaType"_a = SkAlphaType::kUnpremul_SkAlphaType,
             "colorSpace"_a = py::none(), "surfaceProps"_a = py::none(), py::keep_alive<1, 2>())
        .def("toarray", &readToNumpy<SkSurface>, "Returns a ``ndarray`` of the image's pixels.", "srcX"_a = 0,
             "srcY"_a = 0, "colorType"_a = SkColorType::kN32_SkColorType,
             "alphaType"_a = SkAlphaType::kUnpremul_SkAlphaType, "colorSpace"_a = py::none())
        .def_static(
            "MakeRasterDirect",
            [](const SkImageInfo &imageInfo, const py::buffer &pixels, const size_t &rowBytes,
               const SkSurfaceProps *surfaceProps)
            {
                py::buffer_info bufInfo = pixels.request();
                return SkSurface::MakeRasterDirect(
                    imageInfo, bufInfo.ptr, validateImageInfo_Buffer(imageInfo, bufInfo, rowBytes), surfaceProps);
            },
            "Allocates raster :py:class:`Surface` with the specified *pixels*.", "imageInfo"_a, "pixels"_a,
            "rowBytes"_a = 0, "surfaceProps"_a = py::none())
        .def_static("MakeRasterDirect",
                    py::overload_cast<const SkPixmap &, const SkSurfaceProps *>(&SkSurface::MakeRasterDirect),
                    "pixmap"_a, "surfaceProps"_a = py::none())
        .def_static("MakeRaster",
                    py::overload_cast<const SkImageInfo &, size_t, const SkSurfaceProps *>(&SkSurface::MakeRaster),
                    "imageInfo"_a, "rowBytes"_a = 0, "surfaceProps"_a = py::none())
        .def_static("MakeRasterN32Premul", &SkSurface::MakeRasterN32Premul, "width"_a, "height"_a,
                    "surfaceProps"_a = py::none())
        .def_static("MakeNull", &SkSurface::MakeNull, "width"_a, "height"_a)
        .def("width", &SkSurface::width)
        .def("height", &SkSurface::height)
        .def("imageInfo", &SkSurface::imageInfo)
        .def("generationID", &SkSurface::generationID);

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
             "canvas"_a, "x"_a, "y"_a, "sampling"_a = SkSamplingOptions(), "paint"_a = py::none())
        .def(
            "peekPixels",
            [](SkSurface &self)
            {
                SkPixmap pixmap;
                if (self.peekPixels(&pixmap))
                    return pixmap;
                throw std::runtime_error("Failed to peek pixels");
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