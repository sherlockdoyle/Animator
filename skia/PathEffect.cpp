#include "common.h"
#include "include/core/SkPathEffect.h"
#include "include/core/SkStrokeRec.h"
#include "include/effects/Sk1DPathEffect.h"
#include "include/effects/Sk2DPathEffect.h"
#include "include/effects/SkCornerPathEffect.h"
#include "include/effects/SkDashPathEffect.h"
#include "include/effects/SkDiscretePathEffect.h"
#include "include/effects/SkImageFilters.h"
#include "include/effects/SkOpPathEffect.h"
#include "include/effects/SkStrokeAndFillPathEffect.h"
#include "include/effects/SkTrimPathEffect.h"
#include <pybind11/stl.h>

struct PyDashInfo : public SkPathEffect::DashInfo
{
    SkPathEffect::DashType fType;
    void alloc() { fIntervals = new SkScalar[fCount]; }
    ~PyDashInfo() { delete[] fIntervals; }
};

void initPathEffect(py::module &m)
{
    py::class_<SkStrokeRec> StrokeRec(m, "StrokeRec");

    py::enum_<SkStrokeRec::InitStyle>(StrokeRec, "InitStyle")
        .value("kHairline_InitStyle", SkStrokeRec::InitStyle::kHairline_InitStyle)
        .value("kFill_InitStyle", SkStrokeRec::InitStyle::kFill_InitStyle);
    StrokeRec.def(py::init<SkStrokeRec::InitStyle>(), "style"_a)
        .def(py::init<const SkPaint &, SkPaint::Style, SkScalar>(), "paint"_a, "style"_a, "resScale"_a = 1)
        .def(py::init<const SkPaint &, SkScalar>(), "paint"_a, "resScale"_a = 1);

    py::enum_<SkStrokeRec::Style>(StrokeRec, "Style")
        .value("kHairline_Style", SkStrokeRec::Style::kHairline_Style)
        .value("kFill_Style", SkStrokeRec::Style::kFill_Style)
        .value("kStroke_Style", SkStrokeRec::Style::kStroke_Style)
        .value("kStrokeAndFill_Style", SkStrokeRec::Style::kStrokeAndFill_Style);
    StrokeRec.def_readonly_static("kStyleCount", &SkStrokeRec::kStyleCount)
        .def("getStyle", &SkStrokeRec::getStyle)
        .def("getWidth", &SkStrokeRec::getWidth)
        .def("getMiter", &SkStrokeRec::getMiter)
        .def("getCap", &SkStrokeRec::getCap)
        .def("getJoin", &SkStrokeRec::getJoin)
        .def("isHairlineStyle", &SkStrokeRec::isHairlineStyle)
        .def("isFillStyle", &SkStrokeRec::isFillStyle)
        .def("setFillStyle", &SkStrokeRec::setFillStyle)
        .def("setHairlineStyle", &SkStrokeRec::setHairlineStyle)
        .def("setStrokeStyle", &SkStrokeRec::setStrokeStyle, "width"_a, "strokeAndFill"_a = false)
        .def("setStrokeParams", &SkStrokeRec::setStrokeParams, "cap"_a, "join"_a, "miterLimit"_a)
        .def("getResScale", &SkStrokeRec::getResScale)
        .def("setResScale", &SkStrokeRec::setResScale, "rs"_a)
        .def("needToApply", &SkStrokeRec::needToApply)
        .def("applyToPath", &SkStrokeRec::applyToPath, "dst"_a, "src"_a)
        .def("applyToPaint", &SkStrokeRec::applyToPaint, "paint"_a)
        .def("getInflationRadius", &SkStrokeRec::getInflationRadius)
        .def_static("GetInflationRadius",
                    py::overload_cast<const SkPaint &, SkPaint::Style>(&SkStrokeRec::GetInflationRadius), "paint"_a,
                    "style"_a)
        .def_static(
            "GetInflationRadius",
            py::overload_cast<SkPaint::Join, SkScalar, SkPaint::Cap, SkScalar>(&SkStrokeRec::GetInflationRadius),
            "join"_a, "miterLimit"_a, "cap"_a, "strokeWidth"_a)
        .def("hasEqualEffect", &SkStrokeRec::hasEqualEffect, "other"_a)
        .def("__eq__", &SkStrokeRec::hasEqualEffect, py::is_operator(), "other"_a)
        .def("__str__",
             [](const SkStrokeRec &self)
             {
                 return "StrokeRec({}, width={}, miter={}, cap={}, join={}, resScale={})"_s.format(
                     self.getStyle(), self.getWidth(), self.getMiter(), self.getCap(), self.getJoin(),
                     self.getResScale());
             });

    py::class_<SkPathEffect, sk_sp<SkPathEffect>, SkFlattenable> PathEffect(m, "PathEffect");
    PathEffect.def_static("MakeSum", &SkPathEffect::MakeSum, "first"_a, "second"_a)
        .def_static("MakeCompose", &SkPathEffect::MakeCompose, "outer"_a, "inner"_a)
        .def_static("GetFlattenableType", &SkPathEffect::GetFlattenableType);

    py::enum_<SkPathEffect::DashType>(PathEffect, "DashType")
        .value("kNone_DashType", SkPathEffect::DashType::kNone_DashType)
        .value("kDash_DashType", SkPathEffect::DashType::kDash_DashType);

    py::class_<PyDashInfo>(
        PathEffect, "DashInfo",
        "Contains information about a dash pattern. This also contains an extra field ``fType`` for the dash type.")
        .def(py::init())
        .def_property_readonly("fIntervals", [](const PyDashInfo &self)
                               { return std::vector<SkScalar>(self.fIntervals, self.fIntervals + self.fCount); })
        .def_readonly("fCount", &PyDashInfo::fCount)
        .def_readonly("fPhase", &PyDashInfo::fPhase)
        .def_readonly("fType", &PyDashInfo::fType, "The :py:class:`skia.PathEffect.DashType` of this dash.")
        .def("__str__",
             [](const PyDashInfo &self)
             {
                 std::stringstream s;
                 s << "DashInfo({}"_s.format(self.fType);

                 if (self.fType != SkPathEffect::DashType::kNone_DashType)
                 {
                     s << ", count=" << self.fCount << ", intervals=[";
                     for (int i = 0; i < self.fCount; ++i)
                     {
                         if (i > 0)
                             s << ", ";
                         s << self.fIntervals[i];
                     }
                     s << "], phase=" << self.fPhase;
                 }

                 s << ")";
                 return s.str();
             });
    PathEffect
        .def(
            "asADash",
            [](const SkPathEffect &self)
            {
                std::unique_ptr<PyDashInfo> info = std::make_unique<PyDashInfo>();
                info->fType = self.asADash(info.get());
                if (info->fCount)
                {
                    info->alloc();
                    info->fType = self.asADash(info.get());
                }
                return info;
            },
            R"doc(
                Return a :py:class:`skia.PathEffect.DashInfo` object with the dash information. The returned object also
                contains an extra field ``fType`` for the dash type.
            )doc")
        .def(
            "filterPath",
            [](const SkPathEffect &self, const SkPath &src, SkStrokeRec *rec, const SkRect *cullR,
               const SkMatrix &ctm) -> std::optional<SkPath>
            {
                SkPath dst;
                if (self.filterPath(&dst, src, rec, cullR, ctm))
                    return dst;
                return std::nullopt;
            },
            R"doc(
                Given a *src* path (input) and a stroke-*rec* (input and output), apply this effect to the *src* path,
                returning the new path.
            )doc",
            "src"_a, "rec"_a, "cullR"_a = skif::kNoCropRect, "ctm"_a = SkMatrix::I())
        .def("needsCTM", &SkPathEffect::needsCTM)
        .def_static(
            "Deserialize",
            [](const py::buffer &data)
            {
                const py::buffer_info bufInfo = data.request();
                return SkPathEffect::Deserialize(bufInfo.ptr, bufInfo.size * bufInfo.itemsize, nullptr);
            },
            "data"_a);

    py::class_<SkPath1DPathEffect> Path1DPathEffect(m, "Path1DPathEffect");

    py::enum_<SkPath1DPathEffect::Style>(Path1DPathEffect, "Style")
        .value("kTranslate_Style", SkPath1DPathEffect::Style::kTranslate_Style)
        .value("kRotate_Style", SkPath1DPathEffect::Style::kRotate_Style)
        .value("kMorph_Style", SkPath1DPathEffect::Style::kMorph_Style)
        .value("kLastEnum_Style", SkPath1DPathEffect::Style::kLastEnum_Style);
    Path1DPathEffect.def_static("Make", &SkPath1DPathEffect::Make, "path"_a, "advance"_a, "phase"_a, "style"_a);

    py::class_<SkLine2DPathEffect>(m, "Line2DPathEffect")
        .def_static("Make", &SkLine2DPathEffect::Make, "width"_a, "matrix"_a);

    py::class_<SkPath2DPathEffect>(m, "Path2DPathEffect")
        .def_static("Make", &SkPath2DPathEffect::Make, "matrix"_a, "path"_a);

    py::class_<SkCornerPathEffect>(m, "CornerPathEffect").def_static("Make", &SkCornerPathEffect::Make, "radius"_a);

    py::class_<SkDashPathEffect>(m, "DashPathEffect")
        .def_static(
            "Make",
            [](const std::vector<SkScalar> &intervals, const SkScalar &phase)
            {
                const size_t count = intervals.size();
                if (count < 2 || count & 1)
                    throw py::value_error("intervals must be an array of even length >= 2");
                return SkDashPathEffect::Make(intervals.data(), count, phase);
            },
            "intervals"_a, "phase"_a = 0);

    py::class_<SkDiscretePathEffect>(m, "DiscretePathEffect")
        .def_static("Make", &SkDiscretePathEffect::Make, "segLength"_a, "dev"_a, "seedAssist"_a = 0);

    py::class_<SkMergePathEffect>(m, "MergePathEffect")
        .def_static("Make", &SkMergePathEffect::Make, "one"_a, "two"_a, "op"_a);

    py::class_<SkMatrixPathEffect>(m, "MatrixPathEffect")
        .def_static("MakeTranslate", &SkMatrixPathEffect::MakeTranslate, "dx"_a, "dy"_a)
        .def_static("Make", &SkMatrixPathEffect::Make, "matrix"_a);

    py::class_<SkStrokePathEffect>(m, "StrokePathEffect")
        .def_static("Make", &SkStrokePathEffect::Make, "width"_a, "join"_a, "cap"_a, "miter"_a = 4);

    py::class_<SkTrimPathEffect> TrimPathEffect(m, "TrimPathEffect");

    py::enum_<SkTrimPathEffect::Mode>(TrimPathEffect, "Mode")
        .value("kNormal", SkTrimPathEffect::Mode::kNormal)
        .value("kInverted", SkTrimPathEffect::Mode::kInverted);
    TrimPathEffect.def_static("Make", &SkTrimPathEffect::Make, "startT"_a, "stopT"_a,
                              "mode"_a = SkTrimPathEffect::Mode::kNormal);

    py::class_<SkStrokeAndFillPathEffect>(m, "StrokeAndFillPathEffect")
        .def_static("Make", &SkStrokeAndFillPathEffect::Make);
}