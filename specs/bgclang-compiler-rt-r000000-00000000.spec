BuildRoot: /tmp
Prefix: /opt/bgclang

%define debug_package %{nil}
%define __strip /bin/true

%define rev 000000
%define date 00000000

Name: bgclang-compiler-rt-r%{rev}-%{date}
BuildRequires: bgclang-r%{rev}-%{date}
Requires: bgclang-r%{rev}-%{date}
Version: 1
Release: 1
Summary: bgclang (A modern software programming environment for the BG/Q)
License: University of Illinois/NCSA Open Source License
Vendor: ALCF (Argonne Leadership Computing Facility)
Group: Development/Compilers
URL: http://trac.alcf.anl.gov/projects/llvm-bgq/
Source0: compiler-rt-bgq-r%{rev}-%{date}.tar.bz2
Source1: llvm-cmake-modules-r%{rev}.tar.bz2
AutoReqProv: no

%description
bgclang is a modern software programming environment for the BG/Q derived from
the LLVM/Clang projects (http://llvm.org/).

%prep
%setup -q -n compiler-rt

tar -jxf %{_sourcedir}/llvm-cmake-modules-r%{rev}.tar.bz2

rm -rf ../compiler-rt-build
mkdir -p ../compiler-rt-build

%build
export PATH=/soft/buildtools/cmake/current/bin:$PATH

PREFIX=$(rpm --dbpath %{_dbpath} -q --queryformat '%{INSTPREFIXES}' bgclang-r%{rev}-%{date} 2> /dev/null)
CC=$PREFIX/r%{rev}-%{date}/bin/bgclang
CXX="$CC++"

cd ../compiler-rt-build
rm -rf CMakeCache.txt CMakeFiles

DEST=%{buildroot}/opt/bgclang/r%{rev}-%{date}/compiler-rt

cat > bgclang-toolchain.cmake <<EOF;
SET(CMAKE_SYSTEM_NAME Linux)

SET(CMAKE_C_COMPILER $CC)
SET(CMAKE_CXX_COMPILER $CXX)

SET(CMAKE_FIND_ROOT_PATH
    /bgsys/drivers/ppcfloor
    /bgsys/drivers/ppcfloor/gnu-linux/powerpc64-bgq-linux)

ADD_DEFINITIONS(-I/bgsys/drivers/V1R2M0/ppc64 -I/bgsys/drivers/V1R2M0/ppc64/comm/sys/include -I/bgsys/drivers/V1R2M0/ppc64/spi/include -I/bgsys/drivers/V1R2M0/ppc64/spi/include/kernel/cnk)

SET(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
SET(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
SET(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)

SET(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "%{_builddir}/compiler-rt/llvm/cmake/modules")
include(CheckCXXCompilerFlag)
SET(LLVM_NATIVE_ARCH PowerPC)
SET(LLVM_USE_SANITIZER "")

SET(TARGET_TRIPLE powerpc64-bgq-linux)
EOF

cmake ../compiler-rt -DCMAKE_TOOLCHAIN_FILE=bgclang-toolchain.cmake -DCMAKE_INSTALL_PREFIX=$DEST -DLLVM_BINARY_DIR=$DEST -DLLVM_LIBRARY_DIR=$DEST -DLLVM_LIBRARY_OUTPUT_INTDIR=$DEST -DLLVM_TOOLS_BINARY_DIR=$DEST -DPACKAGE_VERSION=current -DCMAKE_CXX_FLAGS="-O3"

%install

DEST=%{buildroot}/opt/bgclang/r%{rev}-%{date}/compiler-rt

cd ../compiler-rt-build
make clean
make VERBOSE=1 install

%files
/opt/bgclang/r%{rev}-%{date}/compiler-rt

%post
cd ${RPM_INSTALL_PREFIX}

if [ ! -e compiler-rt ]; then
	ln -s current/compiler-rt compiler-rt
fi

