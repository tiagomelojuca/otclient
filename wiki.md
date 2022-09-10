# The Official OTClient Wiki

## Welcome!
If you are looking for information about OTClient, here is the right place. This is the official community maintained repository of information and documentation for users, developers and contributors.

## About OTClient
OTClient is an alternative Tibia client for usage with otserv.
It aims to be complete and flexible, for that it uses Lua
scripting for all game interface functionality and configurations using a new file type known as OTML, that was created with the purpose to be easy for typing/reading.
OTClient works with a modular system, each functionality is a separated module,
this gives the possibility to users modify anything easily. It also allows to
extend game functionalitty with modules known as "addons", feature inspirited by "World of Warcraft", where
users can create their own game interfaces and functionality on top of the original game. The game interface look and style is completely flexible, you can change styles using a syntax near CSS and QML.

## Getting Started
Getting started with OTClient is simple! OTClient has multi client/protocol support which means it can run different Tibia protocols/clients (from 7.4 to 10.99). In order to run the different versions all you need to do is this:
* Copy the Tibia.dat and Tibia.spr from your regular Tibia client into `/data/things/<version>/` folder.

For example: `/data/things/871/` this will check for the 8.71 tibia dat/spr files here.

Now you can use that client version by selecting it in the login process:

![Version](http://i.imgur.com/P1pVBG8.png)

To login to the server you would like to play you can just enter in the **server** and the **port** (like so in the article above)

### Menu
There are menu buttons for the client management and game features located at the top of the client window.

![Module Manager](http://i.imgur.com/KUlnZ0B.png)

![Game Options](http://i.imgur.com/bqGNsSm.png)

![Console Options](http://i.imgur.com/uye4dZn.png)

![Graphics Options](http://i.imgur.com/ZvNkX64.png)

![Audio Options](http://i.imgur.com/QVhGmTE.png)

For any of the traditional game features, this is where they will be located.

## General Resources
* [[FAQ]]

## Developing Resources
* [[OTClient Coding Style]]
* [[Submitting Patches]]
* [[Compiling on Linux]]
* [[Compiling on Windows]]
* [[Module Tutorial]]
* [[CMake useful options]]

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

# Setup Instructions
### 1 - Setup the Libraries/SDK/JDK/Programs
Download the following files:
* [Android SDK](http://developer.android.com/sdk/installing/index.html?pkg=tools)
* [Android NDK R10d](https://dl.google.com/android/ndk/android-ndk-r10d-windows-x86_64.exe)
* [Android Libraries](http://goo.gl/NER92t) for armeabi-v7a
* [Java JDK](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
* [Apache ANT](http://ant.apache.org/bindownload.cgi)
* [Cygwin](https://cygwin.com/install.html) to use **make** on **Windows** 
* [CMake](http://www.cmake.org/download/)

### 2 - Extract and Install
Extract and install the files downloaded. <br />
For **Cygwin**, you will need select **make** program to install.

### 3 - Copy the Android Libraries
Put the android libraries inside the android ndk folder.

### 4 - Create Environment Variables:
- ANDROID_SDK pointing to the android sdk folder
- ANDROID_NDK pointing to the android ndk folder
- JAVA_HOME pointing to the java folder
- ANT_HOME pointing to the apache ant folder
- CYGWIN_HOME pointing to the cygwin folder

### 5 - Add folders to your system path variable:
- ANDROID_NDK
- ANDROID_SDK/platform-tools (to use adb)
- ANDROID_SDK/tools (to use android)
- JAVA_HOME/bin
- ANT_HOME/bin
- CYGWIN_HOME/bin

### 6 - Clone the Mobile OTClient sources
`git clone -b mobile_port https://github.com/edubart/otclient.git otclient-mobile`

or simply

`git checkout mobile_port` from within the otclient git repository.

### 7 - Connect a Phone
Must connect a phone that with a armeabi-v7a processor.

## 8 - Run Compilation Script
**Windows:** Run compile_android_windows.bat script.<br/>
**Linux:** Run compile_android_unix.sh script.<br/>

Lastly contribute to the project! ;)

## Debian/Ubuntu

First install required development packages using apt-get

```sh
sudo apt install -y build-essential cmake git-core
sudo apt install -y libboost-all-dev libphysfs-dev libssl-dev liblua5.1-0-dev
sudo apt install -y libglew-dev libvorbis-dev libopenal-dev zlib1g-dev
```

and if you are using 18.04, you may also need `sudo apt install -y libogg-dev`

Get the sources, compile and run

```sh
git clone git://github.com/edubart/otclient.git
cd otclient
mkdir -p build
cd build
cmake ..
make -j $(nproc)
./otclient
```

#### Common Ubuntu problems:

If you have this error at make:
```
Linking CXX executable otclient /usr/lib/gcc/x86_64-linux-gnu/5/../../../x86_64-linux-gnu/libphysfs.a: error adding symbols: Archive has no index; run ranlib to add one collect2: 
```

Then do:
```
git clone -b stable-3.0 https://github.com/icculus/physfs.git
cd physfs
sudo mkdir build
cd build
sudo cmake ..
sudo make -j $(nproc)
sudo make install
sudo cp /usr/local/lib/libphysfs.a /usr/lib/x86_64-linux-gnu/.
```


## Manjaro/Arch 

First upgrade your system and install required development packages using pacman

```sh
sudo pacman -Syu && sudo pacman -S base-devel git cmake boost physfs openssl lua51 glew libvorbis openal zlib libogg
```

Get the sources, compile and run

```sh
git clone git://github.com/edubart/otclient.git
cd otclient && mkdir build && cd build && cmake .. && make
./otclient
```


## Fedora

These instructions were tested on Fedora 20. Some packages that I suggest to be installed might not actually be needed and there might be a simpler way to link in Lua, but I am not aware of it. In case of a problem, contact d33tah.

#### Install Lua 5.1 to /opt/lua5.1

```
sudo yum install readline-devel
yum-builddep lua
wget "http://www.lua.org/ftp/lua-5.1.5.tar.gz" -O- | tar zxvf -
cd lua-5.1.5
make linux
mkdir /opt/lua5.1
make INSTALL_TOP=/opt/lua5.1 install
```

#### Install needed packages

```
yum install boost-devel physfs-devel mesa-libGLw mesa-libGL-devel glew-devel openal-devel libvorbis-devel boost-system boost-thread boost-chrono boost-filesystem
```

#### Build otclient

The final command, `make`, will take most time. If you have a multi-core processor, try `make -j$(nproc)` to speed up the build process.

```
mkdir build && cd build
cmake  -DUSE_STATIC_LIBS=OFF -DLUA_LIBRARY=/opt/lua5.1/lib/liblua.a -DLUA_INCLUDE_DIR=/opt/lua5.1/include/ ..
make
```

#### Test if it runs

```
./otclient
```

This is how we compile `otclient` on **Mac OS X**. XQuartz (X Window System implementation from Apple) is used to compile and run `otclient`. (We do not use the native Cocoa API for this purpose.) Also, you will need to know the basics of how using the terminal in Mac OS to follow this tutorial.

## Requirements
* Mac OS X 10.6 or higher
* [Command Line Tools (choose the latest)](https://developer.apple.com/download/all/)
* [XQuartz](http://xquartz.macosforge.org/landing/)
* [Homebrew](http://mxcl.github.com/homebrew/)

You should install all mentioned requirements, in order. Sorry but it won't be covered here.

## Installing needed libraries

HomeBrew is used to install most of the required libraries:

```bash
brew install \
  boost@1.76 \
  cmake \
  git \
  glew \
  libogg \
  libvorbis \
  lua@5.1 \
  physfs \
  gmp
```

## Cloning and compiling

Before start executing the sequence of commands below, note that:
- You may need to change the included directory of your installed version of OpenSSL. Check your installed version with `brew info openssl`. 
- If you're on an Apple Silicon Mac the prefix of HomeBrew dependencies directory could be in `/opt/homebrew/Cellar/`.
- If you run into problems during the build process, it's likely already been addressed in the [Issues](https://github.com/edubart/otclient/issues) section. Start looking there.

```bash
git clone git://github.com/edubart/otclient.git

cd otclient

mkdir build

cd build

cmake \
  -DUSE_STATIC_LIBS=OFF \
  -DLUA_LIBRARY=/opt/homebrew/Cellar/lua@5.1/5.1.5_8/lib/liblua.5.1.5.dylib \
  -DLUA_INCLUDE_DIR=/opt/homebrew/Cellar/lua@5.1/5.1.5_8/include/lua5.1/ \
  -DBoost_INCLUDE_DIR=/opt/homebrew/Cellar/boost@1.59/1.59.0/include/ \
  -DOPENSSL_INCLUDE_DIR=/opt/homebrew/Cellar/openssl@1.1/1.1.1p/include/ \
  -DGMP_INCLUDE_DIR=/opt/homebrew/Cellar/gmp/6.2.1_1/include/ \
  -DGMP_LIBRARY=/opt/homebrew/Cellar/gmp/6.2.1_1/lib/libgmp.dylib \
  ../

make -j$(sysctl -n hw.ncpu)
```

Now you can run the otclient output binary. It should be in the same directory:

```bash
./otclient
```

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

### Can I use OTClient for commercial purposes?
Yes, you can! OTClient is made available under the MIT license, thus this means that you can do whatever you want, commercial, non-commercial, closed or open. You are only required to distribute your customized OTClient included with a copy of the license copyright notice, located in the repository in the file named LICENSE.

### Can you provide a way to hide all module scripts?
Unfortunately this is something that the OTClient developers are **NOT** going to be working on. Otclient is an opensource project, it's goal for the project is to get every developer or even players that uses it helping out the project, with contribution from everyone we can achieve a great client for everyone, not just for you. We are of the opinion that taking a whole project made by hours of work from other people then wanting to hide it all is kind of rude and pointless, you would be hiding 99% of our open source work which is already out there. We give an amazing client for free and it's fair to deserve something back from you and the community. What we want is contributions and you can do these in two ways, directly in our codebase or by customizing the client for your server while the changes is visible then the main project could benefit from these changes. So the fact that you can't hide the code is a good thing for this project goal, we would like to keep that way, so we discourage any change or help that could lock down the otclient scripts. I am not saying that you can't, just saying this is "forbidden" for us.

### Clone a new repository
```sh
git clone git://github.com/edubart/otclient.git
```

### Update your fork
Remember to always update your fork before making a pull request.
Make sure that you have the remote upstream, if you does not have it yet, create now.
```sh
git remote add upstream git://github.com/edubart/otclient.git
git fetch upstream
```

### Update your fork before pull requests
Make sure that you are pulling from upstream with rebase if you pretend to make pull requests on the upstream.
```sh
git pull --rebase upstream master  # pull new upstream changes to your local repository
git push -f                        # this may overwrite your fork
```

### Reset your repository
```sh
git stash                        # save any changes
git fetch                        # update remote repository information
git reset --hard origin/master   # reset your local ranch making identical to the remote master
git stash pop                    # restore changes
```

### Reset your fork
This is just like the instructions above, but with a different remote.
```sh
git stash                        # save any changes
git fetch                        # update remote repository information
git reset --hard upstream/master   # reset your local ranch making identical to the remote master
git stash pop                    # restore changes
```

### Commit new changes
```sh
git add file                     # add new files
git commit -a                    # commit all modified files
git pull --rebase                # update your local repository before pushing
git push                         # push your changes to the master
```

### Redo last commit
If you commited anything wrong and **didn't push yet**, instead of doing another commit to fix,
you can redo the previous commit.
```sh
git commit -a --amend            # append new changes to the latest commit
```

### Save current changes for later
You can use stash for storing changes in a temporarly without needing to store then on a new branch.
```sh
git stash
```

To restore just pop latest stash.
```sh
git stash pop
```

### Joining commits
Use with care, rebase will rewrite the commit history, so make sure that you didn't pushed the commits that you are joining yet.
```sh
git rebase -i HEAD~2               # will enter in interactive rebase in the latest 2 commits
```

Now in the interactive rebase, mark the commits that you want to join with "squash", in rebase you can also
delete commits, change commits order, commit messages and more. If anything goes wrong use git rebase --abort
to cancel.

### Checking changes
There are many tools that can be used to check current changes and commit history,
in the web you can also find graphical good tools, the next ones generially comes with git, and I usually
get what I want with gitk.
```sh
git status
git diff
gitk
```

### Branchs
Create new branch 'tmp' based on the current branch and change to it.
```sh
git checkout -b tmp
```

Change to branch master.
```sh
git checkout master
```

Merge commits from branch tmp into the current branch.
```sh
git merge tmp
```

I am writing this tutorial to help people get started in contributing to otclient by creating new modules and working within otclient lua environment.

**So to start things off I will be covering:**
* the creation of modules.
* go over some of the basics to working within otclients lua environment.
* how to efficiently test your modules and scripts.

**For this tutorial you will need:**
* otclients latest source code from the git repository [otclient repo](https://github.com/edubart/otclient). There is a tutorial on how to work with the git repository [here](http://otclient.info/tutorials/git_workflow.html).
* a text editor of some sort (I like to use [Sublime Text 2](http://www.sublimetext.com/2) or [Notepad++](http://notepad-plus-plus.org/download/v6.1.5.html)) just be sure to read the [code conventions](https://github.com/edubart/otclient/wiki/OTClient-Coding-Style) first too.
* it would also be good to have basic knowledge of lua and programming skills (but this is something you can pick up quickly by practicing).

Now that you have what you need we can get started!

# Creating a New Module
Otclient front end runs off what we call 'modules'. Modules are a way of effectively implementing client features separate to each other. If you are considering creating a new module it is advised that you think about what the feature might be and whether or not it would fit into an already existing module (most likely a game\_xxx module), the modules are found in the /modules directory of otclient.

Their are currently two module 'environments': **Game** and **Client**. Game modules use the prefix game\_ and should be reflecting features that specifically relate back to the player or game environment features for example game\_outfit or game\_mounts are both features that are used in the game environment. Client modules use the prefix client\_ and should be reflecting features that specifically relate back to the client and the client only. It does not have anything to do with the players game environment, e.g. client\_options and client_skins are only directly related to the clients functionality. This might be a little bit hard to visualize for now but you will pick this up more later.

So now that you have an understanding of what a module is and somewhat how they operate we will go ahead and start creating a new one.

## Starting from scratch
We are going to create a fresh module from scratch, the first thing you need to do is create the modules directory. The directory name should reflect the overall feature itself, so we will call ours `game_spells` to start creating a new module that will list all the players spells with their appropriate information. We won't be creating this entire module but we can get started to see how it all works.

* `Create a new directory called game_spells inside the clients /modules directory.`

Inside game\_spells we need to start by adding 3 new base files: spells.lua, spells.otmod and spells.otui for the modules logic, registration, and interface design.

* `Create 3 new base files spells.lua, spells.otmod and spells.otui inside /modules/game_spells`

You might already know what the .lua file represents but what are these new extensions .otmod and .otui?
### .otmod
.otmod file is the file that is used to initialize the module within otclient, it is like a register in that it will register the module for use inside the client. This file generally has a structure like this (I have added comments, if you copy this code be sure to remove the -- comments):
```lua
Module
  name: game_spells -- name of the module (generally the same name as the modules directory.
  description: Display a players spells with their appropriate information -- description of the module explaining what it is.
  author: BeniS -- names of the creators and contributors of the module.
  website: www.otclient.info -- if you have an external website you can link it here.
  sandboxed: true -- Sandboxing is a way of containing the modules variable and functions so that you do not have conflicts between other modules.
  scripts: [ spells.lua ] -- The scripts is the logic behind the module where all the functions are contained.
  @onLoad: init() -- this is where you define the initialization function of the module (we will cover this more later).
  @onUnload: terminate() -- this is where you define the termination function of the module (we will cover this more later)
```

* `Copy the .otmod code above into your spells.otmod file and remove the -- comments.`

### .otui
.otui file is the file that is used to create the modules user interface. This is a custom made styling language specifically designed for otclient called OTML, it feels a lot like CSS formatting for those of you who have experience in webdesign. The typical structure of a .otui file looks like this (this is the start base file, not completed):
```css
MainWindow
  !text: tr('Spells')
  size: 160 450

  @onEnter: modules.game_spells.destroy()
  @onEscape: modules.game_spells.destroy()

  Label
    id: spellsLabel
    !text: tr('Player Spells')
    width: 130
    anchors.top: prev.top
    anchors.left: prev.left
    margin-top: 5
    margin-left: 5
```

**MainWindow** This is the window we will be using for the spell list interface, it is a standard window class derived from `/client_skins/default/styles/windows.otui` styling file it extends Window which extends UIWindow. UIWindow is a base class of this initialization, it controls the widgets functionality and behaviors.
* **!text:** This is the text that is displayed in the MainWindow heading section.
* **size:** this is used to set the MainWindows width/height.
* **@onEnter:** configures the MainWindow widgets onEnter callback (function that will be called when you press the enter key).
* **@onEscape:** configures the MainWindow widgets onEscape callback (function that will be called when you press the escape key).

**Label** This is a label widget that is used for displaying text in most cases. It is a derivative of UILabel class.
* **id:** This is the id that this commonest will alias itself with for referencing using functions such as widget:getChildById("spellsLabel")
* **!text:** This is the text that will be displayed by the UILabel widget.
* **width:** This is the width size of the Label.
* **anchors.top/bottom/left/right:** Anchors are where the top/bottom/left/right of the Label should be positioned, this is often based on the previous (prev) UI component or the parents anchors.
* **margin-top/bottom/left/right:** Margins are offsets to the anchors, they will allow you to fine-tune the placement of UI components.

This is just the surface of .otui formatting and styling, there is a lot more that can be done but the main idea is that you get a grasp on how to hierarchy the UI components to display correctly, etc. the OTML styling conventions force you to keep the designing of an interface separate to the logic code for example the .lua.

* `Copy the otui code above into your spells.otui file`

Now that we understand what file is used to register the module and what file(s) are used to build the modules UI we can delve into the modules logic code and try understand how it all works together. The file spells.lua is the file that contains the modules logic code. This is where the spells will be populated and the handling of spell selection and spell display will be controlled.

* `Open the file spells.lua and copy in the following base code to get started.`

We will be picking apart this code to help better understand it. I went ahead and started the base code for you, here it is:
```lua
Spells = {}

spellWindow = nil
selectedSpell = nil
spells = {}

function init()
  connect(g_game, { onOpenSpellWindow = Spells.create,
                    onGameEnd = Spells.destroy })
end

function terminate()
  disconnect(g_game, { onOpenSpellWindow = Spells.create,
                       onGameEnd = Spells.destroy })
  Spells.destroy()
  
  Spells = nil
end

function Spells.create(spellList)
  spells = spellList
  Spells.destroy()

  spellWindow = g_ui.displayUI('spells.otui')
end

function Spells.destroy()
  if spellWindow then
    spellWindow:destroy()
    spellWindow = nil
    selectedSpell = nil
    spells = {}
  end
end

function Spells.selectSpell()
  if table.empty(spells) then
    return
  end
  -- TODO
end
```

The main things I want to focus on here are:
* the variables (spellWindow, selectedSpell and spells).
* and the functions (storing of functions and discuss what init and terminate are required for).

**The variables**  
Variables within a sandboxed module do not have to be localized with the keyword `local` as they are inside their own module environment. If the module is `sandboxed: false` then you will need to make sure you localize the variable and reset them inside the terminate function (which we will discuss more later).

Inside this spell module we need to have a way of storing the modules window object, we do this by setting the variable `spellWindow` that we have initialized as nil, but that we will setup soon enough. We also need a way of containing what spell the player has selected which means we should store a reference to the spell somehow using the variable `selectedSpell`. Last but not least and most likely not last either! We need to store the list of spells and we do this with the `spells` variable.

**The functions**  
Functions much like variables are contained within sandboxed modules so localization can vary depending on your preferences. If you are not using a `sandboxed: true` module then you will need to make sure you are localizing and storing functions correctly. I personally like to use a table to store my functions within to keep things organized more this is where you see `Spells = {}`. Spells is a table that I will be using to store all the public functions of a module. Private module functions will be localized even though it is not entirely necessary inside a sandboxed module, I prefer to state when the function is private via the local keyword.

So what are the functions init() and terminate() used for?  
As you might have already noticed inside the spells.otmod code you will see:
```lua
@onLoad: init()
@onUnLoad: terminate()
```
### init()
The init function is a function that is called when otclient attempts to load the registered module using onLoad signal call. Inside this function you should be initializing all the components that are required by your module. As you can see inside spells.lua we are calling a function within `init()`:
```lua
connect(g_game, { onOpenSpellWindow = Spells.create,
                    onGameEnd = Spells.destroy })
```
This connect function is used to set a callback for certain signal calls, in this case onOpenSpellWindow will call the `Spells.create` function, which of course has our spell window creation code (or at lease it will soon!).

### terminate()
The terminate function is a function that is called when otclient attempts to unload the registered module using onUnLoad signal call. Inside this function you should be destroying and reseting variables that need to be cleared on termination of the module. Remember that not all variables will need to be reset, but particular ones such as widget references and the Spells table are all required to be reset onUnLoad. As you can see inside spells.lua we are calling and setting a number of things within terminate():
```lua
disconnect(g_game, { onOpenSpellWindow = Spells.create,
                       onGameEnd = Spells.destroy })
Spells.destroy()
  
Spells = nil
```
I stated earlier that we called the function connect inside `init()`. Now that we are terminating the module we need to disconnect the callbacks from the set signal calls. This is done via the `disconnect(...)` function.

With these main things covered you can pretty much do what you like within the module. You can carefully construct and craft it to suit what you need. Follow on through the tutorial to extend your knowledge of creating modules and also working within otclients module environment.

## How to test your modules effectively
Testing your modules will be an important part of getting them working the way you need. Testing modules can at times be a bit of a challenge so there are a few things that you'll need to know in order to make it easier for you.

### Reloading your module
You can reload your modules in the client using the Module Manager module ![Module Manager](http://3.imgland.net/qJ2lIKk.png) select your module and click **reload**. Be aware that your init() and terminate() functions will be called on reloading so if you are not initializing and destroying particular things correctly then you may get errors on reloading.

**Important Note:** There are some rare changes that might not be reloaded correctly with the module manager, things such as .otui @ changes (e.g. @onClick: edits). 
There may be some other changes that do not reload correctly, but for the most part it works fine. If you find yourself having weird errors attempted to do a full restart of the client to ensure its not a reloading issue.

### Helpful test commands
There are a selection of helpful commands that can be useful for testing found in `/modules/client_terminal/commands.lua` script file. Here is a list of the current commands that you can enter into the client terminal:
```
dumpWidgets(widget, level)
drawDebugBoxes(enable)
hideMap()
showMap()
debugContainersItems()
debugPosition(enable)
autoReloadModule(name)
```
You can add new commands to your /mod directory in order to avoid making changes to the modules command file.

You should always ensure that your modules are thoroughly tested before creating pull requests to the main git repository. These tips can be very useful in the testing phases!

# Some helpful guidance
While developing your module be sure to give it lots of thought about how it is going to work and whether or not you can merge the feature to an already existing module. Also global functions and constants variables can be found in the modules/corelib and modules/gamelib directories. Please give careful consideration to what you put into these files and if possible try to avoid it. Follow the rule "Keep everything to their own cause, and only that cause".

### ESSENTIAL RULES THAT MUST BE FOLLOWED
Before implementing anything, you must REALLY follow the next 8 code rules. They are coding techniques that changes the way you will implement anything. There is a logical reason behind each one.

* Avoid pointers at all costs, use only when really needed like for C strings (char*), avoid even for buffers of ints.
* If you need a buffer, use std::vector.
* Never use pointers for objects, if you think you need so I'm sure you can either use std::shared_ptr or pass the object by reference.
* Never use **delete** keyword, and when I say never, I mean NEVER. If you think you need to use delete you didn't read the previous two rules.
* Pass small objects like Position, Rect, std::string, by reference.
* Include only declarations from other objects in headers files, never definitions, you can see the declarations.h pattern in the source.
* If you think anything can go wrong on your code, you can use **assert** or throw an exception for checking.
* C++0x comes with a varieties of new utilities, you can and you are encouraged to use them.

### Indentation
* 4 spaces are used for indentation
* Spaces, not tabs!

### Declaring variables
* Variables/functions start with a small letter and each consecutive word starts with a capital letter.
* Avoid short names and abbreviations whenever possible. Use readable names.

```cpp
    int a; // Wrong
    int whorisize; // Wrong
    int hsize; // Wrong
    int windowHSize; // Wrong
    int windowHorizontalSize; // Correct
```

* Single character variable names are only suitable for counter variables, where the purpose of the variable is obvious.
* Classes always start with a uppercase character.
* Class members variables always begin with m_ followed by a name starting with a lower case character.

```cpp
    class DummyClass
    {
        int mVariable; // Wrong
        int m_Variable; // Wrong
        int m_variable; // Correct
    };
```

* Struct member variables must not begin with m_, avoid structs and use only when it feels right.
* Global variables begins with g_
* Use bultin int types:

```cpp
    uint32_t var; // Wrong
    uint32 var; // Correct

    unsigned long var; // Wrong
    ulong var; // Correct
```

### Singletons
* Use the following style to declare singletons:

```cpp
    // on game.cpp top
    Game g_game;
    // on game.h bottom
    class Game { ... };
    extern Game g_game;
```

### Loops and iterators
* Use **auto** keyword on every iterator:

```cpp
    std::map<int, std::string>::iterator it = myMap.begin(); // Wrong
    auto it = myMap.begin(); // Correct

    for(std::map<int, std::string>::iterator it = myMap.begin(); it != myMap.end(); it++) // Wrong
    for(auto it = myMap.begin(); it != myMap.end(); ++it) // Correct
    or
    for(auto pair : myMap) // Correct
```

* Use C++0x for each when you can:

```cpp
    for(auto it = files.begin(); it != files.end(); ++it) { } // Wrong
    for(const std::string& file : files) { } // Correct
```

### Sources files
* If you need any STL header use global.h, avoid flooding includes.
* All sources files must have the license and copyright notice on top.
* Only include needed headers.
* Whenever is possible, forward declare classes names instead of including it's headers.

```cpp
    // Wrong
    #include "foo.h"
    class Dummy {
        Foo *m_foo;
    };

    // Correct
    class Foo;
    class Dummy {
        Foo *m_foo;
    };
```

### Classes
* When using **new** keyword place brackets only when needed:

```cpp
    new DummyClass(); // Wrong
    new DummyClass; // Correct
```

* Avoid empty constructors in sources files.
* Declare destructors only when needed.
* Get methods must have **const** keyword.

### Documentation
* Comment anything that you feel relevant.
* Document functions on headers using /// to enable doxygen output.

### Algorithms
* Use high level classes like Rect, Point, std::string whenever is possible.
* Use high level APIs, e.g. for strings boost algorithm is there.
* Make algorithms readable and organized.
* Comment complex ones.

### Pointers and memory
* Avoid to use **delete** keyword or manage memory on you own, always prefer smart pointers.
* Prefer to forward complex objects variables by reference and using **const** keyword.

### Before I start, here are some notes:

**Things I will *NOT* teach you:**
* C++
* Lua
* Compiling otclient, there are tutorials over here in the wiki, please check them out.

**Things I will teach you:**
* Basic usage of git.
* Testing your code before pushing.

**Another thing, before diving in, obtain a copy of Git, there are several ways to do this, here are some of them:**
* Compiling from source code (I won't do that)
* Obtaining it by your package manager (Linux or Cygwin)
* The Native way in windows, is obtaining an installer through [here](http://git-scm.com/download/win)

**Configuring git**
* Configure your email address and github user:
```sh
   git config --global user.name="your name here"
   git config --global user.email="your email here"
```
* (Optional) Configure email sending stuff:
```sh
   git config --global sendemail.smtpencryption=tls
   git config --global sendemail.smtpserver=smtp.gmail.com
   git config --global sendemail.smtpuser=example@gmail.com
   git config --global sendemail.smtpserverport=587
```

Okay, now you're ready to dive in.
* Open up Git Shell.
* Obtain a copy of otclient's source code:
```sh
   git clone https://github.com/edubart/otclient.git
```
* Change directory to otclient's source code:
```sh
   cd otclient
```
* Before you do anything, please work on a different branch than master, we will use _tutorial_.
* Tip: to see which branch you're currently working on, do:
```sh
   git branch
```
  Which should (hopefully) output:
  *  master

* Create your work branch, we will be using _tutorial_:
```sh
   git checkout -b tutorial
```
This creates new branch called tutorial and switches to it and is also a shortcut to:
```sh
   git branch tutorial
   git checkout tutorial
```
Make sure you're in the branch tutorial, do:
```sh
   git branch
```
Which should output:
   * master
   * tutorial

## The Job
* Step 1, Do some change
![code](http://i.imgur.com/d7q4K.png)

* Step 2, check our changes:
![changes](http://i.imgur.com/N44kp.png)

Like you see, nothing has been added to the repo yet, add it with:
```sh
   git add file
```
And then, commit it with:
```sh
   git commit
```
**Note**: This will open the text editor git is configured with,  to configure the text editor git uses, do:
```sh
   git config --global core.editor=vim
```
Replace vim with your text editor.

Here's an image  to demonstrate how this is done:

![add](http://i.imgur.com/WZnuR.png)

* Step 3, make a .patch file

Making a patch file is a simple process, and is done like so:
```sh
   git format-patch master..tutorial
```
Which should output the filename the patch saved to, the file contains your changes.

* Step 4, now, send the patch to some developer.
![send_patch](http://i.imgur.com/KIttX.png)

## Notes
* this step is optional (the sending email thing), alternatively you can use github issues to send patches etc. Use whatever you feel comfortable with.
* Read the manual page for git send-email if you're wondering how this is done.
* It's the developer freedom to choose whether your patch should be commited to the family tree or not, it really depends on how useful your patch is.

## Bonus
* It's good to write the signed-off-by line in your patch, to tell that this is your code, etc.  It's not of much use, however, you can use it to reward yourself a bit more.
![signedoffby](http://i.imgur.com/Kpfgh.png)

* See if your patch is good:
```sh
   git apply --check <patch file>
```
  This will tell you whether your patch file is formatted good or not. Remember to do this before sending!

Happy hacking!

