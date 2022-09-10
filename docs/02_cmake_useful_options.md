So, the main page got you here and you want to configure your compilation process for your own needs but clueless about what each option does or how to use luajit, etc.  Then this is the right place.
These are the options I use whenever building a project (most of those ones are builtin otclient's CMakeLists.txt).

### Options list and what each do
* CRASH_HANDLER - This helps generate crash reports when the application crashes whether it's compiled with debug mode or even release (**Note**: Release with debug info, see CMAKE_BUILD_TYPE).  It's also very helpful to send it to the developers when you encounter a crash and possibly some code.
* LUAJIT - This enables compiling with luajit, lua is way slower than luajit.  We do not use lua 5.2 features and that's what luajit is missing.
* USE_STATIC_LIBS - This option is really useful when releasing an executable.
   see also [GCC Linker](http://gcc.gnu.org/onlinedocs/gcc/Link-Options.html)
* WINDOWS_CONSOLE - This option is useful when being a bit more verbose, on windows.
* CMAKE_BUILD_TYPE - Specify the build type, valid ones are:
   * Release
   * Debug
   * RelWithDebInfo (Release with debug information)

  See also: [CMake variables](http://www.cmake.org/Wiki/CMake_Useful_Variables)
* The -G CMake option - Specify the Makefile generator, they depend on how CMake is compiled, here are a list of ones I know of:
   * MSYS Makefiles
   * UNIX Makefiles
   * MinGW Makefiles
   * CodeBlocks - Unix Makefiles
   * Eclipse CDT4 - Unix Makefiles
   * KDevelop3
   * KDevelop3 - Unix Makesfiles

  Note Unix stuff _should_ be available for Win32 (some of them).
  See also: [CMake cmd options](http://linux.die.net/man/1/cmake)
  Try: cmake --help

This is it for now folks, I might be adding more later on.
