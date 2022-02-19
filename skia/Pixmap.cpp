#include "common.h"
#include "include/core/SkPixmap.h"
// #include <optional>
// #include <pybind11/numpy.h>
#include <pybind11/stl.h>

template <bool readonly = true> py::memoryview Pixmap_addr(const SkPixmap &pixmap)
{
    if (pixmap.addr() == nullptr)
        throw std::runtime_error("Pixmap is empty.");
    return py::memoryview::from_memory(pixmap.writable_addr(), pixmap.computeByteSize(), readonly);
}

template <typename T> py::memoryview Pixmap_addrN(const SkPixmap &pixmap)
{
    const size_t tSize = sizeof(T);
    const int pixelSize = pixmap.info().bytesPerPixel();
    if (pixelSize != tSize)
        throw std::runtime_error("Pixmap pixel size mismatch. Pixel size is " + std::to_string(pixelSize * 8) + ".");
    if (pixmap.addr() == nullptr)
        throw std::runtime_error("Pixmap is empty.");
    return py::memoryview::from_buffer(reinterpret_cast<const T *>(pixmap.addr()), tSize,
                                       py::format_descriptor<T>::value, {pixmap.rowBytesAsPixels(), pixmap.height()},
                                       {pixmap.rowBytes(), tSize});
}

void initPixmap(py::module &m)
{
    py::class_<SkPixmap>(m, "Pixmap", py::buffer_protocol(), R"doc(
        :py:class:`Pixmap` provides a utility to pair :py:class:`ImageInfo` with pixels and row bytes. The buffer
        protocol is supported. It is possible to mount :py:class:`Pixmap` as array::

            array = np.array(pixmap, copy=False)

        Or mount array as :py:class:`Pixmap` with :py:class:`ImageInfo`::

            buffer = np.zeros((100, 100, 4), np.uint8)
            array = skia.Pixmap(skia.ImageInfo.MakeN32Premul(100, 100), buffer)
    )doc")
        .def_buffer(
            [](SkPixmap &self)
            {
                if (self.addr() == nullptr)
                    throw std::runtime_error("Pixmap is empty");
                return imageInfoToBufferInfo(self.info(), self.writable_addr(), self.rowBytes(), false);
            })
        .def(
            "tobytes",
            [](const SkPixmap &self)
            { return py::bytes(reinterpret_cast<const char *>(self.addr()), self.computeByteSize()); },
            "Convert :py:class:`Pixmap` to bytes.")
        .def(py::init())
        .def(py::init(
                 [](const SkImageInfo &info, const std::optional<py::buffer> &addr, size_t rowBytes)
                 {
                     if (addr)
                     {
                         py::buffer_info buf = addr->request();
                         rowBytes = validateImageInfo_Buffer(info, buf, rowBytes);
                         return SkPixmap(info, buf.ptr, rowBytes);
                     }
                     return SkPixmap(info, nullptr, rowBytes == 0 ? info.minRowBytes() : rowBytes);
                 }),
             R"doc(
                Creates :py:class:`Pixmap` from info width, height, :py:class:`AlphaType`, and :py:class:`ColorType`,
                and a buffer *addr*.
            )doc",
             "info"_a, "addr"_a, "rowBytes"_a = 0, py::keep_alive<1, 3>())
        .def(py::init(
                 [](py::array &array, const SkColorType &ct, const SkAlphaType &at, const sk_sp<SkColorSpace> &cs)
                 { return SkPixmap(ndarrayToImageInfo(array, ct, at, cs), array.mutable_data(), array.strides(0)); }),
             "Creates :py:class:`Pixmap` backed by numpy array.", "array"_a, "colorType"_a = kN32_SkColorType,
             "alphaType"_a = kUnpremul_SkAlphaType, "colorSpace"_a = py::none(), py::keep_alive<1, 2>())
        .def("reset", py::overload_cast<>(&SkPixmap::reset))
        .def(
            "reset",
            [](SkPixmap &self, const SkImageInfo &imageInfo, const std::optional<py::buffer> &addr, size_t rowBytes)
            {
                if (addr)
                {
                    py::buffer_info buf = addr->request();
                    rowBytes = validateImageInfo_Buffer(imageInfo, buf, rowBytes);
                    self.reset(imageInfo, buf.ptr, rowBytes);
                }
                else
                    self.reset(imageInfo, nullptr, rowBytes == 0 ? imageInfo.minRowBytes() : rowBytes);
            },
            "Sets width, height, :py:class:`AlphaType`, and :py:class:`ColorType` from info, and a buffer *addr*.",
            "info"_a, "addr"_a, "rowBytes"_a = 0, py::keep_alive<1, 3>())
        .def("setColorSpace", &SkPixmap::setColorSpace, "colorSpace"_a)
        .def(
            "extractSubset",
            [](const SkPixmap &self, const SkIRect &area)
            {
                SkPixmap subset;
                if (self.extractSubset(&subset, area))
                    return subset;
                throw std::runtime_error("Resulting subset is empty");
            },
            "Returns a new :py:class:`Pixmap` with subset of the original :py:class:`Pixmap` specified by *area*.",
            "area"_a)
        .def("info", &SkPixmap::info, py::return_value_policy::reference_internal)
        .def("rowBytes", &SkPixmap::rowBytes)
        .def("addr", &Pixmap_addr<true>, "Returns the pixels as a ``memoryview``.")
        .def("width", &SkPixmap::width)
        .def("height", &SkPixmap::height)
        .def("dimensions", &SkPixmap::dimensions)
        .def("colorType", &SkPixmap::colorType)
        .def("alphaType", &SkPixmap::alphaType)
        .def("colorSpace", &SkPixmap::colorSpace, py::return_value_policy::reference_internal)
        .def("refColorSpace", &SkPixmap::refColorSpace)
        .def("isOpaque", &SkPixmap::isOpaque)
        .def("bounds", &SkPixmap::bounds)
        .def("rowBytesAsPixels", &SkPixmap::rowBytesAsPixels)
        .def("shiftPerPixel", &SkPixmap::shiftPerPixel)
        .def("computeByteSize", &SkPixmap::computeByteSize)
        .def("computeIsOpaque", &SkPixmap::computeIsOpaque)
        .def("getColor", &SkPixmap::getColor, "x"_a, "y"_a)
        .def("getAlphaf", &SkPixmap::getAlphaf, "x"_a, "y"_a)
        .def("addr8", &Pixmap_addrN<uint8_t>)
        .def("addr16", &Pixmap_addrN<uint16_t>)
        .def("addr32", &Pixmap_addrN<uint32_t>)
        .def("addr64", &Pixmap_addrN<uint64_t>)
        .def("addrF16", &Pixmap_addrN<uint16_t>)
        .def("writable_addr", &Pixmap_addr<false>)
        .def("readPixels", &readPixels<SkPixmap>,
             "Copies *dstInfo* pixels starting from (*srcX*, *srcY*) to *dstPixels* buffer.", "dstInfo"_a,
             "dstPixels"_a, "dstRowBytes"_a = 0, "srcX"_a = 0, "srcY"_a = 0)
        .def("readPixels", py::overload_cast<const SkPixmap &, int, int>(&SkPixmap::readPixels, py::const_), "dst"_a,
             "srcX"_a = 0, "srcY"_a = 0)
        .def("scalePixels", &SkPixmap::scalePixels, "dst"_a, "sampling"_a)
        .def("erase", py::overload_cast<SkColor, const SkIRect &>(&SkPixmap::erase, py::const_), "color"_a, "subset"_a)
        .def("erase", py::overload_cast<SkColor>(&SkPixmap::erase, py::const_), "color"_a)
        .def("erase",
             py::overload_cast<const SkColor4f &, SkColorSpace *, const SkIRect *>(&SkPixmap::erase, py::const_),
             "color"_a, "cs"_a = py::none(), "subset"_a = py::none())
        .def("__str__",
             [](const SkPixmap &self)
             {
                 return "Pixmap({} x {}, colorType={}, alphaType={}, colorSpace={})"_s.format(
                     self.width(), self.height(), self.colorType(), self.alphaType(), self.colorSpace());
             });

    //     py::class_<SkYUVAPixmapInfo> yuvapixmapinfo(m, "YUVAPixmapInfo",
    //                                                 R"doc(
    //     :py:class:`~skia.YUVAInfo` combined with per-plane
    //     :py:class:`~skia.ColorType` and row bytes. Fully specifies the
    //     :py:class:`~skia.Pixmaps` for a YUVA image without the actual pixel memory
    //     and data.
    //     )doc");

    //     py::enum_<SkYUVAPixmapInfo::DataType>(yuvapixmapinfo, "DataType",
    //                                           R"doc(
    //     Data type for Y, U, V, and possibly A channels independent of how values are
    //     packed into planes.
    //     )doc")
    //         .value("kUnorm8", SkYUVAPixmapInfo::DataType::kUnorm8, "8 bit unsigned normalized")
    //         .value("kUnorm16", SkYUVAPixmapInfo::DataType::kUnorm16, "16 bit unsigned normalized")
    //         .value("kFloat16", SkYUVAPixmapInfo::DataType::kFloat16, "16 bit (half) floating point")
    //         .value("kUnorm10_Unorm2", SkYUVAPixmapInfo::DataType::kUnorm10_Unorm2,
    //                "10 bit unorm for Y, U, and V. 2 bit unorm for alpha (if present).")
    //         .value("kLast", SkYUVAPixmapInfo::DataType::kLast)
    //         .export_values();

    //     py::class_<SkYUVAPixmapInfo::SupportedDataTypes>(yuvapixmapinfo, "SupportedDataTypes")
    //         .def(py::init<>(),
    //              R"doc(
    //         Defaults to nothing supported.
    //         )doc")
    //         .def(py::init<const GrImageContext &>(),
    //              R"doc(
    //         Init based on texture formats supported by the context.
    //         )doc",
    //              "context"_a)
    //         .def_static("All", &SkYUVAPixmapInfo::SupportedDataTypes::All,
    //                     R"doc(
    //         All legal combinations of PlanarConfig and DataType are supported.
    //         )doc")
    //         .def("supported", &SkYUVAPixmapInfo::SupportedDataTypes::supported,
    //              R"doc(
    //         Checks whether there is a supported combination of color types for
    //         planes structured as indicated by PlanarConfig with channel data types
    //         as indicated by DataType.
    //         )doc",
    //              "planarConfig"_a, "dataType"_a)
    //         .def("enableDataType", &SkYUVAPixmapInfo::SupportedDataTypes::enableDataType,
    //              R"doc(
    //         Update to add support for pixmaps with numChannel channels where each
    //         channel is represented as DataType.
    //         )doc",
    //              "dataType"_a, "numChannels"_a);

    //     yuvapixmapinfo.def_readonly_static("kMaxPlanes", &SkYUVAPixmapInfo::kMaxPlanes)
    //         .def_static("DefaultColorTypeForDataType", &SkYUVAPixmapInfo::DefaultColorTypeForDataType,
    //                     R"doc(
    //         Gets the default SkColorType to use with numChannels channels, each
    //         represented as DataType. Returns kUnknown_SkColorType if no such color
    //         type.
    //         )doc",
    //                     "dataType"_a, "numChannels"_a)
    //         .def_static("NumChannelsAndDataType", &SkYUVAPixmapInfo::NumChannelsAndDataType,
    //                     R"doc(
    //         If the :py:class:`ColorType` is supported for YUVA pixmaps this will
    //         return the number of YUVA channels that can be stored in a plane of
    //         this color type and what the DataType is of those channels. If the
    //         :py:class:`ColorType` is not supported as a YUVA plane the number of
    //         channels is reported as 0 and the DataType returned should be
    //         ignored.
    //         )doc",
    //                     "colorType"_a)
    //         .def(py::init<>(),
    //              R"doc(
    //         Default SkYUVAPixmapInfo is invalid.
    //         )doc")
    //         .def(py::init([](const SkYUVAInfo &info, const std::vector<SkColorType> &colorType, py::object
    //         rowBytesOrNone) {
    //                  std::vector<size_t> rowBytes;
    //                  if (!rowBytesOrNone.is_none())
    //                      rowBytes = rowBytesOrNone.cast<std::vector<size_t>>();
    //                  if (colorType.size() < SkYUVAPixmapInfo::kMaxPlanes)
    //                      throw py::value_error(
    //                          py::str("colorType must have {} elements").format(SkYUVAPixmapInfo::kMaxPlanes));
    //                  if (!rowBytes.empty() && (rowBytes.size() < SkYUVAPixmapInfo::kMaxPlanes))
    //                      throw py::value_error(
    //                          py::str("rowBytes must have {} elements").format(SkYUVAPixmapInfo::kMaxPlanes));
    //                  return SkYUVAPixmapInfo(info, colorType.data(), (rowBytes.empty()) ? nullptr : rowBytes.data());
    //              }),
    //              R"doc(
    //         Initializes the :py:class:`YUVAPixmapInfo` from a :py:class:`YUVAInfo`
    //         with per-plane color types and row bytes. This will be invalid if the
    //         colorTypes aren't compatible with the :py:class:`YUVAInfo` or if a
    //         rowBytes entry is not valid for the plane dimensions and color type.
    //         Color type and row byte values beyond the number of planes in
    //         :py:class:`YUVAInfo` are ignored. All :py:class:`ColorTypes` must have
    //         the same DataType or this will be invalid.

    //         If rowBytes is nullptr then ``bpp*width`` is assumed for each plane.
    //         )doc",
    //              "info"_a, "colorType"_a, "rowBytes"_a = nullptr)
    //         .def(py::init([](const SkYUVAInfo &info, SkYUVAPixmapInfo::DataType dataType, py::object rowBytesOrNone)
    //         {
    //                  std::vector<size_t> rowBytes;
    //                  if (!rowBytesOrNone.is_none())
    //                      rowBytes = rowBytesOrNone.cast<std::vector<size_t>>();
    //                  if (!rowBytes.empty() && (rowBytes.size() < SkYUVAPixmapInfo::kMaxPlanes))
    //                      throw py::value_error(
    //                          py::str("rowBytes must have {} elements").format(SkYUVAPixmapInfo::kMaxPlanes));
    //                  return SkYUVAPixmapInfo(info, dataType, (rowBytes.empty()) ? nullptr : rowBytes.data());
    //              }),
    //              R"doc(
    //         Like above but uses DefaultColorTypeForDataType to determine each
    //         plane's :py:class:`ColorType`. If rowBytes is nullptr then bpp*width is
    //         assumed for each plane.
    //         )doc",
    //              "info"_a, "dataType"_a, "rowBytes"_a = nullptr)
    //         .def(
    //             "__eq__", [](const SkYUVAPixmapInfo &self, const SkYUVAPixmapInfo &that) { return self == that; },
    //             py::is_operator())
    //         .def(
    //             "__ne__", [](const SkYUVAPixmapInfo &self, const SkYUVAPixmapInfo &that) { return self != that; },
    //             py::is_operator())
    //         .def("yuvaInfo", &SkYUVAPixmapInfo::yuvaInfo)
    //         .def("yuvColorSpace", &SkYUVAPixmapInfo::yuvColorSpace)
    //         .def("numPlanes", &SkYUVAPixmapInfo::numPlanes,
    //              R"doc(
    //         The number of :py:class:`Pixmap` planes, 0 if this
    //         :py:class:`YUVAPixmapInfo` is invalid.
    //         )doc")
    //         .def("dataType", &SkYUVAPixmapInfo::dataType,
    //              R"doc(
    //         The per-YUV[A] channel data type.
    //         )doc")
    //         .def("rowBytes", &SkYUVAPixmapInfo::rowBytes,
    //              R"doc(
    //         Row bytes for the ith plane. Returns zero if ``i >= numPlanes()`` or
    //         this :py:class:`YUVAPixmapInfo` is invalid.
    //         )doc",
    //              "i"_a)
    //         .def("planeInfo", &SkYUVAPixmapInfo::planeInfo,
    //              R"doc(
    //         Image info for the ith plane, or default :py:class:`ImageInfo` if
    //         ``i >= numPlanes()``
    //         )doc",
    //              "i"_a)
    //         .def(
    //             "computeTotalBytes",
    //             [](const SkYUVAPixmapInfo &self, bool returnPlaneSizes) -> py::object {
    //                 std::vector<size_t> planeSizes(SkYUVAPixmapInfo::kMaxPlanes);
    //                 auto size = self.computeTotalBytes(planeSizes.data());
    //                 if (returnPlaneSizes)
    //                     return py::make_tuple(size, planeSizes);
    //                 return py::cast(size);
    //             },
    //             R"doc(
    //         Determine size to allocate for all planes. Optionally returns the
    //         per-plane sizes if returnPlaneSizes is True. If total size overflows
    //         will return SIZE_MAX and set all planeSizes to SIZE_MAX. Returns 0 and
    //         fills planesSizes with 0 if this :py:class:`YUVAPixmapInfo` is not
    //         valid.
    //         )doc",
    //             "returnPlaneSizes"_a = false)
    //         .def(
    //             "initPixmapsFromSingleAllocation",
    //             [](const SkYUVAPixmapInfo &self, py::buffer b) {
    //                 auto buffer = b.request();
    //                 std::vector<SkPixmap> pixmaps(SkYUVAPixmapInfo::kMaxPlanes);
    //                 auto result = self.initPixmapsFromSingleAllocation(buffer.ptr, pixmaps.data());
    //                 if (!result)
    //                     throw std::runtime_error("Failed to initialize pixmaps.");
    //                 return pixmaps;
    //             },
    //             R"doc(
    //         Takes an allocation that is assumed to be at least
    //         :py:meth:`computeTotalBytes` in size and configures the first
    //         :py:meth:`numPlanes` entries in pixmaps array to point into that
    //         memory. The remaining entries of pixmaps are default initialized.
    //         Fails if this :py:class:`YUVAPixmapInfo` not valid.

    //         :param memory: Buffer that is at least  :py:meth:`computeTotalBytes` in
    //             size.
    //         :rtype: List[skia.Pixmap]
    //         )doc",
    //             "memory"_a)
    //         .def("isValid", &SkYUVAPixmapInfo::isValid,
    //              R"doc(
    //         Returns true if this has been configured with a non-empty dimensioned
    //         :py:class:`YUVAInfo` with compatible color types and row bytes.
    //         )doc")
    //         .def("isSupported", &SkYUVAPixmapInfo::isSupported,
    //              R"doc(
    //         Is this valid and does it use color types allowed by the passed
    //         :py:class:`SupportedDataTypes`?
    //         )doc",
    //              "supportedDataTypes"_a);

    //     py::class_<SkYUVAPixmaps>(m, "YUVAPixmaps",
    //                               R"doc(
    //     Helper to store :py:class:`Pixmap` planes as described by a
    //     :py:class:`YUVAPixmapInfo`. Can be responsible for
    //     allocating/freeing memory for pixmaps or use external memory.
    //     )doc")
    //         .def_static("Allocate", &SkYUVAPixmaps::Allocate,
    //                     R"doc(
    //         Allocate space for pixmaps' pixels in the :py:class:`YUVAPixmaps`.
    //         )doc",
    //                     "yuvaPixmapInfo"_a)
    //         .def_static("FromData", &SkYUVAPixmaps::FromData,
    //                     R"doc(
    //         Use storage in :py:class:`Data` as backing store for pixmaps' pixels.
    //         :py:class:`Data` is retained by the :py:class:`YUVAPixmaps`.
    //         )doc",
    //                     "yuvaPixmapInfo"_a, "data"_a)
    //         .def_static(
    //             "FromExternalMemory",
    //             [](const SkYUVAPixmapInfo &info, py::buffer b) {
    //                 auto buffer = b.request();
    //                 return SkYUVAPixmaps::FromExternalMemory(info, buffer.ptr);
    //             },
    //             R"doc(
    //         Use passed in memory as backing store for pixmaps' pixels. Caller must
    //         ensure memory remains allocated while pixmaps are in use. There must be
    //         at least :py:meth:`YUVAPixmapInfo.computeTotalBytes` allocated starting
    //         at memory.
    //         )doc",
    //             "yuvaPixmapInfo"_a, "memory"_a)
    //         .def_static(
    //             "FromExternalPixmaps",
    //             [](const SkYUVAInfo &info, const std::vector<SkPixmap> &pixmaps) {
    //                 if (pixmaps.size() < SkYUVAPixmaps::kMaxPlanes)
    //                     throw py::value_error(py::str("pixmaps must have {}
    //                     elements").format(SkYUVAPixmaps::kMaxPlanes));
    //                 return SkYUVAPixmaps::FromExternalPixmaps(info, pixmaps.data());
    //             },
    //             R"doc(
    //         Wraps existing :py:class:`Pixmap`. The :py:class:`YUVAPixmaps` will
    //         have no ownership of the :py:class:`Pixmap`' pixel memory so the
    //         caller must ensure it remains valid. Will return an invalid
    //         :py:class:`YUVAPixmaps` if the :py:class:`YUVAInfo` isn't compatible
    //         with the :py:class:`Pixmap` array (number of planes, plane dimensions,
    //         sufficient color channels in planes, ...).
    //         )doc",
    //             "yuvaInfo"_a, "pixmaps"_a)
    //         .def(py::init<>())
    //         .def("isValid", &SkYUVAPixmaps::isValid,
    //              R"doc(
    //         Does have initialized pixmaps compatible with its :py:class:`YUVAInfo`.
    //         )doc")
    //         .def("yuvaInfo", &SkYUVAPixmaps::yuvaInfo)
    //         .def("numPlanes", &SkYUVAPixmaps::numPlanes,
    //              R"doc(
    //         Number of pixmap planes or 0 if this :py:class:`YUVAPixmaps` is invalid.
    //         )doc")
    //         .def("planes", &SkYUVAPixmaps::planes,
    //              R"doc(
    //         Access the :py:class:`Pixmap` planes. They are default initialized if
    //         this is not a valid :py:class:`YUVAPixmaps`.
    //         )doc")
    //         .def("plane", &SkYUVAPixmaps::plane,
    //              R"doc(
    //         Get the ith :py:class:`Pixmap` plane. :py:class:`Pixmap` will be default
    //         initialized if i >= numPlanes or this :py:class:`YUVAPixmaps` is
    //         invalid.
    //         )doc",
    //              "i"_a)
    //         .def(
    //             "toLegacy",
    //             [](const SkYUVAPixmaps &self) {
    //                 SkYUVASizeInfo info;
    //                 std::vector<SkYUVAIndex> indices(SkYUVAPixmaps::kMaxPlanes);
    //                 self.toLegacy(&info, indices.data());
    //                 return py::make_tuple(info, indices);
    //             },
    //             R"doc(
    //         Conversion to legacy SkYUVA data structures.
    //         )doc");

    //     py::class_<SkYUVAIndex> yuvaindex(m, "YUVAIndex");

    //     py::enum_<SkYUVAIndex::Index>(yuvaindex, "Index")
    //         .value("kY_Index", SkYUVAIndex::kY_Index)
    //         .value("kU_Index", SkYUVAIndex::kU_Index)
    //         .value("kV_Index", SkYUVAIndex::kV_Index)
    //         .value("kA_Index", SkYUVAIndex::kA_Index)
    //         .value("kLast_Index", SkYUVAIndex::kLast_Index)
    //         .export_values();

    //     yuvaindex.def(py::init<>())
    //         .def(
    //             "__eq__", [](const SkYUVAIndex &self, const SkYUVAIndex &that) { return self == that; },
    //             py::is_operator())
    //         .def(
    //             "__ne__", [](const SkYUVAIndex &self, const SkYUVAIndex &that) { return self == that; },
    //             py::is_operator())
    //         .def_readonly_static("kIndexCount", &SkYUVAIndex::kIndexCount)
    //         .def_readwrite("fIndex", &SkYUVAIndex::fIndex,
    //                        R"doc(
    //         The index is a number between -1..3 which defines which image source
    //         to read from, where -1 means the image source doesn't exist. The
    //         assumption is we will always have image sources for each of YUV
    //         planes, but optionally have image source for A plane.
    //         )doc")
    //         .def_readwrite("fChannel", &SkYUVAIndex::fChannel,
    //                        R"doc(
    //         The channel describes from which channel to read the info from.
    //         Currently we only deal with YUV and NV12 and channel info is ignored.
    //         )doc")
    //         .def_static(
    //             "AreValidIndices",
    //             [](const std::vector<SkYUVAIndex> &yuvaIndices, bool returnNumPlanes) -> py::object {
    //                 int numPlanes = 0;
    //                 if (yuvaIndices.size() < 4)
    //                     throw py::value_error("yuvaIndices must have 4 elements.");
    //                 auto result = SkYUVAIndex::AreValidIndices(yuvaIndices.data(), &numPlanes);
    //                 if (returnNumPlanes)
    //                     return py::make_tuple(result, numPlanes);
    //                 return py::cast(result);
    //             },
    //             "yuvaIndices"_a, "returnNumPlanes"_a = false);

    //     py::class_<SkYUVASizeInfo>(m, "YUVASizeInfo")
    //         .def(py::init<>())
    //         .def_property(
    //             "fSizes",
    //             [](const SkYUVASizeInfo &self) {
    //                 return std::vector<SkISize>(self.fSizes, self.fSizes + SkYUVASizeInfo::kMaxCount);
    //             },
    //             [](SkYUVASizeInfo &self, const std::vector<SkISize> &value) {
    //                 if (value.size() != SkYUVASizeInfo::kMaxCount)
    //                     throw py::value_error(py::str("value must have {}
    //                     elements.").format(SkYUVASizeInfo::kMaxCount));
    //                 std::copy(value.begin(), value.end(), self.fSizes);
    //             })
    //         .def_property(
    //             "fWidthBytes",
    //             [](const SkYUVASizeInfo &self) {
    //                 return std::vector<size_t>(self.fWidthBytes, self.fWidthBytes + SkYUVASizeInfo::kMaxCount);
    //             },
    //             [](SkYUVASizeInfo &self, const std::vector<size_t> &value) {
    //                 if (value.size() != SkYUVASizeInfo::kMaxCount)
    //                     throw py::value_error(py::str("value must have {}
    //                     elements.").format(SkYUVASizeInfo::kMaxCount));
    //                 std::copy(value.begin(), value.end(), self.fWidthBytes);
    //             },
    //             R"doc(
    //         While the widths of the Y, U, V and A planes are not restricted, the
    //         implementation often requires that the width of the memory allocated
    //         for each plane be a multiple of 8.

    //         This struct allows us to inform the client how many "widthBytes"
    //         that we need.  Note that we use the new idea of "widthBytes"
    //         because this idea is distinct from "rowBytes" (used elsewhere in
    //         Skia).  "rowBytes" allow the last row of the allocation to not
    //         include any extra padding, while, in this case, every single row of
    //         the allocation must be at least "widthBytes".
    //         )doc")
    //         .def_readwrite("fOrigin", &SkYUVASizeInfo::fOrigin,
    //                        R"doc(
    //         YUVA data often comes from formats like JPEG that support EXIF
    //         orientation. Code that operates on the raw YUV data often needs to
    //         know that orientation.
    //         )doc")
    //         .def(
    //             "__eq__", [](const SkYUVASizeInfo &self, const SkYUVASizeInfo &that) { return self == that; },
    //             py::is_operator())
    //         .def("computeTotalBytes", &SkYUVASizeInfo::computeTotalBytes)
    //         // .def("computePlanes", &SkYUVASizeInfo)
    //         ;
}