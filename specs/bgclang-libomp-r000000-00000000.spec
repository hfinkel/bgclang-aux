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
PREFIX=$(rpm --dbpath %{_dbpath} -q --queryformat '%{INSTPREFIXES}' bgclang-r%{rev}-%{date} 2> /dev/null)
CC=$PREFIX/r%{rev}-%{date}/bin/bgclang

cd runtime
make -f Makefile.bgq CC=$CC CXX=$CC++
cd ..

%install
DEST=%{buildroot}/opt/bgclang/r%{rev}-%{date}/omp

set -x
mkdir -p $DEST
mkdir -p $DEST/lib
mkdir -p $DEST/include

cd runtime/build
for f in libiomp5.a libiomp5.so.1.0 libiomp5.so.1 libiomp5.so; do
	cp -d $f $DEST/lib/
done

cp omp.h $DEST/include/omp.h
set +x

%files
/opt/bgclang/r%{rev}-%{date}/omp

%post
cd ${RPM_INSTALL_PREFIX}

if [ ! -e omp ]; then
	ln -s current/omp omp
fi

