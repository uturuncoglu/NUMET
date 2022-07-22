cmake_minimum_required(VERSION 3.12)
enable_language(Fortran)

# Where to look for Find<Package>.cmake files
list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_LIST_DIR}/cmake)

# Find ESMF
find_package(ESMF 8.4.0 REQUIRED)

# Set compilers per ESMFMKFILE
set(CMAKE_CXX_COMPILER ${ESMF_CXXCOMPILER})
set(CMAKE_Fortran_COMPILER ${ESMF_F90COMPILER})

# Specific project settings
project(NUMET VERSION 0.1.0 DESCRIPTION "Nuopc Unified Modeling Environment Toolkit")
add_executable(numet.exe numet.F90)
target_link_libraries(numet.exe ESMF)
install(TARGETS numet.exe)
target_include_directories(numet.exe PUBLIC ${PROJECT_BINARY_DIR})

# Generate 
find_package(Python 3 COMPONENTS Interpreter REQUIRED)
execute_process(COMMAND ${Python_EXECUTABLE}
  ${CMAKE_CURRENT_LIST_DIR}/nuGen.py --ifile ${CMAKE_CURRENT_LIST_DIR}/../nuBuild.yaml
  RESULT_VARIABLE ret)
if(ret EQUAL "1")
  message( FATAL_ERROR "nuGen.py failed processing nuBuild.yaml")
endif()

include(${CMAKE_CURRENT_BINARY_DIR}/compList.txt)
