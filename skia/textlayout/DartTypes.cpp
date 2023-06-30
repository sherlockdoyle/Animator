#include "modules/skparagraph/include/DartTypes.h"
#include "common.h"
#include <pybind11/operators.h>

using namespace skia::textlayout;

void initDartTypes(py::module &m)
{
    py::enum_<Affinity>(m, "Affinity")
        .value("kUpstream", Affinity::kUpstream)
        .value("kDownstream", Affinity::kDownstream);

    py::enum_<RectHeightStyle>(m, "RectHeightStyle")
        .value("kTight", RectHeightStyle::kTight)
        .value("kMax", RectHeightStyle::kMax)
        .value("kIncludeLineSpacingMiddle", RectHeightStyle::kIncludeLineSpacingMiddle)
        .value("kIncludeLineSpacingTop", RectHeightStyle::kIncludeLineSpacingTop)
        .value("kIncludeLineSpacingBottom", RectHeightStyle::kIncludeLineSpacingBottom)
        .value("kStrut", RectHeightStyle::kStrut);

    py::enum_<RectWidthStyle>(m, "RectWidthStyle")
        .value("kTight", RectWidthStyle::kTight)
        .value("kMax", RectWidthStyle::kMax);

    py::enum_<TextAlign>(m, "TextAlign")
        .value("kLeft", TextAlign::kLeft)
        .value("kRight", TextAlign::kRight)
        .value("kCenter", TextAlign::kCenter)
        .value("kJustify", TextAlign::kJustify)
        .value("kStart", TextAlign::kStart)
        .value("kEnd", TextAlign::kEnd);

    py::enum_<TextDirection>(m, "TextDirection").value("kRtl", TextDirection::kRtl).value("kLtr", TextDirection::kLtr);

    py::class_<PositionWithAffinity>(m, "PositionWithAffinity")
        .def_readwrite("position", &PositionWithAffinity::position)
        .def_readwrite("affinity", &PositionWithAffinity::affinity)
        .def(py::init())
        .def(py::init<int32_t, Affinity>(), "position"_a = 0, "affinity"_a = Affinity::kDownstream)
        .def("__str__", [](const PositionWithAffinity &self)
             { return "PositionWithAffinity(position={}, affinity={})"_s.format(self.position, self.affinity); });

    py::class_<TextBox>(m, "TextBox")
        .def_readwrite("rect", &TextBox::rect)
        .def_readwrite("direction", &TextBox::direction)
        .def(py::init<SkRect, TextDirection>(), "rect"_a, "direction"_a)
        .def("__str__",
             [](const TextBox &self) { return "TextBox(rect={}, direction={})"_s.format(self.rect, self.direction); });

    typedef SkRange<size_t> Range;
    py::class_<Range>(m, "Range")
        .def(py::init())
        .def(py::init<size_t, size_t>(), "start"_a, "end"_a)
        .def(py::init(
            [](const py::tuple &t)
            {
                if (t.size() != 2)
                    throw py::value_error("Range must have exactly 2 elements.");
                return Range(t[0].cast<size_t>(), t[1].cast<size_t>());
            }))
        .def_readwrite("start", &Range::start)
        .def_readwrite("end", &Range::end)
        .def(py::self == py::self)
        .def("width", &Range::width)
        .def("Shift", &Range::Shift)
        .def("contains", &Range::contains, "other"_a)
        .def("__contains__", &Range::contains, py::is_operator())
        .def("intersects", &Range::intersects, "other"_a)
        .def("intersection", &Range::intersection, "other"_a)
        .def("__and__", &Range::intersection, py::is_operator())
        .def("empty", &Range::empty)
        .def("__str__", [](const Range &self) { return "Range({}, {})"_s.format(self.start, self.end); });

    py::implicitly_convertible<py::tuple, Range>();

    py::enum_<TextBaseline>(m, "TextBaseline")
        .value("kAlphabetic", TextBaseline::kAlphabetic)
        .value("kIdeographic", TextBaseline::kIdeographic);

    py::enum_<TextHeightBehavior>(m, "TextHeightBehavior", py::arithmetic())
        .value("kAll", TextHeightBehavior::kAll)
        .value("kDisableFirstAscent", TextHeightBehavior::kDisableFirstAscent)
        .value("kDisableLastDescent", TextHeightBehavior::kDisableLastDescent)
        .value("kDisableAll", TextHeightBehavior::kDisableAll);

    py::enum_<LineMetricStyle>(m, "LineMetricStyle")
        .value("Typographic", LineMetricStyle::Typographic)
        .value("CSS", LineMetricStyle::CSS);
}