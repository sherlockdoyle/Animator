#include "common.h"
#include "include/core/SkCanvas.h"
#include "include/core/SkPath.h"

void initPlot(py::module &m)
{
    m.def(
         "Point_Polygon",
         [](const py::array &pts, const bool &isClosed, const SkPathFillType &fillType, const bool &isVolatile) {
             return SkPath::Polygon(static_cast<const SkPoint *>(pts.data()), pts.size() / 2, isClosed, fillType,
                                    isVolatile);
         },
         "points"_a, "isClosed"_a, "ft"_a = SkPathFillType::kWinding, "isVolatile"_a = false)
        .def(
            "Canvas_drawPoints",
            [](SkCanvas &canvas, const SkCanvas::PointMode &mode, py::array &pts, const SkMatrix &matrix,
               const SkPaint &paint)
            {
                SkPoint *pts_cast = static_cast<SkPoint *>(pts.mutable_data());
                const int count = pts.size() / 2;
                matrix.mapPoints(pts_cast, count);
                canvas.drawPoints(mode, count, pts_cast, paint);
            },
            "Draw points, *pts*, with the specified *mode* and *paint* after transforming by *matrix*.", "canvas"_a,
            "mode"_a, "pts"_a, "matrix"_a, "paint"_a);
}