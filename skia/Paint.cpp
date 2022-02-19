#include "common.h"
#include "include/core/SkBlender.h"
#include "include/core/SkColorFilter.h"
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
        .def(py::init<const SkColor4f &, SkColorSpace *>(), "color"_a, "colorSpace"_a)
        .def(py::init<const SkPaint &>(), "paint"_a)
        .def(py::init(
                 [](const py::kwargs &kwargs)
                 {
                     SkPaint paint;
                     for (auto item : kwargs)
                     {
                         std::string key(py::str(item.first));
                         auto value = item.second;
                         if (key == "AntiAlias")
                             paint.setAntiAlias(value.cast<bool>());
                         else if (key == "Dither")
                             paint.setDither(value.cast<bool>());
                         else if (key == "Style")
                             paint.setStyle(value.cast<SkPaint::Style>());
                         else if (key == "Stroke")
                             paint.setStroke(value.cast<bool>());
                         else if (key == "Color")
                             paint.setColor(value.cast<SkColor>());
                         else if (key == "Color4f")
                             paint.setColor4f(value.cast<SkColor4f>());
                         else if (key == "Alphaf")
                             paint.setAlphaf(value.cast<float>());
                         else if (key == "Alpha")
                             paint.setAlpha(value.cast<U8CPU>());
                         else if (key == "ARGB")
                         {
                             py::tuple t = value.cast<py::tuple>();
                             if (t.size() != 4)
                                 throw py::value_error("ARGB must be 4-element tuple.");
                             paint.setARGB(t[0].cast<U8CPU>(), t[1].cast<U8CPU>(), t[2].cast<U8CPU>(),
                                           t[3].cast<U8CPU>());
                         }
                         else if (key == "StrokeWidth")
                             paint.setStrokeWidth(value.cast<SkScalar>());
                         else if (key == "StrokeMiter")
                             paint.setStrokeMiter(value.cast<SkScalar>());
                         else if (key == "StrokeCap")
                             paint.setStrokeCap(value.cast<SkPaint::Cap>());
                         else if (key == "StrokeJoin")
                             paint.setStrokeJoin(value.cast<SkPaint::Join>());
                         else if (key == "Shader")
                             paint.setShader(value.cast<sk_sp<SkShader>>());
                         else if (key == "ColorFilter")
                             paint.setColorFilter(value.cast<sk_sp<SkColorFilter>>());
                         else if (key == "BlendMode")
                             paint.setBlendMode(value.cast<SkBlendMode>());
                         else if (key == "Blender")
                             paint.setBlender(value.cast<sk_sp<SkBlender>>());
                         else if (key == "PathEffect")
                             paint.setPathEffect(value.cast<sk_sp<SkPathEffect>>());
                         else if (key == "MaskFilter")
                             paint.setMaskFilter(value.cast<sk_sp<SkMaskFilter>>());
                         else if (key == "ImageFilter")
                             paint.setImageFilter(value.cast<sk_sp<SkImageFilter>>());
                         else
                             throw py::key_error(key);
                     }
                     return paint;
                 }),
             R"doc(
                 Construct a new paint from a dict of keyword arguments. This creates a new :py:class:`Paint` object and
                 calls the respective setters for each keyword argument.

                 Supported keyword arguments: ``AntiAlias``, ``Dither``, ``Style``, ``Stroke``, ``Color``, ``Color4f``,
                ``Alpha``, ``ARGB``, ``StrokeWidth``, ``StrokeMiter``, ``StrokeCap``, ``StrokeJoin``, ``Shader``,
                ``ColorFilter``, ``BlendMode``, ``Blender``, ``PathEffect``, ``MaskFilter``, ``ImageFilter``.

                :note: Later setters override earlier ones.
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
             "colorSpace"_a)
        .def("setColor4f", &SkPaint::setColor4f, "color"_a, "colorSpace"_a)
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
        .def(
            "getFillPath",
            [](const SkPaint &paint, const SkPath &src, const SkRect *cullRect, const SkScalar &resScale)
            {
                SkPath dst;
                bool isFill = paint.getFillPath(src, &dst, cullRect, resScale);
                return py::make_tuple(dst, isFill);
            },
            R"doc(
                Returns the filled equivalent of the stroked path.

                :param src: :py:class:`Path` to create a filled version
                :param cullRect: optional limit passed to :py:class:`PathEffect`
                :param resScale: if > 1, increase precision, else if (0 < resScale < 1) reduce precision to favor speed
                    and size
                :return: a tuple of (:py:class:`Path`, bool) where the bool indicates whether the path represents style
                    fill or hairline (true for fill, false for hairline)
            )doc",
            "src"_a, "cullRect"_a = py::none(), "resScale"_a = 1)
        .def(
            "getFillPath",
            [](const SkPaint &paint, const SkPath &src, const SkRect *cullRect, const SkMatrix &ctm)
            {
                SkPath dst;
                bool isFill = paint.getFillPath(src, &dst, cullRect, ctm);
                return py::make_tuple(dst, isFill);
            },
            "Returns the filled equivalent of the stroked path.", "src"_a, "cullRect"_a, "ctm"_a)
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
                const skstd::optional<SkBlendMode> blendMode = paint.asBlendMode();
                return "Paint({}{}Style={}, Color4f={}, StrokeWidth={:g}, StrokeMiter={:g}, StrokeCap={}, StrokeJoin={}, Shader={}, ColorFilter={}, Blender={}, PathEffect={}, MaskFilter={}, ImageFilter={})"_s
                    .format(paint.isAntiAlias() ? "AntiAlias, " : "", paint.isDither() ? "Dither, " : "",
                            paint.getStyle(), paint.getColor4f(), paint.getStrokeWidth(), paint.getStrokeMiter(),
                            paint.getStrokeCap(), paint.getStrokeJoin(), paint.getShader(), paint.getColorFilter(),
                            blendMode ? "{}"_s.format(blendMode.value()) : "{}"_s.format(paint.getBlender()),
                            paint.getPathEffect(), paint.getMaskFilter(), paint.getImageFilter());
            });
}