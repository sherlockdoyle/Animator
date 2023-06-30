#include "common.h"
#include "include/core/SkMatrix.h"
#include "include/core/SkPoint3.h"
#include "include/core/SkRSXform.h"
#include <pybind11/iostream.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>

typedef py::array_t<SkScalar> ndarray;

SkScalar getItem(const SkMatrix &m, int index)
{
    if (index < 0 || 9 <= index)
        throw py::index_error("Index out of range.");
    return m[index];
}
void setItem(SkMatrix &m, int index, SkScalar value)
{
    if (index < 0 || 9 <= index)
        throw py::index_error("Index out of range.");
    m[index] = value;
}

void initMatrix(py::module &m)
{
    py::class_<SkRSXform>(m, "RSXform")
        .def_static("Make", &SkRSXform::Make, "scos"_a, "ssin"_a, "tx"_a, "ty"_a)
        .def(py::init(&SkRSXform::Make), "scos"_a, "ssin"_a, "tx"_a, "ty"_a)
        .def_static("MakeFromRadians", &SkRSXform::MakeFromRadians, "scale"_a, "radians"_a, "tx"_a, "ty"_a, "ax"_a,
                    "ay"_a)
        .def_readwrite("fSCos", &SkRSXform::fSCos)
        .def_readwrite("fSSin", &SkRSXform::fSSin)
        .def_readwrite("fTx", &SkRSXform::fTx)
        .def_readwrite("fTy", &SkRSXform::fTy)
        .def("rectStaysRect", &SkRSXform::rectStaysRect)
        .def("setIdentity", &SkRSXform::setIdentity)
        .def("set", &SkRSXform::set, "scos"_a, "ssin"_a, "tx"_a, "ty"_a)
        .def(
            "toQuad",
            [](const SkRSXform &rsxForm, const SkScalar &width, const SkScalar &height)
            {
                std::vector<SkPoint> quad(4);
                rsxForm.toQuad(width, height, quad.data());
                return quad;
            },
            R"doc(
                Maps a rectangle with the given *width* and *height* with this :py:class:`RSXform` and returns a list of
                4 points, the corners of the resulting quadrilateral.

                :param width: The width of the rectangle.
                :param height: The height of the rectangle.
                :return: A list of 4 points, the corners of the resulting quadrilateral.
            )doc",
            "width"_a, "height"_a)
        .def(
            "toQuad",
            [](const SkRSXform &rsxForm, const SkSize &size)
            {
                std::vector<SkPoint> quad(4);
                rsxForm.toQuad(size, quad.data());
                return quad;
            },
            R"doc(
                Maps a rectangle with the given *size* with this :py:class:`RSXform` and returns a list of 4 points, the
                corners of the resulting quadrilateral.

                :param size: The size of the rectangle.
                :return: A list of 4 points, the corners of the resulting quadrilateral.
            )doc",
            "size"_a)
        .def(
            "toTriStrip",
            [](const SkRSXform &rsxForm, const SkScalar &width, const SkScalar &height)
            {
                std::vector<SkPoint> strip(4);
                rsxForm.toTriStrip(width, height, strip.data());
                return strip;
            },
            "Returns a list of 4 points, the corners of the resulting strip.", "width"_a, "height"_a)
        .def("__str__",
             [](const SkRSXform &rsxForm)
             {
                 std::stringstream s;
                 s << "RSXform(" << rsxForm.fSCos << ", " << rsxForm.fSSin << ", " << rsxForm.fTx << ", " << rsxForm.fTy
                   << ")";
                 return s.str();
             });

    py::enum_<SkApplyPerspectiveClip>(m, "ApplyPerspectiveClip")
        .value("kNo", SkApplyPerspectiveClip::kNo)
        .value("kYes", SkApplyPerspectiveClip::kYes);

    py::class_<SkMatrix> Matrix(m, "Matrix");
    Matrix
        .def(py::init(
                 [](const ndarray &array)
                 {
                     if (array.size() != 9)
                         throw py::value_error("Matrix must be a 3x3 matrix.");
                     SkMatrix matrix;
                     matrix.set9(array.data());
                     return matrix;
                 }),
             "Creates a :py:class:`Matrix` from 3x3 float32 NumPy array.", "array"_a)
        .def(py::init())
        .def_static("Scale", &SkMatrix::Scale, "sx"_a, "sy"_a)
        .def_static("Translate", py::overload_cast<SkScalar, SkScalar>(&SkMatrix::Translate), "dx"_a, "dy"_a)
        .def_static("Translate", py::overload_cast<SkVector>(&SkMatrix::Translate), "t"_a)
        .def_static("Translate", py::overload_cast<SkIVector>(&SkMatrix::Translate), "t"_a)
        .def_static("RotateDeg", py::overload_cast<SkScalar>(&SkMatrix::RotateDeg), "deg"_a)
        .def_static("RotateDeg", py::overload_cast<SkScalar, SkPoint>(&SkMatrix::RotateDeg), "deg"_a, "pt"_a)
        .def_static("RotateRad", &SkMatrix::RotateRad, "rad"_a)
        .def_static("Skew", &SkMatrix::Skew, "kx"_a, "ky"_a);

    py::enum_<SkMatrix::ScaleToFit>(Matrix, "ScaleToFit")
        .value("kFill_ScaleToFit", SkMatrix::ScaleToFit::kFill_ScaleToFit)
        .value("kStart_ScaleToFit", SkMatrix::ScaleToFit::kStart_ScaleToFit)
        .value("kCenter_ScaleToFit", SkMatrix::ScaleToFit::kCenter_ScaleToFit)
        .value("kEnd_ScaleToFit", SkMatrix::ScaleToFit::kEnd_ScaleToFit);
    Matrix
        .def_static("RectToRect", &SkMatrix::RectToRect, "src"_a, "dst"_a,
                    "mode"_a = SkMatrix::ScaleToFit::kFill_ScaleToFit)
        .def_static("MakeAll", &SkMatrix::MakeAll, "scaleX"_a, "skewX"_a, "transX"_a, "skewY"_a, "scaleY"_a, "transY"_a,
                    "pers0"_a, "pers1"_a, "pers2"_a);

    py::enum_<SkMatrix::TypeMask>(Matrix, "TypeMask", py::arithmetic())
        .value("kIdentity_Mask", SkMatrix::TypeMask::kIdentity_Mask)
        .value("kTranslate_Mask", SkMatrix::TypeMask::kTranslate_Mask)
        .value("kScale_Mask", SkMatrix::TypeMask::kScale_Mask)
        .value("kAffine_Mask", SkMatrix::TypeMask::kAffine_Mask)
        .value("kPerspective_Mask", SkMatrix::TypeMask::kPerspective_Mask);
    Matrix.def("getType", &SkMatrix::getType)
        .def("isIdentity", &SkMatrix::isIdentity)
        .def("isScaleTranslate", &SkMatrix::isScaleTranslate)
        .def("isTranslate", &SkMatrix::isTranslate)
        .def("rectStaysRect", &SkMatrix::rectStaysRect)
        .def("preservesAxisAlignment", &SkMatrix::preservesAxisAlignment)
        .def("hasPerspective", &SkMatrix::hasPerspective)
        .def("isSimilarity", &SkMatrix::isSimilarity, "tol"_a = SK_ScalarNearlyZero)
        .def("preservesRightAngles", &SkMatrix::preservesRightAngles, "tol"_a = SK_ScalarNearlyZero)
        .def_readonly_static("kMScaleX", &SkMatrix::kMScaleX)
        .def_readonly_static("kMSkewX", &SkMatrix::kMSkewX)
        .def_readonly_static("kMTransX", &SkMatrix::kMTransX)
        .def_readonly_static("kMSkewY", &SkMatrix::kMSkewY)
        .def_readonly_static("kMScaleY", &SkMatrix::kMScaleY)
        .def_readonly_static("kMTransY", &SkMatrix::kMTransY)
        .def_readonly_static("kMPersp0", &SkMatrix::kMPersp0)
        .def_readonly_static("kMPersp1", &SkMatrix::kMPersp1)
        .def_readonly_static("kMPersp2", &SkMatrix::kMPersp2)
        .def_readonly_static("kAScaleX", &SkMatrix::kAScaleX)
        .def_readonly_static("kASkewY", &SkMatrix::kASkewY)
        .def_readonly_static("kASkewX", &SkMatrix::kASkewX)
        .def_readonly_static("kAScaleY", &SkMatrix::kAScaleY)
        .def_readonly_static("kATransX", &SkMatrix::kATransX)
        .def_readonly_static("kATransY", &SkMatrix::kATransY)
        .def("__getitem__", &getItem, py::is_operator(), "index"_a)
        .def("get", &SkMatrix::get, "index"_a)
        .def("rc", &SkMatrix::rc, "r"_a, "c"_a)
        .def("getScaleX", &SkMatrix::getScaleX)
        .def("getScaleY", &SkMatrix::getScaleY)
        .def("getSkewY", &SkMatrix::getSkewY)
        .def("getSkewX", &SkMatrix::getSkewX)
        .def("getTranslateX", &SkMatrix::getTranslateX)
        .def("getTranslateY", &SkMatrix::getTranslateY)
        .def("getPerspX", &SkMatrix::getPerspX)
        .def("getPerspY", &SkMatrix::getPerspY)
        .def("__setitem__", &setItem, py::is_operator(), "index"_a, "value"_a)
        .def("set", &SkMatrix::set, "index"_a, "value"_a)
        .def("setScaleX", &SkMatrix::setScaleX, "v"_a)
        .def("setScaleY", &SkMatrix::setScaleY, "v"_a)
        .def("setSkewY", &SkMatrix::setSkewY, "v"_a)
        .def("setSkewX", &SkMatrix::setSkewX, "v"_a)
        .def("setTranslateX", &SkMatrix::setTranslateX, "v"_a)
        .def("setTranslateY", &SkMatrix::setTranslateY, "v"_a)
        .def("setPerspX", &SkMatrix::setPerspX, "v"_a)
        .def("setPerspY", &SkMatrix::setPerspY, "v"_a)
        .def("setAll", &SkMatrix::setAll, "scaleX"_a, "skewX"_a, "transX"_a, "skewY"_a, "scaleY"_a, "transY"_a,
             "persp0"_a, "persp1"_a, "persp2"_a)
        .def(
            "get9",
            [](const SkMatrix &matrix)
            {
                std::vector<SkScalar> buffer(9);
                matrix.get9(buffer.data());
                return buffer;
            },
            R"doc(
                Returns nine scalar values contained by :py:class:`Matrix` into list, in member value ascending order:
                kMScaleX, kMSkewX, kMTransX, kMSkewY, kMScaleY, kMTransY, kMPersp0, kMPersp1, kMPersp2.
            )doc")
        .def(
            "set9",
            [](SkMatrix &matrix, const std::vector<SkScalar> &values)
            {
                if (values.size() != 9)
                    throw py::value_error("set9 expects 9 values.");
                return matrix.set9(values.data());
            },
            "buffer"_a)
        .def("reset", &SkMatrix::reset)
        .def("setIdentity", &SkMatrix::setIdentity)
        .def("setTranslate", py::overload_cast<SkScalar, SkScalar>(&SkMatrix::setTranslate), "dx"_a, "dy"_a)
        .def("setTranslate", py::overload_cast<const SkVector &>(&SkMatrix::setTranslate), "v"_a)
        .def("setScale", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar>(&SkMatrix::setScale), "sx"_a, "sy"_a,
             "px"_a, "py"_a)
        .def("setScale", py::overload_cast<SkScalar, SkScalar>(&SkMatrix::setScale), "sx"_a, "sy"_a)
        .def("setRotate", py::overload_cast<SkScalar, SkScalar, SkScalar>(&SkMatrix::setRotate), "degrees"_a, "px"_a,
             "py"_a)
        .def("setRotate", py::overload_cast<SkScalar>(&SkMatrix::setRotate), "degrees"_a)
        .def("setSinCos", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar>(&SkMatrix::setSinCos), "sinValue"_a,
             "cosValue"_a, "px"_a, "py"_a)
        .def("setSinCos", py::overload_cast<SkScalar, SkScalar>(&SkMatrix::setSinCos), "sinValue"_a, "cosValue"_a)
        .def("setRSXform", &SkMatrix::setRSXform, "rsxForm"_a)
        .def("setSkew", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar>(&SkMatrix::setSkew), "kx"_a, "ky"_a,
             "px"_a, "py"_a)
        .def("setSkew", py::overload_cast<SkScalar, SkScalar>(&SkMatrix::setSkew), "kx"_a, "ky"_a)
        .def("setConcat", &SkMatrix::setConcat, "a"_a, "b"_a)
        .def("preTranslate", &SkMatrix::preTranslate, "dx"_a, "dy"_a)
        .def("preScale", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar>(&SkMatrix::preScale), "sx"_a, "sy"_a,
             "px"_a, "py"_a)
        .def("preScale", py::overload_cast<SkScalar, SkScalar>(&SkMatrix::preScale), "sx"_a, "sy"_a)
        .def("preRotate", py::overload_cast<SkScalar, SkScalar, SkScalar>(&SkMatrix::preRotate), "degrees"_a, "px"_a,
             "py"_a)
        .def("preRotate", py::overload_cast<SkScalar>(&SkMatrix::preRotate), "degrees"_a)
        .def("preSkew", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar>(&SkMatrix::preSkew), "kx"_a, "ky"_a,
             "px"_a, "py"_a)
        .def("preSkew", py::overload_cast<SkScalar, SkScalar>(&SkMatrix::preSkew), "kx"_a, "ky"_a)
        .def("preConcat", &SkMatrix::preConcat, "other"_a)
        .def("__imatmul__", &SkMatrix::preConcat, py::is_operator(),
             R"doc(
                Concatenates the matrix with the *other* matrix and returns the result. This is equivalent to
                ``self.preConcat(other)``.
            )doc",
             "other"_a)
        .def("postTranslate", &SkMatrix::postTranslate, "dx"_a, "dy"_a)
        .def("postScale", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar>(&SkMatrix::postScale), "sx"_a,
             "sy"_a, "px"_a, "py"_a)
        .def("postScale", py::overload_cast<SkScalar, SkScalar>(&SkMatrix::postScale), "sx"_a, "sy"_a)
        .def("postRotate", py::overload_cast<SkScalar, SkScalar, SkScalar>(&SkMatrix::postRotate), "degrees"_a, "px"_a,
             "py"_a)
        .def("postRotate", py::overload_cast<SkScalar>(&SkMatrix::postRotate), "degrees"_a)
        .def("postSkew", py::overload_cast<SkScalar, SkScalar, SkScalar, SkScalar>(&SkMatrix::postSkew), "kx"_a, "ky"_a,
             "px"_a, "py"_a)
        .def("postSkew", py::overload_cast<SkScalar, SkScalar>(&SkMatrix::postSkew), "kx"_a, "ky"_a)
        .def("postConcat", &SkMatrix::postConcat, "other"_a)
        .def("setRectToRect", &SkMatrix::setRectToRect, "src"_a, "dst"_a, "stf"_a)
        .def_static("MakeRectToRect", &SkMatrix::MakeRectToRect, "src"_a, "dst"_a, "stf"_a)
        .def(
            "setPolyToPoly",
            [](SkMatrix &matrix, const std::vector<SkPoint> &src, const std::vector<SkPoint> &dst)
            {
                if (src.size() != dst.size())
                    throw py::value_error("src and dst must have the same size.");
                return matrix.setPolyToPoly(src.data(), dst.data(), src.size());
            },
            "src"_a, "dst"_a)
        .def("invert", &SkMatrix::invert, "inverse"_a)
        .def(
            "makeInverse",
            [](const SkMatrix &matrix)
            {
                SkMatrix inverse;
                if (matrix.invert(&inverse))
                    return inverse;
                throw py::value_error("Matrix is not invertible.");
            },
            R"doc(
                Returns the inverse of the matrix. If the matrix is singular, throws a ValueError.

                :return: The inverse of the matrix.
            )doc")
        .def_static(
            "SetAffineIdentity",
            []()
            {
                std::vector<SkScalar> affine(6);
                SkMatrix::SetAffineIdentity(affine.data());
                return affine;
            },
            R"doc(
                Returns affine with identity values in column major order. Sets affine to:

                    | 1 0 0 |
                    | 0 1 0 |

                :return: list of 6 floats
            )doc")
        .def(
            "asAffine",
            [](const SkMatrix &self) -> std::optional<std::vector<SkScalar>>
            {
                std::vector<SkScalar> affine(6);
                if (self.asAffine(affine.data()))
                    return affine;
                return std::nullopt;
            },
            R"doc(
                Returns affine in column major order. Sets affine to:

                    | scale-x  skew-x translate-x |
                    | skew-y  scale-y translate-y |
                
                If :py:class:`Matrix` contains perspective, returns ``None``.

                :return: list of 6 floats or ``None``
                :rtype: list | None
            )doc")
        .def(
            "setAffine",
            [](SkMatrix &matrix, const std::vector<SkScalar> &affine)
            {
                if (affine.size() != 6)
                    throw py::value_error("affine must have 6 elements.");
                return matrix.setAffine(affine.data());
            },
            "affine"_a)
        .def("normalizePerspective", &SkMatrix::normalizePerspective)
        .def(
            "mapPoints",
            [](const SkMatrix &matrix, std::vector<SkPoint> &pts)
            {
                matrix.mapPoints(pts.data(), pts.size());
                return pts;
            },
            R"doc(
                Maps *src* list of :py:class:`Point` and returns a new list of :py:class:`Point`.

                :param src: list of :py:class:`Point` to transform
                :return: list of mapped :py:class:`Point`
            )doc",
            "pts"_a)
        .def(
            "mapHomogeneousPoints",
            [](const SkMatrix &matrix, std::vector<SkPoint3> &src)
            {
                matrix.mapHomogeneousPoints(src.data(), src.data(), src.size());
                return src;
            },
            R"doc(
                Maps *src* list of :py:class:`Point3` and returns a new list of :py:class:`Point3`.

                :param src: list of :py:class:`Point3` to transform
                :return: list of mapped :py:class:`Point3`
            )doc",
            "src"_a)
        .def(
            "mapHomogeneousPoints",
            [](const SkMatrix &matrix, const std::vector<SkPoint> &src)
            {
                std::vector<SkPoint3> dst(src.size());
                matrix.mapHomogeneousPoints(dst.data(), src.data(), src.size());
                return dst;
            },
            "Returns homogeneous points, starting with 2D src points (with implied w = 1).", "src"_a)
        .def("mapPoint", &SkMatrix::mapPoint, "pt"_a)
        .def("mapXY", py::overload_cast<SkScalar, SkScalar>(&SkMatrix::mapXY, py::const_), "x"_a, "y"_a)
        .def("mapOrigin", &SkMatrix::mapOrigin)
        .def(
            "mapVectors",
            [](const SkMatrix &matrix, std::vector<SkVector> &vecs)
            {
                matrix.mapVectors(vecs.data(), vecs.size());
                return vecs;
            },
            R"doc(
                Maps *vecs* list of :py:class:`Point` and returns a new list of :py:class:`Point`, multiplying each
                vector by :py:class:`Matrix`, treating translation as zero.

                :param vecs: list of :py:class:`Point` to transform
                :return: list of transformed :py:class:`Point`
            )doc",
            "vecs"_a)
        .def("mapVector", py::overload_cast<SkScalar, SkScalar>(&SkMatrix::mapVector, py::const_), "dx"_a, "dy"_a)
        .def("mapRect", py::overload_cast<const SkRect &, SkApplyPerspectiveClip>(&SkMatrix::mapRect, py::const_),
             "src"_a, "pc"_a = SkApplyPerspectiveClip::kYes)
        .def(
            "mapRectToQuad",
            [](const SkMatrix &matrix, const SkRect &rect)
            {
                std::vector<SkPoint> dst(4);
                matrix.mapRectToQuad(dst.data(), rect);
                return dst;
            },
            R"doc(
                Maps four corners of *rect* to a list of 4 :py:class:`Point`.

                :param rect: :py:class:`Rect` to map
                :return: mapped corner :py:class:`Point`
            )doc",
            "rect"_a)
        .def(
            "mapRectScaleTranslate",
            [](const SkMatrix &matrix, const SkRect &src)
            {
                SkRect dst;
                matrix.mapRectScaleTranslate(&dst, src);
                return dst;
            },
            R"doc(
                Returns bounds of src corners mapped by :py:class:`Matrix`.

                :param src: :py:class:`Rect` to map
                :return: bounds of mapped :py:class:`Point`
            )doc",
            "src"_a)
        .def("mapRadius", &SkMatrix::mapRadius, "radius"_a)
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def("dump",
             [](const SkMatrix &self)
             {
                 py::scoped_ostream_redirect stream;
                 self.dump();
             })
        .def("getMinScale", &SkMatrix::getMinScale)
        .def("getMaxScale", &SkMatrix::getMaxScale)
        .def(
            "getMinMaxScales",
            [](const SkMatrix &self) -> std::optional<py::tuple>
            {
                SkScalar scaleFactors[2];
                if (self.getMinMaxScales(scaleFactors))
                    return py::make_tuple(scaleFactors[0], scaleFactors[1]);
                return std::nullopt;
            },
            R"doc(
                Returns a tuple of (minimum scaling factor, maximum scaling factor). Return ``None`` if scale factors
                are not found.

                :return: minimum and maximum scale factors
                :rtype: (float, float) | None
            )doc")
        .def(
            "decomposeScale",
            [](const SkMatrix &self) -> std::optional<py::tuple>
            {
                SkSize scale;
                SkMatrix remaining;
                if (self.decomposeScale(&scale, &remaining))
                    return py::make_tuple(scale, remaining);
                return std::nullopt;
            },
            R"doc(
                Decomposes :py:class:`Matrix` into scale components and whatever remains. Returns ``None`` if
                :py:class:`Matrix` could not be decomposed.
                
                :return: tuple of (axes scaling factors, :py:class:`Matrix` without scaling) or ``None``
                :rtype: (:py:class:`Size`, :py:class:`Matrix`) | None
            )doc")
        .def_static("I", &SkMatrix::I)
        .def_static("InvalidMatrix", &SkMatrix::InvalidMatrix)
        .def_static("Concat", &SkMatrix::Concat, "a"_a, "b"_a)
        .def(
            "__matmul__", [](const SkMatrix &matrix, const SkMatrix &other) { return matrix * other; },
            py::is_operator(),
            "Returns the result of multiplying this :py:class:`Matrix` by *other*. Same as :py:meth:`Matrix.Concat`.",
            "other"_a)
        .def("dirtyMatrixTypeCache", &SkMatrix::dirtyMatrixTypeCache)
        .def("setScaleTranslate", &SkMatrix::setScaleTranslate, "sx"_a, "sy"_a, "tx"_a, "ty"_a)
        .def("isFinite", &SkMatrix::isFinite)
        .def("__str__",
             [](const SkMatrix &matrix)
             {
                 return "Matrix(({}, {}, {}), ({}, {}, {}), ({}, {}, {}))"_s.format(
                     matrix[0], matrix[1], matrix[2], matrix[3], matrix[4], matrix[5], matrix[6], matrix[7], matrix[8]);
             });

    py::implicitly_convertible<ndarray, SkMatrix>();
}