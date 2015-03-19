BuildRoot: /tmp
Prefix: /opt/bgclang

%define debug_package %{nil}
%define __strip /bin/true

%define rev 000000
%define date 00000000

Name: bgclang-libcxx-r%{rev}-%{date}
BuildRequires: bgclang-r%{rev}-%{date}
Requires: bgclang-r%{rev}-%{date}
Version: 1
Release: 1
Summary: bgclang (A modern software programming environment for the BG/Q)
License: University of Illinois/NCSA Open Source License
Vendor: ALCF (Argonne Leadership Computing Facility)
Group: Development/Compilers
URL: http://trac.alcf.anl.gov/projects/llvm-bgq/
Source0: libcxx-bgq-r%{rev}-%{date}.tar.bz2
Source1: libstdc++fixup-r%{rev}-%{date}.tar.bz2
AutoReqProv: no

%description
bgclang is a modern software programming environment for the BG/Q derived from
the LLVM/Clang projects (http://llvm.org/).

%prep
%setup -q -n libcxx

sed -i 's/\/c++\/v1//g' CMakeLists.txt
sed -i 's/\/c++\/v1//g' include/CMakeLists.txt

(cd .. && tar -jxf %{_sourcedir}/libstdc++fixup-r%{rev}-%{date}.tar.bz2)

%build
export PATH=/soft/buildtools/cmake/current/bin:$PATH

PREFIX=$(rpm --dbpath %{_dbpath} -q --queryformat '%{INSTPREFIXES}' bgclang-r%{rev}-%{date} 2> /dev/null)
CC=$PREFIX/r%{rev}-%{date}/bin/bgclang
CXX="$CC++"

export CC
export CXX

DEST=%{buildroot}/opt/bgclang/r%{rev}-%{date}/libc++

mkdir -p ../libcxx-build
cd ../libcxx-build
rm -rf CMakeCache.txt CMakeFiles

INCPATHS='/bgsys/drivers/toolchain/V1R2M1_base_4.7.2/gnu-linux-4.7.2/powerpc64-bgq-linux/include/c++/4.7.2;/bgsys/drivers/toolchain/V1R2M1_base_4.7.2/gnu-linux-4.7.2/powerpc64-bgq-linux/include/c++/4.7.2/powerpc64-bgq-linux'

cmake ../libcxx -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_C_COMPILER=$CC -DCMAKE_CXX_COMPILER=$CXX -DCMAKE_INSTALL_PREFIX=$DEST -DLIBCXX_CXX_ABI=libstdc++ -DLIBCXX_LIBSUPCXX_INCLUDE_PATHS="$INCPATHS" -DCMAKE_SHARED_LINKER_FLAGS='-Wl,--build-id'
make clean
make VERBOSE=1

mkdir -p ../libcxx-build-static
cd ../libcxx-build-static
rm -rf CMakeCache.txt CMakeFiles

cmake ../libcxx -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_C_COMPILER=$CC -DCMAKE_CXX_COMPILER=$CXX -DCMAKE_INSTALL_PREFIX=$DEST -DLIBCXX_CXX_ABI=libstdc++ -DLIBCXX_LIBSUPCXX_INCLUDE_PATHS="$INCPATHS" -DLIBCXX_ENABLE_SHARED=0
make clean
make VERBOSE=1

%install
DEST=%{buildroot}/opt/bgclang/r%{rev}-%{date}/libc++

cd ../libcxx-build
make VERBOSE=1 install

cd ../libcxx-build-static
make VERBOSE=1 install

rm -f ${DEST}/include/Makefile
rm -f ${DEST}/include/cmake_install.cmake

mkdir %{buildroot}/opt/bgclang/r%{rev}-%{date}/libstdc++fixup

%files
/opt/bgclang/r%{rev}-%{date}/libc++
/opt/bgclang/r%{rev}-%{date}/libstdc++fixup

%post
cd ${RPM_INSTALL_PREFIX}

for d in libc++ libstdc++fixup; do
	if [ ! -e $d ]; then
		ln -s current/$d $d
	fi
done

