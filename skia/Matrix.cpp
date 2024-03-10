#include "common.h"
#include "include/core/SkM44.h"
#include "include/core/SkMatrix.h"
#include "include/core/SkPoint3.h"
#include "include/core/SkRSXform.h"
#include <pybind11/iostream.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>

typedef py::array_t<SkScalar> ndarray;

SkScalar Matrix_getItem(const SkMatrix &self, int index)
{
    if (index < 0 || 9 <= index)
        throw py::index_error("Index out of range.");
    return self[index];
}
void Matrix_setItem(SkMatrix &self, int index, SkScalar value)
{
    if (index < 0 || 9 <= index)
        throw py::index_error("Index out of range.");
    self[index] = value;
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
                std::array<SkPoint, 4> quad;
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
                std::array<SkPoint, 4> quad;
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
                std::array<SkPoint, 4> strip;
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
        .def("__getitem__", &Matrix_getItem, py::is_operator(), "index"_a)
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
        .def("__setitem__", &Matrix_setItem, py::is_operator(), "index"_a, "value"_a)
        .def("set", &SkMatrix::set, "index"_a, "value"_a)
        .def(
            "setFromMatrix",
            [](SkMatrix &self, const SkMatrix &src)
            {
                src.get9(&self[0]);
                self.dirtyMatrixTypeCache();
            },
            "Sets the values from the given matrix.", "src"_a)
        .def(
            "setFromM44",
            [](SkMatrix &self, const SkM44 &src)
            {
                self.setAll(src.rc(0, 0), src.rc(0, 1), src.rc(0, 3), src.rc(1, 0), src.rc(1, 1), src.rc(1, 3),
                            src.rc(3, 0), src.rc(3, 1), src.rc(3, 3));
            },
            "Sets the values from the given py::class:`M44`.", "src"_a)
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
                std::array<SkScalar, 9> buffer;
                matrix.get9(buffer.data());
                return buffer;
            },
            R"doc(
                Returns nine scalar values contained by :py:class:`Matrix` into list, in member value ascending order:
                kMScaleX, kMSkewX, kMTransX, kMSkewY, kMScaleY, kMTransY, kMPersp0, kMPersp1, kMPersp2.
            )doc")
        .def(
            "set9", [](SkMatrix &matrix, const std::array<SkScalar, 9> &values) { return matrix.set9(values.data()); },
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
                std::array<SkScalar, 6> affine;
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
            [](const SkMatrix &self) -> std::optional<std::array<SkScalar, 6>>
            {
                std::array<SkScalar, 6> affine;
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
            [](SkMatrix &matrix, const std::array<SkScalar, 6> &affine) { return matrix.setAffine(affine.data()); },
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
                std::array<SkPoint, 4> dst;
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

    py::class_<SkM44> M44(m, "M44");
    M44.def(py::init<const SkM44 &>(), "src"_a)
        .def(py::init())
        .def(py::init<const SkM44 &, const SkM44 &>(), "a"_a, "b"_a);

    py::enum_<SkM44::Uninitialized_Constructor>(M44, "Uninitialized_Constructor")
        .value("kUninitialized_Constructor", SkM44::Uninitialized_Constructor::kUninitialized_Constructor);
    M44.def(py::init<SkM44::Uninitialized_Constructor>());

    py::enum_<SkM44::NaN_Constructor>(M44, "NaN_Constructor")
        .value("kNaN_Constructor", SkM44::NaN_Constructor::kNaN_Constructor);
    M44.def(py::init<SkM44::NaN_Constructor>())
        .def(py::init([](const SkScalar &m0, const SkScalar &m4, const SkScalar &m8, const SkScalar &m12,
                         const SkScalar &m1, const SkScalar &m5, const SkScalar &m9, const SkScalar &m13,
                         const SkScalar &m2, const SkScalar &m6, const SkScalar &m10, const SkScalar &m14,
                         const SkScalar &m3, const SkScalar &m7, const SkScalar &m11, const SkScalar &m15)
                      { return SkM44(m0, m4, m8, m12, m1, m5, m9, m13, m2, m6, m10, m14, m3, m7, m11, m15); }),
             "m0"_a, "m4"_a, "m8"_a, "m12"_a, "m1"_a, "m5"_a, "m9"_a, "m13"_a, "m2"_a, "m6"_a, "m10"_a, "m14"_a, "m3"_a,
             "m7"_a, "m11"_a, "m15"_a)
        .def_static(
            "Rows",
            [](const std::array<float, 4> &r0, const std::array<float, 4> &r1, const std::array<float, 4> &r2,
               const std::array<float, 4> &r3)
            {
                return SkM44::Rows({r0[0], r0[1], r0[2], r0[3]}, {r1[0], r1[1], r1[2], r1[3]},
                                   {r2[0], r2[1], r2[2], r2[3]}, {r3[0], r3[1], r3[2], r3[3]});
            },
            "Creates a :py:class:`M44` from 4 rows of 4 floats.", "r0"_a, "r1"_a, "r2"_a, "r3"_a)
        .def_static(
            "Cols",
            [](const std::array<float, 4> &c0, const std::array<float, 4> &c1, const std::array<float, 4> &c2,
               const std::array<float, 4> &c3)
            {
                return SkM44::Cols({c0[0], c0[1], c0[2], c0[3]}, {c1[0], c1[1], c1[2], c1[3]},
                                   {c2[0], c2[1], c2[2], c2[3]}, {c3[0], c3[1], c3[2], c3[3]});
            },
            "Creates a :py:class:`M44` from 4 columns of 4 floats.", "c0"_a, "c1"_a, "c2"_a, "c3"_a)
        .def_static(
            "RowMajor", [](const std::array<float, 4> &r) { return SkM44::RowMajor(r.data()); }, "r"_a)
        .def(py::init(
                 [](const ndarray &array)
                 {
                     if (array.size() != 16)
                         throw py::value_error("Matrix must be a 4x4 matrix.");
                     return SkM44::RowMajor(array.data());
                 }),
             "Creates a :py:class:`M44` from 4x4 float32 NumPy array.", "array"_a)
        .def_static(
            "ColMajor", [](const std::array<float, 4> &c) { return SkM44::ColMajor(c.data()); }, "c"_a)
        .def_static("Translate", SkM44::Translate, "x"_a, "y"_a, "z"_a = 0)
        .def_static("Scale", SkM44::Scale, "x"_a, "y"_a, "z"_a = 1)
        .def_static(
            "Rotate",
            [](const std::array<float, 3> &axis, const SkScalar &radians) {
                return SkM44::Rotate({axis[0], axis[1], axis[2]}, radians);
            },
            "Creates a :py:class:`M44` from a 3D axis represented as a list and angle.", "axis"_a, "radians"_a)
        .def_static(
            "Rotate",
            [](const SkScalar &x, const SkScalar &y, const SkScalar &z, const SkScalar &radians) {
                return SkM44::Rotate(SkV3{x, y, z}, radians);
            },
            "Creates a :py:class:`M44` from a 3D axis represented as 3 scalars and an angle.", "x"_a, "y"_a, "z"_a,
            "radians"_a)
        .def_static("RectToRect", SkM44::RectToRect, "src"_a, "dst"_a)
        .def_static(
            "LookAt",
            [](const std::array<float, 3> &eye, const std::array<float, 3> &center, const std::array<float, 3> &up) {
                return SkM44::LookAt({eye[0], eye[1], eye[2]}, {center[0], center[1], center[2]},
                                     {up[0], up[1], up[2]});
            },
            "Creates a look-at :py:class:`M44` from an eye, center, and up vector.", "eye"_a, "center"_a, "up"_a)
        .def_static("Perspective", SkM44::Perspective, "near"_a, "far"_a, "angle"_a)
        .def_static(
            "Perspective",
            [](const SkScalar &depth)
            {
                SkM44 m;
                m.setRC(3, 2, -1 / depth);
                return m;
            },
            "Creates a perspective :py:class:`M44` from a *depth*.", "depth"_a)
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def(
            "getColMajor",
            [](const SkM44 &self)
            {
                std::array<SkScalar, 16> v;
                self.getColMajor(v.data());
                return v;
            },
            "Returns the matrix in column-major order.")
        .def(
            "getRowMajor",
            [](const SkM44 &self)
            {
                std::array<SkScalar, 16> v;
                self.getRowMajor(v.data());
                return v;
            },
            "Returns the matrix in row-major order.")
        .def("rc", &SkM44::rc, "r"_a, "c"_a)
        .def(
            "__getitem__",
            [](const SkM44 &self, const py::tuple &index)
            {
                if (index.size() != 2)
                    throw py::index_error("Index must be a 2-tuple.");
                return self.rc(index[0].cast<int>(), index[1].cast<int>());
            },
            py::is_operator())
        .def("setRC", &SkM44::setRC, "r"_a, "c"_a, "value"_a)
        .def(
            "__setitem__",
            [](SkM44 &self, const py::tuple &index, const SkScalar &value)
            {
                if (index.size() != 2)
                    throw py::index_error("Index must be a 2-tuple.");
                self.setRC(index[0].cast<int>(), index[1].cast<int>(), value);
            },
            py::is_operator())
        .def(
            "row",
            [](const SkM44 &self, const int &i)
            {
                auto row = self.row(i);
                return std::array{row.x, row.y, row.z, row.w};
            },
            "Returns the *i*-th row as a list.", "i"_a)
        .def(
            "col",
            [](const SkM44 &self, const int &i)
            {
                auto col = self.col(i);
                return std::array{col.x, col.y, col.z, col.w};
            },
            "Returns the *i*-th column as a list.", "i"_a)
        .def(
            "setRow",
            [](SkM44 &self, const int &i, const std::array<float, 4> &v) {
                self.setRow(i, {v[0], v[1], v[2], v[3]});
            },
            "Sets the *i*-th row from a list.", "i"_a, "v"_a)
        .def(
            "setCol",
            [](SkM44 &self, const int &i, const std::array<float, 4> &v) {
                self.setCol(i, {v[0], v[1], v[2], v[3]});
            },
            "Sets the *i*-th column from a list.", "i"_a, "v"_a)
        .def("setIdentity", &SkM44::setIdentity)
        .def("setTranslate", &SkM44::setTranslate, "x"_a, "y"_a, "z"_a = 0)
        .def("setScale", &SkM44::setScale, "x"_a, "y"_a, "z"_a = 1)
        .def(
            "setRotateUnitSinCos",
            [](SkM44 &self, const std::array<float, 3> &axis, const SkScalar &sinAngle, const SkScalar &cosAngle) {
                return self.setRotateUnitSinCos({axis[0], axis[1], axis[2]}, sinAngle, cosAngle);
            },
            "Set this matrix to rotate about the specified unit-length axis list, by an angle specified by its sin() "
            "and cos().",
            "axis"_a, "sinAngle"_a, "cosAngle"_a)
        .def(
            "setRotateUnit",
            [](SkM44 &self, const std::array<float, 3> &axis, const SkScalar &radians) {
                return self.setRotateUnit({axis[0], axis[1], axis[2]}, radians);
            },
            "Set this matrix to rotate about the specified unit-length axis list, by an angle specified in radians.",
            "axis"_a, "radians"_a)
        .def(
            "setRotate",
            [](SkM44 &self, const std::array<float, 3> &axis, const SkScalar &radians) {
                return self.setRotate({axis[0], axis[1], axis[2]}, radians);
            },
            "Set this matrix to rotate about the specified axis list, by an angle specified in radians.", "axis"_a,
            "radians"_a)
        .def("setConcat", &SkM44::setConcat, "a"_a, "b"_a)
        .def(py::self * py::self)
        .def("preConcat", py::overload_cast<const SkM44 &>(&SkM44::preConcat), "m"_a)
        .def("postConcat", &SkM44::postConcat, "m"_a)
        .def("normalizePerspective", &SkM44::normalizePerspective)
        .def("isFinite", &SkM44::isFinite)
        .def("invert", &SkM44::invert, "inverse"_a)
        .def(
            "makeInverse",
            [](const SkM44 &self)
            {
                SkM44 inverse;
                if (self.invert(&inverse))
                    return inverse;
                throw py::value_error("Matrix is not invertible.");
            },
            "Returns the inverse of this matrix.")
        .def("transpose", &SkM44::transpose)
        .def("dump", &SkM44::dump)
        .def(
            "map",
            [](const SkM44 &self, const float &x, const float &y, const float &z, const float &w)
            {
                auto v4 = self.map(x, y, z, w);
                return std::array{v4.x, v4.y, v4.z, v4.w};
            },
            "Returns the matrix-vector (size 4) product.", "x"_a, "y"_a, "z"_a, "w"_a)
        .def(
            "__mul__",
            [](const SkM44 &self, const std::array<float, 4> &v)
            {
                auto v4 = self * SkV4{v[0], v[1], v[2], v[3]};
                return std::array{v4.x, v4.y, v4.z, v4.w};
            },
            py::is_operator(), "Returns the matrix-vector (size 4) product.")
        .def(
            "__mul__",
            [](const SkM44 &self, const std::array<float, 3> &v)
            {
                auto v3 = self * SkV3{v[0], v[1], v[2]};
                return std::array{v3.x, v3.y, v3.z};
            },
            py::is_operator(), "Returns the matrix-vector (size 3) product.")
        .def("asM33", &SkM44::asM33)
        .def(py::init<const SkMatrix &>(), "src"_a)
        .def("preTranslate", &SkM44::preTranslate, "x"_a, "y"_a, "z"_a = 0)
        .def("postTranslate", &SkM44::postTranslate, "x"_a, "y"_a, "z"_a = 0)
        .def("preScale", py::overload_cast<SkScalar, SkScalar>(&SkM44::preScale), "x"_a, "y"_a)
        .def("preScale", py::overload_cast<SkScalar, SkScalar, SkScalar>(&SkM44::preScale), "x"_a, "y"_a, "z"_a)
        .def("preConcat", py::overload_cast<const SkMatrix &>(&SkM44::preConcat), "b"_a)
        .def("__str__",
             [](const SkM44 &self)
             {
                 return "M44(({}, {}, {}, {}), ({}, {}, {}, {}), ({}, {}, {}, {}), ({}, {}, {}, {}))"_s.format(
                     self.rc(0, 0), self.rc(0, 1), self.rc(0, 2), self.rc(0, 3), self.rc(1, 0), self.rc(1, 1),
                     self.rc(1, 2), self.rc(1, 3), self.rc(2, 0), self.rc(2, 1), self.rc(2, 2), self.rc(2, 3),
                     self.rc(3, 0), self.rc(3, 1), self.rc(3, 2), self.rc(3, 3));
             });
}