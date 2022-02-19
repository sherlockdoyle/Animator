#include "common.h"
#include "include/third_party/skcms/skcms.h"
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

void initCms(py::module &m)
{
    py::module cms = m.def_submodule("cms", R"doc(
        This module provides an interface to the Skia CMS library. Every function in the library is exposed as a static
        method (constructor) or as a class method of some class. Usually of the class corresponding to the type of the
        first parameter of the function.
    )doc");

    py::class_<skcms_Matrix3x3>(cms, "Matrix3x3")
        .def(py::init(
                 []() {
                     return skcms_Matrix3x3{{{1, 0, 0}, {0, 1, 0}, {0, 0, 1}}};
                 }),
             "Create a new identity Matrix3x3.")
        .def(py::init(
                 [](float a, float b, float c, float d, float e, float f, float g, float h, float i) {
                     return skcms_Matrix3x3{{{a, b, c}, {d, e, f}, {g, h, i}}};
                 }),
             "Create a new Matrix3x3 with the given values.", "a"_a, "b"_a, "c"_a, "d"_a, "e"_a, "f"_a, "g"_a, "h"_a,
             "i"_a)
        .def(py::init(
                 [](std::vector<std::vector<float>> values)
                 {
                     if (values.size() != 3)
                         throw py::value_error("Matrix3x3 must have 3 rows");
                     for (auto &row : values)
                         if (row.size() != 3)
                             throw py::value_error("Matrix3x3 must have 3 columns");
                     return skcms_Matrix3x3{{{values[0][0], values[0][1], values[0][2]},
                                             {values[1][0], values[1][1], values[1][2]},
                                             {values[2][0], values[2][1], values[2][2]}}};
                 }),
             R"doc(
                Create a new Matrix3x3 with the given values.

                :param values: A list of 3 rows, each of which is a list of 3 values.
            )doc",
             "values"_a)
        .def(
            "invert",
            [](const skcms_Matrix3x3 &mat)
            {
                skcms_Matrix3x3 dst;
                if (skcms_Matrix3x3_invert(&mat, &dst))
                    return dst;
                throw py::value_error("Matrix3x3 is not invertible");
            },
            R"doc(
                Returns the inverse of the matrix, or raises ValueError if the matrix is not invertible.

                :return: The inverse of the matrix.
            )doc")
        .def("concat", &skcms_Matrix3x3_concat, "other"_a)
        .def_static(
            "AdaptToXYZD50",
            [](const float &wx, const float &wy)
            {
                skcms_Matrix3x3 dst;
                if (skcms_AdaptToXYZD50(wx, wy, &dst))
                    return dst;
                throw py::value_error("Parameters must be in the range [0, 1]");
            },
            "wx"_a, "wy"_a)
        .def_static(
            "PrimariesToXYZD50",
            [](const float &rx, const float &ry, const float &gx, const float &gy, const float &bx, const float &by,
               const float &wx, const float &wy)
            {
                skcms_Matrix3x3 dst;
                if (skcms_PrimariesToXYZD50(rx, ry, gx, gy, bx, by, wx, wy, &dst))
                    return dst;
                throw py::value_error("Invalid parameters");
            },
            "rx"_a, "ry"_a, "gx"_a, "gy"_a, "bx"_a, "by"_a, "wx"_a, "wy"_a)
        .def(
            "__getitem__",
            [](const skcms_Matrix3x3 &mat, py::tuple index)
            {
                if (index.size() != 2)
                    throw py::index_error("Matrix3x3 index must be a 2-tuple");
                int i = py::cast<int>(index[0]);
                int j = py::cast<int>(index[1]);
                if (i < 0 || i > 2 || j < 0 || j > 2)
                    throw py::index_error("Matrix3x3 index out of range");
                return mat.vals[i][j];
            },
            R"doc(
                Returns the value of the matrix at the given index (2-tuple). Use as mat[row][column].

                :param index: The index (row, column) of the value to return.
                :return: The value at the given index.
            )doc",
            "index"_a)
        .def(
            "__setitem__",
            [](skcms_Matrix3x3 &mat, py::tuple index, float value)
            {
                if (index.size() != 2)
                    throw py::index_error("Matrix3x3 index must be a 2-tuple");
                int i = py::cast<int>(index[0]);
                int j = py::cast<int>(index[1]);
                if (i < 0 || i > 2 || j < 0 || j > 2)
                    throw py::index_error("Matrix3x3 index out of range");
                mat.vals[i][j] = value;
            },
            R"doc(
                 Sets the value of the matrix at the given index (2-tuple). Use as mat[row][column] = value.

                 :param index: The index (row, column) of the value to set.
                 :param value: The value to set.
             )doc",
            "index"_a, "value"_a)
        .def("__str__",
             [](const skcms_Matrix3x3 &mat)
             {
                 std::stringstream s;
                 s << "Matrix3x3((" << mat.vals[0][0] << ", " << mat.vals[0][1] << ", " << mat.vals[0][2] << "), ("
                   << mat.vals[1][0] << ", " << mat.vals[1][1] << ", " << mat.vals[1][2] << "), (" << mat.vals[2][0]
                   << ", " << mat.vals[2][1] << ", " << mat.vals[2][2] << "))";
                 return s.str();
             });

    py::class_<skcms_Matrix3x4>(cms, "Matrix3x4")
        .def(py::init(
                 []() {
                     return skcms_Matrix3x4{{{1, 0, 0, 0}, {0, 1, 0, 0}, {0, 0, 1, 0}}};
                 }),
             "Create a new identity Matrix3x4.")
        .def(py::init(
                 [](float a, float b, float c, float d, float e, float f, float g, float h, float i, float j, float k,
                    float l) {
                     return skcms_Matrix3x4{{{a, b, c, d}, {e, f, g, h}, {i, j, k, l}}};
                 }),
             "Create a new Matrix3x4 with the given values.", "a"_a, "b"_a, "c"_a, "d"_a, "e"_a, "f"_a, "g"_a, "h"_a,
             "i"_a, "j"_a, "k"_a, "l"_a)
        .def(py::init(
                 [](std::vector<std::vector<float>> values)
                 {
                     if (values.size() != 3)
                         throw py::value_error("Matrix3x4 must have 3 rows");
                     for (auto &row : values)
                         if (row.size() != 4)
                             throw py::value_error("Matrix3x4 must have 4 columns");
                     return skcms_Matrix3x4{{{values[0][0], values[0][1], values[0][2], values[0][3]},
                                             {values[1][0], values[1][1], values[1][2], values[1][3]},
                                             {values[2][0], values[2][1], values[2][2], values[2][3]}}};
                 }),
             R"doc(
                Create a new Matrix3x4 with the given values.

                :param values: A list of 3 lists of 4 values.
            )doc",
             "values"_a)
        .def(
            "__getitem__",
            [](const skcms_Matrix3x4 &mat, py::tuple index)
            {
                if (index.size() != 2)
                    throw py::index_error("Matrix3x4 index must be a 2-tuple");
                int i = py::cast<int>(index[0]);
                int j = py::cast<int>(index[1]);
                if (i < 0 || i > 2 || j < 0 || j > 3)
                    throw py::index_error("Matrix3x4 index out of range");
                return mat.vals[i][j];
            },
            R"doc(
                Returns the value of the matrix at the given index (2-tuple). Use as mat[row][column].

                :param index: The index (row, column) of the value to return.
                :return: The value at the given index.
            )doc",
            "index"_a)
        .def(
            "__setitem__",
            [](skcms_Matrix3x4 &mat, py::tuple index, float value)
            {
                if (index.size() != 2)
                    throw py::index_error("Matrix3x4 index must be a 2-tuple");
                int i = py::cast<int>(index[0]);
                int j = py::cast<int>(index[1]);
                if (i < 0 || i > 2 || j < 0 || j > 3)
                    throw py::index_error("Matrix3x4 index out of range");
                mat.vals[i][j] = value;
            },
            R"doc(
                 Sets the value of the matrix at the given index (2-tuple). Use as mat[row][column] = value.

                 :param index: The index (row, column) of the value to set.
                 :param value: The value to set.
             )doc",
            "index"_a, "value"_a)
        .def("__str__",
             [](const skcms_Matrix3x4 &mat)
             {
                 std::stringstream s;
                 s << "Matrix3x4((" << mat.vals[0][0] << ", " << mat.vals[0][1] << ", " << mat.vals[0][2] << ", "
                   << mat.vals[0][3] << "), (" << mat.vals[1][0] << ", " << mat.vals[1][1] << ", " << mat.vals[1][2]
                   << ", " << mat.vals[1][3] << "), (" << mat.vals[2][0] << ", " << mat.vals[2][1] << ", "
                   << mat.vals[2][2] << ", " << mat.vals[2][3] << "))";
                 return s.str();
             });

    py::class_<skcms_TransferFunction>(cms, "TransferFunction")
        .def(py::init([]() { return *skcms_Identity_TransferFunction(); }), "Create a new identity TransferFunction.")
        .def(py::init([](float g, float a, float b, float c, float d, float e, float f)
                      { return skcms_TransferFunction{g, a, b, c, d, e, f}; }),
             "Create a new TransferFunction with the given values.", "g"_a, "a"_a, "b"_a, "c"_a, "d"_a, "e"_a, "f"_a)
        .def(py::init(
                 [](const std::vector<float> &v)
                 {
                     if (v.size() != 7)
                         throw py::value_error("Number of elements must be 9.");
                     return skcms_TransferFunction{v[0], v[1], v[2], v[3], v[4], v[5], v[6]};
                 }),
             R"doc(
                Create a new TransferFunction with the given values.

                :param v: A list of 7 values.
            )doc",
             "v"_a)
        .def_readwrite("g", &skcms_TransferFunction::g)
        .def_readwrite("a", &skcms_TransferFunction::a)
        .def_readwrite("b", &skcms_TransferFunction::b)
        .def_readwrite("c", &skcms_TransferFunction::c)
        .def_readwrite("d", &skcms_TransferFunction::d)
        .def_readwrite("e", &skcms_TransferFunction::e)
        .def_readwrite("f", &skcms_TransferFunction::f)
        .def("eval", &skcms_TransferFunction_eval, "x"_a)
        .def(
            "invert",
            [](const skcms_TransferFunction &tf)
            {
                skcms_TransferFunction inv;
                if (skcms_TransferFunction_invert(&tf, &inv))
                    return inv;
                throw py::value_error("Unable to invert transfer function.");
            },
            R"doc(
                Inverts the transfer function.

                :return: The inverted transfer function.
            )doc")
        .def("makePQish", &skcms_TransferFunction_makePQish, "A"_a, "B"_a, "C"_a, "D"_a, "E"_a, "F"_a)
        .def("makeScaledHLGish", &skcms_TransferFunction_makeScaledHLGish, "K"_a, "R"_a, "G"_a, "a"_a, "b"_a, "c"_a)
        .def("makeHLGish", &skcms_TransferFunction_makeHLGish, "R"_a, "G"_a, "a"_a, "b"_a, "c"_a)
        .def("makePQ", &skcms_TransferFunction_makePQ)
        .def("makeHLG", &skcms_TransferFunction_makeHLG)
        .def("isSRGBish", &skcms_TransferFunction_isSRGBish)
        .def("isPQish", &skcms_TransferFunction_isPQish)
        .def("isHLGish", &skcms_TransferFunction_isHLGish)
        .def_static("sRGB_TransferFunction", &skcms_sRGB_TransferFunction, py::return_value_policy::reference)
        .def_static("sRGB_Inverse_TransferFunction", &skcms_sRGB_Inverse_TransferFunction,
                    py::return_value_policy::reference)
        .def_static("Identity_TransferFunction", &skcms_Identity_TransferFunction, py::return_value_policy::reference)
        .def("__str__",
             [](const skcms_TransferFunction &tf)
             {
                 std::stringstream s;
                 s << "TransferFunction(" << tf.g << ", " << tf.a << ", " << tf.b << ", " << tf.c << ", " << tf.d
                   << ", " << tf.e << ", " << tf.f << ")";
                 return s.str();
             });

    py::class_<skcms_Curve>(cms, "Curve")
        .def(py::init())
        .def_readwrite("alias_of_table_entries", &skcms_Curve::alias_of_table_entries)
        .def_readwrite("parametric", &skcms_Curve::parametric)
        .def_readwrite("table_entries", &skcms_Curve::table_entries)
        .def_readwrite("table_8", &skcms_Curve::table_8)
        .def_readwrite("table_16", &skcms_Curve::table_16)
        .def("areApproximateInverses", &skcms_AreApproximateInverses,
             R"doc(
                 Practical test that answers: Is curve roughly the inverse of *inv_tf*? Typically used by passing the
                 inverse of a known parametric transfer function (like sRGB), to determine if a particular curve is
                 very close to sRGB.
            )doc",
             "inv_tf"_a)
        .def(
            "approximateCurve",
            [](const skcms_Curve &curve)
            {
                skcms_TransferFunction approx;
                float max_error;
                if (skcms_ApproximateCurve(&curve, &approx, &max_error))
                    return py::make_tuple(approx, max_error);
                throw py::value_error("Unable to approximate curve.");
            },
            R"doc(
                Approximate the curve with a transfer function.

                :return: A tuple of the approximated transfer function and the maximum error.
                :rtype: (TransferFunction, float)
            )doc");

    py::class_<skcms_A2B>(cms, "A2B",
                          R"doc(
                            :warning: Indexed assignment to array attributes will not work. Instead assign to the whole
                                array. This will cause a memory copy. Instead of doing ``a2b.input_curves[0] = curve``,
                                do ``a2b.input_curves = [curve, *a2b.input_curves[1:]]``.
                        )doc")
        .def(py::init())
        .def_readwrite("input_channels", &skcms_A2B::input_channels)
        .def_property(
            "input_curves",
            [](const skcms_A2B &a2b)
            { return std::vector<const skcms_Curve *>(&a2b.input_curves, &a2b.input_curves + 4); },
            [](skcms_A2B &a2b, const std::vector<skcms_Curve> &curves)
            {
                if (curves.size() != 4)
                    throw py::value_error("Number of curves must be 4.");
                for (int i = 0; i < 4; i++)
                    a2b.input_curves[i] = curves[i];
            })
        .def_property(
            "grid_points",
            [](const skcms_A2B &a2b) { return std::vector<const uint8_t *>(&a2b.grid_points, &a2b.grid_points + 4); },
            [](skcms_A2B &a2b, const std::vector<uint8_t> &points)
            {
                if (points.size() != 4)
                    throw py::value_error("Number of points must be 4.");
                for (int i = 0; i < 4; i++)
                    a2b.grid_points[i] = points[i];
            })
        .def_readwrite("grid_8", &skcms_A2B::grid_8)
        .def_readwrite("grid_16", &skcms_A2B::grid_16)
        .def_readwrite("matrix_channels", &skcms_A2B::matrix_channels)
        .def_property(
            "matrix_curves",
            [](const skcms_A2B &a2b)
            { return std::vector<const skcms_Curve *>(&a2b.matrix_curves, &a2b.matrix_curves + 4); },
            [](skcms_A2B &a2b, const std::vector<skcms_Curve> &curves)
            {
                if (curves.size() != 3)
                    throw py::value_error("Number of curves must be 3.");
                for (int i = 0; i < 3; i++)
                    a2b.matrix_curves[i] = curves[i];
            })
        .def_readwrite("matrix", &skcms_A2B::matrix)
        .def_readwrite("output_channels", &skcms_A2B::output_channels)
        .def_property(
            "output_curves",
            [](const skcms_A2B &a2b)
            { return std::vector<const skcms_Curve *>(&a2b.output_curves, &a2b.output_curves + 4); },
            [](skcms_A2B &a2b, const std::vector<skcms_Curve> &curves)
            {
                if (curves.size() != 3)
                    throw py::value_error("Number of curves must be 3.");
                for (int i = 0; i < 3; i++)
                    a2b.output_curves[i] = curves[i];
            });

    py::class_<skcms_B2A>(cms, "B2A",
                          R"doc(
                            :warning: Indexed assignment to array attributes will not work. Instead assign to the whole
                                array. This will cause a memory copy. Instead of doing ``b2a.input_curves[0] = curve``,
                                do ``b2a.input_curves = [curve, *b2a.input_curves[1:]]``.
                        )doc")
        .def(py::init())
        .def_readwrite("input_channels", &skcms_B2A::input_channels)
        .def_property(
            "input_curves",
            [](const skcms_B2A &b2a)
            { return std::vector<const skcms_Curve *>(&b2a.input_curves, &b2a.input_curves + 3); },
            [](skcms_B2A &b2a, const std::vector<skcms_Curve> &curves)
            {
                if (curves.size() != 3)
                    throw py::value_error("Number of curves must be 3.");
                for (int i = 0; i < 3; i++)
                    b2a.input_curves[i] = curves[i];
            })
        .def_readwrite("matrix_channels", &skcms_B2A::matrix_channels)
        .def_readwrite("matrix", &skcms_B2A::matrix)
        .def_property(
            "matrix_curves",
            [](const skcms_B2A &b2a)
            { return std::vector<const skcms_Curve *>(&b2a.matrix_curves, &b2a.matrix_curves + 3); },
            [](skcms_B2A &b2a, const std::vector<skcms_Curve> &curves)
            {
                if (curves.size() != 3)
                    throw py::value_error("Number of curves must be 3.");
                for (int i = 0; i < 3; i++)
                    b2a.matrix_curves[i] = curves[i];
            })
        .def_readwrite("output_channels", &skcms_B2A::output_channels)
        .def_property(
            "grid_points",
            [](const skcms_B2A &b2a) { return std::vector<const uint8_t *>(&b2a.grid_points, &b2a.grid_points + 4); },
            [](skcms_B2A &b2a, const std::vector<uint8_t> &points)
            {
                if (points.size() != 4)
                    throw py::value_error("Number of points must be 4.");
                for (int i = 0; i < 4; i++)
                    b2a.grid_points[i] = points[i];
            })
        .def_readwrite("grid_8", &skcms_B2A::grid_8)
        .def_readwrite("grid_16", &skcms_B2A::grid_16)
        .def_property(
            "output_curves",
            [](const skcms_B2A &b2a)
            { return std::vector<const skcms_Curve *>(&b2a.output_curves, &b2a.output_curves + 4); },
            [](skcms_B2A &b2a, const std::vector<skcms_Curve> &curves)
            {
                if (curves.size() != 4)
                    throw py::value_error("Number of curves must be 4.");
                for (int i = 0; i < 4; i++)
                    b2a.output_curves[i] = curves[i];
            });

    py::class_<skcms_ICCProfile>(cms, "ICCProfile")
        .def(py::init(
            []()
            {
                std::unique_ptr<skcms_ICCProfile> profile(new skcms_ICCProfile());
                skcms_Init(profile.get());
                return profile;
            }))
        .def_property_readonly("buffer",
                               py::cpp_function(
                                   [](const skcms_ICCProfile &profile) -> std::optional<py::memoryview>
                                   {
                                       if (profile.buffer == nullptr)
                                           return std::nullopt;
                                       return py::memoryview::from_buffer(profile.buffer, sizeof(uint8_t),
                                                                          py::format_descriptor<uint8_t>::value,
                                                                          {profile.size}, {sizeof(uint8_t)});
                                   },
                                   py::keep_alive<0, 1>()),
                               R"doc(
                The ICC profile buffer represented as a :py:class:`memoryview`.

                :note: A reference to the profile is needed to keep the buffer alive.
            )doc")
        .def_readwrite("size", &skcms_ICCProfile::size)
        .def_readwrite("data_color_space", &skcms_ICCProfile::data_color_space)
        .def_readwrite("pcs", &skcms_ICCProfile::pcs)
        .def_readwrite("tag_count", &skcms_ICCProfile::tag_count)
        .def_readwrite("has_trc", &skcms_ICCProfile::has_trc)
        .def_property(
            "trc",
            [](const skcms_ICCProfile &profile)
            { return std::vector<const skcms_Curve *>(&profile.trc, &profile.trc + 3); },
            [](skcms_ICCProfile &profile, const std::vector<skcms_Curve> &trcs)
            {
                if (trcs.size() != 3)
                    throw py::value_error("Number of curves must be 3.");
                for (int i = 0; i < 3; i++)
                    profile.trc[i] = trcs[i];
            },
            R"doc(
                :warning: Indexed assignment to this attributes will not work. Instead assign to the whole array. This
                    will cause a memory copy. Instead of doing ``profile.trc[0] = curve``, do ``profile.trc = [curve,
                    *profile.trc[1:]]``.
            )doc")
        .def_readwrite("has_toXYZD50", &skcms_ICCProfile::has_toXYZD50)
        .def_readwrite("toXYZD50", &skcms_ICCProfile::toXYZD50)
        .def_readwrite("has_A2B", &skcms_ICCProfile::has_A2B)
        .def_readwrite("A2B", &skcms_ICCProfile::A2B)
        .def_readwrite("has_B2A", &skcms_ICCProfile::has_B2A)
        .def_readwrite("B2A", &skcms_ICCProfile::B2A)
        .def_static("sRGB_profile", &skcms_sRGB_profile, py::return_value_policy::reference)
        .def_static("XYZD50_profile", &skcms_XYZD50_profile, py::return_value_policy::reference)
        .def("approximatelyEqualProfiles", &skcms_ApproximatelyEqualProfiles,
             "Practical equality test for two :py:class:`ICCProfile`.", "other"_a)
        .def("__eq__", &skcms_ApproximatelyEqualProfiles, py::is_operator(),
             "Same as :py:meth:`~ICCProfile.approximatelyEqualProfiles`.", "other"_a)
        .def("TRCs_AreApproximateInverse", &skcms_TRCs_AreApproximateInverse,
             R"doc(
                Similar to :py:meth:`Curve.areApproximateInverse`, answering the question for all three TRC curves of
                the profile. Again, passing skcms_sRGB_InverseTransferFunction as *inv_tf* will answer the question:
                "Does this profile have a transfer function that is very close to sRGB?"
            )doc",
             "inv_tf"_a)
        .def_static(
            "ParseWithA2BPriority",
            [](const py::buffer &buf, const std::vector<int> &priority)
            {
                py::buffer_info info = buf.request();
                std::unique_ptr<skcms_ICCProfile> profile(new skcms_ICCProfile());
                if (skcms_ParseWithA2BPriority(info.ptr, info.size * info.itemsize, priority.data(), priority.size(),
                                               profile.get()))
                    return profile;
                throw py::value_error("Failed to parse ICC profile.");
            },
            R"doc(
                Parse an ICC profile from a buffer.

                :param buffer: The buffer containing the ICC profile.
                :param priority: Selects an A2B profile (if present) according to priority list (each entry 0-2).
                :return: The parsed ICC profile.
            )doc",
            "buf"_a, "priority"_a, py::keep_alive<0, 1>())
        .def_static(
            "Parse",
            [](const py::buffer &buf)
            {
                py::buffer_info info = buf.request();
                std::unique_ptr<skcms_ICCProfile> profile(new skcms_ICCProfile());
                if (skcms_Parse(info.ptr, info.size * info.itemsize, profile.get()))
                    return profile;
                throw py::value_error("Failed to parse ICC profile.");
            },
            R"doc(
                Parse an ICC profile from a buffer.

                :param buffer: The buffer containing the ICC profile.
                :return: The parsed ICC profile.
            )doc",
            "buf"_a, py::keep_alive<0, 1>())
        .def(
            "getCHAD",
            [](const skcms_ICCProfile &profile)
            {
                skcms_Matrix3x3 m;
                if (skcms_GetCHAD(&profile, &m))
                    return m;
                throw py::value_error("Failed to get CHAD matrix.");
            },
            R"doc(
                :return: The color hue and chroma adjustment matrix.
                :rtype: :py:class:`Matrix3x3`
            )doc")
        .def(
            "getWTPT",
            [](const skcms_ICCProfile &profile)
            {
                std::vector<float> xyz(3);
                if (skcms_GetWTPT(&profile, xyz.data()))
                    return xyz;
                throw py::value_error("Failed to get WTPT.");
            },
            R"doc(
                :return: The white point of the profile.
                :rtype: :py:class:`Matrix3x3`
            )doc")
        .def("makeUsableAsDestination", &skcms_MakeUsableAsDestination)
        .def("makeUsableAsDestinationWithSingleCurve", &skcms_MakeUsableAsDestinationWithSingleCurve)
        .def("setTransferFunction", &skcms_SetTransferFunction, "tf"_a)
        .def("setXYZD50", &skcms_SetXYZD50, "m"_a);

    enum Signature
    {
        CMYK = skcms_Signature_CMYK,
        Gray = skcms_Signature_Gray,
        RGB = skcms_Signature_RGB,
        Lab = skcms_Signature_Lab,
        XYZ = skcms_Signature_XYZ
    };
    py::enum_<Signature>(cms, "Signature")
        .value("CMYK", Signature::CMYK)
        .value("Gray", Signature::Gray)
        .value("RGB", Signature::RGB)
        .value("Lab", Signature::Lab)
        .value("XYZ", Signature::XYZ);

    py::enum_<skcms_PixelFormat>(cms, "PixelFormat")
        .value("A_8", skcms_PixelFormat_A_8)
        .value("A_8_", skcms_PixelFormat_A_8_)
        .value("G_8", skcms_PixelFormat_G_8)
        .value("G_8_", skcms_PixelFormat_G_8_)
        .value("RGBA_8888_Palette8", skcms_PixelFormat_RGBA_8888_Palette8)
        .value("BGRA_8888_Palette8", skcms_PixelFormat_BGRA_8888_Palette8)

        .value("RGB_565", skcms_PixelFormat_RGB_565)
        .value("BGR_565", skcms_PixelFormat_BGR_565)

        .value("ABGR_4444", skcms_PixelFormat_ABGR_4444)
        .value("ARGB_4444", skcms_PixelFormat_ARGB_4444)

        .value("RGB_888", skcms_PixelFormat_RGB_888)
        .value("BGR_888", skcms_PixelFormat_BGR_888)
        .value("RGBA_8888", skcms_PixelFormat_RGBA_8888)
        .value("BGRA_8888", skcms_PixelFormat_BGRA_8888)
        .value("RGBA_8888_sRGB", skcms_PixelFormat_RGBA_8888_sRGB)
        .value("BGRA_8888_sRGB", skcms_PixelFormat_BGRA_8888_sRGB)

        .value("RGBA_1010102", skcms_PixelFormat_RGBA_1010102)
        .value("BGRA_1010102", skcms_PixelFormat_BGRA_1010102)

        .value("RGB_161616LE", skcms_PixelFormat_RGB_161616LE)
        .value("BGR_161616LE", skcms_PixelFormat_BGR_161616LE)
        .value("RGBA_16161616LE", skcms_PixelFormat_RGBA_16161616LE)
        .value("BGRA_16161616LE", skcms_PixelFormat_BGRA_16161616LE)

        .value("RGB_161616BE", skcms_PixelFormat_RGB_161616BE)
        .value("BGR_161616BE", skcms_PixelFormat_BGR_161616BE)
        .value("RGBA_16161616BE", skcms_PixelFormat_RGBA_16161616BE)
        .value("BGRA_16161616BE", skcms_PixelFormat_BGRA_16161616BE)

        .value("RGB_hhh_Norm", skcms_PixelFormat_RGB_hhh_Norm)
        .value("BGR_hhh_Norm", skcms_PixelFormat_BGR_hhh_Norm)
        .value("RGBA_hhhh_Norm", skcms_PixelFormat_RGBA_hhhh_Norm)
        .value("BGRA_hhhh_Norm", skcms_PixelFormat_BGRA_hhhh_Norm)

        .value("RGB_hhh", skcms_PixelFormat_RGB_hhh)
        .value("BGR_hhh", skcms_PixelFormat_BGR_hhh)
        .value("RGBA_hhhh", skcms_PixelFormat_RGBA_hhhh)
        .value("BGRA_hhhh", skcms_PixelFormat_BGRA_hhhh)

        .value("RGB_fff", skcms_PixelFormat_RGB_fff)
        .value("BGR_fff", skcms_PixelFormat_BGR_fff)
        .value("RGBA_ffff", skcms_PixelFormat_RGBA_ffff)
        .value("BGRA_ffff", skcms_PixelFormat_BGRA_ffff);

    py::enum_<skcms_AlphaFormat>(cms, "AlphaFormat")
        .value("Opaque", skcms_AlphaFormat_Opaque)
        .value("Unpremul", skcms_AlphaFormat_Unpremul)
        .value("PremulAsEncoded", skcms_AlphaFormat_PremulAsEncoded);

    cms.def(
           "transform",
           [](const py::array &src, const skcms_PixelFormat &srcFmt, const skcms_AlphaFormat &srcAlpha,
              const skcms_ICCProfile *srcProfile, const skcms_PixelFormat &dstFmt, const skcms_AlphaFormat &dstAlpha,
              const skcms_ICCProfile *dstProfile)
           {
               py::ssize_t ndim = src.ndim();
               auto shape = src.shape();
               auto strides = src.strides();
               py::array dst(src.dtype(), std::vector<py::ssize_t>(shape, shape + ndim),
                             std::vector<py::ssize_t>(strides, strides + ndim));
               if (skcms_Transform(src.data(), srcFmt, srcAlpha, srcProfile, dst.mutable_data(), dstFmt, dstAlpha,
                                   dstProfile, src.size()))
                   return dst;
               throw py::value_error("Failed to transform.");
           },
           R"doc(
                Convert pixels from src format and color profile to dst format and color profile.

                :param numpy.ndarray src: The source pixels.
                :param PixelFormat srcFmt: The source pixel format.
                :param AlphaFormat srcAlpha: The source alpha format.
                :param ICCProfile srcProfile: The source color profile. If ``None``, the sRGB color profile is used.
                :param PixelFormat dstFmt: The destination pixel format.
                :param AlphaFormat dstAlpha: The destination alpha format.
                :param ICCProfile dstProfile: The destination color profile. If ``None``, the sRGB color profile is
                    used.
                :return: The destination pixels.
                :rtype: numpy.ndarray
            )doc",
           "src"_a, "srcFmt"_a, "srcAlpha"_a, "srcProfile"_a, "dstFmt"_a, "dstAlpha"_a, "dstProfile"_a)
        .def(
            "transformWithPalette",
            [](const py::array &src, const skcms_PixelFormat &srcFmt, const skcms_AlphaFormat &srcAlpha,
               const skcms_ICCProfile *srcProfile, const skcms_PixelFormat &dstFmt, const skcms_AlphaFormat &dstAlpha,
               const skcms_ICCProfile *dstProfile, const py::object &palette)
            {
                py::ssize_t ndim = src.ndim();
                auto shape = src.shape();
                auto strides = src.strides();
                py::array dst(src.dtype(), std::vector<py::ssize_t>(shape, shape + ndim),
                              std::vector<py::ssize_t>(strides, strides + ndim));
                if (skcms_TransformWithPalette(src.data(), srcFmt, srcAlpha, srcProfile, dst.mutable_data(), dstFmt,
                                               dstAlpha, dstProfile, src.size(),
                                               palette.is_none() ? nullptr : palette.cast<py::array>().data()))
                    return dst;
                throw py::value_error("Failed to transform.");
            },
            R"doc(
                Convert pixels from src format and color profile to dst format and color profile.

                :param numpy.ndarray src: The source pixels.
                :param PixelFormat srcFmt: The source pixel format.
                :param AlphaFormat srcAlpha: The source alpha format.
                :param ICCProfile srcProfile: The source color profile. If ``None``, the sRGB color profile is used.
                :param PixelFormat dstFmt: The destination pixel format.
                :param AlphaFormat dstAlpha: The destination alpha format.
                :param ICCProfile dstProfile: The destination color profile. If ``None``, the sRGB color profile is
                    used.
                :param numpy.ndarray palette: The palette.
                :return: The destination pixels.
                :rtype: numpy.ndarray
            )doc",
            "src"_a, "srcFmt"_a, "srcAlpha"_a, "srcProfile"_a, "dstFmt"_a, "dstAlpha"_a, "dstProfile"_a,
            "palette"_a = py::none())
        .def(
            "transformWithPalette",
            [](const py::array &src, const skcms_PixelFormat &srcFmt, const skcms_AlphaFormat &srcAlpha,
               const skcms_ICCProfile *srcProfile, py::array &dst, const skcms_PixelFormat &dstFmt,
               const skcms_AlphaFormat &dstAlpha, const skcms_ICCProfile *dstProfile, const py::object &palette)
            {
                if (skcms_TransformWithPalette(src.data(), srcFmt, srcAlpha, srcProfile, dst.mutable_data(), dstFmt,
                                               dstAlpha, dstProfile, src.size(),
                                               palette.is_none() ? nullptr : palette.cast<py::array>().data()))
                    return dst;
                throw py::value_error("Failed to transform.");
            },
            R"doc(
                Convert pixels from src format and color profile to dst format and color profile.

                :param numpy.ndarray src: The source pixels.
                :param PixelFormat srcFmt: The source pixel format.
                :param AlphaFormat srcAlpha: The source alpha format.
                :param ICCProfile srcProfile: The source color profile. If ``None``, the sRGB color profile is used.
                :param numpy.ndarray dst: The destination pixels.
                :param PixelFormat dstFmt: The destination pixel format.
                :param AlphaFormat dstAlpha: The destination alpha format.
                :param ICCProfile dstProfile: The destination color profile. If ``None``, the sRGB color profile is
                    used.
                :param numpy.ndarray palette: The palette.
                :return: The destination pixels.
                :rtype: numpy.ndarray
            )doc",
            "src"_a, "srcFmt"_a, "srcAlpha"_a, "srcProfile"_a, "dst"_a, "dstFmt"_a, "dstAlpha"_a, "dstProfile"_a,
            "palette"_a = py::none())
        .def("disableRuntimeCPUDetection", &skcms_DisableRuntimeCPUDetection);
}