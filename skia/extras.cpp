#include "common.h"

void initExtras(py::module &m)
{
    initUniqueColor(m);

    py::module plot = m.def_submodule("plot",
                                      R"doc(
            This module provides alternate to functions that allows numpy arrays to be used for the :class:`Plot`
            entity. Class methods of the form ``Class.method`` have alternate implementations as ``Class_method`` that
            take a numpy array as some of it's arguments.
        )doc");
    initPlot(plot);
}