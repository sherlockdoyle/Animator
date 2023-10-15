#ifndef _COMMON_H_
#define _COMMON_H_

#include "include/core/SkImageInfo.h"
#include "include/core/SkRefCnt.h"
#include "include/core/SkString.h"
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

using namespace pybind11::literals;
namespace py = pybind11;

PYBIND11_DECLARE_HOLDER_TYPE(T, sk_sp<T>);

SkImageInfo ndarrayToImageInfo(const py::array &array, const SkColorType &ct, const SkAlphaType &at,
                               const sk_sp<SkColorSpace> &cs);
size_t validateImageInfo_Buffer(const SkImageInfo &imgInfo, const py::buffer_info &bufInfo, size_t rowBytes);
py::buffer_info imageInfoToBufferInfo(const SkImageInfo &imgInfo, void *data, py::ssize_t rowBytes, bool readonly);

template <typename T>
bool readPixels(T &readable, const SkImageInfo &imgInfo, const py::buffer &dstPixels, size_t dstRowBytes, int srcX,
                int srcY)
{
    const py::buffer_info bufInfo = dstPixels.request();
    return readable.readPixels(imgInfo, bufInfo.ptr, validateImageInfo_Buffer(imgInfo, bufInfo, dstRowBytes), srcX,
                               srcY);
}
template <typename T>
py::array readToNumpy(T &readable, int srcX, int srcY, SkColorType ct, SkAlphaType at, const sk_sp<SkColorSpace> &cs)
{
    SkImageInfo imgInfo = SkImageInfo::Make(readable.imageInfo().dimensions(), ct, at, cs);
    py::array array(imageInfoToBufferInfo(imgInfo, nullptr, 0, false));
    if (readable.readPixels(imgInfo, array.mutable_data(), imgInfo.minRowBytes(), srcX, srcY))
        return array;
    throw py::value_error("Failed to read pixels.");
}

static inline py::str SkString2pyStr(const SkString &s) { return py::str(s.c_str(), s.size()); }

void initBitmap(py::module &);
void initBlender(py::module &);
void initCanvas(py::module &);
void initCms(py::module &);
// void initCodec(py::module &);
void initColor(py::module &);
void initColorFilter(py::module &);
void initColorSpace(py::module &);
void initDartTypes(py::module &);
void initData(py::module &);
void initExtras(py::module &);
void initFlattenable(py::module &);
void initFont(py::module &);
void initImage(py::module &);
void initImageFilter(py::module &);
void initImageInfo(py::module &);
void initMaskFilter(py::module &);
void initMatrix(py::module &);
void initPaint(py::module &);
void initParagraph(py::module &);
void initParagraphStyle(py::module &);
void initPath(py::module &);
void initPathEffect(py::module &);
void initPathMeasure(py::module &);
void initPicture(py::module &);
void initPixmap(py::module &);
void initPlot(py::module &);
void initPoint(py::module &);
void initRect(py::module &);
void initRegion(py::module &);
void initRuntimeEffect(py::module &);
void initSize(py::module &);
void initShader(py::module &);
void initShadow(py::module &);
void initSurface(py::module &);
void initSvg(py::module &);
void initTextBlob(py::module &);
void initTextlayout(py::module &);
void initTextStyle(py::module &);
void initUniqueColor(py::module &);
void initVertices(py::module &);
// void initSVGDOM(py::module &);

#endif