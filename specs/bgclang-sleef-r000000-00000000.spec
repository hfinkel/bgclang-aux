BuildRoot: /tmp
Prefix: /opt/bgclang

%define debug_package %{nil}
%define __strip /bin/true

%define rev 000000
%define date 00000000

Name: bgclang-sleef-r%{rev}-%{date}
BuildRequires: bgclang-r%{rev}-%{date}
Requires: bgclang-r%{rev}-%{date}
Version: 1
Release: 1
Summary: bgclang (A modern software programming environment for the BG/Q)
License: University of Illinois/NCSA Open Source License
Vendor: ALCF (Argonne Leadership Computing Facility)
Group: Development/Compilers
URL: http://trac.alcf.anl.gov/projects/llvm-bgq/
Source0: sleef-bgq-r%{rev}-%{date}.tar.bz2
AutoReqProv: no

%description
bgclang is a modern software programming environment for the BG/Q derived from
the LLVM/Clang projects (http://llvm.org/).

%prep
%setup -q -n sleef

%build
PREFIX=$(rpm --dbpath %{_dbpath} -q --queryformat '%{INSTPREFIXES}' bgclang-r%{rev}-%{date} 2> /dev/null)
CC=$PREFIX/r%{rev}-%{date}/bin/bgclang

set -x
cd simd
for f in sleefsimddp sleefsimdsp ../purec/sleefdp ../purec/sleefsp; do
	$CC -O3 -fPIC -I. -DADD_UNDERSCORES -DNO_EXT_STRUCTS -DENABLE_QPX -c $f.c -g -o $f.o
done

ar cr libsleef.a sleefsimddp.o sleefsimdsp.o ../purec/sleefdp.o ../purec/sleefsp.o
$CC sleefsimddp.o sleefsimdsp.o ../purec/sleefdp.o ../purec/sleefsp.o -o libsleef.so.1.0 -shared -Wl,-soname,libsleef.so.1
ln -s libsleef.so.1.0 libsleef.so.1
ln -s libsleef.so.1 libsleef.so
set +x

%install
DEST=%{buildroot}/opt/bgclang/r%{rev}-%{date}/sleef

set -x
mkdir -p $DEST
mkdir -p $DEST/lib
mkdir -p $DEST/include

cd simd
for f in libsleef.a libsleef.so.1.0 libsleef.so.1 libsleef.so; do
	cp -d $f $DEST/lib/
done

cp qpxmath.h $DEST/include/
cp qpxmath.include $DEST/include/

cd ../purec
cp fastmath.h $DEST/include/
cp fastmath.include $DEST/include/

set +x

%files
/opt/bgclang/r%{rev}-%{date}/sleef

%post
cd ${RPM_INSTALL_PREFIX}

if [ ! -e sleef ]; then
	ln -s current/sleef sleef
fi

