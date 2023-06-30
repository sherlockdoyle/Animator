#include "common.h"
#include "include/core/SkColor.h"
#include <pybind11/operators.h>
#include <pybind11/stl.h>

void initColor(py::module &m)
{
    m.def(
        "Color", [](U8CPU r, U8CPU g, U8CPU b, U8CPU a) { return SkColorSetARGB(a, r, g, b); },
        R"doc(
            Returns color value from 8-bit component values.

            :param int r: amount of red, from no red (0) to full red (255)
            :param int g: amount of green, from no green (0) to full green (255)
            :param int b: amount of blue, from no blue (0) to full blue (255)
            :param int a: amount of alpha, from fully transparent (0) to fully opaque (255)
            :return: color and alpha, unpremultiplied
        )doc",
        "r"_a, "g"_a, "b"_a, "a"_a = 255);
    m.def(
        "Color", [](SkColor4f &color4f) { return color4f.toSkColor(); },
        R"doc(
            Returns color value from 4-float component values (:py:class:`Color4f`).

            :param color4f: color and alpha, unpremultiplied
            :return: color and alpha, unpremultiplied
        )doc",
        "color4f"_a);
    m.def("ColorSetARGB", &SkColorSetARGB, "a"_a, "r"_a, "g"_a, "b"_a);
    m.def(
        "ColorSetRGB", [](U8CPU r, U8CPU g, U8CPU b) { return SkColorSetRGB(r, g, b); }, "r"_a, "g"_a, "b"_a);
    m.def(
        "ColorGetA", [](SkColor color) { return SkColorGetA(color); }, "color"_a);
    m.def(
        "ColorGetR", [](SkColor color) { return SkColorGetR(color); }, "color"_a);
    m.def(
        "ColorGetG", [](SkColor color) { return SkColorGetG(color); }, "color"_a);
    m.def(
        "ColorGetB", [](SkColor color) { return SkColorGetB(color); }, "color"_a);

    m.def("ColorSetA", &SkColorSetA, "c"_a, "a"_a);
    m.attr("AlphaTRANSPARENT") = SK_AlphaTRANSPARENT;
    m.attr("AlphaOPAQUE") = SK_AlphaOPAQUE;
    m.attr("ColorTRANSPARENT") = SK_ColorTRANSPARENT;
    m.attr("ColorBLACK") = SK_ColorBLACK;
    m.attr("ColorDKGRAY") = SK_ColorDKGRAY;
    m.attr("ColorGRAY") = SK_ColorGRAY;
    m.attr("ColorLTGRAY") = SK_ColorLTGRAY;
    m.attr("ColorWHITE") = SK_ColorWHITE;
    m.attr("ColorRED") = SK_ColorRED;
    m.attr("ColorGREEN") = SK_ColorGREEN;
    m.attr("ColorBLUE") = SK_ColorBLUE;
    m.attr("ColorYELLOW") = SK_ColorYELLOW;
    m.attr("ColorCYAN") = SK_ColorCYAN;
    m.attr("ColorMAGENTA") = SK_ColorMAGENTA;

    m.def(
        "RGBToHSV",
        [](U8CPU red, U8CPU green, U8CPU blue)
        {
            std::vector<SkScalar> hsv(3);
            SkRGBToHSV(red, green, blue, hsv.data());
            return hsv;
        },
        R"doc(
            Converts RGB to its HSV components.

            :param int red: red component value from 0 to 255
            :param int green: green component value from 0 to 255
            :param int blue: blue component value from 0 to 255
            :return: three element array which holds the resulting HSV components. hsv[0] contains hsv hue, a value from
                0 to less than 360. hsv[1] contains hsv saturation, a value from 0 to 1. hsv[2] contains hsv value, a
                value from 0 to 1.
        )doc",
        "red"_a, "green"_a, "blue"_a);
    m.def(
        "ColorToHSV",
        [](SkColor color)
        {
            std::vector<SkScalar> hsv(3);
            SkColorToHSV(color, hsv.data());
            return hsv;
        },
        R"doc(
            Converts ARGB color to its HSV components. Alpha in ARGB is ignored.

            :param color: ARGB color to convert
            :return: three element array which holds the resulting HSV components. hsv[0] contains hsv hue, a value from
                0 to less than 360. hsv[1] contains hsv saturation, a value from 0 to 1. hsv[2] contains hsv value, a
                value from 0 to 1.
        )doc",
        py::arg("color"));
    m.def(
        "HSVToColor",
        [](const std::vector<SkScalar> &hsv, U8CPU alpha)
        {
            if (hsv.size() != 3)
                throw py::value_error("hsv must be 3 element array");
            return SkHSVToColor(alpha, hsv.data());
        },
        R"doc(
            Converts HSV components to an ARGB color. Alpha is passed through unchanged.

            :param hsv: three element array which holds the input HSV components. hsv[0] represents hsv hue, an angle
                from 0 to less than 360. hsv[1] represents hsv saturation, and varies from 0 to 1. hsv[2] represents hsv
                value, and varies from 0 to 1.
            :param alpha: alpha component of the returned ARGB color
            :return: ARGB equivalent to HSV
        )doc",
        "hsv"_a, "alpha"_a = 255);

    m.def("PreMultiplyARGB", &SkPreMultiplyARGB, "a"_a, "r"_a, "g"_a, "b"_a);
    m.def("PreMultiplyColor", &SkPreMultiplyColor, "c"_a);

    py::enum_<SkColorChannel>(m, "ColorChannel")
        .value("kR", SkColorChannel::kR)
        .value("kG", SkColorChannel::kG)
        .value("kB", SkColorChannel::kB)
        .value("kA", SkColorChannel::kA)
        .value("kLastEnum", SkColorChannel::kLastEnum);

    py::enum_<SkColorChannelFlag>(m, "ColorChannelFlag", py::arithmetic())
        .value("kRed_ColorChannelFlag", SkColorChannelFlag::kRed_SkColorChannelFlag)
        .value("kGreen_ColorChannelFlag", SkColorChannelFlag::kGreen_SkColorChannelFlag)
        .value("kBlue_ColorChannelFlag", SkColorChannelFlag::kBlue_SkColorChannelFlag)
        .value("kAlpha_ColorChannelFlag", SkColorChannelFlag::kAlpha_SkColorChannelFlag)
        .value("kGray_ColorChannelFlag", SkColorChannelFlag::kGray_SkColorChannelFlag)
        .value("kGrayAlpha_ColorChannelFlags", SkColorChannelFlag::kGrayAlpha_SkColorChannelFlags)
        .value("kRG_ColorChannelFlags", SkColorChannelFlag::kRG_SkColorChannelFlags)
        .value("kRGB_ColorChannelFlags", SkColorChannelFlag::kRGB_SkColorChannelFlags)
        .value("kRGBA_ColorChannelFlags", SkColorChannelFlag::kRGBA_SkColorChannelFlags);

    py::class_<SkColor4f>(m, "Color4f")
        .def(py::init(&SkColor4f::FromColor),
             R"doc(
                Create a new :py:class:`Color4f` from an ARGB color.

                :param color: ARGB color to convert
            )doc",
             "color"_a)
        .def(py::init(
                 [](float r, float g, float b, float a)
                 {
                     SkColor4f color4f = {r, g, b, a};
                     return color4f;
                 }),
             R"doc(
                Create a new Color4f instance initialized with the given values.

                :red: red components
                :green: green components
                :blue: blue components
                :alpha: alpha components
            )doc",
             "red"_a, "green"_a, "blue"_a, "alpha"_a = 1.0f)
        .def(py::init(
                 [](const py::tuple &tuple)
                 {
                     SkColor4f color4f = {0, 0, 0, 1};
                     const size_t size = tuple.size();
                     if (size == 3 || size == 4)
                         for (size_t i = 0; i < size; ++i)
                             color4f[i] = tuple[i].cast<float>();
                     else
                         throw py::value_error("tuple must have 3 or 4 elements");
                     return color4f;
                 }),
             R"doc(
                Create a new Color4f instance given (R, G, B) or (R, G, B, A) tuple.

                :param t: tuple of color components
            )doc",
             "t"_a)
        .def_readwrite("fR", &SkColor4f::fR)
        .def_readwrite("fG", &SkColor4f::fG)
        .def_readwrite("fB", &SkColor4f::fB)
        .def_readwrite("fA", &SkColor4f::fA)
        .def(py::self == py::self, "other"_a)
        .def(py::self != py::self, "other"_a)
        .def(py::self * float(), "scale"_a)
        .def(py::self * py::self, "scale"_a)
        .def("vec",
             [](SkColor4f &color4f)
             {
                 return py::memoryview::from_buffer(color4f.vec(), sizeof(float), py::format_descriptor<float>::value,
                                                    {4}, {sizeof(float)}, false);
             })
        .def(
            "array",
            [](SkColor4f &color4f)
            { return py::array_t<float>({4}, {sizeof(float)}, color4f.vec(), py::capsule([]() {})); },
            R"doc(
                Return a numpy array of the color components. Changes to the array will be reflected in the color.

                :return: numpy array of the color components
            )doc",
            py::keep_alive<0, 1>())
        .def(
            "__getitem__",
            [](const SkColor4f &c, int index)
            {
                if (index < 0 || index >= 4)
                    throw py::index_error("Index out of range.");
                return c[index];
            },
            "index"_a)
        .def(
            "__setitem__",
            [](SkColor4f &c, int index, float value)
            {
                if (index < 0 || index >= 4)
                    throw py::index_error("Index out of range.");
                c[index] = value;
            },
            "index"_a, "value"_a)
        .def("isOpaque", &SkColor4f::isOpaque)
        .def("fitsInBytes", &SkColor4f::fitsInBytes)
        .def_static("FromColor", &SkColor4f::FromColor, "color"_a)
        .def("toColor", &SkColor4f::toSkColor)
        .def_static("FromPMColor", &SkColor4f::FromColor, "pmcolor"_a)
        .def("premul", &SkColor4f::premul)
        .def("toBytes_RGBA", &SkColor4f::toBytes_RGBA)
        .def_static("FromBytes_RGBA", &SkColor4f::FromBytes_RGBA, "color"_a)
        .def("makeOpaque", &SkColor4f::makeOpaque)
        .def("__int__", &SkColor4f::toSkColor, R"doc(
                Convert the color to an integer (ARGB color).

                :return: ARGB color
            )doc")
        .def("__len__", [](const SkColor4f &) { return 4; })
        .def("__str__",
             [](const SkColor4f &color4f)
             {
                 std::stringstream s;
                 s << "Color4f(" << color4f.fR << ", " << color4f.fG << ", " << color4f.fB << ", " << color4f.fA << ")";
                 return s.str();
             })
        .def_readonly_static("kTransparent", &SkColors::kTransparent)
        .def_readonly_static("kBlack", &SkColors::kBlack)
        .def_readonly_static("kDkGray", &SkColors::kDkGray)
        .def_readonly_static("kGray", &SkColors::kGray)
        .def_readonly_static("kLtGray", &SkColors::kLtGray)
        .def_readonly_static("kWhite", &SkColors::kWhite)
        .def_readonly_static("kRed", &SkColors::kRed)
        .def_readonly_static("kGreen", &SkColors::kGreen)
        .def_readonly_static("kBlue", &SkColors::kBlue)
        .def_readonly_static("kYellow", &SkColors::kYellow)
        .def_readonly_static("kCyan", &SkColors::kCyan)
        .def_readonly_static("kMagenta", &SkColors::kMagenta);

    py::implicitly_convertible<py::tuple, SkColor4f>();
    py::implicitly_convertible<SkColor, SkColor4f>();
}