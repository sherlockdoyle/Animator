"""
Custom Skia bindings for animator.

Refer to the Skia documentation for more information. Unless otherwise documented, all functions behave the same as the
corresponding Skia function. Small changes like throwing exceptions instead of returning false have been made.
"""
from __future__ import annotations

import typing
from enum import IntEnum, IntFlag

import numpy

import animator.skia
import animator.skia.cms as cms
import animator.skia.sksl as sksl
import animator.skia.textlayout as textlayout

buffer = bytes | memoryview | bytearray | numpy.ndarray

__all__ = [
    "AlphaOPAQUE",
    "AlphaTRANSPARENT",
    "AlphaType",
    "ApplyPerspectiveClip",
    "AutoCanvasRestore",
    "Bitmap",
    "BlendMode",
    "BlendModeCoeff",
    "Blender",
    "Blenders",
    "BlurStyle",
    "Canvas",
    "ClipOp",
    "Color",
    "Color4f",
    "ColorBLACK",
    "ColorBLUE",
    "ColorCYAN",
    "ColorChannel",
    "ColorChannelFlag",
    "ColorDKGRAY",
    "ColorFilter",
    "ColorFilters",
    "ColorGRAY",
    "ColorGREEN",
    "ColorGetA",
    "ColorGetB",
    "ColorGetG",
    "ColorGetR",
    "ColorInfo",
    "ColorLTGRAY",
    "ColorMAGENTA",
    "ColorMatrix",
    "ColorMatrixFilter",
    "ColorRED",
    "ColorSetA",
    "ColorSetARGB",
    "ColorSetRGB",
    "ColorSpace",
    "ColorSpacePrimaries",
    "ColorTRANSPARENT",
    "ColorTable",
    "ColorToHSV",
    "ColorType",
    "ColorWHITE",
    "ColorYELLOW",
    "CornerPathEffect",
    "CubicMap",
    "CubicResampler",
    "DashPathEffect",
    "Data",
    "DiscretePathEffect",
    "EncodedImageFormat",
    "FilterMode",
    "Flattenable",
    "Font",
    "FontArguments",
    "FontHinting",
    "FontMetrics",
    "FontMgr",
    "FontParameters",
    "FontStyle",
    "FontStyleSet",
    "GradientShader",
    "HSVToColor",
    "HighContrastConfig",
    "HighContrastFilter",
    "IPoint",
    "IRect",
    "ISize",
    "Image",
    "ImageFilter",
    "ImageFilters",
    "ImageInfo",
    "Line2DPathEffect",
    "LumaColorFilter",
    "MakeNullCanvas",
    "MaskFilter",
    "Matrix",
    "MatrixPathEffect",
    "MergePathEffect",
    "MipmapMode",
    "NamedGamut",
    "NamedTransferFn",
    "OpBuilder",
    "OverdrawColorFilter",
    "Paint",
    "ParsePath",
    "Path",
    "Path1DPathEffect",
    "Path2DPathEffect",
    "PathBuilder",
    "PathDirection",
    "PathEffect",
    "PathFillType",
    "PathMeasure",
    "PathOp",
    "PathSegmentMask",
    "PathVerb",
    "Picture",
    "PixelGeometry",
    "Pixmap",
    "Point",
    "Point3",
    "PreMultiplyARGB",
    "PreMultiplyColor",
    "RGBToHSV",
    "RRect",
    "RSXform",
    "Rect",
    "Region",
    "RuntimeBlendBuilder",
    "RuntimeColorFilterBuilder",
    "RuntimeEffect",
    "RuntimeEffectBuilder",
    "RuntimeShaderBuilder",
    "SamplingOptions",
    "Shader",
    "ShaderMaskFilter",
    "ShadowFlags",
    "ShadowUtils",
    "Size",
    "StrokeAndFillPathEffect",
    "StrokePathEffect",
    "StrokeRec",
    "Surface",
    "SurfaceProps",
    "TableMaskFilter",
    "TextBlob",
    "TextBlobBuilder",
    "TextEncoding",
    "TextUtils_Align",
    "TileMode",
    "TrimPathEffect",
    "Typeface",
    "Vertices",
    "YUVColorSpace",
    "cms",
    "kTileModeCount",
    "sksl",
    "textlayout",
    "uniqueColor",
]

class AlphaType:
    """
    Members:

      kUnknown_AlphaType

      kOpaque_AlphaType

      kPremul_AlphaType

      kUnpremul_AlphaType

      kLastEnum_AlphaType
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
    def isOpaque(self) -> bool:
        """
        Returns true if this alpha type is opaque (*kOpaque_AlphaType*).

        *kOpaque_AlphaType* is a hint that the ColorType is opaque, or that all alpha values are set to their
        1.0 equivalent. If :py:class:`AlphaType` is *kOpaque_AlphaType*, and :py:class:`ColorType` is not
        opaque, then the result of drawing any pixel with a alpha value less than 1.0 is undefined.
        """
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
    __members__: dict  # value = {'kUnknown_AlphaType': <AlphaType.kUnknown_AlphaType: 0>, 'kOpaque_AlphaType': <AlphaType.kOpaque_AlphaType: 1>, 'kPremul_AlphaType': <AlphaType.kPremul_AlphaType: 2>, 'kUnpremul_AlphaType': <AlphaType.kUnpremul_AlphaType: 3>, 'kLastEnum_AlphaType': <AlphaType.kUnpremul_AlphaType: 3>}
    kLastEnum_AlphaType: animator.skia.AlphaType  # value = <AlphaType.kUnpremul_AlphaType: 3>
    kOpaque_AlphaType: animator.skia.AlphaType  # value = <AlphaType.kOpaque_AlphaType: 1>
    kPremul_AlphaType: animator.skia.AlphaType  # value = <AlphaType.kPremul_AlphaType: 2>
    kUnknown_AlphaType: animator.skia.AlphaType  # value = <AlphaType.kUnknown_AlphaType: 0>
    kUnpremul_AlphaType: animator.skia.AlphaType  # value = <AlphaType.kUnpremul_AlphaType: 3>
    pass

class ApplyPerspectiveClip:
    """
    Members:

      kNo

      kYes
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
    __members__: dict  # value = {'kNo': <ApplyPerspectiveClip.kNo: 0>, 'kYes': <ApplyPerspectiveClip.kYes: 1>}
    kNo: animator.skia.ApplyPerspectiveClip  # value = <ApplyPerspectiveClip.kNo: 0>
    kYes: animator.skia.ApplyPerspectiveClip  # value = <ApplyPerspectiveClip.kYes: 1>
    pass

class AutoCanvasRestore:
    def __enter__(self) -> None: ...
    def __exit__(self, *args) -> None: ...
    def __init__(self, canvas: Canvas, doSave: bool = True) -> None: ...
    def restore(self) -> None: ...
    pass

class Bitmap:
    """
    :py:class:`Bitmap` describes a two-dimensional raster pixel array.

    :py:class:`Bitmap` supports buffer protocol. It is possible to mount :py:class:`Bitmap` as array::

        array = np.array(pixmap, copy=False)

    Or mount array as :py:class:`Bitmap` with :py:class:`ImageInfo`::

        buffer = np.zeros((100, 100, 4), np.uint8)
        bitmap = skia.Bitmap()
        bitmap.setInfo(skia.ImageInfo.MakeN32Premul(100, 100))
        bitmap.setPixels(buffer)
    """

    class AllocFlags(IntEnum):
        """
        Members:

          kZeroPixels_AllocFlag
        """

        def __and__(self, other: object) -> object: ...
        def __eq__(self, other: object) -> bool: ...
        def __ge__(self, other: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __gt__(self, other: object) -> bool: ...
        def __hash__(self) -> int: ...
        def __index__(self) -> int: ...
        def __init__(self, value: int) -> None: ...
        def __int__(self) -> int: ...
        def __invert__(self) -> object: ...
        def __le__(self, other: object) -> bool: ...
        def __lt__(self, other: object) -> bool: ...
        def __ne__(self, other: object) -> bool: ...
        def __or__(self, other: object) -> object: ...
        def __rand__(self, other: object) -> object: ...
        def __repr__(self) -> str: ...
        def __ror__(self, other: object) -> object: ...
        def __rxor__(self, other: object) -> object: ...
        def __setstate__(self, state: int) -> None: ...
        def __xor__(self, other: object) -> object: ...
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
        __members__: dict  # value = {'kZeroPixels_AllocFlag': <AllocFlags.kZeroPixels_AllocFlag: 1>}
        kZeroPixels_AllocFlag: animator.skia.Bitmap.AllocFlags  # value = <AllocFlags.kZeroPixels_AllocFlag: 1>
        pass
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, src: Bitmap) -> None: ...
    def __str__(self) -> str: ...
    def allocN32Pixels(self, width: int, height: int, isOpaque: bool = False) -> None: ...
    @typing.overload
    def allocPixels(self) -> None: ...
    @typing.overload
    def allocPixels(self, info: ImageInfo) -> None: ...
    @typing.overload
    def allocPixels(self, info: ImageInfo, rowBytes: int) -> None: ...
    def allocPixelsFlags(self, info: ImageInfo, flags: int = 0) -> None: ...
    def alphaType(self) -> AlphaType: ...
    def asImage(self) -> Image: ...
    def bounds(self) -> IRect: ...
    def bytesPerPixel(self) -> int: ...
    def colorSpace(self) -> ColorSpace: ...
    def colorType(self) -> ColorType: ...
    def computeByteSize(self) -> int: ...
    def computeIsOpaque(self) -> bool:
        """
        Returns ``True`` if all pixels are opaque.
        """
    def dimensions(self) -> ISize: ...
    def drawsNothing(self) -> bool: ...
    def empty(self) -> bool: ...
    @typing.overload
    def erase(self, c: _Color4f, area: _IRect) -> None: ...
    @typing.overload
    def erase(self, c: int, area: _IRect) -> None: ...
    def eraseARGB(self, a: int, r: int, g: int, b: int) -> None: ...
    @typing.overload
    def eraseColor(self, c: _Color4f) -> None: ...
    @typing.overload
    def eraseColor(self, c: int) -> None: ...
    def extractAlpha(self, paint: Paint | None = None) -> tuple[Bitmap, IPoint]:
        """
        Returns a tuple of (bitmap describing the alpha values, top-left position of the alpha values).
        """
    def extractSubset(self, subset: _IRect) -> Bitmap: ...
    def getAlphaf(self, x: int, y: int) -> float: ...
    def getBounds(self) -> IRect:
        """
        Returns :py:class:`IRect` { 0, 0, :py:meth:`width`, :py:meth:`height` }.
        """
    def getColor(self, x: int, y: int) -> int: ...
    def getColor4f(self, x: int, y: int) -> Color4f: ...
    def getGenerationID(self) -> int: ...
    def getPixels(self) -> memoryview:
        """
        Return a ``memoryview`` object of the pixel data.
        """
    def getSubset(self) -> IRect: ...
    def height(self) -> int: ...
    def info(self) -> ImageInfo: ...
    @typing.overload
    def installPixels(self, info: ImageInfo, pixels: buffer | None, rowBytes: int = 0) -> bool:
        """
        Sets :py:class:`ImageInfo` *info* and pixel data from the buffer *pixels*.

        :warning: Keep a reference to the buffer until the bitmap is no longer needed.
        """
    @typing.overload
    def installPixels(self, pixmap: Pixmap) -> bool: ...
    def isImmutable(self) -> bool: ...
    def isNull(self) -> bool: ...
    def isOpaque(self) -> bool: ...
    def makeShader(
        self,
        tmx: TileMode = TileMode.kClamp,
        tmy: TileMode = TileMode.kClamp,
        sampling: SamplingOptions = ...,
        localMatrix: Matrix | None = None,
    ) -> Shader: ...
    def notifyPixelsChanged(self) -> None: ...
    def peekPixels(self) -> Pixmap:
        """
        Returns a :py:class:`Pixmap` describing the pixel data.
        """
    def pixelRefOrigin(self) -> IPoint: ...
    def pixmap(self) -> Pixmap: ...
    @typing.overload
    def readPixels(self, dst: Pixmap, srcX: int = 0, srcY: int = 0) -> bool: ...
    @typing.overload
    def readPixels(
        self, dstInfo: ImageInfo, dstPixels: buffer, dstRowBytes: int = 0, srcX: int = 0, srcY: int = 0
    ) -> bool:
        """
        Copies *dstInfo* pixels starting from (*srcX*, *srcY*) to *dstPixels* buffer.
        """
    def readyToDraw(self) -> bool: ...
    def refColorSpace(self) -> ColorSpace: ...
    def reset(self) -> None: ...
    def rowBytes(self) -> int: ...
    def rowBytesAsPixels(self) -> int: ...
    def setAlphaType(self, alphaType: AlphaType) -> bool: ...
    def setImmutable(self) -> None: ...
    def setInfo(self, imageInfo: ImageInfo, rowBytes: int = 0) -> bool: ...
    def setPixels(self, pixels: buffer | None) -> None:
        """
        Sets pixel data from the buffer *pixels*.

        :warning: Keep a reference to the buffer until the bitmap is no longer needed.
        """
    def shiftPerPixel(self) -> int: ...
    def swap(self, other: Bitmap) -> None: ...
    def tobytes(self) -> bytes:
        """
        Convert :py:class:`Bitmap` to bytes.
        """
    def tryAllocN32Pixels(self, width: int, height: int, isOpaque: bool = False) -> bool: ...
    @typing.overload
    def tryAllocPixels(self) -> bool: ...
    @typing.overload
    def tryAllocPixels(self, info: ImageInfo) -> bool: ...
    @typing.overload
    def tryAllocPixels(self, info: ImageInfo, rowBytes: int) -> bool: ...
    def tryAllocPixelsFlags(self, info: ImageInfo, flags: int = 0) -> bool: ...
    def width(self) -> int: ...
    def writePixels(self, src: Pixmap, dstX: int = 0, dstY: int = 0) -> bool: ...
    pass

class BlendMode:
    """
    Members:

      kClear

      kSrc

      kDst

      kSrcOver

      kDstOver

      kSrcIn

      kDstIn

      kSrcOut

      kDstOut

      kSrcATop

      kDstATop

      kXor

      kPlus

      kModulate

      kScreen

      kOverlay

      kDarken

      kLighten

      kColorDodge

      kColorBurn

      kHardLight

      kSoftLight

      kDifference

      kExclusion

      kMultiply

      kHue

      kSaturation

      kColor

      kLuminosity

      kLastCoeffMode

      kLastSeparableMode

      kLastMode
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
    def asCoeff(self) -> tuple[BlendModeCoeff, BlendModeCoeff] | None:
        """
        Returns the source and destination coefficients for the coeffient-based blend mode, or None otherwise.
        """
    def name_(self) -> str:
        """
        Returns name of blend mode as returned by the C++ API.
        """
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
    __members__: dict  # value = {'kClear': <BlendMode.kClear: 0>, 'kSrc': <BlendMode.kSrc: 1>, 'kDst': <BlendMode.kDst: 2>, 'kSrcOver': <BlendMode.kSrcOver: 3>, 'kDstOver': <BlendMode.kDstOver: 4>, 'kSrcIn': <BlendMode.kSrcIn: 5>, 'kDstIn': <BlendMode.kDstIn: 6>, 'kSrcOut': <BlendMode.kSrcOut: 7>, 'kDstOut': <BlendMode.kDstOut: 8>, 'kSrcATop': <BlendMode.kSrcATop: 9>, 'kDstATop': <BlendMode.kDstATop: 10>, 'kXor': <BlendMode.kXor: 11>, 'kPlus': <BlendMode.kPlus: 12>, 'kModulate': <BlendMode.kModulate: 13>, 'kScreen': <BlendMode.kScreen: 14>, 'kOverlay': <BlendMode.kOverlay: 15>, 'kDarken': <BlendMode.kDarken: 16>, 'kLighten': <BlendMode.kLighten: 17>, 'kColorDodge': <BlendMode.kColorDodge: 18>, 'kColorBurn': <BlendMode.kColorBurn: 19>, 'kHardLight': <BlendMode.kHardLight: 20>, 'kSoftLight': <BlendMode.kSoftLight: 21>, 'kDifference': <BlendMode.kDifference: 22>, 'kExclusion': <BlendMode.kExclusion: 23>, 'kMultiply': <BlendMode.kMultiply: 24>, 'kHue': <BlendMode.kHue: 25>, 'kSaturation': <BlendMode.kSaturation: 26>, 'kColor': <BlendMode.kColor: 27>, 'kLuminosity': <BlendMode.kLuminosity: 28>, 'kLastCoeffMode': <BlendMode.kScreen: 14>, 'kLastSeparableMode': <BlendMode.kMultiply: 24>, 'kLastMode': <BlendMode.kLuminosity: 28>}
    kClear: animator.skia.BlendMode  # value = <BlendMode.kClear: 0>
    kColor: animator.skia.BlendMode  # value = <BlendMode.kColor: 27>
    kColorBurn: animator.skia.BlendMode  # value = <BlendMode.kColorBurn: 19>
    kColorDodge: animator.skia.BlendMode  # value = <BlendMode.kColorDodge: 18>
    kDarken: animator.skia.BlendMode  # value = <BlendMode.kDarken: 16>
    kDifference: animator.skia.BlendMode  # value = <BlendMode.kDifference: 22>
    kDst: animator.skia.BlendMode  # value = <BlendMode.kDst: 2>
    kDstATop: animator.skia.BlendMode  # value = <BlendMode.kDstATop: 10>
    kDstIn: animator.skia.BlendMode  # value = <BlendMode.kDstIn: 6>
    kDstOut: animator.skia.BlendMode  # value = <BlendMode.kDstOut: 8>
    kDstOver: animator.skia.BlendMode  # value = <BlendMode.kDstOver: 4>
    kExclusion: animator.skia.BlendMode  # value = <BlendMode.kExclusion: 23>
    kHardLight: animator.skia.BlendMode  # value = <BlendMode.kHardLight: 20>
    kHue: animator.skia.BlendMode  # value = <BlendMode.kHue: 25>
    kLastCoeffMode: animator.skia.BlendMode  # value = <BlendMode.kScreen: 14>
    kLastMode: animator.skia.BlendMode  # value = <BlendMode.kLuminosity: 28>
    kLastSeparableMode: animator.skia.BlendMode  # value = <BlendMode.kMultiply: 24>
    kLighten: animator.skia.BlendMode  # value = <BlendMode.kLighten: 17>
    kLuminosity: animator.skia.BlendMode  # value = <BlendMode.kLuminosity: 28>
    kModulate: animator.skia.BlendMode  # value = <BlendMode.kModulate: 13>
    kMultiply: animator.skia.BlendMode  # value = <BlendMode.kMultiply: 24>
    kOverlay: animator.skia.BlendMode  # value = <BlendMode.kOverlay: 15>
    kPlus: animator.skia.BlendMode  # value = <BlendMode.kPlus: 12>
    kSaturation: animator.skia.BlendMode  # value = <BlendMode.kSaturation: 26>
    kScreen: animator.skia.BlendMode  # value = <BlendMode.kScreen: 14>
    kSoftLight: animator.skia.BlendMode  # value = <BlendMode.kSoftLight: 21>
    kSrc: animator.skia.BlendMode  # value = <BlendMode.kSrc: 1>
    kSrcATop: animator.skia.BlendMode  # value = <BlendMode.kSrcATop: 9>
    kSrcIn: animator.skia.BlendMode  # value = <BlendMode.kSrcIn: 5>
    kSrcOut: animator.skia.BlendMode  # value = <BlendMode.kSrcOut: 7>
    kSrcOver: animator.skia.BlendMode  # value = <BlendMode.kSrcOver: 3>
    kXor: animator.skia.BlendMode  # value = <BlendMode.kXor: 11>
    pass

class BlendModeCoeff:
    """
    Members:

      kZero

      kOne

      kSC

      kISC

      kDC

      kIDC

      kSA

      kISA

      kDA

      kIDA

      kCoeffCount
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
    __members__: dict  # value = {'kZero': <BlendModeCoeff.kZero: 0>, 'kOne': <BlendModeCoeff.kOne: 1>, 'kSC': <BlendModeCoeff.kSC: 2>, 'kISC': <BlendModeCoeff.kISC: 3>, 'kDC': <BlendModeCoeff.kDC: 4>, 'kIDC': <BlendModeCoeff.kIDC: 5>, 'kSA': <BlendModeCoeff.kSA: 6>, 'kISA': <BlendModeCoeff.kISA: 7>, 'kDA': <BlendModeCoeff.kDA: 8>, 'kIDA': <BlendModeCoeff.kIDA: 9>, 'kCoeffCount': <BlendModeCoeff.kCoeffCount: 10>}
    kCoeffCount: animator.skia.BlendModeCoeff  # value = <BlendModeCoeff.kCoeffCount: 10>
    kDA: animator.skia.BlendModeCoeff  # value = <BlendModeCoeff.kDA: 8>
    kDC: animator.skia.BlendModeCoeff  # value = <BlendModeCoeff.kDC: 4>
    kIDA: animator.skia.BlendModeCoeff  # value = <BlendModeCoeff.kIDA: 9>
    kIDC: animator.skia.BlendModeCoeff  # value = <BlendModeCoeff.kIDC: 5>
    kISA: animator.skia.BlendModeCoeff  # value = <BlendModeCoeff.kISA: 7>
    kISC: animator.skia.BlendModeCoeff  # value = <BlendModeCoeff.kISC: 3>
    kOne: animator.skia.BlendModeCoeff  # value = <BlendModeCoeff.kOne: 1>
    kSA: animator.skia.BlendModeCoeff  # value = <BlendModeCoeff.kSA: 6>
    kSC: animator.skia.BlendModeCoeff  # value = <BlendModeCoeff.kSC: 2>
    kZero: animator.skia.BlendModeCoeff  # value = <BlendModeCoeff.kZero: 0>
    pass

class Flattenable:
    class Type:
        """
        Members:

          kColorFilter_Type

          kBlender_Type

          kDrawable_Type

          kImageFilter_Type

          kMaskFilter_Type

          kPathEffect_Type

          kShader_Type
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
        __members__: dict  # value = {'kColorFilter_Type': <Type.kColorFilter_Type: 0>, 'kBlender_Type': <Type.kBlender_Type: 1>, 'kDrawable_Type': <Type.kDrawable_Type: 2>, 'kImageFilter_Type': <Type.kImageFilter_Type: 4>, 'kMaskFilter_Type': <Type.kMaskFilter_Type: 5>, 'kPathEffect_Type': <Type.kPathEffect_Type: 6>, 'kShader_Type': <Type.kShader_Type: 7>}
        kBlender_Type: animator.skia.Flattenable.Type  # value = <Type.kBlender_Type: 1>
        kColorFilter_Type: animator.skia.Flattenable.Type  # value = <Type.kColorFilter_Type: 0>
        kDrawable_Type: animator.skia.Flattenable.Type  # value = <Type.kDrawable_Type: 2>
        kImageFilter_Type: animator.skia.Flattenable.Type  # value = <Type.kImageFilter_Type: 4>
        kMaskFilter_Type: animator.skia.Flattenable.Type  # value = <Type.kMaskFilter_Type: 5>
        kPathEffect_Type: animator.skia.Flattenable.Type  # value = <Type.kPathEffect_Type: 6>
        kShader_Type: animator.skia.Flattenable.Type  # value = <Type.kShader_Type: 7>
        pass
    @staticmethod
    def Deserialize(type: Flattenable.Type, data: buffer) -> Flattenable:
        """
        Deserialize a flattenable of the given *type* from a buffer *data*.
        """
    @staticmethod
    def DeserializeAsType(
        type: Flattenable.Type, data: buffer
    ) -> ColorFilter | Blender | ImageFilter | MaskFilter | PathEffect | Shader:
        """
        Deserialize a flattenable of the given *type* from a buffer *data*. The return value is correctly typed.
        """
    def __init__(self) -> None: ...
    def __str__(self) -> str: ...
    def getFlattenableType(self) -> Flattenable.Type: ...
    def getTypeName(self) -> str: ...
    def serialize(self) -> Data: ...
    pass

class Blenders:
    @staticmethod
    def Arithmetic(k1: float, k2: float, k3: float, k4: float, enforcePremul: bool = False) -> Blender: ...
    pass

class BlurStyle(IntEnum):
    """
    Members:

      kNormal_BlurStyle

      kSolid_BlurStyle

      kOuter_BlurStyle

      kInner_BlurStyle

      kLastEnum_BlurStyle
    """

    def __and__(self, other: object) -> object: ...
    def __eq__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __gt__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __invert__(self) -> object: ...
    def __le__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __or__(self, other: object) -> object: ...
    def __rand__(self, other: object) -> object: ...
    def __repr__(self) -> str: ...
    def __ror__(self, other: object) -> object: ...
    def __rxor__(self, other: object) -> object: ...
    def __setstate__(self, state: int) -> None: ...
    def __xor__(self, other: object) -> object: ...
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
    __members__: dict  # value = {'kNormal_BlurStyle': <BlurStyle.kNormal_BlurStyle: 0>, 'kSolid_BlurStyle': <BlurStyle.kSolid_BlurStyle: 1>, 'kOuter_BlurStyle': <BlurStyle.kOuter_BlurStyle: 2>, 'kInner_BlurStyle': <BlurStyle.kInner_BlurStyle: 3>, 'kLastEnum_BlurStyle': <BlurStyle.kInner_BlurStyle: 3>}
    kInner_BlurStyle: animator.skia.BlurStyle  # value = <BlurStyle.kInner_BlurStyle: 3>
    kLastEnum_BlurStyle: animator.skia.BlurStyle  # value = <BlurStyle.kInner_BlurStyle: 3>
    kNormal_BlurStyle: animator.skia.BlurStyle  # value = <BlurStyle.kNormal_BlurStyle: 0>
    kOuter_BlurStyle: animator.skia.BlurStyle  # value = <BlurStyle.kOuter_BlurStyle: 2>
    kSolid_BlurStyle: animator.skia.BlurStyle  # value = <BlurStyle.kSolid_BlurStyle: 1>
    pass

class Canvas:
    class Lattice:
        class RectType:
            """
            Members:

              kDefault

              kTransparent

              kFixedColor
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
            __members__: dict  # value = {'kDefault': <RectType.kDefault: 0>, 'kTransparent': <RectType.kTransparent: 1>, 'kFixedColor': <RectType.kFixedColor: 2>}
            kDefault: animator.skia.Canvas.Lattice.RectType  # value = <RectType.kDefault: 0>
            kFixedColor: animator.skia.Canvas.Lattice.RectType  # value = <RectType.kFixedColor: 2>
            kTransparent: animator.skia.Canvas.Lattice.RectType  # value = <RectType.kTransparent: 1>
            pass
        def __init__(
            self,
            fXDivs: list,
            fYDivs: list,
            fRectTypes: list | None = None,
            fBounds: _IRect | None = None,
            fColors: list | None = None,
        ) -> None: ...
        def __str__(self) -> str: ...
        @property
        def fBounds(self) -> IRect:
            """
            :type: IRect
            """
        @property
        def fColors(self) -> list[int] | None:
            """
            :type: list[int] | None
            """
        @property
        def fRectTypes(self) -> list[Canvas.Lattice.RectType] | None:
            """
            :type: list[Canvas.Lattice.RectType] | None
            """
        @property
        def fXCount(self) -> int:
            """
            :type: int
            """
        @property
        def fXDivs(self) -> list[int]:
            """
            :type: list[int]
            """
        @property
        def fYCount(self) -> int:
            """
            :type: int
            """
        @property
        def fYDivs(self) -> list[int]:
            """
            :type: list[int]
            """

    class PointMode:
        """
        Members:

          kPoints_PointMode

          kLines_PointMode

          kPolygon_PointMode
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
        __members__: dict  # value = {'kPoints_PointMode': <PointMode.kPoints_PointMode: 0>, 'kLines_PointMode': <PointMode.kLines_PointMode: 1>, 'kPolygon_PointMode': <PointMode.kPolygon_PointMode: 2>}
        kLines_PointMode: animator.skia.Canvas.PointMode  # value = <PointMode.kLines_PointMode: 1>
        kPoints_PointMode: animator.skia.Canvas.PointMode  # value = <PointMode.kPoints_PointMode: 0>
        kPolygon_PointMode: animator.skia.Canvas.PointMode  # value = <PointMode.kPolygon_PointMode: 2>
        pass

    class SaveLayerFlags(IntFlag):
        """
        Members:

          kPreserveLCDText_SaveLayerFlag

          kInitWithPrevious_SaveLayerFlag

          kF16ColorType
        """

        def __and__(self, other: object) -> object: ...
        def __eq__(self, other: object) -> bool: ...
        def __ge__(self, other: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __gt__(self, other: object) -> bool: ...
        def __hash__(self) -> int: ...
        def __index__(self) -> int: ...
        def __init__(self, value: int) -> None: ...
        def __int__(self) -> int: ...
        def __invert__(self) -> object: ...
        def __le__(self, other: object) -> bool: ...
        def __lt__(self, other: object) -> bool: ...
        def __ne__(self, other: object) -> bool: ...
        def __or__(self, other: object) -> object: ...
        def __rand__(self, other: object) -> object: ...
        def __repr__(self) -> str: ...
        def __ror__(self, other: object) -> object: ...
        def __rxor__(self, other: object) -> object: ...
        def __setstate__(self, state: int) -> None: ...
        def __xor__(self, other: object) -> object: ...
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
        __members__: dict  # value = {'kPreserveLCDText_SaveLayerFlag': <SaveLayerFlags.kPreserveLCDText_SaveLayerFlag: 2>, 'kInitWithPrevious_SaveLayerFlag': <SaveLayerFlags.kInitWithPrevious_SaveLayerFlag: 4>, 'kF16ColorType': <SaveLayerFlags.kF16ColorType: 16>}
        kF16ColorType: animator.skia.Canvas.SaveLayerFlags  # value = <SaveLayerFlags.kF16ColorType: 16>
        kInitWithPrevious_SaveLayerFlag: animator.skia.Canvas.SaveLayerFlags  # value = <SaveLayerFlags.kInitWithPrevious_SaveLayerFlag: 4>
        kPreserveLCDText_SaveLayerFlag: animator.skia.Canvas.SaveLayerFlags  # value = <SaveLayerFlags.kPreserveLCDText_SaveLayerFlag: 2>
        pass

    class SaveLayerRec:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(
            self,
            bounds: _Rect | None = None,
            paint: Paint | None = None,
            backdrop: ImageFilter | None = None,
            saveLayerFlags: int = 0,
        ) -> None: ...
        @typing.overload
        def __init__(
            self, bounds: _Rect | None = None, paint: Paint | None = None, saveLayerFlags: int = 0
        ) -> None: ...
        @property
        def fBackdrop(self) -> ImageFilter:
            """
            :type: ImageFilter
            """
        @fBackdrop.setter
        def fBackdrop(self, arg0: ImageFilter) -> None:
            pass
        @property
        def fBounds(self) -> Rect:
            """
            :type: _Rect
            """
        @fBounds.setter
        def fBounds(self, arg0: _Rect) -> None:
            pass
        @property
        def fPaint(self) -> Paint:
            """
            :type: Paint
            """
        @fPaint.setter
        def fPaint(self, arg0: Paint) -> None:
            pass
        @property
        def fSaveLayerFlags(self) -> int:
            """
            :type: int
            """
        @fSaveLayerFlags.setter
        def fSaveLayerFlags(self, arg0: int) -> None:
            pass
        pass

    class SrcRectConstraint:
        """
        Members:

          kStrict_SrcRectConstraint

          kFast_SrcRectConstraint
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
        __members__: dict  # value = {'kStrict_SrcRectConstraint': <SrcRectConstraint.kStrict_SrcRectConstraint: 0>, 'kFast_SrcRectConstraint': <SrcRectConstraint.kFast_SrcRectConstraint: 1>}
        kFast_SrcRectConstraint: animator.skia.Canvas.SrcRectConstraint  # value = <SrcRectConstraint.kFast_SrcRectConstraint: 1>
        kStrict_SrcRectConstraint: animator.skia.Canvas.SrcRectConstraint  # value = <SrcRectConstraint.kStrict_SrcRectConstraint: 0>
        pass
    @staticmethod
    def MakeRasterDirect(
        info: ImageInfo, pixels: buffer, rowBytes: int = 0, props: SurfaceProps | None = None
    ) -> Canvas:
        """
        Allocates raster :py:class:`Canvas` that will draw directly into pixel buffer.

        :param info: :py:class:`ImageInfo` describing pixel buffer
        :param pixels: pixel buffer
        :param rowBytes: number of bytes per row
        :param props: optional :py:class:`SurfaceProps`
        """
    @staticmethod
    def MakeRasterDirectN32(width: int, height: int, pixels: buffer, rowBytes: int) -> Canvas:
        """
        Allocates raster :py:class:`Canvas` that will draw directly into pixel buffer.
        """
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(
        self,
        array: numpy.ndarray,
        ct: ColorType = ColorType.kRGBA_8888_ColorType,
        at: AlphaType = AlphaType.kUnpremul_AlphaType,
        cs: ColorSpace | None = None,
        surfaceProps: SurfaceProps | None = None,
    ) -> None:
        """
        Creates raster :py:class:`Canvas` backed by numpy array.

        :param array: numpy array of shape=(height, width, channels) and appropriate dtype. Must have the valid number
            of channels for the specified color type.
        :param ct: color type
        :param at: alpha type
        :param cs: color space
        :param surfaceProps: optional surface properties
        """
    @typing.overload
    def __init__(self, bitmap: Bitmap) -> None: ...
    @typing.overload
    def __init__(self, bitmap: Bitmap, props: SurfaceProps) -> None: ...
    @typing.overload
    def __init__(self, width: int, height: int, props: SurfaceProps | None = None) -> None: ...
    def __str__(self) -> str: ...
    def accessTopLayerPixels(self) -> tuple | None:
        """
        Returns a tuple of ``(memoryview of pixels, image info, rowBytes, origin)`` if the pixels can be read directly.
        Otherwise, returns ``None``.
        """
    @typing.overload
    def clear(self, color: _Color4f) -> None: ...
    @typing.overload
    def clear(self, color: _Color) -> None: ...
    def clipIRect(self, irect: _IRect, op: ClipOp = ClipOp.kIntersect) -> None: ...
    def clipPath(self, path: Path, op: ClipOp = ClipOp.kIntersect, doAntiAlias: bool = False) -> None: ...
    def clipRRect(self, rrect: RRect, op: ClipOp = ClipOp.kIntersect, doAntiAlias: bool = False) -> None: ...
    def clipRect(self, rect: _Rect, op: ClipOp = ClipOp.kIntersect, doAntiAlias: bool = False) -> None: ...
    def clipRegion(self, deviceRgn: Region, op: ClipOp = ClipOp.kIntersect) -> None: ...
    def clipShader(self, sh: Shader, op: ClipOp = ClipOp.kIntersect) -> None: ...
    def concat(self, matrix: Matrix) -> None: ...
    def discard(self) -> None: ...
    def drawArc(self, oval: _Rect, startAngle: float, sweepAngle: float, useCenter: bool, paint: Paint) -> None: ...
    def drawAtlas(
        self,
        atlas: Image,
        xform: list[RSXform] | None,
        tex: list[_Rect],
        colors: list[_Color] | None,
        mode: BlendMode,
        sampling: SamplingOptions,
        cullRect: _Rect | None = None,
        paint: Paint | None = None,
    ) -> None:
        """
        Draws a set of sprites from *atlas*, defined by *xform*, *tex*, and *colors* using *mode* and *sampling*.
        """
    @typing.overload
    def drawCircle(self, center: _Point, radius: float, paint: Paint) -> None: ...
    @typing.overload
    def drawCircle(self, cx: float, cy: float, radius: float, paint: Paint) -> None: ...
    @typing.overload
    def drawColor(self, color: _Color4f, mode: BlendMode = BlendMode.kSrcOver) -> None: ...
    @typing.overload
    def drawColor(self, color: _Color, mode: BlendMode = BlendMode.kSrcOver) -> None: ...
    def drawDRRect(self, outer: RRect, inner: RRect, paint: Paint) -> None: ...
    @typing.overload
    def drawGlyphs(
        self,
        glyphs: list[int],
        positions: list[_Point],
        clusters: list[int],
        utf8text: str,
        origin: _Point,
        font: Font,
        paint: Paint,
    ) -> None:
        """
        Draws *glyphs*, at *positions* relative to *origin* styled with *font* and *paint* with supporting *utf8text*
        and *clusters* information.
        """
    @typing.overload
    def drawGlyphs(self, glyphs: list[int], positions: list[_Point], origin: _Point, font: Font, paint: Paint) -> None:
        """Draws *glyphs*, at *positions* relative to *origin* styled with *font* and *paint*."""
    @typing.overload
    def drawGlyphs(self, glyphs: list[int], xforms: list[RSXform], origin: _Point, font: Font, paint: Paint) -> None:
        """Draws *glyphs*, with *xforms* relative to *origin* styled with *font* and *paint*."""
    def drawIRect(self, rect: _IRect, paint: Paint) -> None: ...
    @typing.overload
    def drawImage(self, image: Image, left: float, top: float) -> None: ...
    @typing.overload
    def drawImage(
        self, image: Image, left: float, top: float, sampling: SamplingOptions = ..., paint: Paint | None = None
    ) -> None: ...
    def drawImageLattice(
        self,
        image: Image,
        lattice: Canvas.Lattice,
        dst: _Rect,
        filter: FilterMode = FilterMode.kNearest,
        paint: Paint | None = None,
    ) -> None: ...
    def drawImageNine(
        self, image: Image, center: _IRect, dst: _Rect, filter: FilterMode, paint: Paint | None = None
    ) -> None: ...
    @typing.overload
    def drawImageRect(
        self, image: Image, dst: _Rect, sampling: SamplingOptions = ..., paint: Paint | None = None
    ) -> None: ...
    @typing.overload
    def drawImageRect(
        self,
        image: Image,
        src: _Rect,
        dst: _Rect,
        sampling: SamplingOptions = ...,
        paint: Paint | None = None,
        constraint: Canvas.SrcRectConstraint = SrcRectConstraint.kFast_SrcRectConstraint,
    ) -> None: ...
    @typing.overload
    def drawLine(self, p0: _Point, p1: _Point, paint: Paint) -> None: ...
    @typing.overload
    def drawLine(self, x0: float, y0: float, x1: float, y1: float, paint: Paint) -> None: ...
    def drawOval(self, oval: _Rect, paint: Paint) -> None: ...
    def drawPaint(self, paint: Paint) -> None: ...
    def drawParagraph(self, paragraph: textlayout.Paragraph, x: float, y: float) -> None:
        """
        Draws the *paragraph* at the given *x* and *y* position.
        """
    def drawPatch(
        self,
        cubics: typing.Sequence[_Point],
        colors: typing.Sequence[_Color] | None,
        texCoords: typing.Sequence[_Point] | None,
        mode: BlendMode,
        paint: Paint,
    ) -> None: ...
    def drawPath(self, path: Path, paint: Paint) -> None: ...
    def drawPicture(self, picture: Picture, matrix: Matrix | None = None, paint: Paint | None = None) -> None: ...
    @typing.overload
    def drawPoint(self, p: _Point, paint: Paint) -> None: ...
    @typing.overload
    def drawPoint(self, x: float, y: float, paint: Paint) -> None: ...
    def drawPoints(self, mode: Canvas.PointMode, pts: list[_Point], paint: Paint) -> None:
        """
        Draw a list of points, *pts*, with the specified *mode* and *paint*.
        """
    def drawRRect(self, rrect: RRect, paint: Paint) -> None: ...
    def drawRect(self, rect: _Rect, paint: Paint) -> None: ...
    def drawRegion(self, region: Region, paint: Paint) -> None: ...
    def drawRoundRect(self, rect: _Rect, rx: float, ry: float, paint: Paint) -> None: ...
    def drawShadow(
        self,
        path: Path,
        zPlaneParams: _Point3,
        lightPos: _Point3,
        lightRadius: float,
        ambientColor: _Color,
        spotColor: _Color,
        flags: int = ShadowFlags.kNone_ShadowFlag,
    ) -> None:
        """
        Draw an offset spot shadow and outlining ambient shadow for the given *path* using a disc light.
        """
    def drawSimpleText(self, text: str, encoding: TextEncoding, x: float, y: float, font: Font, paint: Paint) -> None:
        """
        Draws *text* at (*x*, *y*) using *font* and *paint*.
        """
    def drawString(self, text: str, x: float, y: float, font: Font, paint: Paint) -> None: ...
    def drawText(
        self,
        text: str,
        x: float,
        y: float,
        font: Font,
        paint: Paint,
        encoding: TextEncoding = TextEncoding.kUTF8,
        align: TextUtils_Align = TextUtils_Align.kLeft_Align,
    ) -> None:
        """
        Draws the *text* at (*x*, *y*) using the given *font* and *paint* useing SkTextUtils.
        """
    def drawTextBlob(self, blob: TextBlob, x: float, y: float, paint: Paint) -> None: ...
    def drawVertices(self, vertices: Vertices, mode: BlendMode, paint: Paint) -> None: ...
    def getBaseLayerSize(self) -> ISize: ...
    def getBaseProps(self) -> SurfaceProps: ...
    def getDeviceClipBounds(self) -> IRect: ...
    def getLocalClipBounds(self) -> Rect: ...
    def getLocalToDeviceAs3x3(self) -> Matrix: ...
    def getProps(self) -> SurfaceProps | None:
        """
        Returns :py:class:`SurfaceProps`, if :py:class:`Canvas` is associated with raster surface. Otherwise,
        returns ``None``.
        """
    def getSaveCount(self) -> int: ...
    def getSurface(self) -> Surface: ...
    def getTopProps(self) -> SurfaceProps: ...
    def getTotalMatrix(self) -> Matrix: ...
    def imageInfo(self) -> ImageInfo: ...
    def isClipEmpty(self) -> bool: ...
    def isClipRect(self) -> bool: ...
    def makeSurface(self, info: ImageInfo, props: SurfaceProps | None = None) -> Surface: ...
    def peekPixels(self) -> Pixmap:
        """
        Returns a :py:class:`Pixmap` describing the pixel data.
        """
    @typing.overload
    def quickReject(self, path: Path) -> bool: ...
    @typing.overload
    def quickReject(self, rect: _Rect) -> bool: ...
    @typing.overload
    def readPixels(self, bitmap: Bitmap, srcX: int = 0, srcY: int = 0) -> bool: ...
    @typing.overload
    def readPixels(
        self, dstInfo: ImageInfo, dstPixels: buffer, dstRowBytes: int = 0, srcX: int = 0, srcY: int = 0
    ) -> bool:
        """
        Copies *dstInfo* pixels starting from (*srcX*, *srcY*) to *dstPixels* buffer.
        """
    @typing.overload
    def readPixels(self, pixmap: Pixmap, srcX: int = 0, srcY: int = 0) -> bool: ...
    def resetMatrix(self) -> None: ...
    def restore(self) -> None: ...
    def restoreToCount(self, saveCount: int) -> None: ...
    @typing.overload
    def rotate(self, degrees: float) -> None: ...
    @typing.overload
    def rotate(self, degrees: float, px: float, py: float) -> None: ...
    def save(self) -> int: ...
    @typing.overload
    def saveLayer(self, bounds: _Rect | None = None, paint: Paint | None = None) -> int: ...
    @typing.overload
    def saveLayer(self, layerRec: Canvas.SaveLayerRec) -> int: ...
    def saveLayerAlpha(self, bounds: _Rect | None, alpha: int) -> int: ...
    def saveLayerAlphaf(self, bounds: _Rect | None, alpha: float) -> int: ...
    def scale(self, sx: float, sy: float) -> None: ...
    def setMatrix(self, matrix: Matrix) -> None: ...
    def skew(self, sx: float, sy: float) -> None: ...
    def toarray(
        self,
        srcX: int = 0,
        srcY: int = 0,
        ct: ColorType = ColorType.kRGBA_8888_ColorType,
        at: AlphaType = AlphaType.kUnpremul_AlphaType,
        cs: ColorSpace | None = None,
    ) -> numpy.ndarray:
        """
        Returns a ``ndarray`` of the current canvas' pixels.
        """
    def translate(self, dx: float, dy: float) -> None: ...
    @typing.overload
    def writePixels(self, bitmap: Bitmap, x: int = 0, y: int = 0) -> bool: ...
    @typing.overload
    def writePixels(self, info: ImageInfo, pixels: buffer, rowBytes: int = 0, x: int = 0, y: int = 0) -> bool:
        """
        Writes *pixels* from a buffer to the canvas.
        """

class ClipOp:
    """
    Members:

      kDifference

      kIntersect

      kMax_EnumValue
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
    __members__: dict  # value = {'kDifference': <ClipOp.kDifference: 0>, 'kIntersect': <ClipOp.kIntersect: 1>, 'kMax_EnumValue': <ClipOp.kIntersect: 1>}
    kDifference: animator.skia.ClipOp  # value = <ClipOp.kDifference: 0>
    kIntersect: animator.skia.ClipOp  # value = <ClipOp.kIntersect: 1>
    kMax_EnumValue: animator.skia.ClipOp  # value = <ClipOp.kIntersect: 1>
    pass

class Color4f:
    @staticmethod
    def FromBytes_RGBA(color: _Color) -> Color4f: ...
    @staticmethod
    def FromColor(color: _Color) -> Color4f: ...
    @staticmethod
    def FromPMColor(pmcolor: _Color) -> Color4f: ...
    def __eq__(self, other: _Color4f) -> bool: ...
    def __getitem__(self, index: int) -> float: ...
    @typing.overload
    def __init__(self, color: _Color) -> None:
        """
        Create a new :py:class:`Color4f` from an ARGB color.

        :param color: ARGB color to convert
        """
    @typing.overload
    def __init__(self, red: float, green: float, blue: float, alpha: float = 1.0) -> None:
        """
        Create a new Color4f instance initialized with the given values.

        :red: red components
        :green: green components
        :blue: blue components
        :alpha: alpha components
        """
    @typing.overload
    def __init__(self, t: tuple) -> None:
        """
        Create a new Color4f instance given (R, G, B) or (R, G, B, A) tuple.

        :param t: tuple of color components
        """
    def __int__(self) -> int:
        """
        Convert the color to an integer (ARGB color).

        :return: ARGB color
        """
    def __len__(self) -> int: ...
    @typing.overload
    def __mul__(self, scale: _Color4f) -> Color4f: ...
    @typing.overload
    def __mul__(self, scale: float) -> Color4f: ...
    def __ne__(self, other: _Color4f) -> bool: ...
    def __setitem__(self, index: int, value: float) -> None: ...
    def __str__(self) -> str: ...
    def array(self) -> numpy.ndarray:
        """
        Return a numpy array of the color components. Changes to the array will be reflected in the color.

        :return: numpy array of the color components
        """
    def fitsInBytes(self) -> bool: ...
    def isOpaque(self) -> bool: ...
    def makeOpaque(self) -> Color4f: ...
    def premul(self) -> Color4f: ...
    def toBytes_RGBA(self) -> int: ...
    def toColor(self) -> int: ...
    def vec(self) -> memoryview: ...
    @property
    def fA(self) -> float:
        """
        :type: float
        """
    @fA.setter
    def fA(self, arg0: float) -> None:
        pass
    @property
    def fB(self) -> float:
        """
        :type: float
        """
    @fB.setter
    def fB(self, arg0: float) -> None:
        pass
    @property
    def fG(self) -> float:
        """
        :type: float
        """
    @fG.setter
    def fG(self, arg0: float) -> None:
        pass
    @property
    def fR(self) -> float:
        """
        :type: float
        """
    @fR.setter
    def fR(self, arg0: float) -> None:
        pass
    kBlack: animator.skia.Color4f
    kBlue: animator.skia.Color4f
    kCyan: animator.skia.Color4f
    kDkGray: animator.skia.Color4f
    kGray: animator.skia.Color4f
    kGreen: animator.skia.Color4f
    kLtGray: animator.skia.Color4f
    kMagenta: animator.skia.Color4f
    kRed: animator.skia.Color4f
    kTransparent: animator.skia.Color4f
    kWhite: animator.skia.Color4f
    kYellow: animator.skia.Color4f
    pass

_Color4f = Color4f | int | tuple[float, float, float, float]
_Color = int | Color4f

class ColorChannel:
    """
    Members:

      kR

      kG

      kB

      kA

      kLastEnum
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
    __members__: dict  # value = {'kR': <ColorChannel.kR: 0>, 'kG': <ColorChannel.kG: 1>, 'kB': <ColorChannel.kB: 2>, 'kA': <ColorChannel.kA: 3>, 'kLastEnum': <ColorChannel.kA: 3>}
    kA: animator.skia.ColorChannel  # value = <ColorChannel.kA: 3>
    kB: animator.skia.ColorChannel  # value = <ColorChannel.kB: 2>
    kG: animator.skia.ColorChannel  # value = <ColorChannel.kG: 1>
    kLastEnum: animator.skia.ColorChannel  # value = <ColorChannel.kA: 3>
    kR: animator.skia.ColorChannel  # value = <ColorChannel.kR: 0>
    pass

class ColorChannelFlag(IntEnum):
    """
    Members:

      kRed_ColorChannelFlag

      kGreen_ColorChannelFlag

      kBlue_ColorChannelFlag

      kAlpha_ColorChannelFlag

      kGray_ColorChannelFlag

      kGrayAlpha_ColorChannelFlags

      kRG_ColorChannelFlags

      kRGB_ColorChannelFlags

      kRGBA_ColorChannelFlags
    """

    def __and__(self, other: object) -> object: ...
    def __eq__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __gt__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __invert__(self) -> object: ...
    def __le__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __or__(self, other: object) -> object: ...
    def __rand__(self, other: object) -> object: ...
    def __repr__(self) -> str: ...
    def __ror__(self, other: object) -> object: ...
    def __rxor__(self, other: object) -> object: ...
    def __setstate__(self, state: int) -> None: ...
    def __xor__(self, other: object) -> object: ...
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
    __members__: dict  # value = {'kRed_ColorChannelFlag': <ColorChannelFlag.kRed_ColorChannelFlag: 1>, 'kGreen_ColorChannelFlag': <ColorChannelFlag.kGreen_ColorChannelFlag: 2>, 'kBlue_ColorChannelFlag': <ColorChannelFlag.kBlue_ColorChannelFlag: 4>, 'kAlpha_ColorChannelFlag': <ColorChannelFlag.kAlpha_ColorChannelFlag: 8>, 'kGray_ColorChannelFlag': <ColorChannelFlag.kGray_ColorChannelFlag: 16>, 'kGrayAlpha_ColorChannelFlags': <ColorChannelFlag.kGrayAlpha_ColorChannelFlags: 24>, 'kRG_ColorChannelFlags': <ColorChannelFlag.kRG_ColorChannelFlags: 3>, 'kRGB_ColorChannelFlags': <ColorChannelFlag.kRGB_ColorChannelFlags: 7>, 'kRGBA_ColorChannelFlags': <ColorChannelFlag.kRGBA_ColorChannelFlags: 15>}
    kAlpha_ColorChannelFlag: animator.skia.ColorChannelFlag  # value = <ColorChannelFlag.kAlpha_ColorChannelFlag: 8>
    kBlue_ColorChannelFlag: animator.skia.ColorChannelFlag  # value = <ColorChannelFlag.kBlue_ColorChannelFlag: 4>
    kGrayAlpha_ColorChannelFlags: animator.skia.ColorChannelFlag  # value = <ColorChannelFlag.kGrayAlpha_ColorChannelFlags: 24>
    kGray_ColorChannelFlag: animator.skia.ColorChannelFlag  # value = <ColorChannelFlag.kGray_ColorChannelFlag: 16>
    kGreen_ColorChannelFlag: animator.skia.ColorChannelFlag  # value = <ColorChannelFlag.kGreen_ColorChannelFlag: 2>
    kRGBA_ColorChannelFlags: animator.skia.ColorChannelFlag  # value = <ColorChannelFlag.kRGBA_ColorChannelFlags: 15>
    kRGB_ColorChannelFlags: animator.skia.ColorChannelFlag  # value = <ColorChannelFlag.kRGB_ColorChannelFlags: 7>
    kRG_ColorChannelFlags: animator.skia.ColorChannelFlag  # value = <ColorChannelFlag.kRG_ColorChannelFlags: 3>
    kRed_ColorChannelFlag: animator.skia.ColorChannelFlag  # value = <ColorChannelFlag.kRed_ColorChannelFlag: 1>
    pass

class ColorFilter(Flattenable):
    @staticmethod
    def Deserialize(buffer: buffer) -> ColorFilter:
        """
        Deserialize a color filter from a buffer.
        """
    def asAColorMatrix(self) -> list[float] | None:
        """
        If the filter can be represented by a 5x4 matrix, this returns list of floats appropriately. If not,
        this returns ``None``.

        :return: list of floats or None
        :rtype: List[float] | None
        """
    def asAColorMode(self) -> tuple | None:
        """
        If the filter can be represented by a source color plus Mode, this returns (color, mode) appropriately.
        If not, this returns ``None``.

        :return: (color, mode) or None
        :rtype: Tuple[int, skia.BlendMode] | None
        """
    def filterColor(self, color: _Color) -> int: ...
    def filterColor4f(self, srcColor: _Color4f, srcCS: ColorSpace, dstCS: ColorSpace) -> Color4f: ...
    def isAlphaUnchanged(self) -> bool: ...
    def makeComposed(self, inner: ColorFilter) -> ColorFilter: ...
    pass

class ColorFilters:
    @staticmethod
    @typing.overload
    def Blend(c: _Color4f, cs: ColorSpace, mode: BlendMode) -> ColorFilter: ...
    @staticmethod
    @typing.overload
    def Blend(c: _Color, mode: BlendMode) -> ColorFilter: ...
    @staticmethod
    def Compose(outer: ColorFilter, inner: ColorFilter) -> ColorFilter: ...
    @staticmethod
    @typing.overload
    def HSLAMatrix(cm: ColorMatrix) -> ColorFilter: ...
    @staticmethod
    @typing.overload
    def HSLAMatrix(rowMajor: list[float]) -> ColorFilter: ...
    @staticmethod
    def Lerp(t: float, dst: ColorFilter, src: ColorFilter) -> ColorFilter: ...
    @staticmethod
    def Lighting(mul: _Color, add: _Color) -> ColorFilter: ...
    @staticmethod
    def LinearToSRGBGamma() -> ColorFilter: ...
    @staticmethod
    @typing.overload
    def Matrix(cm: ColorMatrix) -> ColorFilter: ...
    @staticmethod
    @typing.overload
    def Matrix(rowMajor: list[float]) -> ColorFilter: ...
    @staticmethod
    def SRGBToLinearGamma() -> ColorFilter: ...
    @staticmethod
    @typing.overload
    def Table(table: ColorTable) -> ColorFilter: ...
    @staticmethod
    @typing.overload
    def Table(table: list[int]) -> ColorFilter: ...
    @staticmethod
    def TableARGB(
        tableA: list[int] | None,
        tableR: list[int] | None,
        tableG: list[int] | None,
        tableB: list[int] | None,
    ) -> ColorFilter: ...
    pass

class ColorInfo:
    def __eq__(self, arg0: ColorInfo) -> bool: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: ColorInfo) -> None: ...
    @typing.overload
    def __init__(self, ct: ColorType, at: AlphaType, cs: ColorSpace | None = None) -> None: ...
    def __ne__(self, arg0: ColorInfo) -> bool: ...
    def __str__(self) -> str: ...
    def alphaType(self) -> AlphaType: ...
    def bytesPerPixel(self) -> int: ...
    def colorSpace(self) -> ColorSpace: ...
    def colorType(self) -> ColorType: ...
    def gammaCloseToSRGB(self) -> bool: ...
    def isOpaque(self) -> bool: ...
    def makeAlphaType(self, newAlphaType: AlphaType) -> ColorInfo: ...
    def makeColorSpace(self, cs: ColorSpace) -> ColorInfo: ...
    def makeColorType(self, newColorType: ColorType) -> ColorInfo: ...
    def refColorSpace(self) -> ColorSpace: ...
    def shiftPerPixel(self) -> int: ...
    pass

class ColorMatrix:
    @staticmethod
    def RGBtoYUV(cs: YUVColorSpace) -> ColorMatrix: ...
    @staticmethod
    def YUVtoRGB(cs: YUVColorSpace) -> ColorMatrix: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(
        self,
        m00: float,
        m01: float,
        m02: float,
        m03: float,
        m04: float,
        m10: float,
        m11: float,
        m12: float,
        m13: float,
        m14: float,
        m20: float,
        m21: float,
        m22: float,
        m23: float,
        m24: float,
        m30: float,
        m31: float,
        m32: float,
        m33: float,
        m34: float,
    ) -> None: ...
    @typing.overload
    def __init__(self, m: list[float]) -> None:
        """
        Construct a color matrix from a list of 20 floats.
        """
    def __str__(self) -> str: ...
    def getRowMajor(self) -> list[float]:
        """
        Returns a list of 20 floats representing the row-major matrix.
        """
    def postConcat(self, mat: ColorMatrix) -> None: ...
    def postTranslate(self, dr: float, dg: float, db: float, da: float) -> None: ...
    def preConcat(self, mat: ColorMatrix) -> None: ...
    def setConcat(self, a: ColorMatrix, b: ColorMatrix) -> None: ...
    def setIdentity(self) -> None: ...
    def setRowMajor(self, src: list[float]) -> None: ...
    def setSaturation(self, sat: float) -> None: ...
    def setScale(self, rScale: float, gScale: float, bScale: float, aScale: float = 1) -> None: ...
    pass

class ColorMatrixFilter(ColorFilter, Flattenable):
    @staticmethod
    def MakeLightingFilter(mul: int, add: int) -> ColorFilter: ...
    pass

class ColorSpace:
    @staticmethod
    def Deserialize(buffer: buffer) -> ColorSpace:
        """
        Deserialize a color space from a buffer.
        """
    @staticmethod
    def Equals(x: ColorSpace, y: ColorSpace) -> bool: ...
    @staticmethod
    def Make(profile: cms.ICCProfile) -> ColorSpace: ...
    @staticmethod
    def MakeRGB(transferFn: cms.TransferFunction, toXYZ: cms.Matrix3x3) -> ColorSpace: ...
    @staticmethod
    def MakeSRGB() -> ColorSpace: ...
    @staticmethod
    def MakeSRGBLinear() -> ColorSpace: ...
    def __eq__(self, arg0: ColorSpace) -> bool: ...
    def __hash__(self) -> int: ...
    def __init__(self, profile: cms.ICCProfile) -> None: ...
    def __str__(self) -> str: ...
    def gammaCloseToSRGB(self) -> bool: ...
    def gammaIsLinear(self) -> bool: ...
    def gamutTransformTo(self, dst: ColorSpace) -> cms.Matrix3x3:
        """
        Returns the matrix that transforms from this color space to the destination color space.

        :param skia.ColorSpace dst: The destination color space.
        :return: The matrix that transforms from this color space to the destination color space.
        :rtype: skia.cms.Matrix3x3
        """
    def hash(self) -> int: ...
    def invTransferFn(self) -> cms.TransferFunction:
        """
        Returns the inverse transfer function from this color space.
        """
    def isNumericalTransferFn(self) -> cms.TransferFunction | None:
        """
        Returns the transfer function from this color space if the transfer function can be represented as
        coefficients to the standard ICC 7-parameter equation. Returns ``None`` otherwise (eg, PQ, HLG).

        :return: The transfer function from this color space.
        :rtype: skia.cms.TransferFunction | None
        """
    def isSRGB(self) -> bool: ...
    def makeColorSpin(self) -> ColorSpace: ...
    def makeLinearGamma(self) -> ColorSpace: ...
    def makeSRGBGamma(self) -> ColorSpace: ...
    def serialize(self) -> Data: ...
    def toProfile(self) -> cms.ICCProfile:
        """
        Convert this color space to an skcms ICC profile struct and return it.
        """
    def toXYZD50(self) -> cms.Matrix3x3 | None:
        """
        Returns the matrix if the color gamut can be described as a matrix. Returns ``None`` otherwise.

        :return: The matrix describing this color space.
        :rtype: skia.cms.Matrix3x3 | None
        """
    def toXYZD50Hash(self) -> int: ...
    def transferFn(self) -> cms.TransferFunction:
        """
        Returns the transfer function from this color space.
        """
    def transferFnHash(self) -> int: ...
    pass

class ColorSpacePrimaries:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(
        self, fRX: float, fRY: float, fGX: float, fGY: float, fBX: float, fBY: float, fWX: float, fWY: float
    ) -> None: ...
    def toXYZD50(self) -> cms.Matrix3x3: ...
    @property
    def fBX(self) -> float:
        """
        :type: float
        """
    @fBX.setter
    def fBX(self, arg0: float) -> None:
        pass
    @property
    def fBY(self) -> float:
        """
        :type: float
        """
    @fBY.setter
    def fBY(self, arg0: float) -> None:
        pass
    @property
    def fGX(self) -> float:
        """
        :type: float
        """
    @fGX.setter
    def fGX(self, arg0: float) -> None:
        pass
    @property
    def fGY(self) -> float:
        """
        :type: float
        """
    @fGY.setter
    def fGY(self, arg0: float) -> None:
        pass
    @property
    def fRX(self) -> float:
        """
        :type: float
        """
    @fRX.setter
    def fRX(self, arg0: float) -> None:
        pass
    @property
    def fRY(self) -> float:
        """
        :type: float
        """
    @fRY.setter
    def fRY(self, arg0: float) -> None:
        pass
    @property
    def fWX(self) -> float:
        """
        :type: float
        """
    @fWX.setter
    def fWX(self, arg0: float) -> None:
        pass
    @property
    def fWY(self) -> float:
        """
        :type: float
        """
    @fWY.setter
    def fWY(self, arg0: float) -> None:
        pass
    pass

class ColorTable:
    @staticmethod
    @typing.overload
    def Make(table: list[int]) -> ColorTable: ...
    @staticmethod
    @typing.overload
    def Make(
        tableA: list[int] | None, tableR: list[int] | None, tableG: list[int] | None, tableB: list[int] | None
    ) -> ColorTable: ...
    @typing.overload
    def __init__(self, table: list[int]) -> None: ...
    @typing.overload
    def __init__(
        self, tableA: list[int] | None, tableR: list[int] | None, tableG: list[int] | None, tableB: list[int] | None
    ) -> None: ...
    def alphaTable(self) -> memoryview: ...
    def blueTable(self) -> memoryview: ...
    def greenTable(self) -> memoryview: ...
    def redTable(self) -> memoryview: ...
    pass

class ColorType:
    """
    Members:

      kUnknown_ColorType

      kAlpha_8_ColorType

      kRGB_565_ColorType

      kARGB_4444_ColorType

      kRGBA_8888_ColorType

      kRGB_888x_ColorType

      kBGRA_8888_ColorType

      kRGBA_1010102_ColorType

      kBGRA_1010102_ColorType

      kRGB_101010x_ColorType

      kBGR_101010x_ColorType

      kBGR_101010x_XR_ColorType

      kGray_8_ColorType

      kRGBA_F16Norm_ColorType

      kRGBA_F16_ColorType

      kRGBA_F32_ColorType

      kR8G8_unorm_ColorType

      kA16_float_ColorType

      kR16G16_float_ColorType

      kA16_unorm_ColorType

      kR16G16_unorm_ColorType

      kR16G16B16A16_unorm_ColorType

      kSRGBA_8888_ColorType

      kR8_unorm_ColorType

      kLastEnum_ColorType

      kN32_ColorType
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
    def bytesPerPixel(self) -> int:
        """
        Returns the number of bytes required to store a pixel, including unused padding. Returns zero if this
        is *kUnknown_ColorType* or invalid.

        :return: bytes per pixel
        """
    def isAlwaysOpaque(self) -> bool:
        """
        Returns true if :py:class:`ColorType` always decodes alpha to 1.0, making the pixel fully opaque. If
        ``True``, :py:class:`ColorType` does not reserve bits to encode alpha.

        :return: true if alpha is always set to 1.0
        """
    def validateAlphaType(self, alphaType: AlphaType) -> AlphaType | None:
        """
        Returns a :py:class:`AlphaType` if this *colorType* has a valid :py:class:`AlphaType`.

        Returns ``None`` only if *alphaType* is :py:attr:`~skia.Type.kUnknown_AlphaType`, color type is not
        :py:attr:`~skia.ColorType.kUnknown_ColorType`, and :py:class:`ColorType` is not always opaque.

        :param alphaType: alpha type
        :return: alpha type for this color type, or ``None``
        :rtype: :py:class:`AlphaType` | None
        """
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
    __members__: dict  # value = {'kUnknown_ColorType': <ColorType.kUnknown_ColorType: 0>, 'kAlpha_8_ColorType': <ColorType.kAlpha_8_ColorType: 1>, 'kRGB_565_ColorType': <ColorType.kRGB_565_ColorType: 2>, 'kARGB_4444_ColorType': <ColorType.kARGB_4444_ColorType: 3>, 'kRGBA_8888_ColorType': <ColorType.kRGBA_8888_ColorType: 4>, 'kRGB_888x_ColorType': <ColorType.kRGB_888x_ColorType: 5>, 'kBGRA_8888_ColorType': <ColorType.kBGRA_8888_ColorType: 6>, 'kRGBA_1010102_ColorType': <ColorType.kRGBA_1010102_ColorType: 7>, 'kBGRA_1010102_ColorType': <ColorType.kBGRA_1010102_ColorType: 8>, 'kRGB_101010x_ColorType': <ColorType.kRGB_101010x_ColorType: 9>, 'kBGR_101010x_ColorType': <ColorType.kBGR_101010x_ColorType: 10>, 'kBGR_101010x_XR_ColorType': <ColorType.kBGR_101010x_XR_ColorType: 11>, 'kGray_8_ColorType': <ColorType.kGray_8_ColorType: 12>, 'kRGBA_F16Norm_ColorType': <ColorType.kRGBA_F16Norm_ColorType: 13>, 'kRGBA_F16_ColorType': <ColorType.kRGBA_F16_ColorType: 14>, 'kRGBA_F32_ColorType': <ColorType.kRGBA_F32_ColorType: 15>, 'kR8G8_unorm_ColorType': <ColorType.kR8G8_unorm_ColorType: 16>, 'kA16_float_ColorType': <ColorType.kA16_float_ColorType: 17>, 'kR16G16_float_ColorType': <ColorType.kR16G16_float_ColorType: 18>, 'kA16_unorm_ColorType': <ColorType.kA16_unorm_ColorType: 19>, 'kR16G16_unorm_ColorType': <ColorType.kR16G16_unorm_ColorType: 20>, 'kR16G16B16A16_unorm_ColorType': <ColorType.kR16G16B16A16_unorm_ColorType: 21>, 'kSRGBA_8888_ColorType': <ColorType.kSRGBA_8888_ColorType: 22>, 'kR8_unorm_ColorType': <ColorType.kR8_unorm_ColorType: 23>, 'kLastEnum_ColorType': <ColorType.kR8_unorm_ColorType: 23>, 'kN32_ColorType': <ColorType.kRGBA_8888_ColorType: 4>}
    kA16_float_ColorType: animator.skia.ColorType  # value = <ColorType.kA16_float_ColorType: 17>
    kA16_unorm_ColorType: animator.skia.ColorType  # value = <ColorType.kA16_unorm_ColorType: 19>
    kARGB_4444_ColorType: animator.skia.ColorType  # value = <ColorType.kARGB_4444_ColorType: 3>
    kAlpha_8_ColorType: animator.skia.ColorType  # value = <ColorType.kAlpha_8_ColorType: 1>
    kBGRA_1010102_ColorType: animator.skia.ColorType  # value = <ColorType.kBGRA_1010102_ColorType: 8>
    kBGRA_8888_ColorType: animator.skia.ColorType  # value = <ColorType.kBGRA_8888_ColorType: 6>
    kBGR_101010x_ColorType: animator.skia.ColorType  # value = <ColorType.kBGR_101010x_ColorType: 10>
    kBGR_101010x_XR_ColorType: animator.skia.ColorType  # value = <ColorType.kBGR_101010x_XR_ColorType: 11>
    kGray_8_ColorType: animator.skia.ColorType  # value = <ColorType.kGray_8_ColorType: 12>
    kLastEnum_ColorType: animator.skia.ColorType  # value = <ColorType.kR8_unorm_ColorType: 23>
    kN32_ColorType: animator.skia.ColorType  # value = <ColorType.kRGBA_8888_ColorType: 4>
    kR16G16B16A16_unorm_ColorType: animator.skia.ColorType  # value = <ColorType.kR16G16B16A16_unorm_ColorType: 21>
    kR16G16_float_ColorType: animator.skia.ColorType  # value = <ColorType.kR16G16_float_ColorType: 18>
    kR16G16_unorm_ColorType: animator.skia.ColorType  # value = <ColorType.kR16G16_unorm_ColorType: 20>
    kR8G8_unorm_ColorType: animator.skia.ColorType  # value = <ColorType.kR8G8_unorm_ColorType: 16>
    kR8_unorm_ColorType: animator.skia.ColorType  # value = <ColorType.kR8_unorm_ColorType: 23>
    kRGBA_1010102_ColorType: animator.skia.ColorType  # value = <ColorType.kRGBA_1010102_ColorType: 7>
    kRGBA_8888_ColorType: animator.skia.ColorType  # value = <ColorType.kRGBA_8888_ColorType: 4>
    kRGBA_F16Norm_ColorType: animator.skia.ColorType  # value = <ColorType.kRGBA_F16Norm_ColorType: 13>
    kRGBA_F16_ColorType: animator.skia.ColorType  # value = <ColorType.kRGBA_F16_ColorType: 14>
    kRGBA_F32_ColorType: animator.skia.ColorType  # value = <ColorType.kRGBA_F32_ColorType: 15>
    kRGB_101010x_ColorType: animator.skia.ColorType  # value = <ColorType.kRGB_101010x_ColorType: 9>
    kRGB_565_ColorType: animator.skia.ColorType  # value = <ColorType.kRGB_565_ColorType: 2>
    kRGB_888x_ColorType: animator.skia.ColorType  # value = <ColorType.kRGB_888x_ColorType: 5>
    kSRGBA_8888_ColorType: animator.skia.ColorType  # value = <ColorType.kSRGBA_8888_ColorType: 22>
    kUnknown_ColorType: animator.skia.ColorType  # value = <ColorType.kUnknown_ColorType: 0>
    pass

class CornerPathEffect:
    @staticmethod
    def Make(radius: float) -> PathEffect: ...
    pass

class CubicMap:
    @staticmethod
    def IsLinear(p1: _Point, p2: _Point) -> bool: ...
    def __init__(self, p1: _Point, p2: _Point) -> None: ...
    def computeFromT(self, t: float) -> Point: ...
    def computeYFromX(self, x: float) -> float: ...

class CubicResampler:
    @staticmethod
    def CatmullRom() -> CubicResampler: ...
    @staticmethod
    def Mitchell() -> CubicResampler: ...
    def __init__(self, B: float, C: float) -> None: ...
    def __str__(self) -> str: ...
    @property
    def B(self) -> float:
        """
        :type: float
        """
    @B.setter
    def B(self, arg0: float) -> None:
        pass
    @property
    def C(self) -> float:
        """
        :type: float
        """
    @C.setter
    def C(self, arg0: float) -> None:
        pass
    pass

class DashPathEffect:
    @staticmethod
    def Make(intervals: list[float], phase: float = 0) -> PathEffect: ...
    pass

class Data:
    """
    :py:class:`Data` supports Python buffer protocol, meaning that
    :py:class:`Data` can be converted to Python buffer types without copy::

        bytes(data)
        memoryview(data)
        np.array(data)

    :note: Remember to keep a reference to :py:class:`Data` when converting to Python buffer types.
    """

    @staticmethod
    def MakeEmpty() -> Data: ...
    @staticmethod
    def MakeFromFileName(path: str) -> Data: ...
    @staticmethod
    def MakeSubset(src: Data, offset: int, length: int) -> Data: ...
    @staticmethod
    def MakeUninitialized(length: int) -> Data: ...
    @staticmethod
    def MakeWithCString(cstr: str) -> Data:
        """
        Create a new dataref by copying the specified string or bytes.
        """
    @staticmethod
    def MakeWithCopy(data: buffer) -> Data:
        """
        Create a new dataref by copying the specified data.
        """
    @staticmethod
    def MakeWithoutCopy(data: buffer) -> Data: ...
    @staticmethod
    def MakeZeroInitialized(length: int) -> Data: ...
    def __eq__(self, other: Data) -> bool:
        """
        Same as :py:meth:`~Data.equals`.
        """
    def __init__(self, buf: buffer, copy: bool = False) -> None:
        """
        Create a new :py:class:`Data`.

        :param bytes|bytearray|memoryview buf: Buffer object
        :param bool copy: Whether to copy data, default `False`.
        """
    def __str__(self) -> str: ...
    def bytes(self) -> bytes:
        """
        Like :py:meth:``~Data.data``, returns a read-only ptr into the data, but in this case it is cast to
        ``bytes``.
        """
    def copyRange(self, offset: int, length: int, buffer: buffer | None) -> int:
        """
        Helper to copy a range of the data into a caller-provided buffer.

        Returns the actual number of bytes copied, after clamping offset and length to the size of the data. If
        buffer is NULL, it is ignored, and only the computed number of bytes is returned.
        """
    def data(self) -> memoryview:
        """
        Returns the read-only memoryview to the data.
        """
    def equals(self, other: Data) -> bool: ...
    def isEmpty(self) -> bool: ...
    def size(self) -> int: ...
    def writable_data(self) -> memoryview:
        """
        Returns the read-write memoryview to the data.
        """

class DiscretePathEffect:
    @staticmethod
    def Make(segLength: float, dev: float, seedAssist: int = 0) -> PathEffect: ...
    pass

class EncodedImageFormat:
    """
    Members:

      kBMP

      kGIF

      kICO

      kJPEG

      kPNG

      kWBMP

      kWEBP

      kPKM

      kKTX

      kASTC

      kDNG

      kHEIF

      kAVIF

      kJPEGXL
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
    __members__: dict  # value = {'kBMP': <EncodedImageFormat.kBMP: 0>, 'kGIF': <EncodedImageFormat.kGIF: 1>, 'kICO': <EncodedImageFormat.kICO: 2>, 'kJPEG': <EncodedImageFormat.kJPEG: 3>, 'kPNG': <EncodedImageFormat.kPNG: 4>, 'kWBMP': <EncodedImageFormat.kWBMP: 5>, 'kWEBP': <EncodedImageFormat.kWEBP: 6>, 'kPKM': <EncodedImageFormat.kPKM: 7>, 'kKTX': <EncodedImageFormat.kKTX: 8>, 'kASTC': <EncodedImageFormat.kASTC: 9>, 'kDNG': <EncodedImageFormat.kDNG: 10>, 'kHEIF': <EncodedImageFormat.kHEIF: 11>, 'kAVIF': <EncodedImageFormat.kAVIF: 12>, 'kJPEGXL': <EncodedImageFormat.kJPEGXL: 13>}
    kASTC: animator.skia.EncodedImageFormat  # value = <EncodedImageFormat.kASTC: 9>
    kAVIF: animator.skia.EncodedImageFormat  # value = <EncodedImageFormat.kAVIF: 12>
    kBMP: animator.skia.EncodedImageFormat  # value = <EncodedImageFormat.kBMP: 0>
    kDNG: animator.skia.EncodedImageFormat  # value = <EncodedImageFormat.kDNG: 10>
    kGIF: animator.skia.EncodedImageFormat  # value = <EncodedImageFormat.kGIF: 1>
    kHEIF: animator.skia.EncodedImageFormat  # value = <EncodedImageFormat.kHEIF: 11>
    kICO: animator.skia.EncodedImageFormat  # value = <EncodedImageFormat.kICO: 2>
    kJPEG: animator.skia.EncodedImageFormat  # value = <EncodedImageFormat.kJPEG: 3>
    kJPEGXL: animator.skia.EncodedImageFormat  # value = <EncodedImageFormat.kJPEGXL: 13>
    kKTX: animator.skia.EncodedImageFormat  # value = <EncodedImageFormat.kKTX: 8>
    kPKM: animator.skia.EncodedImageFormat  # value = <EncodedImageFormat.kPKM: 7>
    kPNG: animator.skia.EncodedImageFormat  # value = <EncodedImageFormat.kPNG: 4>
    kWBMP: animator.skia.EncodedImageFormat  # value = <EncodedImageFormat.kWBMP: 5>
    kWEBP: animator.skia.EncodedImageFormat  # value = <EncodedImageFormat.kWEBP: 6>
    pass

class FilterMode:
    """
    Members:

      kNearest

      kLinear

      kLast
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
    __members__: dict  # value = {'kNearest': <FilterMode.kNearest: 0>, 'kLinear': <FilterMode.kLinear: 1>, 'kLast': <FilterMode.kLinear: 1>}
    kLast: animator.skia.FilterMode  # value = <FilterMode.kLinear: 1>
    kLinear: animator.skia.FilterMode  # value = <FilterMode.kLinear: 1>
    kNearest: animator.skia.FilterMode  # value = <FilterMode.kNearest: 0>
    pass

class Blender(Flattenable):
    @staticmethod
    def Mode(mode: BlendMode) -> Blender: ...
    pass

class Font:
    class Edging:
        """
        Members:

          kAlias

          kAntiAlias

          kSubpixelAntiAlias
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
        __members__: dict  # value = {'kAlias': <Edging.kAlias: 0>, 'kAntiAlias': <Edging.kAntiAlias: 1>, 'kSubpixelAntiAlias': <Edging.kSubpixelAntiAlias: 2>}
        kAlias: animator.skia.Font.Edging  # value = <Edging.kAlias: 0>
        kAntiAlias: animator.skia.Font.Edging  # value = <Edging.kAntiAlias: 1>
        kSubpixelAntiAlias: animator.skia.Font.Edging  # value = <Edging.kSubpixelAntiAlias: 2>
        pass
    def __eq__(self, arg0: Font) -> bool: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, typeface: Typeface) -> None: ...
    @typing.overload
    def __init__(self, typeface: Typeface, size: float) -> None: ...
    @typing.overload
    def __init__(self, typeface: Typeface, size: float, scaleX: float, skewX: float) -> None: ...
    def __ne__(self, arg0: Font) -> bool: ...
    def __str__(self) -> str: ...
    def countText(self, text: str, encoding: TextEncoding = TextEncoding.kUTF8) -> int:
        """
        Returns number of glyphs represented by text.
        """
    def dump(self) -> None: ...
    def getBounds(self, glyphs: list[int], paint: Paint | None = None) -> list[Rect]:
        """
        Returns the bounds for each glyph in *glyphs* with optional *paint*.
        """
    def getEdging(self) -> Font.Edging: ...
    def getHinting(self) -> FontHinting: ...
    def getIntercepts(
        self, glyphs: list[int], pos: list[_Point], top: float, bottom: float, paint: Paint | None = None
    ) -> list[float]:
        """
        Returns intervals [start, end] describing lines parallel to the advance that intersect with the *glyphs*.
        """
    def getMetrics(self) -> tuple[FontMetrics, float]:
        """
        Returns a tuple of (font metrics, line spacing).

        :rtype: Tuple[FontMetrics, float]
        """
    def getPath(self, glyphID: int) -> Path | None:
        """
        Returns path to be the outline of the glyph or None if the glyph has no outline.

        :rtpye: :py:class:`Path` | None
        """
    def getPaths(self, glyphIDs: list[int]) -> list[Path | None]:
        """
        Returns a list of paths to be the outlines of the glyphs. Some elements may be None if the glyph has no
        outline.
        """
    def getPos(self, glyphs: list[int], origin: _Point = ...) -> list[Point]:
        """
        Returns the positions for each glyph, beginning at the specified *origin*.
        """
    def getScaleX(self) -> float: ...
    def getSize(self) -> float: ...
    def getSkewX(self) -> float: ...
    def getSpacing(self) -> float: ...
    def getTypeface(self) -> Typeface: ...
    def getTypefaceOrDefault(self) -> Typeface: ...
    def getWidths(self, glyphs: list[int]) -> list[float]:
        """
        Returns the advance for each glyph in *glyphs*.
        """
    def getWidthsBounds(self, glyphs: list[int], paint: Paint | None = None) -> tuple:
        """
        Returns the advance and bounds for each glyph in *glyphs* with optional *paint*.

        :rtpye: Tuple[List[float], List[:py:class:`Rect`]]
        """
    def getXPos(self, glyphs: list[int], origin: float = 0) -> list[float]:
        """
        Returns the x-positions for each glyph, beginning at the specified *origin*.
        """
    def isBaselineSnap(self) -> bool: ...
    def isEmbeddedBitmaps(self) -> bool: ...
    def isEmbolden(self) -> bool: ...
    def isForceAutoHinting(self) -> bool: ...
    def isLinearMetrics(self) -> bool: ...
    def isSubpixel(self) -> bool: ...
    def makeWithSize(self, size: float) -> Font: ...
    def measureText(
        self, text: str, encoding: TextEncoding = TextEncoding.kUTF8, paint: Paint | None = None
    ) -> tuple[float, Rect]:
        """
        Returns a tuple of (advance width of text, bounding box relative to (0, 0)).

        :param text: The text to measure.
        :param encoding: The encoding of the text.
        :param paint: The paint to use for the text.
        :rtpye: Tuple[float, :py:class:`Rect`]
        """
    def refTypeface(self) -> Typeface: ...
    def refTypefaceOrDefault(self) -> Typeface: ...
    def setBaselineSnap(self, baselineSnap: bool) -> None: ...
    def setEdging(self, edging: Font.Edging) -> None: ...
    def setEmbeddedBitmaps(self, embeddedBitmaps: bool) -> None: ...
    def setEmbolden(self, embolden: bool) -> None: ...
    def setForceAutoHinting(self, forceAutoHinting: bool) -> None: ...
    def setHinting(self, hintingLevel: FontHinting) -> None: ...
    def setLinearMetrics(self, linearMetrics: bool) -> None: ...
    def setScaleX(self, scaleX: float) -> None: ...
    def setSize(self, textSize: float) -> None: ...
    def setSkewX(self, skewX: float) -> None: ...
    def setSubpixel(self, subpixel: bool) -> None: ...
    def setTypeface(self, tf: Typeface) -> None: ...
    def textToGlyphs(self, text: str, encoding: TextEncoding = TextEncoding.kUTF8) -> list[int]:
        """
        Converts text into glyph indices and returns them.
        """
    def unicharToGlyph(self, uni: int) -> int: ...
    def unicharsToGlyphs(self, uni: list[int]) -> list[int]: ...
    defaultSize = 12.0
    pass

class FontArguments:
    class Palette:
        class Override:
            def __init__(self, index: int, color: _Color) -> None: ...
            def __str__(self) -> str: ...
            @property
            def color(self) -> int:
                """
                :type: int
                """
            @color.setter
            def color(self, arg0: int) -> None:
                pass
            @property
            def index(self) -> int:
                """
                :type: int
                """
            @index.setter
            def index(self, arg0: int) -> None:
                pass
            pass

        class OverrideVector:
            def __bool__(self) -> bool:
                """
                Check whether the list is nonempty
                """
            @typing.overload
            def __delitem__(self, arg0: int) -> None:
                """
                Delete the list elements at index ``i``
                """
            @typing.overload
            def __delitem__(self, arg0: slice) -> None:
                """
                Delete list elements using a slice object
                """
            @typing.overload
            def __getitem__(self, arg0: int) -> FontArguments.Palette.Override: ...
            @typing.overload
            def __getitem__(self, s: slice) -> FontArguments.Palette.OverrideVector:
                """
                Retrieve list elements using a slice object
                """
            @typing.overload
            def __init__(self) -> None: ...
            @typing.overload
            def __init__(self, arg0: FontArguments.Palette.OverrideVector) -> None:
                """
                Copy constructor
                """
            @typing.overload
            def __init__(self, arg0: typing.Iterable) -> None: ...
            def __iter__(self) -> typing.Iterator: ...
            def __len__(self) -> int: ...
            @typing.overload
            def __setitem__(self, arg0: int, arg1: FontArguments.Palette.Override) -> None: ...
            @typing.overload
            def __setitem__(self, arg0: slice, arg1: FontArguments.Palette.OverrideVector) -> None:
                """
                Assign list elements using a slice object
                """
            def append(self, x: FontArguments.Palette.Override) -> None:
                """
                Add an item to the end of the list
                """
            def clear(self) -> None:
                """
                Clear the contents
                """
            @typing.overload
            def extend(self, L: FontArguments.Palette.OverrideVector) -> None:
                """
                Extend the list by appending all the items in the given list
                """
            @typing.overload
            def extend(self, L: typing.Iterable) -> None:
                """
                Extend the list by appending all the items in the given list
                """
            def insert(self, i: int, x: FontArguments.Palette.Override) -> None:
                """
                Insert an item at a given position.
                """
            @typing.overload
            def pop(self) -> FontArguments.Palette.Override:
                """
                Remove and return the last item
                """
            @typing.overload
            def pop(self, i: int) -> FontArguments.Palette.Override:
                """
                Remove and return the item at index ``i``
                """
        def __init__(self, index: int, overrides: FontArguments.Palette.OverrideVector) -> None: ...
        def __str__(self) -> str: ...
        @property
        def index(self) -> int:
            """
            :type: int
            """
        @index.setter
        def index(self, arg0: int) -> None:
            pass
        @property
        def overrideCount(self) -> int:
            """
            :type: int
            """
        @property
        def overrides(self) -> FontArguments.Palette.OverrideVector:
            """
            :type: FontArguments.Palette.OverrideVector
            """
        @overrides.setter
        def overrides(self, arg1: FontArguments.Palette.OverrideVector) -> None:
            pass
        pass

    class VariationPosition:
        class Coordinate:
            def __init__(self, axis: int, value: float) -> None: ...
            def __str__(self) -> str: ...
            @property
            def axis(self) -> int:
                """
                :type: int
                """
            @axis.setter
            def axis(self, arg0: int) -> None:
                pass
            @property
            def value(self) -> float:
                """
                :type: float
                """
            @value.setter
            def value(self, arg0: float) -> None:
                pass
            pass

        class CoordinateVector:
            def __bool__(self) -> bool:
                """
                Check whether the list is nonempty
                """
            @typing.overload
            def __delitem__(self, arg0: int) -> None:
                """
                Delete the list elements at index ``i``
                """
            @typing.overload
            def __delitem__(self, arg0: slice) -> None:
                """
                Delete list elements using a slice object
                """
            @typing.overload
            def __getitem__(self, arg0: int) -> FontArguments.VariationPosition.Coordinate: ...
            @typing.overload
            def __getitem__(self, s: slice) -> FontArguments.VariationPosition.CoordinateVector:
                """
                Retrieve list elements using a slice object
                """
            @typing.overload
            def __init__(self) -> None: ...
            @typing.overload
            def __init__(self, arg0: FontArguments.VariationPosition.CoordinateVector) -> None:
                """
                Copy constructor
                """
            @typing.overload
            def __init__(self, arg0: typing.Iterable) -> None: ...
            def __iter__(self) -> typing.Iterator: ...
            def __len__(self) -> int: ...
            @typing.overload
            def __setitem__(self, arg0: int, arg1: FontArguments.VariationPosition.Coordinate) -> None: ...
            @typing.overload
            def __setitem__(self, arg0: slice, arg1: FontArguments.VariationPosition.CoordinateVector) -> None:
                """
                Assign list elements using a slice object
                """
            def append(self, x: FontArguments.VariationPosition.Coordinate) -> None:
                """
                Add an item to the end of the list
                """
            def clear(self) -> None:
                """
                Clear the contents
                """
            @typing.overload
            def extend(self, L: FontArguments.VariationPosition.CoordinateVector) -> None:
                """
                Extend the list by appending all the items in the given list
                """
            @typing.overload
            def extend(self, L: typing.Iterable) -> None:
                """
                Extend the list by appending all the items in the given list
                """
            def insert(self, i: int, x: FontArguments.VariationPosition.Coordinate) -> None:
                """
                Insert an item at a given position.
                """
            @typing.overload
            def pop(self) -> FontArguments.VariationPosition.Coordinate:
                """
                Remove and return the last item
                """
            @typing.overload
            def pop(self, i: int) -> FontArguments.VariationPosition.Coordinate:
                """
                Remove and return the item at index ``i``
                """
        def __init__(self, coordinates: FontArguments.VariationPosition.CoordinateVector) -> None: ...
        def __str__(self) -> str: ...
        @property
        def coordinateCount(self) -> int:
            """
            :type: int
            """
        @property
        def coordinates(self) -> FontArguments.VariationPosition.CoordinateVector:
            """
            :type: FontArguments.VariationPosition.CoordinateVector
            """
        @coordinates.setter
        def coordinates(self, arg1: FontArguments.VariationPosition.CoordinateVector) -> None:
            pass
        pass
    def __init__(self) -> None: ...
    def getCollectionIndex(self) -> int: ...
    def getPalette(self) -> FontArguments.Palette: ...
    def getVariationDesignPosition(self) -> FontArguments.VariationPosition: ...
    def setCollectionIndex(self, collectionIndex: int) -> FontArguments: ...
    def setPalette(self, palette: FontArguments.Palette) -> FontArguments: ...
    def setVariationDesignPosition(self, position: FontArguments.VariationPosition) -> FontArguments: ...
    pass

class FontHinting:
    """
    Members:

      kNone

      kSlight

      kNormal

      kFull
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
    __members__: dict  # value = {'kNone': <FontHinting.kNone: 0>, 'kSlight': <FontHinting.kSlight: 1>, 'kNormal': <FontHinting.kNormal: 2>, 'kFull': <FontHinting.kFull: 3>}
    kFull: animator.skia.FontHinting  # value = <FontHinting.kFull: 3>
    kNone: animator.skia.FontHinting  # value = <FontHinting.kNone: 0>
    kNormal: animator.skia.FontHinting  # value = <FontHinting.kNormal: 2>
    kSlight: animator.skia.FontHinting  # value = <FontHinting.kSlight: 1>
    pass

class FontMetrics:
    class FontMetricsFlags(IntEnum):
        """
        Members:

          kUnderlineThicknessIsValid_Flag

          kUnderlinePositionIsValid_Flag

          kStrikeoutThicknessIsValid_Flag

          kStrikeoutPositionIsValid_Flag

          kBoundsInvalid_Flag
        """

        def __and__(self, other: object) -> object: ...
        def __eq__(self, other: object) -> bool: ...
        def __ge__(self, other: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __gt__(self, other: object) -> bool: ...
        def __hash__(self) -> int: ...
        def __index__(self) -> int: ...
        def __init__(self, value: int) -> None: ...
        def __int__(self) -> int: ...
        def __invert__(self) -> object: ...
        def __le__(self, other: object) -> bool: ...
        def __lt__(self, other: object) -> bool: ...
        def __ne__(self, other: object) -> bool: ...
        def __or__(self, other: object) -> object: ...
        def __rand__(self, other: object) -> object: ...
        def __repr__(self) -> str: ...
        def __ror__(self, other: object) -> object: ...
        def __rxor__(self, other: object) -> object: ...
        def __setstate__(self, state: int) -> None: ...
        def __xor__(self, other: object) -> object: ...
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
        __members__: dict  # value = {'kUnderlineThicknessIsValid_Flag': <FontMetricsFlags.kUnderlineThicknessIsValid_Flag: 1>, 'kUnderlinePositionIsValid_Flag': <FontMetricsFlags.kUnderlinePositionIsValid_Flag: 2>, 'kStrikeoutThicknessIsValid_Flag': <FontMetricsFlags.kStrikeoutThicknessIsValid_Flag: 4>, 'kStrikeoutPositionIsValid_Flag': <FontMetricsFlags.kStrikeoutPositionIsValid_Flag: 8>, 'kBoundsInvalid_Flag': <FontMetricsFlags.kBoundsInvalid_Flag: 16>}
        kBoundsInvalid_Flag: animator.skia.FontMetrics.FontMetricsFlags  # value = <FontMetricsFlags.kBoundsInvalid_Flag: 16>
        kStrikeoutPositionIsValid_Flag: animator.skia.FontMetrics.FontMetricsFlags  # value = <FontMetricsFlags.kStrikeoutPositionIsValid_Flag: 8>
        kStrikeoutThicknessIsValid_Flag: animator.skia.FontMetrics.FontMetricsFlags  # value = <FontMetricsFlags.kStrikeoutThicknessIsValid_Flag: 4>
        kUnderlinePositionIsValid_Flag: animator.skia.FontMetrics.FontMetricsFlags  # value = <FontMetricsFlags.kUnderlinePositionIsValid_Flag: 2>
        kUnderlineThicknessIsValid_Flag: animator.skia.FontMetrics.FontMetricsFlags  # value = <FontMetricsFlags.kUnderlineThicknessIsValid_Flag: 1>
        pass
    def __eq__(self, other: FontMetrics) -> bool: ...
    def __init__(self) -> None: ...
    def __str__(self) -> str: ...
    def hasBounds(self) -> bool: ...
    def hasStrikeoutPosition(self) -> float | None:
        """
        Returns the strikeout position if it is valid, otherwise ``None``.
        """
    def hasStrikeoutThickness(self) -> float | None:
        """
        Returns the strikeout thickness if it is valid, otherwise ``None``.
        """
    def hasUnderlinePosition(self) -> float | None:
        """
        Returns the underline position if it is valid, otherwise ``None``.
        """
    def hasUnderlineThickness(self) -> float | None:
        """
        Returns the underline thickness if it is valid, otherwise ``None``.
        """
    @property
    def fAscent(self) -> float:
        """
        :type: float
        """
    @fAscent.setter
    def fAscent(self, arg0: float) -> None:
        pass
    @property
    def fAvgCharWidth(self) -> float:
        """
        :type: float
        """
    @fAvgCharWidth.setter
    def fAvgCharWidth(self, arg0: float) -> None:
        pass
    @property
    def fBottom(self) -> float:
        """
        :type: float
        """
    @fBottom.setter
    def fBottom(self, arg0: float) -> None:
        pass
    @property
    def fCapHeight(self) -> float:
        """
        :type: float
        """
    @fCapHeight.setter
    def fCapHeight(self, arg0: float) -> None:
        pass
    @property
    def fDescent(self) -> float:
        """
        :type: float
        """
    @fDescent.setter
    def fDescent(self, arg0: float) -> None:
        pass
    @property
    def fFlags(self) -> int:
        """
        :type: int
        """
    @fFlags.setter
    def fFlags(self, arg0: int) -> None:
        pass
    @property
    def fLeading(self) -> float:
        """
        :type: float
        """
    @fLeading.setter
    def fLeading(self, arg0: float) -> None:
        pass
    @property
    def fMaxCharWidth(self) -> float:
        """
        :type: float
        """
    @fMaxCharWidth.setter
    def fMaxCharWidth(self, arg0: float) -> None:
        pass
    @property
    def fStrikeoutPosition(self) -> float:
        """
        :type: float
        """
    @fStrikeoutPosition.setter
    def fStrikeoutPosition(self, arg0: float) -> None:
        pass
    @property
    def fStrikeoutThickness(self) -> float:
        """
        :type: float
        """
    @fStrikeoutThickness.setter
    def fStrikeoutThickness(self, arg0: float) -> None:
        pass
    @property
    def fTop(self) -> float:
        """
        :type: float
        """
    @fTop.setter
    def fTop(self, arg0: float) -> None:
        pass
    @property
    def fUnderlinePosition(self) -> float:
        """
        :type: float
        """
    @fUnderlinePosition.setter
    def fUnderlinePosition(self, arg0: float) -> None:
        pass
    @property
    def fUnderlineThickness(self) -> float:
        """
        :type: float
        """
    @fUnderlineThickness.setter
    def fUnderlineThickness(self, arg0: float) -> None:
        pass
    @property
    def fXHeight(self) -> float:
        """
        :type: float
        """
    @fXHeight.setter
    def fXHeight(self, arg0: float) -> None:
        pass
    @property
    def fXMax(self) -> float:
        """
        :type: float
        """
    @fXMax.setter
    def fXMax(self, arg0: float) -> None:
        pass
    @property
    def fXMin(self) -> float:
        """
        :type: float
        """
    @fXMin.setter
    def fXMin(self, arg0: float) -> None:
        pass
    pass

class FontMgr:
    @staticmethod
    def New_Custom_Data(arg0: list[Data]) -> FontMgr: ...
    @staticmethod
    def RefDefault() -> FontMgr: ...
    @staticmethod
    def RefEmpty() -> FontMgr: ...
    def __getitem__(self, index: int) -> str:
        """
        Same as :py:meth:`getFamilyName`.
        """
    def __init__(self) -> None: ...
    def __len__(self) -> int: ...
    def __str__(self) -> str: ...
    def countFamilies(self) -> int: ...
    def createStyleSet(self, index: int) -> FontStyleSet: ...
    def getFamilyName(self, index: int) -> str:
        """
        Return the name of the font family at the given *index*.
        """
    def legacyMakeTypeface(self, familyName: str, style: FontStyle) -> Typeface: ...
    def makeFromData(self, data: Data, ttcIndex: int = 0) -> Typeface: ...
    def makeFromFile(self, path: str, ttcIndex: int = 0) -> Typeface: ...
    def matchFamily(self, familyName: str | None) -> FontStyleSet: ...
    def matchFamilyStyle(self, familyName: str | None, style: FontStyle) -> Typeface: ...
    def matchFamilyStyleCharacter(
        self, familyName: str | None, style: FontStyle, bcp47: list[str], character: int
    ) -> Typeface:
        """
        Use the system fallback to find a typeface for the given character. ``bcp47Count`` is automatically set
        to the number of strings in *bcp47*.
        """

class FontParameters:
    class Variation:
        class Axis:
            @typing.overload
            def __init__(self) -> None: ...
            @typing.overload
            def __init__(self, arg0: int, arg1: float, arg2: float, arg3: float, arg4: bool) -> None: ...
            def __str__(self) -> str: ...
            def isHidden(self) -> bool: ...
            def setHidden(self, hidden: bool) -> None: ...
            @property
            def def_(self) -> float:
                """
                :type: float
                """
            @def_.setter
            def def_(self, arg0: float) -> None:
                pass
            @property
            def max(self) -> float:
                """
                :type: float
                """
            @max.setter
            def max(self, arg0: float) -> None:
                pass
            @property
            def min(self) -> float:
                """
                :type: float
                """
            @min.setter
            def min(self, arg0: float) -> None:
                pass
            @property
            def tag(self) -> int:
                """
                :type: int
                """
            @tag.setter
            def tag(self, arg0: int) -> None:
                pass
            pass
        pass
    pass

class FontStyle:
    class Slant:
        """
        Members:

          kUpright_Slant

          kItalic_Slant

          kOblique_Slant
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
        __members__: dict  # value = {'kUpright_Slant': <Slant.kUpright_Slant: 0>, 'kItalic_Slant': <Slant.kItalic_Slant: 1>, 'kOblique_Slant': <Slant.kOblique_Slant: 2>}
        kItalic_Slant: animator.skia.FontStyle.Slant  # value = <Slant.kItalic_Slant: 1>
        kOblique_Slant: animator.skia.FontStyle.Slant  # value = <Slant.kOblique_Slant: 2>
        kUpright_Slant: animator.skia.FontStyle.Slant  # value = <Slant.kUpright_Slant: 0>
        pass

    class Weight(IntEnum):
        """
        Members:

          kInvisible_Weight

          kThin_Weight

          kExtraLight_Weight

          kLight_Weight

          kNormal_Weight

          kMedium_Weight

          kSemiBold_Weight

          kBold_Weight

          kExtraBold_Weight

          kBlack_Weight

          kExtraBlack_Weight
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
        __members__: dict  # value = {'kInvisible_Weight': <Weight.kInvisible_Weight: 0>, 'kThin_Weight': <Weight.kThin_Weight: 100>, 'kExtraLight_Weight': <Weight.kExtraLight_Weight: 200>, 'kLight_Weight': <Weight.kLight_Weight: 300>, 'kNormal_Weight': <Weight.kNormal_Weight: 400>, 'kMedium_Weight': <Weight.kMedium_Weight: 500>, 'kSemiBold_Weight': <Weight.kSemiBold_Weight: 600>, 'kBold_Weight': <Weight.kBold_Weight: 700>, 'kExtraBold_Weight': <Weight.kExtraBold_Weight: 800>, 'kBlack_Weight': <Weight.kBlack_Weight: 900>, 'kExtraBlack_Weight': <Weight.kExtraBlack_Weight: 1000>}
        kBlack_Weight: animator.skia.FontStyle.Weight  # value = <Weight.kBlack_Weight: 900>
        kBold_Weight: animator.skia.FontStyle.Weight  # value = <Weight.kBold_Weight: 700>
        kExtraBlack_Weight: animator.skia.FontStyle.Weight  # value = <Weight.kExtraBlack_Weight: 1000>
        kExtraBold_Weight: animator.skia.FontStyle.Weight  # value = <Weight.kExtraBold_Weight: 800>
        kExtraLight_Weight: animator.skia.FontStyle.Weight  # value = <Weight.kExtraLight_Weight: 200>
        kInvisible_Weight: animator.skia.FontStyle.Weight  # value = <Weight.kInvisible_Weight: 0>
        kLight_Weight: animator.skia.FontStyle.Weight  # value = <Weight.kLight_Weight: 300>
        kMedium_Weight: animator.skia.FontStyle.Weight  # value = <Weight.kMedium_Weight: 500>
        kNormal_Weight: animator.skia.FontStyle.Weight  # value = <Weight.kNormal_Weight: 400>
        kSemiBold_Weight: animator.skia.FontStyle.Weight  # value = <Weight.kSemiBold_Weight: 600>
        kThin_Weight: animator.skia.FontStyle.Weight  # value = <Weight.kThin_Weight: 100>
        pass

    class Width(IntEnum):
        """
        Members:

          kUltraCondensed_Width

          kExtraCondensed_Width

          kCondensed_Width

          kSemiCondensed_Width

          kNormal_Width

          kSemiExpanded_Width

          kExpanded_Width

          kExtraExpanded_Width

          kUltraExpanded_Width
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
        __members__: dict  # value = {'kUltraCondensed_Width': <Width.kUltraCondensed_Width: 1>, 'kExtraCondensed_Width': <Width.kExtraCondensed_Width: 2>, 'kCondensed_Width': <Width.kCondensed_Width: 3>, 'kSemiCondensed_Width': <Width.kSemiCondensed_Width: 4>, 'kNormal_Width': <Width.kNormal_Width: 5>, 'kSemiExpanded_Width': <Width.kSemiExpanded_Width: 6>, 'kExpanded_Width': <Width.kExpanded_Width: 7>, 'kExtraExpanded_Width': <Width.kExtraExpanded_Width: 8>, 'kUltraExpanded_Width': <Width.kUltraExpanded_Width: 9>}
        kCondensed_Width: animator.skia.FontStyle.Width  # value = <Width.kCondensed_Width: 3>
        kExpanded_Width: animator.skia.FontStyle.Width  # value = <Width.kExpanded_Width: 7>
        kExtraCondensed_Width: animator.skia.FontStyle.Width  # value = <Width.kExtraCondensed_Width: 2>
        kExtraExpanded_Width: animator.skia.FontStyle.Width  # value = <Width.kExtraExpanded_Width: 8>
        kNormal_Width: animator.skia.FontStyle.Width  # value = <Width.kNormal_Width: 5>
        kSemiCondensed_Width: animator.skia.FontStyle.Width  # value = <Width.kSemiCondensed_Width: 4>
        kSemiExpanded_Width: animator.skia.FontStyle.Width  # value = <Width.kSemiExpanded_Width: 6>
        kUltraCondensed_Width: animator.skia.FontStyle.Width  # value = <Width.kUltraCondensed_Width: 1>
        kUltraExpanded_Width: animator.skia.FontStyle.Width  # value = <Width.kUltraExpanded_Width: 9>
        pass
    @staticmethod
    def Bold() -> FontStyle: ...
    @staticmethod
    def BoldItalic() -> FontStyle: ...
    @staticmethod
    def Italic() -> FontStyle: ...
    @staticmethod
    def Normal() -> FontStyle: ...
    def __eq__(self, arg0: FontStyle) -> bool: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(
        self,
        weight: FontStyle.Weight = Weight.kNormal_Weight,
        width: FontStyle.Width = Width.kNormal_Width,
        slant: FontStyle.Slant = Slant.kUpright_Slant,
    ) -> None: ...
    def __str__(self) -> str: ...
    def slant(self) -> FontStyle.Slant: ...
    def weight(self) -> int: ...
    def width(self) -> int: ...
    pass

class FontStyleSet:
    @staticmethod
    def CreateEmpty() -> FontStyleSet: ...
    def __getitem__(self, index: int) -> tuple:
        """
        Same as :py:meth:`getStyle`.
        """
    def __len__(self) -> int: ...
    def __str__(self) -> str: ...
    def count(self) -> int: ...
    def createTypeface(self, index: int) -> Typeface: ...
    def getStyle(self, index: int) -> tuple:
        """
        Return a tuple of (font style, style name) for the given *index*.
        """
    def matchStyle(self, pattern: FontStyle) -> Typeface: ...
    pass

class GradientShader:
    class Flags(IntEnum):
        """
        Members:

          kInterpolateColorsInPremul_Flag
        """

        def __and__(self, other: object) -> object: ...
        def __eq__(self, other: object) -> bool: ...
        def __ge__(self, other: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __gt__(self, other: object) -> bool: ...
        def __hash__(self) -> int: ...
        def __index__(self) -> int: ...
        def __init__(self, value: int) -> None: ...
        def __int__(self) -> int: ...
        def __invert__(self) -> object: ...
        def __le__(self, other: object) -> bool: ...
        def __lt__(self, other: object) -> bool: ...
        def __ne__(self, other: object) -> bool: ...
        def __or__(self, other: object) -> object: ...
        def __rand__(self, other: object) -> object: ...
        def __repr__(self) -> str: ...
        def __ror__(self, other: object) -> object: ...
        def __rxor__(self, other: object) -> object: ...
        def __setstate__(self, state: int) -> None: ...
        def __xor__(self, other: object) -> object: ...
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
        __members__: dict  # value = {'kInterpolateColorsInPremul_Flag': <Flags.kInterpolateColorsInPremul_Flag: 1>}
        kInterpolateColorsInPremul_Flag: animator.skia.GradientShader.Flags  # value = <Flags.kInterpolateColorsInPremul_Flag: 1>
        pass

    class Interpolation:
        class ColorSpace(IntEnum):
            """
            Members:

              kDestination

              kSRGBLinear

              kLab

              kOKLab

              kLCH

              kOKLCH

              kSRGB

              kHSL

              kHWB

              kLastColorSpace
            """

            def __eq__(self, other: object) -> bool: ...
            def __ge__(self, other: object) -> bool: ...
            def __getstate__(self) -> int: ...
            def __gt__(self, other: object) -> bool: ...
            def __hash__(self) -> int: ...
            def __index__(self) -> int: ...
            def __init__(self, value: int) -> None: ...
            def __int__(self) -> int: ...
            def __le__(self, other: object) -> bool: ...
            def __lt__(self, other: object) -> bool: ...
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
            __members__: dict  # value = {'kDestination': <ColorSpace.kDestination: 0>, 'kSRGBLinear': <ColorSpace.kSRGBLinear: 1>, 'kLab': <ColorSpace.kLab: 2>, 'kOKLab': <ColorSpace.kOKLab: 3>, 'kLCH': <ColorSpace.kLCH: 4>, 'kOKLCH': <ColorSpace.kOKLCH: 5>, 'kSRGB': <ColorSpace.kSRGB: 6>, 'kHSL': <ColorSpace.kHSL: 7>, 'kHWB': <ColorSpace.kHWB: 8>, 'kLastColorSpace': <ColorSpace.kHWB: 8>}
            kDestination: animator.skia.GradientShader.Interpolation.ColorSpace  # value = <ColorSpace.kDestination: 0>
            kHSL: animator.skia.GradientShader.Interpolation.ColorSpace  # value = <ColorSpace.kHSL: 7>
            kHWB: animator.skia.GradientShader.Interpolation.ColorSpace  # value = <ColorSpace.kHWB: 8>
            kLCH: animator.skia.GradientShader.Interpolation.ColorSpace  # value = <ColorSpace.kLCH: 4>
            kLab: animator.skia.GradientShader.Interpolation.ColorSpace  # value = <ColorSpace.kLab: 2>
            kLastColorSpace: animator.skia.GradientShader.Interpolation.ColorSpace  # value = <ColorSpace.kHWB: 8>
            kOKLCH: animator.skia.GradientShader.Interpolation.ColorSpace  # value = <ColorSpace.kOKLCH: 5>
            kOKLab: animator.skia.GradientShader.Interpolation.ColorSpace  # value = <ColorSpace.kOKLab: 3>
            kSRGB: animator.skia.GradientShader.Interpolation.ColorSpace  # value = <ColorSpace.kSRGB: 6>
            kSRGBLinear: animator.skia.GradientShader.Interpolation.ColorSpace  # value = <ColorSpace.kSRGBLinear: 1>
            pass

        class HueMethod(IntEnum):
            """
            Members:

              kShorter

              kLonger

              kIncreasing

              kDecreasing

              kLastHueMethod
            """

            def __eq__(self, other: object) -> bool: ...
            def __ge__(self, other: object) -> bool: ...
            def __getstate__(self) -> int: ...
            def __gt__(self, other: object) -> bool: ...
            def __hash__(self) -> int: ...
            def __index__(self) -> int: ...
            def __init__(self, value: int) -> None: ...
            def __int__(self) -> int: ...
            def __le__(self, other: object) -> bool: ...
            def __lt__(self, other: object) -> bool: ...
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
            __members__: dict  # value = {'kShorter': <HueMethod.kShorter: 0>, 'kLonger': <HueMethod.kLonger: 1>, 'kIncreasing': <HueMethod.kIncreasing: 2>, 'kDecreasing': <HueMethod.kDecreasing: 3>, 'kLastHueMethod': <HueMethod.kDecreasing: 3>}
            kDecreasing: animator.skia.GradientShader.Interpolation.HueMethod  # value = <HueMethod.kDecreasing: 3>
            kIncreasing: animator.skia.GradientShader.Interpolation.HueMethod  # value = <HueMethod.kIncreasing: 2>
            kLastHueMethod: animator.skia.GradientShader.Interpolation.HueMethod  # value = <HueMethod.kDecreasing: 3>
            kLonger: animator.skia.GradientShader.Interpolation.HueMethod  # value = <HueMethod.kLonger: 1>
            kShorter: animator.skia.GradientShader.Interpolation.HueMethod  # value = <HueMethod.kShorter: 0>
            pass

        class InPremul:
            """
            Members:

              kNo

              kYes
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
            __members__: dict  # value = {'kNo': <InPremul.kNo: 0>, 'kYes': <InPremul.kYes: 1>}
            kNo: animator.skia.GradientShader.Interpolation.InPremul  # value = <InPremul.kNo: 0>
            kYes: animator.skia.GradientShader.Interpolation.InPremul  # value = <InPremul.kYes: 1>
            pass
        @staticmethod
        def FromFlags(flags: int) -> GradientShader.Interpolation: ...
        @property
        def fColorSpace(self) -> GradientShader.Interpolation.ColorSpace:
            """
            :type: GradientShader.Interpolation.ColorSpace
            """
        @fColorSpace.setter
        def fColorSpace(self, arg0: GradientShader.Interpolation.ColorSpace) -> None:
            pass
        @property
        def fHueMethod(self) -> GradientShader.Interpolation.HueMethod:
            """
            :type: GradientShader.Interpolation.HueMethod
            """
        @fHueMethod.setter
        def fHueMethod(self, arg0: GradientShader.Interpolation.HueMethod) -> None:
            pass
        @property
        def fInPremul(self) -> GradientShader.Interpolation.InPremul:
            """
            :type: GradientShader.Interpolation.InPremul
            """
        @fInPremul.setter
        def fInPremul(self, arg0: GradientShader.Interpolation.InPremul) -> None:
            pass
        kColorSpaceCount = 9
        kHueMethodCount = 4
        pass
    @staticmethod
    @typing.overload
    def MakeLinear(
        pts: typing.Sequence[_Point],
        colors: typing.Sequence[_Color4f],
        colorSpace: ColorSpace | None = None,
        pos: list[float] | None = None,
        mode: TileMode = TileMode.kClamp,
        flags: int = 0,
        localMatrix: Matrix | None = None,
    ) -> Shader:
        """
        Returns a linear gradient shader between the two specified *pts* with the specified *colors*.
        """
    @staticmethod
    @typing.overload
    def MakeLinear(
        pts: typing.Sequence[_Point],
        colors: typing.Sequence[_Color4f],
        colorSpace: ColorSpace | None = None,
        pos: list[float] | None = None,
        mode: TileMode = TileMode.kClamp,
        interpolation: GradientShader.Interpolation = ...,
        localMatrix: Matrix | None = None,
    ) -> Shader:
        """
        Returns a linear gradient shader between the two specified *pts* with the specified *colors*.
        """
    @staticmethod
    @typing.overload
    def MakeLinear(
        pts: typing.Sequence[_Point],
        colors: typing.Sequence[_Color],
        pos: list[float] | None = None,
        mode: TileMode = TileMode.kClamp,
        flags: int = 0,
        localMatrix: Matrix | None = None,
    ) -> Shader:
        """
        Returns a linear gradient shader between the two specified *pts* with the specified *colors*.
        """
    @staticmethod
    @typing.overload
    def MakeRadial(
        center: _Point,
        radius: float,
        colors: typing.Sequence[_Color4f],
        colorSpace: ColorSpace | None = None,
        pos: list[float] | None = None,
        mode: TileMode = TileMode.kClamp,
        flags: int = 0,
        localMatrix: Matrix | None = None,
    ) -> Shader:
        """
        Returns a radial gradient shader with the specified *center*, *radius* and *colors*.
        """
    @staticmethod
    @typing.overload
    def MakeRadial(
        center: _Point,
        radius: float,
        colors: typing.Sequence[_Color4f],
        colorSpace: ColorSpace | None = None,
        pos: list[float] | None = None,
        mode: TileMode = TileMode.kClamp,
        interpolation: GradientShader.Interpolation = ...,
        localMatrix: Matrix | None = None,
    ) -> Shader:
        """
        Returns a radial gradient shader with the specified *center*, *radius* and *colors*.
        """
    @staticmethod
    @typing.overload
    def MakeRadial(
        center: _Point,
        radius: float,
        colors: typing.Sequence[_Color],
        pos: list[float] | None = None,
        mode: TileMode = TileMode.kClamp,
        flags: int = 0,
        localMatrix: Matrix | None = None,
    ) -> Shader:
        """
        Returns a radial gradient shader with the specified *center*, *radius* and *colors*.
        """
    @staticmethod
    @typing.overload
    def MakeSweep(
        cx: float,
        cy: float,
        colors: typing.Sequence[_Color4f],
        colorSpace: ColorSpace | None = None,
        pos: list[float] | None = None,
        mode: TileMode = TileMode.kClamp,
        startAngle: float = 0,
        endAngle: float = 360,
        flags: int = 0,
        localMatrix: Matrix | None = None,
    ) -> Shader:
        """
        Returns a sweep gradient shader with the specified center (*cx*, *cy*) and *colors*.
        """
    @staticmethod
    @typing.overload
    def MakeSweep(
        cx: float,
        cy: float,
        colors: typing.Sequence[_Color4f],
        colorSpace: ColorSpace | None = None,
        pos: list[float] | None = None,
        mode: TileMode = TileMode.kClamp,
        startAngle: float = 0,
        endAngle: float = 360,
        interpolation: GradientShader.Interpolation = ...,
        localMatrix: Matrix | None = None,
    ) -> Shader:
        """
        Returns a sweep gradient shader with the specified center (*cx*, *cy*) and *colors*.
        """
    @staticmethod
    @typing.overload
    def MakeSweep(
        cx: float,
        cy: float,
        colors: typing.Sequence[_Color],
        pos: list[float] | None = None,
        mode: TileMode = TileMode.kClamp,
        startAngle: float = 0,
        endAngle: float = 360,
        flags: int = 0,
        localMatrix: Matrix | None = None,
    ) -> Shader:
        """
        Returns a sweep gradient shader with the specified center (*cx*, *cy*) and *colors*.
        """
    @staticmethod
    @typing.overload
    def MakeTwoPointConical(
        start: _Point,
        startRadius: float,
        end: _Point,
        endRadius: float,
        colors: typing.Sequence[_Color4f],
        colorSpace: ColorSpace | None = None,
        pos: list[float] | None = None,
        mode: TileMode = TileMode.kClamp,
        flags: int = 0,
        localMatrix: Matrix | None = None,
    ) -> Shader:
        """
        Returns a conical gradient shader with the specified *start* and *end* points, the *startRadius* and
        *endRadius*, and the *colors*.
        """
    @staticmethod
    @typing.overload
    def MakeTwoPointConical(
        start: _Point,
        startRadius: float,
        end: _Point,
        endRadius: float,
        colors: typing.Sequence[_Color4f],
        colorSpace: ColorSpace | None = None,
        pos: list[float] | None = None,
        mode: TileMode = TileMode.kClamp,
        interpolation: GradientShader.Interpolation = ...,
        localMatrix: Matrix | None = None,
    ) -> Shader:
        """
        Returns a conical gradient shader with the specified *start* and *end* points, the *startRadius* and
        *endRadius*, and the *colors*.
        """
    @staticmethod
    @typing.overload
    def MakeTwoPointConical(
        start: _Point,
        startRadius: float,
        end: _Point,
        endRadius: float,
        colors: typing.Sequence[_Color],
        pos: list[float] | None = None,
        mode: TileMode = TileMode.kClamp,
        flags: int = 0,
        localMatrix: Matrix | None = None,
    ) -> Shader:
        """
        Returns a conical gradient shader with the specified *start* and *end* points, the *startRadius* and
        *endRadius*, and the *colors*.
        """

class HighContrastConfig:
    class InvertStyle:
        """
        Members:

          kNoInvert

          kInvertBrightness

          kInvertLightness

          kLast
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
        __members__: dict  # value = {'kNoInvert': <InvertStyle.kNoInvert: 0>, 'kInvertBrightness': <InvertStyle.kInvertBrightness: 1>, 'kInvertLightness': <InvertStyle.kInvertLightness: 2>, 'kLast': <InvertStyle.kInvertLightness: 2>}
        kInvertBrightness: animator.skia.HighContrastConfig.InvertStyle  # value = <InvertStyle.kInvertBrightness: 1>
        kInvertLightness: animator.skia.HighContrastConfig.InvertStyle  # value = <InvertStyle.kInvertLightness: 2>
        kLast: animator.skia.HighContrastConfig.InvertStyle  # value = <InvertStyle.kInvertLightness: 2>
        kNoInvert: animator.skia.HighContrastConfig.InvertStyle  # value = <InvertStyle.kNoInvert: 0>
        pass
    def __init__(
        self,
        grayscale: bool = False,
        invertStyle: HighContrastConfig.InvertStyle = InvertStyle.kNoInvert,
        contrast: float = 0,
    ) -> None: ...
    def isValid(self) -> bool: ...
    @property
    def fContrast(self) -> float:
        """
        :type: float
        """
    @fContrast.setter
    def fContrast(self, arg0: float) -> None:
        pass
    @property
    def fGrayscale(self) -> bool:
        """
        :type: bool
        """
    @fGrayscale.setter
    def fGrayscale(self, arg0: bool) -> None:
        pass
    @property
    def fInvertStyle(self) -> HighContrastConfig.InvertStyle:
        """
        :type: HighContrastConfig.InvertStyle
        """
    @fInvertStyle.setter
    def fInvertStyle(self, arg0: HighContrastConfig.InvertStyle) -> None:
        pass
    pass

class HighContrastFilter:
    @staticmethod
    def Make(config: HighContrastConfig) -> ColorFilter: ...
    pass

class IPoint:
    @staticmethod
    def Make(x: int, y: int) -> IPoint: ...
    def __add__(self, other: IPoint) -> IPoint: ...
    def __eq__(self, other: IPoint) -> bool: ...
    def __iadd__(self, other: IPoint) -> None: ...
    @typing.overload
    def __init__(self, t: tuple) -> None:
        """
        Create an :py:class:`IPoint` from a tuple of two integers.

        :param t: Tuple of two integers.
        """
    @typing.overload
    def __init__(self, x: int, y: int) -> None: ...
    def __isub__(self, other: IPoint) -> None: ...
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    def __ne__(self, other: IPoint) -> bool: ...
    def __neg__(self) -> IPoint: ...
    def __str__(self) -> str: ...
    def __sub__(self, other: IPoint) -> IPoint: ...
    def equals(self, x: int, y: int) -> bool: ...
    def isZero(self) -> bool: ...
    def set(self, x: int, y: int) -> None: ...
    def x(self) -> int: ...
    def y(self) -> int: ...
    @property
    def fX(self) -> int:
        """
        :type: int
        """
    @fX.setter
    def fX(self, arg0: int) -> None:
        pass
    @property
    def fY(self) -> int:
        """
        :type: int
        """
    @fY.setter
    def fY(self, arg0: int) -> None:
        pass
    pass

class IRect:
    @staticmethod
    def Intersects(a: _IRect, b: _IRect) -> bool: ...
    @staticmethod
    def MakeEmpty() -> IRect: ...
    @staticmethod
    def MakeLTRB(l: int, t: int, r: int, b: int) -> IRect: ...
    @staticmethod
    def MakePtSize(pt: IPoint, size: _ISize) -> IRect: ...
    @staticmethod
    def MakeSize(size: _ISize) -> IRect: ...
    @staticmethod
    def MakeWH(w: int, h: int) -> IRect: ...
    @staticmethod
    def MakeXYWH(x: int, y: int, w: int, h: int) -> IRect: ...
    @typing.overload
    def __contains__(self, arg0: IPoint) -> bool:
        """
        Returns true if the point is contained within the :py:class:`IRect`.

        :param IPoint point: point to test
        :return: true if the point is contained within the :py:class:`IRect`
        """
    @typing.overload
    def __contains__(self, arg0: _IRect) -> bool: ...
    @typing.overload
    def __contains__(self, arg0: _Rect) -> bool: ...
    def __eq__(self, other: _IRect) -> bool: ...
    @typing.overload
    def __init__(self) -> None:
        """
        Constructs an :py:class:`IRect` set to (0, 0, 0, 0). Many other rectangles are empty; if left is equal
        to or greater than right, or if top is equal to or greater than bottom. Setting all members to zero is
        a convenience, but does not designate a special empty rectangle.
        """
    @typing.overload
    def __init__(self, l: int, t: int, r: int, b: int) -> None:
        """
        Constructs an :py:class:`IRect` set to (l, t, r, b). Does not sort input; :py:class:`IRect` may result
        in fLeft greater than fRight, or fTop greater than fBottom.

        :param int l: value for :py:class:`IRect` fLeft
        :param int t: value for :py:class:`IRect` fTop
        :param int r: value for :py:class:`IRect` fRight
        :param int b: value for :py:class:`IRect` fBottom
        """
    @typing.overload
    def __init__(self, pt: IPoint, size: _ISize) -> None:
        """
        Constructs an :py:class:`IRect` set to (pt.x(), pt.y(), pt.x() + size.width(), pt.y() + size.height()).
        Does not validate input; size.width() or size.height() may be negative.

        :param IPoint pt: values for :py:class:`IRect` fLeft and fTop
        :param ISize size: values for :py:class:`IRect` width and height
        """
    @typing.overload
    def __init__(self, size: _ISize) -> None:
        """
        Constructs an :py:class:`IRect` set to (0, 0, size.width(), size.height()). Does not validate input;
        size.width() or size.height() may be negative.

        :param ISize size: values for :py:class:`IRect` width and height
        """
    @typing.overload
    def __init__(self, t: tuple) -> None:
        """
        Create an :py:class:`IRect` from a tuple of 0, 2, or 4 integers.
        """
    @typing.overload
    def __init__(self, w: int, h: int) -> None:
        """
        Constructs an :py:class:`IRect` set to (0, 0, w, h). Does not validate input; w or h may be negative.

        :param int w: width of constructed :py:class:`IRect`
        :param int h: height of constructed :py:class:`IRect`
        """
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    def __ne__(self, other: _IRect) -> bool: ...
    def __str__(self) -> str: ...
    def adjust(self, dL: int, dT: int, dR: int, dB: int) -> None: ...
    def bottom(self) -> int: ...
    @typing.overload
    def contains(self, r: _IRect) -> bool: ...
    @typing.overload
    def contains(self, r: _Rect) -> bool: ...
    @typing.overload
    def contains(self, x: int, y: int) -> bool: ...
    def containsNoEmptyCheck(self, r: _IRect) -> bool: ...
    def height(self) -> int: ...
    def height64(self) -> int: ...
    def inset(self, dx: int, dy: int) -> None: ...
    @typing.overload
    def intersect(self, a: _IRect, b: _IRect) -> bool: ...
    @typing.overload
    def intersect(self, r: _IRect) -> bool: ...
    def isEmpty(self) -> bool: ...
    def isEmpty64(self) -> bool: ...
    def join(self, r: _IRect) -> None: ...
    def left(self) -> int: ...
    def makeInset(self, dx: int, dy: int) -> IRect: ...
    @typing.overload
    def makeOffset(self, dx: int, dy: int) -> IRect: ...
    @typing.overload
    def makeOffset(self, offset: IPoint) -> IRect: ...
    def makeOutset(self, dx: int, dy: int) -> IRect: ...
    def makeSorted(self) -> IRect: ...
    @typing.overload
    def offset(self, delta: IPoint) -> None: ...
    @typing.overload
    def offset(self, dx: int, dy: int) -> None: ...
    def offsetTo(self, newX: int, newY: int) -> None: ...
    def outset(self, dx: int, dy: int) -> None: ...
    def right(self) -> int: ...
    def setEmpty(self) -> None: ...
    def setLTRB(self, left: int, top: int, right: int, bottom: int) -> None: ...
    def setSize(self, size: _ISize) -> None: ...
    def setWH(self, width: int, height: int) -> None: ...
    def setXYWH(self, x: int, y: int, width: int, height: int) -> None: ...
    def size(self) -> ISize: ...
    def sort(self) -> None: ...
    def top(self) -> int: ...
    def topLeft(self) -> IPoint: ...
    def width(self) -> int: ...
    def width64(self) -> int: ...
    def x(self) -> int: ...
    def y(self) -> int: ...
    @property
    def fBottom(self) -> int:
        """
        :type: int
        """
    @fBottom.setter
    def fBottom(self, arg0: int) -> None:
        pass
    @property
    def fLeft(self) -> int:
        """
        :type: int
        """
    @fLeft.setter
    def fLeft(self, arg0: int) -> None:
        pass
    @property
    def fRight(self) -> int:
        """
        :type: int
        """
    @fRight.setter
    def fRight(self, arg0: int) -> None:
        pass
    @property
    def fTop(self) -> int:
        """
        :type: int
        """
    @fTop.setter
    def fTop(self, arg0: int) -> None:
        pass
    pass

_IRect = IRect | tuple[()] | tuple[int, int] | tuple[int, int, int, int]

class ISize:
    @staticmethod
    def Make(w: int, h: int) -> ISize: ...
    @staticmethod
    def MakeEmpty() -> ISize: ...
    def __eq__(self, other: _ISize) -> bool: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, t: tuple) -> None:
        """
        Create an :py:class:`ISize` from a tuple of two integers.

        :param t: Tuple of two integers.
        """
    @typing.overload
    def __init__(self, w: int, h: int) -> None: ...
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    def __ne__(self, other: _ISize) -> bool: ...
    def __str__(self) -> str: ...
    def area(self) -> int: ...
    def equals(self, w: int, h: int) -> bool: ...
    def height(self) -> int: ...
    def isEmpty(self) -> bool: ...
    def isZero(self) -> bool: ...
    def set(self, w: int, h: int) -> None: ...
    def setEmpty(self) -> None: ...
    def width(self) -> int: ...
    @property
    def fHeight(self) -> int:
        """
        :type: int
        """
    @fHeight.setter
    def fHeight(self, arg0: int) -> None:
        pass
    @property
    def fWidth(self) -> int:
        """
        :type: int
        """
    @fWidth.setter
    def fWidth(self, arg0: int) -> None:
        pass
    pass

_ISize = ISize | tuple[int, int]

class Image:
    """
    :py:class:`Image` describes a two dimensional array of pixels to draw.

    A few high-level methods in addition to C++ API::

        image = skia.Image.open('/path/to/image.png')
        image = image.resize(120, 120)
        image = image.convert(alphaType=skia.kUnpremul_AlphaType)
        image.save('/path/to/output.jpg', skia.kJPEG)

    NumPy arrays can be directly imported or exported::

        image = skia.Image.fromarray(array)
        array = image.toarray()

    General pixel buffers can be exchanged in the following approach::

        image = skia.Image.frombytes(pixels, (100, 100))
        pixels = image.tobytes()
    """

    class BitDepth:
        """
        Members:

          kU8

          kF16
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
        __members__: dict  # value = {'kU8': <BitDepth.kU8: 0>, 'kF16': <BitDepth.kF16: 1>}
        kF16: animator.skia.Image.BitDepth  # value = <BitDepth.kF16: 1>
        kU8: animator.skia.Image.BitDepth  # value = <BitDepth.kU8: 0>
        pass

    class CachingHint:
        """
        Members:

          kAllow_CachingHint

          kDisallow_CachingHint
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
        __members__: dict  # value = {'kAllow_CachingHint': <CachingHint.kAllow_CachingHint: 0>, 'kDisallow_CachingHint': <CachingHint.kDisallow_CachingHint: 1>}
        kAllow_CachingHint: animator.skia.Image.CachingHint  # value = <CachingHint.kAllow_CachingHint: 0>
        kDisallow_CachingHint: animator.skia.Image.CachingHint  # value = <CachingHint.kDisallow_CachingHint: 1>
        pass

    class TextureCompressionType:
        """
        Members:

          kNone

          kETC2_RGB8_UNORM

          kBC1_RGB8_UNORM

          kBC1_RGBA8_UNORM

          kLast

          kETC1_RGB8
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
        __members__: dict  # value = {'kNone': <TextureCompressionType.kNone: 0>, 'kETC2_RGB8_UNORM': <TextureCompressionType.kETC2_RGB8_UNORM: 1>, 'kBC1_RGB8_UNORM': <TextureCompressionType.kBC1_RGB8_UNORM: 2>, 'kBC1_RGBA8_UNORM': <TextureCompressionType.kBC1_RGBA8_UNORM: 3>, 'kLast': <TextureCompressionType.kBC1_RGBA8_UNORM: 3>, 'kETC1_RGB8': <TextureCompressionType.kETC2_RGB8_UNORM: 1>}
        kBC1_RGB8_UNORM: animator.skia.Image.TextureCompressionType  # value = <TextureCompressionType.kBC1_RGB8_UNORM: 2>
        kBC1_RGBA8_UNORM: animator.skia.Image.TextureCompressionType  # value = <TextureCompressionType.kBC1_RGBA8_UNORM: 3>
        kETC1_RGB8: animator.skia.Image.TextureCompressionType  # value = <TextureCompressionType.kETC2_RGB8_UNORM: 1>
        kETC2_RGB8_UNORM: animator.skia.Image.TextureCompressionType  # value = <TextureCompressionType.kETC2_RGB8_UNORM: 1>
        kLast: animator.skia.Image.TextureCompressionType  # value = <TextureCompressionType.kBC1_RGBA8_UNORM: 3>
        kNone: animator.skia.Image.TextureCompressionType  # value = <TextureCompressionType.kNone: 0>
        pass
    @staticmethod
    def DeferredFromEncodedData(encoded: Data, alphaType: AlphaType | None = None) -> Image: ...
    @staticmethod
    def DeferredFromPicture(
        picture: Picture,
        dimensions: _ISize,
        matrix: Matrix | None = None,
        paint: Paint | None = None,
        bitDepth: Image.BitDepth = BitDepth.kU8,
        colorSpace: ColorSpace | None = None,
        props: SurfaceProps = ...,
    ) -> Image: ...
    @staticmethod
    def RasterFromBitmap(bitmap: Bitmap) -> Image: ...
    @staticmethod
    def RasterFromCompressedTextureData(
        data: Data, width: int, height: int, type: Image.TextureCompressionType
    ) -> Image: ...
    @staticmethod
    def RasterFromData(info: ImageInfo, pixels: Data, rowBytes: int) -> Image: ...
    @staticmethod
    def RasterFromPixmap(pixmap: Pixmap) -> Image:
        """
        Creates :py:class:`Image` from *pixmap*, sharing :py:class:`Pixmap` pixels.
        """
    @staticmethod
    def RasterFromPixmapCopy(pixmap: Pixmap) -> Image: ...
    def __str__(self) -> str: ...
    def _repr_png_(self) -> bytes: ...
    def alphaType(self) -> AlphaType: ...
    def bitmap(
        self,
        colorType: ColorType = ColorType.kUnknown_ColorType,
        alphaType: AlphaType = AlphaType.kUnknown_AlphaType,
        colorSpace: ColorSpace | None = None,
    ) -> Bitmap:
        """
        Creates a new :py:class:`Bitmap` from :py:class:`Image` with a copy of pixels.
        """
    def bounds(self) -> IRect: ...
    def colorSpace(self) -> ColorSpace: ...
    def colorType(self) -> ColorType: ...
    def dimensions(self) -> ISize: ...
    def encodeToData(
        self, encodedImageFormat: EncodedImageFormat = EncodedImageFormat.kPNG, quality: int = 100
    ) -> Data: ...
    @staticmethod
    def fromarray(
        array: numpy.ndarray,
        ct: ColorType = ColorType.kRGBA_8888_ColorType,
        at: AlphaType = AlphaType.kUnpremul_AlphaType,
        cs: ColorSpace | None = None,
        copy: bool = True,
    ) -> Image:
        """
        Creates a new :py:class:`Image` from numpy array.

        :param array: A numpy array of shape ``(height, width, channels)`` and appropriate dtype.
        :param ct: The color type of the image.
        :param at: The alpha type of the image.
        :param cs: The color space of the image.
        :param copy: Whether to copy the data from the array.
        :return: A new :py:class:`Image` sharing the data in the array if copy is ``False``, or a new
            :py:class:`Image` with a copy of the data if copy is ``True``.
        """
    @staticmethod
    def frombytes(
        buffer: buffer,
        dimensions: _ISize,
        ct: ColorType = ColorType.kRGBA_8888_ColorType,
        at: AlphaType = AlphaType.kUnpremul_AlphaType,
        cs: ColorSpace | None = None,
        copy: bool = True,
    ) -> Image:
        """
        Creates a new :py:class:`Image` from bytes.

        :param buffer: A Python buffer object.
        :param dimensions: The dimensions of the image.
        :param ct: The color type of the image.
        :param at: The alpha type of the image.
        :param cs: The color space of the image.
        :param copy: Whether to copy the data from the buffer.
        :return: A new :py:class:`Image` sharing the data in the buffer if copy is ``False``, or a new
            :py:class:`Image` with a copy of the data if copy is ``True``.
        """
    def hasMipmaps(self) -> bool: ...
    def height(self) -> int: ...
    def imageInfo(self) -> ImageInfo: ...
    def isAlphaOnly(self) -> bool: ...
    def isLazyGenerated(self) -> bool: ...
    def isOpaque(self) -> bool: ...
    def isValid(self) -> bool:
        """
        Returns ``True`` if :py:class:`Image` can be drawn on raster surface.
        """
    def makeColorSpace(self, target: ColorSpace) -> Image:
        """
        Creates :py:class:`Image` in *target* colorspace.
        """
    def makeColorTypeAndColorSpace(self, targetColorType: ColorType, targetColorSpace: ColorSpace) -> Image:
        """
        Creates :py:class:`Image` in *targetColorType* and *targetColorSpace*.
        """
    def makeNonTextureImage(self) -> Image: ...
    def makeRasterImage(self, cachingHint: Image.CachingHint = CachingHint.kDisallow_CachingHint) -> Image: ...
    def makeRawShader(
        self,
        tmx: TileMode = TileMode.kClamp,
        tmy: TileMode = TileMode.kClamp,
        sampling: SamplingOptions = ...,
        localMatrix: Matrix | None = None,
    ) -> Shader: ...
    def makeShader(
        self,
        tmx: TileMode = TileMode.kClamp,
        tmy: TileMode = TileMode.kClamp,
        sampling: SamplingOptions = ...,
        localMatrix: Matrix | None = None,
    ) -> Shader: ...
    def makeSubset(self, subset: _IRect) -> Image:
        """
        Returns subset of :py:class:`Image` with *subset* bounds.
        """
    def makeWithFilter(
        self, filter: ImageFilter, subset: _IRect | None = None, clipBounds: _IRect | None = None
    ) -> tuple:
        """
        Creates filtered :py:class:`Image` and returns ``(filteredImage, outSubset, offset)``.
        """
    @staticmethod
    def open(fp: object) -> Image:
        """
        Opens an image from a file like object or a path.
        """
    def peekPixels(self) -> Pixmap:
        """
        Returns a :py:class:`Pixmap` describing the pixel data.
        """
    @typing.overload
    def readPixels(
        self, dst: Pixmap, srcX: int = 0, srcY: int = 0, cachingHint: Image.CachingHint = CachingHint.kAllow_CachingHint
    ) -> bool:
        """
        Copies pixels starting from (*srcX*, *srcY*) to *dst* :py:class:`Pixmap`.
        """
    @typing.overload
    def readPixels(
        self,
        dstInfo: ImageInfo,
        dstPixels: buffer,
        dstRowBytes: int = 0,
        srcX: int = 0,
        srcY: int = 0,
        cachingHint: Image.CachingHint = CachingHint.kAllow_CachingHint,
    ) -> bool:
        """
        Copies *dstInfo* pixels starting from (*srcX*, *srcY*) to *dstPixels* buffer.
        """
    def refColorSpace(self) -> ColorSpace: ...
    def refEncodedData(self) -> Data: ...
    def reinterpretColorSpace(self, newColorSpace: ColorSpace) -> Image: ...
    def resize(
        self,
        width: int,
        height: int,
        sampling: SamplingOptions = ...,
        cachingHint: Image.CachingHint = CachingHint.kAllow_CachingHint,
    ) -> Image:
        """
        Creates a new :py:class:`Image` by scaling pixels to fit *width* and *height*.
        """
    def save(
        self, fp: object, encodedImageFormat: EncodedImageFormat = EncodedImageFormat.kPNG, quality: int = 100
    ) -> None:
        """
        Saves the image to a file like object or a path.

        :param fp: A file like object or a path.
        :param format: The format of the image. Should be one of :py:attr:`EncodedImageFormat.kJPEG`,
            :py:attr:`EncodedImageFormat.kPNG`, :py:attr:`EncodedImageFormat.kWEBP`.
        :param quality: The quality of the image. 100 is the best quality.
        """
    def scalePixels(
        self,
        dst: Pixmap,
        sampling: SamplingOptions = ...,
        cachingHint: Image.CachingHint = CachingHint.kAllow_CachingHint,
    ) -> bool: ...
    def toarray(
        self,
        srcX: int = 0,
        srcY: int = 0,
        ct: ColorType = ColorType.kRGBA_8888_ColorType,
        at: AlphaType = AlphaType.kUnpremul_AlphaType,
        cs: ColorSpace | None = None,
    ) -> numpy.ndarray:
        """
        Returns a ``ndarray`` of the image's pixels.
        """
    def tobytes(self) -> bytes:
        """
        Returns python ``bytes`` object from internal pixels.
        """
    def uniqueID(self) -> int: ...
    def width(self) -> int: ...
    def withDefaultMipmaps(self) -> Image: ...
    pass

class ImageFilter(Flattenable):
    class MapDirection:
        """
        Members:

          kForward_MapDirection

          kReverse_MapDirection
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
        __members__: dict  # value = {'kForward_MapDirection': <MapDirection.kForward_MapDirection: 0>, 'kReverse_MapDirection': <MapDirection.kReverse_MapDirection: 1>}
        kForward_MapDirection: animator.skia.ImageFilter.MapDirection  # value = <MapDirection.kForward_MapDirection: 0>
        kReverse_MapDirection: animator.skia.ImageFilter.MapDirection  # value = <MapDirection.kReverse_MapDirection: 1>
        pass
    @staticmethod
    def Deserialize(data: buffer) -> ImageFilter: ...
    def asAColorFilter(self) -> ColorFilter | None: ...
    def canComputeFastBounds(self) -> bool: ...
    def computeFastBounds(self, bounds: _Rect) -> Rect: ...
    def countInputs(self) -> int: ...
    def filterBounds(
        self, src: _IRect, ctm: Matrix, direction: ImageFilter.MapDirection, inputRect: _IRect | None = None
    ) -> IRect: ...
    def getInput(self, i: int) -> ImageFilter: ...
    def isColorFilterNode(self) -> ColorFilter | None: ...
    def makeWithLocalMatrix(self, matrix: Matrix) -> ImageFilter: ...
    pass

class ImageFilters:
    class CropRect:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, crop: _IRect) -> None: ...
        @typing.overload
        def __init__(self, crop: None) -> None: ...
        @typing.overload
        def __init__(self, crop: _Rect) -> None: ...
        def __str__(self) -> str: ...
        @property
        def fCropRect(self) -> Rect:
            """
            :type: _Rect
            """
        @fCropRect.setter
        def fCropRect(self, arg0: _Rect) -> None:
            pass
        pass

    class Dither:
        """
        Members:

          kNo

          kYes
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
        __members__: dict  # value = {'kNo': <Dither.kNo: 0>, 'kYes': <Dither.kYes: 1>}
        kNo: animator.skia.ImageFilters.Dither  # value = <Dither.kNo: 0>
        kYes: animator.skia.ImageFilters.Dither  # value = <Dither.kYes: 1>
        pass
    @staticmethod
    def Arithmetic(
        k1: float,
        k2: float,
        k3: float,
        k4: float,
        enforcePMColor: bool = False,
        background: ImageFilter | None = None,
        foreground: ImageFilter | None = None,
        cropRect: ImageFilters.CropRect = ...,
    ) -> ImageFilter: ...
    @staticmethod
    @typing.overload
    def Blend(
        blender: Blender,
        background: ImageFilter,
        foreground: ImageFilter | None = None,
        cropRect: ImageFilters.CropRect = ...,
    ) -> ImageFilter: ...
    @staticmethod
    @typing.overload
    def Blend(
        mode: BlendMode,
        background: ImageFilter,
        foreground: ImageFilter | None = None,
        cropRect: ImageFilters.CropRect = ...,
    ) -> ImageFilter: ...
    @staticmethod
    def Blur(
        sigmaX: float,
        sigmaY: float,
        tileMode: TileMode = TileMode.kDecal,
        input: ImageFilter | None = None,
        cropRect: ImageFilters.CropRect = ...,
    ) -> ImageFilter: ...
    @staticmethod
    def ColorFilter(
        cf: ColorFilter, input: ImageFilter | None = None, cropRect: ImageFilters.CropRect = ...
    ) -> ImageFilter: ...
    @staticmethod
    def Compose(outer: ImageFilter, inner: ImageFilter) -> ImageFilter: ...
    @staticmethod
    def Dilate(
        radiusX: float, radiusY: float, input: ImageFilter | None = None, cropRect: ImageFilters.CropRect = ...
    ) -> ImageFilter: ...
    @staticmethod
    def DisplacementMap(
        xChannelSelector: ColorChannel,
        yChannelSelector: ColorChannel,
        scale: float,
        displacement: ImageFilter,
        color: ImageFilter | None = None,
        cropRect: ImageFilters.CropRect = ...,
    ) -> ImageFilter: ...
    @staticmethod
    def DistantLitDiffuse(
        direction: _Point3,
        lightColor: _Color,
        surfaceScale: float,
        kd: float,
        input: ImageFilter | None = None,
        cropRect: ImageFilters.CropRect = ...,
    ) -> ImageFilter: ...
    @staticmethod
    def DistantLitSpecular(
        direction: _Point3,
        lightColor: _Color,
        surfaceScale: float,
        ks: float,
        shininess: float,
        input: ImageFilter | None = None,
        cropRect: ImageFilters.CropRect = ...,
    ) -> ImageFilter: ...
    @staticmethod
    def DropShadow(
        dx: float,
        dy: float,
        sigmaX: float,
        sigmaY: float,
        color: _Color,
        input: ImageFilter | None = None,
        cropRect: ImageFilters.CropRect = ...,
    ) -> ImageFilter: ...
    @staticmethod
    def DropShadowOnly(
        dx: float,
        dy: float,
        sigmaX: float,
        sigmaY: float,
        color: _Color,
        input: ImageFilter | None = None,
        cropRect: ImageFilters.CropRect = ...,
    ) -> ImageFilter: ...
    @staticmethod
    def Erode(
        radiusX: float, radiusY: float, input: ImageFilter | None = None, cropRect: ImageFilters.CropRect = ...
    ) -> ImageFilter: ...
    @staticmethod
    def Image(
        image: Image,
        srcRect: _Rect | None = None,
        dstRect: _Rect | None | None = None,
        sampling: SamplingOptions = ...,
    ) -> ImageFilter: ...
    @staticmethod
    def Magnifier(
        lensBounds: _Rect,
        zoomAmount: float,
        inset: float,
        sampling: SamplingOptions = ...,
        input: ImageFilter | None = None,
        cropRect: ImageFilters.CropRect = ...,
    ) -> ImageFilter: ...
    @staticmethod
    def MatrixConvolution(
        kernelSize: _ISize,
        kernel: list[float],
        gain: float = 1,
        bias: float = 0,
        kernelOffset: IPoint | None = None,
        tileMode: TileMode = TileMode.kClamp,
        convolveAlpha: bool = False,
        input: ImageFilter | None = None,
        cropRect: ImageFilters.CropRect = ...,
    ) -> ImageFilter:
        """
        If *kernelOffset* is not specified, it is assumed to be half the kernel width and height.
        """
    @staticmethod
    def MatrixTransform(
        matrix: Matrix, sampling: SamplingOptions = ..., input: ImageFilter | None = None
    ) -> ImageFilter: ...
    @staticmethod
    @typing.overload
    def Merge(filters: list, cropRect: ImageFilters.CropRect = ...) -> ImageFilter:
        """
        Create a filter that merges the *filters* together by drawing their results in order with src-over
        blending. If any of the filters is ``None``, the source bitmap is used.
        """
    @staticmethod
    @typing.overload
    def Merge(first: ImageFilter, second: ImageFilter, cropRect: ImageFilters.CropRect = ...) -> ImageFilter: ...
    @staticmethod
    def Offset(
        dx: float, dy: float, input: ImageFilter | None = None, cropRect: ImageFilters.CropRect = ...
    ) -> ImageFilter: ...
    @staticmethod
    @typing.overload
    def Picture(pic: Picture) -> ImageFilter: ...
    @staticmethod
    @typing.overload
    def Picture(pic: Picture, targetRect: _Rect) -> ImageFilter: ...
    @staticmethod
    def PointLitDiffuse(
        location: _Point3,
        lightColor: _Color,
        surfaceScale: float,
        kd: float,
        input: ImageFilter | None = None,
        cropRect: ImageFilters.CropRect = ...,
    ) -> ImageFilter: ...
    @staticmethod
    def PointLitSpecular(
        location: _Point3,
        lightColor: _Color,
        surfaceScale: float,
        ks: float,
        shininess: float,
        input: ImageFilter | None = None,
        cropRect: ImageFilters.CropRect = ...,
    ) -> ImageFilter: ...
    @staticmethod
    @typing.overload
    def RuntimeShader(
        builder: RuntimeShaderBuilder,
        childShaderNames: list[str],
        inputs: list[ImageFilter],
        maxSampleRadius: float = 0,
    ) -> ImageFilter: ...
    @staticmethod
    @typing.overload
    def RuntimeShader(
        builder: RuntimeShaderBuilder,
        sampleRadius: float = 0,
        childShaderName: str = '',
        input: ImageFilter | None = None,
    ) -> ImageFilter: ...
    @staticmethod
    def Shader(
        shader: Shader, dither: ImageFilters.Dither = Dither.kNo, cropRect: ImageFilters.CropRect = ...
    ) -> ImageFilter: ...
    @staticmethod
    def SpotLitDiffuse(
        location: _Point3,
        target: _Point3,
        falloffExponent: float,
        cutoffAngle: float,
        lightColor: _Color,
        surfaceScale: float,
        kd: float,
        input: ImageFilter | None = None,
        cropRect: ImageFilters.CropRect = ...,
    ) -> ImageFilter: ...
    @staticmethod
    def SpotLitSpecular(
        location: _Point3,
        target: _Point3,
        falloffExponent: float,
        cutoffAngle: float,
        lightColor: _Color,
        surfaceScale: float,
        ks: float,
        shininess: float,
        input: ImageFilter | None = None,
        cropRect: ImageFilters.CropRect = ...,
    ) -> ImageFilter: ...
    @staticmethod
    def Tile(src: _Rect, dst: _Rect, input: ImageFilter | None = None) -> ImageFilter: ...
    pass

class ImageInfo:
    """
    :note: The :py:meth:`~ImageInfo.Make` methods are also available as constructors.
    """

    @staticmethod
    def ByteSizeOverflowed(byteSize: int) -> bool: ...
    @staticmethod
    @typing.overload
    def Make(dimensions: _ISize, colorInfo: ColorInfo) -> ImageInfo: ...
    @staticmethod
    @typing.overload
    def Make(dimensions: _ISize, ct: ColorType, at: AlphaType, cs: ColorSpace | None = None) -> ImageInfo: ...
    @staticmethod
    @typing.overload
    def Make(width: int, height: int, ct: ColorType, at: AlphaType, cs: ColorSpace | None = None) -> ImageInfo: ...
    @staticmethod
    @typing.overload
    def MakeA8(dimensions: _ISize) -> ImageInfo: ...
    @staticmethod
    @typing.overload
    def MakeA8(width: int, height: int) -> ImageInfo: ...
    @staticmethod
    def MakeN32(width: int, height: int, at: AlphaType, cs: ColorSpace | None = None) -> ImageInfo: ...
    @staticmethod
    @typing.overload
    def MakeN32Premul(dimensions: _ISize, cs: ColorSpace | None = None) -> ImageInfo: ...
    @staticmethod
    @typing.overload
    def MakeN32Premul(width: int, height: int, cs: ColorSpace | None = None) -> ImageInfo: ...
    @staticmethod
    def MakeS32(width: int, height: int, at: AlphaType) -> ImageInfo: ...
    @staticmethod
    @typing.overload
    def MakeUnknown() -> ImageInfo: ...
    @staticmethod
    @typing.overload
    def MakeUnknown(width: int, height: int) -> ImageInfo: ...
    def __eq__(self, arg0: ImageInfo) -> bool: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, dimensions: _ISize, colorInfo: ColorInfo) -> None: ...
    @typing.overload
    def __init__(self, dimensions: _ISize, ct: ColorType, at: AlphaType, cs: ColorSpace | None = None) -> None: ...
    @typing.overload
    def __init__(self, width: int, height: int, ct: ColorType, at: AlphaType, cs: ColorSpace | None = None) -> None: ...
    def __ne__(self, arg0: ImageInfo) -> bool: ...
    def __str__(self) -> str: ...
    def alphaType(self) -> AlphaType: ...
    def bounds(self) -> IRect: ...
    def bytesPerPixel(self) -> int: ...
    def colorInfo(self) -> ColorInfo: ...
    def colorSpace(self) -> ColorSpace: ...
    def colorType(self) -> ColorType: ...
    def computeByteSize(self, rowBytes: int) -> int: ...
    def computeMinByteSize(self) -> int: ...
    def computeOffset(self, x: int, y: int, rowBytes: int) -> int: ...
    def dimensions(self) -> ISize: ...
    def gammaCloseToSRGB(self) -> bool: ...
    def height(self) -> int: ...
    def isEmpty(self) -> bool: ...
    def isOpaque(self) -> bool: ...
    def makeAlphaType(self, newAlphaType: AlphaType) -> ImageInfo: ...
    def makeColorSpace(self, cs: ColorSpace) -> ImageInfo: ...
    def makeColorType(self, newColorType: ColorType) -> ImageInfo: ...
    def makeDimensions(self, newSize: _ISize) -> ImageInfo: ...
    def makeWH(self, newWidth: int, newHeight: int) -> ImageInfo: ...
    def minRowBytes(self) -> int: ...
    def minRowBytes64(self) -> int: ...
    def refColorSpace(self) -> ColorSpace: ...
    def reset(self) -> None: ...
    def shiftPerPixel(self) -> int: ...
    def validRowBytes(self, rowBytes: int) -> bool: ...
    def width(self) -> int: ...
    pass

class Line2DPathEffect:
    @staticmethod
    def Make(width: float, matrix: Matrix) -> PathEffect: ...
    pass

class LumaColorFilter:
    @staticmethod
    def Make() -> ColorFilter: ...
    pass

class MaskFilter(Flattenable):
    @staticmethod
    def Deserialize(data: buffer) -> MaskFilter: ...
    @staticmethod
    def MakeBlur(style: BlurStyle, sigma: float, respectCTM: bool = True) -> MaskFilter: ...
    def approximateFilteredBounds(self, src: _Rect) -> Rect: ...
    pass

class Matrix:
    class ScaleToFit:
        """
        Members:

          kFill_ScaleToFit

          kStart_ScaleToFit

          kCenter_ScaleToFit

          kEnd_ScaleToFit
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
        __members__: dict  # value = {'kFill_ScaleToFit': <ScaleToFit.kFill_ScaleToFit: 0>, 'kStart_ScaleToFit': <ScaleToFit.kStart_ScaleToFit: 1>, 'kCenter_ScaleToFit': <ScaleToFit.kCenter_ScaleToFit: 2>, 'kEnd_ScaleToFit': <ScaleToFit.kEnd_ScaleToFit: 3>}
        kCenter_ScaleToFit: animator.skia.Matrix.ScaleToFit  # value = <ScaleToFit.kCenter_ScaleToFit: 2>
        kEnd_ScaleToFit: animator.skia.Matrix.ScaleToFit  # value = <ScaleToFit.kEnd_ScaleToFit: 3>
        kFill_ScaleToFit: animator.skia.Matrix.ScaleToFit  # value = <ScaleToFit.kFill_ScaleToFit: 0>
        kStart_ScaleToFit: animator.skia.Matrix.ScaleToFit  # value = <ScaleToFit.kStart_ScaleToFit: 1>
        pass

    class TypeMask(IntEnum):
        """
        Members:

          kIdentity_Mask

          kTranslate_Mask

          kScale_Mask

          kAffine_Mask

          kPerspective_Mask
        """

        def __and__(self, other: object) -> object: ...
        def __eq__(self, other: object) -> bool: ...
        def __ge__(self, other: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __gt__(self, other: object) -> bool: ...
        def __hash__(self) -> int: ...
        def __index__(self) -> int: ...
        def __init__(self, value: int) -> None: ...
        def __int__(self) -> int: ...
        def __invert__(self) -> object: ...
        def __le__(self, other: object) -> bool: ...
        def __lt__(self, other: object) -> bool: ...
        def __ne__(self, other: object) -> bool: ...
        def __or__(self, other: object) -> object: ...
        def __rand__(self, other: object) -> object: ...
        def __repr__(self) -> str: ...
        def __ror__(self, other: object) -> object: ...
        def __rxor__(self, other: object) -> object: ...
        def __setstate__(self, state: int) -> None: ...
        def __xor__(self, other: object) -> object: ...
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
        __members__: dict  # value = {'kIdentity_Mask': <TypeMask.kIdentity_Mask: 0>, 'kTranslate_Mask': <TypeMask.kTranslate_Mask: 1>, 'kScale_Mask': <TypeMask.kScale_Mask: 2>, 'kAffine_Mask': <TypeMask.kAffine_Mask: 4>, 'kPerspective_Mask': <TypeMask.kPerspective_Mask: 8>}
        kAffine_Mask: animator.skia.Matrix.TypeMask  # value = <TypeMask.kAffine_Mask: 4>
        kIdentity_Mask: animator.skia.Matrix.TypeMask  # value = <TypeMask.kIdentity_Mask: 0>
        kPerspective_Mask: animator.skia.Matrix.TypeMask  # value = <TypeMask.kPerspective_Mask: 8>
        kScale_Mask: animator.skia.Matrix.TypeMask  # value = <TypeMask.kScale_Mask: 2>
        kTranslate_Mask: animator.skia.Matrix.TypeMask  # value = <TypeMask.kTranslate_Mask: 1>
        pass
    @staticmethod
    def Concat(a: Matrix, b: Matrix) -> Matrix: ...
    @staticmethod
    def I() -> Matrix: ...
    @staticmethod
    def InvalidMatrix() -> Matrix: ...
    @staticmethod
    def MakeAll(
        scaleX: float,
        skewX: float,
        transX: float,
        skewY: float,
        scaleY: float,
        transY: float,
        pers0: float,
        pers1: float,
        pers2: float,
    ) -> Matrix: ...
    @staticmethod
    def MakeRectToRect(src: _Rect, dst: _Rect, stf: Matrix.ScaleToFit) -> Matrix: ...
    @staticmethod
    def RectToRect(src: _Rect, dst: _Rect, mode: Matrix.ScaleToFit = ScaleToFit.kFill_ScaleToFit) -> Matrix: ...
    @staticmethod
    @typing.overload
    def RotateDeg(deg: float) -> Matrix: ...
    @staticmethod
    @typing.overload
    def RotateDeg(deg: float, pt: _Point) -> Matrix: ...
    @staticmethod
    def RotateRad(rad: float) -> Matrix: ...
    @staticmethod
    def Scale(sx: float, sy: float) -> Matrix: ...
    @staticmethod
    def SetAffineIdentity() -> list[float]:
        """
        Returns affine with identity values in column major order. Sets affine to:

            | 1 0 0 |
            | 0 1 0 |

        :return: list of 6 floats
        """
    @staticmethod
    def Skew(kx: float, ky: float) -> Matrix: ...
    @staticmethod
    @typing.overload
    def Translate(dx: float, dy: float) -> Matrix: ...
    @staticmethod
    @typing.overload
    def Translate(t: IPoint) -> Matrix: ...
    @staticmethod
    @typing.overload
    def Translate(t: _Point) -> Matrix: ...
    def __eq__(self, arg0: Matrix) -> bool: ...
    def __getitem__(self, index: int) -> float: ...
    def __imatmul__(self, other: Matrix) -> Matrix:
        """
        Concatenates the matrix with the *other* matrix and returns the result. This is equivalent to
        ``self.preConcat(other)``.
        """
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, array: numpy.ndarray) -> None:
        """
        Creates a :py:class:`Matrix` from 3x3 float32 NumPy array.
        """
    def __matmul__(self, other: Matrix) -> Matrix:
        """
        Returns the result of multiplying this :py:class:`Matrix` by *other*. Same as :py:meth:`Matrix.Concat`.
        """
    def __ne__(self, arg0: Matrix) -> bool: ...
    def __setitem__(self, index: int, value: float) -> None: ...
    def __str__(self) -> str: ...
    def asAffine(self) -> list[float] | None:
        """
        Returns affine in column major order. Sets affine to:

            | scale-x  skew-x translate-x |
            | skew-y  scale-y translate-y |

        If :py:class:`Matrix` contains perspective, returns ``None``.

        :return: list of 6 floats or ``None``
        :rtype: list | None
        """
    def decomposeScale(self) -> tuple | None:
        """
        Decomposes :py:class:`Matrix` into scale components and whatever remains. Returns ``None`` if
        :py:class:`Matrix` could not be decomposed.

        :return: tuple of (axes scaling factors, :py:class:`Matrix` without scaling) or ``None``
        :rtype: (:py:class:`Size`, :py:class:`Matrix`) | None
        """
    def dirtyMatrixTypeCache(self) -> None: ...
    def dump(self) -> None: ...
    def get(self, index: int) -> float: ...
    def get9(self) -> list[float]:
        """
        Returns nine scalar values contained by :py:class:`Matrix` into list, in member value ascending order:
        kMScaleX, kMSkewX, kMTransX, kMSkewY, kMScaleY, kMTransY, kMPersp0, kMPersp1, kMPersp2.
        """
    def getMaxScale(self) -> float: ...
    def getMinMaxScales(self) -> tuple | None:
        """
        Returns a tuple of (minimum scaling factor, maximum scaling factor). Return ``None`` if scale factors
        are not found.

        :return: minimum and maximum scale factors
        :rtype: (float, float) | None
        """
    def getMinScale(self) -> float: ...
    def getPerspX(self) -> float: ...
    def getPerspY(self) -> float: ...
    def getScaleX(self) -> float: ...
    def getScaleY(self) -> float: ...
    def getSkewX(self) -> float: ...
    def getSkewY(self) -> float: ...
    def getTranslateX(self) -> float: ...
    def getTranslateY(self) -> float: ...
    def getType(self) -> Matrix.TypeMask: ...
    def hasPerspective(self) -> bool: ...
    def invert(self, inverse: Matrix) -> bool: ...
    def isFinite(self) -> bool: ...
    def isIdentity(self) -> bool: ...
    def isScaleTranslate(self) -> bool: ...
    def isSimilarity(self, tol: float = 0.000244140625) -> bool: ...
    def isTranslate(self) -> bool: ...
    def makeInverse(self) -> Matrix:
        """
        Returns the inverse of the matrix. If the matrix is singular, throws a ValueError.

        :return: The inverse of the matrix.
        """
    @typing.overload
    def mapHomogeneousPoints(self, src: list[_Point3]) -> list[Point3]:
        """
        Maps *src* list of :py:class:`Point3` and returns a new list of :py:class:`Point3`.

        :param src: list of :py:class:`Point3` to transform
        :return: list of mapped :py:class:`Point3`
        """
    @typing.overload
    def mapHomogeneousPoints(self, src: list[_Point]) -> list[Point3]:
        """
        Returns homogeneous points, starting with 2D src points (with implied w = 1).
        """
    def mapOrigin(self) -> Point: ...
    def mapPoint(self, pt: _Point) -> Point: ...
    def mapPoints(self, pts: list[_Point]) -> list[Point]:
        """
        Maps *src* list of :py:class:`Point` and returns a new list of :py:class:`Point`.

        :param src: list of :py:class:`Point` to transform
        :return: list of mapped :py:class:`Point`
        """
    def mapRadius(self, radius: float) -> float: ...
    def mapRect(self, src: _Rect, pc: ApplyPerspectiveClip = ApplyPerspectiveClip.kYes) -> Rect: ...
    def mapRectScaleTranslate(self, src: _Rect) -> Rect:
        """
        Returns bounds of src corners mapped by :py:class:`Matrix`.

        :param src: :py:class:`Rect` to map
        :return: bounds of mapped :py:class:`Point`
        """
    def mapRectToQuad(self, rect: _Rect) -> list[Point]:
        """
        Maps four corners of *rect* to a list of 4 :py:class:`Point`.

        :param rect: :py:class:`Rect` to map
        :return: mapped corner :py:class:`Point`
        """
    def mapVector(self, dx: float, dy: float) -> Point: ...
    def mapVectors(self, vecs: list[_Point]) -> list[Point]:
        """
        Maps *vecs* list of :py:class:`Point` and returns a new list of :py:class:`Point`, multiplying each
        vector by :py:class:`Matrix`, treating translation as zero.

        :param vecs: list of :py:class:`Point` to transform
        :return: list of transformed :py:class:`Point`
        """
    def mapXY(self, x: float, y: float) -> Point: ...
    def normalizePerspective(self) -> None: ...
    def postConcat(self, other: Matrix) -> Matrix: ...
    @typing.overload
    def postRotate(self, degrees: float) -> Matrix: ...
    @typing.overload
    def postRotate(self, degrees: float, px: float, py: float) -> Matrix: ...
    @typing.overload
    def postScale(self, sx: float, sy: float) -> Matrix: ...
    @typing.overload
    def postScale(self, sx: float, sy: float, px: float, py: float) -> Matrix: ...
    @typing.overload
    def postSkew(self, kx: float, ky: float) -> Matrix: ...
    @typing.overload
    def postSkew(self, kx: float, ky: float, px: float, py: float) -> Matrix: ...
    def postTranslate(self, dx: float, dy: float) -> Matrix: ...
    def preConcat(self, other: Matrix) -> Matrix: ...
    @typing.overload
    def preRotate(self, degrees: float) -> Matrix: ...
    @typing.overload
    def preRotate(self, degrees: float, px: float, py: float) -> Matrix: ...
    @typing.overload
    def preScale(self, sx: float, sy: float) -> Matrix: ...
    @typing.overload
    def preScale(self, sx: float, sy: float, px: float, py: float) -> Matrix: ...
    @typing.overload
    def preSkew(self, kx: float, ky: float) -> Matrix: ...
    @typing.overload
    def preSkew(self, kx: float, ky: float, px: float, py: float) -> Matrix: ...
    def preTranslate(self, dx: float, dy: float) -> Matrix: ...
    def preservesAxisAlignment(self) -> bool: ...
    def preservesRightAngles(self, tol: float = 0.000244140625) -> bool: ...
    def rc(self, r: int, c: int) -> float: ...
    def rectStaysRect(self) -> bool: ...
    def reset(self) -> Matrix: ...
    def set(self, index: int, value: float) -> Matrix: ...
    def set9(self, buffer: list[float]) -> Matrix: ...
    def setAffine(self, affine: list[float]) -> Matrix: ...
    def setAll(
        self,
        scaleX: float,
        skewX: float,
        transX: float,
        skewY: float,
        scaleY: float,
        transY: float,
        persp0: float,
        persp1: float,
        persp2: float,
    ) -> Matrix: ...
    def setConcat(self, a: Matrix, b: Matrix) -> Matrix: ...
    def setIdentity(self) -> Matrix: ...
    def setPerspX(self, v: float) -> Matrix: ...
    def setPerspY(self, v: float) -> Matrix: ...
    def setPolyToPoly(self, src: list[_Point], dst: list[_Point]) -> bool: ...
    def setRSXform(self, rsxForm: RSXform) -> Matrix: ...
    def setRectToRect(self, src: _Rect, dst: _Rect, stf: Matrix.ScaleToFit) -> bool: ...
    @typing.overload
    def setRotate(self, degrees: float) -> Matrix: ...
    @typing.overload
    def setRotate(self, degrees: float, px: float, py: float) -> Matrix: ...
    @typing.overload
    def setScale(self, sx: float, sy: float) -> Matrix: ...
    @typing.overload
    def setScale(self, sx: float, sy: float, px: float, py: float) -> Matrix: ...
    def setScaleTranslate(self, sx: float, sy: float, tx: float, ty: float) -> None: ...
    def setScaleX(self, v: float) -> Matrix: ...
    def setScaleY(self, v: float) -> Matrix: ...
    @typing.overload
    def setSinCos(self, sinValue: float, cosValue: float) -> Matrix: ...
    @typing.overload
    def setSinCos(self, sinValue: float, cosValue: float, px: float, py: float) -> Matrix: ...
    @typing.overload
    def setSkew(self, kx: float, ky: float) -> Matrix: ...
    @typing.overload
    def setSkew(self, kx: float, ky: float, px: float, py: float) -> Matrix: ...
    def setSkewX(self, v: float) -> Matrix: ...
    def setSkewY(self, v: float) -> Matrix: ...
    @typing.overload
    def setTranslate(self, dx: float, dy: float) -> Matrix: ...
    @typing.overload
    def setTranslate(self, v: _Point) -> Matrix: ...
    def setTranslateX(self, v: float) -> Matrix: ...
    def setTranslateY(self, v: float) -> Matrix: ...
    kAScaleX = 0
    kAScaleY = 3
    kASkewX = 2
    kASkewY = 1
    kATransX = 4
    kATransY = 5
    kMPersp0 = 6
    kMPersp1 = 7
    kMPersp2 = 8
    kMScaleX = 0
    kMScaleY = 4
    kMSkewX = 1
    kMSkewY = 3
    kMTransX = 2
    kMTransY = 5
    pass

class MatrixPathEffect:
    @staticmethod
    def Make(matrix: Matrix) -> PathEffect: ...
    @staticmethod
    def MakeTranslate(dx: float, dy: float) -> PathEffect: ...
    pass

class MergePathEffect:
    @staticmethod
    def Make(one: PathEffect, two: PathEffect, op: PathOp) -> PathEffect: ...
    pass

class MipmapMode:
    """
    Members:

      kNone

      kNearest

      kLinear

      kLast
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
    __members__: dict  # value = {'kNone': <MipmapMode.kNone: 0>, 'kNearest': <MipmapMode.kNearest: 1>, 'kLinear': <MipmapMode.kLinear: 2>, 'kLast': <MipmapMode.kLinear: 2>}
    kLast: animator.skia.MipmapMode  # value = <MipmapMode.kLinear: 2>
    kLinear: animator.skia.MipmapMode  # value = <MipmapMode.kLinear: 2>
    kNearest: animator.skia.MipmapMode  # value = <MipmapMode.kNearest: 1>
    kNone: animator.skia.MipmapMode  # value = <MipmapMode.kNone: 0>
    pass

class NamedGamut:
    kAdobeRGB: animator.skia.cms.Matrix3x3
    kDisplayP3: animator.skia.cms.Matrix3x3
    kRec2020: animator.skia.cms.Matrix3x3
    kSRGB: animator.skia.cms.Matrix3x3
    kXYZ: animator.skia.cms.Matrix3x3
    pass

class NamedTransferFn:
    k2Dot2: animator.skia.cms.TransferFunction
    kHLG: animator.skia.cms.TransferFunction
    kLinear: animator.skia.cms.TransferFunction
    kPQ: animator.skia.cms.TransferFunction
    kRec2020: animator.skia.cms.TransferFunction
    kSRGB: animator.skia.cms.TransferFunction
    pass

class OpBuilder:
    def __init__(self) -> None: ...
    def add(self, path: Path, op: PathOp) -> None: ...
    def resolve(self) -> Path:
        """
        Computes the sum of all paths and operands and returns it, and resets the builder to its initial state.
        If the operation fails, throws a runtime error.
        """

class OverdrawColorFilter:
    @staticmethod
    def MakeWithColors(colors: list[_Color]) -> ColorFilter: ...
    kNumColors = 6
    pass

class Paint:
    class Cap:
        """
        Members:

          kButt_Cap

          kRound_Cap

          kSquare_Cap

          kLast_Cap

          kDefault_Cap
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
        __members__: dict  # value = {'kButt_Cap': <Cap.kButt_Cap: 0>, 'kRound_Cap': <Cap.kRound_Cap: 1>, 'kSquare_Cap': <Cap.kSquare_Cap: 2>, 'kLast_Cap': <Cap.kSquare_Cap: 2>, 'kDefault_Cap': <Cap.kButt_Cap: 0>}
        kButt_Cap: animator.skia.Paint.Cap  # value = <Cap.kButt_Cap: 0>
        kDefault_Cap: animator.skia.Paint.Cap  # value = <Cap.kButt_Cap: 0>
        kLast_Cap: animator.skia.Paint.Cap  # value = <Cap.kSquare_Cap: 2>
        kRound_Cap: animator.skia.Paint.Cap  # value = <Cap.kRound_Cap: 1>
        kSquare_Cap: animator.skia.Paint.Cap  # value = <Cap.kSquare_Cap: 2>
        pass

    class Join:
        """
        Members:

          kMiter_Join

          kRound_Join

          kBevel_Join

          kLast_Join

          kDefault_Join
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
        __members__: dict  # value = {'kMiter_Join': <Join.kMiter_Join: 0>, 'kRound_Join': <Join.kRound_Join: 1>, 'kBevel_Join': <Join.kBevel_Join: 2>, 'kLast_Join': <Join.kBevel_Join: 2>, 'kDefault_Join': <Join.kMiter_Join: 0>}
        kBevel_Join: animator.skia.Paint.Join  # value = <Join.kBevel_Join: 2>
        kDefault_Join: animator.skia.Paint.Join  # value = <Join.kMiter_Join: 0>
        kLast_Join: animator.skia.Paint.Join  # value = <Join.kBevel_Join: 2>
        kMiter_Join: animator.skia.Paint.Join  # value = <Join.kMiter_Join: 0>
        kRound_Join: animator.skia.Paint.Join  # value = <Join.kRound_Join: 1>
        pass

    class Style:
        """
        Members:

          kFill_Style

          kStroke_Style

          kStrokeAndFill_Style
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
        __members__: dict  # value = {'kFill_Style': <Style.kFill_Style: 0>, 'kStroke_Style': <Style.kStroke_Style: 1>, 'kStrokeAndFill_Style': <Style.kStrokeAndFill_Style: 2>}
        kFill_Style: animator.skia.Paint.Style  # value = <Style.kFill_Style: 0>
        kStrokeAndFill_Style: animator.skia.Paint.Style  # value = <Style.kStrokeAndFill_Style: 2>
        kStroke_Style: animator.skia.Paint.Style  # value = <Style.kStroke_Style: 1>
        pass
    def __eq__(self, other: Paint) -> bool: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(
        self,
        antiAlias: bool = ...,
        dither: bool = ...,
        style: Style = ...,
        stroke: bool = ...,
        color: _Color = ...,
        color4f: _Color4f = ...,
        alphaf: float = ...,
        alpha: int = ...,
        argb: tuple[int, int, int, int] = ...,
        strokeWidth: float = ...,
        strokeMiter: float = ...,
        strokeCap: Cap = ...,
        strokeJoin: Join = ...,
        shader: Shader | None = ...,
        colorFilter: ColorFilter | None = ...,
        blendMode: BlendMode = ...,
        blender: Blender | None = ...,
        pathEffect: PathEffect = ...,
        maskFilter: MaskFilter | None = ...,
        imageFilter: ImageFilter | None = ...,
    ) -> None:
        """
        Construct a new paint from keyword arguments. This creates a new :py:class:`Paint` object and calls the
        respective setters for each keyword argument.

        Supported keyword arguments: ``antiAlias``, ``dither``, ``style``, ``stroke``, ``color``, ``color4f``,
        ``alphaf``, ``alpha``, ``argb``, ``strokeWidth``, ``strokeMiter``, ``strokeCap``, ``strokeJoin``, ``shader``,
        ``colorFilter``, ``blendMode``, ``blender``, ``pathEffect``, ``maskFilter``, ``imageFilter``.

        :note: Later arguments override earlier ones.
        """
    @typing.overload
    def __init__(self, color: _Color4f, colorSpace: ColorSpace | None = None) -> None: ...
    @typing.overload
    def __init__(self, paint: Paint) -> None: ...
    def __ne__(self, other: Paint) -> bool: ...
    def __str__(self) -> str: ...
    def asBlendMode(self) -> BlendMode | None: ...
    def getAlpha(self) -> int: ...
    def getAlphaf(self) -> float: ...
    def getBlendMode_or(self, defaultMode: BlendMode) -> BlendMode: ...
    def getBlender(self) -> Blender: ...
    def getColor(self) -> int: ...
    def getColor4f(self) -> Color4f: ...
    def getColorFilter(self) -> ColorFilter: ...
    def getImageFilter(self) -> ImageFilter: ...
    def getMaskFilter(self) -> MaskFilter: ...
    def getPathEffect(self) -> PathEffect: ...
    def getShader(self) -> Shader: ...
    def getStrokeCap(self) -> Paint.Cap: ...
    def getStrokeJoin(self) -> Paint.Join: ...
    def getStrokeMiter(self) -> float: ...
    def getStrokeWidth(self) -> float: ...
    def getStyle(self) -> Paint.Style: ...
    def isAntiAlias(self) -> bool: ...
    def isDither(self) -> bool: ...
    def isSrcOver(self) -> bool: ...
    def nothingToDraw(self) -> bool: ...
    def refBlender(self) -> Blender: ...
    def refColorFilter(self) -> ColorFilter: ...
    def refImageFilter(self) -> ImageFilter: ...
    def refMaskFilter(self) -> MaskFilter: ...
    def refPathEffect(self) -> PathEffect: ...
    def refShader(self) -> Shader: ...
    def reset(self) -> None: ...
    def setARGB(self, a: int, r: int, g: int, b: int) -> None: ...
    def setAlpha(self, a: int) -> None: ...
    def setAlphaf(self, a: float) -> None: ...
    def setAntiAlias(self, aa: bool) -> None: ...
    def setBlendMode(self, mode: BlendMode) -> None: ...
    def setBlender(self, blender: Blender | None) -> None: ...
    @typing.overload
    def setColor(self, color: _Color4f, colorSpace: ColorSpace | None = None) -> None: ...
    @typing.overload
    def setColor(self, color: _Color) -> None: ...
    def setColor4f(self, color: _Color4f, colorSpace: ColorSpace | None = None) -> None: ...
    def setColorFilter(self, colorFilter: ColorFilter | None) -> None: ...
    def setDither(self, dither: bool) -> None: ...
    def setImageFilter(self, imageFilter: ImageFilter | None) -> None: ...
    def setMaskFilter(self, maskFilter: MaskFilter | None) -> None: ...
    def setPathEffect(self, pathEffect: PathEffect | None) -> None: ...
    def setShader(self, shader: Shader | None) -> None: ...
    def setStroke(self, isStroke: bool) -> None: ...
    def setStrokeCap(self, cap: Paint.Cap) -> None: ...
    def setStrokeJoin(self, join: Paint.Join) -> None: ...
    def setStrokeMiter(self, miter: float) -> None: ...
    def setStrokeWidth(self, width: float) -> None: ...
    def setStyle(self, style: Paint.Style) -> None: ...
    kCapCount = 3
    kJoinCount = 3
    kStyleCount = 3
    pass

class ParsePath:
    class PathEncoding:
        """
        Members:

          Absolute

          Relative
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
        Absolute: animator.skia.ParsePath.PathEncoding  # value = <PathEncoding.Absolute: 0>
        Relative: animator.skia.ParsePath.PathEncoding  # value = <PathEncoding.Relative: 1>
        __members__: dict  # value = {'Absolute': <PathEncoding.Absolute: 0>, 'Relative': <PathEncoding.Relative: 1>}
        pass
    @staticmethod
    def FromSVGString(str: str) -> Path:
        """
        Create a :py:class:`skia.Path` from an SVG string.
        """
    @staticmethod
    def ToSVGString(path: Path, encoding: ParsePath.PathEncoding = PathEncoding.Absolute) -> str:
        """
        Create an SVG string from a :py:class:`skia.Path`.
        """

class Path:
    class AddPathMode:
        """
        Members:

          kAppend_AddPathMode

          kExtend_AddPathMode
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
        __members__: dict  # value = {'kAppend_AddPathMode': <AddPathMode.kAppend_AddPathMode: 0>, 'kExtend_AddPathMode': <AddPathMode.kExtend_AddPathMode: 1>}
        kAppend_AddPathMode: animator.skia.Path.AddPathMode  # value = <AddPathMode.kAppend_AddPathMode: 0>
        kExtend_AddPathMode: animator.skia.Path.AddPathMode  # value = <AddPathMode.kExtend_AddPathMode: 1>
        pass

    class ArcSize:
        """
        Members:

          kSmall_ArcSize

          kLarge_ArcSize
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
        __members__: dict  # value = {'kSmall_ArcSize': <ArcSize.kSmall_ArcSize: 0>, 'kLarge_ArcSize': <ArcSize.kLarge_ArcSize: 1>}
        kLarge_ArcSize: animator.skia.Path.ArcSize  # value = <ArcSize.kLarge_ArcSize: 1>
        kSmall_ArcSize: animator.skia.Path.ArcSize  # value = <ArcSize.kSmall_ArcSize: 0>
        pass

    class Iter:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, path: Path, forceClose: bool) -> None: ...
        def __iter__(self) -> Path.Iter: ...
        def __next__(self) -> tuple[Path.Verb, list[Point], float | None]:
            """
            Returns a tuple of (:py:class:`Path.Verb`, list of :py:class:`Point`, weight) for the next segment in the
            path. If the verb is not :py:attr:`Path.Verb.kConic_Verb`, the weight is ``None``.
            """
        def conicWeight(self) -> float: ...
        def isCloseLine(self) -> bool: ...
        def isClosedContour(self) -> bool: ...
        def next(self) -> tuple[Path.Verb, list[Point]]:
            """
            Returns a tuple of (:py:class:`Path.Verb`, list of :py:class:`Point`) for the next segment in the path.
            """
        def setPath(self, path: Path, forceClose: bool) -> None: ...
        pass

    class SegmentMask:
        """
        Members:

          kLine_SegmentMask

          kQuad_SegmentMask

          kConic_SegmentMask

          kCubic_SegmentMask
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
        __members__: dict  # value = {'kLine_SegmentMask': <SegmentMask.kLine_SegmentMask: 1>, 'kQuad_SegmentMask': <SegmentMask.kQuad_SegmentMask: 2>, 'kConic_SegmentMask': <SegmentMask.kConic_SegmentMask: 4>, 'kCubic_SegmentMask': <SegmentMask.kCubic_SegmentMask: 8>}
        kConic_SegmentMask: animator.skia.Path.SegmentMask  # value = <SegmentMask.kConic_SegmentMask: 4>
        kCubic_SegmentMask: animator.skia.Path.SegmentMask  # value = <SegmentMask.kCubic_SegmentMask: 8>
        kLine_SegmentMask: animator.skia.Path.SegmentMask  # value = <SegmentMask.kLine_SegmentMask: 1>
        kQuad_SegmentMask: animator.skia.Path.SegmentMask  # value = <SegmentMask.kQuad_SegmentMask: 2>
        pass

    class Verb:
        """
        Members:

          kMove_Verb

          kLine_Verb

          kQuad_Verb

          kConic_Verb

          kCubic_Verb

          kClose_Verb

          kDone_Verb
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
        __members__: dict  # value = {'kMove_Verb': <Verb.kMove_Verb: 0>, 'kLine_Verb': <Verb.kLine_Verb: 1>, 'kQuad_Verb': <Verb.kQuad_Verb: 2>, 'kConic_Verb': <Verb.kConic_Verb: 3>, 'kCubic_Verb': <Verb.kCubic_Verb: 4>, 'kClose_Verb': <Verb.kClose_Verb: 5>, 'kDone_Verb': <Verb.kDone_Verb: 6>}
        kClose_Verb: animator.skia.Path.Verb  # value = <Verb.kClose_Verb: 5>
        kConic_Verb: animator.skia.Path.Verb  # value = <Verb.kConic_Verb: 3>
        kCubic_Verb: animator.skia.Path.Verb  # value = <Verb.kCubic_Verb: 4>
        kDone_Verb: animator.skia.Path.Verb  # value = <Verb.kDone_Verb: 6>
        kLine_Verb: animator.skia.Path.Verb  # value = <Verb.kLine_Verb: 1>
        kMove_Verb: animator.skia.Path.Verb  # value = <Verb.kMove_Verb: 0>
        kQuad_Verb: animator.skia.Path.Verb  # value = <Verb.kQuad_Verb: 2>
        pass
    @staticmethod
    def Circle(center_x: float, center_y: float, radius: float, dir: PathDirection = PathDirection.kCW) -> Path: ...
    @staticmethod
    def ConvertConicToQuads(p0: _Point, p1: _Point, p2: _Point, w: float, pow2: int) -> list[Point]:
        """
        Approximates conic represented by start point *p0*, control point *p1*, end point *p2* and weight *w*,
        with quad array and returns it. Maximum possible return array size is given by: (1 + 2 * (1 << pow2)).
        """
    @staticmethod
    def GetFromText(text: str, x: float, y: float, font: Font, encoding: TextEncoding = TextEncoding.kUTF8) -> Path:
        """
        Returns the path representing the *text* using SkTextUtils.
        """
    @staticmethod
    def IsCubicDegenerate(p1: _Point, p2: _Point, p3: _Point, p4: _Point, exact: bool) -> bool: ...
    @staticmethod
    def IsLineDegenerate(p1: _Point, p2: _Point, exact: bool) -> bool: ...
    @staticmethod
    def IsQuadDegenerate(p1: _Point, p2: _Point, p3: _Point, exact: bool) -> bool: ...
    @staticmethod
    def Line(a: _Point, b: _Point) -> Path: ...
    @staticmethod
    def Make(
        pts: list[_Point],
        vbs: list[int],
        ws: list[float],
        ft: PathFillType,
        isVolatile: bool = False,
    ) -> Path: ...
    @staticmethod
    @typing.overload
    def Oval(r: _Rect, dir: PathDirection = PathDirection.kCW) -> Path: ...
    @staticmethod
    @typing.overload
    def Oval(r: _Rect, dir: PathDirection, startIndex: int) -> Path: ...
    @staticmethod
    def Polygon(
        points: list[_Point], isClosed: bool, ft: PathFillType = PathFillType.kWinding, isVolatile: bool = False
    ) -> Path:
        """
        Create a polygonal path from a list of points.
        """
    @staticmethod
    @typing.overload
    def RRect(bounds: _Rect, rx: float, ry: float, dir: PathDirection = PathDirection.kCW) -> Path: ...
    @staticmethod
    @typing.overload
    def RRect(rr: RRect, dir: PathDirection = PathDirection.kCW) -> Path: ...
    @staticmethod
    @typing.overload
    def RRect(rr: RRect, dir: PathDirection, startIndex: int) -> Path: ...
    @staticmethod
    def Rect(rect: _Rect, dir: PathDirection = PathDirection.kCW, startIndex: int = 0) -> Path: ...
    def __add__(self, arg0: Path) -> Path: ...
    def __and__(self, arg0: Path) -> Path: ...
    def __eq__(self, other: Path) -> bool: ...
    def __iadd__(self, arg0: Path) -> Path: ...
    def __iand__(self, arg0: Path) -> Path: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, path: Path) -> None: ...
    def __ior__(self, arg0: Path) -> Path: ...
    def __isub__(self, arg0: Path) -> Path: ...
    def __iter__(self) -> Path.Iter: ...
    def __ixor__(self, arg0: Path) -> Path: ...
    def __len__(self) -> int: ...
    def __ne__(self, other: Path) -> bool: ...
    def __or__(self, arg0: Path) -> Path: ...
    def __str__(self) -> str: ...
    def __sub__(self, arg0: Path) -> Path: ...
    def __xor__(self, arg0: Path) -> Path: ...
    def addArc(self, oval: _Rect, startAngle: float, sweepAngle: float) -> Path: ...
    def addCircle(self, x: float, y: float, radius: float, dir: PathDirection = PathDirection.kCW) -> Path: ...
    @typing.overload
    def addOval(self, oval: _Rect, dir: PathDirection = PathDirection.kCW) -> Path: ...
    @typing.overload
    def addOval(self, oval: _Rect, dir: PathDirection, start: int) -> Path: ...
    @typing.overload
    def addPath(
        self, src: Path, dx: float, dy: float, mode: Path.AddPathMode = AddPathMode.kAppend_AddPathMode
    ) -> Path: ...
    @typing.overload
    def addPath(self, src: Path, matrix: Matrix, mode: Path.AddPathMode = AddPathMode.kAppend_AddPathMode) -> Path: ...
    @typing.overload
    def addPath(self, src: Path, mode: Path.AddPathMode = AddPathMode.kAppend_AddPathMode) -> Path: ...
    def addPoly(self, pts: typing.Sequence[_Point], close: bool) -> Path:
        """
        Adds contour created from *pts*.
        """
    @typing.overload
    def addRRect(self, rrect: RRect, dir: PathDirection = PathDirection.kCW) -> Path: ...
    @typing.overload
    def addRRect(self, rrect: RRect, dir: PathDirection, start: int) -> Path: ...
    @typing.overload
    def addRect(
        self, left: float, top: float, right: float, bottom: float, dir: PathDirection = PathDirection.kCW
    ) -> Path: ...
    @typing.overload
    def addRect(self, rect: _Rect, dir: PathDirection = PathDirection.kCW) -> Path: ...
    @typing.overload
    def addRect(self, rect: _Rect, dir: PathDirection, start: int) -> Path: ...
    @typing.overload
    def addRoundRect(
        self, rect: _Rect, radii: typing.Sequence[float], dir: PathDirection = PathDirection.kCW
    ) -> Path: ...
    @typing.overload
    def addRoundRect(self, rect: _Rect, rx: float, ry: float, dir: PathDirection = PathDirection.kCW) -> Path: ...
    def approximateBytesUsed(self) -> int: ...
    @typing.overload
    def arcTo(self, oval: _Rect, startAngle: float, sweepAngle: float, forceMoveTo: bool) -> Path: ...
    @typing.overload
    def arcTo(self, p1: _Point, p2: _Point, radius: float) -> Path: ...
    @typing.overload
    def arcTo(
        self, r: _Point, xAxisRotate: float, largeArc: Path.ArcSize, sweep: PathDirection, xy: _Point
    ) -> Path: ...
    @typing.overload
    def arcTo(
        self, rx: float, ry: float, xAxisRotate: float, largeArc: Path.ArcSize, sweep: PathDirection, x: float, y: float
    ) -> Path: ...
    @typing.overload
    def arcTo(self, x1: float, y1: float, x2: float, y2: float, radius: float) -> Path: ...
    def asWinding(self) -> Path:
        """
        Return the result with fill type winding to area equivalent to path. If the conversion fails, throws
        a runtime error.
        """
    def close(self) -> Path: ...
    def computeTightBounds(self) -> Rect: ...
    @typing.overload
    def conicTo(self, p1: _Point, p2: _Point, w: float) -> Path: ...
    @typing.overload
    def conicTo(self, x1: float, y1: float, x2: float, y2: float, w: float) -> Path: ...
    def conservativelyContainsRect(self, rect: _Rect) -> bool: ...
    def contains(self, x: float, y: float) -> bool: ...
    def countPoints(self) -> int: ...
    def countVerbs(self) -> int: ...
    @typing.overload
    def cubicTo(self, p1: _Point, p2: _Point, p3: _Point) -> Path: ...
    @typing.overload
    def cubicTo(self, x1: float, y1: float, x2: float, y2: float, x3: float, y3: float) -> Path: ...
    def dump(self) -> None: ...
    def dumpArrays(self) -> None: ...
    def dumpHex(self) -> None: ...
    @typing.overload
    def fillPathWithPaint(self, paint: Paint, cullRect: _Rect | None = None, resScale: float = 1) -> tuple:
        """
        Returns the filled equivalent of the stroked path.

        :param paint: :py:class:`Paint` from which attributes such as stroke cap, width, miter, and join, as
            well as pathEffect will be used
        :param cullRect: optional limit passed to :py:class:`PathEffect`
        :param resScale: if > 1, increase precision, else if (0 < resScale < 1) reduce precision to favor speed
            and size
        :return: a tuple of (:py:class:`Path`, bool) where the bool indicates whether the path represents style
            fill or hairline (true for fill, false for hairline)
        """
    @typing.overload
    def fillPathWithPaint(self, paint: Paint, cullRect: _Rect, ctm: Matrix) -> tuple:
        """
        Returns the filled equivalent of the stroked path.
        """
    def getBounds(self) -> Rect: ...
    def getFillType(self) -> PathFillType: ...
    def getGenerationID(self) -> int: ...
    def getLastPt(self) -> Point | None:
        """
        Returns last point on :py:class:`Path`. Returns ``None`` if :py:class:`Point` array is empty.
        """
    def getPoint(self, index: int) -> Point: ...
    def getPoints(self, max: int = -1) -> list[Point]:
        """
        Returns a list of :py:class:`Point` representing the points in the :py:class:`Path`, up to a maximum of
        *max* points. If *max* is negative, return all points.
        """
    def getSegmentMasks(self) -> int: ...
    def getVerbs(self, max: int = -1) -> list[Path.Verb]:
        """
        Returns a list of :py:enum:`Path.Verb` representing the verbs in the :py:class:`Path`, up to a maximum
        of *max* verbs. If *max* is negative, return all verbs.
        """
    def incReserve(self, extraPtCount: int) -> None: ...
    def interpolate(self, ending: Path, weight: float) -> Path | None:
        """
        Interpolates between :py:class:`Path` with :py:class:`Point` array of equal size and return the result.
        If arrays were not equal size, returns ``None``.

        :param ending: :py:class:`Point` array averaged with this :py:class:`Point` array
        :param weight: contribution of this :py:class:`Point` array, and one minus contribution of *ending*
            :py:class:`Point` array

        :return: interpolated average or None
        :rtype: :py:class:`Path` | None
        """
    def iop(self, other: Path, op: PathOp) -> Path:
        """
        Apply the *op* to this path and the specified path in place and return itself. If the operation fails,
        throws a runtime error.
        """
    def isConvex(self) -> bool: ...
    def isEmpty(self) -> bool: ...
    def isFinite(self) -> bool: ...
    def isInterpolatable(self, compare: Path) -> bool: ...
    def isInverseFillType(self) -> bool: ...
    def isLastContourClosed(self) -> bool: ...
    def isLine(self) -> list[Point] | None:
        """
        If the :py:class:`Path` contains only one line, return the start and end points as a list of two
        :py:class:`Point`. If the :py:class:`Path` is not one line, return ``None``.

        :return: start and end points of the line or None
        :rtype: List[:py:class:`Point`] | None
        """
    def isOval(self, oval: _Rect | None = None) -> bool: ...
    def isRRect(self, rrect: RRect | None = None) -> bool: ...
    def isRect(self) -> tuple | None:
        """
        Returns a tuple of (rect - storage for bounds of :py:class:`Rect`, isClosed - if :py:class:`Path` is
        closed, direction - :py:class:`Path` direcion) if :py:class`Path` is equivalent to :py:class:`Rect` when
        filled. Otherwise returns ``None``.

        :rtype: Tuple[:py:class:`Rect`, bool, :py:enum:`PathDirection`] | None
        """
    def isValid(self) -> bool: ...
    def isVolatile(self) -> bool: ...
    def isimplify(self) -> Path:
        """
        Simplify the path in place and return itself. If the simplify fails, throws a runtime error.
        """
    @typing.overload
    def lineTo(self, p: _Point) -> Path: ...
    @typing.overload
    def lineTo(self, x: float, y: float) -> Path: ...
    def makeOffset(self, dx: float, dy: float) -> Path:
        """
        Offsets :py:class:`Point` array by (*dx*, *dy*) and returns the result as a new :py:class:`Path`.
        """
    def makeScale(self, sx: float, sy: float) -> Path: ...
    def makeTransform(self, m: Matrix, pc: ApplyPerspectiveClip = ApplyPerspectiveClip.kYes) -> Path: ...
    @typing.overload
    def moveTo(self, p: _Point) -> Path: ...
    @typing.overload
    def moveTo(self, x: float, y: float) -> Path: ...
    def offset(self, dx: float, dy: float) -> None: ...
    def op(self, two: Path, op: PathOp) -> Path:
        """
        Return the resultant path of applying the *op *to this path and the specified path. If the operation
        fails, throws a runtime error.
        """
    @typing.overload
    def quadTo(self, p1: _Point, p2: _Point) -> Path: ...
    @typing.overload
    def quadTo(self, x1: float, y1: float, x2: float, y2: float) -> Path: ...
    def rArcTo(
        self,
        rx: float,
        ry: float,
        xAxisRotate: float,
        largeArc: Path.ArcSize,
        sweep: PathDirection,
        dx: float,
        dy: float,
    ) -> Path: ...
    def rConicTo(self, dx1: float, dy1: float, dx2: float, dy2: float, w: float) -> Path: ...
    def rCubicTo(self, dx1: float, dy1: float, dx2: float, dy2: float, dx3: float, dy3: float) -> Path: ...
    def rLineTo(self, dx: float, dy: float) -> Path: ...
    def rMoveTo(self, dx: float, dy: float) -> Path: ...
    def rQuadTo(self, dx1: float, dy1: float, dx2: float, dy2: float) -> Path: ...
    def readFromMemory(self, data: buffer) -> int:
        """
        Reads the path from the buffer and returns the number of bytes read.
        """
    def reset(self) -> Path: ...
    def reverseAddPath(self, src: Path) -> Path: ...
    def rewind(self) -> Path: ...
    def serialize(self) -> Data: ...
    def setFillType(self, ft: PathFillType) -> None: ...
    def setIsVolatile(self, isVolatile: bool) -> Path: ...
    @typing.overload
    def setLastPt(self, p: _Point) -> None: ...
    @typing.overload
    def setLastPt(self, x: float, y: float) -> None: ...
    def simplify(self) -> Path:
        """
        Return the path as a set of non-overlapping contours that describe the same area as the original path.
        If the simplify fails, throws a runtime error.
        """
    def swap(self, other: Path) -> None: ...
    def tightBounds(self) -> Rect:
        """
        Return the resulting rectangle to the tight bounds of the path.
        """
    def toggleInverseFillType(self) -> None: ...
    def transform(self, matrix: Matrix, pc: ApplyPerspectiveClip = ApplyPerspectiveClip.kYes) -> None: ...
    def updateBoundsCache(self) -> None: ...
    pass

class Path1DPathEffect:
    class Style:
        """
        Members:

          kTranslate_Style

          kRotate_Style

          kMorph_Style

          kLastEnum_Style
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
        __members__: dict  # value = {'kTranslate_Style': <Style.kTranslate_Style: 0>, 'kRotate_Style': <Style.kRotate_Style: 1>, 'kMorph_Style': <Style.kMorph_Style: 2>, 'kLastEnum_Style': <Style.kMorph_Style: 2>}
        kLastEnum_Style: animator.skia.Path1DPathEffect.Style  # value = <Style.kMorph_Style: 2>
        kMorph_Style: animator.skia.Path1DPathEffect.Style  # value = <Style.kMorph_Style: 2>
        kRotate_Style: animator.skia.Path1DPathEffect.Style  # value = <Style.kRotate_Style: 1>
        kTranslate_Style: animator.skia.Path1DPathEffect.Style  # value = <Style.kTranslate_Style: 0>
        pass
    @staticmethod
    def Make(path: Path, advance: float, phase: float, style: Path1DPathEffect.Style) -> PathEffect: ...
    pass

class Path2DPathEffect:
    @staticmethod
    def Make(matrix: Matrix, path: Path) -> PathEffect: ...
    pass

class PathBuilder:
    class ArcSize:
        """
        Members:

          kSmall_ArcSize

          kLarge_ArcSize
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
        __members__: dict  # value = {'kSmall_ArcSize': <ArcSize.kSmall_ArcSize: 0>, 'kLarge_ArcSize': <ArcSize.kLarge_ArcSize: 1>}
        kLarge_ArcSize: animator.skia.PathBuilder.ArcSize  # value = <ArcSize.kLarge_ArcSize: 1>
        kSmall_ArcSize: animator.skia.PathBuilder.ArcSize  # value = <ArcSize.kSmall_ArcSize: 0>
        pass
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, ft: PathFillType) -> None: ...
    @typing.overload
    def __init__(self, pathBuilder: PathBuilder) -> None: ...
    @typing.overload
    def __init__(self, src: Path) -> None: ...
    def addArc(self, oval: _Rect, startAngleDeg: float, sweepAngleDeg: float) -> PathBuilder: ...
    def addCircle(
        self, center_x: float, center_y: float, radius: float, dir: PathDirection = PathDirection.kCW
    ) -> PathBuilder: ...
    @typing.overload
    def addOval(self, oval: _Rect, dir: PathDirection, index: int) -> PathBuilder: ...
    @typing.overload
    def addOval(self, rect: _Rect, dir: PathDirection = PathDirection.kCW) -> PathBuilder: ...
    def addPath(self, src: Path) -> PathBuilder: ...
    def addPolygon(self, pts: list[_Point], isClosed: bool) -> PathBuilder: ...
    @typing.overload
    def addRRect(self, rrect: RRect, dir: PathDirection = PathDirection.kCW) -> PathBuilder: ...
    @typing.overload
    def addRRect(self, rrect: RRect, dir: PathDirection, index: int) -> PathBuilder: ...
    @typing.overload
    def addRect(self, rect: _Rect, dir: PathDirection = PathDirection.kCW) -> PathBuilder: ...
    @typing.overload
    def addRect(self, rect: _Rect, dir: PathDirection, index: int) -> PathBuilder: ...
    @typing.overload
    def arcTo(self, oval: _Rect, startAngleDeg: float, sweepAngleDeg: float, forceMoveTo: bool) -> PathBuilder: ...
    @typing.overload
    def arcTo(self, p1: _Point, p2: _Point, radius: float) -> PathBuilder: ...
    @typing.overload
    def arcTo(
        self, r: _Point, xAxisRotate: float, largeArc: PathBuilder.ArcSize, sweep: PathDirection, xy: Point
    ) -> PathBuilder: ...
    def close(self) -> PathBuilder: ...
    def computeBounds(self) -> Rect: ...
    @typing.overload
    def conicTo(self, pt1: _Point, pt2: _Point, w: float) -> PathBuilder: ...
    @typing.overload
    def conicTo(self, pts: list[_Point], w: float) -> PathBuilder: ...
    @typing.overload
    def conicTo(self, x1: float, y1: float, x2: float, y2: float, w: float) -> PathBuilder: ...
    @typing.overload
    def cubicTo(self, pt1: _Point, pt2: _Point, pt3: _Point) -> PathBuilder: ...
    @typing.overload
    def cubicTo(self, pts: list[_Point]) -> PathBuilder: ...
    @typing.overload
    def cubicTo(self, x1: float, y1: float, x2: float, y2: float, x3: float, y3: float) -> PathBuilder: ...
    def detach(self) -> Path: ...
    def fillType(self) -> PathFillType: ...
    @typing.overload
    def incReserve(self, extraPtCount: int) -> None: ...
    @typing.overload
    def incReserve(self, extraPtCount: int, extraVerbCount: int) -> None: ...
    @typing.overload
    def lineTo(self, pt: _Point) -> PathBuilder: ...
    @typing.overload
    def lineTo(self, x: float, y: float) -> PathBuilder: ...
    @typing.overload
    def moveTo(self, pt: _Point) -> PathBuilder: ...
    @typing.overload
    def moveTo(self, x: float, y: float) -> PathBuilder: ...
    def offset(self, dx: float, dy: float) -> PathBuilder: ...
    def polylineTo(self, pts: list[_Point]) -> PathBuilder:
        """
        Append a series of line segments to the path between adjacent points in the list.
        """
    @typing.overload
    def quadTo(self, pt1: _Point, pt2: _Point) -> PathBuilder: ...
    @typing.overload
    def quadTo(self, pts: list[_Point]) -> PathBuilder: ...
    @typing.overload
    def quadTo(self, x1: float, y1: float, x2: float, y2: float) -> PathBuilder: ...
    @typing.overload
    def rConicTo(self, pt1: _Point, pt2: _Point, w: float) -> PathBuilder: ...
    @typing.overload
    def rConicTo(self, x1: float, y1: float, x2: float, y2: float, w: float) -> PathBuilder: ...
    @typing.overload
    def rCubicTo(self, pt1: _Point, pt2: _Point, pt3: _Point) -> PathBuilder: ...
    @typing.overload
    def rCubicTo(self, x1: float, y1: float, x2: float, y2: float, x3: float, y3: float) -> PathBuilder: ...
    @typing.overload
    def rLineTo(self, pt: _Point) -> PathBuilder: ...
    @typing.overload
    def rLineTo(self, x: float, y: float) -> PathBuilder: ...
    @typing.overload
    def rQuadTo(self, pt1: _Point, pt2: _Point) -> PathBuilder: ...
    @typing.overload
    def rQuadTo(self, x1: float, y1: float, x2: float, y2: float) -> PathBuilder: ...
    def reset(self) -> PathBuilder: ...
    def setFillType(self, ft: PathFillType) -> PathBuilder: ...
    def setIsVolatile(self, isVolatile: bool) -> PathBuilder: ...
    def snapshot(self) -> Path: ...
    def toggleInverseFillType(self) -> PathBuilder: ...
    pass

class PathDirection:
    """
    Members:

      kCW

      kCCW
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
    __members__: dict  # value = {'kCW': <PathDirection.kCW: 0>, 'kCCW': <PathDirection.kCCW: 1>}
    kCCW: animator.skia.PathDirection  # value = <PathDirection.kCCW: 1>
    kCW: animator.skia.PathDirection  # value = <PathDirection.kCW: 0>
    pass

class PathEffect(Flattenable):
    class DashInfo:
        """
        Contains information about a dash pattern. This also contains an extra field ``fType`` for the dash type.
        """

        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, intervals: list, phase: float) -> None:
            """
            Create a DashInfo from a list of intervals and a phase.
            """
        def __str__(self) -> str: ...
        @property
        def fCount(self) -> int:
            """
            :type: int
            """
        @property
        def fIntervals(self) -> list[float]:
            """
            :type: list[float]
            """
        @property
        def fPhase(self) -> float:
            """
            :type: float
            """
        @property
        def fType(self) -> PathEffect.DashType:
            """
            The :py:class:`skia.PathEffect.DashType` of this dash.

            :type: PathEffect.DashType
            """

    class DashType:
        """
        Members:

          kNone_DashType

          kDash_DashType
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
        __members__: dict  # value = {'kNone_DashType': <DashType.kNone_DashType: 0>, 'kDash_DashType': <DashType.kDash_DashType: 1>}
        kDash_DashType: animator.skia.PathEffect.DashType  # value = <DashType.kDash_DashType: 1>
        kNone_DashType: animator.skia.PathEffect.DashType  # value = <DashType.kNone_DashType: 0>
        pass
    @staticmethod
    def Deserialize(data: buffer) -> PathEffect: ...
    @staticmethod
    def GetFlattenableType() -> Flattenable.Type: ...
    @staticmethod
    def MakeCompose(outer: PathEffect, inner: PathEffect) -> PathEffect: ...
    @staticmethod
    def MakeSum(first: PathEffect, second: PathEffect) -> PathEffect: ...
    def asADash(self) -> PathEffect.DashInfo:
        """
        Return a :py:class:`skia.PathEffect.DashInfo` object with the dash information. The returned object also
        contains an extra field ``fType`` for the dash type.
        """
    def filterPath(self, src: Path, rec: StrokeRec, cullR: _Rect = ..., ctm: Matrix = ...) -> Path | None:
        """
        Given a *src* path (input) and a stroke-*rec* (input and output), apply this effect to the *src* path,
        returning the new path.
        """
    def needsCTM(self) -> bool: ...
    pass

class PathFillType:
    """
    Members:

      kWinding

      kEvenOdd

      kInverseWinding

      kInverseEvenOdd
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
    def convertToNonInverse(self) -> PathFillType: ...
    def isEvenOdd(self) -> bool: ...
    def isInverse(self) -> bool: ...
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
    __members__: dict  # value = {'kWinding': <PathFillType.kWinding: 0>, 'kEvenOdd': <PathFillType.kEvenOdd: 1>, 'kInverseWinding': <PathFillType.kInverseWinding: 2>, 'kInverseEvenOdd': <PathFillType.kInverseEvenOdd: 3>}
    kEvenOdd: animator.skia.PathFillType  # value = <PathFillType.kEvenOdd: 1>
    kInverseEvenOdd: animator.skia.PathFillType  # value = <PathFillType.kInverseEvenOdd: 3>
    kInverseWinding: animator.skia.PathFillType  # value = <PathFillType.kInverseWinding: 2>
    kWinding: animator.skia.PathFillType  # value = <PathFillType.kWinding: 0>
    pass

class PathMeasure:
    class MatrixFlags(IntEnum):
        """
        Members:

          kGetPosition_MatrixFlag

          kGetTangent_MatrixFlag

          kGetPosAndTan_MatrixFlag
        """

        def __and__(self, other: object) -> object: ...
        def __eq__(self, other: object) -> bool: ...
        def __ge__(self, other: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __gt__(self, other: object) -> bool: ...
        def __hash__(self) -> int: ...
        def __index__(self) -> int: ...
        def __init__(self, value: int) -> None: ...
        def __int__(self) -> int: ...
        def __invert__(self) -> object: ...
        def __le__(self, other: object) -> bool: ...
        def __lt__(self, other: object) -> bool: ...
        def __ne__(self, other: object) -> bool: ...
        def __or__(self, other: object) -> object: ...
        def __rand__(self, other: object) -> object: ...
        def __repr__(self) -> str: ...
        def __ror__(self, other: object) -> object: ...
        def __rxor__(self, other: object) -> object: ...
        def __setstate__(self, state: int) -> None: ...
        def __xor__(self, other: object) -> object: ...
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
        __members__: dict  # value = {'kGetPosition_MatrixFlag': <MatrixFlags.kGetPosition_MatrixFlag: 1>, 'kGetTangent_MatrixFlag': <MatrixFlags.kGetTangent_MatrixFlag: 2>, 'kGetPosAndTan_MatrixFlag': <MatrixFlags.kGetPosAndTan_MatrixFlag: 3>}
        kGetPosAndTan_MatrixFlag: animator.skia.PathMeasure.MatrixFlags  # value = <MatrixFlags.kGetPosAndTan_MatrixFlag: 3>
        kGetPosition_MatrixFlag: animator.skia.PathMeasure.MatrixFlags  # value = <MatrixFlags.kGetPosition_MatrixFlag: 1>
        kGetTangent_MatrixFlag: animator.skia.PathMeasure.MatrixFlags  # value = <MatrixFlags.kGetTangent_MatrixFlag: 2>
        pass
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, path: Path, forceClosed: bool = False, resScale: float = 1) -> None: ...
    def getLength(self) -> float: ...
    def getMatrix(
        self, distance: float, flags: PathMeasure.MatrixFlags = MatrixFlags.kGetPosAndTan_MatrixFlag
    ) -> Matrix:
        """
        Pins *distance* to 0 <= distance <= getLength(), and returns the corresponding matrix (by calling
        getPosTan).
        """
    def getPosTan(self, distance: float) -> tuple:
        """
        Pins *distance* to 0 <= distance <= getLength(), and returns the corresponding position and tangent.
        """
    def getSegment(self, startD: float, stopD: float, startWithMoveTo: bool = True) -> Path:
        """
        Given a start and stop distance, return the intervening segment(s).
        """
    def isClosed(self) -> bool: ...
    def nextContour(self) -> bool: ...
    def setPath(self, path: Path, forceClosed: bool = False) -> None: ...
    pass

class PathOp:
    """
    Members:

      kDifference_PathOp

      kIntersect_PathOp

      kUnion_PathOp

      kXOR_PathOp

      kReverseDifference_PathOp
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
    __members__: dict  # value = {'kDifference_PathOp': <PathOp.kDifference_PathOp: 0>, 'kIntersect_PathOp': <PathOp.kIntersect_PathOp: 1>, 'kUnion_PathOp': <PathOp.kUnion_PathOp: 2>, 'kXOR_PathOp': <PathOp.kXOR_PathOp: 3>, 'kReverseDifference_PathOp': <PathOp.kReverseDifference_PathOp: 4>}
    kDifference_PathOp: animator.skia.PathOp  # value = <PathOp.kDifference_PathOp: 0>
    kIntersect_PathOp: animator.skia.PathOp  # value = <PathOp.kIntersect_PathOp: 1>
    kReverseDifference_PathOp: animator.skia.PathOp  # value = <PathOp.kReverseDifference_PathOp: 4>
    kUnion_PathOp: animator.skia.PathOp  # value = <PathOp.kUnion_PathOp: 2>
    kXOR_PathOp: animator.skia.PathOp  # value = <PathOp.kXOR_PathOp: 3>
    pass

class PathSegmentMask(IntEnum):
    """
    Members:

      kLine_PathSegmentMask

      kQuad_PathSegmentMask

      kConic_PathSegmentMask

      kCubic_PathSegmentMask
    """

    def __and__(self, other: object) -> object: ...
    def __eq__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __gt__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __invert__(self) -> object: ...
    def __le__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __or__(self, other: object) -> object: ...
    def __rand__(self, other: object) -> object: ...
    def __repr__(self) -> str: ...
    def __ror__(self, other: object) -> object: ...
    def __rxor__(self, other: object) -> object: ...
    def __setstate__(self, state: int) -> None: ...
    def __xor__(self, other: object) -> object: ...
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
    __members__: dict  # value = {'kLine_PathSegmentMask': <PathSegmentMask.kLine_PathSegmentMask: 1>, 'kQuad_PathSegmentMask': <PathSegmentMask.kQuad_PathSegmentMask: 2>, 'kConic_PathSegmentMask': <PathSegmentMask.kConic_PathSegmentMask: 4>, 'kCubic_PathSegmentMask': <PathSegmentMask.kCubic_PathSegmentMask: 8>}
    kConic_PathSegmentMask: animator.skia.PathSegmentMask  # value = <PathSegmentMask.kConic_PathSegmentMask: 4>
    kCubic_PathSegmentMask: animator.skia.PathSegmentMask  # value = <PathSegmentMask.kCubic_PathSegmentMask: 8>
    kLine_PathSegmentMask: animator.skia.PathSegmentMask  # value = <PathSegmentMask.kLine_PathSegmentMask: 1>
    kQuad_PathSegmentMask: animator.skia.PathSegmentMask  # value = <PathSegmentMask.kQuad_PathSegmentMask: 2>
    pass

class PathVerb:
    """
    Members:

      kMove

      kLine

      kQuad

      kConic

      kCubic

      kClose
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
    __members__: dict  # value = {'kMove': <PathVerb.kMove: 0>, 'kLine': <PathVerb.kLine: 1>, 'kQuad': <PathVerb.kQuad: 2>, 'kConic': <PathVerb.kConic: 3>, 'kCubic': <PathVerb.kCubic: 4>, 'kClose': <PathVerb.kClose: 5>}
    kClose: animator.skia.PathVerb  # value = <PathVerb.kClose: 5>
    kConic: animator.skia.PathVerb  # value = <PathVerb.kConic: 3>
    kCubic: animator.skia.PathVerb  # value = <PathVerb.kCubic: 4>
    kLine: animator.skia.PathVerb  # value = <PathVerb.kLine: 1>
    kMove: animator.skia.PathVerb  # value = <PathVerb.kMove: 0>
    kQuad: animator.skia.PathVerb  # value = <PathVerb.kQuad: 2>
    pass

class Picture:
    @staticmethod
    @typing.overload
    def MakeFromData(data: Data) -> Picture:
        """
        Recreates :py:class:`Picture` that was serialized into data.
        """
    @staticmethod
    @typing.overload
    def MakeFromData(data: buffer) -> Picture: ...
    @staticmethod
    def MakePlaceholder(cull: _Rect) -> Picture: ...
    def __init__(self, cull: _Rect) -> None:
        """
        Returns a placeholder :py:class:`Picture` of the specified dimensions *cull*.
        """
    def approximateBytesUsed(self) -> int: ...
    def approximateOpCount(self, nested: bool = False) -> int: ...
    def cullRect(self) -> Rect: ...
    def makeShader(
        self,
        tmx: TileMode,
        tmy: TileMode,
        mode: FilterMode,
        localMatrix: Matrix | None = None,
        tileRect: _Rect | None = None,
    ) -> Shader: ...
    def playback(self, canvas: Canvas) -> None:
        """
        Replays the drawing commands on the specified canvas.
        """
    def serialize(self) -> Data:
        """
        Returns storage containing :py:class:`Data` describing :py:class:`Picture`.
        """
    def uniqueID(self) -> int: ...
    pass

class PixelGeometry:
    """
    Members:

      kUnknown_PixelGeometry

      kRGB_H_PixelGeometry

      kBGR_H_PixelGeometry

      kRGB_V_PixelGeometry

      kBGR_V_PixelGeometry
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
    def pixelGeometryIsBGR(self) -> bool: ...
    def pixelGeometryIsH(self) -> bool: ...
    def pixelGeometryIsRGB(self) -> bool: ...
    def pixelGeometryIsV(self) -> bool: ...
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
    __members__: dict  # value = {'kUnknown_PixelGeometry': <PixelGeometry.kUnknown_PixelGeometry: 0>, 'kRGB_H_PixelGeometry': <PixelGeometry.kRGB_H_PixelGeometry: 1>, 'kBGR_H_PixelGeometry': <PixelGeometry.kBGR_H_PixelGeometry: 2>, 'kRGB_V_PixelGeometry': <PixelGeometry.kRGB_V_PixelGeometry: 3>, 'kBGR_V_PixelGeometry': <PixelGeometry.kBGR_V_PixelGeometry: 4>}
    kBGR_H_PixelGeometry: animator.skia.PixelGeometry  # value = <PixelGeometry.kBGR_H_PixelGeometry: 2>
    kBGR_V_PixelGeometry: animator.skia.PixelGeometry  # value = <PixelGeometry.kBGR_V_PixelGeometry: 4>
    kRGB_H_PixelGeometry: animator.skia.PixelGeometry  # value = <PixelGeometry.kRGB_H_PixelGeometry: 1>
    kRGB_V_PixelGeometry: animator.skia.PixelGeometry  # value = <PixelGeometry.kRGB_V_PixelGeometry: 3>
    kUnknown_PixelGeometry: animator.skia.PixelGeometry  # value = <PixelGeometry.kUnknown_PixelGeometry: 0>
    pass

class Pixmap:
    """
    :py:class:`Pixmap` provides a utility to pair :py:class:`ImageInfo` with pixels and row bytes. The buffer
    protocol is supported. It is possible to mount :py:class:`Pixmap` as array::

        array = np.array(pixmap, copy=False)

    Or mount array as :py:class:`Pixmap` with :py:class:`ImageInfo`::

        buffer = np.zeros((100, 100, 4), np.uint8)
        array = skia.Pixmap(skia.ImageInfo.MakeN32Premul(100, 100), buffer)
    """

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(
        self,
        array: numpy.ndarray,
        colorType: ColorType = ColorType.kRGBA_8888_ColorType,
        alphaType: AlphaType = AlphaType.kUnpremul_AlphaType,
        colorSpace: ColorSpace | None = None,
    ) -> None:
        """
        Creates :py:class:`Pixmap` backed by numpy array.
        """
    @typing.overload
    def __init__(self, info: ImageInfo, addr: buffer | None, rowBytes: int = 0) -> None:
        """
        Creates :py:class:`Pixmap` from info width, height, :py:class:`AlphaType`, and :py:class:`ColorType`,
        and a buffer *addr*.
        """
    def __str__(self) -> str: ...
    def addr(self) -> memoryview:
        """
        Returns the pixels as a ``memoryview``.
        """
    def addr16(self) -> memoryview: ...
    def addr32(self) -> memoryview: ...
    def addr64(self) -> memoryview: ...
    def addr8(self) -> memoryview: ...
    def addrF16(self) -> memoryview: ...
    def alphaType(self) -> AlphaType: ...
    def bounds(self) -> IRect: ...
    def colorSpace(self) -> ColorSpace: ...
    def colorType(self) -> ColorType: ...
    def computeByteSize(self) -> int: ...
    def computeIsOpaque(self) -> bool: ...
    def dimensions(self) -> ISize: ...
    @typing.overload
    def erase(self, color: _Color4f, subset: _IRect | None = None) -> bool: ...
    @typing.overload
    def erase(self, color: _Color) -> bool: ...
    @typing.overload
    def erase(self, color: _Color, subset: _IRect) -> bool: ...
    def extractSubset(self, area: _IRect) -> Pixmap:
        """
        Returns a new :py:class:`Pixmap` with subset of the original :py:class:`Pixmap` specified by *area*.
        """
    def getAlphaf(self, x: int, y: int) -> float: ...
    def getColor(self, x: int, y: int) -> int: ...
    def getColor4f(self, x: int, y: int) -> Color4f: ...
    def height(self) -> int: ...
    def info(self) -> ImageInfo: ...
    def isOpaque(self) -> bool: ...
    @typing.overload
    def readPixels(self, dst: Pixmap, srcX: int = 0, srcY: int = 0) -> bool: ...
    @typing.overload
    def readPixels(
        self, dstInfo: ImageInfo, dstPixels: buffer, dstRowBytes: int = 0, srcX: int = 0, srcY: int = 0
    ) -> bool:
        """
        Copies *dstInfo* pixels starting from (*srcX*, *srcY*) to *dstPixels* buffer.
        """
    def refColorSpace(self) -> ColorSpace: ...
    @typing.overload
    def reset(self) -> None: ...
    @typing.overload
    def reset(self, info: ImageInfo, addr: buffer | None, rowBytes: int = 0) -> None:
        """
        Sets width, height, :py:class:`AlphaType`, and :py:class:`ColorType` from info, and a buffer *addr*.
        """
    def rowBytes(self) -> int: ...
    def rowBytesAsPixels(self) -> int: ...
    def scalePixels(self, dst: Pixmap, sampling: SamplingOptions) -> bool: ...
    def setColorSpace(self, colorSpace: ColorSpace) -> None: ...
    def shiftPerPixel(self) -> int: ...
    def tobytes(self) -> bytes:
        """
        Convert :py:class:`Pixmap` to bytes.
        """
    def width(self) -> int: ...
    def writable_addr(self) -> memoryview: ...
    pass

class Point:
    @staticmethod
    def CrossProduct(a: _Point, b: _Point) -> float: ...
    @staticmethod
    def Distance(a: _Point, b: _Point) -> float: ...
    @staticmethod
    def DotProduct(a: _Point, b: _Point) -> float: ...
    @staticmethod
    def Length(x: float, y: float) -> float: ...
    @staticmethod
    def Make(x: float, y: float) -> Point: ...
    @staticmethod
    def Normalize(vec: _Point) -> float: ...
    @staticmethod
    @typing.overload
    def Offset(points: typing.Sequence[_Point], dx: float, dy: float) -> list[Point]: ...
    @staticmethod
    @typing.overload
    def Offset(points: typing.Sequence[_Point], offset: _Point) -> list[Point]: ...
    def __add__(self, other: _Point) -> Point: ...
    def __eq__(self, other: _Point) -> bool: ...
    def __iadd__(self, other: _Point) -> None: ...
    def __imul__(self, scale: float) -> Point: ...
    @typing.overload
    def __init__(self, ipoint: IPoint) -> None:
        """
        Create a :py:class:`Point` from an :py:class:`IPoint`.

        :param t: :py:class:`IPoint` to convert.
        """
    @typing.overload
    def __init__(self, t: tuple[float, float]) -> None:
        """
        Create a :py:class:`Point` from a tuple of two floats.

        :param t: Tuple of two floats.
        """
    @typing.overload
    def __init__(self, x: float, y: float) -> None: ...
    def __isub__(self, other: _Point) -> None: ...
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    def __mul__(self, scale: float) -> Point: ...
    def __ne__(self, other: _Point) -> bool: ...
    def __neg__(self) -> Point: ...
    def __str__(self) -> str: ...
    def __sub__(self, other: _Point) -> Point: ...
    def cross(self, vec: _Point) -> float: ...
    def distanceToOrigin(self) -> float: ...
    def dot(self, vec: _Point) -> float: ...
    def equals(self, x: float, y: float) -> bool: ...
    def isFinite(self) -> bool: ...
    def isZero(self) -> bool: ...
    @typing.overload
    def iset(self, p: IPoint) -> None: ...
    @typing.overload
    def iset(self, x: int, y: int) -> None: ...
    def length(self) -> float: ...
    def makeScaled(self, scale: float) -> Point:
        """
        Return a new point that is the result of scaling this point by the given *scale*.

        :param scale: factor to multiply :py:class:`Point` by
        :return: a new :py:class:`Point` scaled by *scale*
        """
    def negate(self) -> None: ...
    def normalize(self) -> bool: ...
    def offset(self, dx: float, dy: float) -> None: ...
    def scale(self, scale: float) -> None: ...
    def set(self, x: float, y: float) -> None: ...
    def setAbs(self, pt: _Point) -> None: ...
    @typing.overload
    def setLength(self, length: float) -> bool: ...
    @typing.overload
    def setLength(self, x: float, y: float, length: float) -> bool: ...
    def setNormalize(self, x: float, y: float) -> bool: ...
    def x(self) -> float: ...
    def y(self) -> float: ...
    @property
    def fX(self) -> float:
        """
        :type: float
        """
    @fX.setter
    def fX(self, arg0: float) -> None:
        pass
    @property
    def fY(self) -> float:
        """
        :type: float
        """
    @fY.setter
    def fY(self, arg0: float) -> None:
        pass
    pass

_Point = Point | tuple[float, float]

class Point3:
    @staticmethod
    def CrossProduct(a: _Point3, b: _Point3) -> Point3: ...
    @staticmethod
    def DotProduct(a: _Point3, b: _Point3) -> float: ...
    @staticmethod
    def Length(x: float, y: float, z: float) -> float: ...
    @staticmethod
    def Make(x: float, y: float, z: float) -> Point3: ...
    def __add__(self, other: _Point3) -> Point3: ...
    def __eq__(self, other: _Point3) -> bool: ...
    def __iadd__(self, other: _Point3) -> None: ...
    @typing.overload
    def __init__(self, t: tuple) -> None: ...
    @typing.overload
    def __init__(self, x: float, y: float, z: float) -> None: ...
    def __isub__(self, other: _Point3) -> None: ...
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    def __ne__(self, other: _Point3) -> bool: ...
    def __neg__(self) -> Point3: ...
    def __rmul__(self, t: float) -> Point3: ...
    def __str__(self) -> str: ...
    def __sub__(self, other: _Point3) -> Point3: ...
    def cross(self, vec: _Point3) -> Point3: ...
    def dot(self, vec: _Point3) -> float: ...
    def isFinite(self) -> bool: ...
    def length(self) -> float: ...
    def makeScale(self, scale: float) -> Point3: ...
    def normalize(self) -> bool: ...
    def scale(self, value: float) -> None: ...
    def set(self, x: float, y: float, z: float) -> None: ...
    def x(self) -> float: ...
    def y(self) -> float: ...
    def z(self) -> float: ...
    @property
    def fX(self) -> float:
        """
        :type: float
        """
    @fX.setter
    def fX(self, arg0: float) -> None:
        pass
    @property
    def fY(self) -> float:
        """
        :type: float
        """
    @fY.setter
    def fY(self, arg0: float) -> None:
        pass
    @property
    def fZ(self) -> float:
        """
        :type: float
        """
    @fZ.setter
    def fZ(self, arg0: float) -> None:
        pass
    pass

_Point3 = Point3 | tuple[float, float, float]

class RRect:
    class Corner:
        """
        Members:

          kUpperLeft_Corner

          kUpperRight_Corner

          kLowerRight_Corner

          kLowerLeft_Corner
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
        __members__: dict  # value = {'kUpperLeft_Corner': <Corner.kUpperLeft_Corner: 0>, 'kUpperRight_Corner': <Corner.kUpperRight_Corner: 1>, 'kLowerRight_Corner': <Corner.kLowerRight_Corner: 2>, 'kLowerLeft_Corner': <Corner.kLowerLeft_Corner: 3>}
        kLowerLeft_Corner: animator.skia.RRect.Corner  # value = <Corner.kLowerLeft_Corner: 3>
        kLowerRight_Corner: animator.skia.RRect.Corner  # value = <Corner.kLowerRight_Corner: 2>
        kUpperLeft_Corner: animator.skia.RRect.Corner  # value = <Corner.kUpperLeft_Corner: 0>
        kUpperRight_Corner: animator.skia.RRect.Corner  # value = <Corner.kUpperRight_Corner: 1>
        pass

    class Type:
        """
        Members:

          kEmpty_Type

          kRect_Type

          kOval_Type

          kSimple_Type

          kNinePatch_Type

          kComplex_Type

          kLastType
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
        __members__: dict  # value = {'kEmpty_Type': <Type.kEmpty_Type: 0>, 'kRect_Type': <Type.kRect_Type: 1>, 'kOval_Type': <Type.kOval_Type: 2>, 'kSimple_Type': <Type.kSimple_Type: 3>, 'kNinePatch_Type': <Type.kNinePatch_Type: 4>, 'kComplex_Type': <Type.kComplex_Type: 5>, 'kLastType': <Type.kComplex_Type: 5>}
        kComplex_Type: animator.skia.RRect.Type  # value = <Type.kComplex_Type: 5>
        kEmpty_Type: animator.skia.RRect.Type  # value = <Type.kEmpty_Type: 0>
        kLastType: animator.skia.RRect.Type  # value = <Type.kComplex_Type: 5>
        kNinePatch_Type: animator.skia.RRect.Type  # value = <Type.kNinePatch_Type: 4>
        kOval_Type: animator.skia.RRect.Type  # value = <Type.kOval_Type: 2>
        kRect_Type: animator.skia.RRect.Type  # value = <Type.kRect_Type: 1>
        kSimple_Type: animator.skia.RRect.Type  # value = <Type.kSimple_Type: 3>
        pass
    @staticmethod
    def MakeEmpty() -> RRect: ...
    @staticmethod
    def MakeOval(oval: _Rect) -> RRect: ...
    @staticmethod
    def MakeRect(rect: _Rect) -> RRect: ...
    @staticmethod
    def MakeRectXY(rect: _Rect, xRad: float, yRad: float) -> RRect: ...
    def __contains__(self, rect: _Rect) -> bool:
        """
        Same as :py:meth:`RRect.contains`.
        """
    def __eq__(self, arg0: RRect) -> bool: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, rect: _Rect, xRad: float, yRad: float) -> None: ...
    @typing.overload
    def __init__(self, rrect: RRect) -> None: ...
    def __ne__(self, arg0: RRect) -> bool: ...
    def __str__(self) -> str: ...
    def contains(self, rect: _Rect) -> bool: ...
    def dump(self, asHex: bool = False) -> None: ...
    def getBounds(self) -> Rect: ...
    def getSimpleRadii(self) -> Point: ...
    def getType(self) -> RRect.Type: ...
    def height(self) -> float: ...
    def inset(self, dx: float, dy: float) -> None: ...
    def isComplex(self) -> bool: ...
    def isEmpty(self) -> bool: ...
    def isNinePatch(self) -> bool: ...
    def isOval(self) -> bool: ...
    def isRect(self) -> bool: ...
    def isSimple(self) -> bool: ...
    def isValid(self) -> bool: ...
    def makeInset(self, dx: float, dy: float) -> RRect:
        """
        Copies :py:class:`RRect`, then insets bounds by *dx* and *dy*, and adjusts radii by *dx* and *dy*.

        :param dx: added to rect().fLeft, and subtracted from rect().fRight
        :param dy: added to rect().fTop, and subtracted from rect().fBottom
        :return: insets bounds and radii
        """
    def makeOffset(self, dx: float, dy: float) -> RRect: ...
    def makeOutset(self, dx: float, dy: float) -> RRect:
        """
        Outsets bounds by *dx* and *dy*, and adjusts radii by *dx* and *dy*.

        :param dx: subtracted from rect().fLeft, and added to rect().fRight
        :param dy: subtracted from rect().fTop, and added to rect().fBottom
        :return: outset bounds and radii
        """
    def offset(self, dx: float, dy: float) -> None: ...
    def outset(self, dx: float, dy: float) -> None: ...
    def radii(self, corner: RRect.Corner) -> Point: ...
    def readFromMemory(self, buffer: Data) -> int:
        """
        Reads :py:class:`RRect` from given :py:class:`Data`.
        """
    def rect(self) -> Rect: ...
    def setEmpty(self) -> None: ...
    def setNinePatch(self, rect: _Rect, leftRad: float, topRad: float, rightRad: float, bottomRad: float) -> None: ...
    def setOval(self, oval: _Rect) -> None: ...
    def setRect(self, rect: _Rect) -> None: ...
    def setRectRadii(self, rect: _Rect, radii: list[_Point]) -> None: ...
    def setRectXY(self, rect: _Rect, xRad: float, yRad: float) -> None: ...
    def transform(self, matrix: Matrix) -> RRect | None:
        """
        Transforms the :py:class:`RRect` by matrix, returning result. Returns the transformed :py:class:`RRect`
        if the transformation can be represented by another :py:class:`RRect`. Returns ``None`` if matrix
        contains transformations that are not axis aligned.

        :param matrix: :py:class:`Matrix` specifying the transform
        :return: transformed :py:class:`RRect` or ``None``
        :rtype: :py:class:`RRect` | None
        """
    def type(self) -> RRect.Type: ...
    def width(self) -> float: ...
    def writeToMemory(self) -> Data:
        """
        Writes :py:class:`RRect` to :py:class:`Data` and returns it.
        """
    kSizeInMemory = 48
    pass

class RSXform:
    @staticmethod
    def Make(scos: float, ssin: float, tx: float, ty: float) -> RSXform: ...
    @staticmethod
    def MakeFromRadians(scale: float, radians: float, tx: float, ty: float, ax: float, ay: float) -> RSXform: ...
    def __init__(self, scos: float, ssin: float, tx: float, ty: float) -> None: ...
    def __str__(self) -> str: ...
    def rectStaysRect(self) -> bool: ...
    def set(self, scos: float, ssin: float, tx: float, ty: float) -> None: ...
    def setIdentity(self) -> None: ...
    @typing.overload
    def toQuad(self, size: Size) -> list[Point]:
        """
        Maps a rectangle with the given *size* with this :py:class:`RSXform` and returns a list of 4 points, the
        corners of the resulting quadrilateral.

        :param size: The size of the rectangle.
        :return: A list of 4 points, the corners of the resulting quadrilateral.
        """
    @typing.overload
    def toQuad(self, width: float, height: float) -> list[Point]:
        """
        Maps a rectangle with the given *width* and *height* with this :py:class:`RSXform` and returns a list of
        4 points, the corners of the resulting quadrilateral.

        :param width: The width of the rectangle.
        :param height: The height of the rectangle.
        :return: A list of 4 points, the corners of the resulting quadrilateral.
        """
    def toTriStrip(self, width: float, height: float) -> list[Point]:
        """
        Returns a list of 4 points, the corners of the resulting strip.
        """
    @property
    def fSCos(self) -> float:
        """
        :type: float
        """
    @fSCos.setter
    def fSCos(self, arg0: float) -> None:
        pass
    @property
    def fSSin(self) -> float:
        """
        :type: float
        """
    @fSSin.setter
    def fSSin(self, arg0: float) -> None:
        pass
    @property
    def fTx(self) -> float:
        """
        :type: float
        """
    @fTx.setter
    def fTx(self, arg0: float) -> None:
        pass
    @property
    def fTy(self) -> float:
        """
        :type: float
        """
    @fTy.setter
    def fTy(self, arg0: float) -> None:
        pass
    pass

class Rect:
    @staticmethod
    def Intersects(a: _Rect, b: _Rect) -> bool: ...
    @staticmethod
    @typing.overload
    def Make(irect: _IRect) -> Rect: ...
    @staticmethod
    @typing.overload
    def Make(size: _ISize) -> Rect: ...
    @staticmethod
    def MakeEmpty() -> Rect: ...
    @staticmethod
    def MakeIWH(w: int, h: int) -> Rect: ...
    @staticmethod
    def MakeLTRB(l: float, t: float, r: float, b: float) -> Rect: ...
    @staticmethod
    def MakeSize(size: Size) -> Rect: ...
    @staticmethod
    def MakeWH(w: float, h: float) -> Rect: ...
    @staticmethod
    def MakeXYWH(x: float, y: float, w: float, h: float) -> Rect: ...
    @typing.overload
    def __contains__(self, arg0: _IRect) -> bool: ...
    @typing.overload
    def __contains__(self, arg0: _Point) -> bool:
        """
        Returns ``True`` if :py:class:`Point` is inside :py:class:`Rect`.
        """
    @typing.overload
    def __contains__(self, arg0: _Rect) -> bool: ...
    def __eq__(self, other: _Rect) -> bool: ...
    @typing.overload
    def __init__(self) -> None:
        """
        Constructs a :py:class:`Rect` set to (0, 0, 0, 0). Many other rectangles are empty; if left is equal to
        or greater than right, or if top is equal to or greater than bottom. Setting all members to zero is a
        convenience, but does not designate a special empty rectangle.
        """
    @typing.overload
    def __init__(self, irect: _IRect) -> None:
        """
        Constructs a :py:class:`Rect` set to iRect, promoting integer to floats. Does not validate input; fLeft
        may be greater than fRight, fTop may be greater than fBottom.
        """
    @typing.overload
    def __init__(self, l: float, t: float, r: float, b: float) -> None:
        """
        Constructs a :py:class:`Rect` set to (l, t, r, b). Does not sort input; :py:class:`Rect` may result in
        fLeft greater than fRight, or fTop greater than fBottom.

        :param float l: stored in fLeft
        :param float t: stored in fTop
        :param float r: stored in fRight
        :param float b: stored in fBottom
        """
    @typing.overload
    def __init__(self, size: _ISize) -> None:
        """
        Constructs a :py:class:`Rect` set to (0, 0, size.width(), size.height()). Does not validate input;
        size.width() or size.height() may be negative.

        :param ISize size: values for :py:class:`Rect` width and height
        """
    @typing.overload
    def __init__(self, size: Size) -> None:
        """
        Constructs a :py:class:`Rect` set to (0, 0, size.width(), size.height()). Does not validate input;
        size.width() or size.height() may be negative.

        :param Size size: values for :py:class:`Rect` width and height
        """
    @typing.overload
    def __init__(self, t: tuple) -> None:
        """
        Create an :py:class:`Rect` from a tuple of 0, 2, or 4 floats.
        """
    @typing.overload
    def __init__(self, w: float, h: float) -> None:
        """
        Constructs a :py:class:`Rect` set to (0, 0, w, h). Does not validate input; w or h may be negative.

        :param float w: width of constructed :py:class:`Rect`
        :param float h: height of constructed :py:class:`Rect`
        """
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    def __ne__(self, other: _Rect) -> bool: ...
    def __str__(self) -> str: ...
    def asScalars(self) -> memoryview:
        """
        Returns a :py:class:`memoryview` of :py:class:`Scalar` containing the :py:class:`Rect`'s coordinates.
        """
    def bottom(self) -> float: ...
    def center(self) -> Point: ...
    def centerX(self) -> float: ...
    def centerY(self) -> float: ...
    @typing.overload
    def contains(self, r: _IRect) -> bool: ...
    @typing.overload
    def contains(self, r: _Rect) -> bool: ...
    @typing.overload
    def contains(self, x: float, y: float) -> bool: ...
    def dump(self, asHex: bool = False) -> None: ...
    def dumpHex(self) -> None: ...
    def height(self) -> float: ...
    def inset(self, dx: float, dy: float) -> None: ...
    @typing.overload
    def intersect(self, a: _Rect, b: _Rect) -> bool: ...
    @typing.overload
    def intersect(self, r: _Rect) -> bool: ...
    def intersects(self, r: _Rect) -> bool: ...
    def isEmpty(self) -> bool: ...
    def isFinite(self) -> bool: ...
    def isSorted(self) -> bool: ...
    def join(self, r: _Rect) -> None: ...
    def joinNonEmptyArg(self, r: _Rect) -> None: ...
    def joinPossiblyEmptyRect(self, r: _Rect) -> None: ...
    def left(self) -> float: ...
    def makeInset(self, dx: float, dy: float) -> Rect: ...
    @typing.overload
    def makeOffset(self, dx: float, dy: float) -> Rect: ...
    @typing.overload
    def makeOffset(self, v: _Point) -> Rect: ...
    def makeOutset(self, dx: float, dy: float) -> Rect: ...
    def makeSorted(self) -> Rect: ...
    @typing.overload
    def offset(self, delta: _Point) -> None: ...
    @typing.overload
    def offset(self, dx: float, dy: float) -> None: ...
    def offsetTo(self, newX: float, newY: float) -> None: ...
    def outset(self, dx: float, dy: float) -> None: ...
    def right(self) -> float: ...
    def round(self) -> IRect: ...
    def roundIn(self) -> IRect: ...
    def roundOut(self) -> IRect: ...
    @typing.overload
    def set(self, p0: _Point, p1: _Point) -> None: ...
    @typing.overload
    def set(self, src: _IRect) -> None: ...
    def setBounds(self, points: list[_Point]) -> None:
        """
        Sets to bounds of :py:class:`Point` list. If list is empty, or contains an infinity or NaN, sets to
        (0, 0, 0, 0). Result is either empty or sorted: fLeft is less than or equal to fRight, and fTop is less
        than or equal to fBottom.

        :param Point[] points: :py:class:`Point` array
        """
    def setBoundsCheck(self, points: list[_Point]) -> bool:
        """
        Same as :py:meth:`setBounds` but returns ``False`` if list is empty or contains an infinity or NaN.
        """
    def setBoundsNoCheck(self, points: list[_Point]) -> None:
        """
        Sets to bounds of :py:class:`Point` list. If any point is infinity or NaN, all :py:class:`Rect`
        dimensions are set to NaN.
        """
    def setEmpty(self) -> None: ...
    def setIWH(self, width: int, height: int) -> None: ...
    def setLTRB(self, left: float, top: float, right: float, bottom: float) -> None: ...
    def setWH(self, width: float, height: float) -> None: ...
    def setXYWH(self, x: float, y: float, width: float, height: float) -> None: ...
    def sort(self) -> None: ...
    def toQuad(self) -> list[Point]:
        """
        Returns four points in quad that enclose :py:class:`Rect` ordered as: top-left, top-right, bottom-right,
        bottom-left.

        :return: list of four :py:class:`Point` objects
        """
    def top(self) -> float: ...
    def width(self) -> float: ...
    def x(self) -> float: ...
    def y(self) -> float: ...
    @property
    def fBottom(self) -> float:
        """
        :type: float
        """
    @fBottom.setter
    def fBottom(self, arg0: float) -> None:
        pass
    @property
    def fLeft(self) -> float:
        """
        :type: float
        """
    @fLeft.setter
    def fLeft(self, arg0: float) -> None:
        pass
    @property
    def fRight(self) -> float:
        """
        :type: float
        """
    @fRight.setter
    def fRight(self, arg0: float) -> None:
        pass
    @property
    def fTop(self) -> float:
        """
        :type: float
        """
    @fTop.setter
    def fTop(self, arg0: float) -> None:
        pass
    pass

_Rect = Rect | tuple[()] | tuple[float, float] | tuple[float, float, float, float]

class Region:
    """
    :py:class:`Region` describes the set of pixels used to clip :py:class:`Canvas`.

    :py:class:`Region` supports a few operators::

        regionA == regionB  # Equality
        regionA != regionB  # Inequality

        regionA - regionB   # Difference
        regionA & regionB   # Intersect
        regionA | regionB   # Union
        regionA ^ regionB   # XOR

        regionA -= regionB  # In-place Difference
        regionA &= regionB  # In-place Intersect
        regionA |= regionB  # In-place Union
        regionA ^= regionB  # In-place XOR
    """

    class Cliperator:
        def __init__(self, region: Region, clip: _IRect) -> None: ...
        def __iter__(self) -> Region.Cliperator: ...
        def __next__(self) -> IRect: ...
        def done(self) -> bool: ...
        def next(self) -> None: ...
        def rect(self) -> IRect: ...
        pass

    class Iterator:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, region: Region) -> None: ...
        def __iter__(self) -> Region.Iterator: ...
        def __next__(self) -> IRect: ...
        def done(self) -> bool: ...
        def next(self) -> None: ...
        def rect(self) -> IRect: ...
        def reset(self, region: Region) -> None: ...
        def rewind(self) -> bool: ...
        def rgn(self) -> Region: ...
        pass

    class Op:
        """
        Members:

          kDifference_Op

          kIntersect_Op

          kUnion_Op

          kXOR_Op

          kReverseDifference_Op

          kReplace_Op

          kLastOp
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
        __members__: dict  # value = {'kDifference_Op': <Op.kDifference_Op: 0>, 'kIntersect_Op': <Op.kIntersect_Op: 1>, 'kUnion_Op': <Op.kUnion_Op: 2>, 'kXOR_Op': <Op.kXOR_Op: 3>, 'kReverseDifference_Op': <Op.kReverseDifference_Op: 4>, 'kReplace_Op': <Op.kReplace_Op: 5>, 'kLastOp': <Op.kReplace_Op: 5>}
        kDifference_Op: animator.skia.Region.Op  # value = <Op.kDifference_Op: 0>
        kIntersect_Op: animator.skia.Region.Op  # value = <Op.kIntersect_Op: 1>
        kLastOp: animator.skia.Region.Op  # value = <Op.kReplace_Op: 5>
        kReplace_Op: animator.skia.Region.Op  # value = <Op.kReplace_Op: 5>
        kReverseDifference_Op: animator.skia.Region.Op  # value = <Op.kReverseDifference_Op: 4>
        kUnion_Op: animator.skia.Region.Op  # value = <Op.kUnion_Op: 2>
        kXOR_Op: animator.skia.Region.Op  # value = <Op.kXOR_Op: 3>
        pass

    class Spanerator:
        def __init__(self, region: Region, y: int, left: int, right: int) -> None: ...
        def __iter__(self) -> Region.Spanerator: ...
        def __next__(self) -> tuple: ...
        def next(self) -> tuple | None:
            """
            Advances iterator to next span intersecting :py:class:`Region` within line segment provided in constructor.
            Returns ``None`` if no intervals were found.
            """
    @typing.overload
    def __and__(self, arg0: _IRect) -> Region: ...
    @typing.overload
    def __and__(self, arg0: Region) -> Region: ...
    @typing.overload
    def __contains__(self, arg0: _IRect) -> bool: ...
    @typing.overload
    def __contains__(self, arg0: Region) -> bool: ...
    @typing.overload
    def __contains__(self, point: tuple) -> bool:
        """
        Checks if *point* is inside :py:class:`Region`.
        """
    def __eq__(self, other: Region) -> bool: ...
    @typing.overload
    def __iand__(self, arg0: _IRect) -> Region: ...
    @typing.overload
    def __iand__(self, arg0: Region) -> Region: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, rect: _IRect) -> None: ...
    @typing.overload
    def __init__(self, region: Region) -> None: ...
    @typing.overload
    def __ior__(self, arg0: _IRect) -> Region: ...
    @typing.overload
    def __ior__(self, arg0: Region) -> Region: ...
    @typing.overload
    def __isub__(self, arg0: _IRect) -> Region: ...
    @typing.overload
    def __isub__(self, arg0: Region) -> Region: ...
    def __iter__(self) -> Region.Iterator: ...
    @typing.overload
    def __ixor__(self, arg0: _IRect) -> Region: ...
    @typing.overload
    def __ixor__(self, arg0: Region) -> Region: ...
    def __ne__(self, other: Region) -> bool: ...
    @typing.overload
    def __or__(self, arg0: _IRect) -> Region: ...
    @typing.overload
    def __or__(self, arg0: Region) -> Region: ...
    def __rand__(self, arg0: _IRect) -> Region: ...
    def __ror__(self, arg0: _IRect) -> Region: ...
    def __rsub__(self, arg0: _IRect) -> Region: ...
    def __rxor__(self, arg0: _IRect) -> Region: ...
    def __str__(self) -> str: ...
    @typing.overload
    def __sub__(self, arg0: _IRect) -> Region: ...
    @typing.overload
    def __sub__(self, arg0: Region) -> Region: ...
    @typing.overload
    def __xor__(self, arg0: _IRect) -> Region: ...
    @typing.overload
    def __xor__(self, arg0: Region) -> Region: ...
    def computeRegionComplexity(self) -> int: ...
    @typing.overload
    def contains(self, other: _IRect) -> bool: ...
    @typing.overload
    def contains(self, other: Region) -> bool: ...
    @typing.overload
    def contains(self, x: int, y: int) -> bool: ...
    def getBoundaryPath(self, path: Path) -> bool: ...
    def getBounds(self) -> IRect: ...
    @typing.overload
    def intersects(self, other: Region) -> bool: ...
    @typing.overload
    def intersects(self, rect: _IRect) -> bool: ...
    def isComplex(self) -> bool: ...
    def isEmpty(self) -> bool: ...
    def isRect(self) -> bool: ...
    def makeTranslate(self, dx: int, dy: int) -> Region:
        """
        Makes a copy of :py:class:`Region` translated by *dx* and *dy*.
        """
    @typing.overload
    def op(self, rect: _IRect, op: Region.Op) -> bool: ...
    @typing.overload
    def op(self, rect: _IRect, rgn: Region, op: Region.Op) -> bool: ...
    @typing.overload
    def op(self, rgn: Region, op: Region.Op) -> bool: ...
    @typing.overload
    def op(self, rgn: Region, rect: _IRect, op: Region.Op) -> bool: ...
    @typing.overload
    def op(self, rgna: Region, rgnb: Region, op: Region.Op) -> bool: ...
    def quickContains(self, r: _IRect) -> bool: ...
    @typing.overload
    def quickReject(self, rect: _IRect) -> bool: ...
    @typing.overload
    def quickReject(self, region: Region) -> bool: ...
    def readFromMemory(self, buffer: Data) -> int:
        """
        Reads :py:class:`Region` from given :py:class:`Data`.
        """
    def set(self, src: Region) -> bool: ...
    def setEmpty(self) -> bool: ...
    def setPath(self, path: Path, clip: Region) -> bool: ...
    def setRect(self, rect: _IRect) -> bool: ...
    def setRects(self, rects: list[_IRect]) -> bool:
        """
        Constructs :py:class:`Region` as the union of :py:class:`IRect` in *rects* array.
        """
    def setRegion(self, region: Region) -> bool: ...
    def swap(self, other: Region) -> None: ...
    def translate(self, dx: int, dy: int) -> None: ...
    def writeToMemory(self) -> Data:
        """
        Writes :py:class:`Region` to :py:class:`Data` and returns it.
        """
    kOpCnt = 6
    pass

class RuntimeEffectBuilder:
    class BuilderChild:
        def __str__(self) -> str: ...
        def set(self, val: Shader | ColorFilter | Blender | None) -> None:
            """
            Set the child to the given *val*.
            """

    class BuilderUniform:
        def __str__(self) -> str: ...
        @typing.overload
        def set(self, val: Matrix) -> None:
            """
            Set the matrix uniform to the given *val*.
            """
        @typing.overload
        def set(self, val: int | float) -> None:
            """
            Set the uniform with a single value to the given *val*. *val* is automatically type-cast.
            """
        @typing.overload
        def set(self, val: typing.Sequence[int] | typing.Sequence[float]) -> None:
            """
            Set the uniform with an array of values to the given *val*. *val* is automatically type-cast.
            """
    def child(self, name: str) -> RuntimeEffectBuilder.BuilderChild: ...
    def children(self) -> list[RuntimeEffect.ChildPtr]: ...
    def effect(self) -> RuntimeEffect: ...
    def uniform(self, name: str) -> RuntimeEffectBuilder.BuilderUniform: ...
    def uniforms(self) -> Data: ...
    pass

class RuntimeColorFilterBuilder(RuntimeEffectBuilder):
    def __init__(self, effect: RuntimeEffect) -> None: ...
    def makeColorFilter(self) -> ColorFilter: ...
    pass

class RuntimeEffect:
    class Child:
        def __str__(self) -> str: ...
        @property
        def index(self) -> int:
            """
            :type: int
            """
        @property
        def name(self) -> str:
            """
            :type: str
            """
        @property
        def type(self) -> RuntimeEffect.ChildType:
            """
            :type: RuntimeEffect.ChildType
            """

    class ChildPtr:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, b: Blender) -> None: ...
        @typing.overload
        def __init__(self, cf: ColorFilter) -> None: ...
        @typing.overload
        def __init__(self, s: Shader) -> None: ...
        def __str__(self) -> str: ...
        def blender(self) -> Blender: ...
        def colorFilter(self) -> ColorFilter: ...
        def flattenable(self) -> Flattenable: ...
        def shader(self) -> Shader: ...
        def type(self) -> RuntimeEffect.ChildType | None: ...
        pass

    class ChildType:
        """
        Members:

          kShader

          kColorFilter

          kBlender
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
        __members__: dict  # value = {'kShader': <ChildType.kShader: 0>, 'kColorFilter': <ChildType.kColorFilter: 1>, 'kBlender': <ChildType.kBlender: 2>}
        kBlender: animator.skia.RuntimeEffect.ChildType  # value = <ChildType.kBlender: 2>
        kColorFilter: animator.skia.RuntimeEffect.ChildType  # value = <ChildType.kColorFilter: 1>
        kShader: animator.skia.RuntimeEffect.ChildType  # value = <ChildType.kShader: 0>
        pass

    class Options:
        def __init__(self, forceUnoptimized: bool = False) -> None: ...
        def __str__(self) -> str: ...
        pass

    class Result:
        def __str__(self) -> str: ...
        @property
        def effect(self) -> RuntimeEffect | None:
            """
            :type: RuntimeEffect
            """
        @property
        def errorText(self) -> str:
            """
            :type: str
            """

    class TracedShader:
        @property
        def debugTrace(self) -> sksl.DebugTrace:
            """
            :type: sksl.DebugTrace
            """
        @property
        def shader(self) -> Shader:
            """
            :type: Shader
            """

    class Uniform:
        class Flags(IntEnum):
            """
            Members:

              kArray_Flag

              kColor_Flag

              kVertex_Flag

              kFragment_Flag

              kHalfPrecision_Flag
            """

            def __and__(self, other: object) -> object: ...
            def __eq__(self, other: object) -> bool: ...
            def __ge__(self, other: object) -> bool: ...
            def __getstate__(self) -> int: ...
            def __gt__(self, other: object) -> bool: ...
            def __hash__(self) -> int: ...
            def __index__(self) -> int: ...
            def __init__(self, value: int) -> None: ...
            def __int__(self) -> int: ...
            def __invert__(self) -> object: ...
            def __le__(self, other: object) -> bool: ...
            def __lt__(self, other: object) -> bool: ...
            def __ne__(self, other: object) -> bool: ...
            def __or__(self, other: object) -> object: ...
            def __rand__(self, other: object) -> object: ...
            def __repr__(self) -> str: ...
            def __ror__(self, other: object) -> object: ...
            def __rxor__(self, other: object) -> object: ...
            def __setstate__(self, state: int) -> None: ...
            def __xor__(self, other: object) -> object: ...
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
            __members__: dict  # value = {'kArray_Flag': <Flags.kArray_Flag: 1>, 'kColor_Flag': <Flags.kColor_Flag: 2>, 'kVertex_Flag': <Flags.kVertex_Flag: 4>, 'kFragment_Flag': <Flags.kFragment_Flag: 8>, 'kHalfPrecision_Flag': <Flags.kHalfPrecision_Flag: 16>}
            kArray_Flag: animator.skia.RuntimeEffect.Uniform.Flags  # value = <Flags.kArray_Flag: 1>
            kColor_Flag: animator.skia.RuntimeEffect.Uniform.Flags  # value = <Flags.kColor_Flag: 2>
            kFragment_Flag: animator.skia.RuntimeEffect.Uniform.Flags  # value = <Flags.kFragment_Flag: 8>
            kHalfPrecision_Flag: animator.skia.RuntimeEffect.Uniform.Flags  # value = <Flags.kHalfPrecision_Flag: 16>
            kVertex_Flag: animator.skia.RuntimeEffect.Uniform.Flags  # value = <Flags.kVertex_Flag: 4>
            pass

        class Type:
            """
            Members:

              kFloat

              kFloat2

              kFloat3

              kFloat4

              kFloat2x2

              kFloat3x3

              kFloat4x4

              kInt

              kInt2

              kInt3

              kInt4
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
            __members__: dict  # value = {'kFloat': <Type.kFloat: 0>, 'kFloat2': <Type.kFloat2: 1>, 'kFloat3': <Type.kFloat3: 2>, 'kFloat4': <Type.kFloat4: 3>, 'kFloat2x2': <Type.kFloat2x2: 4>, 'kFloat3x3': <Type.kFloat3x3: 5>, 'kFloat4x4': <Type.kFloat4x4: 6>, 'kInt': <Type.kInt: 7>, 'kInt2': <Type.kInt2: 8>, 'kInt3': <Type.kInt3: 9>, 'kInt4': <Type.kInt4: 10>}
            kFloat: animator.skia.RuntimeEffect.Uniform.Type  # value = <Type.kFloat: 0>
            kFloat2: animator.skia.RuntimeEffect.Uniform.Type  # value = <Type.kFloat2: 1>
            kFloat2x2: animator.skia.RuntimeEffect.Uniform.Type  # value = <Type.kFloat2x2: 4>
            kFloat3: animator.skia.RuntimeEffect.Uniform.Type  # value = <Type.kFloat3: 2>
            kFloat3x3: animator.skia.RuntimeEffect.Uniform.Type  # value = <Type.kFloat3x3: 5>
            kFloat4: animator.skia.RuntimeEffect.Uniform.Type  # value = <Type.kFloat4: 3>
            kFloat4x4: animator.skia.RuntimeEffect.Uniform.Type  # value = <Type.kFloat4x4: 6>
            kInt: animator.skia.RuntimeEffect.Uniform.Type  # value = <Type.kInt: 7>
            kInt2: animator.skia.RuntimeEffect.Uniform.Type  # value = <Type.kInt2: 8>
            kInt3: animator.skia.RuntimeEffect.Uniform.Type  # value = <Type.kInt3: 9>
            kInt4: animator.skia.RuntimeEffect.Uniform.Type  # value = <Type.kInt4: 10>
            pass
        def __str__(self) -> str: ...
        def isArray(self) -> bool: ...
        def isColor(self) -> bool: ...
        def sizeInBytes(self) -> int: ...
        @property
        def count(self) -> int:
            """
            :type: int
            """
        @property
        def flags(self) -> int:
            """
            :type: int
            """
        @property
        def name(self) -> str:
            """
            :type: str
            """
        @property
        def offset(self) -> int:
            """
            :type: int
            """
        @property
        def type(self) -> RuntimeEffect.Uniform.Type:
            """
            :type: RuntimeEffect.Uniform.Type
            """
    @staticmethod
    def MakeForBlender(sksl: str, options: RuntimeEffect.Options = ...) -> RuntimeEffect.Result: ...
    @staticmethod
    def MakeForColorFilter(sksl: str, options: RuntimeEffect.Options = ...) -> RuntimeEffect.Result: ...
    @staticmethod
    def MakeForShader(sksl: str, options: RuntimeEffect.Options = ...) -> RuntimeEffect.Result: ...
    @staticmethod
    def MakeTraced(shader: Shader, traceCoord: IPoint) -> RuntimeEffect.TracedShader: ...
    def __str__(self) -> str: ...
    def allowBlender(self) -> bool: ...
    def allowColorFilter(self) -> bool: ...
    def allowShader(self) -> bool: ...
    def children(self) -> list[RuntimeEffect.Child]: ...
    def findChild(self, name: str) -> RuntimeEffect.Child: ...
    def findUniform(self, name: str) -> RuntimeEffect.Uniform: ...
    def makeBlender(self, uniforms: Data, children: list[RuntimeEffect.ChildPtr] = []) -> Blender:
        """
        Create a blender from this effect with the given *uniforms* and *children*.
        """
    @typing.overload
    def makeColorFilter(self, uniforms: Data) -> ColorFilter: ...
    @typing.overload
    def makeColorFilter(self, uniforms: Data, children: list[ColorFilter]) -> ColorFilter:
        """
        Create a color filter from this effect with the given *uniforms* and *children*.
        """
    @typing.overload
    def makeColorFilter(self, uniforms: Data, children: list[RuntimeEffect.ChildPtr]) -> ColorFilter:
        """
        Create a color filter from this effect with the given *uniforms* and *children*.
        """
    def makeImage(
        self,
        uniforms: Data,
        children: list[RuntimeEffect.ChildPtr],
        resultInfo: ImageInfo,
        localMatrix: Matrix | None = None,
        mipmapped: bool = False,
    ) -> Image:
        """
        Create an image from this effect with the given *uniforms* and *children*.

        :note: The *resultInfo* and *localMatrix* parameters are swapped from the corresponding parameters in
            the C++ API.
        """
    @typing.overload
    def makeShader(
        self, uniforms: Data, children: list[RuntimeEffect.ChildPtr], localMatrix: Matrix | None = None
    ) -> Shader:
        """
        Create a shader from this effect with the given *uniforms* and *children*.
        """
    @typing.overload
    def makeShader(self, uniforms: Data, children: list[Shader], localMatrix: Matrix | None = None) -> Shader:
        """
        Create a shader from this effect with the given *uniforms* and *children*.
        """
    def source(self) -> str: ...
    def uniformSize(self) -> int: ...
    def uniforms(self) -> list[RuntimeEffect.Uniform]: ...
    pass

class RuntimeBlendBuilder(RuntimeEffectBuilder):
    def __init__(self, effect: RuntimeEffect) -> None: ...
    def makeBlender(self) -> Blender: ...
    pass

class RuntimeShaderBuilder(RuntimeEffectBuilder):
    def __init__(self, effect: RuntimeEffect) -> None: ...
    def makeImage(self, resultInfo: ImageInfo, localMatrix: Matrix | None = None, mipmapped: bool = False) -> Image:
        """
        Create an image from this shader builder with the given *resultInfo*.

        :note: The *resultInfo* and *localMatrix* parameters are swapped from the corresponding parameters in
            the C++ API.
        """
    def makeShader(self, localMatrix: Matrix | None = None) -> Shader: ...
    pass

class SamplingOptions:
    @staticmethod
    def Aniso(maxAniso: int) -> SamplingOptions: ...
    def __eq__(self, arg0: SamplingOptions) -> bool: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, c: CubicResampler) -> None: ...
    @typing.overload
    def __init__(self, fm: FilterMode) -> None: ...
    @typing.overload
    def __init__(self, fm: FilterMode, mm: MipmapMode) -> None: ...
    @typing.overload
    def __init__(self, other: SamplingOptions) -> None: ...
    def __ne__(self, arg0: SamplingOptions) -> bool: ...
    def __str__(self) -> str: ...
    def isAniso(self) -> bool: ...
    @property
    def cubic(self) -> CubicResampler:
        """
        :type: CubicResampler
        """
    @property
    def filter(self) -> FilterMode:
        """
        :type: FilterMode
        """
    @property
    def maxAniso(self) -> int:
        """
        :type: int
        """
    @property
    def mipmap(self) -> MipmapMode:
        """
        :type: MipmapMode
        """
    @property
    def useCubic(self) -> bool:
        """
        :type: bool
        """

class Shader(Flattenable):
    """
    Functions from the SkShaders namespace are also available here as static methods.
    """

    @staticmethod
    @typing.overload
    def Blend(blender: Blender, dst: Shader, src: Shader) -> Shader: ...
    @staticmethod
    @typing.overload
    def Blend(mode: BlendMode, dst: Shader, src: Shader) -> Shader: ...
    @staticmethod
    @typing.overload
    def Color(color: _Color4f, space: ColorSpace | None = None) -> Shader: ...
    @staticmethod
    @typing.overload
    def Color(color: _Color) -> Shader: ...
    @staticmethod
    def CoordClamp(shader: Shader, subset: _Rect) -> Shader: ...
    @staticmethod
    def Empty() -> Shader: ...
    @staticmethod
    def MakeFractalNoise(
        baseFrequencyX: float, baseFrequencyY: float, numOctaves: int, seed: float, tileSize: _ISize | None = None
    ) -> Shader: ...
    @staticmethod
    def MakeTurbulence(
        baseFrequencyX: float, baseFrequencyY: float, numOctaves: int, seed: float, tileSize: _ISize | None = None
    ) -> Shader: ...
    def isAImage(self) -> tuple | None:
        """
        Iff this shader is backed by a single :py:class:`Image`, return it, the local matrix, and the tile mode.
        Else return ``None``.
        """
    def isOpaque(self) -> bool: ...
    def makeWithColorFilter(self, filter: ColorFilter) -> Shader: ...
    def makeWithLocalMatrix(self, localMatrix: Matrix) -> Shader: ...
    pass

class ShaderMaskFilter:
    @staticmethod
    def Make(shader: Shader) -> MaskFilter: ...
    pass

class ShadowFlags(IntEnum):
    """
    Members:

      kNone_ShadowFlag

      kTransparentOccluder_ShadowFlag

      kGeometricOnly_ShadowFlag

      kDirectionalLight_ShadowFlag

      kConcaveBlurOnly_ShadowFlag

      kAll_ShadowFlag
    """

    def __and__(self, other: object) -> object: ...
    def __eq__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __gt__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __invert__(self) -> object: ...
    def __le__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __or__(self, other: object) -> object: ...
    def __rand__(self, other: object) -> object: ...
    def __repr__(self) -> str: ...
    def __ror__(self, other: object) -> object: ...
    def __rxor__(self, other: object) -> object: ...
    def __setstate__(self, state: int) -> None: ...
    def __xor__(self, other: object) -> object: ...
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
    __members__: dict  # value = {'kNone_ShadowFlag': <ShadowFlags.kNone_ShadowFlag: 0>, 'kTransparentOccluder_ShadowFlag': <ShadowFlags.kTransparentOccluder_ShadowFlag: 1>, 'kGeometricOnly_ShadowFlag': <ShadowFlags.kGeometricOnly_ShadowFlag: 2>, 'kDirectionalLight_ShadowFlag': <ShadowFlags.kDirectionalLight_ShadowFlag: 4>, 'kConcaveBlurOnly_ShadowFlag': <ShadowFlags.kConcaveBlurOnly_ShadowFlag: 8>, 'kAll_ShadowFlag': <ShadowFlags.kAll_ShadowFlag: 15>}
    kAll_ShadowFlag: animator.skia.ShadowFlags  # value = <ShadowFlags.kAll_ShadowFlag: 15>
    kConcaveBlurOnly_ShadowFlag: animator.skia.ShadowFlags  # value = <ShadowFlags.kConcaveBlurOnly_ShadowFlag: 8>
    kDirectionalLight_ShadowFlag: animator.skia.ShadowFlags  # value = <ShadowFlags.kDirectionalLight_ShadowFlag: 4>
    kGeometricOnly_ShadowFlag: animator.skia.ShadowFlags  # value = <ShadowFlags.kGeometricOnly_ShadowFlag: 2>
    kNone_ShadowFlag: animator.skia.ShadowFlags  # value = <ShadowFlags.kNone_ShadowFlag: 0>
    kTransparentOccluder_ShadowFlag: animator.skia.ShadowFlags  # value = <ShadowFlags.kTransparentOccluder_ShadowFlag: 1>
    pass

class ShadowUtils:
    @staticmethod
    def ComputeTonalColors(inAmbientColor: _Color, inSpotColor: _Color) -> tuple[int, int]:
        """
        Compute and return color values for one-pass tonal alpha.
        """
    @staticmethod
    def DrawShadow(
        canvas: Canvas,
        path: Path,
        zPlaneParams: _Point3,
        lightPos: _Point3,
        lightRadius: float,
        ambientColor: _Color,
        spotColor: _Color,
        flags: int = ShadowFlags.kNone_ShadowFlag,
    ) -> None: ...
    @staticmethod
    def GetLocalBounds(
        ctm: Matrix,
        path: Path,
        zPlaneParams: _Point3,
        lightPos: _Point3,
        lightRadius: float,
        flags: int = ShadowFlags.kNone_ShadowFlag,
    ) -> Rect:
        """
        Return bounding box for shadows relative to path. Includes both the ambient and spot shadow bounds.
        """

class Size:
    @staticmethod
    @typing.overload
    def Make(src: _ISize) -> Size: ...
    @staticmethod
    @typing.overload
    def Make(w: float, h: float) -> Size: ...
    @staticmethod
    def MakeEmpty() -> Size: ...
    def __eq__(self, other: Size) -> bool: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, src: _ISize) -> None: ...
    @typing.overload
    def __init__(self, t: tuple) -> None:
        """
        Create a :py:class:`Size` from a tuple of two floats.

        :param t: Tuple of two floats.
        """
    @typing.overload
    def __init__(self, w: float, h: float) -> None: ...
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    def __ne__(self, other: Size) -> bool: ...
    def __str__(self) -> str: ...
    def equals(self, w: float, h: float) -> bool: ...
    def height(self) -> float: ...
    def isEmpty(self) -> bool: ...
    def isZero(self) -> bool: ...
    def set(self, w: float, h: float) -> None: ...
    def setEmpty(self) -> None: ...
    def toCeil(self) -> ISize: ...
    def toFloor(self) -> ISize: ...
    def toRound(self) -> ISize: ...
    def width(self) -> float: ...
    @property
    def fHeight(self) -> float:
        """
        :type: float
        """
    @fHeight.setter
    def fHeight(self, arg0: float) -> None:
        pass
    @property
    def fWidth(self) -> float:
        """
        :type: float
        """
    @fWidth.setter
    def fWidth(self, arg0: float) -> None:
        pass
    pass

class StrokeAndFillPathEffect:
    @staticmethod
    def Make() -> PathEffect: ...
    pass

class StrokePathEffect:
    @staticmethod
    def Make(width: float, join: Paint.Join, cap: Paint.Cap, miter: float = 4) -> PathEffect: ...
    pass

class StrokeRec:
    class InitStyle:
        """
        Members:

          kHairline_InitStyle

          kFill_InitStyle
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
        __members__: dict  # value = {'kHairline_InitStyle': <InitStyle.kHairline_InitStyle: 0>, 'kFill_InitStyle': <InitStyle.kFill_InitStyle: 1>}
        kFill_InitStyle: animator.skia.StrokeRec.InitStyle  # value = <InitStyle.kFill_InitStyle: 1>
        kHairline_InitStyle: animator.skia.StrokeRec.InitStyle  # value = <InitStyle.kHairline_InitStyle: 0>
        pass

    class Style:
        """
        Members:

          kHairline_Style

          kFill_Style

          kStroke_Style

          kStrokeAndFill_Style
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
        __members__: dict  # value = {'kHairline_Style': <Style.kHairline_Style: 0>, 'kFill_Style': <Style.kFill_Style: 1>, 'kStroke_Style': <Style.kStroke_Style: 2>, 'kStrokeAndFill_Style': <Style.kStrokeAndFill_Style: 3>}
        kFill_Style: animator.skia.StrokeRec.Style  # value = <Style.kFill_Style: 1>
        kHairline_Style: animator.skia.StrokeRec.Style  # value = <Style.kHairline_Style: 0>
        kStrokeAndFill_Style: animator.skia.StrokeRec.Style  # value = <Style.kStrokeAndFill_Style: 3>
        kStroke_Style: animator.skia.StrokeRec.Style  # value = <Style.kStroke_Style: 2>
        pass
    @staticmethod
    @typing.overload
    def GetInflationRadius(join: Paint.Join, miterLimit: float, cap: Paint.Cap, strokeWidth: float) -> float: ...
    @staticmethod
    @typing.overload
    def GetInflationRadius(paint: Paint, style: Paint.Style) -> float: ...
    def __eq__(self, other: StrokeRec) -> bool: ...
    @typing.overload
    def __init__(self, paint: Paint, resScale: float = 1) -> None: ...
    @typing.overload
    def __init__(self, paint: Paint, style: Paint.Style, resScale: float = 1) -> None: ...
    @typing.overload
    def __init__(self, style: StrokeRec.InitStyle) -> None: ...
    def __str__(self) -> str: ...
    def applyAndGetPath(self, src: Path) -> Path:
        """
        Apply the stroke parameters to the src path and return the result.
        """
    def applyToPaint(self, paint: Paint) -> None: ...
    def applyToPath(self, dst: Path, src: Path) -> bool: ...
    def getCap(self) -> Paint.Cap: ...
    def getInflationRadius(self) -> float: ...
    def getJoin(self) -> Paint.Join: ...
    def getMiter(self) -> float: ...
    def getPaint(self) -> Paint:
        """
        Apply the stroke parameters to a paint and return it.
        """
    def getResScale(self) -> float: ...
    def getStyle(self) -> StrokeRec.Style: ...
    def getWidth(self) -> float: ...
    def hasEqualEffect(self, other: StrokeRec) -> bool: ...
    def isFillStyle(self) -> bool: ...
    def isHairlineStyle(self) -> bool: ...
    def needToApply(self) -> bool: ...
    def setFillStyle(self) -> None: ...
    def setHairlineStyle(self) -> None: ...
    def setResScale(self, rs: float) -> None: ...
    def setStrokeParams(self, cap: Paint.Cap, join: Paint.Join, miterLimit: float) -> None: ...
    def setStrokeStyle(self, width: float, strokeAndFill: bool = False) -> None: ...
    kStyleCount = 4
    pass

class Surface:
    """
    :py:class:`Surface` is responsible for managing the pixels that a canvas draws into. Functions from the SkShaders
    namespace are also available here as static methods.

    Example::
        surface = skia.Surface(640, 480)
        with surface as canvas:
            draw(canvas)
        image = surface.makeImageSnapshot()
    """

    class ContentChangeMode:
        """
        Members:

          kDiscard_ContentChangeMode

          kRetain_ContentChangeMode
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
        __members__: dict  # value = {'kDiscard_ContentChangeMode': <ContentChangeMode.kDiscard_ContentChangeMode: 0>, 'kRetain_ContentChangeMode': <ContentChangeMode.kRetain_ContentChangeMode: 1>}
        kDiscard_ContentChangeMode: animator.skia.Surface.ContentChangeMode  # value = <ContentChangeMode.kDiscard_ContentChangeMode: 0>
        kRetain_ContentChangeMode: animator.skia.Surface.ContentChangeMode  # value = <ContentChangeMode.kRetain_ContentChangeMode: 1>
        pass
    @staticmethod
    def Null(width: int, height: int) -> Surface: ...
    @staticmethod
    def Raster(imageInfo: ImageInfo, rowBytes: int = 0, surfaceProps: SurfaceProps | None = None) -> Surface: ...
    @staticmethod
    @typing.overload
    def WrapPixels(
        imageInfo: ImageInfo, pixels: buffer, rowBytes: int = 0, surfaceProps: SurfaceProps | None = None
    ) -> Surface:
        """
        Allocates raster :py:class:`Surface` with the specified *pixels*.
        """
    @staticmethod
    @typing.overload
    def WrapPixels(pixmap: Pixmap, props: SurfaceProps | None = None) -> Surface: ...
    def __enter__(self) -> Canvas:
        """
        Returns a :py:class:`Canvas` object that can be used to draw on the surface.
        """
    def __exit__(self, arg0: object, arg1: object, arg2: object) -> None: ...
    @typing.overload
    def __init__(
        self,
        array: numpy.ndarray,
        colorType: ColorType = ColorType.kRGBA_8888_ColorType,
        alphaType: AlphaType = AlphaType.kUnpremul_AlphaType,
        colorSpace: ColorSpace | None = None,
        surfaceProps: SurfaceProps | None = None,
    ) -> None:
        """
        Creates :py:class:`Surface` backed by numpy array.
        """
    @typing.overload
    def __init__(self, width: int, height: int, surfaceProps: SurfaceProps | None = None) -> None: ...
    def __str__(self) -> str: ...
    def draw(
        self, canvas: Canvas, x: float, y: float, sampling: SamplingOptions = ..., paint: Paint | None = None
    ) -> None: ...
    def generationID(self) -> int: ...
    def getCanvas(self) -> Canvas: ...
    def height(self) -> int: ...
    def imageInfo(self) -> ImageInfo: ...
    @typing.overload
    def makeImageSnapshot(self) -> Image: ...
    @typing.overload
    def makeImageSnapshot(self, bounds: _IRect) -> Image: ...
    @typing.overload
    def makeSurface(self, imageInfo: ImageInfo) -> Surface: ...
    @typing.overload
    def makeSurface(self, width: int, height: int) -> Surface: ...
    def notifyContentWillChange(self, mode: Surface.ContentChangeMode) -> None: ...
    def peekPixels(self) -> Pixmap:
        """
        Returns a :py:class:`Pixmap` describing the pixel data.
        """
    def props(self) -> SurfaceProps: ...
    @typing.overload
    def readPixels(self, dst: Bitmap, srcX: int = 0, srcY: int = 0) -> bool: ...
    @typing.overload
    def readPixels(self, dst: Pixmap, srcX: int = 0, srcY: int = 0) -> bool: ...
    @typing.overload
    def readPixels(
        self, dstInfo: ImageInfo, dstPixels: buffer, dstRowBytes: int = 0, srcX: int = 0, srcY: int = 0
    ) -> bool:
        """
        Copies *dstInfo* pixels starting from (*srcX*, *srcY*) to *dstPixels* buffer.
        """
    def toarray(
        self,
        srcX: int = 0,
        srcY: int = 0,
        colorType: ColorType = ColorType.kRGBA_8888_ColorType,
        alphaType: AlphaType = AlphaType.kUnpremul_AlphaType,
        colorSpace: ColorSpace | None = None,
    ) -> numpy.ndarray:
        """
        Returns a ``ndarray`` of the image's pixels.
        """
    def width(self) -> int: ...
    @typing.overload
    def writePixels(self, src: Bitmap, dstX: int = 0, dstY: int = 0) -> None: ...
    @typing.overload
    def writePixels(self, src: Pixmap, dstX: int = 0, dstY: int = 0) -> None: ...
    pass

class SurfaceProps:
    class Flags(IntEnum):
        """
        Members:

          kUseDeviceIndependentFonts_Flag

          kDynamicMSAA_Flag

          kAlwaysDither_Flag
        """

        def __and__(self, other: object) -> object: ...
        def __eq__(self, other: object) -> bool: ...
        def __ge__(self, other: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __gt__(self, other: object) -> bool: ...
        def __hash__(self) -> int: ...
        def __index__(self) -> int: ...
        def __init__(self, value: int) -> None: ...
        def __int__(self) -> int: ...
        def __invert__(self) -> object: ...
        def __le__(self, other: object) -> bool: ...
        def __lt__(self, other: object) -> bool: ...
        def __ne__(self, other: object) -> bool: ...
        def __or__(self, other: object) -> object: ...
        def __rand__(self, other: object) -> object: ...
        def __repr__(self) -> str: ...
        def __ror__(self, other: object) -> object: ...
        def __rxor__(self, other: object) -> object: ...
        def __setstate__(self, state: int) -> None: ...
        def __xor__(self, other: object) -> object: ...
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
        __members__: dict  # value = {'kUseDeviceIndependentFonts_Flag': <Flags.kUseDeviceIndependentFonts_Flag: 1>, 'kDynamicMSAA_Flag': <Flags.kDynamicMSAA_Flag: 2>, 'kAlwaysDither_Flag': <Flags.kAlwaysDither_Flag: 4>}
        kAlwaysDither_Flag: animator.skia.SurfaceProps.Flags  # value = <Flags.kAlwaysDither_Flag: 4>
        kDynamicMSAA_Flag: animator.skia.SurfaceProps.Flags  # value = <Flags.kDynamicMSAA_Flag: 2>
        kUseDeviceIndependentFonts_Flag: animator.skia.SurfaceProps.Flags  # value = <Flags.kUseDeviceIndependentFonts_Flag: 1>
        pass
    def __eq__(self, arg0: SurfaceProps) -> bool: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, flags: int, pg: PixelGeometry) -> None: ...
    @typing.overload
    def __init__(self, props: SurfaceProps) -> None: ...
    def __ne__(self, arg0: SurfaceProps) -> bool: ...
    def cloneWithPixelGeometry(self, newPixelGeometry: PixelGeometry) -> SurfaceProps: ...
    def flags(self) -> int: ...
    def isAlwaysDither(self) -> bool: ...
    def isUseDeviceIndependentFonts(self) -> bool: ...
    def pixelGeometry(self) -> PixelGeometry: ...
    pass

class TableMaskFilter:
    @staticmethod
    def Create(table: list[int]) -> MaskFilter: ...
    @staticmethod
    def CreateClip(min: int, max: int) -> MaskFilter: ...
    @staticmethod
    def CreateGamma(gamma: float) -> MaskFilter: ...
    @staticmethod
    def MakeClipTable(min: int, max: int) -> list[int]:
        """
        Utility that returns a clipping table.
        """
    @staticmethod
    def MakeGammaTable(gamma: float) -> list[int]:
        """
        Utility that returns the *gamma* table.
        """

class TextBlob:
    class Iter:
        class Run:
            def __str__(self) -> str: ...
            @property
            def fGlyphCount(self) -> int:
                """
                :type: int
                """
            @property
            def fGlyphIndices(self) -> list[int]:
                """
                :type: list[int]
                """
            @property
            def fTypeface(self) -> Typeface:
                """
                :type: Typeface
                """
        def __init__(self, arg0: TextBlob) -> None: ...
        def __iter__(self) -> TextBlob.Iter: ...
        def __next__(self) -> TextBlob.Iter.Run: ...
        def next(self) -> TextBlob.Iter.Run | None: ...
        pass
    @staticmethod
    def Deserialize(data: buffer) -> TextBlob:
        """
        Recreates :py:class:`TextBlob` that was serialized into data.
        """
    @staticmethod
    def MakeFromPosText(
        text: str, pos: list[_Point], font: Font, encoding: TextEncoding = TextEncoding.kUTF8
    ) -> TextBlob:
        """
        Returns a :py:class:`TextBlob` built from a single run of *text* with *pos*.
        """
    @staticmethod
    def MakeFromPosTextH(
        text: str, xpos: list[float], constY: float, font: Font, encoding: TextEncoding = TextEncoding.kUTF8
    ) -> TextBlob:
        """
        Returns a :py:class:`TextBlob` built from a single run of *text* with *xpos* and a single *constY* value.
        """
    @staticmethod
    def MakeFromRSXform(
        text: str, xform: list[RSXform], font: Font, encoding: TextEncoding = TextEncoding.kUTF8
    ) -> TextBlob: ...
    @staticmethod
    def MakeFromString(string: str, font: Font, encoding: TextEncoding = TextEncoding.kUTF8) -> TextBlob: ...
    @staticmethod
    def MakeFromText(text: str, font: Font, encoding: TextEncoding = TextEncoding.kUTF8) -> TextBlob:
        """
        Creates :py:class:`TextBlob` with a single run of *text*.
        """
    @staticmethod
    def MakeOnPath(
        text: str, path: Path, font: Font, offset: float = 0, encoding: TextEncoding = TextEncoding.kUTF8
    ) -> TextBlob:
        """
        Returns a :py:class:`TextBlob` built from a single run of *text* along *path* starting at *offset*.
        """
    def __init__(
        self,
        text: str,
        font: Font,
        pos: list[_Point] | None = None,
        encoding: TextEncoding = TextEncoding.kUTF8,
    ) -> None:
        """
        Creates a :py:class:`TextBlob` with a single run of *text* and optional *pos*.
        """
    def __iter__(self) -> TextBlob.Iter: ...
    def __str__(self) -> str: ...
    def bounds(self) -> Rect: ...
    def getIntercepts(self, bounds: list[float], paint: Paint | None = None) -> list[float]:
        """
        Returns the number of intervals that intersect *bounds*.
        """
    def serialize(self) -> Data: ...
    def uniqueID(self) -> int: ...
    pass

class TextBlobBuilder:
    """
    In Skia, you call the ``alloc*`` methods of this class with the count of glyphs to create a ``RunBuffer``
    object. Then the object is filled with the required data before the next call to another method.

    However, in this Python binding, the ``alloc*`` methods do not return the ``RunBuffer`` object. Instead of
    passing the count of glyphs, you need to call them with the required data directly and it'll handle the
    allocation and data filling automatically. All the other parameters are the same as in the C++ API. You can
    optionally pass a *encoding* parameter to specify the encoding of the text. These methods return the
    :py:class:`TextBlobBuilder` object itself for method chaining.
    """

    def __init__(self) -> None: ...
    def allocRun(
        self,
        font: Font,
        text: str,
        x: float,
        y: float,
        bounds: _Rect | None = None,
        encoding: TextEncoding = TextEncoding.kUTF8,
    ) -> TextBlobBuilder:
        """
        Sets a new run with glyphs for *text*.
        """
    def allocRunPos(
        self,
        font: Font,
        text: str,
        pos: list[_Point],
        bounds: _Rect | None = None,
        encoding: TextEncoding = TextEncoding.kUTF8,
    ) -> TextBlobBuilder:
        """
        Sets a new run with glyphs for *text* at *pos*.
        """
    def allocRunPosH(
        self,
        font: Font,
        text: str,
        xpos: list[float],
        y: float,
        bounds: _Rect | None = None,
        encoding: TextEncoding = TextEncoding.kUTF8,
    ) -> TextBlobBuilder:
        """
        Sets a new run with glyphs for *text* at *xpos*.
        """
    def allocRunRSXform(
        self, font: Font, text: str, xforms: list[RSXform], encoding: TextEncoding = TextEncoding.kUTF8
    ) -> TextBlobBuilder:
        """
        Sets a new run with glyphs for *text* with *xforms*.
        """
    def allocRunText(
        self,
        font: Font,
        text: str,
        clusters: list[int],
        x: float,
        y: float,
        utf8text: str,
        bounds: _Rect | None = None,
        encoding: TextEncoding = TextEncoding.kUTF8,
    ) -> TextBlobBuilder:
        """
        Sets a new run with glyphs for *text* with supporting *clusters* and *utf8text*.
        """
    def allocRunTextPos(
        self,
        font: Font,
        text: str,
        clusters: list[int],
        pos: list[_Point],
        utf8text: str,
        bounds: _Rect | None = None,
        encoding: TextEncoding = TextEncoding.kUTF8,
    ) -> TextBlobBuilder:
        """
        Sets a new run with glyphs for *text* at *pos* with supporting *clusters* and *utf8text*.
        """
    def allocRunTextPosH(
        self,
        font: Font,
        text: str,
        clusters: list[int],
        xpos: list[float],
        y: float,
        utf8text: str,
        bounds: _Rect | None = None,
        encoding: TextEncoding = TextEncoding.kUTF8,
    ) -> TextBlobBuilder:
        """
        Sets a new run with glyphs for *text* at *xpos* with supporting *clusters* and *utf8text*.
        """
    def allocRunTextRSXform(
        self,
        font: Font,
        text: str,
        clusters: list[int],
        xforms: list[RSXform],
        utf8text: str,
        bounds: _Rect | None = None,
        encoding: TextEncoding = TextEncoding.kUTF8,
    ) -> TextBlobBuilder:
        """
        Sets a new run with glyphs for *text* with *xforms* and supporting *clusters* and *utf8text*.
        """
    def make(self) -> TextBlob: ...
    pass

class TextEncoding:
    """
    Members:

      kUTF8

      kUTF16

      kUTF32

      kGlyphID
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
    __members__: dict  # value = {'kUTF8': <TextEncoding.kUTF8: 0>, 'kUTF16': <TextEncoding.kUTF16: 1>, 'kUTF32': <TextEncoding.kUTF32: 2>, 'kGlyphID': <TextEncoding.kGlyphID: 3>}
    kGlyphID: animator.skia.TextEncoding  # value = <TextEncoding.kGlyphID: 3>
    kUTF16: animator.skia.TextEncoding  # value = <TextEncoding.kUTF16: 1>
    kUTF32: animator.skia.TextEncoding  # value = <TextEncoding.kUTF32: 2>
    kUTF8: animator.skia.TextEncoding  # value = <TextEncoding.kUTF8: 0>
    pass

class TextUtils_Align:
    """
    Members:

      kLeft_Align

      kCenter_Align

      kRight_Align
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
    __members__: dict  # value = {'kLeft_Align': <TextUtils_Align.kLeft_Align: 0>, 'kCenter_Align': <TextUtils_Align.kCenter_Align: 1>, 'kRight_Align': <TextUtils_Align.kRight_Align: 2>}
    kCenter_Align: animator.skia.TextUtils_Align  # value = <TextUtils_Align.kCenter_Align: 1>
    kLeft_Align: animator.skia.TextUtils_Align  # value = <TextUtils_Align.kLeft_Align: 0>
    kRight_Align: animator.skia.TextUtils_Align  # value = <TextUtils_Align.kRight_Align: 2>

class TileMode:
    """
    Members:

      kClamp

      kRepeat

      kMirror

      kDecal

      kLastTileMode
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
    __members__: dict  # value = {'kClamp': <TileMode.kClamp: 0>, 'kRepeat': <TileMode.kRepeat: 1>, 'kMirror': <TileMode.kMirror: 2>, 'kDecal': <TileMode.kDecal: 3>, 'kLastTileMode': <TileMode.kDecal: 3>}
    kClamp: animator.skia.TileMode  # value = <TileMode.kClamp: 0>
    kDecal: animator.skia.TileMode  # value = <TileMode.kDecal: 3>
    kLastTileMode: animator.skia.TileMode  # value = <TileMode.kDecal: 3>
    kMirror: animator.skia.TileMode  # value = <TileMode.kMirror: 2>
    kRepeat: animator.skia.TileMode  # value = <TileMode.kRepeat: 1>
    pass

class TrimPathEffect:
    class Mode:
        """
        Members:

          kNormal

          kInverted
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
        __members__: dict  # value = {'kNormal': <Mode.kNormal: 0>, 'kInverted': <Mode.kInverted: 1>}
        kInverted: animator.skia.TrimPathEffect.Mode  # value = <Mode.kInverted: 1>
        kNormal: animator.skia.TrimPathEffect.Mode  # value = <Mode.kNormal: 0>
        pass
    @staticmethod
    def Make(startT: float, stopT: float, mode: TrimPathEffect.Mode = Mode.kNormal) -> PathEffect: ...
    pass

class Typeface:
    class LocalizedStrings:
        def __iter__(self) -> Typeface.LocalizedStrings: ...
        def __next__(self) -> tuple: ...
        pass

    class SerializeBehavior:
        """
        Members:

          kDoIncludeData

          kDontIncludeData

          kIncludeDataIfLocal
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
        __members__: dict  # value = {'kDoIncludeData': <SerializeBehavior.kDoIncludeData: 0>, 'kDontIncludeData': <SerializeBehavior.kDontIncludeData: 1>, 'kIncludeDataIfLocal': <SerializeBehavior.kIncludeDataIfLocal: 2>}
        kDoIncludeData: animator.skia.Typeface.SerializeBehavior  # value = <SerializeBehavior.kDoIncludeData: 0>
        kDontIncludeData: animator.skia.Typeface.SerializeBehavior  # value = <SerializeBehavior.kDontIncludeData: 1>
        kIncludeDataIfLocal: animator.skia.Typeface.SerializeBehavior  # value = <SerializeBehavior.kIncludeDataIfLocal: 2>
        pass
    @staticmethod
    def Equal(facea: Typeface, faceb: Typeface) -> bool: ...
    @staticmethod
    def MakeDefault() -> Typeface: ...
    @staticmethod
    def MakeDeserialize(data: Data) -> Typeface:
        """
        Given the data previously written by :py:meth:`serialize`, return a new instance of a typeface referring
        to the same font.
        """
    @staticmethod
    def MakeFromData(data: Data, index: int = 0) -> Typeface: ...
    @staticmethod
    def MakeFromFile(path: str, index: int = 0) -> Typeface: ...
    @staticmethod
    def MakeFromName(familyName: str | None, fontStyle: FontStyle = ...) -> Typeface: ...
    @staticmethod
    def UniqueID(face: Typeface) -> int: ...
    def __eq__(self, arg0: Typeface) -> bool: ...
    @typing.overload
    def __init__(self) -> None:
        """
        Returns the default normal typeface.
        """
    @typing.overload
    def __init__(self, familyName: str | None, fontStyle: FontStyle = ...) -> None:
        """
        Creates a new reference to the typeface that most closely matches the requested familyName and fontStyle.
        """
    def __str__(self) -> str: ...
    def copyTableData(self, tag: int) -> Data: ...
    def countGlyphs(self) -> int: ...
    def countTables(self) -> int: ...
    def createFamilyNameIterator(self) -> Typeface.LocalizedStrings:
        """
        Returns an iterator which returns tuple of (family name, language) specified by the font.

        :warning: Please use :py:meth:`~Typeface.getFamilyNames` instead which returns a list instead of
            an iterator. There's probably a memory leak in this method, but I don't know how to fix it.
        """
    def fontStyle(self) -> FontStyle: ...
    def getBounds(self) -> Rect: ...
    def getFamilyName(self) -> str:
        """
        Returns the family name for this typeface.
        """
    def getFamilyNames(self) -> list:
        """
        Returns a list of tuple of (family name, language) specified by the font.
        """
    def getKerningPairAdjustments(self, glyphs: list[int]) -> list[int] | None:
        """
        Given a run of *glyphs*, return the associated horizontal adjustments.
        """
    def getPostScriptName(self) -> str:
        """
        Returns the PostScript name for this typeface.
        """
    def getTableData(self, tag: int, offset: int = 0, length: int = -1) -> bytes:
        """
        Returns the contents of a table.

        :param tag: The table tag whose contents are to be copied.
        :param offset: The offset into the table at which to start copying.
        :param length: The number of bytes to copy. If this is negative, the entire table is copied.
        :return: table contents
        """
    def getTableSize(self, tag: int) -> int: ...
    def getTableTags(self) -> list[int]:
        """
        Returns the list of table tags in the font.
        """
    def getUnitsPerEm(self) -> int: ...
    def getVariationDesignParameters(self) -> list[FontParameters.Variation.Axis]:
        """
        Returns the design variation parameters.
        """
    def getVariationDesignPosition(self) -> FontArguments.VariationPosition.CoordinateVector:
        """
        Returns the design variation coordinates.
        """
    def isBold(self) -> bool: ...
    def isFixedPitch(self) -> bool: ...
    def isItalic(self) -> bool: ...
    def makeClone(self, fontArguments: FontArguments) -> Typeface: ...
    def serialize(self, behavior: Typeface.SerializeBehavior = SerializeBehavior.kIncludeDataIfLocal) -> Data: ...
    def textToGlyphs(self, text: str, encoding: TextEncoding = TextEncoding.kUTF8) -> list[int]:
        """
        Given a string, return its corresponding glyph IDs.

        :param text: the text string.
        :param encoding: the text encoding.
        :return: the corresponding glyph IDs for each character.
        """
    def unicharToGlyph(self, unichar: int) -> int: ...
    def unicharsToGlyphs(self, uni: list[int]) -> list[int]:
        """
        Given an array of UTF32 character codes, return their corresponding glyph IDs.

        :param chars: the array of UTF32 chars.
        :return: the corresponding glyph IDs for each character.
        """
    def uniqueID(self) -> int: ...
    pass

class Vertices:
    class VertexMode:
        """
        Members:

          kTriangles_VertexMode

          kTriangleStrip_VertexMode

          kTriangleFan_VertexMode

          kLast_VertexMode
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
        __members__: dict  # value = {'kTriangles_VertexMode': <VertexMode.kTriangles_VertexMode: 0>, 'kTriangleStrip_VertexMode': <VertexMode.kTriangleStrip_VertexMode: 1>, 'kTriangleFan_VertexMode': <VertexMode.kTriangleFan_VertexMode: 2>, 'kLast_VertexMode': <VertexMode.kTriangleFan_VertexMode: 2>}
        kLast_VertexMode: animator.skia.Vertices.VertexMode  # value = <VertexMode.kTriangleFan_VertexMode: 2>
        kTriangleFan_VertexMode: animator.skia.Vertices.VertexMode  # value = <VertexMode.kTriangleFan_VertexMode: 2>
        kTriangleStrip_VertexMode: animator.skia.Vertices.VertexMode  # value = <VertexMode.kTriangleStrip_VertexMode: 1>
        kTriangles_VertexMode: animator.skia.Vertices.VertexMode  # value = <VertexMode.kTriangles_VertexMode: 0>
        pass
    @staticmethod
    def MakeCopy(
        mode: Vertices.VertexMode,
        positions: list[_Point],
        texs: list[_Point] | None,
        colors: list[_Color] | None,
        indices: list[int] | None = None,
    ) -> Vertices:
        """
        Create a vertices by copying the specified arrays.
        """
    def __init__(
        self,
        mode: Vertices.VertexMode,
        positions: typing.Sequence[_Point],
        texs: typing.Sequence[_Point] | None = None,
        colors: typing.Sequence[_Color] | None = None,
        indices: list[int] | None = None,
    ) -> None:
        """
        Create a vertices by copying the specified arrays.
        """
    def approximateSize(self) -> int: ...
    def bounds(self) -> Rect: ...
    def uniqueID(self) -> int: ...
    pass

class YUVColorSpace:
    """
    Members:

      kJPEG_Full_YUVColorSpace

      kRec601_Limited_YUVColorSpace

      kRec709_Full_YUVColorSpace

      kRec709_Limited_YUVColorSpace

      kBT2020_8bit_Full_YUVColorSpace

      kBT2020_8bit_Limited_YUVColorSpace

      kBT2020_10bit_Full_YUVColorSpace

      kBT2020_10bit_Limited_YUVColorSpace

      kBT2020_12bit_Full_YUVColorSpace

      kBT2020_12bit_Limited_YUVColorSpace

      kIdentity_YUVColorSpace

      kLastEnum_YUVColorSpace

      kJPEG_YUVColorSpace

      kRec601_YUVColorSpace

      kRec709_YUVColorSpace

      kBT2020_YUVColorSpace
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
    __members__: dict  # value = {'kJPEG_Full_YUVColorSpace': <YUVColorSpace.kJPEG_Full_YUVColorSpace: 0>, 'kRec601_Limited_YUVColorSpace': <YUVColorSpace.kRec601_Limited_YUVColorSpace: 1>, 'kRec709_Full_YUVColorSpace': <YUVColorSpace.kRec709_Full_YUVColorSpace: 2>, 'kRec709_Limited_YUVColorSpace': <YUVColorSpace.kRec709_Limited_YUVColorSpace: 3>, 'kBT2020_8bit_Full_YUVColorSpace': <YUVColorSpace.kBT2020_8bit_Full_YUVColorSpace: 4>, 'kBT2020_8bit_Limited_YUVColorSpace': <YUVColorSpace.kBT2020_8bit_Limited_YUVColorSpace: 5>, 'kBT2020_10bit_Full_YUVColorSpace': <YUVColorSpace.kBT2020_10bit_Full_YUVColorSpace: 6>, 'kBT2020_10bit_Limited_YUVColorSpace': <YUVColorSpace.kBT2020_10bit_Limited_YUVColorSpace: 7>, 'kBT2020_12bit_Full_YUVColorSpace': <YUVColorSpace.kBT2020_12bit_Full_YUVColorSpace: 8>, 'kBT2020_12bit_Limited_YUVColorSpace': <YUVColorSpace.kBT2020_12bit_Limited_YUVColorSpace: 9>, 'kIdentity_YUVColorSpace': <YUVColorSpace.kIdentity_YUVColorSpace: 10>, 'kLastEnum_YUVColorSpace': <YUVColorSpace.kIdentity_YUVColorSpace: 10>, 'kJPEG_YUVColorSpace': <YUVColorSpace.kJPEG_Full_YUVColorSpace: 0>, 'kRec601_YUVColorSpace': <YUVColorSpace.kRec601_Limited_YUVColorSpace: 1>, 'kRec709_YUVColorSpace': <YUVColorSpace.kRec709_Limited_YUVColorSpace: 3>, 'kBT2020_YUVColorSpace': <YUVColorSpace.kBT2020_8bit_Limited_YUVColorSpace: 5>}
    kBT2020_10bit_Full_YUVColorSpace: animator.skia.YUVColorSpace  # value = <YUVColorSpace.kBT2020_10bit_Full_YUVColorSpace: 6>
    kBT2020_10bit_Limited_YUVColorSpace: animator.skia.YUVColorSpace  # value = <YUVColorSpace.kBT2020_10bit_Limited_YUVColorSpace: 7>
    kBT2020_12bit_Full_YUVColorSpace: animator.skia.YUVColorSpace  # value = <YUVColorSpace.kBT2020_12bit_Full_YUVColorSpace: 8>
    kBT2020_12bit_Limited_YUVColorSpace: animator.skia.YUVColorSpace  # value = <YUVColorSpace.kBT2020_12bit_Limited_YUVColorSpace: 9>
    kBT2020_8bit_Full_YUVColorSpace: animator.skia.YUVColorSpace  # value = <YUVColorSpace.kBT2020_8bit_Full_YUVColorSpace: 4>
    kBT2020_8bit_Limited_YUVColorSpace: animator.skia.YUVColorSpace  # value = <YUVColorSpace.kBT2020_8bit_Limited_YUVColorSpace: 5>
    kBT2020_YUVColorSpace: animator.skia.YUVColorSpace  # value = <YUVColorSpace.kBT2020_8bit_Limited_YUVColorSpace: 5>
    kIdentity_YUVColorSpace: animator.skia.YUVColorSpace  # value = <YUVColorSpace.kIdentity_YUVColorSpace: 10>
    kJPEG_Full_YUVColorSpace: animator.skia.YUVColorSpace  # value = <YUVColorSpace.kJPEG_Full_YUVColorSpace: 0>
    kJPEG_YUVColorSpace: animator.skia.YUVColorSpace  # value = <YUVColorSpace.kJPEG_Full_YUVColorSpace: 0>
    kLastEnum_YUVColorSpace: animator.skia.YUVColorSpace  # value = <YUVColorSpace.kIdentity_YUVColorSpace: 10>
    kRec601_Limited_YUVColorSpace: animator.skia.YUVColorSpace  # value = <YUVColorSpace.kRec601_Limited_YUVColorSpace: 1>
    kRec601_YUVColorSpace: animator.skia.YUVColorSpace  # value = <YUVColorSpace.kRec601_Limited_YUVColorSpace: 1>
    kRec709_Full_YUVColorSpace: animator.skia.YUVColorSpace  # value = <YUVColorSpace.kRec709_Full_YUVColorSpace: 2>
    kRec709_Limited_YUVColorSpace: animator.skia.YUVColorSpace  # value = <YUVColorSpace.kRec709_Limited_YUVColorSpace: 3>
    kRec709_YUVColorSpace: animator.skia.YUVColorSpace  # value = <YUVColorSpace.kRec709_Limited_YUVColorSpace: 3>
    pass

@typing.overload
def Color(color4f: _Color4f) -> int:
    """
    Returns color value from 4-float component values (:py:class:`Color4f`).

    :param color4f: color and alpha, unpremultiplied
    :return: color and alpha, unpremultiplied
    """

@typing.overload
def Color(r: int, g: int, b: int, a: int = 255) -> int:
    """
    Returns color value from 8-bit component values.

    :param int r: amount of red, from no red (0) to full red (255)
    :param int g: amount of green, from no green (0) to full green (255)
    :param int b: amount of blue, from no blue (0) to full blue (255)
    :param int a: amount of alpha, from fully transparent (0) to fully opaque (255)
    :return: color and alpha, unpremultiplied
    """

def ColorGetA(color: _Color) -> int:
    pass

def ColorGetB(color: _Color) -> int:
    pass

def ColorGetG(color: _Color) -> int:
    pass

def ColorGetR(color: _Color) -> int:
    pass

def ColorSetA(c: int, a: int) -> int:
    pass

def ColorSetARGB(a: int, r: int, g: int, b: int) -> int:
    pass

def ColorSetRGB(r: int, g: int, b: int) -> int:
    pass

def ColorToHSV(color: _Color) -> list[float]:
    """
    Converts ARGB color to its HSV components. Alpha in ARGB is ignored.

    :param color: ARGB color to convert
    :return: three element array which holds the resulting HSV components. hsv[0] contains hsv hue, a value from
        0 to less than 360. hsv[1] contains hsv saturation, a value from 0 to 1. hsv[2] contains hsv value, a
        value from 0 to 1.
    """

def HSVToColor(hsv: list[float], alpha: int = 255) -> int:
    """
    Converts HSV components to an ARGB color. Alpha is passed through unchanged.

    :param hsv: three element array which holds the input HSV components. hsv[0] represents hsv hue, an angle
        from 0 to less than 360. hsv[1] represents hsv saturation, and varies from 0 to 1. hsv[2] represents hsv
        value, and varies from 0 to 1.
    :param alpha: alpha component of the returned ARGB color
    :return: ARGB equivalent to HSV
    """

def MakeNullCanvas() -> Canvas:
    pass

def PreMultiplyARGB(a: int, r: int, g: int, b: int) -> int:
    pass

def PreMultiplyColor(c: int) -> int:
    pass

def RGBToHSV(red: int, green: int, blue: int) -> list[float]:
    """
    Converts RGB to its HSV components.

    :param int red: red component value from 0 to 255
    :param int green: green component value from 0 to 255
    :param int blue: blue component value from 0 to 255
    :return: three element array which holds the resulting HSV components. hsv[0] contains hsv hue, a value from
        0 to less than 360. hsv[1] contains hsv saturation, a value from 0 to 1. hsv[2] contains hsv value, a
        value from 0 to 1.
    """

def uniqueColor(l: float = 71, s: float = 100) -> Color4f:
    """
    Returns a unique color every time it is called. Uses HSLuv (https://www.hsluv.org/) internally.

    :param l: Lightness of the generated color. Must be between 0 and 100. Interesting values: 50, 71, 76.
    :param s: Saturation of the generated color. Must be between 0 and 100.
    :return: A tuple of (r, g, b, a). a is always 1.
    """

AlphaOPAQUE = 255
AlphaTRANSPARENT = 0
ColorBLACK = 4278190080
ColorBLUE = 4278190335
ColorCYAN = 4278255615
ColorDKGRAY = 4282664004
ColorGRAY = 4287137928
ColorGREEN = 4278255360
ColorLTGRAY = 4291611852
ColorMAGENTA = 4294902015
ColorRED = 4294901760
ColorTRANSPARENT = 0
ColorWHITE = 4294967295
ColorYELLOW = 4294967040
kTileModeCount = 4
