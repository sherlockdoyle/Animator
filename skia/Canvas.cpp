#include "common.h"
#include "include/core/SkBitmap.h"
#include "include/core/SkCanvas.h"
#include "include/core/SkColorSpace.h"
#include "include/core/SkFont.h"
#include "include/core/SkPath.h"
#include "include/core/SkPicture.h"
#include "include/core/SkPoint3.h"
#include "include/core/SkRRect.h"
#include "include/core/SkRSXform.h"
#include "include/core/SkRegion.h"
#include "include/core/SkShader.h"
#include "include/core/SkSurface.h"
#include "include/core/SkTextBlob.h"
#include "include/core/SkVertices.h"
#include "include/utils/SkNullCanvas.h"
#include "include/utils/SkShadowUtils.h"
#include "include/utils/SkTextUtils.h"
#include "modules/skparagraph/include/Paragraph.h"
#include <pybind11/stl.h>

struct PyLattice : public SkCanvas::Lattice
{
    PyLattice(int xCount, int yCount)
    {
        fXDivs = nullptr;
        fYDivs = nullptr;
        fRectTypes = nullptr;
        fXCount = xCount;
        fYCount = yCount;
        fBounds = nullptr;
        fColors = nullptr;
    }
    ~PyLattice()
    {
        delete[] fXDivs;
        delete[] fYDivs;
        delete[] fRectTypes;
        delete fBounds;
        delete[] fColors;
    }
};

void initCanvas(py::module &m)
{
    py::enum_<SkClipOp>(m, "ClipOp")
        .value("kDifference", SkClipOp::kDifference)
        .value("kIntersect", SkClipOp::kIntersect)
        .value("kMax_EnumValue", SkClipOp::kMax_EnumValue);

    py::class_<SkCanvas, std::unique_ptr<SkCanvas>> Canvas(m, "Canvas");
    Canvas
        .def(py::init(
                 [](py::array &array, const SkColorType &ct, const SkAlphaType &at, const sk_sp<SkColorSpace> &cs,
                    const SkSurfaceProps *surfaceProps)
                 {
                     SkImageInfo info = ndarrayToImageInfo(array, ct, at, cs);
                     std::unique_ptr<SkCanvas> canvas =
                         SkCanvas::MakeRasterDirect(info, array.mutable_data(), array.strides(0), surfaceProps);
                     if (!canvas)
                         throw py::value_error("Failed to create canvas");
                     return canvas;
                 }),
             R"doc(
                Creates raster :py:class:`Canvas` backed by numpy array.

                :param array: numpy array of shape=(height, width, channels) and appropriate dtype. Must have the valid
                    number of channels for the specified color type.
                :param ct: color type
                :param at: alpha type
                :param cs: color space
                :param surfaceProps: optional surface properties
            )doc",
             "array"_a, "ct"_a = SkColorType::kN32_SkColorType, "at"_a = SkAlphaType::kUnpremul_SkAlphaType,
             "cs"_a = nullptr, "surfaceProps"_a = nullptr)
        .def("toarray", &readToNumpy<SkCanvas>, "Returns a ``ndarray`` of the current canvas' pixels.", "srcX"_a = 0,
             "srcY"_a = 0, "ct"_a = SkColorType::kN32_SkColorType, "at"_a = SkAlphaType::kUnpremul_SkAlphaType,
             "cs"_a = nullptr)
        .def_static(
            "MakeRasterDirect",
            [](const SkImageInfo &info, const py::buffer &pixels, size_t rowBytes, const SkSurfaceProps *props)
            {
                py::buffer_info buf = pixels.request();
                rowBytes = validateImageInfo_Buffer(info, buf, rowBytes);
                std::unique_ptr<SkCanvas> canvas = SkCanvas::MakeRasterDirect(info, buf.ptr, rowBytes, props);
                if (!canvas)
                    throw py::value_error("Failed to create canvas");
                return canvas;
            },
            R"doc(
                Allocates raster :py:class:`Canvas` that will draw directly into pixel buffer.

                :param info: :py:class:`ImageInfo` describing pixel buffer
                :param pixels: pixel buffer
                :param rowBytes: number of bytes per row
                :param props: optional :py:class:`SurfaceProps`
            )doc",
            "info"_a, "pixels"_a, "rowBytes"_a = 0, "props"_a = nullptr)
        .def_static(
            "MakeRasterDirectN32",
            [](const int &width, const int &height, const py::buffer &pixels, size_t rowBytes)
            {
                py::buffer_info buf = pixels.request();
                rowBytes = validateImageInfo_Buffer(SkImageInfo::MakeN32Premul(width, height), buf, rowBytes);
                std::unique_ptr<SkCanvas> canvas =
                    SkCanvas::MakeRasterDirectN32(width, height, static_cast<SkPMColor *>(buf.ptr), rowBytes);
                if (!canvas)
                    throw py::value_error("Failed to create canvas");
                return canvas;
            },
            "Allocates raster :py:class:`Canvas` that will draw directly into pixel buffer.", "width"_a, "height"_a,
            "pixels"_a, "rowBytes"_a)
        .def(py::init())
        .def(py::init<int, int, const SkSurfaceProps *>(), "width"_a, "height"_a, "props"_a = nullptr)
        .def(py::init<const SkBitmap &>(), "bitmap"_a)
        .def(py::init<const SkBitmap &, const SkSurfaceProps &>(), "bitmap"_a, "props"_a)
        .def("imageInfo", &SkCanvas::imageInfo)
        .def(
            "getProps",
            [](const SkCanvas &canvas) -> std::optional<SkSurfaceProps>
            {
                SkSurfaceProps props;
                if (canvas.getProps(&props))
                    return props;
                return std::nullopt;
            },
            R"doc(
                Returns :py:class:`SurfaceProps`, if :py:class:`Canvas` is associated with raster surface. Otherwise,
                returns ``None``.
            )doc")
        .def("getBaseProps", &SkCanvas::getBaseProps)
        .def("getTopProps", &SkCanvas::getTopProps)
        .def("getBaseLayerSize", &SkCanvas::getBaseLayerSize)
        .def("makeSurface", &SkCanvas::makeSurface, "info"_a, "props"_a = nullptr)
        .def("getSurface", &SkCanvas::getSurface, py::return_value_policy::reference)
        .def(
            "accessTopLayerPixels",
            [](SkCanvas &self) -> std::optional<py::tuple>
            {
                SkImageInfo info;
                size_t rowBytes;
                SkIPoint origin;
                void *addr = self.accessTopLayerPixels(&info, &rowBytes, &origin);
                if (!addr)
                    return std::nullopt;
                const py::buffer_info bufInfo = imageInfoToBufferInfo(info, addr, rowBytes, true);
                return py::make_tuple(py::memoryview::from_buffer(bufInfo.ptr, bufInfo.itemsize, bufInfo.format.c_str(),
                                                                  bufInfo.shape, bufInfo.strides, bufInfo.readonly),
                                      info, rowBytes, origin);
            },
            R"doc(
                Returns a tuple of ``(memoryview of pixels, image info, rowBytes, origin)`` if the pixels can be read
                directly. Otherwise, returns ``None``.
            )doc")
        .def(
            "peekPixels",
            [](SkCanvas &self)
            {
                SkPixmap pixmap;
                if (self.peekPixels(&pixmap))
                    return pixmap;
                throw std::runtime_error("Failed to peek pixels");
            },
            "Returns a :py:class:`Pixmap` describing the pixel data.")
        .def("readPixels", &readPixels<SkCanvas>,
             "Copies *dstInfo* pixels starting from (*srcX*, *srcY*) to *dstPixels* buffer.", "dstInfo"_a,
             "dstPixels"_a, "dstRowBytes"_a = 0, "srcX"_a = 0, "srcY"_a = 0)
        .def("readPixels", py::overload_cast<const SkPixmap &, int, int>(&SkCanvas::readPixels), "pixmap"_a,
             "srcX"_a = 0, "srcY"_a = 0)
        .def("readPixels", py::overload_cast<const SkBitmap &, int, int>(&SkCanvas::readPixels), "bitmap"_a,
             "srcX"_a = 0, "srcY"_a = 0)
        .def(
            "writePixels",
            [](SkCanvas &canvas, const SkImageInfo &info, const py::buffer &pixels, const size_t &rowBytes,
               const int &x, const int &y)
            {
                const py::buffer_info bufInfo = pixels.request();
                return canvas.writePixels(info, bufInfo.ptr, validateImageInfo_Buffer(info, bufInfo, rowBytes), x, y);
            },
            "Writes *pixels* from a buffer to the canvas.", "info"_a, "pixels"_a, "rowBytes"_a = 0, "x"_a = 0,
            "y"_a = 0)
        .def("writePixels", py::overload_cast<const SkBitmap &, int, int>(&SkCanvas::writePixels), "bitmap"_a,
             "x"_a = 0, "y"_a = 0)
        .def("save", &SkCanvas::save)
        .def("saveLayer", py::overload_cast<const SkRect *, const SkPaint *>(&SkCanvas::saveLayer),
             "bounds"_a = nullptr, "paint"_a = nullptr)
        .def("saveLayerAlphaf", &SkCanvas::saveLayerAlphaf, "bounds"_a, "alpha"_a)
        .def("saveLayerAlpha", &SkCanvas::saveLayerAlpha, "bounds"_a, "alpha"_a);

    py::enum_<SkCanvas::SaveLayerFlagsSet>(Canvas, "SaveLayerFlags", py::arithmetic())
        .value("kPreserveLCDText_SaveLayerFlag", SkCanvas::SaveLayerFlagsSet::kPreserveLCDText_SaveLayerFlag)
        .value("kInitWithPrevious_SaveLayerFlag", SkCanvas::SaveLayerFlagsSet::kInitWithPrevious_SaveLayerFlag)
        .value("kF16ColorType", SkCanvas::SaveLayerFlagsSet::kF16ColorType);

    py::class_<SkCanvas::SaveLayerRec>(Canvas, "SaveLayerRec")
        .def(py::init())
        .def(py::init<const SkRect *, const SkPaint *, SkCanvas::SaveLayerFlags>(), py::keep_alive<1, 3>(),
             "bounds"_a = nullptr, "paint"_a = nullptr, "saveLayerFlags"_a = 0)
        .def(py::init<const SkRect *, const SkPaint *, const SkImageFilter *, SkCanvas::SaveLayerFlags>(),
             py::keep_alive<1, 3>(), py::keep_alive<1, 4>(), "bounds"_a = nullptr, "paint"_a = nullptr,
             "backdrop"_a = nullptr, "saveLayerFlags"_a = 0)
        .def_readwrite("fBounds", &SkCanvas::SaveLayerRec::fBounds)
        .def_readwrite("fPaint", &SkCanvas::SaveLayerRec::fPaint)
        .def_readwrite("fBackdrop", &SkCanvas::SaveLayerRec::fBackdrop)
        .def_readwrite("fSaveLayerFlags", &SkCanvas::SaveLayerRec::fSaveLayerFlags);
    Canvas.def("saveLayer", py::overload_cast<const SkCanvas::SaveLayerRec &>(&SkCanvas::saveLayer), "layerRec"_a)
        .def("restore", &SkCanvas::restore)
        .def("getSaveCount", &SkCanvas::getSaveCount)
        .def("restoreToCount", &SkCanvas::restoreToCount, "saveCount"_a)
        .def("translate", &SkCanvas::translate, "dx"_a, "dy"_a)
        .def("scale", &SkCanvas::scale, "sx"_a, "sy"_a)
        .def("rotate", py::overload_cast<SkScalar>(&SkCanvas::rotate), "degrees"_a)
        .def("rotate", py::overload_cast<SkScalar, SkScalar, SkScalar>(&SkCanvas::rotate), "degrees"_a, "px"_a, "py"_a)
        .def("skew", &SkCanvas::skew, "sx"_a, "sy"_a)
        .def("concat", py::overload_cast<const SkMatrix &>(&SkCanvas::concat), "matrix"_a)
        .def("concat", py::overload_cast<const SkM44 &>(&SkCanvas::concat), "m"_a)
        .def("setMatrix", py::overload_cast<const SkM44 &>(&SkCanvas::setMatrix), "matrix"_a)
        .def("setMatrix", py::overload_cast<const SkMatrix &>(&SkCanvas::setMatrix), "matrix"_a)
        .def("resetMatrix", &SkCanvas::resetMatrix)
        .def("clipRect", py::overload_cast<const SkRect &, SkClipOp, bool>(&SkCanvas::clipRect), "rect"_a,
             "op"_a = SkClipOp::kIntersect, "doAntiAlias"_a = false)
        .def("clipIRect", py::overload_cast<const SkIRect &, SkClipOp>(&SkCanvas::clipIRect), "irect"_a,
             "op"_a = SkClipOp::kIntersect)
        .def("clipRRect", py::overload_cast<const SkRRect &, SkClipOp, bool>(&SkCanvas::clipRRect), "rrect"_a,
             "op"_a = SkClipOp::kIntersect, "doAntiAlias"_a = false)
        .def("clipPath", py::overload_cast<const SkPath &, SkClipOp, bool>(&SkCanvas::clipPath), "path"_a,
             "op"_a = SkClipOp::kIntersect, "doAntiAlias"_a = false)
        .def("clipShader", &SkCanvas::clipShader, "sh"_a, "op"_a = SkClipOp::kIntersect)
        .def("clipRegion", &SkCanvas::clipRegion, "deviceRgn"_a, "op"_a = SkClipOp::kIntersect)
        .def("quickReject", py::overload_cast<const SkRect &>(&SkCanvas::quickReject, py::const_), "rect"_a)
        .def("quickReject", py::overload_cast<const SkPath &>(&SkCanvas::quickReject, py::const_), "path"_a)
        .def("getLocalClipBounds", py::overload_cast<>(&SkCanvas::getLocalClipBounds, py::const_))
        .def("getDeviceClipBounds", py::overload_cast<>(&SkCanvas::getDeviceClipBounds, py::const_))
        .def("drawColor", py::overload_cast<SkColor, SkBlendMode>(&SkCanvas::drawColor), "color"_a,
             "mode"_a = SkBlendMode::kSrcOver)
        .def("drawColor", py::overload_cast<const SkColor4f &, SkBlendMode>(&SkCanvas::drawColor), "color"_a,
             "mode"_a = SkBlendMode::kSrcOver)
        .def("clear", py::overload_cast<SkColor>(&SkCanvas::clear), "color"_a)
        .def("clear", py::overload_cast<const SkColor4f &>(&SkCanvas::clear), "color"_a)
        .def("discard", &SkCanvas::discard)
        .def("drawPaint", &SkCanvas::drawPaint, "paint"_a);

    py::enum_<SkCanvas::PointMode>(Canvas, "PointMode")
        .value("kPoints_PointMode", SkCanvas::PointMode::kPoints_PointMode)
        .value("kLines_PointMode", SkCanvas::PointMode::kLines_PointMode)
        .value("kPolygon_PointMode", SkCanvas::PointMode::kPolygon_PointMode);
    Canvas
        .def(
            "drawPoints",
            [](SkCanvas &self, const SkCanvas::PointMode &mode, const std::vector<SkPoint> &pts, const SkPaint &paint)
            { self.drawPoints(mode, pts.size(), pts.data(), paint); },
            "Draw a list of points, *pts*, with the specified *mode* and *paint*.", "mode"_a, "pts"_a, "paint"_a)
        .def("drawPoint", py::overload_cast<SkScalar, SkScalar, const SkPaint &>(&SkCanvas::drawPoint), "x"_a, "y"_a,
             "paint"_a)
        .def("drawPoint", py::overload_cast<SkPoint, const SkPaint &>(&SkCanvas::drawPoint), "p"_a, "paint"_a)
        .def("drawLine",
             py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar, const SkPaint &>(&SkCanvas::drawLine), "x0"_a,
             "y0"_a, "x1"_a, "y1"_a, "paint"_a)
        .def("drawLine", py::overload_cast<SkPoint, SkPoint, const SkPaint &>(&SkCanvas::drawLine), "p0"_a, "p1"_a,
             "paint"_a)
        .def("drawRect", &SkCanvas::drawRect, "rect"_a, "paint"_a)
        .def("drawIRect", &SkCanvas::drawIRect, "rect"_a, "paint"_a)
        .def("drawRegion", &SkCanvas::drawRegion, "region"_a, "paint"_a)
        .def("drawOval", &SkCanvas::drawOval, "oval"_a, "paint"_a)
        .def("drawRRect", &SkCanvas::drawRRect, "rrect"_a, "paint"_a)
        .def("drawDRRect", &SkCanvas::drawDRRect, "outer"_a, "inner"_a, "paint"_a)
        .def("drawCircle", py::overload_cast<SkScalar, SkScalar, SkScalar, const SkPaint &>(&SkCanvas::drawCircle),
             "cx"_a, "cy"_a, "radius"_a, "paint"_a)
        .def("drawCircle", py::overload_cast<SkPoint, SkScalar, const SkPaint &>(&SkCanvas::drawCircle), "center"_a,
             "radius"_a, "paint"_a)
        .def("drawArc", &SkCanvas::drawArc, "oval"_a, "startAngle"_a, "sweepAngle"_a, "useCenter"_a, "paint"_a)
        .def("drawRoundRect", &SkCanvas::drawRoundRect, "rect"_a, "rx"_a, "ry"_a, "paint"_a)
        .def("drawPath", &SkCanvas::drawPath, "path"_a, "paint"_a)
        .def("drawImage", py::overload_cast<const sk_sp<SkImage> &, SkScalar, SkScalar>(&SkCanvas::drawImage),
             "image"_a, "left"_a, "top"_a);

    py::enum_<SkCanvas::SrcRectConstraint>(Canvas, "SrcRectConstraint")
        .value("kStrict_SrcRectConstraint", SkCanvas::SrcRectConstraint::kStrict_SrcRectConstraint)
        .value("kFast_SrcRectConstraint", SkCanvas::SrcRectConstraint::kFast_SrcRectConstraint);
    Canvas
        .def("drawImage",
             py::overload_cast<const sk_sp<SkImage> &, SkScalar, SkScalar, const SkSamplingOptions &, const SkPaint *>(
                 &SkCanvas::drawImage),
             "image"_a, "left"_a, "top"_a, "sampling"_a = dso, "paint"_a = nullptr)
        .def("drawImageRect",
             py::overload_cast<const sk_sp<SkImage> &, const SkRect &, const SkRect &, const SkSamplingOptions &,
                               const SkPaint *, SkCanvas::SrcRectConstraint>(&SkCanvas::drawImageRect),
             "image"_a, "src"_a, "dst"_a, "sampling"_a = dso, "paint"_a = nullptr,
             "constraint"_a = SkCanvas::SrcRectConstraint::kFast_SrcRectConstraint)
        .def("drawImageRect",
             py::overload_cast<const sk_sp<SkImage> &, const SkRect &, const SkSamplingOptions &, const SkPaint *>(
                 &SkCanvas::drawImageRect),
             "image"_a, "dst"_a, "sampling"_a = dso, "paint"_a = nullptr)
        .def("drawImageNine",
             py::overload_cast<const SkImage *, const SkIRect &, const SkRect &, SkFilterMode, const SkPaint *>(
                 &SkCanvas::drawImageNine),
             "image"_a, "center"_a, "dst"_a, "filter"_a, "paint"_a = nullptr);

    py::class_<PyLattice> Lattice(Canvas, "Lattice");

    py::enum_<SkCanvas::Lattice::RectType>(Lattice, "RectType")
        .value("kDefault", SkCanvas::Lattice::RectType::kDefault)
        .value("kTransparent", SkCanvas::Lattice::RectType::kTransparent)
        .value("kFixedColor", SkCanvas::Lattice::RectType::kFixedColor);
    Lattice
        .def(py::init(
                 [](const py::list &fXDivs, const py::list &fYDivs, const std::optional<py::list> &fRectTypes,
                    const SkIRect *fBounds, const std::optional<py::list> &fColors)
                 {
                     const int xCount = fXDivs.size(), yCount = fYDivs.size();
                     if (xCount == 0 || yCount == 0)
                         throw py::value_error("Lattice must have at least one div");

                     std::unique_ptr<int[]> xDivs(new int[xCount]);
                     std::unique_ptr<int[]> yDivs(new int[yCount]);
                     std::unique_ptr<SkCanvas::Lattice::RectType[]> rectTypes;
                     std::unique_ptr<SkIRect> bounds;
                     std::unique_ptr<SkColor[]> colors;

                     for (int i = 0; i < xCount; ++i)
                         xDivs[i] = fXDivs[i].cast<int>();
                     for (int i = 0; i < yCount; ++i)
                         yDivs[i] = fYDivs[i].cast<int>();

                     if (fRectTypes)
                     {
                         const int rectCount = fRectTypes->size();
                         if (rectCount != xCount * yCount)
                             throw py::value_error("Lattice must have rectTypes for every div");
                         rectTypes = std::make_unique<SkCanvas::Lattice::RectType[]>(rectCount);
                         for (int i = 0; i < rectCount; ++i)
                             rectTypes[i] = fRectTypes->operator[](i).cast<SkCanvas::Lattice::RectType>();
                     }

                     if (fBounds)
                         bounds = std::make_unique<SkIRect>(
                             SkIRect{fBounds->fLeft, fBounds->fTop, fBounds->fRight, fBounds->fBottom});

                     if (fColors)
                     {
                         const int colorCount = fColors->size();
                         if (colorCount != xCount * yCount)
                             throw py::value_error("Lattice must have colors for every div");
                         colors = std::make_unique<SkColor[]>(colorCount);
                         for (int i = 0; i < colorCount; ++i)
                             colors[i] = fColors->operator[](i).cast<SkColor>();
                     }

                     std::unique_ptr<PyLattice> lattice = std::make_unique<PyLattice>(fXDivs.size(), fYDivs.size());
                     lattice->fXDivs = xDivs.release();
                     lattice->fYDivs = yDivs.release();
                     lattice->fRectTypes = rectTypes.release();
                     lattice->fBounds = bounds.release();
                     lattice->fColors = colors.release();
                     return lattice;
                 }),
             "Constructs a lattice from the given divs, rectTypes, bounds, and colors.", "fXDivs"_a, "fYDivs"_a,
             "fRectTypes"_a = std::nullopt, "fBounds"_a = nullptr, "fColors"_a = std::nullopt)
        .def_property_readonly("fXDivs", [](const PyLattice &self)
                               { return std::vector<int>(self.fXDivs, self.fXDivs + self.fXCount); })
        .def_property_readonly("fYDivs", [](const PyLattice &self)
                               { return std::vector<int>(self.fYDivs, self.fYDivs + self.fYCount); })
        .def_property_readonly("fRectTypes",
                               [](const PyLattice &self) -> std::optional<std::vector<SkCanvas::Lattice::RectType>>
                               {
                                   if (self.fRectTypes)
                                       return std::vector<SkCanvas::Lattice::RectType>(
                                           self.fRectTypes, self.fRectTypes + self.fXCount * self.fYCount);
                                   return std::nullopt;
                               })
        .def_readonly("fXCount", &PyLattice::fXCount)
        .def_readonly("fYCount", &PyLattice::fYCount)
        .def_readonly("fBounds", &PyLattice::fBounds)
        .def_property_readonly("fColors",
                               [](const PyLattice &self) -> std::optional<std::vector<SkColor>>
                               {
                                   if (self.fColors)
                                       return std::vector<SkColor>(self.fColors,
                                                                   self.fColors + self.fXCount * self.fYCount);
                                   return std::nullopt;
                               })
        .def("__str__", [](const PyLattice &self) { return "Lattice({} x {})"_s.format(self.fXCount, self.fYCount); });
    Canvas
        .def("drawImageLattice",
             py::overload_cast<const SkImage *, const SkCanvas::Lattice &, const SkRect &, SkFilterMode,
                               const SkPaint *>(&SkCanvas::drawImageLattice),
             "image"_a, "lattice"_a, "dst"_a, "filter"_a = SkFilterMode::kNearest, "paint"_a = nullptr)
        .def(
            "drawSimpleText",
            [](SkCanvas &self, const std::string &text, const SkTextEncoding &encoding, const SkScalar &x,
               const SkScalar &y, const SkFont &font, const SkPaint &paint)
            { self.drawSimpleText(text.c_str(), text.size(), encoding, x, y, font, paint); },
            "Draws *text* at (*x*, *y*) using *font* and *paint*.", "text"_a, "encoding"_a, "x"_a, "y"_a, "font"_a,
            "paint"_a)
        .def(
            "drawString",
            py::overload_cast<const char[], SkScalar, SkScalar, const SkFont &, const SkPaint &>(&SkCanvas::drawString),
            "text"_a, "x"_a, "y"_a, "font"_a, "paint"_a)
        .def(
            "drawGlyphs",
            [](SkCanvas &self, const std::vector<SkGlyphID> &glyphs, const std::vector<SkPoint> &positions,
               const std::vector<uint32_t> &clusters, const std::string &utf8text, const SkPoint &origin,
               const SkFont &font, const SkPaint &paint)
            {
                const size_t count = glyphs.size();
                if (positions.size() != count || clusters.size() != count)
                    throw py::value_error("glyphs, positions, and clusters must be the same length");
                self.drawGlyphs(count, glyphs.data(), positions.data(), clusters.data(), utf8text.size(),
                                utf8text.c_str(), origin, font, paint);
            },
            R"doc(
                Draws *glyphs*, at *positions* relative to *origin* styled with *font* and *paint* with supporting
                *utf8text* and *clusters* information.
            )doc",
            "glyphs"_a, "positions"_a, "clusters"_a, "utf8text"_a, "origin"_a, "font"_a, "paint"_a)
        .def(
            "drawGlyphs",
            [](SkCanvas &self, const std::vector<SkGlyphID> &glyphs, const std::vector<SkPoint> &positions,
               const SkPoint &origin, const SkFont &font, const SkPaint &paint)
            {
                const size_t count = glyphs.size();
                if (positions.size() != count)
                    throw py::value_error("glyphs and positions must be the same length");
                self.drawGlyphs(count, glyphs.data(), positions.data(), origin, font, paint);
            },
            "Draws *glyphs*, at *positions* relative to *origin* styled with *font* and *paint*.", "glyphs"_a,
            "positions"_a, "origin"_a, "font"_a, "paint"_a)
        .def(
            "drawGlyphs",
            [](SkCanvas &self, const std::vector<SkGlyphID> &glyphs, const std::vector<SkRSXform> &xforms,
               const SkPoint &origin, const SkFont &font, const SkPaint &paint)
            {
                const size_t count = glyphs.size();
                if (xforms.size() != count)
                    throw py::value_error("glyphs and xforms must be the same length");
                self.drawGlyphs(count, glyphs.data(), xforms.data(), origin, font, paint);
            },
            "Draws *glyphs*, with *xforms* relative to *origin* styled with *font* and *paint*.", "glyphs"_a,
            "xforms"_a, "origin"_a, "font"_a, "paint"_a)
        .def("drawTextBlob",
             py::overload_cast<const sk_sp<SkTextBlob> &, SkScalar, SkScalar, const SkPaint &>(&SkCanvas::drawTextBlob),
             "blob"_a, "x"_a, "y"_a, "paint"_a)
        .def("drawPicture",
             py::overload_cast<const sk_sp<SkPicture> &, const SkMatrix *, const SkPaint *>(&SkCanvas::drawPicture),
             "picture"_a, "matrix"_a = nullptr, "paint"_a = nullptr)
        .def("drawVertices",
             py::overload_cast<const sk_sp<SkVertices> &, SkBlendMode, const SkPaint &>(&SkCanvas::drawVertices),
             "vertices"_a, "mode"_a, "paint"_a)
        .def(
            "drawPatch",
            [](SkCanvas &self, const std::vector<SkPoint> &cubics, const std::optional<std::vector<SkColor>> &colors,
               const std::optional<std::vector<SkPoint>> &texCoords, const SkBlendMode &mode, const SkPaint &paint)
            {
                if (cubics.size() != 12)
                    throw py::value_error("cubics must be a list of 12 points");
                if (colors && colors->size() != 4)
                    throw py::value_error("colors must be a list of 4 colors");
                if (texCoords && texCoords->size() != 4)
                    throw py::value_error("texCoords must be a list of 4 points");

                self.drawPatch(cubics.data(), colors ? colors->data() : nullptr,
                               texCoords ? texCoords->data() : nullptr, mode, paint);
            },
            "cubics"_a, "colors"_a, "texCoords"_a, "mode"_a, "paint"_a)
        .def(
            "drawAtlas",
            [](SkCanvas &self, const SkImage *atlas, const std::optional<std::vector<SkRSXform>> &xform,
               const std::vector<SkRect> &tex, const std::optional<std::vector<SkColor>> &colors,
               const SkBlendMode &mode, const SkSamplingOptions &sampling, const SkRect *cullRect, const SkPaint *paint)
            {
                if ((xform && xform->size() != tex.size()) || (colors && colors->size() != tex.size()))
                    throw py::value_error("xform and colors must be the same length as tex.");
                self.drawAtlas(atlas, xform ? xform->data() : nullptr, tex.data(), colors ? colors->data() : nullptr,
                               tex.size(), mode, sampling, cullRect, paint);
            },
            "Draws a set of sprites from *atlas*, defined by *xform*, *tex*, and *colors* using *mode* and *sampling*.",
            "atlas"_a, "xform"_a, "tex"_a, "colors"_a, "mode"_a, "sampling"_a, "cullRect"_a = nullptr,
            "paint"_a = nullptr)
        // .def("drawAnnotation",
        //      py::overload_cast<const SkRect &, const char[], const sk_sp<SkData> &>(&SkCanvas::drawAnnotation),
        //      "rect"_a, "key"_a, "value"_a)
        .def("isClipEmpty", &SkCanvas::isClipEmpty)
        .def("isClipRect", &SkCanvas::isClipRect)
        .def("getLocalToDevice", &SkCanvas::getLocalToDevice)
        .def("getLocalToDeviceAs3x3", &SkCanvas::getLocalToDeviceAs3x3)
        .def("getTotalMatrix", &SkCanvas::getTotalMatrix)
        .def(
            "drawParagraph",
            [](SkCanvas &self, skia::textlayout::Paragraph *const paragraph, const SkScalar &x, const SkScalar &y)
            { paragraph->paint(&self, x, y); },
            "Draws the *paragraph* at the given *x* and *y* position.", "paragraph"_a, "x"_a, "y"_a)
        .def("drawShadow", &SkShadowUtils::DrawShadow,
             "Draw an offset spot shadow and outlining ambient shadow for the given *path* using a disc light.",
             "path"_a, "zPlaneParams"_a, "lightPos"_a, "lightRadius"_a, "ambientColor"_a, "spotColor"_a,
             "flags"_a = SkShadowFlags::kNone_ShadowFlag)
        .def("__str__",
             [](const SkCanvas &self)
             {
                 const SkISize size = self.getBaseLayerSize();
                 return "Canvas({} x {})"_s.format(size.width(), size.height());
             });

    py::class_<SkAutoCanvasRestore>(m, "AutoCanvasRestore")
        .def(py::init<SkCanvas *, bool>(), "canvas"_a, "doSave"_a = true, py::keep_alive<1, 2>())
        .def("restore", &SkAutoCanvasRestore::restore)
        .def("__enter__", [](SkAutoCanvasRestore &) {})
        .def("__exit__", [](SkAutoCanvasRestore &self, py::args) { self.restore(); });

    m.def("MakeNullCanvas", &SkMakeNullCanvas);

    py::enum_<SkTextUtils::Align>(m, "TextUtils_Align")
        .value("kLeft_Align", SkTextUtils::Align::kLeft_Align)
        .value("kCenter_Align", SkTextUtils::Align::kCenter_Align)
        .value("kRight_Align", SkTextUtils::Align::kRight_Align);
    Canvas.def(
        "drawText",
        [](SkCanvas *self, const std::string &text, const SkScalar &x, const SkScalar &y, const SkFont &font,
           const SkPaint &paint, const SkTextEncoding &encoding, const SkTextUtils::Align &align)
        { SkTextUtils::Draw(self, text.c_str(), text.size(), encoding, x, y, font, paint, align); },
        "Draws the *text* at (*x*, *y*) using the given *font* and *paint* using SkTextUtils.", "text"_a, "x"_a, "y"_a,
        "font"_a, "paint"_a, "encoding"_a = SkTextEncoding::kUTF8, "align"_a = SkTextUtils::Align::kLeft_Align);

    // py::class_<SkSVGCanvas>(m, "SVGCanvas")
    //     .def_static("Make", &SkSVGCanvas::Make,
    //                 R"doc(
    //     Returns a new canvas that will generate SVG commands from its draw
    //     calls, and send them to the provided stream. Ownership of the stream is
    //     not transfered, and it must remain valid for the lifetime of the
    //     returned canvas::

    //         stream = skia.FILEWStream('output.svg')
    //         canvas = skia.SVGCanvas.Make((640, 480), stream)
    //         draw(canvas)
    //         # Make sure to delete the canvas before the stream goes out of scope
    //         del canvas
    //         stream.flush()

    //     The canvas may buffer some drawing calls, so the output is not
    //     guaranteed to be valid or complete until the canvas instance is deleted.

    //     The 'bounds' parameter defines an initial SVG viewport (viewBox
    //     attribute on the root SVG element).
    //     )doc",
    //                 "bounds"_a, "stream"_a, "flags"_a = 0)
    //     .def_property_readonly_static("kConvertTextToPaths_Flag",
    //                                   [](py::object obj) { return
    //                                   uint32_t(SkSVGCanvas::kConvertTextToPaths_Flag); })
    //     .def_property_readonly_static("kNoPrettyXML_Flag",
    //                                   [](py::object obj) { return uint32_t(SkSVGCanvas::kNoPrettyXML_Flag); })
    // ;
}