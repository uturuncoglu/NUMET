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
 - An implementation of the top level application and driver that is fully configurable at build- and run-time via the nuBuild.yaml and nuRun.config files, respectively.
 - A CMake-based build system that uses the same nuBuild.yaml file to ochestrate the complete build procedure.
 - Run configuration management that is built on a self-describing component standard.

## The NumetProto example
Refer to [NumetProto](https://github.com/esmf-org/nuopc-app-prototypes/tree/develop/NumetProto) as a NUOPC prototype example that demponstrates the usage of NUMET.

## Adding NUMET to a project
A project that wants to use NUMET sets up NUMET as a Git submodule:

    git submodule add https://github.com:theurich/NUMET
    
## nuBuild.yaml
A suitable nuBuild.yaml file need to be composed. It's a yaml file with a very simple format:

    components:

      tawas:
        source_dir:   ./TAWAS
        shared:       true

      lumo:
        source_dir:   ./LUMO
        shared:       false
        fort_module:  lumo

In this example, two components are specified: tawas and lumo. The source code of the first compoennt is located in the ./TAWAS directory uder the project directory, It is configured to be built as a shared library. Further, since there is no Fortran module name specified via fort_module, this component will not create a build dependency for the NUMET executable. Instead the componet becomes available to be loaded at run-time. The nuRun.config section will provide further details.

The second component in the example, lumo, on the other hand does specify the fort_module key. It will be built into the NEMET executable by accessing the Fortran module at build-time, and linking against the lumet library.

## Building the NUMET executable
With the NUMET submodule and the nuBuild.yaml file in place, the NUMET executable can be built. This is accomplished by the following build procedure, starting at the root of the project directory:

    mkdir build
    cd build
    cmake ../NUMET
    cmake --build .

A successful build produces the numet.exe in the build directory. Shared object libraries, e.g. here for the TAWAS component, are located under their respective subdirectories.

## nuRun.config
The nuRun.config file needs to be located under the run directory from where the NUMET executable is launched. It is read by the NUMET executable during startup. This configuration file specifies a few global ESMF and NUMET level settings, the list of components used during this run, details about the components, and run sequence details.

    logKindFlag:            ESMF_LOGKIND_MULTI
    globalResourceControl:  .true.
    
    NUMET_log_flush:        .true.
    NUMET_field_dictionary: ./fd.yaml

    NUMET_component_list:   ATM OCN
    NUMET_attributes::
      Verbosity = high
    ::
    
    ATM_model:            ../build/TAWAS/libtawas.so
    ATM_petlist:          0-3
    ATM_omp_num_threads:  1
    ATM_ttributes::
      Verbosity = high
    ::
    
    OCN_model:            lumo
    OCN_petlist:          1 3
    OCN_attributes::
      Verbosity = high
    ::
    
    startTime:  2012-10-24T18:00:00
    stopTime:   2012-10-24T19:00:00
    
    runSeq::
      @900
        ATM -> OCN
        OCN -> ATM
        ATM
        OCN
      @
    ::

There are two options under the XXX_model: field. First the value is used to search whether a build-time dependency exsits with the same name. If so, the respective component, which was accessed via its Fortran module at build time, is selected to execute. Second, if the value does not match a build-time dependency, it is assumed to correspond to a shared object, and the attempt is made to access the object at run-time.
