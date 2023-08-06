#include "../lib_geometry/XYPatternBlock.h"

#include <pybind11/stl.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

void init_XYPatternBlock(py::module &m) {
    
    py::class_<XYPatternBlock>(m, "XYPatternBlock")
    .def(py::init())
    //Interface for setting parameters
    .def("setParam", py::overload_cast<std::string, std::string>(&XYPatternBlock::setParam))
    .def("setParam", py::overload_cast<std::string, double>(&XYPatternBlock::setParam))
    .def("addIDPoint", &XYPatternBlock::addIDPoint)
    .def("setCoreWidth", &XYPatternBlock::setCoreWidth, py::arg("v"))
    .def("setAutoDrop", &XYPatternBlock::setAutoDrop, py::arg("v"))

    //Interface for building components
    .def("buildCompositeSegList", &XYPatternBlock::buildCompositeSegList, py::arg("osx"), py::arg("osy"))
    
    //Interface for getting information
    .def("distanceToClosestEntry", &XYPatternBlock::distanceToClosestEntry
        ,"By default, any_segment is set to true and the shortest distance is calculated by considering the endpoints of ANY of the lane segments. If any_segment is false, only the first,last (or outer) lane segments are considered.\n Returns: -1 if there are any problems or Distance to the shortest entry point.")
    .def("distanceToCrossAxis", &XYPatternBlock::distanceToCrossAxis)
    
    .def("getLanePoints", &XYPatternBlock::getLanePoints
        ,"Produce a set of points on either side of a center point (cptx, cpty) at angles perpendicular to the given angle.")
    .def("getLaneSegments", &XYPatternBlock::getLaneSegments
        ,"Produce a set of line segments of the given length (blocklen) at the given angle, each with the one of the given points (pts) as the center point.")
    .def("getCompositeSegList", &XYPatternBlock::getCompositeSegList
        ,"Produce a single XYSegList comprised of each of the given XYSegLists. Each given XYSegList should be a single line segment. Each line segment should be parallel and in order.")
    ;
}
