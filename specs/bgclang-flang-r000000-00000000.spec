BuildRoot: /tmp
Prefix: /opt/bgclang

%define debug_package %{nil}
%define __strip /bin/true

%define rev 000000
%define date 00000000

Name: bgclang-flang-r%{rev}-%{date}
BuildRequires: bgclang-r%{rev}-%{date}
BuildRequires: bgclang-libomp-r%{rev}-%{date}
Requires: bgclang-r%{rev}-%{date}
Requires: bgclang-libomp-r%{rev}-%{date}
Version: 1
Release: 1
Summary: bgclang (A modern software programming environment for the BG/Q)
License: Apache 2 License
Vendor: ALCF (Argonne Leadership Computing Facility)
Group: Development/Compilers
URL: http://trac.alcf.anl.gov/projects/llvm-bgq/
Source0: flang-bgq-r%{rev}-%{date}.tar.bz2
AutoReqProv: no

%description
bgclang is a modern software programming environment for the BG/Q derived from
the LLVM/Clang projects (http://llvm.org/).

%prep
%setup -q -n flang

%build
export PATH=/soft/buildtools/cmake/current/bin:$PATH
export PATH=/soft/interpreters/python-2.7.9/powerpc64-linux-gnu/bin:$PATH

DEST=%{buildroot}/opt/bgclang/r%{rev}-%{date}

PREFIX=$(rpm --dbpath %{_dbpath} -q --queryformat '%{INSTPREFIXES}' bgclang-r%{rev}-%{date} 2> /dev/null)
CC=$PREFIX/r%{rev}-%{date}/bin/clang
FLANG=$PREFIX/r%{rev}-%{date}/bin/flang
LLVMCFG=$PREFIX/r%{rev}-%{date}/bin/llvm-config
LOMP=$PREFIX/r%{rev}-%{date}/omp/lib/libomp.so

LD_LIBRARY_PATH="$PREFIX/stage3/libc++/lib:$LD_LIBRARY_PATH"
export LD_LIBRARY_PATH

CXXLDFLAGS="-L$PREFIX/stage3/libc++/lib -stdlib=libc++ '-Wl,-rpath,\$ORIGIN/../../stage3/libc++/lib' -Wl,--build-id"

rm -rf ../flang-build
mkdir -p ../flang-build
cd ../flang-build

cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=$DEST -DCMAKE_C_COMPILER=$CC -DCMAKE_CXX_COMPILER=$CC++ -DCMAKE_Fortran_COMPILER=$FLANG -DLLVM_CONFIG=$LLVMCFG -DCMAKE_CXX_FLAGS="-I$PREFIX/stage3/libc++/include/c++/v1 -Qunused-arguments $CXXLDFLAGS" -DCMAKE_EXE_LINKER_FLAGS="$CXXLDFLAGS" -DCMAKE_SHARED_LINKER_FLAGS="$CXXLDFLAGS" -DCMAKE_MODULE_LINKER_FLAGS="$CXXLDFLAGS" -DFLANG_LIBOMP=$LOMP -DCMAKE_CXX_FLAGS_RELEASE="-std=gnu++11 -O3 -g -mno-altivec" -DCMAKE_C_FLAGS_RELEASE="-std=c11 -O3 -g -mno-altivec" -DCMAKE_FORTRAN_FLAGS_RELEASE="-O2 -mno-altivec" ../flang
make -j32 VERBOSE=1 || true
make -j32 VERBOSE=1

%install
DEST=%{buildroot}/opt/bgclang/r%{rev}-%{date}

LD_LIBRARY_PATH="$PREFIX/stage3/libc++/lib:$LD_LIBRARY_PATH"
export LD_LIBRARY_PATH

cd ../flang-build
make VERBOSE=1 install

%files
/opt/bgclang/r%{rev}-%{date}

%post
cd ${RPM_INSTALL_PREFIX}

cd r%{rev}-%{date}
(cd wbin && ln -sf ../bin/bgflang bgflang && ln -sf ../bin/bgflang powerpc64-bgq-linux-flang)

