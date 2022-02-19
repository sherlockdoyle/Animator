#include "common.h"
#include "include/core/SkString.h"
#include "include/utils/SkParsePath.h"

void initSvg(py::module &m)
{
    py::class_<SkParsePath> ParsePath(m, "ParsePath");
    ParsePath.def_static(
        "FromSVGString",
        [](const char str[])
        {
            SkPath result;
            if (SkParsePath::FromSVGString(str, &result))
                return result;
            throw py::value_error("Failed to parse path.");
        },
        "Create a :py:class:`skia.Path` from an SVG string.", "str"_a);

    py::enum_<SkParsePath::PathEncoding>(ParsePath, "PathEncoding")
        .value("Absolute", SkParsePath::PathEncoding::Absolute)
        .value("Relative", SkParsePath::PathEncoding::Relative);
    ParsePath.def_static(
        "ToSVGString",
        [](const SkPath &path, const SkParsePath::PathEncoding &encoding)
        {
            SkString str;
            SkParsePath::ToSVGString(path, &str, encoding);
            return py::str(str.c_str());
        },
        "Create an SVG string from a :py:class:`skia.Path`.", "path"_a,
        "encoding"_a = SkParsePath::PathEncoding::Absolute);
}