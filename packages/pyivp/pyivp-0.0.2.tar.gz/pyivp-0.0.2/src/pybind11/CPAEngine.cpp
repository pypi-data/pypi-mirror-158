#include "../lib_geometry/CPAEngine.h"

// #include <pybind11/stl.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;




void init_CPAEngine(py::module &m) {
    
    py::class_<CPAEngine>(m, "CPAEngine")
    .def(py::init())
    .def(py::init<double, double, double, double, double, double>())
    .def("reset", &CPAEngine::reset)
    .def("initNonCache", &CPAEngine::initNonCache)
    .def("evalCPA", &CPAEngine::evalCPA)
    .def("evalTimeCPA", &CPAEngine::evalTimeCPA)
    .def("evalROC", &CPAEngine::evalROC)
    .def("evalRangeRateOverRange", &CPAEngine::evalRangeRateOverRange)
    .def("crossesStern", &CPAEngine::crossesStern)
    .def("crossesSternDist", &CPAEngine::crossesSternDist)
    .def("crossesSternDistBool", &CPAEngine::crossesSternDistBool)
    .def("crossesBow", &CPAEngine::crossesBow)
    .def("crossesBowDist", &CPAEngine::crossesBowDist)
    .def("crossesBowDistBool", &CPAEngine::crossesBowDistBool)
    .def("crossesBowOrStern", &CPAEngine::crossesBowOrStern)
    .def("passesPort", &CPAEngine::passesPort)
    .def("passesPortDist", &CPAEngine::passesPortDist)
    .def("passesPortDistBool", &CPAEngine::passesPortDistBool)
    .def("passesStar", &CPAEngine::passesStar)
    .def("passesStarDist", &CPAEngine::passesStarDist)
    .def("passesStarDistBool", &CPAEngine::passesStarDistBool)
    .def("passesPortOrStar", &CPAEngine::passesPortOrStar)
    .def("turnsRight", &CPAEngine::turnsRight)
    .def("turnsLeft", &CPAEngine::turnsLeft)
    .def("foreOfContact", &CPAEngine::foreOfContact)
    .def("aftOfContact", &CPAEngine::aftOfContact)
    .def("portOfContact", &CPAEngine::portOfContact)
    .def("starboardOfContact", &CPAEngine::starboardOfContact)
    .def("minMaxROC", &CPAEngine::minMaxROC)
    .def("bearingRate", &CPAEngine::bearingRate)
    .def("bearingRateOld", &CPAEngine::bearingRateOld)
    .def("ownshipContactRelBearing", &CPAEngine::ownshipContactRelBearing)
    .def("contactOwnshipRelBearing", &CPAEngine::contactOwnshipRelBearing)
    .def("ownshipContactAbsBearing", &CPAEngine::ownshipContactAbsBearing)
    .def("cnSpdToOS", &CPAEngine::cnSpdToOS)
    .def("getOSSpeedInCNHeading", &CPAEngine::getOSSpeedInCNHeading)
    .def("getOSSpeedGamma", &CPAEngine::getOSSpeedGamma)
    .def("getOSSpeedEpsilon", &CPAEngine::getOSSpeedEpsilon)
    .def("getOSTimeGamma", &CPAEngine::getOSTimeGamma)
    .def("getOSTimeEpsilon", &CPAEngine::getOSTimeEpsilon)
    .def("getCNSpeedInOSPos", &CPAEngine::getCNSpeedInOSPos)
    .def("getRangeGamma", &CPAEngine::getRangeGamma)
    .def("getRangeEpsilon", &CPAEngine::getRangeEpsilon)
    .def("getThetaGamma", &CPAEngine::getThetaGamma)
    .def("getThetaEpsilon", &CPAEngine::getThetaEpsilon)
    .def("getRange", &CPAEngine::getRange)
    .def("getARange", &CPAEngine::getARange)
    .def("getARangeRate", &CPAEngine::getARangeRate);
}