#include "common.h"
#include "include/core/SkData.h"
#include "include/core/SkMatrix.h"
#include "include/core/SkRRect.h"
#include "include/core/SkRect.h"
#include <pybind11/iostream.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>

void initRect(py::module &m)
{
    py::class_<SkIRect>(m, "IRect")
        .def(py::init(
                 [](const py::tuple &t)
                 {
                     if (t.size() == 0)
                         return SkIRect::MakeEmpty();
                     else if (t.size() == 2)
                         return SkIRect::MakeWH(t[0].cast<int32_t>(), t[1].cast<int32_t>());
                     else if (t.size() == 4)
                         return SkIRect::MakeLTRB(t[0].cast<int32_t>(), t[1].cast<int32_t>(), t[2].cast<int32_t>(),
                                                  t[3].cast<int32_t>());
                     else
                         throw py::value_error("Invalid tuple.");
                 }),
             "Create an :py:class:`IRect` from a tuple of 0, 2, or 4 integers.", "t"_a)
        .def_readwrite("fLeft", &SkIRect::fLeft)
        .def_readwrite("fTop", &SkIRect::fTop)
        .def_readwrite("fRight", &SkIRect::fRight)
        .def_readwrite("fBottom", &SkIRect::fBottom)
        .def_static("MakeEmpty", &SkIRect::MakeEmpty)
        .def(py::init(&SkIRect::MakeEmpty),
             R"doc(
                 Constructs an :py:class:`IRect` set to (0, 0, 0, 0). Many other rectangles are empty; if left is equal
                 to or greater than right, or if top is equal to or greater than bottom. Setting all members to zero is
                 a convenience, but does not designate a special empty rectangle.
            )doc")
        .def_static("MakeWH", &SkIRect::MakeWH, "w"_a, "h"_a)
        .def(py::init(&SkIRect::MakeWH),
             R"doc(
                Constructs an :py:class:`IRect` set to (0, 0, w, h). Does not validate input; w or h may be negative.

                :param int w: width of constructed :py:class:`IRect`
                :param int h: height of constructed :py:class:`IRect`
            )doc",
             "w"_a, "h"_a)
        .def_static("MakeSize", &SkIRect::MakeSize, "size"_a)
        .def(py::init(&SkIRect::MakeSize),
             R"doc(
                Constructs an :py:class:`IRect` set to (0, 0, size.width(), size.height()). Does not validate input;
                size.width() or size.height() may be negative.

                :param ISize size: values for :py:class:`IRect` width and height
            )doc",
             "size"_a)
        .def_static("MakePtSize", &SkIRect::MakePtSize, "pt"_a, "size"_a)
        .def(py::init(&SkIRect::MakePtSize),
             R"doc(
                Constructs an :py:class:`IRect` set to (pt.x(), pt.y(), pt.x() + size.width(), pt.y() + size.height()).
                Does not validate input; size.width() or size.height() may be negative.

                :param IPoint pt: values for :py:class:`IRect` fLeft and fTop
                :param ISize size: values for :py:class:`IRect` width and height
            )doc",
             "pt"_a, "size"_a)
        .def_static("MakeLTRB", &SkIRect::MakeLTRB, "l"_a, "t"_a, "r"_a, "b"_a)
        .def(py::init(&SkIRect::MakeLTRB),
             R"doc(
                Constructs an :py:class:`IRect` set to (l, t, r, b). Does not sort input; :py:class:`IRect` may result
                in fLeft greater than fRight, or fTop greater than fBottom.

                :param int l: value for :py:class:`IRect` fLeft
                :param int t: value for :py:class:`IRect` fTop
                :param int r: value for :py:class:`IRect` fRight
                :param int b: value for :py:class:`IRect` fBottom
            )doc",
             "l"_a, "t"_a, "r"_a, "b"_a)
        .def_static("MakeXYWH", &SkIRect::MakeXYWH, "x"_a, "y"_a, "w"_a, "h"_a)
        .def("left", &SkIRect::left)
        .def("top", &SkIRect::top)
        .def("right", &SkIRect::right)
        .def("bottom", &SkIRect::bottom)
        .def("x", &SkIRect::x)
        .def("y", &SkIRect::y)
        .def("topLeft", &SkIRect::topLeft)
        .def("width", &SkIRect::width)
        .def("height", &SkIRect::height)
        .def("size", &SkIRect::size)
        .def("width64", &SkIRect::width64)
        .def("height64", &SkIRect::height64)
        .def("isEmpty64", &SkIRect::isEmpty64)
        .def("isEmpty", &SkIRect::isEmpty)
        .def(py::self == py::self, "other"_a)
        .def(py::self != py::self, "other"_a)
        .def("setEmpty", &SkIRect::setEmpty)
        .def("setLTRB", &SkIRect::setLTRB, "left"_a, "top"_a, "right"_a, "bottom"_a)
        .def("setXYWH", &SkIRect::setXYWH, "x"_a, "y"_a, "width"_a, "height"_a)
        .def("setWH", &SkIRect::setWH, "width"_a, "height"_a)
        .def("setSize", &SkIRect::setSize, "size"_a)
        .def("makeOffset", py::overload_cast<int32_t, int32_t>(&SkIRect::makeOffset, py::const_), "dx"_a, "dy"_a)
        .def("makeOffset", py::overload_cast<SkIVector>(&SkIRect::makeOffset, py::const_), "offset"_a)
        .def("makeInset", &SkIRect::makeInset, "dx"_a, "dy"_a)
        .def("makeOutset", &SkIRect::makeOutset, "dx"_a, "dy"_a)
        .def("offset", py::overload_cast<int32_t, int32_t>(&SkIRect::offset), "dx"_a, "dy"_a)
        .def("offset", py::overload_cast<const SkIPoint &>(&SkIRect::offset), "delta"_a)
        .def("offsetTo", &SkIRect::offsetTo, "newX"_a, "newY"_a)
        .def("inset", &SkIRect::inset, "dx"_a, "dy"_a)
        .def("outset", &SkIRect::outset, "dx"_a, "dy"_a)
        .def("adjust", &SkIRect::adjust, "dL"_a, "dT"_a, "dR"_a, "dB"_a)
        .def("contains", py::overload_cast<int32_t, int32_t>(&SkIRect::contains, py::const_), "x"_a, "y"_a)
        .def(
            "__contains__", [](const SkIRect &r, const SkIPoint &p) { return r.contains(p.fX, p.fY); },
            py::is_operator(),
            R"doc(
                Returns true if the point is contained within the :py:class:`IRect`.

                :param IPoint point: point to test
                :return: true if the point is contained within the :py:class:`IRect`
            )doc")
        .def("contains", py::overload_cast<const SkIRect &>(&SkIRect::contains, py::const_), "r"_a)
        .def("__contains__", py::overload_cast<const SkIRect &>(&SkIRect::contains, py::const_), py::is_operator())
        .def("contains", py::overload_cast<const SkRect &>(&SkIRect::contains, py::const_), "r"_a)
        .def("__contains__", py::overload_cast<const SkRect &>(&SkIRect::contains, py::const_), py::is_operator())
        .def("containsNoEmptyCheck", &SkIRect::containsNoEmptyCheck, "r"_a)
        .def("intersect", py::overload_cast<const SkIRect &>(&SkIRect::intersect), "r"_a)
        .def("intersect", py::overload_cast<const SkIRect &, const SkIRect &>(&SkIRect::intersect), "a"_a, "b"_a)
        .def_static("Intersects", &SkIRect::Intersects, "a"_a, "b"_a)
        .def("join", &SkIRect::join, "r"_a)
        .def("sort", &SkIRect::sort)
        .def("makeSorted", &SkIRect::makeSorted)
        .def(
            "__iter__", [](const SkIRect &r) { return py::make_iterator(&r.fLeft, &r.fLeft + 4); },
            py::keep_alive<0, 1>())
        .def("__len__", [](const SkIRect &) { return 4; })
        .def("__str__",
             [](const SkIRect &r)
             {
                 std::stringstream s;
                 s << "IRect(" << r.fLeft << ", " << r.fTop << ", " << r.fRight << ", " << r.fBottom << ")";
                 return s.str();
             });

    py::implicitly_convertible<py::tuple, SkIRect>();

    py::class_<SkRect>(m, "Rect")
        .def(py::init(
                 [](const py::tuple &t)
                 {
                     if (t.size() == 0)
                         return SkRect::MakeEmpty();
                     else if (t.size() == 2)
                         return SkRect::MakeWH(t[0].cast<float>(), t[1].cast<float>());
                     else if (t.size() == 4)
                         return SkRect::MakeLTRB(t[0].cast<float>(), t[1].cast<float>(), t[2].cast<float>(),
                                                 t[3].cast<float>());
                     else
                         throw py::value_error("Invalid tuple.");
                 }),
             "Create an :py:class:`Rect` from a tuple of 0, 2, or 4 floats.", "t"_a)
        .def_readwrite("fLeft", &SkRect::fLeft)
        .def_readwrite("fTop", &SkRect::fTop)
        .def_readwrite("fRight", &SkRect::fRight)
        .def_readwrite("fBottom", &SkRect::fBottom)
        .def_static("MakeEmpty", &SkRect::MakeEmpty)
        .def(py::init(&SkRect::MakeEmpty),
             R"doc(
                 Constructs a :py:class:`Rect` set to (0, 0, 0, 0). Many other rectangles are empty; if left is equal to
                 or greater than right, or if top is equal to or greater than bottom. Setting all members to zero is a
                 convenience, but does not designate a special empty rectangle.
            )doc")
        .def_static("MakeWH", &SkRect::MakeWH, "w"_a, "h"_a)
        .def(py::init(&SkRect::MakeWH),
             R"doc(
                Constructs a :py:class:`Rect` set to (0, 0, w, h). Does not validate input; w or h may be negative.

                :param float w: width of constructed :py:class:`Rect`
                :param float h: height of constructed :py:class:`Rect`
            )doc",
             "w"_a, "h"_a)
        .def_static("MakeIWH", &SkRect::MakeIWH, "w"_a, "h"_a)
        .def_static("MakeSize", &SkRect::MakeSize, "size"_a)
        .def(py::init(&SkRect::MakeSize),
             R"doc(
                Constructs a :py:class:`Rect` set to (0, 0, size.width(), size.height()). Does not validate input;
                size.width() or size.height() may be negative.

                :param Size size: values for :py:class:`Rect` width and height
            )doc",
             "size"_a)
        .def_static("MakeLTRB", &SkRect::MakeLTRB, "l"_a, "t"_a, "r"_a, "b"_a)
        .def(py::init(&SkRect::MakeLTRB),
             R"doc(
                Constructs a :py:class:`Rect` set to (l, t, r, b). Does not sort input; :py:class:`Rect` may result in
                fLeft greater than fRight, or fTop greater than fBottom.

                :param float l: stored in fLeft
                :param float t: stored in fTop
                :param float r: stored in fRight
                :param float b: stored in fBottom
            )doc",
             "l"_a, "t"_a, "r"_a, "b"_a)
        .def_static("MakeXYWH", &SkRect::MakeXYWH, "x"_a, "y"_a, "w"_a, "h"_a)
        .def_static("Make", py::overload_cast<const SkISize &>(&SkRect::Make), "size"_a)
        .def(py::init(py::overload_cast<const SkISize &>(&SkRect::Make)),
             R"doc(
                Constructs a :py:class:`Rect` set to (0, 0, size.width(), size.height()). Does not validate input;
                size.width() or size.height() may be negative.

                :param ISize size: values for :py:class:`Rect` width and height
            )doc",
             "size"_a)
        .def_static("Make", py::overload_cast<const SkIRect &>(&SkRect::Make), "irect"_a)
        .def(py::init(py::overload_cast<const SkIRect &>(&SkRect::Make)),
             R"doc(
                Constructs a :py:class:`Rect` set to iRect, promoting integer to floats. Does not validate input; fLeft
                may be greater than fRight, fTop may be greater than fBottom.
            )doc",
             "irect"_a)
        .def("isEmpty", &SkRect::isEmpty)
        .def("isSorted", &SkRect::isSorted)
        .def("isFinite", &SkRect::isFinite)
        .def("x", &SkRect::x)
        .def("y", &SkRect::y)
        .def("left", &SkRect::left)
        .def("top", &SkRect::top)
        .def("right", &SkRect::right)
        .def("bottom", &SkRect::bottom)
        .def("width", &SkRect::width)
        .def("height", &SkRect::height)
        .def("centerX", &SkRect::centerX)
        .def("centerY", &SkRect::centerY)
        .def("center", &SkRect::center)
        .def(py::self == py::self, "other"_a)
        .def(py::self != py::self, "other"_a)
        .def(
            "toQuad",
            [](const SkRect &rect)
            {
                std::vector<SkPoint> quad(4);
                rect.toQuad(quad.data());
                return quad;
            },
            R"doc(
                Returns four points in quad that enclose :py:class:`Rect` ordered as: top-left, top-right, bottom-right,
                bottom-left.

                :return: list of four :py:class:`Point` objects
            )doc")
        .def("setEmpty", &SkRect::setEmpty)
        .def("set", py::overload_cast<const SkIRect &>(&SkRect::set), "src"_a)
        .def("setLTRB", &SkRect::setLTRB, "left"_a, "top"_a, "right"_a, "bottom"_a)
        .def(
            "setBounds",
            [](SkRect &rect, const std::vector<SkPoint> &points) { rect.setBounds(points.data(), points.size()); },
            R"doc(
                Sets to bounds of :py:class:`Point` list. If list is empty, or contains an infinity or NaN, sets to
                (0, 0, 0, 0). Result is either empty or sorted: fLeft is less than or equal to fRight, and fTop is less
                than or equal to fBottom.

                :param Point[] points: :py:class:`Point` array
            )doc",
            "points"_a)
        .def(
            "setBoundsCheck",
            [](SkRect &rect, const std::vector<SkPoint> &points)
            { return rect.setBoundsCheck(points.data(), points.size()); },
            R"doc(
                Same as :py:meth:`setBounds` but returns ``False`` if list is empty or contains an infinity or NaN.
            )doc",
            "points"_a)
        .def(
            "setBoundsNoCheck",
            [](SkRect &rect, const std::vector<SkPoint> &points)
            { rect.setBoundsNoCheck(points.data(), points.size()); },
            R"doc(
                Sets to bounds of :py:class:`Point` list. If any point is infinity or NaN, all :py:class:`Rect`
                dimensions are set to NaN.
            )doc",
            "points"_a)
        .def("set", py::overload_cast<const SkPoint &, const SkPoint &>(&SkRect::set), "p0"_a, "p1"_a)
        .def("setXYWH", &SkRect::setXYWH, "x"_a, "y"_a, "width"_a, "height"_a)
        .def("setWH", &SkRect::setWH, "width"_a, "height"_a)
        .def("setIWH", &SkRect::setIWH, "width"_a, "height"_a)
        .def("makeOffset", py::overload_cast<float, float>(&SkRect::makeOffset, py::const_), "dx"_a, "dy"_a)
        .def("makeOffset", py::overload_cast<SkVector>(&SkRect::makeOffset, py::const_), "v"_a)
        .def("makeInset", &SkRect::makeInset, "dx"_a, "dy"_a)
        .def("makeOutset", &SkRect::makeOutset, "dx"_a, "dy"_a)
        .def("offset", py::overload_cast<float, float>(&SkRect::offset), "dx"_a, "dy"_a)
        .def("offset", py::overload_cast<const SkPoint &>(&SkRect::offset), "delta"_a)
        .def("offsetTo", &SkRect::offsetTo, "newX"_a, "newY"_a)
        .def("inset", &SkRect::inset, "dx"_a, "dy"_a)
        .def("outset", &SkRect::outset, "dx"_a, "dy"_a)
        .def("intersect", py::overload_cast<const SkRect &>(&SkRect::intersect), "r"_a)
        .def("intersect", py::overload_cast<const SkRect &, const SkRect &>(&SkRect::intersect), "a"_a, "b"_a)
        .def("intersects", &SkRect::intersects, "r"_a)
        .def_static("Intersects", py::overload_cast<const SkRect &, const SkRect &>(&SkRect::Intersects), "a"_a, "b"_a)
        .def("join", &SkRect::join, "r"_a)
        .def("joinNonEmptyArg", &SkRect::joinNonEmptyArg, "r"_a)
        .def("joinPossiblyEmptyRect", &SkRect::joinPossiblyEmptyRect, "r"_a)
        .def("contains", py::overload_cast<float, float>(&SkRect::contains, py::const_), "x"_a, "y"_a)
        .def(
            "__contains__", [](const SkRect &r, const SkPoint &p) { return r.contains(p.fX, p.fY); }, py::is_operator(),
            "Returns ``True`` if :py:class:`Point` is inside :py:class:`Rect`.")
        .def("contains", py::overload_cast<const SkRect &>(&SkRect::contains, py::const_), "r"_a)
        .def("__contains__", py::overload_cast<const SkRect &>(&SkRect::contains, py::const_), py::is_operator())
        .def("contains", py::overload_cast<const SkIRect &>(&SkRect::contains, py::const_), "r"_a)
        .def("__contains__", py::overload_cast<const SkIRect &>(&SkRect::contains, py::const_), py::is_operator())
        .def("round", py::overload_cast<>(&SkRect::round, py::const_))
        .def("roundOut", py::overload_cast<>(&SkRect::roundOut, py::const_))
        .def("roundIn", py::overload_cast<>(&SkRect::roundIn, py::const_))
        .def("sort", &SkRect::sort)
        .def("makeSorted", &SkRect::makeSorted)
        .def(
            "asScalars",
            [](const SkRect &r)
            {
                return py::memoryview::from_buffer(r.asScalars(), sizeof(float), py::format_descriptor<float>::value,
                                                   {4}, {sizeof(float)});
            },
            "Returns a :py:class:`memoryview` of :py:class:`Scalar` containing the :py:class:`Rect`'s coordinates.")
        .def(
            "dump",
            [](const SkRect &rect, bool asHex)
            {
                py::scoped_ostream_redirect stream;
                rect.dump(asHex);
            },
            "asHex"_a = false)
        .def("dumpHex",
             [](const SkRect &rect)
             {
                 py::scoped_ostream_redirect stream;
                 rect.dumpHex();
             })
        .def(
            "__iter__", [](const SkRect &r) { return py::make_iterator(&r.fLeft, &r.fLeft + 4); },
            py::keep_alive<0, 1>())
        .def("__len__", [](const SkRect &) { return 4; })
        .def("__str__",
             [](const SkRect &r)
             {
                 std::stringstream s;
                 s << "Rect(" << r.fLeft << ", " << r.fTop << ", " << r.fRight << ", " << r.fBottom << ")";
                 return s.str();
             });

    py::implicitly_convertible<py::tuple, SkRect>();
    py::implicitly_convertible<SkIRect, SkRect>();

    py::class_<SkRRect> RRect(m, "RRect");
    RRect.def(py::init()).def(py::init<const SkRRect &>(), "rrect"_a);

    py::enum_<SkRRect::Type>(RRect, "Type")
        .value("kEmpty_Type", SkRRect::Type::kEmpty_Type)
        .value("kRect_Type", SkRRect::Type::kRect_Type)
        .value("kOval_Type", SkRRect::Type::kOval_Type)
        .value("kSimple_Type", SkRRect::Type::kSimple_Type)
        .value("kNinePatch_Type", SkRRect::Type::kNinePatch_Type)
        .value("kComplex_Type", SkRRect::Type::kComplex_Type)
        .value("kLastType", SkRRect::Type::kLastType);
    RRect.def("getType", &SkRRect::getType)
        .def("type", &SkRRect::type)
        .def("isEmpty", &SkRRect::isEmpty)
        .def("isRect", &SkRRect::isRect)
        .def("isOval", &SkRRect::isOval)
        .def("isSimple", &SkRRect::isSimple)
        .def("isNinePatch", &SkRRect::isNinePatch)
        .def("isComplex", &SkRRect::isComplex)
        .def("width", &SkRRect::width)
        .def("height", &SkRRect::height)
        .def("getSimpleRadii", &SkRRect::getSimpleRadii)
        .def("setEmpty", &SkRRect::setEmpty)
        .def("setRect", &SkRRect::setRect, "rect"_a)
        .def_static("MakeEmpty", &SkRRect::MakeEmpty)
        .def_static("MakeRect", &SkRRect::MakeRect, "rect"_a)
        .def_static("MakeOval", &SkRRect::MakeOval, "oval"_a)
        .def_static("MakeRectXY", &SkRRect::MakeRectXY, "rect"_a, "xRad"_a, "yRad"_a)
        .def(py::init(&SkRRect::MakeRectXY), "rect"_a, "xRad"_a, "yRad"_a)
        .def("setOval", &SkRRect::setOval, "oval"_a)
        .def("setRectXY", &SkRRect::setRectXY, "rect"_a, "xRad"_a, "yRad"_a)
        .def("setNinePatch", &SkRRect::setNinePatch, "rect"_a, "leftRad"_a, "topRad"_a, "rightRad"_a, "bottomRad"_a)
        .def(
            "setRectRadii",
            [](SkRRect &rrect, const SkRect &rect, const std::vector<SkVector> &radii)
            {
                if (radii.size() != 4)
                    throw py::value_error("radii must be a list of 4 vectors.");
                rrect.setRectRadii(rect, radii.data());
            },
            "rect"_a, "radii"_a);

    py::enum_<SkRRect::Corner>(RRect, "Corner")
        .value("kUpperLeft_Corner", SkRRect::Corner::kUpperLeft_Corner)
        .value("kUpperRight_Corner", SkRRect::Corner::kUpperRight_Corner)
        .value("kLowerRight_Corner", SkRRect::Corner::kLowerRight_Corner)
        .value("kLowerLeft_Corner", SkRRect::Corner::kLowerLeft_Corner);
    RRect.def("rect", &SkRRect::rect)
        .def("radii", &SkRRect::radii, "corner"_a)
        .def("getBounds", &SkRRect::getBounds)
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def(
            "makeInset",
            [](const SkRRect &rrect, const SkScalar &dx, const SkScalar &dy)
            {
                SkRRect dst;
                rrect.inset(dx, dy, &dst);
                return dst;
            },
            R"doc(
                Copies :py:class:`RRect`, then insets bounds by *dx* and *dy*, and adjusts radii by *dx* and *dy*.

                :param dx: added to rect().fLeft, and subtracted from rect().fRight
                :param dy: added to rect().fTop, and subtracted from rect().fBottom
                :return: insets bounds and radii
            )doc",
            "dx"_a, "dy"_a)
        .def("inset", py::overload_cast<SkScalar, SkScalar>(&SkRRect::inset), "dx"_a, "dy"_a)
        .def(
            "makeOutset",
            [](const SkRRect &rrect, const SkScalar &dx, const SkScalar &dy)
            {
                SkRRect dst;
                rrect.outset(dx, dy, &dst);
                return dst;
            },
            R"doc(
                Outsets bounds by *dx* and *dy*, and adjusts radii by *dx* and *dy*.

                :param dx: subtracted from rect().fLeft, and added to rect().fRight
                :param dy: subtracted from rect().fTop, and added to rect().fBottom
                :return: outset bounds and radii
            )doc",
            "dx"_a, "dy"_a)
        .def("outset", py::overload_cast<SkScalar, SkScalar>(&SkRRect::outset), "dx"_a, "dy"_a)
        .def("offset", &SkRRect::offset, "dx"_a, "dy"_a)
        .def("makeOffset", &SkRRect::makeOffset, "dx"_a, "dy"_a)
        .def("contains", &SkRRect::contains, "rect"_a)
        .def("__contains__", &SkRRect::contains, py::is_operator(), "Same as :py:meth:`RRect.contains`.", "rect"_a)
        .def("isValid", &SkRRect::isValid)
        .def_readonly_static("kSizeInMemory", &SkRRect::kSizeInMemory)
        .def(
            "writeToMemory",
            [](const SkRRect &self)
            {
                sk_sp<SkData> data = SkData::MakeUninitialized(SkRRect::kSizeInMemory);
                self.writeToMemory(data->writable_data());
                return data;
            },
            "Writes :py:class:`RRect` to :py:class:`Data` and returns it.")
        .def(
            "readFromMemory",
            [](SkRRect &self, const SkData &data) { return self.readFromMemory(data.data(), data.size()); },
            "Reads :py:class:`RRect` from given :py:class:`Data`.", "buffer"_a)
        .def(
            "transform",
            [](const SkRRect &self, const SkMatrix &matrix) -> std::optional<SkRRect>
            {
                SkRRect dst;
                if (self.transform(matrix, &dst))
                    return dst;
                return std::nullopt;
            },
            R"doc(
                Transforms the :py:class:`RRect` by matrix, returning result. Returns the transformed :py:class:`RRect`
                if the transformation can be represented by another :py:class:`RRect`. Returns ``None`` if matrix
                contains transformations that are not axis aligned.

                :param matrix: :py:class:`Matrix` specifying the transform
                :return: transformed :py:class:`RRect` or ``None``
                :rtype: :py:class:`RRect` | None
            )doc",
            "matrix"_a)
        .def(
            "dump",
            [](const SkRRect &rrect, const bool &asHex)
            {
                py::scoped_ostream_redirect stream;
                rrect.dump(asHex);
            },
            "asHex"_a = false)
        .def("__str__",
             [](const SkRRect &r)
             {
                 std::stringstream s;
                 s << "RRect(" << py::cast(r.rect()).attr("__str__")();
                 SkVector radii = r.radii(SkRRect::Corner::kUpperLeft_Corner);
                 s << ", TL=(" << radii.fX << ", " << radii.fY << ")";
                 radii = r.radii(SkRRect::Corner::kUpperRight_Corner);
                 s << ", TR=(" << radii.fX << ", " << radii.fY << ")";
                 radii = r.radii(SkRRect::Corner::kLowerRight_Corner);
                 s << ", BR=(" << radii.fX << ", " << radii.fY << ")";
                 radii = r.radii(SkRRect::Corner::kLowerLeft_Corner);
                 s << ", BL=(" << radii.fX << ", " << radii.fY << "))";
                 return s.str();
             });
}