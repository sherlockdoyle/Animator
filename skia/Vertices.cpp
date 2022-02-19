#include "common.h"
#include "include/core/SkVertices.h"
#include <pybind11/stl.h>

sk_sp<SkVertices> Vertices_MakeCopy(const SkVertices::VertexMode &mode, const std::vector<SkPoint> &positions,
                                    const std::optional<std::vector<SkPoint>> &texs,
                                    const std::optional<std::vector<SkColor>> &colors,
                                    const std::optional<std::vector<uint16_t>> &indices)
{
    const size_t vertexCount = positions.size();
    if ((texs && texs->size() != vertexCount) || (colors && colors->size() != vertexCount))
        throw py::value_error("positions, texs, and colors must be the same length");

    if (indices)
        return SkVertices::MakeCopy(mode, vertexCount, positions.data(), texs ? texs->data() : nullptr,
                                    colors ? colors->data() : nullptr, indices->size(),
                                    indices ? indices->data() : nullptr);
    return SkVertices::MakeCopy(mode, vertexCount, positions.data(), texs ? texs->data() : nullptr,
                                colors ? colors->data() : nullptr);
}

void initVertices(py::module &m)
{
    py::class_<SkVertices, sk_sp<SkVertices>> Vertices(m, "Vertices");

    py::enum_<SkVertices::VertexMode>(Vertices, "VertexMode")
        .value("kTriangles_VertexMode", SkVertices::VertexMode::kTriangles_VertexMode)
        .value("kTriangleStrip_VertexMode", SkVertices::VertexMode::kTriangleStrip_VertexMode)
        .value("kTriangleFan_VertexMode", SkVertices::VertexMode::kTriangleFan_VertexMode)
        .value("kLast_VertexMode", SkVertices::VertexMode::kLast_VertexMode);

    Vertices
        .def(py::init(&Vertices_MakeCopy), "Create a vertices by copying the specified arrays.", "mode"_a,
             "positions"_a, "texs"_a = py::none(), "colors"_a = py::none(), "indices"_a = py::none())
        .def_static("Vertices_MakeCopy", &Vertices_MakeCopy, "Create a vertices by copying the specified arrays.",
                    "mode"_a, "positions"_a, "texs"_a, "colors"_a, "indices"_a = py::none())
        .def("uniqueID", &SkVertices::uniqueID)
        .def("bounds", &SkVertices::bounds)
        .def("approximateSize", &SkVertices::approximateSize);
}