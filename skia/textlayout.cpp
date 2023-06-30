#include "common.h"

void initTextlayout(py::module &m)
{
    py::module textlayout =
        m.def_submodule("textlayout", "This module provides an interface to the Skia text layout library.");

    initDartTypes(textlayout);
    initTextStyle(textlayout);
    initParagraphStyle(textlayout);
    initParagraph(textlayout);
}