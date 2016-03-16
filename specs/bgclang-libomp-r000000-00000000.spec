BuildRoot: /tmp
Prefix: /opt/bgclang

%define debug_package %{nil}
%define __strip /bin/true

%define rev 000000
%define date 00000000

Name: bgclang-libomp-r%{rev}-%{date}
BuildRequires: bgclang-r%{rev}-%{date}
Requires: bgclang-r%{rev}-%{date}
Version: 1
Release: 1
Summary: bgclang (A modern software programming environment for the BG/Q)
License: University of Illinois/NCSA Open Source License
Vendor: ALCF (Argonne Leadership Computing Facility)
Group: Development/Compilers
URL: http://trac.alcf.anl.gov/projects/llvm-bgq/
Source0: openmp-bgq-r%{rev}-%{date}.tar.bz2
AutoReqProv: no

%description
bgclang is a modern software programming environment for the BG/Q derived from
the LLVM/Clang projects (http://llvm.org/).

%prep
%setup -q -n openmp

%build
export PATH=/soft/buildtools/cmake/current/bin:$PATH
export PATH=/soft/interpreters/python-2.7.9/powerpc64-linux-gnu/bin:$PATH

PREFIX=$(rpm --dbpath %{_dbpath} -q --queryformat '%{INSTPREFIXES}' bgclang-r%{rev}-%{date} 2> /dev/null)
CC=$PREFIX/r%{rev}-%{date}/bin/bgclang

DEST=%{buildroot}/opt/bgclang/r%{rev}-%{date}/omp

rm -rf ../openmp-build
mkdir -p ../openmp-build
cd ../openmp-build

cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_INSTALL_PREFIX=$DEST -DCMAKE_C_COMPILER=$CC -DCMAKE_CXX_COMPILER=$CC++ -DLIBOMP_OMPT_SUPPORT=ON -DLIBOMP_OMPT_BLAME=ON -DLIBOMP_OMPT_TRACE=ON -DCMAKE_SHARED_LINKER_FLAGS='-Wl,--build-id' -DLIBOMP_USE_ITT_NOTIFY=0 ../openmp
make clean
make VERBOSE=1

rm -rf ../openmp-build-static
mkdir -p ../openmp-build-static
cd ../openmp-build-static

cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_INSTALL_PREFIX=$DEST -DCMAKE_C_COMPILER=$CC -DCMAKE_CXX_COMPILER=$CC++ -DLIBOMP_OMPT_SUPPORT=ON -DLIBOMP_OMPT_BLAME=ON -DLIBOMP_OMPT_TRACE=ON -DLIBOMP_ENABLE_SHARED=0 -DLIBOMP_USE_ITT_NOTIFY=0 ../openmp
make clean
make VERBOSE=1

%install
DEST=%{buildroot}/opt/bgclang/r%{rev}-%{date}/omp

cd ../openmp-build
make VERBOSE=1 install

cd ../openmp-build-static
make VERBOSE=1 install

%files
/opt/bgclang/r%{rev}-%{date}/omp

%post
cd ${RPM_INSTALL_PREFIX}

if [ ! -e omp ]; then
	ln -s current/omp omp
fi

