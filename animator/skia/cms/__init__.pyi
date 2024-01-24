"""
This module provides an interface to the Skia CMS library. Every function in the library is exposed as a static method
(constructor) or as a class method of some class. Usually of the class corresponding to the type of the first parameter
of the function.
"""
from __future__ import annotations

import typing

import numpy

import animator.skia

buffer = bytes | memoryview | bytearray | numpy.ndarray

__all__ = [
    'A2B',
    'AlphaFormat',
    'B2A',
    'CICP',
    'Curve',
    'ICCProfile',
    'Matrix3x3',
    'Matrix3x4',
    'PixelFormat',
    'Signature',
    'TFType',
    'TransferFunction',
    'WriteICCProfile',
    'disableRuntimeCPUDetection',
    'transform',
]

class A2B:
    """
    :warning: Indexed assignment to array attributes will not work. Instead assign to the whole
        array. This will cause a memory copy. Instead of doing ``a2b.input_curves[0] = curve``,
        do ``a2b.input_curves = [curve, *a2b.input_curves[1:]]``.
    """

    grid_16: int
    grid_8: int
    grid_points: list[int]
    input_channels: int
    input_curves: list[Curve]
    matrix: Matrix3x4
    matrix_channels: int
    matrix_curves: list[Curve]
    output_channels: int
    output_curves: list[Curve]
    def __init__(self) -> None: ...

class AlphaFormat:
    """
    Members:

      Opaque

      Unpremul

      PremulAsEncoded
    """

    Opaque: typing.ClassVar[AlphaFormat]  # value = <AlphaFormat.Opaque: 0>
    PremulAsEncoded: typing.ClassVar[AlphaFormat]  # value = <AlphaFormat.PremulAsEncoded: 2>
    Unpremul: typing.ClassVar[AlphaFormat]  # value = <AlphaFormat.Unpremul: 1>
    __members__: typing.ClassVar[
        dict[str, AlphaFormat]
    ]  # value = {'Opaque': <AlphaFormat.Opaque: 0>, 'Unpremul': <AlphaFormat.Unpremul: 1>, 'PremulAsEncoded': <AlphaFormat.PremulAsEncoded: 2>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class B2A:
    """
    :warning: Indexed assignment to array attributes will not work. Instead assign to the whole
        array. This will cause a memory copy. Instead of doing ``b2a.input_curves[0] = curve``,
        do ``b2a.input_curves = [curve, *b2a.input_curves[1:]]``.
    """

    grid_16: int
    grid_8: int
    grid_points: list[int]
    input_channels: int
    input_curves: list[Curve]
    matrix: Matrix3x4
    matrix_channels: int
    matrix_curves: list[Curve]
    output_channels: int
    output_curves: list[Curve]
    def __init__(self) -> None: ...

class CICP:
    color_primaries: int
    matrix_coefficients: int
    transfer_characteristics: int
    video_full_range_flag: int
    def __init__(self) -> None: ...

class Curve:
    alias_of_table_entries: int
    parametric: TransferFunction
    table_16: int
    table_8: int
    table_entries: int
    def __init__(self) -> None: ...
    def approximateCurve(self) -> tuple:
        """
        Approximate the curve with a transfer function.

        :return: A tuple of the approximated transfer function and the maximum error.
        :rtype: (TransferFunction, float)
        """
    def areApproximateInverses(self, inv_tf: TransferFunction) -> bool:
        """
        Practical test that answers: Is curve roughly the inverse of *inv_tf*? Typically used by passing the
        inverse of a known parametric transfer function (like sRGB), to determine if a particular curve is
        very close to sRGB.
        """

class ICCProfile:
    __hash__: typing.ClassVar[None] = None
    A2B: A2B
    B2A: B2A
    CICP: CICP
    data_color_space: int
    has_A2B: bool
    has_B2A: bool
    has_CICP: bool
    has_toXYZD50: bool
    has_trc: bool
    pcs: int
    size: int
    tag_count: int
    toXYZD50: Matrix3x3
    @staticmethod
    def Parse(buf: buffer) -> ICCProfile:
        """
        Parse an ICC profile from a buffer.

        :param buffer: The buffer containing the ICC profile.
        :return: The parsed ICC profile.
        """
    @staticmethod
    def ParseWithA2BPriority(buf: buffer, priority: list[int]) -> ICCProfile:
        """
        Parse an ICC profile from a buffer.

        :param buffer: The buffer containing the ICC profile.
        :param priority: Selects an A2B profile (if present) according to priority list (each entry 0-2).
        :return: The parsed ICC profile.
        """
    @staticmethod
    def XYZD50_profile() -> ICCProfile: ...
    @staticmethod
    def sRGB_profile() -> ICCProfile: ...
    def TRCs_AreApproximateInverse(self, inv_tf: TransferFunction) -> bool:
        """
        Similar to :py:meth:`Curve.areApproximateInverse`, answering the question for all three TRC curves of
        the profile. Again, passing skcms_sRGB_InverseTransferFunction as *inv_tf* will answer the question:
        "Does this profile have a transfer function that is very close to sRGB?"
        """
    def __eq__(self, other: ICCProfile) -> bool:
        """
        Same as :py:meth:`~ICCProfile.approximatelyEqualProfiles`.
        """
    def __init__(self) -> None: ...
    def approximatelyEqualProfiles(self, other: ICCProfile) -> bool:
        """
        Practical equality test for two :py:class:`ICCProfile`.
        """
    def getCHAD(self) -> Matrix3x3:
        """
        :return: The color hue and chroma adjustment matrix.
        :rtype: :py:class:`Matrix3x3`
        """
    def getWTPT(self) -> list[float]:
        """
        :return: The white point of the profile.
        :rtype: :py:class:`Matrix3x3`
        """
    def makeUsableAsDestination(self) -> bool: ...
    def makeUsableAsDestinationWithSingleCurve(self) -> bool: ...
    def setTransferFunction(self, tf: TransferFunction) -> None: ...
    def setXYZD50(self, m: Matrix3x3) -> None: ...
    def writeICCProfile(self, description: str) -> animator.skia.Data: ...
    @property
    def buffer(self) -> memoryview | None:
        """
        The ICC profile buffer represented as a :py:class:`memoryview`.

        :note: A reference to the profile is needed to keep the buffer alive.
        """
    @property
    def trc(self) -> list[Curve]:
        """
        :warning: Indexed assignment to this attributes will not work. Instead assign to the whole array. This will
        cause a memory copy. Instead of doing ``profile.trc[0] = curve``, do ``profile.trc = [curve,
        *profile.trc[1:]]``.
        """
    @trc.setter
    def trc(self, arg1: list[Curve]) -> None: ...

class Matrix3x3:
    @staticmethod
    def AdaptToXYZD50(wx: float, wy: float) -> Matrix3x3: ...
    @staticmethod
    def PrimariesToXYZD50(
        rx: float, ry: float, gx: float, gy: float, bx: float, by: float, wx: float, wy: float
    ) -> Matrix3x3: ...
    def __getitem__(self, index: tuple) -> float:
        """
        Returns the value of the matrix at the given index (2-tuple). Use as mat[row][column].

        :param index: The index (row, column) of the value to return.
        :return: The value at the given index.
        """
    @typing.overload
    def __init__(self) -> None:
        """
        Create a new identity Matrix3x3.
        """
    @typing.overload
    def __init__(
        self, a: float, b: float, c: float, d: float, e: float, f: float, g: float, h: float, i: float
    ) -> None:
        """
        Create a new Matrix3x3 with the given values.
        """
    @typing.overload
    def __init__(self, values: list[list[float]]) -> None:
        """
        Create a new Matrix3x3 with the given values.

        :param values: A list of 3 rows, each of which is a list of 3 values.
        """
    def __setitem__(self, index: tuple, value: float) -> None:
        """
        Sets the value of the matrix at the given index (2-tuple). Use as mat[row][column] = value.

        :param index: The index (row, column) of the value to set.
        :param value: The value to set.
        """
    def __str__(self) -> str: ...
    def concat(self, other: Matrix3x3) -> Matrix3x3: ...
    def invert(self) -> Matrix3x3:
        """
        Returns the inverse of the matrix, or raises ValueError if the matrix is not invertible.

        :return: The inverse of the matrix.
        """

class Matrix3x4:
    def __getitem__(self, index: tuple) -> float:
        """
        Returns the value of the matrix at the given index (2-tuple). Use as mat[row][column].

        :param index: The index (row, column) of the value to return.
        :return: The value at the given index.
        """
    @typing.overload
    def __init__(self) -> None:
        """
        Create a new identity Matrix3x4.
        """
    @typing.overload
    def __init__(
        self,
        a: float,
        b: float,
        c: float,
        d: float,
        e: float,
        f: float,
        g: float,
        h: float,
        i: float,
        j: float,
        k: float,
        l: float,
    ) -> None:
        """
        Create a new Matrix3x4 with the given values.
        """
    @typing.overload
    def __init__(self, values: list[list[float]]) -> None:
        """
        Create a new Matrix3x4 with the given values.

        :param values: A list of 3 lists of 4 values.
        """
    def __setitem__(self, index: tuple, value: float) -> None:
        """
        Sets the value of the matrix at the given index (2-tuple). Use as mat[row][column] = value.

        :param index: The index (row, column) of the value to set.
        :param value: The value to set.
        """
    def __str__(self) -> str: ...

class PixelFormat:
    """
    Members:

      A_8

      A_8_

      G_8

      G_8_

      RGB_565

      BGR_565

      ABGR_4444

      ARGB_4444

      RGB_888

      BGR_888

      RGBA_8888

      BGRA_8888

      RGBA_8888_sRGB

      BGRA_8888_sRGB

      RGBA_1010102

      BGRA_1010102

      RGB_161616LE

      BGR_161616LE

      RGBA_16161616LE

      BGRA_16161616LE

      RGB_161616BE

      BGR_161616BE

      RGBA_16161616BE

      BGRA_16161616BE

      RGB_hhh_Norm

      BGR_hhh_Norm

      RGBA_hhhh_Norm

      BGRA_hhhh_Norm

      RGB_hhh

      BGR_hhh

      RGBA_hhhh

      BGRA_hhhh

      RGB_fff

      BGR_fff

      RGBA_ffff

      BGRA_ffff

      RGB_101010x_XR

      BGR_101010x_XR
    """

    ABGR_4444: typing.ClassVar[PixelFormat]  # value = <PixelFormat.ABGR_4444: 6>
    ARGB_4444: typing.ClassVar[PixelFormat]  # value = <PixelFormat.ARGB_4444: 7>
    A_8: typing.ClassVar[PixelFormat]  # value = <PixelFormat.A_8: 0>
    A_8_: typing.ClassVar[PixelFormat]  # value = <PixelFormat.A_8_: 1>
    BGRA_1010102: typing.ClassVar[PixelFormat]  # value = <PixelFormat.BGRA_1010102: 15>
    BGRA_16161616BE: typing.ClassVar[PixelFormat]  # value = <PixelFormat.BGRA_16161616BE: 23>
    BGRA_16161616LE: typing.ClassVar[PixelFormat]  # value = <PixelFormat.BGRA_16161616LE: 19>
    BGRA_8888: typing.ClassVar[PixelFormat]  # value = <PixelFormat.BGRA_8888: 11>
    BGRA_8888_sRGB: typing.ClassVar[PixelFormat]  # value = <PixelFormat.BGRA_8888_sRGB: 13>
    BGRA_ffff: typing.ClassVar[PixelFormat]  # value = <PixelFormat.BGRA_ffff: 35>
    BGRA_hhhh: typing.ClassVar[PixelFormat]  # value = <PixelFormat.BGRA_hhhh: 31>
    BGRA_hhhh_Norm: typing.ClassVar[PixelFormat]  # value = <PixelFormat.BGRA_hhhh_Norm: 27>
    BGR_101010x_XR: typing.ClassVar[PixelFormat]  # value = <PixelFormat.BGR_101010x_XR: 37>
    BGR_161616BE: typing.ClassVar[PixelFormat]  # value = <PixelFormat.BGR_161616BE: 21>
    BGR_161616LE: typing.ClassVar[PixelFormat]  # value = <PixelFormat.BGR_161616LE: 17>
    BGR_565: typing.ClassVar[PixelFormat]  # value = <PixelFormat.BGR_565: 5>
    BGR_888: typing.ClassVar[PixelFormat]  # value = <PixelFormat.BGR_888: 9>
    BGR_fff: typing.ClassVar[PixelFormat]  # value = <PixelFormat.BGR_fff: 33>
    BGR_hhh: typing.ClassVar[PixelFormat]  # value = <PixelFormat.BGR_hhh: 29>
    BGR_hhh_Norm: typing.ClassVar[PixelFormat]  # value = <PixelFormat.BGR_hhh_Norm: 25>
    G_8: typing.ClassVar[PixelFormat]  # value = <PixelFormat.G_8: 2>
    G_8_: typing.ClassVar[PixelFormat]  # value = <PixelFormat.G_8_: 3>
    RGBA_1010102: typing.ClassVar[PixelFormat]  # value = <PixelFormat.RGBA_1010102: 14>
    RGBA_16161616BE: typing.ClassVar[PixelFormat]  # value = <PixelFormat.RGBA_16161616BE: 22>
    RGBA_16161616LE: typing.ClassVar[PixelFormat]  # value = <PixelFormat.RGBA_16161616LE: 18>
    RGBA_8888: typing.ClassVar[PixelFormat]  # value = <PixelFormat.RGBA_8888: 10>
    RGBA_8888_sRGB: typing.ClassVar[PixelFormat]  # value = <PixelFormat.RGBA_8888_sRGB: 12>
    RGBA_ffff: typing.ClassVar[PixelFormat]  # value = <PixelFormat.RGBA_ffff: 34>
    RGBA_hhhh: typing.ClassVar[PixelFormat]  # value = <PixelFormat.RGBA_hhhh: 30>
    RGBA_hhhh_Norm: typing.ClassVar[PixelFormat]  # value = <PixelFormat.RGBA_hhhh_Norm: 26>
    RGB_101010x_XR: typing.ClassVar[PixelFormat]  # value = <PixelFormat.RGB_101010x_XR: 36>
    RGB_161616BE: typing.ClassVar[PixelFormat]  # value = <PixelFormat.RGB_161616BE: 20>
    RGB_161616LE: typing.ClassVar[PixelFormat]  # value = <PixelFormat.RGB_161616LE: 16>
    RGB_565: typing.ClassVar[PixelFormat]  # value = <PixelFormat.RGB_565: 4>
    RGB_888: typing.ClassVar[PixelFormat]  # value = <PixelFormat.RGB_888: 8>
    RGB_fff: typing.ClassVar[PixelFormat]  # value = <PixelFormat.RGB_fff: 32>
    RGB_hhh: typing.ClassVar[PixelFormat]  # value = <PixelFormat.RGB_hhh: 28>
    RGB_hhh_Norm: typing.ClassVar[PixelFormat]  # value = <PixelFormat.RGB_hhh_Norm: 24>
    __members__: typing.ClassVar[
        dict[str, PixelFormat]
    ]  # value = {'A_8': <PixelFormat.A_8: 0>, 'A_8_': <PixelFormat.A_8_: 1>, 'G_8': <PixelFormat.G_8: 2>, 'G_8_': <PixelFormat.G_8_: 3>, 'RGB_565': <PixelFormat.RGB_565: 4>, 'BGR_565': <PixelFormat.BGR_565: 5>, 'ABGR_4444': <PixelFormat.ABGR_4444: 6>, 'ARGB_4444': <PixelFormat.ARGB_4444: 7>, 'RGB_888': <PixelFormat.RGB_888: 8>, 'BGR_888': <PixelFormat.BGR_888: 9>, 'RGBA_8888': <PixelFormat.RGBA_8888: 10>, 'BGRA_8888': <PixelFormat.BGRA_8888: 11>, 'RGBA_8888_sRGB': <PixelFormat.RGBA_8888_sRGB: 12>, 'BGRA_8888_sRGB': <PixelFormat.BGRA_8888_sRGB: 13>, 'RGBA_1010102': <PixelFormat.RGBA_1010102: 14>, 'BGRA_1010102': <PixelFormat.BGRA_1010102: 15>, 'RGB_161616LE': <PixelFormat.RGB_161616LE: 16>, 'BGR_161616LE': <PixelFormat.BGR_161616LE: 17>, 'RGBA_16161616LE': <PixelFormat.RGBA_16161616LE: 18>, 'BGRA_16161616LE': <PixelFormat.BGRA_16161616LE: 19>, 'RGB_161616BE': <PixelFormat.RGB_161616BE: 20>, 'BGR_161616BE': <PixelFormat.BGR_161616BE: 21>, 'RGBA_16161616BE': <PixelFormat.RGBA_16161616BE: 22>, 'BGRA_16161616BE': <PixelFormat.BGRA_16161616BE: 23>, 'RGB_hhh_Norm': <PixelFormat.RGB_hhh_Norm: 24>, 'BGR_hhh_Norm': <PixelFormat.BGR_hhh_Norm: 25>, 'RGBA_hhhh_Norm': <PixelFormat.RGBA_hhhh_Norm: 26>, 'BGRA_hhhh_Norm': <PixelFormat.BGRA_hhhh_Norm: 27>, 'RGB_hhh': <PixelFormat.RGB_hhh: 28>, 'BGR_hhh': <PixelFormat.BGR_hhh: 29>, 'RGBA_hhhh': <PixelFormat.RGBA_hhhh: 30>, 'BGRA_hhhh': <PixelFormat.BGRA_hhhh: 31>, 'RGB_fff': <PixelFormat.RGB_fff: 32>, 'BGR_fff': <PixelFormat.BGR_fff: 33>, 'RGBA_ffff': <PixelFormat.RGBA_ffff: 34>, 'BGRA_ffff': <PixelFormat.BGRA_ffff: 35>, 'RGB_101010x_XR': <PixelFormat.RGB_101010x_XR: 36>, 'BGR_101010x_XR': <PixelFormat.BGR_101010x_XR: 37>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class Signature:
    """
    Members:

      CMYK

      Gray

      RGB

      Lab

      XYZ
    """

    CMYK: typing.ClassVar[Signature]  # value = <Signature.CMYK: 1129142603>
    Gray: typing.ClassVar[Signature]  # value = <Signature.Gray: 1196573017>
    Lab: typing.ClassVar[Signature]  # value = <Signature.Lab: 1281450528>
    RGB: typing.ClassVar[Signature]  # value = <Signature.RGB: 1380401696>
    XYZ: typing.ClassVar[Signature]  # value = <Signature.XYZ: 1482250784>
    __members__: typing.ClassVar[
        dict[str, Signature]
    ]  # value = {'CMYK': <Signature.CMYK: 1129142603>, 'Gray': <Signature.Gray: 1196573017>, 'RGB': <Signature.RGB: 1380401696>, 'Lab': <Signature.Lab: 1281450528>, 'XYZ': <Signature.XYZ: 1482250784>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class TFType:
    """
    Members:

      Invalid

      sRGBish

      PQish

      HLGish

      HLGinvish
    """

    HLGinvish: typing.ClassVar[TFType]  # value = <TFType.HLGinvish: 4>
    HLGish: typing.ClassVar[TFType]  # value = <TFType.HLGish: 3>
    Invalid: typing.ClassVar[TFType]  # value = <TFType.Invalid: 0>
    PQish: typing.ClassVar[TFType]  # value = <TFType.PQish: 2>
    __members__: typing.ClassVar[
        dict[str, TFType]
    ]  # value = {'Invalid': <TFType.Invalid: 0>, 'sRGBish': <TFType.sRGBish: 1>, 'PQish': <TFType.PQish: 2>, 'HLGish': <TFType.HLGish: 3>, 'HLGinvish': <TFType.HLGinvish: 4>}
    sRGBish: typing.ClassVar[TFType]  # value = <TFType.sRGBish: 1>
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class TransferFunction:
    a: float
    b: float
    c: float
    d: float
    e: float
    f: float
    g: float
    @staticmethod
    def Identity_TransferFunction() -> TransferFunction: ...
    @staticmethod
    def sRGB_Inverse_TransferFunction() -> TransferFunction: ...
    @staticmethod
    def sRGB_TransferFunction() -> TransferFunction: ...
    @typing.overload
    def __init__(self) -> None:
        """
        Create a new identity TransferFunction.
        """
    @typing.overload
    def __init__(self, g: float, a: float, b: float, c: float, d: float, e: float, f: float) -> None:
        """
        Create a new TransferFunction with the given values.
        """
    @typing.overload
    def __init__(self, v: list[float]) -> None:
        """
        Create a new TransferFunction with the given values.

        :param v: A list of 7 values.
        """
    def __str__(self) -> str: ...
    def eval(self, x: float) -> float: ...
    def getType(self) -> TFType: ...
    def invert(self) -> TransferFunction:
        """
        Inverts the transfer function.

        :return: The inverted transfer function.
        """
    def isHLGish(self) -> bool: ...
    def isPQish(self) -> bool: ...
    def isSRGBish(self) -> bool: ...
    def makeHLG(self) -> bool: ...
    def makeHLGish(self, R: float, G: float, a: float, b: float, c: float) -> bool: ...
    def makePQ(self) -> bool: ...
    def makePQish(self, A: float, B: float, C: float, D: float, E: float, F: float) -> bool: ...
    def makeScaledHLGish(self, K: float, R: float, G: float, a: float, b: float, c: float) -> bool: ...

def WriteICCProfile(tf: TransferFunction, toXYZD50: Matrix3x3) -> animator.skia.Data: ...
def disableRuntimeCPUDetection() -> None: ...
def transform(
    src: numpy.ndarray,
    srcFmt: PixelFormat,
    srcAlpha: AlphaFormat,
    srcProfile: ICCProfile,
    dstFmt: PixelFormat,
    dstAlpha: AlphaFormat,
    dstProfile: ICCProfile,
) -> numpy.ndarray:
    """
    Convert pixels from src format and color profile to dst format and color profile.

    :param numpy.ndarray src: The source pixels.
    :param PixelFormat srcFmt: The source pixel format.
    :param AlphaFormat srcAlpha: The source alpha format.
    :param ICCProfile srcProfile: The source color profile. If ``None``, the sRGB color profile is used.
    :param PixelFormat dstFmt: The destination pixel format.
    :param AlphaFormat dstAlpha: The destination alpha format.
    :param ICCProfile dstProfile: The destination color profile. If ``None``, the sRGB color profile is used.
    :return: The destination pixels.
    :rtype: numpy.ndarray
    """
