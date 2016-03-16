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
AutoReqProv: no

%description
bgclang is a modern software programming environment for the BG/Q derived from
the LLVM/Clang projects (http://llvm.org/).

%prep
%setup -q -n compiler-rt

rm -rf ../compiler-rt-build
mkdir -p ../compiler-rt-build

%build
export PATH=/soft/buildtools/cmake/current/bin:$PATH
export PATH=/soft/interpreters/python-2.7.9/powerpc64-linux-gnu/bin:$PATH

PREFIX=$(rpm --dbpath %{_dbpath} -q --queryformat '%{INSTPREFIXES}' bgclang-r%{rev}-%{date} 2> /dev/null)
CC=$PREFIX/r%{rev}-%{date}/bin/bgclang
CXX="$CC++"

cd ../compiler-rt-build

DEST=%{buildroot}/opt/bgclang/r%{rev}-%{date}/compiler-rt

cmake ../compiler-rt -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_C_COMPILER=$CC -DCMAKE_CXX_COMPILER=$CXX -DCMAKE_INSTALL_PREFIX=$DEST -DLLVM_CONFIG_PATH=$PREFIX/r%{rev}-%{date}/bin/llvm-config -DCMAKE_CXX_FLAGS="-O3"

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

