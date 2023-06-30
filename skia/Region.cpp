#include "common.h"
#include "include/core/SkData.h"
#include "include/core/SkPath.h"
#include "include/core/SkRegion.h"
#include <pybind11/operators.h>
#include <pybind11/stl.h>

const int SkRegion::kOpCnt;
template <typename OtherType, SkRegion::Op op> SkRegion region_op(const SkRegion &self, const OtherType &other)
{
    SkRegion result;
    result.op(self, other, op);
    return result;
}
template <typename OtherType, SkRegion::Op op> SkRegion &region_iop(SkRegion &self, const OtherType &other)
{
    self.op(other, op);
    return self;
}

void initRegion(py::module &m)
{
    py::class_<SkRegion> Region(m, "Region", R"doc(
        :py:class:`Region` describes the set of pixels used to clip :py:class:`Canvas`.

        :py:class:`Region` supports a few operators::

            regionA == regionB  # Equality
            regionA != regionB  # Inequality

            regionA - regionB   # Difference
            regionA & regionB   # Intersect
            regionA | regionB   # Union
            regionA ^ regionB   # XOR

            regionA -= regionB  # In-place Difference
            regionA &= regionB  # In-place Intersect
            regionA |= regionB  # In-place Union
            regionA ^= regionB  # In-place XOR
    )doc");
    Region.def(py::init())
        .def(py::init<const SkRegion &>(), "region"_a)
        .def(py::init<const SkIRect &>(), "rect"_a)
        .def(py::self == py::self, "other"_a)
        .def(py::self != py::self, "other"_a)
        .def("set", &SkRegion::set, "src"_a)
        .def("swap", &SkRegion::swap, "other"_a)
        .def("isEmpty", &SkRegion::isEmpty)
        .def("isRect", &SkRegion::isRect)
        .def("isComplex", &SkRegion::isComplex)
        .def("getBounds", &SkRegion::getBounds)
        .def("computeRegionComplexity", &SkRegion::computeRegionComplexity)
        .def("getBoundaryPath", &SkRegion::getBoundaryPath, "path"_a)
        .def("setEmpty", &SkRegion::setEmpty)
        .def("setRect", &SkRegion::setRect, "rect"_a)
        .def(
            "setRects",
            [](SkRegion &self, const std::vector<SkIRect> &rects) { return self.setRects(rects.data(), rects.size()); },
            "Constructs :py:class:`Region` as the union of :py:class:`IRect` in *rects* array.", "rects"_a)
        .def("setRegion", &SkRegion::setRegion, "region"_a)
        .def("setPath", &SkRegion::setPath, "path"_a, "clip"_a)
        .def("intersects", py::overload_cast<const SkIRect &>(&SkRegion::intersects, py::const_), "rect"_a)
        .def("intersects", py::overload_cast<const SkRegion &>(&SkRegion::intersects, py::const_), "other"_a)
        .def("contains", py::overload_cast<int32_t, int32_t>(&SkRegion::contains, py::const_), "x"_a, "y"_a)
        .def(
            "__contains__",
            [](const SkRegion &self, const py::tuple &point)
            { return self.contains(py::cast<int32_t>(point[0]), py::cast<int32_t>(point[1])); },
            py::is_operator(), "Checks if *point* is inside :py:class:`Region`.", "point"_a)
        .def("contains", py::overload_cast<const SkIRect &>(&SkRegion::contains, py::const_), "other"_a)
        .def("__contains__", py::overload_cast<const SkIRect &>(&SkRegion::contains, py::const_), py::is_operator())
        .def("contains", py::overload_cast<const SkRegion &>(&SkRegion::contains, py::const_), "other"_a)
        .def("__contains__", py::overload_cast<const SkRegion &>(&SkRegion::contains, py::const_), py::is_operator())
        .def("quickContains", &SkRegion::quickContains, "r"_a)
        .def("quickReject", py::overload_cast<const SkIRect &>(&SkRegion::quickReject, py::const_), "rect"_a)
        .def("quickReject", py::overload_cast<const SkRegion &>(&SkRegion::quickReject, py::const_), "region"_a)
        .def("translate", py::overload_cast<int, int>(&SkRegion::translate), "dx"_a, "dy"_a)
        .def(
            "makeTranslate",
            [](const SkRegion &self, const int &dx, const int &dy)
            {
                SkRegion dst;
                self.translate(dx, dy, &dst);
                return dst;
            },
            "Makes a copy of :py:class:`Region` translated by *dx* and *dy*.", "dx"_a, "dy"_a);

    py::enum_<SkRegion::Op>(Region, "Op")
        .value("kDifference_Op", SkRegion::Op::kDifference_Op)
        .value("kIntersect_Op", SkRegion::Op::kIntersect_Op)
        .value("kUnion_Op", SkRegion::Op::kUnion_Op)
        .value("kXOR_Op", SkRegion::Op::kXOR_Op)
        .value("kReverseDifference_Op", SkRegion::Op::kReverseDifference_Op)
        .value("kReplace_Op", SkRegion::Op::kReplace_Op)
        .value("kLastOp", SkRegion::Op::kLastOp);
    Region.def_readonly_static("kOpCnt", &SkRegion::kOpCnt)
        .def("op", py::overload_cast<const SkIRect &, SkRegion::Op>(&SkRegion::op), "rect"_a, "op"_a)
        .def("op", py::overload_cast<const SkRegion &, SkRegion::Op>(&SkRegion::op), "rgn"_a, "op"_a)
        .def("op", py::overload_cast<const SkIRect &, const SkRegion &, SkRegion::Op>(&SkRegion::op), "rect"_a, "rgn"_a,
             "op"_a)
        .def("op", py::overload_cast<const SkRegion &, const SkIRect &, SkRegion::Op>(&SkRegion::op), "rgn"_a, "rect"_a,
             "op"_a)
        .def("op", py::overload_cast<const SkRegion &, const SkRegion &, SkRegion::Op>(&SkRegion::op), "rgna"_a,
             "rgnb"_a, "op"_a);

    py::class_<SkRegion::Iterator>(Region, "Iterator")
        .def(py::init())
        .def(py::init<const SkRegion &>(), "region"_a)
        .def("rewind", &SkRegion::Iterator::rewind)
        .def("reset", &SkRegion::Iterator::reset, "region"_a)
        .def("done", &SkRegion::Iterator::done)
        .def("next", &SkRegion::Iterator::next)
        .def("rect", &SkRegion::Iterator::rect)
        .def("rgn", &SkRegion::Iterator::rgn)
        .def(
            "__iter__", [](const SkRegion::Iterator &self) { return self; }, py::keep_alive<0, 1>())
        .def("__next__",
             [](SkRegion::Iterator &self)
             {
                 if (self.done())
                     throw py::stop_iteration();
                 const SkIRect rect = self.rect();
                 self.next();
                 return rect;
             });
    Region.def(
        "__iter__", [](const SkRegion &self) { return SkRegion::Iterator(self); }, py::keep_alive<0, 1>());

    py::class_<SkRegion::Cliperator>(Region, "Cliperator")
        .def(py::init<const SkRegion &, const SkIRect &>(), "region"_a, "clip"_a)
        .def("done", &SkRegion::Cliperator::done)
        .def("next", &SkRegion::Cliperator::next)
        .def("rect", &SkRegion::Cliperator::rect)
        .def(
            "__iter__", [](const SkRegion::Cliperator &self) { return self; }, py::keep_alive<0, 1>())
        .def("__next__",
             [](SkRegion::Cliperator &it)
             {
                 if (it.done())
                     throw py::stop_iteration();
                 const SkIRect rect = it.rect();
                 it.next();
                 return rect;
             });

    py::class_<SkRegion::Spanerator>(Region, "Spanerator")
        .def(py::init<const SkRegion &, int, int, int>(), "region"_a, "y"_a, "left"_a, "right"_a)
        .def(
            "next",
            [](SkRegion::Spanerator &self) -> std::optional<py::tuple>
            {
                int left, right;
                if (self.next(&left, &right))
                    return py::make_tuple(left, right);
                return std::nullopt;
            },
            R"doc(
                Advances iterator to next span intersecting :py:class:`Region` within line segment provided in
                constructor. Returns ``None`` if no intervals were found.
            )doc")
        .def(
            "__iter__", [](const SkRegion::Spanerator &self) { return self; }, py::keep_alive<0, 1>())
        .def("__next__",
             [](SkRegion::Spanerator &self)
             {
                 int left, right;
                 if (self.next(&left, &right))
                     return py::make_tuple(left, right);
                 throw py::stop_iteration();
             });

    Region
        .def(
            "writeToMemory",
            [](const SkRegion &self)
            {
                size_t size = self.writeToMemory(nullptr);
                sk_sp<SkData> data = SkData::MakeUninitialized(size);
                self.writeToMemory(data->writable_data());
                return data;
            },
            "Writes :py:class:`Region` to :py:class:`Data` and returns it.")
        .def(
            "readFromMemory",
            [](SkRegion &self, const SkData &data) { return self.readFromMemory(data.data(), data.size()); },
            "Reads :py:class:`Region` from given :py:class:`Data`.", "buffer"_a)

        .def("__sub__", &region_op<SkRegion, SkRegion::kDifference_Op>, py::is_operator())
        .def("__and__", &region_op<SkRegion, SkRegion::kIntersect_Op>, py::is_operator())
        .def("__or__", &region_op<SkRegion, SkRegion::kUnion_Op>, py::is_operator())
        .def("__xor__", &region_op<SkRegion, SkRegion::kXOR_Op>, py::is_operator())
        .def("__isub__", &region_iop<SkRegion, SkRegion::kDifference_Op>, py::is_operator())
        .def("__iand__", &region_iop<SkRegion, SkRegion::kIntersect_Op>, py::is_operator())
        .def("__ior__", &region_iop<SkRegion, SkRegion::kUnion_Op>, py::is_operator())
        .def("__ixor__", &region_iop<SkRegion, SkRegion::kXOR_Op>, py::is_operator())

        .def("__sub__", &region_op<SkIRect, SkRegion::kDifference_Op>, py::is_operator())
        .def("__and__", &region_op<SkIRect, SkRegion::kIntersect_Op>, py::is_operator())
        .def("__or__", &region_op<SkIRect, SkRegion::kUnion_Op>, py::is_operator())
        .def("__xor__", &region_op<SkIRect, SkRegion::kXOR_Op>, py::is_operator())
        .def("__rsub__", &region_op<SkIRect, SkRegion::kDifference_Op>, py::is_operator())
        .def("__rand__", &region_op<SkIRect, SkRegion::kIntersect_Op>, py::is_operator())
        .def("__ror__", &region_op<SkIRect, SkRegion::kUnion_Op>, py::is_operator())
        .def("__rxor__", &region_op<SkIRect, SkRegion::kXOR_Op>, py::is_operator())
        .def("__isub__", &region_iop<SkIRect, SkRegion::kDifference_Op>, py::is_operator())
        .def("__iand__", &region_iop<SkIRect, SkRegion::kIntersect_Op>, py::is_operator())
        .def("__ior__", &region_iop<SkIRect, SkRegion::kUnion_Op>, py::is_operator())
        .def("__ixor__", &region_iop<SkIRect, SkRegion::kXOR_Op>, py::is_operator())

        .def("__str__",
             [](const SkRegion &self)
             {
                 std::stringstream s;
                 s << "Region(";
                 SkRegion::Iterator iter(self);
                 while (!iter.done())
                 {
                     const SkIRect &rect = iter.rect();
                     s << "(" << rect.fLeft << ", " << rect.fTop << ", " << rect.fRight << ", " << rect.fBottom << ")";
                     iter.next();
                 }
                 s << ")";
                 return s.str();
             });

    py::implicitly_convertible<SkIRect, SkRegion>();
}