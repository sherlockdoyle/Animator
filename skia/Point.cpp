#include "common.h"
#include "include/core/SkPoint.h"
#include "include/core/SkPoint3.h"
#include <pybind11/operators.h>

void initPoint(py::module &m)
{
    py::class_<SkIPoint>(m, "IPoint")
        .def(py::init(
                 [](const py::tuple &t)
                 {
                     if (t.size() != 2)
                         throw py::value_error("IPoint must have exactly two elements.");
                     return SkIPoint::Make(t[0].cast<int32_t>(), t[1].cast<int32_t>());
                 }),
             R"doc(
                Create an :py:class:`IPoint` from a tuple of two integers.

                :param t: Tuple of two integers.
            )doc",
             "t"_a)
        .def_static("Make", &SkIPoint::Make, "x"_a, "y"_a)
        .def(py::init(&SkIPoint::Make), "x"_a, "y"_a)
        .def_readwrite("fX", &SkIPoint::fX)
        .def_readwrite("fY", &SkIPoint::fY)
        .def("x", &SkIPoint::x)
        .def("y", &SkIPoint::y)
        .def("isZero", &SkIPoint::isZero)
        .def("set", &SkIPoint::set, "x"_a, "y"_a)
        .def(-py::self)
        .def(py::self += py::self, "other"_a)
        .def(py::self -= py::self, "other"_a)
        .def("equals", &SkIPoint::equals, "x"_a, "y"_a)
        .def(py::self == py::self, "other"_a)
        .def(py::self != py::self, "other"_a)
        .def(py::self - py::self, "other"_a)
        .def(py::self + py::self, "other"_a)
        .def(
            "__iter__", [](const SkIPoint &p) { return py::make_iterator(&p.fX, &p.fX + 2); }, py::keep_alive<0, 1>())
        .def("__len__", [](const SkIPoint &) { return 2; })
        .def("__str__",
             [](const SkIPoint &p)
             {
                 std::stringstream s;
                 s << "IPoint(" << p.fX << ", " << p.fY << ")";
                 return s.str();
             });

    py::implicitly_convertible<py::tuple, SkIPoint>();

    py::class_<SkPoint>(m, "Point")
        .def(py::init([](const SkIPoint &p) { return SkPoint::Make(p.fX, p.fY); }), "ipoint"_a,
             R"doc(
                Create a :py:class:`Point` from an :py:class:`IPoint`.

                :param t: :py:class:`IPoint` to convert.
            )doc")
        .def(py::init(
                 [](const py::tuple &t)
                 {
                     if (t.size() != 2)
                         throw py::value_error("Point must have exactly two elements.");
                     return SkPoint::Make(t[0].cast<SkScalar>(), t[1].cast<SkScalar>());
                 }),
             R"doc(
                Create a :py:class:`Point` from a tuple of two floats.

                :param t: Tuple of two floats.
            )doc",
             "t"_a)
        .def_static("Make", &SkPoint::Make, "x"_a, "y"_a)
        .def(py::init(&SkPoint::Make), "x"_a, "y"_a)
        .def_readwrite("fX", &SkPoint::fX)
        .def_readwrite("fY", &SkPoint::fY)
        .def("x", &SkPoint::x)
        .def("y", &SkPoint::y)
        .def("isZero", &SkPoint::isZero)
        .def("set", &SkPoint::set, "x"_a, "y"_a)
        .def("iset", py::overload_cast<int32_t, int32_t>(&SkPoint::iset), "x"_a, "y"_a)
        .def("iset", py::overload_cast<const SkIPoint &>(&SkPoint::iset), "p"_a)
        .def("setAbs", &SkPoint::setAbs, "pt"_a)
        .def_static(
            "Offset",
            [](std::vector<SkPoint> &points, const SkVector &offset)
            {
                SkPoint::Offset(points.data(), points.size(), offset);
                return points;
            },
            "points"_a, "offset"_a)
        .def_static(
            "Offset",
            [](std::vector<SkPoint> &points, SkScalar dx, SkScalar dy)
            {
                SkPoint::Offset(points.data(), points.size(), dx, dy);
                return points;
            },
            "points"_a, "dx"_a, "dy"_a)
        .def("offset", &SkPoint::offset, "dx"_a, "dy"_a)
        .def("length", &SkPoint::length)
        .def("distanceToOrigin", &SkPoint::distanceToOrigin)
        .def("normalize", &SkPoint::normalize)
        .def("setNormalize", &SkPoint::setNormalize, "x"_a, "y"_a)
        .def("setLength", py::overload_cast<SkScalar>(&SkPoint::setLength), "length"_a)
        .def("setLength", py::overload_cast<SkScalar, SkScalar, SkScalar>(&SkPoint::setLength), "x"_a, "y"_a,
             "length"_a)
        .def(
            "makeScaled",
            [](const SkPoint &p, const SkScalar &scale)
            {
                SkPoint dst;
                p.scale(scale, &dst);
                return dst;
            },
            R"doc(
                Return a new point that is the result of scaling this point by the given *scale*.

                :param scale: factor to multiply :py:class:`Point` by
                :return: a new :py:class:`Point` scaled by *scale*
            )doc",
            "scale"_a)
        .def("scale", py::overload_cast<SkScalar>(&SkPoint::scale), "scale"_a)
        .def("negate", &SkPoint::negate)
        .def(-py::self)
        .def(py::self += py::self, "other"_a)
        .def(py::self -= py::self, "other"_a)
        .def(py::self * SkScalar(), "scale"_a)
        .def(py::self *= SkScalar(), py::arg("scale"))
        .def("isFinite", &SkPoint::isFinite)
        .def("equals", &SkPoint::equals, "x"_a, "y"_a)
        .def(py::self == py::self, "other"_a)
        .def(py::self != py::self, "other"_a)
        .def(py::self - py::self, "other"_a)
        .def(py::self + py::self, "other"_a)
        .def_static("Length", &SkPoint::Length, "x"_a, "y"_a)
        .def_static("Normalize", &SkPoint::Normalize, "vec"_a)
        .def_static("Distance", &SkPoint::Distance, "a"_a, "b"_a)
        .def_static("DotProduct", &SkPoint::DotProduct, "a"_a, "b"_a)
        .def_static("CrossProduct", &SkPoint::CrossProduct, "a"_a, "b"_a)
        .def("cross", &SkPoint::cross, "vec"_a)
        .def("dot", &SkPoint::dot, "vec"_a)
        .def(
            "__iter__", [](const SkPoint &p) { return py::make_iterator(&p.fX, &p.fX + 2); }, py::keep_alive<0, 1>())
        .def("__len__", [](const SkPoint &) { return 2; })
        .def("__str__",
             [](const SkPoint &p)
             {
                 std::stringstream s;
                 s << "Point(" << p.fX << ", " << p.fY << ")";
                 return s.str();
             });

    py::implicitly_convertible<py::tuple, SkPoint>();
    py::implicitly_convertible<SkIPoint, SkPoint>();

    py::class_<SkPoint3>(m, "Point3")
        .def(py::init(
                 [](const py::tuple &t)
                 {
                     if (t.size() != 3)
                         throw py::value_error("Point3 must have exactly 3 elements.");
                     return SkPoint3::Make(t[0].cast<SkScalar>(), t[1].cast<SkScalar>(), t[2].cast<SkScalar>());
                 }),
             "t"_a)
        .def_readwrite("fX", &SkPoint3::fX)
        .def_readwrite("fY", &SkPoint3::fY)
        .def_readwrite("fZ", &SkPoint3::fZ)
        .def_static("Make", &SkPoint3::Make, "x"_a, "y"_a, "z"_a)
        .def(py::init(&SkPoint3::Make), "x"_a, "y"_a, "z"_a)
        .def("x", &SkPoint3::x)
        .def("y", &SkPoint3::y)
        .def("z", &SkPoint3::z)
        .def("set", &SkPoint3::set, "x"_a, "y"_a, "z"_a)
        .def(py::self == py::self, "other"_a)
        .def(py::self != py::self, "other"_a)
        .def_static("Length", &SkPoint3::Length, "x"_a, "y"_a, "z"_a)
        .def("length", &SkPoint3::length)
        .def("normalize", &SkPoint3::normalize)
        .def("makeScale", &SkPoint3::makeScale, "scale"_a)
        .def("scale", &SkPoint3::scale, "value"_a)
        .def(-py::self)
        .def(py::self - py::self, "other"_a)
        .def(py::self + py::self, "other"_a)
        .def(
            "__iadd__",
            [](SkPoint3 &p, const SkPoint3 &v)
            {
                p += v;
                return p;
            },
            py::is_operator(), "v"_a)
        .def(
            "__isub__",
            [](SkPoint3 &p, const SkPoint3 &v)
            {
                p -= v;
                return p;
            },
            py::is_operator(), "v"_a)
        .def(SkScalar() * py::self, "t"_a)
        .def("isFinite", &SkPoint3::isFinite)
        .def_static("DotProduct", &SkPoint3::DotProduct, "a"_a, "b"_a)
        .def("dot", &SkPoint3::dot, "vec"_a)
        .def_static("CrossProduct", &SkPoint3::CrossProduct, "a"_a, "b"_a)
        .def("cross", &SkPoint3::cross, "vec"_a)
        .def(
            "__iter__", [](const SkPoint3 &p) { return py::make_iterator(&p.fX, &p.fX + 3); }, py::keep_alive<0, 1>())
        .def("__len__", [](const SkPoint3 &) { return 3; })
        .def("__str__",
             [](const SkPoint3 &p)
             {
                 std::stringstream s;
                 s << "Point3(" << p.fX << ", " << p.fY << ", " << p.fZ << ")";
                 return s.str();
             });

    py::implicitly_convertible<py::tuple, SkPoint3>();
}