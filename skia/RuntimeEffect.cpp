#define SK_ENABLE_SKSL
#include "common.h"
#include "include/core/SkImage.h"
#include "include/core/SkStream.h"
#include "include/effects/SkRuntimeEffect.h"
#include <pybind11/stl.h>

static constexpr SkRuntimeEffect::Options dopts;

static void BuilderUniform_throwIfUnequal(const size_t &size, const size_t &count)
{
    if (size != count)
        throw py::value_error("Uniform contains {} elements, but {} elements were provided"_s.format(count, size));
}

void initRuntimeEffect(py::module &m)
{
    py::class_<SkSL::DebugTrace, sk_sp<SkSL::DebugTrace>>(m.def_submodule("sksl"), "DebugTrace")
        .def(
            "writeTrace",
            [](const SkSL::DebugTrace &self)
            {
                SkDynamicMemoryWStream w;
                self.writeTrace(&w);
                sk_sp<SkData> data = w.detachAsData();
                return py::str((char *)data->data(), data->size());
            },
            "Returns serialized debug trace in JSON format")
        .def(
            "dump",
            [](const SkSL::DebugTrace &self)
            {
                SkDynamicMemoryWStream w;
                self.dump(&w);
                sk_sp<SkData> data = w.detachAsData();
                return py::str((char *)data->data(), data->size());
            },
            "Returns human-readable dump of the debug trace");

    py::class_<SkRuntimeEffect, sk_sp<SkRuntimeEffect>> RuntimeEffect(m, "RuntimeEffect");

    py::class_<SkRuntimeEffect::Uniform> Uniform(RuntimeEffect, "Uniform");

    py::enum_<SkRuntimeEffect::Uniform::Type>(Uniform, "Type")
        .value("kFloat", SkRuntimeEffect::Uniform::Type::kFloat)
        .value("kFloat2", SkRuntimeEffect::Uniform::Type::kFloat2)
        .value("kFloat3", SkRuntimeEffect::Uniform::Type::kFloat3)
        .value("kFloat4", SkRuntimeEffect::Uniform::Type::kFloat4)
        .value("kFloat2x2", SkRuntimeEffect::Uniform::Type::kFloat2x2)
        .value("kFloat3x3", SkRuntimeEffect::Uniform::Type::kFloat3x3)
        .value("kFloat4x4", SkRuntimeEffect::Uniform::Type::kFloat4x4)
        .value("kInt", SkRuntimeEffect::Uniform::Type::kInt)
        .value("kInt2", SkRuntimeEffect::Uniform::Type::kInt2)
        .value("kInt3", SkRuntimeEffect::Uniform::Type::kInt3)
        .value("kInt4", SkRuntimeEffect::Uniform::Type::kInt4);

    py::enum_<SkRuntimeEffect::Uniform::Flags>(Uniform, "Flags", py::arithmetic())
        .value("kArray_Flag", SkRuntimeEffect::Uniform::Flags::kArray_Flag)
        .value("kColor_Flag", SkRuntimeEffect::Uniform::Flags::kColor_Flag)
        .value("kVertex_Flag", SkRuntimeEffect::Uniform::Flags::kVertex_Flag)
        .value("kFragment_Flag", SkRuntimeEffect::Uniform::Flags::kFragment_Flag)
        .value("kHalfPrecision_Flag", SkRuntimeEffect::Uniform::Flags::kHalfPrecision_Flag);

    Uniform.def_readonly("name", &SkRuntimeEffect::Uniform::name)
        .def_readonly("offset", &SkRuntimeEffect::Uniform::offset)
        .def_readonly("type", &SkRuntimeEffect::Uniform::type)
        .def_readonly("count", &SkRuntimeEffect::Uniform::count)
        .def_readonly("flags", &SkRuntimeEffect::Uniform::flags)
        .def("isArray", &SkRuntimeEffect::Uniform::isArray)
        .def("isColor", &SkRuntimeEffect::Uniform::isColor)
        .def("sizeInBytes", &SkRuntimeEffect::Uniform::sizeInBytes)
        .def("__str__",
             [](const SkRuntimeEffect::Uniform &self)
             {
                 return "Uniform('{}', type={}{}{}{}{}{})"_s.format(
                     self.name, self.type, self.flags & SkRuntimeEffect::Uniform::Flags::kColor_Flag ? ", color" : "",
                     self.flags & SkRuntimeEffect::Uniform::Flags::kArray_Flag ? ", array[{}]"_s.format(self.count)
                                                                               : "",
                     self.flags & SkRuntimeEffect::Uniform::Flags::kVertex_Flag ? ", vertex" : "",
                     self.flags & SkRuntimeEffect::Uniform::Flags::kFragment_Flag ? ", fragment" : "",
                     self.flags & SkRuntimeEffect::Uniform::Flags::kHalfPrecision_Flag ? ", half" : "");
             });

    py::enum_<SkRuntimeEffect::ChildType>(RuntimeEffect, "ChildType")
        .value("kShader", SkRuntimeEffect::ChildType::kShader)
        .value("kColorFilter", SkRuntimeEffect::ChildType::kColorFilter)
        .value("kBlender", SkRuntimeEffect::ChildType::kBlender);

    py::class_<SkRuntimeEffect::Child>(RuntimeEffect, "Child")
        .def_readonly("name", &SkRuntimeEffect::Child::name)
        .def_readonly("type", &SkRuntimeEffect::Child::type)
        .def_readonly("index", &SkRuntimeEffect::Child::index)
        .def("__str__",
             [](const SkRuntimeEffect::Child &self) { return "Child('{}', type={})"_s.format(self.name, self.type); });

    py::class_<SkRuntimeEffect::Options>(RuntimeEffect, "Options")
        .def(py::init(
                 [](const bool &forceUnoptimized)
                 {
                     SkRuntimeEffect::Options self;
                     self.forceUnoptimized = forceUnoptimized;
                     return self;
                 }),
             "forceUnoptimized"_a = false)
        .def("__str__", [](const SkRuntimeEffect::Options &self)
             { return "Options({})"_s.format(self.forceUnoptimized ? "forceUnoptimized" : ""); });

    py::class_<SkRuntimeEffect::Result>(RuntimeEffect, "Result")
        .def_readonly("effect", &SkRuntimeEffect::Result::effect)
        .def_property_readonly("errorText", [](const SkRuntimeEffect::Result &self)
                               { return py::str(self.errorText.c_str(), self.errorText.size()); })
        .def("__str__",
             [](const SkRuntimeEffect::Result &self)
             {
                 if (self.effect)
                     return "Result({})"_s.format(self.effect);
                 return "Result(error=\"{}\")"_s.format(self.errorText.c_str());
             });
    RuntimeEffect
        .def_static(
            "MakeForColorFilter",
            [](const std::string &sksl, const SkRuntimeEffect::Options &options)
            { return SkRuntimeEffect::MakeForColorFilter(SkString(sksl), options); },
            "sksl"_a, "options"_a = dopts)
        .def_static(
            "MakeForShader",
            [](const std::string &sksl, const SkRuntimeEffect::Options &options)
            { return SkRuntimeEffect::MakeForShader(SkString(sksl), options); },
            "sksl"_a, "options"_a = dopts)
        .def_static(
            "MakeForBlender",
            [](const std::string &sksl, const SkRuntimeEffect::Options &options)
            { return SkRuntimeEffect::MakeForBlender(SkString(sksl), options); },
            "sksl"_a, "options"_a = dopts);

    py::class_<SkRuntimeEffect::ChildPtr>(RuntimeEffect, "ChildPtr")
        .def(py::init())
        .def(py::init<sk_sp<SkShader>>(), "s"_a)
        .def(py::init<sk_sp<SkColorFilter>>(), "cf"_a)
        .def(py::init<sk_sp<SkBlender>>(), "b"_a)
        .def("type", &SkRuntimeEffect::ChildPtr::type)
        .def("shader", &SkRuntimeEffect::ChildPtr::shader, py::return_value_policy::reference_internal)
        .def("colorFilter", &SkRuntimeEffect::ChildPtr::colorFilter, py::return_value_policy::reference_internal)
        .def("blender", &SkRuntimeEffect::ChildPtr::blender, py::return_value_policy::reference_internal)
        .def("flattenable", &SkRuntimeEffect::ChildPtr::flattenable, py::return_value_policy::reference_internal)
        .def("__str__", [](const SkRuntimeEffect::ChildPtr &self) { return "ChildPtr({})"_s.format(self.type()); });

    py::implicitly_convertible<sk_sp<SkShader>, SkRuntimeEffect::ChildPtr>();
    py::implicitly_convertible<sk_sp<SkColorFilter>, SkRuntimeEffect::ChildPtr>();
    py::implicitly_convertible<sk_sp<SkBlender>, SkRuntimeEffect::ChildPtr>();

    RuntimeEffect
        .def(
            "makeShader",
            [](const SkRuntimeEffect &self, const sk_sp<const SkData> &uniforms, std::vector<sk_sp<SkShader>> &children,
               const SkMatrix *localMatrix)
            { return self.makeShader(uniforms, children.data(), children.size(), localMatrix); },
            "Create a shader from this effect with the given *uniforms* and *children*.", "uniforms"_a, "children"_a,
            "localMatrix"_a = nullptr)
        .def(
            "makeShader",
            [](const SkRuntimeEffect &self, const sk_sp<const SkData> &uniforms,
               std::vector<SkRuntimeEffect::ChildPtr> &children, const SkMatrix *localMatrix)
            { return self.makeShader(uniforms, SkSpan(children.data(), children.size()), localMatrix); },
            "Create a shader from this effect with the given *uniforms* and *children*.", "uniforms"_a, "children"_a,
            "localMatrix"_a = nullptr)
        .def("makeColorFilter", py::overload_cast<sk_sp<const SkData>>(&SkRuntimeEffect::makeColorFilter, py::const_),
             "uniforms"_a)
        .def(
            "makeColorFilter",
            [](const SkRuntimeEffect &self, const sk_sp<const SkData> &uniforms,
               std::vector<sk_sp<SkColorFilter>> &children)
            { return self.makeColorFilter(uniforms, children.data(), children.size()); },
            "Create a color filter from this effect with the given *uniforms* and *children*.", "uniforms"_a,
            "children"_a)
        .def(
            "makeColorFilter",
            [](const SkRuntimeEffect &self, const sk_sp<const SkData> &uniforms,
               std::vector<SkRuntimeEffect::ChildPtr> &children)
            { return self.makeColorFilter(uniforms, SkSpan(children.data(), children.size())); },
            "Create a color filter from this effect with the given *uniforms* and *children*.", "uniforms"_a,
            "children"_a)
        .def(
            "makeBlender",
            [](const SkRuntimeEffect &self, const sk_sp<const SkData> &uniforms,
               std::vector<SkRuntimeEffect::ChildPtr> &children)
            { return self.makeBlender(uniforms, SkSpan(children.data(), children.size())); },
            "Create a blender from this effect with the given *uniforms* and *children*.", "uniforms"_a,
            "children"_a = std::vector<SkRuntimeEffect::ChildPtr>{});

    py::class_<SkRuntimeEffect::TracedShader>(RuntimeEffect, "TracedShader")
        .def_readonly("shader", &SkRuntimeEffect::TracedShader::shader)
        .def_readonly("debugTrace", &SkRuntimeEffect::TracedShader::debugTrace);
    RuntimeEffect.def_static("MakeTraced", &SkRuntimeEffect::MakeTraced, "shader"_a, "traceCoord"_a)
        .def("source", &SkRuntimeEffect::source)
        .def("uniformSize", &SkRuntimeEffect::uniformSize)
        .def("uniforms",
             [](const SkRuntimeEffect &self)
             {
                 const SkSpan<const SkRuntimeEffect::Uniform> uniforms = self.uniforms();
                 return std::vector<SkRuntimeEffect::Uniform>(uniforms.begin(), uniforms.end());
             })
        .def("children",
             [](const SkRuntimeEffect &self)
             {
                 const SkSpan<const SkRuntimeEffect::Child> children = self.children();
                 return std::vector<SkRuntimeEffect::Child>(children.begin(), children.end());
             })
        .def("findUniform", &SkRuntimeEffect::findUniform, "name"_a, py::return_value_policy::reference_internal)
        .def("findChild", &SkRuntimeEffect::findChild, "name"_a, py::return_value_policy::reference_internal)
        .def("allowShader", &SkRuntimeEffect::allowShader)
        .def("allowColorFilter", &SkRuntimeEffect::allowColorFilter)
        .def("allowBlender", &SkRuntimeEffect::allowBlender)
        .def("__str__",
             [](const SkRuntimeEffect &self)
             {
                 std::stringstream s;
                 std::string source = self.source();
                 source.erase(source.begin(), std::find_if(source.begin(), source.end(),
                                                           std::not1(std::ptr_fun<int, int>(std::isspace))));
                 source.erase(
                     std::find_if(source.rbegin(), source.rend(), std::not1(std::ptr_fun<int, int>(std::isspace)))
                         .base(),
                     source.end());
                 const size_t pos = source.find('\n');
                 s << "RuntimeEffect(\"" << source.substr(0, pos) << "\"";
                 if (pos != std::string::npos)
                     s << "...";
                 const size_t numUniforms = self.uniforms().size(), numChildren = self.children().size();
                 if (numUniforms)
                 {
                     s << ", " << numUniforms << " uniform";
                     if (numUniforms > 1)
                         s << "s";
                 }
                 if (numChildren)
                 {
                     s << ", " << numChildren << " child";
                     if (numChildren > 1)
                         s << "ren";
                 }
                 s << ")";
                 return s.str();
             });

    py::class_<SkRuntimeEffectBuilder> RuntimeEffectBuilder(m, "RuntimeEffectBuilder");

    py::class_<SkRuntimeEffectBuilder::BuilderUniform>(RuntimeEffectBuilder, "BuilderUniform")
        .def(
            "set",
            [](SkRuntimeEffectBuilder::BuilderUniform &self, const SkMatrix &val)
            {
                const size_t count = self.fVar->sizeInBytes() / 4;
                if (count != 9)
                    throw py::value_error("Uniform contains {} element{}. Call set() with a{} array instead."_s.format(
                        count, count == 1 ? "" : "s", count == 1 ? " scalar or" : "n"));
                switch (self.fVar->type)
                {
                case SkRuntimeEffect::Uniform::Type::kInt:
                case SkRuntimeEffect::Uniform::Type::kInt2:
                case SkRuntimeEffect::Uniform::Type::kInt3:
                case SkRuntimeEffect::Uniform::Type::kInt4:
                    throw py::type_error(
                        "Uniform is of type int, but set() was called with a matrix which contains floats.");
                default:
                    self = val;
                }
            },
            "Set the matrix uniform to the given *val*.", "val"_a)
        .def(
            "set",
            [](SkRuntimeEffectBuilder::BuilderUniform &self, const std::variant<int, float> &val)
            {
                const size_t count = self.fVar->sizeInBytes() / 4;
                if (count != 1)
                    throw py::value_error(
                        "Uniform contains {} elements. Call set() with an array instead."_s.format(count));
                switch (self.fVar->type)
                {
                case SkRuntimeEffect::Uniform::Type::kInt:
                    try
                    {
                        self.set(&std::get<int>(val), 1);
                    }
                    catch (const std::bad_variant_access &)
                    {
                        throw py::type_error("Uniform is of type int, but set() was called with a float.");
                    }
                    break;
                case SkRuntimeEffect::Uniform::Type::kFloat:
                    try
                    {
                        self.set(&std::get<float>(val), 1);
                    }
                    catch (const std::bad_variant_access &)
                    {
                        const float v = std::get<int>(val);
                        self.set(&v, 1);
                    }
                    break;
                default:
                    throw std::logic_error("Did a cosmic ray strike? Report this if this persists.");
                }
            },
            "Set the uniform with a single value to the given *val*. *val* is automatically type-cast.", "val"_a)
        .def(
            "set",
            [](SkRuntimeEffectBuilder::BuilderUniform &self,
               const std::variant<std::vector<int>, std::vector<float>> &val)
            {
                const size_t count = self.fVar->sizeInBytes() / 4;
                switch (self.fVar->type)
                {
                case SkRuntimeEffect::Uniform::Type::kInt:
                case SkRuntimeEffect::Uniform::Type::kInt2:
                case SkRuntimeEffect::Uniform::Type::kInt3:
                case SkRuntimeEffect::Uniform::Type::kInt4:
                    try
                    {
                        const std::vector<int> &v = std::get<std::vector<int>>(val);
                        BuilderUniform_throwIfUnequal(v.size(), count);
                        self.set(v.data(), count);
                    }
                    catch (const std::bad_variant_access &)
                    {
                        throw py::type_error("Uniform is of type int, but set() was called with a float.");
                    }
                    break;
                default: // float
                    try
                    {
                        const std::vector<float> &v = std::get<std::vector<float>>(val);
                        BuilderUniform_throwIfUnequal(v.size(), count);
                        self.set(v.data(), count);
                    }
                    catch (const std::bad_variant_access &)
                    {
                        const std::vector<int> &iv = std::get<std::vector<int>>(val);
                        BuilderUniform_throwIfUnequal(iv.size(), count);
                        const std::vector<float> v(iv.begin(), iv.end());
                        self.set(v.data(), count);
                    }
                }
            },
            "Set the uniform with an array of values to the given *val*. *val* is automatically type-cast.", "val"_a)
        .def("__str__", [](const SkRuntimeEffectBuilder::BuilderUniform &self)
             { return "BuilderUniform({})"_s.format(self.fVar); });

    py::class_<SkRuntimeEffectBuilder::BuilderChild>(RuntimeEffectBuilder, "BuilderChild")
        .def(
            "set",
            [](SkRuntimeEffectBuilder::BuilderChild &self,
               const std::optional<std::variant<sk_sp<SkShader>, sk_sp<SkColorFilter>, sk_sp<SkBlender>>> &val)
            {
                if (val)
                    try
                    {
                        switch (self.fChild->type)
                        {
                        case SkRuntimeEffect::ChildType::kShader:
                            self = std::get<sk_sp<SkShader>>(*val);
                            break;
                        case SkRuntimeEffect::ChildType::kColorFilter:
                            self = std::get<sk_sp<SkColorFilter>>(*val);
                            break;
                        case SkRuntimeEffect::ChildType::kBlender:
                            self = std::get<sk_sp<SkBlender>>(*val);
                            break;
                        }
                    }
                    catch (const std::bad_variant_access &)
                    {
                        throw py::type_error(
                            "Child is of type {} but set() was called with {}."_s.format(self.fChild->type, val));
                    }
                else
                    self = nullptr;
            },
            "Set the child to the given *val*.", "val"_a)
        .def("__str__",
             [](const SkRuntimeEffectBuilder::BuilderChild &self) { return "BuilderChild({})"_s.format(self.fChild); });

    RuntimeEffectBuilder.def("effect", &SkRuntimeEffectBuilder::effect, py::return_value_policy::reference_internal)
        .def(
            "uniform",
            [](SkRuntimeEffectBuilder &self, const std::string_view &name)
            {
                const SkRuntimeEffectBuilder::BuilderUniform uniform = self.uniform(name);
                if (!uniform.fVar)
                    throw py::value_error("No uniform named '{}' found."_s.format(name));
                return uniform;
            },
            "name"_a)
        .def(
            "child",
            [](SkRuntimeEffectBuilder &self, const std::string_view &name)
            {
                const SkRuntimeEffectBuilder::BuilderChild &child = self.child(name);
                if (!child.fChild)
                    throw py::value_error("No child named '{}' found."_s.format(name));
                return child;
            },
            "name"_a)
        .def("uniforms", &SkRuntimeEffectBuilder::uniforms)
        .def("children",
             [](SkRuntimeEffectBuilder &self)
             {
                 const SkSpan<const SkRuntimeEffect::ChildPtr> children = self.children();
                 return std::vector<SkRuntimeEffect::ChildPtr>(children.begin(), children.end());
             });

    py::class_<SkRuntimeShaderBuilder, SkRuntimeEffectBuilder>(m, "RuntimeShaderBuilder")
        .def(py::init<sk_sp<SkRuntimeEffect>>(), "effect"_a)
        .def("makeShader", &SkRuntimeShaderBuilder::makeShader, "localMatrix"_a = nullptr);

    py::class_<SkRuntimeColorFilterBuilder, SkRuntimeEffectBuilder>(m, "RuntimeColorFilterBuilder")
        .def(py::init<sk_sp<SkRuntimeEffect>>(), "effect"_a)
        .def("makeColorFilter", &SkRuntimeColorFilterBuilder::makeColorFilter);

    py::class_<SkRuntimeBlendBuilder, SkRuntimeEffectBuilder>(m, "RuntimeBlendBuilder")
        .def(py::init<sk_sp<SkRuntimeEffect>>(), "effect"_a)
        .def("makeBlender", &SkRuntimeBlendBuilder::makeBlender);
}