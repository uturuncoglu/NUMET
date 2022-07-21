# NUMET

NUMET is the Nuopc Unified Modeling Environment Toolkit

The goal of NUMET is to unify, provide, and maintain those parts of NUOPC-based modeling systems that are common across most such implementations. This includes the top level application and driver implementation, parts of the build infrastructure, and tools for run configuration management.

The objectives of NUMET are:
 - Simplification of standing up new NUOPC-based systems.
 - Reduction of maintenance cost for established NUOPC-based systems.
 - Improved alignment and interoperability between different NUOPC-based systems. (Configuration files, procedures, etc.)
 - Faster and more coordinated role out of new NUOPC/ESMF features.

The approach of NUMET is to provide a software component that can be pulled into any modeling system as a Git submodule from GitHub. The concrete pieces provided under this repo are:
 - A generic implementation of the top level appplication and driver that can be configured at build- and/or run-time.
 - A CMake based generic build system.
 - Run configuration management built on a self-describing component standard.
