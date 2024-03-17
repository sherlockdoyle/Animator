#include "common.h"
#include "include/core/SkCanvas.h"
#include "include/core/SkPath.h"
#include "include/core/SkVertices.h"

void initPlot(py::module &m)
{
    m.def(
         "Path_Polygon",
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
            "mode"_a, "pts"_a, "matrix"_a, "paint"_a)
        .def(
            "Vertices__init__",
            [](const py::array &positions, const py::array &colors)
            {
                const ssize_t vertexCount = positions.size() / 2;
                if (colors.size() != vertexCount * 4)
                    throw py::value_error("positions and colors must be the same length.");

                const SkColor4f *color4fs = static_cast<const SkColor4f *>(colors.data());
                std::vector<SkColor> colors_cast(vertexCount);
                for (ssize_t i = 0; i < vertexCount; ++i)
                    colors_cast[i] = color4fs[i].toSkColor();
                return SkVertices::MakeCopy(SkVertices::VertexMode::kTriangles_VertexMode, vertexCount,
                                            static_cast<const SkPoint *>(positions.data()), nullptr,
                                            colors_cast.data());
            },
            "Constructs a vertices with the specified *positions* and *colors* (array of Color4f).", "positions"_a,
            "colors"_a);
}