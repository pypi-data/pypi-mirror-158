#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Vc::Vc" for configuration ""
set_property(TARGET Vc::Vc APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(Vc::Vc PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_NOCONFIG "CXX"
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libVc.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS Vc::Vc )
list(APPEND _IMPORT_CHECK_FILES_FOR_Vc::Vc "${_IMPORT_PREFIX}/lib/libVc.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
