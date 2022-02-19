#include "common.h"
#include "include/core/SkSize.h"
#include <pybind11/operators.h>

void initSize(py::module &m)
{
    py::class_<SkISize>(m, "ISize")
        .def(py::init(
                 [](const py::tuple &t)
                 {
                     if (t.size() != 2)
                         throw py::value_error("ISize must have exactly two elements.");
                     return SkISize::Make(t[0].cast<int32_t>(), t[1].cast<int32_t>());
                 }),
             R"doc(
                Create an :py:class:`ISize` from a tuple of two integers.

                :param t: Tuple of two integers.
            )doc",
             "t"_a)
        .def_static("MakeEmpty", &SkISize::MakeEmpty)
        .def(py::init(&SkISize::MakeEmpty))
        .def_static("Make", &SkISize::Make, "w"_a, "h"_a)
        .def(py::init(&SkISize::Make), "w"_a, "h"_a)
        .def_readwrite("fWidth", &SkISize::fWidth)
        .def_readwrite("fHeight", &SkISize::fHeight)
        .def("set", &SkISize::set, "w"_a, "h"_a)
        .def("isZero", &SkISize::isZero)
        .def("isEmpty", &SkISize::isEmpty)
        .def("setEmpty", &SkISize::setEmpty)
        .def("width", &SkISize::width)
        .def("height", &SkISize::height)
        .def("area", &SkISize::area)
        .def("equals", &SkISize::equals, "w"_a, "h"_a)
        .def(py::self == py::self, "other"_a)
        .def(py::self != py::self, "other"_a)
        .def(
            "__iter__", [](const SkISize &isize) { return py::make_iterator(&isize.fWidth, &isize.fWidth + 2); },
            py::keep_alive<0, 1>())
        .def("__len__", [](const SkISize &) { return 2; })
        .def("__str__",
             [](const SkISize &isize)
             {
                 std::stringstream s;
                 s << "ISize(" << isize.fWidth << ", " << isize.fHeight << ")";
                 return s.str();
             });

    py::implicitly_convertible<py::tuple, SkISize>();

    py::class_<SkSize>(m, "Size")
        .def(py::init(
                 [](const py::tuple &t)
                 {
                     if (t.size() != 2)
                         throw py::value_error("Size must have exactly two elements.");
                     return SkSize::Make(t[0].cast<SkScalar>(), t[1].cast<SkScalar>());
                 }),
             R"doc(
                Create a :py:class:`Size` from a tuple of two floats.

                :param t: Tuple of two floats.
            )doc",
             "t"_a)
        .def_readwrite("fWidth", &SkSize::fWidth)
        .def_readwrite("fHeight", &SkSize::fHeight)
        .def_static("MakeEmpty", &SkSize::MakeEmpty)
        .def(py::init(&SkSize::MakeEmpty))
        .def_static("Make", py::overload_cast<SkScalar, SkScalar>(&SkSize::Make), "w"_a, "h"_a)
        .def(py::init(py::overload_cast<SkScalar, SkScalar>(&SkSize::Make)), "w"_a, "h"_a)
        .def_static("Make", py::overload_cast<const SkISize &>(&SkSize::Make), "src"_a)
        .def(py::init(py::overload_cast<const SkISize &>(&SkSize::Make)), "src"_a)
        .def("set", &SkSize::set, "w"_a, "h"_a)
        .def("isZero", &SkSize::isZero)
        .def("isEmpty", &SkSize::isEmpty)
        .def("setEmpty", &SkSize::setEmpty)
        .def("width", &SkSize::width)
        .def("height", &SkSize::height)
        .def("equals", &SkSize::equals, "w"_a, "h"_a)
        .def("toRound", &SkSize::toRound)
        .def("toCeil", &SkSize::toCeil)
        .def("toFloor", &SkSize::toFloor)
        .def(py::self == py::self, "other"_a)
        .def(py::self != py::self, "other"_a)
        .def(
            "__iter__", [](const SkSize &size) { return py::make_iterator(&size.fWidth, &size.fWidth + 2); },
            py::keep_alive<0, 1>())
        .def("__len__", [](const SkSize &) { return 2; })
        .def("__str__",
             [](const SkSize &size)
             {
                 std::stringstream s;
                 s << "Size(" << size.fWidth << ", " << size.fHeight << ")";
                 return s.str();
             });

    py::implicitly_convertible<py::tuple, SkSize>();
    py::implicitly_convertible<SkISize, SkSize>();
}