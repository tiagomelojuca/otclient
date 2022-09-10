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
