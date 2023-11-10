#include "common.h"
#include "pm.h"

class PathMatcher
{
private:
    SkPath path0, path1;

public:
    PathMatcher(const SkPath &p0, const SkPath &p1, const float distFactor = 1.0f,
                const ContourMatcher::MatchType matchType = ContourMatcher::MatchType::split)
    {
        if (p0.isInterpolatable(p1))
        {
            path0 = p0;
            path1 = p1;
        }
        else
            ContourMatcher(p0, p1, distFactor, matchType).writeToPath(path0, path1);
    }
    void interpolate(const SkScalar weight, SkPath *out) { path1.interpolate(path0, weight, out); }
};

void initPathMatcher(py::module &m)
{
    py::class_<PathMatcher> PathMatcherClass(m, "PathMatcher", "Make two path interpolatable.");

    py::enum_<ContourMatcher::MatchType>(PathMatcherClass, "MatchType")
        .value("inBetween", ContourMatcher::MatchType::inBetween, "Add empty segments in between other segments.")
        .value("split", ContourMatcher::MatchType::split, "Split the largest segments.");
    PathMatcherClass
        .def(py::init<const SkPath &, const SkPath &, const float, const ContourMatcher::MatchType>(), "path0"_a,
             "path1"_a, "distFactor"_a = 1.0f, "matchType"_a = ContourMatcher::MatchType::split)
        .def("interpolate", &PathMatcher::interpolate, "Interpolate two paths by *weight* ad write to *out*.",
             "weight"_a, "out"_a);
}