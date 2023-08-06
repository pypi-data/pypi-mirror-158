# Install script for directory: /Users/runner/work/librapid/librapid/src/librapid/vendor/Vc

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/Users/runner/work/librapid/librapid/_skbuild/macosx-10.9-x86_64-3.9/cmake-install/src/librapid")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/Users/runner/work/librapid/librapid/_skbuild/macosx-10.9-x86_64-3.9/cmake-build/src/librapid/vendor/Vc/libVc.a")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libVc.a" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libVc.a")
    execute_process(COMMAND "/usr/bin/ranlib" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libVc.a")
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/Vc" TYPE DIRECTORY FILES "/Users/runner/work/librapid/librapid/src/librapid/vendor/Vc/Vc/" FILES_MATCHING REGEX "/*.(h|tcc|def)$")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/Vc" TYPE FILE FILES
    "/Users/runner/work/librapid/librapid/src/librapid/vendor/Vc/Vc/Allocator"
    "/Users/runner/work/librapid/librapid/src/librapid/vendor/Vc/Vc/IO"
    "/Users/runner/work/librapid/librapid/src/librapid/vendor/Vc/Vc/Memory"
    "/Users/runner/work/librapid/librapid/src/librapid/vendor/Vc/Vc/SimdArray"
    "/Users/runner/work/librapid/librapid/src/librapid/vendor/Vc/Vc/Utils"
    "/Users/runner/work/librapid/librapid/src/librapid/vendor/Vc/Vc/Vc"
    "/Users/runner/work/librapid/librapid/src/librapid/vendor/Vc/Vc/algorithm"
    "/Users/runner/work/librapid/librapid/src/librapid/vendor/Vc/Vc/array"
    "/Users/runner/work/librapid/librapid/src/librapid/vendor/Vc/Vc/iterators"
    "/Users/runner/work/librapid/librapid/src/librapid/vendor/Vc/Vc/limits"
    "/Users/runner/work/librapid/librapid/src/librapid/vendor/Vc/Vc/simdize"
    "/Users/runner/work/librapid/librapid/src/librapid/vendor/Vc/Vc/span"
    "/Users/runner/work/librapid/librapid/src/librapid/vendor/Vc/Vc/type_traits"
    "/Users/runner/work/librapid/librapid/src/librapid/vendor/Vc/Vc/vector"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/Vc/VcTargets.cmake")
    file(DIFFERENT EXPORT_FILE_CHANGED FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/Vc/VcTargets.cmake"
         "/Users/runner/work/librapid/librapid/_skbuild/macosx-10.9-x86_64-3.9/cmake-build/src/librapid/vendor/Vc/CMakeFiles/Export/lib/cmake/Vc/VcTargets.cmake")
    if(EXPORT_FILE_CHANGED)
      file(GLOB OLD_CONFIG_FILES "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/Vc/VcTargets-*.cmake")
      if(OLD_CONFIG_FILES)
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/Vc/VcTargets.cmake\" will be replaced.  Removing files [${OLD_CONFIG_FILES}].")
        file(REMOVE ${OLD_CONFIG_FILES})
      endif()
    endif()
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/Vc" TYPE FILE FILES "/Users/runner/work/librapid/librapid/_skbuild/macosx-10.9-x86_64-3.9/cmake-build/src/librapid/vendor/Vc/CMakeFiles/Export/lib/cmake/Vc/VcTargets.cmake")
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/Vc" TYPE FILE FILES "/Users/runner/work/librapid/librapid/_skbuild/macosx-10.9-x86_64-3.9/cmake-build/src/librapid/vendor/Vc/CMakeFiles/Export/lib/cmake/Vc/VcTargets-release.cmake")
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/Vc" TYPE FILE FILES
    "/Users/runner/work/librapid/librapid/src/librapid/vendor/Vc/cmake/UserWarning.cmake"
    "/Users/runner/work/librapid/librapid/src/librapid/vendor/Vc/cmake/VcMacros.cmake"
    "/Users/runner/work/librapid/librapid/src/librapid/vendor/Vc/cmake/AddCompilerFlag.cmake"
    "/Users/runner/work/librapid/librapid/src/librapid/vendor/Vc/cmake/CheckCCompilerFlag.cmake"
    "/Users/runner/work/librapid/librapid/src/librapid/vendor/Vc/cmake/CheckCXXCompilerFlag.cmake"
    "/Users/runner/work/librapid/librapid/src/librapid/vendor/Vc/cmake/OptimizeForArchitecture.cmake"
    "/Users/runner/work/librapid/librapid/src/librapid/vendor/Vc/cmake/FindVc.cmake"
    "/Users/runner/work/librapid/librapid/_skbuild/macosx-10.9-x86_64-3.9/cmake-build/src/librapid/vendor/Vc/cmake/VcConfig.cmake"
    "/Users/runner/work/librapid/librapid/_skbuild/macosx-10.9-x86_64-3.9/cmake-build/src/librapid/vendor/Vc/cmake/VcConfigVersion.cmake"
    )
endif()

