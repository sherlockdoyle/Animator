#include "common.h"

PYBIND11_MODULE(skia, m)
{
    m.doc() = R"doc(
        Custom Skia bindings for animator.

        Refer to the Skia documentation for more information. Unless otherwise documented, all functions behave the same
        as the corresponding Skia function. Small changes like throwing exceptions instead of returning false have been
        made.
    )doc";

    initData(m);
    initFlattenable(m);
    initBlender(m);
    initPoint(m);
    initColor(m);
    initCms(m);
    initColorSpace(m);
    initSize(m);
    initRect(m);
    initImageInfo(m);
    initColorFilter(m);
    initMatrix(m);
    initFont(m);
    initPath(m);
    initSvg(m);
    initMaskFilter(m);
    initPaint(m);
    initPathEffect(m);
    initPixmap(m);
    initPicture(m);
    initRegion(m);
    initImage(m);
    initShader(m);
    initRuntimeEffect(m);
    initImageFilter(m);
    initBitmap(m);
    initSurface(m);
    initTextBlob(m);
    initVertices(m);
    initShadow(m);
    initTextlayout(m);
    initCanvas(m);
    initPathMeasure(m);

    initExtras(m);
}