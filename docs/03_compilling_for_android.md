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
