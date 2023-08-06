#include "../lib_geometry/EdgeTag.h"

#include <pybind11/stl.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

void init_EdgeTag(py::module &m) {

    py::class_<EdgeTag>(m, "EdgeTag")
    .def(py::init())
    .def(py::init<unsigned int,unsigned int,std::string>())
    .def("setIndices",&EdgeTag::setIndices,"setIndices")
    .def("setTag",&EdgeTag::setTag,"setTag")
    .def("getIndex1",&EdgeTag::getIndex1,"getIndex1")
    .def("getTag",&EdgeTag::getTag,"getTag")
    .def("getIndex2",&EdgeTag::getIndex2,"getIndex2")
    .def("getSpec",&EdgeTag::getSpec,"getSpec")
    .def("setOnSpec",&EdgeTag::setOnSpec,"setOnSpec")
    .def("valid",&EdgeTag::valid,"valid")
    .def("matches",py::overload_cast<unsigned int, unsigned int>(&EdgeTag::matches,py::const_),"matches")
    .def("matches",py::overload_cast<unsigned int, unsigned int, std::string>(&EdgeTag::matches,py::const_),"matches")
    .def("print",&EdgeTag::print,"print")   
    ;

}
