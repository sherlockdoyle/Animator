#include "common.h"
#include "include/core/SkCanvas.h"
#include "include/core/SkData.h"
#include "include/core/SkMatrix.h"
#include "include/core/SkPicture.h"

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

// class PyBBoxHierarchy : public SkBBoxHierarchy
// {
// public:
//     using SkBBoxHierarchy::SkBBoxHierarchy;
//     void insert(const SkRect rects[], int N) override
//     {
//         PYBIND11_OVERRIDE_PURE(void, SkBBoxHierarchy, insert, rects, N);
//     }
//     void search(const SkRect &query, std::vector<int> *results) const override
//     {
//         PYBIND11_OVERRIDE_PURE(void, SkBBoxHierarchy, search, query, results);
//     }
//     size_t bytesUsed() const override { PYBIND11_OVERRIDE_PURE(size_t, SkBBoxHierarchy, bytesUsed); }
// };

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
             "tmx"_a, "tmy"_a, "mode"_a, "localMatrix"_a = py::none(), "tileRect"_a = py::none());

    // py::class_<SkDrawable, sk_sp<SkDrawable>, SkFlattenable>(m, "Drawable",
    //                                                          R"doc(
    // Base-class for objects that draw into :py:class:`Canvas`.

    // The object has a generation ID, which is guaranteed to be unique across all
    // drawables. To allow for clients of the drawable that may want to cache the
    // results, the drawable must change its generation ID whenever its internal
    // state changes such that it will draw differently.
    // )doc")
    //     .def("draw", py::overload_cast<SkCanvas *, const SkMatrix *>(&SkDrawable::draw),
    //          R"doc(
    //     Draws into the specified content.

    //     The drawing sequence will be balanced upon return (i.e. the
    //     ``saveLevel()`` on the canvas will match what it was when
    //     :py:meth:`draw` was called, and the current matrix and clip settings
    //     will not be changed.
    //     )doc",
    //          "canvas"_a.none(false), "matrix"_a = nullptr)
    //     .def("draw", py::overload_cast<SkCanvas *, SkScalar, SkScalar>(&SkDrawable::draw),
    //          "canvas"_a.none(false), "x"_a, "y"_a)
    //     // .def("snapGpuDrawHandler", &SkDrawable::snapGpuDrawHandler)
    //     .def("newPictureSnapshot", [](SkDrawable &drawable) { return
    //     sk_sp<SkPicture>(drawable.newPictureSnapshot());
    //     }) .def("getGenerationID", &SkDrawable::getGenerationID,
    //          R"doc(
    //     Return a unique value for this instance.

    //     If two calls to this return the same value, it is presumed that calling
    //     the draw() method will render the same thing as well.

    //     Subclasses that change their state should call
    //     :py:meth:`notifyDrawingChanged` to ensure that a new value will be
    //     returned the next time it is called.
    //     )doc")
    //     .def("getBounds", &SkDrawable::getBounds,
    //          R"doc(
    //     Return the (conservative) bounds of what the drawable will draw.

    //     If the drawable can change what it draws (e.g. animation or in response
    //     to some external change), then this must return a bounds that is always
    //     valid for all possible states.
    //     )doc")
    //     .def("notifyDrawingChanged", &SkDrawable::notifyDrawingChanged,
    //          R"doc(
    //     Calling this invalidates the previous generation ID, and causes a new
    //     one to be computed the next time getGenerationID() is called.

    //     Typically this is called by the object itself, in response to its
    //     internal state changing.
    //     )doc");

    // py::class_<SkBBHFactory>(m, "BBHFactory");

    // py::class_<SkBBoxHierarchy, PyBBoxHierarchy, sk_sp<SkBBoxHierarchy>, SkRefCnt> bboxhierarchy(m,
    // "BBoxHierarchy");

    // py::class_<SkBBoxHierarchy::Metadata>(bboxhierarchy, "Metadata")
    //     .def_readwrite("isDraw", &SkBBoxHierarchy::Metadata::isDraw);

    // bboxhierarchy.def(py::init())
    //     .def("insert", py::overload_cast<const SkRect[], int>(&SkBBoxHierarchy::insert),
    //          R"doc(
    //     Insert N bounding boxes into the hierarchy.
    //     )doc",
    //          "rects"_a, "N"_a)
    //     .def("insert",
    //          py::overload_cast<const SkRect[], const SkBBoxHierarchy::Metadata[], int>(&SkBBoxHierarchy::insert),
    //          "rects"_a, "metadata"_a, "N"_a)
    //     .def("search", &SkBBoxHierarchy::search,
    //          R"doc(
    //     Populate results with the indices of bounding boxes intersecting that
    //     query.
    //     )doc",
    //          "query"_a, "results"_a)
    //     .def("bytesUsed", &SkBBoxHierarchy::bytesUsed,
    //          R"doc(
    //     Return approximate size in memory of this.
    //     )doc");

    // py::class_<SkPictureRecorder> picturerecorder(m, "PictureRecorder");

    // py::enum_<SkPictureRecorder::FinishFlags>(picturerecorder, "FinishFlags");

    // picturerecorder
    //     .def(py::init())
    //     // .def("beginRecording",
    //     //     py::overload_cast<const SkRect&, sk_sp<SkBBoxHierarchy>, uint32_t>(
    //     //         &SkPictureRecorder::beginRecording),
    //     //     "Returns the canvas that records the drawing commands.")
    //     .def(
    //         "beginRecording",
    //         [](SkPictureRecorder &recorder, const SkRect &bounds) { return recorder.beginRecording(bounds,
    //         nullptr);
    //         }, R"doc(
    //     Returns the canvas that records the drawing commands.

    //     :bounds: the cull rect used when recording this picture. Any
    //         drawing the falls outside of this rect is undefined, and may be
    //         drawn or it may not.
    //     :return: the canvas.
    //     )doc",
    //         "bounds"_a, py::return_value_policy::reference_internal)
    //     .def(
    //         "beginRecording",
    //         [](SkPictureRecorder &recorder, SkScalar width, SkScalar height)
    //         { return recorder.beginRecording(width, height, nullptr); },
    //         "width"_a, "height"_a, py::return_value_policy::reference_internal)
    //     .def("getRecordingCanvas", &SkPictureRecorder::getRecordingCanvas,
    //          R"doc(
    //     Returns the recording canvas if one is active, or NULL if recording is
    //     not active.

    //     This does not alter the refcnt on the canvas (if present).
    //     )doc",
    //          py::return_value_policy::reference_internal)
    //     .def("finishRecordingAsPicture", &SkPictureRecorder::finishRecordingAsPicture,
    //          R"doc(
    //     Signal that the caller is done recording.

    //     This invalidates the canvas returned by :py:meth:`beginRecording` or
    //     :py:meth:`getRecordingCanvas`. Ownership of the object is passed to the
    //     caller, who must call unref() when they are done using it.

    //     The returned picture is immutable. If during recording drawables were
    //     added to the canvas, these will have been "drawn" into a recording
    //     canvas, so that this resulting picture will reflect their current state,
    //     but will not contain a live reference to the drawables themselves.
    //     )doc")
    //     .def("finishRecordingAsPictureWithCull", &SkPictureRecorder::finishRecordingAsPictureWithCull,
    //          R"doc(
    //     Signal that the caller is done recording, and update the cull rect to
    //     use for bounding box hierarchy (BBH) generation.

    //     The behavior is the same as calling :py:meth:`finishRecordingAsPicture`,
    //     except that this method updates the cull rect initially passed into
    //     beginRecording.

    //     :param skia.Rect cullRect: the new culling rectangle to use as the
    //         overall bound for BBH generation and subsequent culling operations.
    //     :return: the picture containing the recorded content.
    //     )doc",
    //          "cullRect"_a)
    //     .def("finishRecordingAsDrawable", &SkPictureRecorder::finishRecordingAsDrawable,
    //          R"doc(
    //     Signal that the caller is done recording.

    //     This invalidates the canvas returned by :py:meth:`beginRecording` or
    //     :py:meth:`getRecordingCanvas`. Ownership of the object is passed to the
    //     caller, who must call unref() when they are done using it.

    //     Unlike :py:meth:`finishRecordingAsPicture`, which returns an immutable
    //     picture, the returned drawable may contain live references to other
    //     drawables (if they were added to the recording canvas) and therefore
    //     this drawable will reflect the current state of those nested drawables
    //     anytime it is drawn or a new picture is snapped from it (by calling
    //     drawable.newPictureSnapshot()).
    //     )doc")
    ;
}