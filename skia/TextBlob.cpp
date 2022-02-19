#include "common.h"
#include "include/core/SkRSXform.h"
#include "include/core/SkSerialProcs.h"
#include "include/core/SkTextBlob.h"
#include <pybind11/stl.h>

void initTextBlob(py::module &m)
{
    py::class_<SkTextBlob, sk_sp<SkTextBlob>> TextBlob(m, "TextBlob");
    TextBlob
        .def(py::init(
                 [](const std::string &text, const SkFont &font, const std::optional<std::vector<SkPoint>> &pos,
                    const SkTextEncoding &encoding)
                 {
                     if (pos)
                     {
                         const size_t byteLength = text.size();
                         if (pos->size() != byteLength)
                             throw py::value_error("text and pos must be the same length");
                         return SkTextBlob::MakeFromPosText(text.c_str(), byteLength, pos->data(), font, encoding);
                     }
                     return SkTextBlob::MakeFromText(text.c_str(), text.size(), font, encoding);
                 }),
             "Creates a :py:class:`TextBlob` with a single run of *text* and optional *pos*.", "text"_a, "font"_a,
             "pos"_a = py::none(), "encoding"_a = SkTextEncoding::kUTF8)
        .def("bounds", &SkTextBlob::bounds)
        .def("uniqueID", &SkTextBlob::uniqueID)
        .def(
            "getIntercepts",
            [](const SkTextBlob &self, const std::vector<SkScalar> &bounds, const SkPaint *paint)
            {
                const size_t count = bounds.size();
                if (count != 2)
                    throw py::value_error("bounds must contain 2 elements");

                int numIntersects = self.getIntercepts(bounds.data(), nullptr, paint);
                std::vector<SkScalar> intervals(numIntersects);
                self.getIntercepts(bounds.data(), intervals.data(), paint);
                return intervals;
            },
            "Returns the number of intervals that intersect *bounds*.", "bounds"_a, "paint"_a = nullptr)
        .def_static(
            "MakeFromText",
            [](const std::string &text, const SkFont &font, const SkTextEncoding &encoding)
            { return SkTextBlob::MakeFromText(text.c_str(), text.size(), font, encoding); },
            "Creates :py:class:`TextBlob` with a single run of *text*.", "text"_a, "font"_a,
            "encoding"_a = SkTextEncoding::kUTF8)
        .def_static("MakeFromString", &SkTextBlob::MakeFromString, "string"_a, "font"_a,
                    "encoding"_a = SkTextEncoding::kUTF8)
        .def_static(
            "MakeFromPosTextH",
            [](const std::string &text, const std::vector<SkScalar> &xpos, const SkScalar &constY, const SkFont &font,
               const SkTextEncoding &encoding)
            {
                const size_t byteLength = text.size();
                if (xpos.size() != byteLength)
                    throw py::value_error("text and xpos must be the same length");
                return SkTextBlob::MakeFromPosTextH(text.c_str(), byteLength, xpos.data(), constY, font, encoding);
            },
            "Returns a :py:class:`TextBlob` built from a single run of *text* with *xpos* and a single *constY* value.",
            "text"_a, "xpos"_a, "constY"_a, "font"_a, "encoding"_a = SkTextEncoding::kUTF8)
        .def_static(
            "MakeFromPosText",
            [](const std::string &text, const std::vector<SkPoint> &pos, const SkFont &font,
               const SkTextEncoding &encoding)
            {
                const size_t byteLength = text.size();
                if (pos.size() != byteLength)
                    throw py::value_error("text and pos must be the same length");
                return SkTextBlob::MakeFromPosText(text.c_str(), byteLength, pos.data(), font, encoding);
            },
            "Returns a :py:class:`TextBlob` built from a single run of *text* with *pos*.", "text"_a, "pos"_a, "font"_a,
            "encoding"_a = SkTextEncoding::kUTF8)
        .def_static(
            "MakeFromRSXform",
            [](const std::string &text, const std::vector<SkRSXform> &xform, const SkFont &font,
               const SkTextEncoding &encoding)
            {
                const size_t byteLength = text.size();
                if (xform.size() != byteLength)
                    throw py::value_error("text and xform must be the same length");
                return SkTextBlob::MakeFromRSXform(text.c_str(), byteLength, xform.data(), font, encoding);
            },
            "text"_a, "xform"_a, "font"_a, "encoding"_a = SkTextEncoding::kUTF8)
        .def("serialize", [](const SkTextBlob &self) { return self.serialize(SkSerialProcs()); })
        .def_static(
            "Deserialize",
            [](const py::buffer &data)
            {
                const py::buffer_info bufInfo = data.request();
                return SkTextBlob::Deserialize(bufInfo.ptr, bufInfo.size * bufInfo.itemsize, SkDeserialProcs());
            },
            "Recreates :py:class:`TextBlob` that was serialized into data.", "data"_a)
        .def(
            "__iter__", [](const SkTextBlob &self) { return SkTextBlob::Iter(self); }, py::keep_alive<0, 1>())
        .def("__str__",
             [](const SkTextBlob &self)
             {
                 int runCount = 0, glyphCount = 0;
                 SkTextBlob::Iter::Run run;
                 SkTextBlob::Iter iter(self);
                 while (iter.next(&run))
                 {
                     ++runCount;
                     glyphCount += run.fGlyphCount;
                 }
                 return "TextBlob({} run{}, {} glyph{})"_s.format(runCount, runCount == 1 ? "" : "s", glyphCount,
                                                                  glyphCount == 1 ? "" : "s");
             });

    py::class_<SkTextBlob::Iter> Iter(TextBlob, "Iter");

    py::class_<SkTextBlob::Iter::Run>(Iter, "Run")
        .def_readonly("fTypeface", &SkTextBlob::Iter::Run::fTypeface, py::return_value_policy::reference)
        .def_readonly("fGlyphCount", &SkTextBlob::Iter::Run::fGlyphCount)
        .def_property_readonly(
            "fGlyphIndices", [](const SkTextBlob::Iter::Run &self)
            { return std::vector<uint16_t>(self.fGlyphIndices, self.fGlyphIndices + self.fGlyphCount); })
        .def("__str__",
             [](const SkTextBlob::Iter::Run &self)
             {
                 std::stringstream s;
                 s << "Run(typeFace={}"_s.format(self.fTypeface) << ", glyphCount=" << self.fGlyphCount
                   << ", glyphIndices=[";
                 for (int i = 0; i < self.fGlyphCount; ++i)
                 {
                     if (i > 0)
                         s << ", ";
                     s << self.fGlyphIndices[i];
                 }
                 s << "])";
                 return s.str();
             });

    Iter.def(py::init<const SkTextBlob &>())
        .def("next",
             [](SkTextBlob::Iter &self) -> std::optional<SkTextBlob::Iter::Run>
             {
                 SkTextBlob::Iter::Run run;
                 if (self.next(&run))
                     return run;
                 return std::nullopt;
             })
        .def(
            "__iter__", [](const SkTextBlob::Iter &self) { return self; }, py::keep_alive<0, 1>())
        .def("__next__",
             [](SkTextBlob::Iter &it)
             {
                 SkTextBlob::Iter::Run run;
                 if (it.next(&run))
                     return run;
                 throw py::stop_iteration();
             });

    py::class_<SkTextBlobBuilder>(m, "TextBlobBuilder", R"doc(
        In Skia, you call the ``alloc*`` methods of this class with the count of glyphs to create a ``RunBuffer``
        object. Then the object is filled with the required data before the next call to another method.

        However, in this Python binding, the ``alloc*`` methods do not return the ``RunBuffer`` object. Instead of
        passing the count of glyphs, you need to call them with the required data directly and it'll handle the
        allocation and data filling automatically. All the other parameters are the same as in the C++ API. You can
        optionally pass a *encoding* parameter to specify the encoding of the text. These methods return the
        :py:class:`TextBlobBuilder` object itself for method chaining.
    )doc")
        .def(py::init())
        .def("make", &SkTextBlobBuilder::make)
        .def(
            "allocRun",
            [](SkTextBlobBuilder &self, const SkFont &font, const std::string &text, const SkScalar &x,
               const SkScalar &y, const SkRect *bounds, const SkTextEncoding &encoding)
            {
                const int count = font.countText(text.c_str(), text.size(), encoding);

                SkTextBlobBuilder::RunBuffer run = self.allocRun(font, count, x, y, bounds);
                font.textToGlyphs(text.c_str(), text.size(), encoding, run.glyphs, count);
                return &self;
            },
            "Sets a new run with glyphs for *text*.", "font"_a, "text"_a, "x"_a, "y"_a, "bounds"_a = py::none(),
            "encoding"_a = SkTextEncoding::kUTF8)
        .def(
            "allocRunPosH",
            [](SkTextBlobBuilder &self, const SkFont &font, const std::string &text, const std::vector<SkScalar> &xpos,
               const SkScalar &y, const SkRect *bounds, const SkTextEncoding &encoding)
            {
                const int count = font.countText(text.c_str(), text.size(), encoding);
                if (xpos.size() != (unsigned)count)
                    throw py::value_error("xpos must be the same length as text");

                SkTextBlobBuilder::RunBuffer run = self.allocRunPosH(font, count, y, bounds);
                font.textToGlyphs(text.c_str(), text.size(), encoding, run.glyphs, count);
                std::copy(xpos.begin(), xpos.end(), run.pos);
                return &self;
            },
            "Sets a new run with glyphs for *text* at *xpos*.", "font"_a, "text"_a, "xpos"_a, "y"_a,
            "bounds"_a = py::none(), "encoding"_a = SkTextEncoding::kUTF8)
        .def(
            "allocRunPos",
            [](SkTextBlobBuilder &self, const SkFont &font, const std::string &text, const std::vector<SkPoint> &pos,
               const SkRect *bounds, const SkTextEncoding &encoding)
            {
                const int count = font.countText(text.c_str(), text.size(), encoding);
                if (pos.size() != (unsigned)count)
                    throw py::value_error("pos must be the same length as text");

                SkTextBlobBuilder::RunBuffer run = self.allocRunPos(font, count, bounds);
                font.textToGlyphs(text.c_str(), text.size(), encoding, run.glyphs, count);
                std::copy(pos.begin(), pos.end(), run.points());
                return &self;
            },
            "Sets a new run with glyphs for *text* at *pos*.", "font"_a, "text"_a, "pos"_a, "bounds"_a = py::none(),
            "encoding"_a = SkTextEncoding::kUTF8)
        .def(
            "allocRunRSXform",
            [](SkTextBlobBuilder &self, const SkFont &font, const std::string &text,
               const std::vector<SkRSXform> &xforms, const SkTextEncoding &encoding)
            {
                const int count = font.countText(text.c_str(), text.size(), encoding);
                if (xforms.size() != (unsigned)count)
                    throw py::value_error("xforms must be the same length as text");

                SkTextBlobBuilder::RunBuffer run = self.allocRunRSXform(font, count);
                font.textToGlyphs(text.c_str(), text.size(), encoding, run.glyphs, count);
                std::copy(xforms.begin(), xforms.end(), run.xforms());
                return &self;
            },
            "Sets a new run with glyphs for *text* with *xforms*.", "font"_a, "text"_a, "xforms"_a,
            "encoding"_a = SkTextEncoding::kUTF8)
        .def(
            "allocRunText",
            [](SkTextBlobBuilder &self, const SkFont &font, const std::string &text,
               const std::vector<uint32_t> &clusters, const SkScalar &x, const SkScalar &y, const std::string &utf8text,
               const SkRect *bounds, const SkTextEncoding &encoding)
            {
                const int count = font.countText(text.c_str(), text.size(), encoding);
                if (clusters.size() != (unsigned)count)
                    throw py::value_error("clusters must be the same length as text");

                SkTextBlobBuilder::RunBuffer run = self.allocRunText(font, count, x, y, utf8text.size(), bounds);
                font.textToGlyphs(text.c_str(), text.size(), encoding, run.glyphs, count);
                std::copy(clusters.begin(), clusters.end(), run.clusters);
                std::copy(utf8text.begin(), utf8text.end(), run.utf8text);
                return &self;
            },
            "Sets a new run with glyphs for *text* with supporting *clusters* and *utf8text*.", "font"_a, "text"_a,
            "clusters"_a, "x"_a, "y"_a, "utf8text"_a, "bounds"_a = py::none(), "encoding"_a = SkTextEncoding::kUTF8)
        .def(
            "allocRunTextPosH",
            [](SkTextBlobBuilder &self, const SkFont &font, const std::string &text,
               const std::vector<uint32_t> &clusters, const std::vector<SkScalar> &xpos, const SkScalar &y,
               const std::string &utf8text, const SkRect *bounds, const SkTextEncoding &encoding)
            {
                const int count = font.countText(text.c_str(), text.size(), encoding);
                if (clusters.size() != (unsigned)count || xpos.size() != (unsigned)count)
                    throw py::value_error("clusters and xpos must be the same length as text");

                SkTextBlobBuilder::RunBuffer run = self.allocRunTextPosH(font, count, y, utf8text.size(), bounds);
                font.textToGlyphs(text.c_str(), text.size(), encoding, run.glyphs, count);
                std::copy(xpos.begin(), xpos.end(), run.pos);
                std::copy(clusters.begin(), clusters.end(), run.clusters);
                std::copy(utf8text.begin(), utf8text.end(), run.utf8text);
                return &self;
            },
            "Sets a new run with glyphs for *text* at *xpos* with supporting *clusters* and *utf8text*.", "font"_a,
            "text"_a, "clusters"_a, "xpos"_a, "y"_a, "utf8text"_a, "bounds"_a = py::none(),
            "encoding"_a = SkTextEncoding::kUTF8)
        .def(
            "allocRunTextPos",
            [](SkTextBlobBuilder &self, const SkFont &font, const std::string &text,
               const std::vector<uint32_t> &clusters, const std::vector<SkPoint> &pos, const std::string &utf8text,
               const SkRect *bounds, const SkTextEncoding &encoding)
            {
                const int count = font.countText(text.c_str(), text.size(), encoding);
                if (clusters.size() != (unsigned)count || pos.size() != (unsigned)count)
                    throw py::value_error("clusters and pos must be the same length as text");

                SkTextBlobBuilder::RunBuffer run = self.allocRunTextPos(font, count, utf8text.size(), bounds);
                font.textToGlyphs(text.c_str(), text.size(), encoding, run.glyphs, count);
                std::copy(pos.begin(), pos.end(), run.points());
                std::copy(clusters.begin(), clusters.end(), run.clusters);
                std::copy(utf8text.begin(), utf8text.end(), run.utf8text);
                return &self;
            },
            "Sets a new run with glyphs for *text* at *pos* with supporting *clusters* and *utf8text*.", "font"_a,
            "text"_a, "clusters"_a, "pos"_a, "utf8text"_a, "bounds"_a = py::none(),
            "encoding"_a = SkTextEncoding::kUTF8)
        .def(
            "allocRunTextRSXform",
            [](SkTextBlobBuilder &self, const SkFont &font, const std::string &text,
               const std::vector<uint32_t> &clusters, const std::vector<SkRSXform> &xforms, const std::string &utf8text,
               const SkRect *bounds, const SkTextEncoding &encoding)
            {
                const int count = font.countText(text.c_str(), text.size(), encoding);
                if (clusters.size() != (unsigned)count || xforms.size() != (unsigned)count)
                    throw py::value_error("clusters and xforms must be the same length as text");

                SkTextBlobBuilder::RunBuffer run = self.allocRunTextRSXform(font, count, utf8text.size(), bounds);
                font.textToGlyphs(text.c_str(), text.size(), encoding, run.glyphs, count);
                std::copy(xforms.begin(), xforms.end(), run.xforms());
                std::copy(clusters.begin(), clusters.end(), run.clusters);
                std::copy(utf8text.begin(), utf8text.end(), run.utf8text);
                return &self;
            },
            "Sets a new run with glyphs for *text* with *xforms* and supporting *clusters* and *utf8text*.", "font"_a,
            "text"_a, "clusters"_a, "xforms"_a, "utf8text"_a, "bounds"_a = py::none(),
            "encoding"_a = SkTextEncoding::kUTF8);
}