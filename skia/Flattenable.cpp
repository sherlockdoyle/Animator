#include "common.h"
#include "include/core/SkBlender.h"
#include "include/core/SkColorFilter.h"
#include "include/core/SkData.h"
#include "include/core/SkDrawable.h"
#include "include/core/SkFlattenable.h"
#include "include/core/SkImageFilter.h"
#include "include/core/SkMaskFilter.h"
#include "include/core/SkPathEffect.h"
#include "include/core/SkShader.h"
#include <pybind11/stl.h>
#include <variant>

class PyFlattanable : public SkFlattenable
{
public:
    using SkFlattenable::SkFlattenable;
    Factory getFactory() const override { PYBIND11_OVERLOAD_PURE(Factory, SkFlattenable, getFactory); }
    const char *getTypeName() const override { PYBIND11_OVERLOAD_PURE(const char *, SkFlattenable, getTypeName); }
    Type getFlattenableType() const override { PYBIND11_OVERLOAD_PURE(Type, SkFlattenable, getFlattenableType); }
};

void initFlattenable(py::module &m)
{
    py::class_<SkFlattenable, PyFlattanable, sk_sp<SkFlattenable>> Flattenable(m, "Flattenable");

    py::enum_<SkFlattenable::Type>(Flattenable, "Type")
        .value("kColorFilter_Type", SkFlattenable::Type::kSkColorFilter_Type)
        .value("kBlender_Type", SkFlattenable::Type::kSkBlender_Type)
        .value("kDrawable_Type", SkFlattenable::Type::kSkDrawable_Type)
        .value("kDrawLooper_Type", SkFlattenable::Type::kSkDrawLooper_Type)
        .value("kImageFilter_Type", SkFlattenable::Type::kSkImageFilter_Type)
        .value("kMaskFilter_Type", SkFlattenable::Type::kSkMaskFilter_Type)
        .value("kPathEffect_Type", SkFlattenable::Type::kSkPathEffect_Type)
        .value("kShader_Type", SkFlattenable::Type::kSkShader_Type);

    Flattenable.def(py::init())
        .def("getTypeName", &SkFlattenable::getTypeName)
        .def("getFlattenableType", &SkFlattenable::getFlattenableType)
        .def("serialize", [](const SkFlattenable &self) { return self.serialize(nullptr); })
        .def_static(
            "Deserialize",
            [](const SkFlattenable::Type &type, const py::buffer &data)
            {
                py::buffer_info info = data.request();
                return SkFlattenable::Deserialize(type, info.ptr, info.size * info.itemsize);
            },
            "Deserialize a flattenable of the given *type* from a buffer *data*.", "type"_a, "data"_a)
        .def_static(
            "DeserializeAsType",
            [](const SkFlattenable::Type &type, const py::buffer &data)
                -> std::variant<sk_sp<SkColorFilter>, sk_sp<SkBlender>, sk_sp<SkDrawable>, sk_sp<SkImageFilter>,
                                sk_sp<SkMaskFilter>, sk_sp<SkPathEffect>, sk_sp<SkShader>>
            {
                py::buffer_info info = data.request();
                sk_sp<SkFlattenable> result = SkFlattenable::Deserialize(type, info.ptr, info.size * info.itemsize);
                if (!result)
                    throw py::value_error(
                        "Failed to deserialize. Hint: Maybe the type is wrong? Maybe it is {}."_s.format(
                            (char *)info.ptr + 4));
                switch (type)
                {
                case SkFlattenable::Type::kSkColorFilter_Type:
                    return sk_sp<SkColorFilter>(reinterpret_cast<SkColorFilter *>(result.release()));
                case SkFlattenable::Type::kSkBlender_Type:
                    return sk_sp<SkBlender>(reinterpret_cast<SkBlender *>(result.release()));
                case SkFlattenable::Type::kSkDrawable_Type:
                    return sk_sp<SkDrawable>(reinterpret_cast<SkDrawable *>(result.release()));
                case SkFlattenable::Type::kSkDrawLooper_Type:
                    throw py::type_error("DrawLooper is unsupported");
                case SkFlattenable::Type::kSkImageFilter_Type:
                    return sk_sp<SkImageFilter>(reinterpret_cast<SkImageFilter *>(result.release()));
                case SkFlattenable::Type::kSkMaskFilter_Type:
                    return sk_sp<SkMaskFilter>(reinterpret_cast<SkMaskFilter *>(result.release()));
                case SkFlattenable::Type::kSkPathEffect_Type:
                    return sk_sp<SkPathEffect>(reinterpret_cast<SkPathEffect *>(result.release()));
                case SkFlattenable::Type::kSkShader_Type:
                    return sk_sp<SkShader>(reinterpret_cast<SkShader *>(result.release()));
                }
            },
            "Deserialize a flattenable of the given *type* from a buffer *data*. The return value is correctly typed.",
            "type"_a, "data"_a)
        .def("__str__", [](const SkFlattenable &self)
             { return "{}({})"_s.format(self.getTypeName(), self.getFlattenableType()); });
}