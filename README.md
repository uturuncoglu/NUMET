# NUMET

NUMET is the **N**uopc **U**nified **M**odeling **E**nvironment **T**oolkit

The goal of NUMET is to unify, provide, and maintain those parts of NUOPC-based modeling systems that are common across most such implementations. This includes the top level application and driver code, parts of the build infrastructure, and tools for run configuration management.

The objectives of NUMET are:
 - **Simplification** of standing up new NUOPC-based systems.
 - **Reduction** of maintenance cost for established NUOPC-based systems.
 - **Improved** alignment and interoperability between different NUOPC-based systems. (Configuration files, procedures, etc.)
 - **Faster and more coordinated** role out of new NUOPC/ESMF features.

The approach of NUMET is to provide a software component that can be pulled into any modeling system as a Git submodule from GitHub. Next to NUMET sit the NUOPC-based model components as usual. The modeling system itself provides the build- and run-time configuration files.

The concrete pieces maintained in and supplied by the NUMET repo are:
 - An implementation of the top level application and driver that is fully configurable at build- and/or run-time via the nuBuild.yaml and nuRun.config files, respectively.
 - A CMake-based build system that is based on the same nuBuild.yaml configuration information.
 - Run configuration management that is built on a self-describing component standard.
