# Microsoft Visual Studio 2017 with vcpkg

#### 1. Download/install the required software

To compile on Windows, you will need to download and install:
* [Git](https://git-scm.com/download/win)
* [Visual Studio 2017 Community](https://www.visualstudio.com/vs/) (compiler)
* [vcpkg](https://github.com/Microsoft/vcpkg) (package manager)

#### 2. Set up vcpkg

Make sure to follow full installation of `vcpkg`, per [Official Quickstart](https://github.com/Microsoft/vcpkg#quick-start) execute the following in _Git Bash_ or _Powershell_:
```
git clone https://github.com/Microsoft/vcpkg
cd vcpkg
.\bootstrap-vcpkg.bat
.\vcpkg integrate install
```
```.\ -> .\\ in Git Bash```

Add `vcpkg` path to your environment variable path (e.g. C:\Projects\vcpkg)

#### 3. Download the source code

    git clone --recursive https://github.com/edubart/otclient.git

#### 4. Install libraries

Choose one set of libraries, depending on the target platform and execute the following in _Git Bash_ or _Powershell_:

* For 64-bit (x64) build:

      vcpkg install boost-iostreams:x64-windows boost-asio:x64-windows boost-system:x64-windows boost-variant:x64-windows boost-lockfree:x64-windows luajit:x64-windows glew:x64-windows boost-filesystem:x64-windows boost-uuid:x64-windows physfs:x64-windows openal-soft:x64-windows libogg:x64-windows libvorbis:x64-windows zlib:x64-windows opengl:x64-windows

* For 32-bit (Win32) build:

      vcpkg install boost-iostreams:x86-windows boost-asio:x86-windows boost-system:x86-windows boost-variant:x86-windows boost-lockfree:x86-windows luajit:x86-windows glew:x86-windows boost-filesystem:x86-windows boost-uuid:x86-windows physfs:x86-windows openal-soft:x86-windows libogg:x86-windows libvorbis:x86-windows zlib:x86-windows opengl:x86-windows

#### 5. Build

1. **Open `vc14/otclient.vcxproj`**. This should launch Visual Studio.

1. Choose build configuration from the drop downs (Debug or Release and Win32 or x64). For best performance choose Release & x64.

1. To start compiling **press F7**.

# Microsoft Visual Studio 2015 (deprecated)
> Note: since 2019-05-07(dd) the otclient.sln MSVS project file is no longer configured for use with OTClient SDK. Please follow Compiling on Windows (with vcpkg) instead. The following tutorial applies to master branch until commit [e3caaac](https://github.com/edubart/otclient/commit/e3caaacc55b68d27176645fbc2dc059398c9458f).

**1. Download the required software**

To compile OTClient on Windows, you will need:

* [Visual Studio 2017](https://www.visualstudio.com/) (compiler)

* [Otclient SDK v1.0](https://github.com/conde2/otclient-sdk) (libraries)

* [OpenGL-ES-SDK](https://github.com/okk3/OpenGL-ES-SDK) (libraries for Directx9 Support)

**2. Install the required software**

Once you have downloaded the software listed in the step above, begin by installing Visual Studio. Extract OTClient SDK anywhere on your computer. (Ex: `C:\otclient-sdk`), run the file "register_otclient_sdk_env.bat" before running Visual Studio, to set the PATH environment variable for OTClient SDK, so that the compiler can find the libraries once we get to compiling the source code. Move the file "register_otclient_boost_env.bat" from OTClient SDK to the directory where you installed Boost C++ libraries and run it there (it should be in the directory called boost_1_63_0).


**3. Download the source code**

If you have a Git client installed, you can clone the latest copy with this command: `git clone https://github.com/edubart/otclient.git`


If you don't have a Git client installed, you can download the latest copy of The OTClient from this URL: https://github.com/edubart/otclient/archive/master.zip

**4. Build**

Find the directory vc14 in the copy of OTClient that you downloaded, and open otclient.sln. This should launch Visual Studio, and you should be good to go.

To configure the build, navigate to Build -> Configuration Manager in the menu. A dialog should pop up where you can choose between Release or Debug build, and 32-bit (Win32) or 64-bit (x64) build.

To start compiling, open the Build menu again and click on Build Solution.

For Directx9 Support: Link the libraries and set OPENGL_ES=2 as a preprocessor.

# Codeblocks
### Download what you will need

There are several tools you need to compile the project, each of which is listed next to their link here:

* [CMake](http://www.cmake.org/cmake/resources/software.html) **2.8.8 or greater**
* [CodeBlocks](http://www.codeblocks.org/downloads/26) **without MinGW, we use a newer version**
* [MinGW32](http://sourceforge.net/projects/mingw/files/Installer/mingw-get-inst/) 20120426 or greater
* [otclient libraries for mingw32](http://www.mediafire.com/file/gf1cr1rj0znxdan/otclient-libs-mingw32.rar)
* otclient source code

_Make sure you install their latest versions, otherwise, things might not work._
_Note we will be using C:/MinGW as our the toolchain directory, you can change it to your liking but care for conflicts._

### Install MinGW32
Note that GCC must be 4.6 or greater, any older GCC that you have already installed will not work because otclient needs C++11 features which are supported only by recent compilers. Run the downloaded **MinGW32** installer and in the installation process **make sure that you use the latest catalog when asked and check the installation of the C++ compiler**. When finished your MinGW should be installed in C:/MinGW.
_Note it's safer to install the MSYS system and work with it.[citiation needed]._

### Install CMake
Run the CMake installer, should in the installation process you get asked if you want CMake to configure your PATH variable, say no, this will be manually set in the next steps.

### Install CodeBlocks
Run the CodeBlocks installer, _Remember, do ***NOT*** install MinGW when it asks.

### Install otclient libraries
Extract the **otclient-libs_mingw32-dwarf2.zip** into *C:/MinGW/. This zip contains 3 folders *lib*, *include* and *bin* which will be merged into *C:/MinGW/lib*, *C:/MinGW/include* and *C:/MinGW/bin*.

### Configure system PATH variable
Now that all needed tools is installed, you must configure the system **PATH** variable to make CMake find MinGW32 and the installed libraries, go to:
```
 Control Panel->System->Advanced->Environment Variables
```

Check if the user variable **PATH** exists, if not, create one, then set it to:
```
C:\Program Files (x86)\CMake 2.8\bin;C:\MinGW\bin;C:\MinGW\lib;C:\MinGW\include
```

_Make sure that the user variable **PATH** exists and refers to the CMake directory properly._

### Download OTClient source code
Download the latest [OTClient sources](https://github.com/edubart/otclient/archive/master.zip). The directory in which you place the source files may not contain any spaces (e.g. "C:\OTClient\" is **good**, however "C:\Program Files\OTClient" is not).

### Generate CodeBlocks Project file
Run the **CMake-gui.exe** located in **\Program Files\CMake 2.8\bin**, and specify the directory in which you just placed the OTClient source code, and where you want the project files to be built. Press configure,  select **CodeBlocks - MinGW Makefiles** as the generator, then generate the project files.

### Scripting and compiling it
Open the said generated Codeblocks Project file (**otclient.cbp**) by CMake with CodeBlocks, and script away! To compile, you must first configure the folder of MinGW32, by going to **Settings** > **Compiler And Debugger...** > **Toolchain Executables**.

**Make sure to copy Tibia.dat and Tibia.spr inside /data/things/<version>/ folder before running the client**

### Problems?
If your CodeBlocks (or CMake) complains it cannot find GCC or any working compiler, configure CodeBlock's compiler via settings there.
Any other problem should be posted in [otclient's otland forum](http://otland.net/f494/) or alternatively IRC (see README), don't spam! Ask, wait, try to solve it yourself until you get an answer, do ***NOT*** re-ask.

### Dx9 Support Layer 
If you would like to enable the dx9 support layer for otclient you need to compile with the *-DOPENGLES=2.0* preprocessor on Codeblocks or the *OPENGL_ES=2* preprocessor on Microsoft Visual Studio 2015. Now otclient.exe will ask for libEGL.dll and libGLESv2.dll which you can get [here](https://github.com/okk3/OpenGL-ES-SDK), place these dlls in the otclient.exe folder according to the architecture (x86-64 for 64bit and x86 for 32bit) your client has been compiled for.

Note: Compiling with the dx9 support layer will probably only work on VS15.
***

***
