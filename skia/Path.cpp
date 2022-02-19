#include "common.h"
#include "include/core/SkData.h"
#include "include/core/SkPath.h"
#include "include/core/SkPathBuilder.h"
#include "include/pathops/SkPathOps.h"
#include <pybind11/iostream.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>

void resizePoints(const SkPath::Verb &verb, std::vector<SkPoint> &pts)
{
    switch (verb)
    {
    case SkPath::Verb::kDone_Verb:
        pts.clear();
        break;
    case SkPath::Verb::kMove_Verb:
    case SkPath::Verb::kClose_Verb:
        pts.resize(1);
        break;
    case SkPath::Verb::kLine_Verb:
        pts.resize(2);
        break;
    case SkPath::Verb::kQuad_Verb:
    case SkPath::Verb::kConic_Verb:
        pts.resize(3);
        break;
    case SkPath::Verb::kCubic_Verb:
        break;
    }
}

void initPath(py::module &m)
{
    py::enum_<SkPathFillType>(m, "PathFillType")
        .value("kWinding", SkPathFillType::kWinding)
        .value("kEvenOdd", SkPathFillType::kEvenOdd)
        .value("kInverseWinding", SkPathFillType::kInverseWinding)
        .value("kInverseEvenOdd", SkPathFillType::kInverseEvenOdd)
        .def("isEvenOdd", &SkPathFillType_IsEvenOdd)
        .def("isInverse", &SkPathFillType_IsInverse)
        .def("convertToNonInverse", &SkPathFillType_ConvertToNonInverse);

    py::enum_<SkPathDirection>(m, "PathDirection")
        .value("kCW", SkPathDirection::kCW)
        .value("kCCW", SkPathDirection::kCCW);

    py::enum_<SkPathSegmentMask>(m, "PathSegmentMask", py::arithmetic())
        .value("kLine_PathSegmentMask", SkPathSegmentMask::kLine_SkPathSegmentMask)
        .value("kQuad_PathSegmentMask", SkPathSegmentMask::kQuad_SkPathSegmentMask)
        .value("kConic_PathSegmentMask", SkPathSegmentMask::kConic_SkPathSegmentMask)
        .value("kCubic_PathSegmentMask", SkPathSegmentMask::kCubic_SkPathSegmentMask);

    py::enum_<SkPathVerb>(m, "PathVerb")
        .value("kMove", SkPathVerb::kMove)
        .value("kLine", SkPathVerb::kLine)
        .value("kQuad", SkPathVerb::kQuad)
        .value("kConic", SkPathVerb::kConic)
        .value("kCubic", SkPathVerb::kCubic)
        .value("kClose", SkPathVerb::kClose);

    py::class_<SkPath> Path(m, "Path");
    Path.def_static(
            "Make",
            [](const std::vector<SkPoint> &pts, const std::vector<uint8_t> &vbs, const std::vector<SkScalar> &ws,
               SkPathFillType ft, bool isVolatile) {
                return SkPath::Make(pts.data(), pts.size(), vbs.data(), vbs.size(), ws.data(), ws.size(), ft,
                                    isVolatile);
            },
            "pts"_a, "vbs"_a, "ws"_a, "ft"_a, "isVolatile"_a = false)
        .def_static("Rect", &SkPath::Rect, "rect"_a, "dir"_a = SkPathDirection::kCW, "startIndex"_a = 0)
        .def_static("Oval", py::overload_cast<const SkRect &, SkPathDirection>(&SkPath::Oval), "r"_a,
                    "dir"_a = SkPathDirection::kCW)
        .def_static("Oval", py::overload_cast<const SkRect &, SkPathDirection, unsigned>(&SkPath::Oval), "r"_a, "dir"_a,
                    "startIndex"_a)
        .def_static("Circle", &SkPath::Circle, "center_x"_a, "center_y"_a, "radius"_a, "dir"_a = SkPathDirection::kCW)
        .def_static("RRect", py::overload_cast<const SkRRect &, SkPathDirection>(&SkPath::RRect), "rr"_a,
                    "dir"_a = SkPathDirection::kCW)
        .def_static("RRect", py::overload_cast<const SkRRect &, SkPathDirection, unsigned>(&SkPath::RRect), "rr"_a,
                    "dir"_a, "startIndex"_a)
        .def_static("RRect", py::overload_cast<const SkRect &, SkScalar, SkScalar, SkPathDirection>(&SkPath::RRect),
                    "bounds"_a, "rx"_a, "ry"_a, "dir"_a = SkPathDirection::kCW)
        .def_static(
            "Polygon",
            [](const std::vector<SkPoint> &pts, const bool &isClosed, const SkPathFillType &fillType,
               const bool &isVolatile)
            { return SkPath::Polygon(pts.data(), pts.size(), isClosed, fillType, isVolatile); },
            "Create a polygonal path from a list of points.", "points"_a, "isClosed"_a,
            "ft"_a = SkPathFillType::kWinding, "isVolatile"_a = false)
        .def_static("Line", &SkPath::Line, "a"_a, "b"_a)
        .def(py::init())
        .def(py::init<const SkPath &>(), "path"_a)
        .def(py::self == py::self, "other"_a)
        .def(py::self != py::self, "other"_a)
        .def("isInterpolatable", &SkPath::isInterpolatable, "compare"_a)
        .def(
            "interpolate",
            [](const SkPath &self, const SkPath &ending, const SkScalar &weight) -> std::optional<SkPath>
            {
                SkPath out;
                if (self.interpolate(ending, weight, &out))
                    return out;
                return std::nullopt;
            },
            R"doc(
                Interpolates between :py:class:`Path` with :py:class:`Point` array of equal size and return the result.
                If arrays were not equal size, returns ``None``.

                :param ending: :py:class:`Point` array averaged with this :py:class:`Point` array
                :param weight: contribution of this :py:class:`Point` array, and one minus contribution of *ending*
                    :py:class:`Point` array

                :return: interpolated average or None
                :rtype: :py:class:`Path` | None
            )doc",
            "ending"_a, "weight"_a)
        .def("getFillType", &SkPath::getFillType)
        .def("setFillType", &SkPath::setFillType, "ft"_a)
        .def("isInverseFillType", &SkPath::isInverseFillType)
        .def("toggleInverseFillType", &SkPath::toggleInverseFillType)
        .def("isConvex", &SkPath::isConvex)
        .def("isOval", &SkPath::isOval, "oval"_a = py::none())
        .def("isRRect", &SkPath::isRRect, "rrect"_a = py::none())
        .def("reset", &SkPath::reset)
        .def("rewind", &SkPath::rewind)
        .def("isEmpty", &SkPath::isEmpty)
        .def("isLastContourClosed", &SkPath::isLastContourClosed)
        .def("isFinite", &SkPath::isFinite)
        .def("isVolatile", &SkPath::isVolatile)
        .def("setIsVolatile", &SkPath::setIsVolatile, "isVolatile"_a)
        .def_static("IsLineDegenerate", &SkPath::IsLineDegenerate, "p1"_a, "p2"_a, "exact"_a)
        .def_static("IsQuadDegenerate", &SkPath::IsQuadDegenerate, "p1"_a, "p2"_a, "p3"_a, "exact"_a)
        .def_static("IsCubicDegenerate", &SkPath::IsCubicDegenerate, "p1"_a, "p2"_a, "p3"_a, "p4"_a, "exact"_a)
        .def(
            "isLine",
            [](const SkPath &self) -> std::optional<std::vector<SkPoint>>
            {
                std::vector<SkPoint> line(2);
                if (self.isLine(line.data()))
                    return line;
                return std::nullopt;
            },
            R"doc(
                If the :py:class:`Path` contains only one line, return the start and end points as a list of two
                :py:class:`Point`. If the :py:class:`Path` is not one line, return ``None``.

                :return: start and end points of the line or None
                :rtype: List[:py:class:`Point`] | None
            )doc")
        .def("countPoints", &SkPath::countPoints)
        .def("getPoint", &SkPath::getPoint, "index"_a)
        .def(
            "getPoints",
            [](const SkPath &self, int max)
            {
                if (max < 0)
                    max = self.countVerbs();
                std::vector<SkPoint> points(max);
                int length = self.getPoints(points.data(), max);
                if (length < max)
                    points.resize(length);
                return points;
            },
            R"doc(
                Returns a list of :py:class:`Point` representing the points in the :py:class:`Path`, up to a maximum of
                *max* points. If *max* is negative, return all points.
            )doc",
            "max"_a = -1)
        .def("countVerbs", &SkPath::countVerbs)
        .def(
            "getVerbs",
            [](const SkPath &path, int max)
            {
                if (max < 0)
                    max = path.countVerbs();
                std::vector<uint8_t> verbs(max);
                int length = path.getVerbs(verbs.data(), max);
                if (length < max)
                    verbs.resize(length);

                std::vector<SkPath::Verb> path_verbs(verbs.size());
                std::transform(verbs.begin(), verbs.end(), path_verbs.begin(),
                               [](const uint8_t &v) { return static_cast<SkPath::Verb>(v); });
                return path_verbs;
            },
            R"doc(
                Returns a list of :py:enum:`Path.Verb` representing the verbs in the :py:class:`Path`, up to a maximum
                of *max* verbs. If *max* is negative, return all verbs.
            )doc",
            "max"_a = -1)
        .def("approximateBytesUsed", &SkPath::approximateBytesUsed)
        .def("swap", &SkPath::swap, "other"_a)
        .def("getBounds", &SkPath::getBounds)
        .def("updateBoundsCache", &SkPath::updateBoundsCache)
        .def("computeTightBounds", &SkPath::computeTightBounds)
        .def("conservativelyContainsRect", &SkPath::conservativelyContainsRect, "rect"_a)
        .def("incReserve", &SkPath::incReserve, "extraPtCount"_a)
        .def("moveTo", py::overload_cast<SkScalar, SkScalar>(&SkPath::moveTo), "x"_a, "y"_a)
        .def("moveTo", py::overload_cast<const SkPoint &>(&SkPath::moveTo), "p"_a)
        .def("rMoveTo", &SkPath::rMoveTo, "dx"_a, "dy"_a)
        .def("lineTo", py::overload_cast<SkScalar, SkScalar>(&SkPath::lineTo), "x"_a, "y"_a)
        .def("lineTo", py::overload_cast<const SkPoint &>(&SkPath::lineTo), "p"_a)
        .def("rLineTo", &SkPath::rLineTo, "dx"_a, "dy"_a)
        .def("quadTo", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar>(&SkPath::quadTo), "x1"_a, "y1"_a,
             "x2"_a, "y2"_a)
        .def("quadTo", py::overload_cast<const SkPoint &, const SkPoint &>(&SkPath::quadTo), "p1"_a, "p2"_a)
        .def("rQuadTo", &SkPath::rQuadTo, "dx1"_a, "dy1"_a, "dx2"_a, "dy2"_a)
        .def("conicTo", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar, SkScalar>(&SkPath::conicTo), "x1"_a,
             "y1"_a, "x2"_a, "y2"_a, "w"_a)
        .def("conicTo", py::overload_cast<const SkPoint &, const SkPoint &, SkScalar>(&SkPath::conicTo), "p1"_a, "p2"_a,
             "w"_a)
        .def("rConicTo", &SkPath::rConicTo, "dx1"_a, "dy1"_a, "dx2"_a, "dy2"_a, "w"_a)
        .def("cubicTo", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar, SkScalar, SkScalar>(&SkPath::cubicTo),
             "x1"_a, "y1"_a, "x2"_a, "y2"_a, "x3"_a, "y3"_a)
        .def("cubicTo", py::overload_cast<const SkPoint &, const SkPoint &, const SkPoint &>(&SkPath::cubicTo), "p1"_a,
             "p2"_a, "p3"_a)
        .def("rCubicTo", &SkPath::rCubicTo, "dx1"_a, "dy1"_a, "dx2"_a, "dy2"_a, "dx3"_a, "dy3"_a)
        .def("arcTo", py::overload_cast<const SkRect &, SkScalar, SkScalar, bool>(&SkPath::arcTo), "oval"_a,
             "startAngle"_a, "sweepAngle"_a, "forceMoveTo"_a)
        .def("arcTo", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar, SkScalar>(&SkPath::arcTo), "x1"_a,
             "y1"_a, "x2"_a, "y2"_a, "radius"_a)
        .def("arcTo", py::overload_cast<const SkPoint, const SkPoint, SkScalar>(&SkPath::arcTo), "p1"_a, "p2"_a,
             "radius"_a);

    py::enum_<SkPath::ArcSize>(Path, "ArcSize")
        .value("kSmall_ArcSize", SkPath::ArcSize::kSmall_ArcSize)
        .value("kLarge_ArcSize", SkPath::ArcSize::kLarge_ArcSize);
    Path.def("arcTo",
             py::overload_cast<SkScalar, SkScalar, SkScalar, SkPath::ArcSize, SkPathDirection, SkScalar, SkScalar>(
                 &SkPath::arcTo),
             "rx"_a, "ry"_a, "xAxisRotate"_a, "largeArc"_a, "sweep"_a, "x"_a, "y"_a)
        .def(
            "arcTo",
            py::overload_cast<const SkPoint, SkScalar, SkPath::ArcSize, SkPathDirection, const SkPoint>(&SkPath::arcTo),
            "r"_a, "xAxisRotate"_a, "largeArc"_a, "sweep"_a, "xy"_a)
        .def("rArcTo", &SkPath::rArcTo, "rx"_a, "ry"_a, "xAxisRotate"_a, "largeArc"_a, "sweep"_a, "dx"_a, "dy"_a)
        .def("close", &SkPath::close)
        .def_static(
            "ConvertConicToQuads",
            [](const SkPoint &p0, const SkPoint &p1, const SkPoint &p2, SkScalar w, int pow2)
            {
                int size = 1 + 2 * (1 << pow2);
                std::vector<SkPoint> pts(size);
                int length = SkPath::ConvertConicToQuads(p0, p1, p2, w, pts.data(), pow2);
                if (length < size)
                    pts.resize(length);
                return pts;
            },
            R"doc(
                Approximates conic represented by start point *p0*, control point *p1*, end point *p2* and weight *w*,
                with quad array and returns it. Maximum possible return array size is given by: (1 + 2 * (1 << pow2)).
            )doc",
            "p0"_a, "p1"_a, "p2"_a, "w"_a, "pow2"_a)
        .def(
            "isRect",
            [](const SkPath &self) -> std::optional<py::tuple>
            {
                SkRect rect;
                bool isClosed;
                SkPathDirection direction;
                if (self.isRect(&rect, &isClosed, &direction))
                    return py::make_tuple(rect, isClosed, direction);
                return std::nullopt;
            },
            R"doc(
                Returns a tuple of (rect - storage for bounds of :py:class:`Rect`, isClosed - if :py:class:`Path` is
                closed, direction - :py:class:`Path` direcion) if :py:class`Path` is equivalent to :py:class:`Rect` when
                filled. Otherwise returns ``None``.

                :rtype: Tuple[:py:class:`Rect`, bool, :py:enum:`PathDirection`] | None
            )doc")
        .def("addRect", py::overload_cast<const SkRect &, SkPathDirection, unsigned>(&SkPath::addRect), "rect"_a,
             "dir"_a, "start"_a)
        .def("addRect", py::overload_cast<const SkRect &, SkPathDirection>(&SkPath::addRect), "rect"_a,
             "dir"_a = SkPathDirection::kCW)
        .def("addRect", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar, SkPathDirection>(&SkPath::addRect),
             "left"_a, "top"_a, "right"_a, "bottom"_a, "dir"_a = SkPathDirection::kCW)
        .def("addOval", py::overload_cast<const SkRect &, SkPathDirection>(&SkPath::addOval), "oval"_a,
             "dir"_a = SkPathDirection::kCW)
        .def("addOval", py::overload_cast<const SkRect &, SkPathDirection, unsigned>(&SkPath::addOval), "oval"_a,
             "dir"_a, "start"_a)
        .def("addCircle", &SkPath::addCircle, "x"_a, "y"_a, "radius"_a, "dir"_a = SkPathDirection::kCW)
        .def("addArc", &SkPath::addArc, "oval"_a, "startAngle"_a, "sweepAngle"_a)
        .def("addRoundRect",
             py::overload_cast<const SkRect &, SkScalar, SkScalar, SkPathDirection>(&SkPath::addRoundRect), "rect"_a,
             "rx"_a, "ry"_a, "dir"_a = SkPathDirection::kCW)
        .def(
            "addRoundRect",
            [](SkPath &path, const SkRect &rect, const std::vector<SkScalar> &radii, const SkPathDirection &dir)
            {
                if (radii.size() != 8)
                {
                    std::stringstream s;
                    s << "radii must have 8 elements (given " << radii.size() << " elements).";
                    throw py::value_error(s.str());
                }
                return path.addRoundRect(rect, radii.data(), dir);
            },
            "rect"_a, "radii"_a, "dir"_a = SkPathDirection::kCW)
        .def("addRRect", py::overload_cast<const SkRRect &, SkPathDirection>(&SkPath::addRRect), "rrect"_a,
             "dir"_a = SkPathDirection::kCW)
        .def("addRRect", py::overload_cast<const SkRRect &, SkPathDirection, unsigned>(&SkPath::addRRect), "rrect"_a,
             "dir"_a, "start"_a)
        .def(
            "addPoly",
            [](SkPath &path, const std::vector<SkPoint> &pts, bool close)
            { return path.addPoly(pts.data(), pts.size(), close); },
            "Adds contour created from *pts*.", "pts"_a, "close"_a);

    py::enum_<SkPath::AddPathMode>(Path, "AddPathMode")
        .value("kAppend_AddPathMode", SkPath::AddPathMode::kAppend_AddPathMode)
        .value("kExtend_AddPathMode", SkPath::AddPathMode::kExtend_AddPathMode);
    Path.def("addPath", py::overload_cast<const SkPath &, SkScalar, SkScalar, SkPath::AddPathMode>(&SkPath::addPath),
             "src"_a, "dx"_a, "dy"_a, "mode"_a = SkPath::kAppend_AddPathMode)
        .def("addPath", py::overload_cast<const SkPath &, SkPath::AddPathMode>(&SkPath::addPath), "src"_a,
             "mode"_a = SkPath::kAppend_AddPathMode)
        .def("addPath", py::overload_cast<const SkPath &, const SkMatrix &, SkPath::AddPathMode>(&SkPath::addPath),
             "src"_a, "matrix"_a, "mode"_a = SkPath::kAppend_AddPathMode)
        .def("reverseAddPath", &SkPath::reverseAddPath, "src"_a)
        .def(
            "makeOffset",
            [](const SkPath &self, const SkScalar &dx, const SkScalar &dy)
            {
                SkPath dst;
                self.offset(dx, dy, &dst);
                return dst;
            },
            "Offsets :py:class:`Point` array by (*dx*, *dy*) and returns the result as a new :py:class:`Path`.", "dx"_a,
            "dy"_a)
        .def("offset", py::overload_cast<SkScalar, SkScalar>(&SkPath::offset), "dx"_a, "dy"_a)
        .def("transform", py::overload_cast<const SkMatrix &, SkApplyPerspectiveClip>(&SkPath::transform), "matrix"_a,
             "pc"_a = SkApplyPerspectiveClip::kYes)
        .def("makeTransform", &SkPath::makeTransform, "m"_a, "pc"_a = SkApplyPerspectiveClip::kYes)
        .def("makeScale", &SkPath::makeScale, "sx"_a, "sy"_a)
        .def(
            "getLastPt",
            [](const SkPath &self) -> std::optional<SkPoint>
            {
                SkPoint lastPt;
                if (self.getLastPt(&lastPt))
                    return lastPt;
                return std::nullopt;
            },
            "Returns last point on :py:class:`Path`. Returns ``None`` if :py:class:`Point` array is empty.")
        .def("setLastPt", py::overload_cast<SkScalar, SkScalar>(&SkPath::setLastPt), "x"_a, "y"_a)
        .def("setLastPt", py::overload_cast<const SkPoint &>(&SkPath::setLastPt), "p"_a);

    py::enum_<SkPath::SegmentMask>(Path, "SegmentMask")
        .value("kLine_SegmentMask", SkPath::SegmentMask::kLine_SegmentMask)
        .value("kQuad_SegmentMask", SkPath::SegmentMask::kQuad_SegmentMask)
        .value("kConic_SegmentMask", SkPath::SegmentMask::kConic_SegmentMask)
        .value("kCubic_SegmentMask", SkPath::SegmentMask::kCubic_SegmentMask);
    Path.def("getSegmentMasks", &SkPath::getSegmentMasks);

    py::enum_<SkPath::Verb>(Path, "Verb")
        .value("kMove_Verb", SkPath::Verb::kMove_Verb)
        .value("kLine_Verb", SkPath::Verb::kLine_Verb)
        .value("kQuad_Verb", SkPath::Verb::kQuad_Verb)
        .value("kConic_Verb", SkPath::Verb::kConic_Verb)
        .value("kCubic_Verb", SkPath::Verb::kCubic_Verb)
        .value("kClose_Verb", SkPath::Verb::kClose_Verb)
        .value("kDone_Verb", SkPath::Verb::kDone_Verb);

    py::class_<SkPath::Iter>(Path, "Iter")
        .def(py::init())
        .def(py::init<const SkPath &, bool>(), "path"_a, "forceClose"_a, py::keep_alive<0, 1>())
        .def("setPath", &SkPath::Iter::setPath, "path"_a, "forceClose"_a, py::keep_alive<0, 1>())
        .def(
            "next",
            [](SkPath::Iter &it)
            {
                std::vector<SkPoint> pts(4);
                SkPath::Verb verb = it.next(pts.data());
                resizePoints(verb, pts);
                return py::make_tuple(verb, pts);
            },
            "Returns a tuple of (:py:class:`Path.Verb`, list of :py:class:`Point`) for the next segment in the path.")
        .def("conicWeight", &SkPath::Iter::conicWeight)
        .def("isCloseLine", &SkPath::Iter::isCloseLine)
        .def("isClosedContour", &SkPath::Iter::isClosedContour)
        .def(
            "__iter__", [](const SkPath::Iter &it) { return it; }, py::keep_alive<0, 1>())
        .def(
            "__next__",
            [](SkPath::Iter &it)
            {
                std::vector<SkPoint> pts(4);
                SkPath::Verb verb = it.next(pts.data());
                resizePoints(verb, pts);
                if (verb == SkPath::Verb::kDone_Verb)
                    throw py::stop_iteration();
                if (verb == SkPath::Verb::kConic_Verb)
                    return py::make_tuple(verb, pts, it.conicWeight());
                return py::make_tuple(verb, pts, py::none());
            },
            R"doc(
                Returns a tuple of (:py:class:`Path.Verb`, list of :py:class:`Point`, weight) for the next segment in
                the path. If the verb is not :py:attr:`Path.Verb.kConic_Verb`, the weight is ``None``.
            )doc");

    Path.def("contains", &SkPath::contains, "x"_a, "y"_a)
        .def("dump",
             [](const SkPath &path)
             {
                 py::scoped_ostream_redirect stream;
                 path.dump();
             })
        .def("dumpHex",
             [](const SkPath &path)
             {
                 py::scoped_ostream_redirect stream;
                 path.dumpHex();
             })
        .def("serialize", &SkPath::serialize)
        .def("getGenerationID", &SkPath::getGenerationID)
        .def("isValid", &SkPath::isValid)
        .def(
            "__iter__", [](const SkPath &path) { return SkPath::Iter(path, false); }, py::keep_alive<0, 1>())
        .def("__len__", &SkPath::countVerbs)
        .def("__str__",
             [](const SkPath &path)
             {
                 std::stringstream s;
                 s << "Path(" << path.countVerbs() << " segments)";
                 return s.str();
             });

    py::class_<SkPathBuilder> PathBuilder(m, "PathBuilder");
    PathBuilder.def(py::init<>())
        .def(py::init<SkPathFillType>(), "ft"_a)
        .def(py::init<const SkPath &>(), "src"_a, py::keep_alive<0, 1>())
        .def(py::init<const SkPathBuilder &>(), "pathBuilder"_a)
        .def("fillType", &SkPathBuilder::fillType)
        .def("computeBounds", &SkPathBuilder::computeBounds)
        .def("snapshot", &SkPathBuilder::snapshot)
        .def("detach", &SkPathBuilder::detach)
        .def("setFillType", &SkPathBuilder::setFillType, "ft"_a)
        .def("setIsVolatile", &SkPathBuilder::setIsVolatile, "isVolatile"_a)
        .def("reset", &SkPathBuilder::reset)
        .def("moveTo", py::overload_cast<SkPoint>(&SkPathBuilder::moveTo), "pt"_a)
        .def("moveTo", py::overload_cast<SkScalar, SkScalar>(&SkPathBuilder::moveTo), "x"_a, "y"_a)
        .def("lineTo", py::overload_cast<SkPoint>(&SkPathBuilder::lineTo), "pt"_a)
        .def("lineTo", py::overload_cast<SkScalar, SkScalar>(&SkPathBuilder::lineTo), "x"_a, "y"_a)
        .def("quadTo", py::overload_cast<SkPoint, SkPoint>(&SkPathBuilder::quadTo), "pt1"_a, "pt2"_a)
        .def("quadTo", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar>(&SkPathBuilder::quadTo), "x1"_a,
             "y1"_a, "x2"_a, "y2"_a)
        .def(
            "quadTo",
            [](SkPathBuilder &self, const std::vector<SkPoint> &pts)
            {
                if (pts.size() < 2)
                    throw py::value_error("pts must have 2 elements.");
                return self.quadTo(pts.data());
            },
            "pts"_a)
        .def("conicTo", py::overload_cast<SkPoint, SkPoint, SkScalar>(&SkPathBuilder::conicTo), "pt1"_a, "pt2"_a, "w"_a)
        .def("conicTo", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar, SkScalar>(&SkPathBuilder::conicTo),
             "x1"_a, "y1"_a, "x2"_a, "y2"_a, "w"_a)
        .def(
            "conicTo",
            [](SkPathBuilder &self, const std::vector<SkPoint> &pts, const SkScalar &w)
            {
                if (pts.size() < 2)
                    throw py::value_error("pts must have 2 elements.");
                return self.conicTo(pts.data(), w);
            },
            "pts"_a, "w"_a)
        .def("cubicTo", py::overload_cast<SkPoint, SkPoint, SkPoint>(&SkPathBuilder::cubicTo), "pt1"_a, "pt2"_a,
             "pt3"_a)
        .def("cubicTo",
             py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar, SkScalar, SkScalar>(&SkPathBuilder::cubicTo),
             "x1"_a, "y1"_a, "x2"_a, "y2"_a, "x3"_a, "y3"_a)
        .def(
            "cubicTo",
            [](SkPathBuilder &self, const std::vector<SkPoint> &pts)
            {
                if (pts.size() < 3)
                    throw py::value_error("pts must have 3 elements.");
                return self.cubicTo(pts.data());
            },
            "pts"_a)
        .def("close", &SkPathBuilder::close)
        .def(
            "polylineTo",
            [](SkPathBuilder &self, const std::vector<SkPoint> &pts)
            { return self.polylineTo(pts.data(), pts.size()); },
            "Append a series of line segments to the path between adjacent points in the list.", "pts"_a)
        .def("rLineTo", py::overload_cast<SkPoint>(&SkPathBuilder::rLineTo), "pt"_a)
        .def("rLineTo", py::overload_cast<SkScalar, SkScalar>(&SkPathBuilder::rLineTo), "x"_a, "y"_a)
        .def("rQuadTo", py::overload_cast<SkPoint, SkPoint>(&SkPathBuilder::rQuadTo), "pt1"_a, "pt2"_a)
        .def("rQuadTo", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar>(&SkPathBuilder::rQuadTo), "x1"_a,
             "y1"_a, "x2"_a, "y2"_a)
        .def("rConicTo", py::overload_cast<SkPoint, SkPoint, SkScalar>(&SkPathBuilder::rConicTo), "pt1"_a, "pt2"_a,
             "w"_a)
        .def("rConicTo", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar, SkScalar>(&SkPathBuilder::rConicTo),
             "x1"_a, "y1"_a, "x2"_a, "y2"_a, "w"_a)
        .def("rCubicTo", py::overload_cast<SkPoint, SkPoint, SkPoint>(&SkPathBuilder::rCubicTo), "pt1"_a, "pt2"_a,
             "pt3"_a)
        .def("rCubicTo",
             py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar, SkScalar, SkScalar>(&SkPathBuilder::rCubicTo),
             "x1"_a, "y1"_a, "x2"_a, "y2"_a, "x3"_a, "y3"_a)
        .def("arcTo", py::overload_cast<const SkRect &, SkScalar, SkScalar, bool>(&SkPathBuilder::arcTo), "oval"_a,
             "startAngleDeg"_a, "sweepAngleDeg"_a, "forceMoveTo"_a)
        .def("arcTo", py::overload_cast<SkPoint, SkPoint, SkScalar>(&SkPathBuilder::arcTo), "p1"_a, "p2"_a, "radius"_a);

    py::enum_<SkPathBuilder::ArcSize>(PathBuilder, "ArcSize")
        .value("kSmall_ArcSize", SkPathBuilder::kSmall_ArcSize)
        .value("kLarge_ArcSize", SkPathBuilder::kLarge_ArcSize);
    PathBuilder
        .def("arcTo",
             py::overload_cast<SkPoint, SkScalar, SkPathBuilder::ArcSize, SkPathDirection, SkPoint>(
                 &SkPathBuilder::arcTo),
             "r"_a, "xAxisRotate"_a, "largeArc"_a, "sweep"_a, "xy"_a)
        .def("addArc", &SkPathBuilder::addArc, "oval"_a, "startAngleDeg"_a, "sweepAngleDeg"_a)
        .def("addRect", py::overload_cast<const SkRect &, SkPathDirection, unsigned>(&SkPathBuilder::addRect), "rect"_a,
             "dir"_a, "index"_a)
        .def("addOval", py::overload_cast<const SkRect &, SkPathDirection, unsigned>(&SkPathBuilder::addOval), "oval"_a,
             "dir"_a, "index"_a)
        .def("addRRect", py::overload_cast<const SkRRect &, SkPathDirection, unsigned>(&SkPathBuilder::addRRect),
             "rrect"_a, "dir"_a, "index"_a)
        .def("addRect", py::overload_cast<const SkRect &, SkPathDirection>(&SkPathBuilder::addRect), "rect"_a,
             "dir"_a = SkPathDirection::kCW)
        .def("addOval", py::overload_cast<const SkRect &, SkPathDirection>(&SkPathBuilder::addOval), "rect"_a,
             "dir"_a = SkPathDirection::kCW)
        .def("addRRect", py::overload_cast<const SkRRect &, SkPathDirection>(&SkPathBuilder::addRRect), "rrect"_a,
             "dir"_a = SkPathDirection::kCW)
        .def("addCircle", &SkPathBuilder::addCircle, "center_x"_a, "center_y"_a, "radius"_a,
             "dir"_a = SkPathDirection::kCW)
        .def(
            "addPolygon",
            [](SkPathBuilder &self, const std::vector<SkPoint> &pts, const bool &isClosed)
            { return self.addPolygon(pts.data(), pts.size(), isClosed); },
            "pts"_a, "isClosed"_a)
        .def("addPath", &SkPathBuilder::addPath, "src"_a)
        .def("incReserve", py::overload_cast<int, int>(&SkPathBuilder::incReserve), "extraPtCount"_a,
             "extraVerbCount"_a)
        .def("incReserve", py::overload_cast<int>(&SkPathBuilder::incReserve), "extraPtCount"_a)
        .def("offset", &SkPathBuilder::offset, "dx"_a, "dy"_a)
        .def("toggleInverseFillType", &SkPathBuilder::toggleInverseFillType);

    py::enum_<SkPathOp>(m, "PathOp")
        .value("kDifference_PathOp", SkPathOp::kDifference_SkPathOp)
        .value("kIntersect_PathOp", SkPathOp::kIntersect_SkPathOp)
        .value("kUnion_PathOp", SkPathOp::kUnion_SkPathOp)
        .value("kXOR_PathOp", SkPathOp::kXOR_SkPathOp)
        .value("kReverseDifference_PathOp", SkPathOp::kReverseDifference_SkPathOp);

    Path.def(
            "op",
            [](const SkPath &one, const SkPath &two, SkPathOp op)
            {
                SkPath result;
                if (Op(one, two, op, &result))
                    return result;
                throw std::runtime_error("Failed to apply op");
            },
            R"doc(
                Return the resultant path of applying the *op *to this path and the specified path. If the operation
                fails, throws a runtime error.
            )doc",
            "two"_a, "op"_a)
        .def(
            "simplify",
            [](const SkPath &path)
            {
                SkPath result;
                if (Simplify(path, &result))
                    return result;
                throw std::runtime_error("Failed to simplify path");
            },
            R"doc(
                Return the path as a set of non-overlapping contours that describe the same area as the original path.
                If the simplify fails, throws a runtime error.
            )doc")
        .def(
            "tightBounds",
            [](const SkPath &path)
            {
                SkRect result;
                if (TightBounds(path, &result))
                    return result;
                throw std::runtime_error("Failed to compute tight bounds");
            },
            "Return the resulting rectangle to the tight bounds of the path.")
        .def(
            "asWinding",
            [](const SkPath &path)
            {
                SkPath result;
                if (AsWinding(path, &result))
                    return result;
                throw std::runtime_error("Failed to convert to winding");
            },
            R"doc(
                Return the result with fill type winding to area equivalent to path. If the conversion fails, throws
                a runtime error.
            )doc");

    py::class_<SkOpBuilder>(m, "OpBuilder")
        .def(py::init<>())
        .def("add", &SkOpBuilder::add, "path"_a, "op"_a)
        .def(
            "resolve",
            [](SkOpBuilder &builder)
            {
                SkPath result;
                if (builder.resolve(&result))
                    return result;
                throw std::runtime_error("Failed to resolve");
            },
            R"doc(
                Computes the sum of all paths and operands and returns it, and resets the builder to its initial state.
                If the operation fails, throws a runtime error.
            )doc");
}