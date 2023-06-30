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
    "A2B",
    "AlphaFormat",
    "B2A",
    "CICP",
    "Curve",
    "ICCProfile",
    "Matrix3x3",
    "Matrix3x4",
    "PixelFormat",
    "Signature",
    "TFType",
    "TransferFunction",
    "WriteICCProfile",
    "disableRuntimeCPUDetection",
    "transform",
    "transformWithPalette",
]

class A2B:
    """
    :warning: Indexed assignment to array attributes will not work. Instead assign to the whole
        array. This will cause a memory copy. Instead of doing ``a2b.input_curves[0] = curve``,
        do ``a2b.input_curves = [curve, *a2b.input_curves[1:]]``.
    """

    def __init__(self) -> None: ...
    @property
    def grid_16(self) -> int:
        """
        :type: int
        """
    @grid_16.setter
    def grid_16(self, arg0: int) -> None:
        pass
    @property
    def grid_8(self) -> int:
        """
        :type: int
        """
    @grid_8.setter
    def grid_8(self, arg0: int) -> None:
        pass
    @property
    def grid_points(self) -> list[int]:
        """
        :type: list[int]
        """
    @grid_points.setter
    def grid_points(self, arg1: list[int]) -> None:
        pass
    @property
    def input_channels(self) -> int:
        """
        :type: int
        """
    @input_channels.setter
    def input_channels(self, arg0: int) -> None:
        pass
    @property
    def input_curves(self) -> list[Curve]:
        """
        :type: list[Curve]
        """
    @input_curves.setter
    def input_curves(self, arg1: list[Curve]) -> None:
        pass
    @property
    def matrix(self) -> Matrix3x4:
        """
        :type: Matrix3x4
        """
    @matrix.setter
    def matrix(self, arg0: Matrix3x4) -> None:
        pass
    @property
    def matrix_channels(self) -> int:
        """
        :type: int
        """
    @matrix_channels.setter
    def matrix_channels(self, arg0: int) -> None:
        pass
    @property
    def matrix_curves(self) -> list[Curve]:
        """
        :type: list[Curve]
        """
    @matrix_curves.setter
    def matrix_curves(self, arg1: list[Curve]) -> None:
        pass
    @property
    def output_channels(self) -> int:
        """
        :type: int
        """
    @output_channels.setter
    def output_channels(self, arg0: int) -> None:
        pass
    @property
    def output_curves(self) -> list[Curve]:
        """
        :type: list[Curve]
        """
    @output_curves.setter
    def output_curves(self, arg1: list[Curve]) -> None:
        pass
    pass

class AlphaFormat:
    """
    Members:

      Opaque

      Unpremul

      PremulAsEncoded
    """

    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    Opaque: AlphaFormat  # value = <AlphaFormat.Opaque: 0>
    PremulAsEncoded: AlphaFormat  # value = <AlphaFormat.PremulAsEncoded: 2>
    Unpremul: AlphaFormat  # value = <AlphaFormat.Unpremul: 1>
    __members__: dict  # value = {'Opaque': <AlphaFormat.Opaque: 0>, 'Unpremul': <AlphaFormat.Unpremul: 1>, 'PremulAsEncoded': <AlphaFormat.PremulAsEncoded: 2>}
    pass

class B2A:
    """
    :warning: Indexed assignment to array attributes will not work. Instead assign to the whole
        array. This will cause a memory copy. Instead of doing ``b2a.input_curves[0] = curve``,
        do ``b2a.input_curves = [curve, *b2a.input_curves[1:]]``.
    """

    def __init__(self) -> None: ...
    @property
    def grid_16(self) -> int:
        """
        :type: int
        """
    @grid_16.setter
    def grid_16(self, arg0: int) -> None:
        pass
    @property
    def grid_8(self) -> int:
        """
        :type: int
        """
    @grid_8.setter
    def grid_8(self, arg0: int) -> None:
        pass
    @property
    def grid_points(self) -> list[int]:
        """
        :type: list[int]
        """
    @grid_points.setter
    def grid_points(self, arg1: list[int]) -> None:
        pass
    @property
    def input_channels(self) -> int:
        """
        :type: int
        """
    @input_channels.setter
    def input_channels(self, arg0: int) -> None:
        pass
    @property
    def input_curves(self) -> list[Curve]:
        """
        :type: list[Curve]
        """
    @input_curves.setter
    def input_curves(self, arg1: list[Curve]) -> None:
        pass
    @property
    def matrix(self) -> Matrix3x4:
        """
        :type: Matrix3x4
        """
    @matrix.setter
    def matrix(self, arg0: Matrix3x4) -> None:
        pass
    @property
    def matrix_channels(self) -> int:
        """
        :type: int
        """
    @matrix_channels.setter
    def matrix_channels(self, arg0: int) -> None:
        pass
    @property
    def matrix_curves(self) -> list[Curve]:
        """
        :type: list[Curve]
        """
    @matrix_curves.setter
    def matrix_curves(self, arg1: list[Curve]) -> None:
        pass
    @property
    def output_channels(self) -> int:
        """
        :type: int
        """
    @output_channels.setter
    def output_channels(self, arg0: int) -> None:
        pass
    @property
    def output_curves(self) -> list[Curve]:
        """
        :type: list[Curve]
        """
    @output_curves.setter
    def output_curves(self, arg1: list[Curve]) -> None:
        pass
    pass

class CICP:
    def __init__(self) -> None: ...
    @property
    def color_primaries(self) -> int:
        """
        :type: int
        """
    @color_primaries.setter
    def color_primaries(self, arg0: int) -> None:
        pass
    @property
    def matrix_coefficients(self) -> int:
        """
        :type: int
        """
    @matrix_coefficients.setter
    def matrix_coefficients(self, arg0: int) -> None:
        pass
    @property
    def transfer_characteristics(self) -> int:
        """
        :type: int
        """
    @transfer_characteristics.setter
    def transfer_characteristics(self, arg0: int) -> None:
        pass
    @property
    def video_full_range_flag(self) -> int:
        """
        :type: int
        """
    @video_full_range_flag.setter
    def video_full_range_flag(self, arg0: int) -> None:
        pass
    pass

class Curve:
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
    @property
    def alias_of_table_entries(self) -> int:
        """
        :type: int
        """
    @alias_of_table_entries.setter
    def alias_of_table_entries(self, arg0: int) -> None:
        pass
    @property
    def parametric(self) -> TransferFunction:
        """
        :type: TransferFunction
        """
    @parametric.setter
    def parametric(self, arg0: TransferFunction) -> None:
        pass
    @property
    def table_16(self) -> int:
        """
        :type: int
        """
    @table_16.setter
    def table_16(self, arg0: int) -> None:
        pass
    @property
    def table_8(self) -> int:
        """
        :type: int
        """
    @table_8.setter
    def table_8(self, arg0: int) -> None:
        pass
    @property
    def table_entries(self) -> int:
        """
        :type: int
        """
    @table_entries.setter
    def table_entries(self, arg0: int) -> None:
        pass
    pass

class ICCProfile:
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
    def TRCs_AreApproximateInverse(self, inv_tf: TransferFunction) -> bool:
        """
        Similar to :py:meth:`Curve.areApproximateInverse`, answering the question for all three TRC curves of
        the profile. Again, passing skcms_sRGB_InverseTransferFunction as *inv_tf* will answer the question:
        "Does this profile have a transfer function that is very close to sRGB?"
        """
    @staticmethod
    def XYZD50_profile() -> ICCProfile: ...
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
    @staticmethod
    def sRGB_profile() -> ICCProfile: ...
    def setTransferFunction(self, tf: TransferFunction) -> None: ...
    def setXYZD50(self, m: Matrix3x3) -> None: ...
    def writeICCProfile(self, description: str) -> animator.skia.Data: ...
    @property
    def A2B(self) -> A2B:
        """
        :type: A2B
        """
    @A2B.setter
    def A2B(self, arg0: A2B) -> None:
        pass
    @property
    def B2A(self) -> B2A:
        """
        :type: B2A
        """
    @B2A.setter
    def B2A(self, arg0: B2A) -> None:
        pass
    @property
    def CICP(self) -> CICP:
        """
        :type: CICP
        """
    @CICP.setter
    def CICP(self, arg0: CICP) -> None:
        pass
    @property
    def buffer(self) -> memoryview | None:
        """
        The ICC profile buffer represented as a :py:class:`memoryview`.

        :note: A reference to the profile is needed to keep the buffer alive.

        :type: memoryview | None
        """
    @property
    def data_color_space(self) -> int:
        """
        :type: int
        """
    @data_color_space.setter
    def data_color_space(self, arg0: int) -> None:
        pass
    @property
    def has_A2B(self) -> bool:
        """
        :type: bool
        """
    @has_A2B.setter
    def has_A2B(self, arg0: bool) -> None:
        pass
    @property
    def has_B2A(self) -> bool:
        """
        :type: bool
        """
    @has_B2A.setter
    def has_B2A(self, arg0: bool) -> None:
        pass
    @property
    def has_CICP(self) -> bool:
        """
        :type: bool
        """
    @has_CICP.setter
    def has_CICP(self, arg0: bool) -> None:
        pass
    @property
    def has_toXYZD50(self) -> bool:
        """
        :type: bool
        """
    @has_toXYZD50.setter
    def has_toXYZD50(self, arg0: bool) -> None:
        pass
    @property
    def has_trc(self) -> bool:
        """
        :type: bool
        """
    @has_trc.setter
    def has_trc(self, arg0: bool) -> None:
        pass
    @property
    def pcs(self) -> int:
        """
        :type: int
        """
    @pcs.setter
    def pcs(self, arg0: int) -> None:
        pass
    @property
    def size(self) -> int:
        """
        :type: int
        """
    @size.setter
    def size(self, arg0: int) -> None:
        pass
    @property
    def tag_count(self) -> int:
        """
        :type: int
        """
    @tag_count.setter
    def tag_count(self, arg0: int) -> None:
        pass
    @property
    def toXYZD50(self) -> Matrix3x3:
        """
        :type: Matrix3x3
        """
    @toXYZD50.setter
    def toXYZD50(self, arg0: Matrix3x3) -> None:
        pass
    @property
    def trc(self) -> list[Curve]:
        """
        :warning: Indexed assignment to this attributes will not work. Instead assign to the whole array. This will
        cause a memory copy. Instead of doing ``profile.trc[0] = curve``, do ``profile.trc = [curve,
        *profile.trc[1:]]``.

        :type: list[Curve]
        """
    @trc.setter
    def trc(self, arg1: list[Curve]) -> None:
        """
        :warning: Indexed assignment to this attributes will not work. Instead assign to the whole array. This will
        cause a memory copy. Instead of doing ``profile.trc[0] = curve``, do ``profile.trc = [curve,
        *profile.trc[1:]]``.
        """

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
    pass

class PixelFormat:
    """
    Members:

      A_8

      A_8_

      G_8

      G_8_

      RGBA_8888_Palette8

      BGRA_8888_Palette8

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

    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    ABGR_4444: PixelFormat  # value = <PixelFormat.ABGR_4444: 8>
    ARGB_4444: PixelFormat  # value = <PixelFormat.ARGB_4444: 9>
    A_8: PixelFormat  # value = <PixelFormat.A_8: 0>
    A_8_: PixelFormat  # value = <PixelFormat.A_8_: 1>
    BGRA_1010102: PixelFormat  # value = <PixelFormat.BGRA_1010102: 17>
    BGRA_16161616BE: PixelFormat  # value = <PixelFormat.BGRA_16161616BE: 25>
    BGRA_16161616LE: PixelFormat  # value = <PixelFormat.BGRA_16161616LE: 21>
    BGRA_8888: PixelFormat  # value = <PixelFormat.BGRA_8888: 13>
    BGRA_8888_Palette8: PixelFormat  # value = <PixelFormat.BGRA_8888_Palette8: 5>
    BGRA_8888_sRGB: PixelFormat  # value = <PixelFormat.BGRA_8888_sRGB: 15>
    BGRA_ffff: PixelFormat  # value = <PixelFormat.BGRA_ffff: 37>
    BGRA_hhhh: PixelFormat  # value = <PixelFormat.BGRA_hhhh: 33>
    BGRA_hhhh_Norm: PixelFormat  # value = <PixelFormat.BGRA_hhhh_Norm: 29>
    BGR_101010x_XR: PixelFormat  # value = <PixelFormat.BGR_101010x_XR: 39>
    BGR_161616BE: PixelFormat  # value = <PixelFormat.BGR_161616BE: 23>
    BGR_161616LE: PixelFormat  # value = <PixelFormat.BGR_161616LE: 19>
    BGR_565: PixelFormat  # value = <PixelFormat.BGR_565: 7>
    BGR_888: PixelFormat  # value = <PixelFormat.BGR_888: 11>
    BGR_fff: PixelFormat  # value = <PixelFormat.BGR_fff: 35>
    BGR_hhh: PixelFormat  # value = <PixelFormat.BGR_hhh: 31>
    BGR_hhh_Norm: PixelFormat  # value = <PixelFormat.BGR_hhh_Norm: 27>
    G_8: PixelFormat  # value = <PixelFormat.G_8: 2>
    G_8_: PixelFormat  # value = <PixelFormat.G_8_: 3>
    RGBA_1010102: PixelFormat  # value = <PixelFormat.RGBA_1010102: 16>
    RGBA_16161616BE: PixelFormat  # value = <PixelFormat.RGBA_16161616BE: 24>
    RGBA_16161616LE: PixelFormat  # value = <PixelFormat.RGBA_16161616LE: 20>
    RGBA_8888: PixelFormat  # value = <PixelFormat.RGBA_8888: 12>
    RGBA_8888_Palette8: PixelFormat  # value = <PixelFormat.RGBA_8888_Palette8: 4>
    RGBA_8888_sRGB: PixelFormat  # value = <PixelFormat.RGBA_8888_sRGB: 14>
    RGBA_ffff: PixelFormat  # value = <PixelFormat.RGBA_ffff: 36>
    RGBA_hhhh: PixelFormat  # value = <PixelFormat.RGBA_hhhh: 32>
    RGBA_hhhh_Norm: PixelFormat  # value = <PixelFormat.RGBA_hhhh_Norm: 28>
    RGB_101010x_XR: PixelFormat  # value = <PixelFormat.RGB_101010x_XR: 38>
    RGB_161616BE: PixelFormat  # value = <PixelFormat.RGB_161616BE: 22>
    RGB_161616LE: PixelFormat  # value = <PixelFormat.RGB_161616LE: 18>
    RGB_565: PixelFormat  # value = <PixelFormat.RGB_565: 6>
    RGB_888: PixelFormat  # value = <PixelFormat.RGB_888: 10>
    RGB_fff: PixelFormat  # value = <PixelFormat.RGB_fff: 34>
    RGB_hhh: PixelFormat  # value = <PixelFormat.RGB_hhh: 30>
    RGB_hhh_Norm: PixelFormat  # value = <PixelFormat.RGB_hhh_Norm: 26>
    __members__: dict  # value = {'A_8': <PixelFormat.A_8: 0>, 'A_8_': <PixelFormat.A_8_: 1>, 'G_8': <PixelFormat.G_8: 2>, 'G_8_': <PixelFormat.G_8_: 3>, 'RGBA_8888_Palette8': <PixelFormat.RGBA_8888_Palette8: 4>, 'BGRA_8888_Palette8': <PixelFormat.BGRA_8888_Palette8: 5>, 'RGB_565': <PixelFormat.RGB_565: 6>, 'BGR_565': <PixelFormat.BGR_565: 7>, 'ABGR_4444': <PixelFormat.ABGR_4444: 8>, 'ARGB_4444': <PixelFormat.ARGB_4444: 9>, 'RGB_888': <PixelFormat.RGB_888: 10>, 'BGR_888': <PixelFormat.BGR_888: 11>, 'RGBA_8888': <PixelFormat.RGBA_8888: 12>, 'BGRA_8888': <PixelFormat.BGRA_8888: 13>, 'RGBA_8888_sRGB': <PixelFormat.RGBA_8888_sRGB: 14>, 'BGRA_8888_sRGB': <PixelFormat.BGRA_8888_sRGB: 15>, 'RGBA_1010102': <PixelFormat.RGBA_1010102: 16>, 'BGRA_1010102': <PixelFormat.BGRA_1010102: 17>, 'RGB_161616LE': <PixelFormat.RGB_161616LE: 18>, 'BGR_161616LE': <PixelFormat.BGR_161616LE: 19>, 'RGBA_16161616LE': <PixelFormat.RGBA_16161616LE: 20>, 'BGRA_16161616LE': <PixelFormat.BGRA_16161616LE: 21>, 'RGB_161616BE': <PixelFormat.RGB_161616BE: 22>, 'BGR_161616BE': <PixelFormat.BGR_161616BE: 23>, 'RGBA_16161616BE': <PixelFormat.RGBA_16161616BE: 24>, 'BGRA_16161616BE': <PixelFormat.BGRA_16161616BE: 25>, 'RGB_hhh_Norm': <PixelFormat.RGB_hhh_Norm: 26>, 'BGR_hhh_Norm': <PixelFormat.BGR_hhh_Norm: 27>, 'RGBA_hhhh_Norm': <PixelFormat.RGBA_hhhh_Norm: 28>, 'BGRA_hhhh_Norm': <PixelFormat.BGRA_hhhh_Norm: 29>, 'RGB_hhh': <PixelFormat.RGB_hhh: 30>, 'BGR_hhh': <PixelFormat.BGR_hhh: 31>, 'RGBA_hhhh': <PixelFormat.RGBA_hhhh: 32>, 'BGRA_hhhh': <PixelFormat.BGRA_hhhh: 33>, 'RGB_fff': <PixelFormat.RGB_fff: 34>, 'BGR_fff': <PixelFormat.BGR_fff: 35>, 'RGBA_ffff': <PixelFormat.RGBA_ffff: 36>, 'BGRA_ffff': <PixelFormat.BGRA_ffff: 37>, 'RGB_101010x_XR': <PixelFormat.RGB_101010x_XR: 38>, 'BGR_101010x_XR': <PixelFormat.BGR_101010x_XR: 39>}
    pass

class Signature:
    """
    Members:

      CMYK

      Gray

      RGB

      Lab

      XYZ
    """

    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    CMYK: Signature  # value = <Signature.CMYK: 1129142603>
    Gray: Signature  # value = <Signature.Gray: 1196573017>
    Lab: Signature  # value = <Signature.Lab: 1281450528>
    RGB: Signature  # value = <Signature.RGB: 1380401696>
    XYZ: Signature  # value = <Signature.XYZ: 1482250784>
    __members__: dict  # value = {'CMYK': <Signature.CMYK: 1129142603>, 'Gray': <Signature.Gray: 1196573017>, 'RGB': <Signature.RGB: 1380401696>, 'Lab': <Signature.Lab: 1281450528>, 'XYZ': <Signature.XYZ: 1482250784>}
    pass

class TFType:
    """
    Members:

      Invalid

      sRGBish

      PQish

      HLGish

      HLGinvish
    """

    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    HLGinvish: TFType  # value = <TFType.HLGinvish: 4>
    HLGish: TFType  # value = <TFType.HLGish: 3>
    Invalid: TFType  # value = <TFType.Invalid: 0>
    PQish: TFType  # value = <TFType.PQish: 2>
    __members__: dict  # value = {'Invalid': <TFType.Invalid: 0>, 'sRGBish': <TFType.sRGBish: 1>, 'PQish': <TFType.PQish: 2>, 'HLGish': <TFType.HLGish: 3>, 'HLGinvish': <TFType.HLGinvish: 4>}
    sRGBish: TFType  # value = <TFType.sRGBish: 1>
    pass

class TransferFunction:
    @staticmethod
    def Identity_TransferFunction() -> TransferFunction: ...
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
    @staticmethod
    def sRGB_Inverse_TransferFunction() -> TransferFunction: ...
    @staticmethod
    def sRGB_TransferFunction() -> TransferFunction: ...
    @property
    def a(self) -> float:
        """
        :type: float
        """
    @a.setter
    def a(self, arg0: float) -> None:
        pass
    @property
    def b(self) -> float:
        """
        :type: float
        """
    @b.setter
    def b(self, arg0: float) -> None:
        pass
    @property
    def c(self) -> float:
        """
        :type: float
        """
    @c.setter
    def c(self, arg0: float) -> None:
        pass
    @property
    def d(self) -> float:
        """
        :type: float
        """
    @d.setter
    def d(self, arg0: float) -> None:
        pass
    @property
    def e(self) -> float:
        """
        :type: float
        """
    @e.setter
    def e(self, arg0: float) -> None:
        pass
    @property
    def f(self) -> float:
        """
        :type: float
        """
    @f.setter
    def f(self, arg0: float) -> None:
        pass
    @property
    def g(self) -> float:
        """
        :type: float
        """
    @g.setter
    def g(self, arg0: float) -> None:
        pass
    pass

def WriteICCProfile(tf: TransferFunction, toXYZD50: Matrix3x3) -> animator.skia.Data:
    pass

def disableRuntimeCPUDetection() -> None:
    pass

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

@typing.overload
def transformWithPalette(
    src: numpy.ndarray,
    srcFmt: PixelFormat,
    srcAlpha: AlphaFormat,
    srcProfile: ICCProfile,
    dst: numpy.ndarray,
    dstFmt: PixelFormat,
    dstAlpha: AlphaFormat,
    dstProfile: ICCProfile,
    palette: numpy.ndarray | None = None,
) -> numpy.ndarray:
    """
    Convert pixels from src format and color profile to dst format and color profile.

    :param numpy.ndarray src: The source pixels.
    :param PixelFormat srcFmt: The source pixel format.
    :param AlphaFormat srcAlpha: The source alpha format.
    :param ICCProfile srcProfile: The source color profile. If ``None``, the sRGB color profile is used.
    :param numpy.ndarray dst: The destination pixels.
    :param PixelFormat dstFmt: The destination pixel format.
    :param AlphaFormat dstAlpha: The destination alpha format.
    :param ICCProfile dstProfile: The destination color profile. If ``None``, the sRGB color profile is used.
    :param numpy.ndarray palette: The palette. If ``None``, no palette is used.
    :return: The destination pixels.
    :rtype: numpy.ndarray
    """

@typing.overload
def transformWithPalette(
    src: numpy.ndarray,
    srcFmt: PixelFormat,
    srcAlpha: AlphaFormat,
    srcProfile: ICCProfile,
    dstFmt: PixelFormat,
    dstAlpha: AlphaFormat,
    dstProfile: ICCProfile,
    palette: numpy.ndarray | None = None,
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
    :param numpy.ndarray palette: The palette. If ``None``, no palette is used.
    :return: The destination pixels.
    :rtype: numpy.ndarray
    """
