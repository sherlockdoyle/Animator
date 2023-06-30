#include "common.h"
#include "include/core/SkData.h"
#include <pybind11/stl.h>

void initData(py::module &m)
{
    py::class_<SkData, sk_sp<SkData>>(m, "Data", py::buffer_protocol(), R"doc(
        :py:class:`Data` supports Python buffer protocol, meaning that
        :py:class:`Data` can be converted to Python buffer types without copy::

            bytes(data)
            memoryview(data)
            np.array(data)

        :note: Remember to keep a reference to :py:class:`Data` when converting to Python buffer types.
    )doc")
        .def_buffer(
            [](SkData &data)
            {
                return py::buffer_info(data.writable_data(), sizeof(uint8_t), py::format_descriptor<uint8_t>::value, 1,
                                       {data.size()}, {sizeof(uint8_t)});
            })
        .def(py::init(
                 [](const py::buffer &b, bool copy)
                 {
                     const py::buffer_info info = b.request();
                     if (copy)
                         return SkData::MakeWithCopy(info.ptr, info.size);
                     else
                         return SkData::MakeWithoutCopy(info.ptr, info.size);
                 }),
             R"doc(
                Create a new :py:class:`Data`.

                :param bytes|bytearray|memoryview buf: Buffer object
                :param bool copy: Whether to copy data, default `False`.
            )doc",
             "buf"_a, "copy"_a = false, py::keep_alive<0, 1>())
        .def("size", &SkData::size)
        .def("isEmpty", &SkData::isEmpty)
        .def(
            "data",
            [](const SkData &data)
            {
                return py::memoryview::from_buffer(data.data(), sizeof(uint8_t), py::format_descriptor<uint8_t>::value,
                                                   {data.size()}, {sizeof(uint8_t)});
            },
            "Returns the read-only memoryview to the data.", py::keep_alive<0, 1>())
        .def(
            "bytes",
            [](const SkData &data) { return py::bytes(reinterpret_cast<const char *>(data.bytes()), data.size()); },
            R"doc(
                Like :py:meth:``~Data.data``, returns a read-only ptr into the data, but in this case it is cast to
                ``bytes``.
            )doc")
        .def(
            "writable_data",
            [](SkData &data)
            {
                return py::memoryview::from_buffer(data.writable_data(), sizeof(uint8_t),
                                                   py::format_descriptor<uint8_t>::value, {data.size()},
                                                   {sizeof(uint8_t)}, false);
            },
            "Returns the read-write memoryview to the data.", py::keep_alive<0, 1>())
        .def(
            "copyRange",
            [](const SkData &self, const size_t &offset, const size_t &length, const std::optional<py::buffer> &buffer)
            {
                if (buffer)
                {
                    const py::buffer_info bufInfo = buffer->request();
                    return self.copyRange(offset, length, bufInfo.ptr);
                }
                return self.copyRange(offset, length, nullptr);
            },
            R"doc(
                Helper to copy a range of the data into a caller-provided buffer.

                Returns the actual number of bytes copied, after clamping offset and length to the size of the data. If
                buffer is NULL, it is ignored, and only the computed number of bytes is returned.
            )doc",
            "offset"_a, "length"_a, "buffer"_a)
        .def("equals", &SkData::equals, "other"_a)
        .def("__eq__", &SkData::equals, py::is_operator(), "Same as :py:meth:`~Data.equals`.", "other"_a)
        .def_static(
            "MakeWithCopy",
            [](const py::buffer &b)
            {
                py::buffer_info info = b.request();
                return SkData::MakeWithCopy(info.ptr, info.size);
            },
            "Create a new dataref by copying the specified data.", "data"_a)
        .def_static("MakeUninitialized", &SkData::MakeUninitialized, "length"_a)
        .def_static("MakeZeroInitialized", &SkData::MakeZeroInitialized, "length"_a)
        .def_static("MakeWithCString", &SkData::MakeWithCString,
                    "Create a new dataref by copying the specified string or bytes.", "cstr"_a)
        .def_static(
            "MakeWithoutCopy",
            [](const py::buffer &b)
            {
                py::buffer_info info = b.request();
                return SkData::MakeWithoutCopy(info.ptr, info.size);
            },
            "data"_a, py::keep_alive<0, 1>())
        .def_static("MakeFromFileName", &SkData::MakeFromFileName, "path"_a)
        .def_static("MakeSubset", &SkData::MakeSubset, "src"_a, "offset"_a, "length"_a)
        .def_static("MakeEmpty", &SkData::MakeEmpty)
        .def("__str__",
             [](const SkData &data)
             {
                 std::stringstream s;
                 s << "Data(size=" << data.size() << ")";
                 return s.str();
             });

    py::implicitly_convertible<py::buffer, SkData>();
}