#include "common.h"
#include "include/core/SkBlender.h"
#include "include/core/SkColorFilter.h"
#include "include/core/SkColorSpace.h"
#include "include/core/SkImageFilter.h"
#include "include/core/SkMaskFilter.h"
#include "include/core/SkPaint.h"
#include "include/core/SkPathEffect.h"
#include "include/core/SkShader.h"
#include <pybind11/operators.h>
#include <pybind11/stl.h>

void initPaint(py::module &m)
{
    py::class_<SkPaint> Paint(m, "Paint");
    Paint.def(py::init())
        .def(py::init<const SkColor4f &, SkColorSpace *>(), "color"_a, "colorSpace"_a = nullptr)
        .def(py::init<const SkPaint &>(), "paint"_a)
        .def(py::init(
                 [](const py::kwargs &kwargs)
                 {
                     SkPaint paint;
                     for (auto item : kwargs)
                     {
                         std::string key(py::str(item.first));
                         auto value = item.second;
                         if (key == "antiAlias")
                             paint.setAntiAlias(value.cast<bool>());
                         else if (key == "dither")
                             paint.setDither(value.cast<bool>());
                         else if (key == "style")
                             paint.setStyle(value.cast<SkPaint::Style>());
                         else if (key == "stroke")
                             paint.setStroke(value.cast<bool>());
                         else if (key == "color")
                             paint.setColor(value.cast<SkColor>());
                         else if (key == "color4f")
                             paint.setColor4f(value.cast<SkColor4f>());
                         else if (key == "alphaf")
                             paint.setAlphaf(value.cast<float>());
                         else if (key == "alpha")
                             paint.setAlpha(value.cast<U8CPU>());
                         else if (key == "argb")
                         {
                             py::tuple t = value.cast<py::tuple>();
                             if (t.size() != 4)
                                 throw py::value_error("argb must be 4-element tuple.");
                             paint.setARGB(t[0].cast<U8CPU>(), t[1].cast<U8CPU>(), t[2].cast<U8CPU>(),
                                           t[3].cast<U8CPU>());
                         }
                         else if (key == "strokeWidth")
                             paint.setStrokeWidth(value.cast<SkScalar>());
                         else if (key == "strokeMiter")
                             paint.setStrokeMiter(value.cast<SkScalar>());
                         else if (key == "strokeCap")
                             paint.setStrokeCap(value.cast<SkPaint::Cap>());
                         else if (key == "strokeJoin")
                             paint.setStrokeJoin(value.cast<SkPaint::Join>());
                         else if (key == "shader")
                             paint.setShader(value.cast<sk_sp<SkShader>>());
                         else if (key == "colorFilter")
                             paint.setColorFilter(value.cast<sk_sp<SkColorFilter>>());
                         else if (key == "blendMode")
                             paint.setBlendMode(value.cast<SkBlendMode>());
                         else if (key == "blender")
                             paint.setBlender(value.cast<sk_sp<SkBlender>>());
                         else if (key == "pathEffect")
                             paint.setPathEffect(value.cast<sk_sp<SkPathEffect>>());
                         else if (key == "maskFilter")
                             paint.setMaskFilter(value.cast<sk_sp<SkMaskFilter>>());
                         else if (key == "imageFilter")
                             paint.setImageFilter(value.cast<sk_sp<SkImageFilter>>());
                         else
                             throw py::key_error(key);
                     }
                     return paint;
                 }),
             R"doc(
                 Construct a new paint from keyword arguments. This creates a new :py:class:`Paint` object and calls the
                 respective setters for each keyword argument.

                 Supported keyword arguments: ``antiAlias``, ``dither``, ``style``, ``stroke``, ``color``, ``color4f``,
                ``alpha``, ``argb``, ``strokeWidth``, ``strokeMiter``, ``strokeCap``, ``strokeJoin``, ``shader``,
                ``colorFilter``, ``blendMode``, ``blender``, ``pathEffect``, ``maskFilter``, ``imageFilter``.

                :note: Later arguments override earlier ones.
            )doc")
        .def(py::self == py::self, "other"_a)
        .def(py::self != py::self, "other"_a)
        .def("reset", &SkPaint::reset)
        .def("isAntiAlias", &SkPaint::isAntiAlias)
        .def("setAntiAlias", &SkPaint::setAntiAlias, "aa"_a)
        .def("isDither", &SkPaint::isDither)
        .def("setDither", &SkPaint::setDither, "dither"_a);

    py::enum_<SkPaint::Style>(Paint, "Style")
        .value("kFill_Style", SkPaint::Style::kFill_Style)
        .value("kStroke_Style", SkPaint::Style::kStroke_Style)
        .value("kStrokeAndFill_Style", SkPaint::Style::kStrokeAndFill_Style);
    Paint.def_readonly_static("kStyleCount", &SkPaint::kStyleCount)
        .def("getStyle", &SkPaint::getStyle)
        .def("setStyle", &SkPaint::setStyle, "style"_a)
        .def("setStroke", &SkPaint::setStroke, "isStroke"_a)
        .def("getColor", &SkPaint::getColor)
        .def("getColor4f", &SkPaint::getColor4f)
        .def("setColor", py::overload_cast<SkColor>(&SkPaint::setColor), "color"_a)
        .def("setColor", py::overload_cast<const SkColor4f &, SkColorSpace *>(&SkPaint::setColor), "color"_a,
             "colorSpace"_a = nullptr)
        .def("setColor4f", &SkPaint::setColor4f, "color"_a, "colorSpace"_a = nullptr)
        .def("getAlphaf", &SkPaint::getAlphaf)
        .def("getAlpha", &SkPaint::getAlpha)
        .def("setAlphaf", &SkPaint::setAlphaf, "a"_a)
        .def("setAlpha", &SkPaint::setAlpha, "a"_a)
        .def("setARGB", &SkPaint::setARGB, "a"_a, "r"_a, "g"_a, "b"_a)
        .def("getStrokeWidth", &SkPaint::getStrokeWidth)
        .def("setStrokeWidth", &SkPaint::setStrokeWidth, "width"_a)
        .def("getStrokeMiter", &SkPaint::getStrokeMiter)
        .def("setStrokeMiter", &SkPaint::setStrokeMiter, "miter"_a);

    py::enum_<SkPaint::Cap>(Paint, "Cap")
        .value("kButt_Cap", SkPaint::Cap::kButt_Cap)
        .value("kRound_Cap", SkPaint::Cap::kRound_Cap)
        .value("kSquare_Cap", SkPaint::Cap::kSquare_Cap)
        .value("kLast_Cap", SkPaint::Cap::kLast_Cap)
        .value("kDefault_Cap", SkPaint::Cap::kDefault_Cap);
    Paint.def_readonly_static("kCapCount", &SkPaint::kCapCount);

    py::enum_<SkPaint::Join>(Paint, "Join")
        .value("kMiter_Join", SkPaint::Join::kMiter_Join)
        .value("kRound_Join", SkPaint::Join::kRound_Join)
        .value("kBevel_Join", SkPaint::Join::kBevel_Join)
        .value("kLast_Join", SkPaint::Join::kLast_Join)
        .value("kDefault_Join", SkPaint::Join::kDefault_Join);
    Paint.def_readonly_static("kJoinCount", &SkPaint::kJoinCount)
        .def("getStrokeCap", &SkPaint::getStrokeCap)
        .def("setStrokeCap", &SkPaint::setStrokeCap, "cap"_a)
        .def("getStrokeJoin", &SkPaint::getStrokeJoin)
        .def("setStrokeJoin", &SkPaint::setStrokeJoin, "join"_a)
        .def("getShader", &SkPaint::getShader, py::return_value_policy::reference_internal)
        .def("refShader", &SkPaint::refShader)
        .def("setShader", &SkPaint::setShader, "shader"_a)
        .def("getColorFilter", &SkPaint::getColorFilter, py::return_value_policy::reference_internal)
        .def("refColorFilter", &SkPaint::refColorFilter)
        .def("setColorFilter", &SkPaint::setColorFilter, "colorFilter"_a)
        .def("asBlendMode", &SkPaint::asBlendMode)
        .def("getBlendMode_or", &SkPaint::getBlendMode_or, "defaultMode"_a)
        .def("isSrcOver", &SkPaint::isSrcOver)
        .def("setBlendMode", &SkPaint::setBlendMode, "mode"_a)
        .def("getBlender", &SkPaint::getBlender, py::return_value_policy::reference_internal)
        .def("refBlender", &SkPaint::refBlender)
        .def("setBlender", &SkPaint::setBlender, "blender"_a)
        .def("getPathEffect", &SkPaint::getPathEffect, py::return_value_policy::reference_internal)
        .def("refPathEffect", &SkPaint::refPathEffect)
        .def("setPathEffect", &SkPaint::setPathEffect, "pathEffect"_a)
        .def("getMaskFilter", &SkPaint::getMaskFilter, py::return_value_policy::reference_internal)
        .def("refMaskFilter", &SkPaint::refMaskFilter)
        .def("setMaskFilter", &SkPaint::setMaskFilter, "maskFilter"_a)
        .def("getImageFilter", &SkPaint::getImageFilter, py::return_value_policy::reference_internal)
        .def("refImageFilter", &SkPaint::refImageFilter)
        .def("setImageFilter", &SkPaint::setImageFilter, "imageFilter"_a)
        .def("nothingToDraw", &SkPaint::nothingToDraw)
        .def(
            "__str__",
            [](const SkPaint &paint)
            {
                const std::optional<SkBlendMode> blendMode = paint.asBlendMode();
                return "Paint({}{}style={}, color4f={}, strokeWidth={:g}, strokeMiter={:g}, strokeCap={}, strokeJoin={}, shader={}, colorFilter={}, blender={}, pathEffect={}, maskFilter={}, imageFilter={})"_s
                    .format(paint.isAntiAlias() ? "antiAlias, " : "", paint.isDither() ? "Dither, " : "",
                            paint.getStyle(), paint.getColor4f(), paint.getStrokeWidth(), paint.getStrokeMiter(),
                            paint.getStrokeCap(), paint.getStrokeJoin(), paint.getShader(), paint.getColorFilter(),
                            blendMode ? "{}"_s.format(blendMode.value()) : "{}"_s.format(paint.getBlender()),
                            paint.getPathEffect(), paint.getMaskFilter(), paint.getImageFilter());
            });
}