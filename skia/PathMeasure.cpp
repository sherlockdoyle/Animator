#include "common.h"
#include "include/core/SkPathMeasure.h"

void initPathMeasure(py::module &m)
{
    py::class_<SkPathMeasure> PathMeasure(m, "PathMeasure");
    PathMeasure.def(py::init())
        .def(py::init<const SkPath &, bool, SkScalar>(), "path"_a, "forceClosed"_a = false, "resScale"_a = 1)
        .def("setPath", &SkPathMeasure::setPath, "path"_a, "forceClosed"_a = false)
        .def("getLength", &SkPathMeasure::getLength)
        .def(
            "getPosTan",
            [](SkPathMeasure &self, const SkScalar &distance)
            {
                SkPoint position;
                SkVector tangent;
                if (self.getPosTan(distance, &position, &tangent))
                    return py::make_tuple(position, tangent);
                throw std::runtime_error("zero-length path in getPosTan.");
            },
            "Pins *distance* to 0 <= distance <= getLength(), and returns the corresponding position and tangent.",
            "distance"_a);

    py::enum_<SkPathMeasure::MatrixFlags>(PathMeasure, "MatrixFlags", py::arithmetic())
        .value("kGetPosition_MatrixFlag", SkPathMeasure::MatrixFlags::kGetPosition_MatrixFlag)
        .value("kGetTangent_MatrixFlag", SkPathMeasure::MatrixFlags::kGetTangent_MatrixFlag)
        .value("kGetPosAndTan_MatrixFlag", SkPathMeasure::MatrixFlags::kGetPosAndTan_MatrixFlag);
    PathMeasure
        .def(
            "getMatrix",
            [](SkPathMeasure &measure, const SkScalar &distance, const SkPathMeasure::MatrixFlags &flags)
            {
                SkMatrix matrix;
                if (measure.getMatrix(distance, &matrix, flags))
                    return matrix;
                throw std::runtime_error("zero-length path in getMatrix.");
            },
            R"doc(
                Pins *distance* to 0 <= distance <= getLength(), and returns the corresponding matrix (by calling
                getPosTan).
            )doc",
            "distance"_a, "flags"_a = SkPathMeasure::MatrixFlags::kGetPosAndTan_MatrixFlag)
        .def(
            "getSegment",
            [](SkPathMeasure &self, const SkScalar &startD, const SkScalar &stopD, const bool &startWithMoveTo)
            {
                SkPath dst;
                if (self.getSegment(startD, stopD, &dst, startWithMoveTo))
                    return dst;
                return SkPath();
            },
            "Given a start and stop distance, return the intervening segment(s).", "startD"_a, "stopD"_a,
            "startWithMoveTo"_a = true)
        .def("isClosed", &SkPathMeasure::isClosed)
        .def("nextContour", &SkPathMeasure::nextContour);
}