#include "common.h"
#include "include/core/SkCanvas.h"
#include "include/core/SkData.h"
#include "include/core/SkMatrix.h"
#include "include/core/SkPicture.h"
#include "include/core/SkPictureRecorder.h"

class PyPicture : public SkPicture
{
public:
    void playback(SkCanvas *canvas, SkPicture::AbortCallback *callback = nullptr) const override
    {
        PYBIND11_OVERRIDE_PURE(void, SkPicture, playback, canvas, callback);
    }
    SkRect cullRect() const override { PYBIND11_OVERRIDE_PURE(SkRect, SkPicture, cullRect); }
    int approximateOpCount(bool nested = false) const override
    {
        PYBIND11_OVERRIDE_PURE(int, SkPicture, approximateOpCount, nested);
    }
    size_t approximateBytesUsed() const override { PYBIND11_OVERRIDE_PURE(size_t, SkPicture, approximateBytesUsed); }
};

void initPicture(py::module &m)
{
    py::class_<SkPicture, PyPicture, sk_sp<SkPicture>>(m, "Picture")
        .def_static(
            "MakeFromData", [](const SkData *data) { return SkPicture::MakeFromData(data); },
            "Recreates :py:class:`Picture` that was serialized into data.", "data"_a)
        .def_static(
            "MakeFromData",
            [](const py::buffer &data)
            {
                const py::buffer_info bufInfo = data.request();
                return SkPicture::MakeFromData(bufInfo.ptr, bufInfo.size);
            },
            "data"_a)
        .def(
            "playback", [](const SkPicture &self, SkCanvas *canvas) { self.playback(canvas); },
            "Replays the drawing commands on the specified canvas.", "canvas"_a)
        .def("cullRect", &SkPicture::cullRect)
        .def("uniqueID", &SkPicture::uniqueID)
        .def(
            "serialize", [](const SkPicture &self) { return self.serialize(); },
            "Returns storage containing :py:class:`Data` describing :py:class:`Picture`.")
        .def_static("MakePlaceholder", &SkPicture::MakePlaceholder, "cull"_a)
        .def(py::init(&SkPicture::MakePlaceholder),
             "Returns a placeholder :py:class:`Picture` of the specified dimensions *cull*.", "cull"_a)
        .def("approximateOpCount", &SkPicture::approximateOpCount, "nested"_a = false)
        .def("approximateBytesUsed", &SkPicture::approximateBytesUsed)
        .def("makeShader",
             py::overload_cast<SkTileMode, SkTileMode, SkFilterMode, const SkMatrix *, const SkRect *>(
                 &SkPicture::makeShader, py::const_),
             "tmx"_a, "tmy"_a, "mode"_a, "localMatrix"_a = nullptr, "tileRect"_a = nullptr);

    py::class_<SkPictureRecorder>(m, "PictureRecorder")
        .def(py::init())
        .def(
            "beginRecording",
            [](SkPictureRecorder &recorder, const SkRect &bounds) { return recorder.beginRecording(bounds); },
            "Returns the canvas that records the drawing commands with the bounds.", "bounds"_a,
            py::return_value_policy::reference_internal)
        .def(
            "beginRecording",
            [](SkPictureRecorder &recorder, const SkScalar &width, const SkScalar &height)
            { return recorder.beginRecording(width, height, nullptr); },
            "Returns the canvas that records the drawing commands with a bounding box of width and height.", "width"_a,
            "height"_a, py::return_value_policy::reference_internal)
        .def("getRecordingCanvas", &SkPictureRecorder::getRecordingCanvas, py::return_value_policy::reference_internal)
        .def("finishRecordingAsPicture", &SkPictureRecorder::finishRecordingAsPicture)
        .def("finishRecordingAsPictureWithCull", &SkPictureRecorder::finishRecordingAsPictureWithCull, "cullRect"_a);
}