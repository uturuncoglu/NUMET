cmake_minimum_required(VERSION 3.12)
enable_language(Fortran)

# Where to look for Find<Package>.cmake files
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/cmake")

# Find ESMF
find_package(ESMF REQUIRED)

# Set compilers per ESMFMKFILE
set(CMAKE_CXX_COMPILER ${ESMF_CXXCOMPILER})
set(CMAKE_Fortran_COMPILER ${ESMF_F90LINKER})

# Specific project settings
project(NUMET VERSION 0.1.0 DESCRIPTION "Nuopc Unified Modeling Environment Toolkit")
add_executable(numet.exe numet.F90)
target_link_libraries(numet.exe ESMF) 
