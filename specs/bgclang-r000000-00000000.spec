BuildRoot: /tmp
Prefix: /opt/bgclang

%define debug_package %{nil}
%define __strip /bin/true

%define rev 000000
%define date 00000000

Name: bgclang-r%{rev}-%{date}
BuildRequires: bgclang-stage2
BuildRequires: bgclang-stage2-libcxx
BuildRequires: bgclang-binutils-r%{rev}-%{date}
Requires: bgclang-stage2-libcxx
Requires: bgclang-binutils-r%{rev}-%{date}
Requires: bgclang-gdb-r%{rev}-%{date}
Requires: toolchain-fixup = 4.7.2
Version: 1
Release: 1
Summary: bgclang (A modern software programming environment for the BG/Q)
License: University of Illinois/NCSA Open Source License
Vendor: ALCF (Argonne Leadership Computing Facility)
Group: Development/Compilers
URL: http://trac.alcf.anl.gov/projects/llvm-bgq/
Source0: llvm-bgq-r%{rev}-%{date}.tar.bz2
Source1: clang-bgq-r%{rev}-%{date}.tar.bz2
Source2: bin-r%{rev}-%{date}.tar.bz2
Source3: mpi-r%{rev}-%{date}.tar.bz2
Source4: wbin-r%{rev}-%{date}.tar.bz2
Source5: clang-tools-extra-r%{rev}.tar.bz2
Source6: ppcfloor-fixup-r%{rev}-%{date}.tar.bz2
Source7: c11threads-r%{rev}-%{date}.tar.bz2

AutoReqProv: no

%description
bgclang is a modern software programming environment for the BG/Q derived from
the LLVM/Clang projects (http://llvm.org/).

Note: The LLVMgold.so binary is distributed under the terms of the GPLv3.

%prep
%setup -q -n llvm
%setup -q -T -D -a 1 -n llvm/tools
cd ..
%setup -q -T -D -a 5 -n llvm/tools/clang/tools
cd ../../..

cd tools/clang

cd ../..

%build
export PATH=/soft/buildtools/cmake/current/bin:$PATH
export PATH=/soft/interpreters/python-2.7.9/powerpc64-linux-gnu/bin:$PATH

PREFIX=$(rpm --dbpath %{_dbpath} -q --queryformat '%{INSTPREFIXES}' bgclang-binutils-r%{rev}-%{date} 2> /dev/null)
BUINC=$PREFIX/r%{rev}-%{date}/binutils/include

cd ../../..
rm -rf ../llvm-build
mkdir -p ../llvm-build

LD_LIBRARY_PATH="$PREFIX/stage2/libc++/lib:$LD_LIBRARY_PATH"
export LD_LIBRARY_PATH

CXXLDFLAGS="-L$PREFIX/stage2/libc++/lib -stdlib=libc++ '-Wl,-rpath,\$ORIGIN/../../stage2/libc++/lib' -Wl,--build-id"

(cd ../llvm-build && cmake -DCMAKE_C_COMPILER=$PREFIX/stage2/bin/clang -DCMAKE_CXX_COMPILER=$PREFIX/stage2/bin/clang++ -DLLVM_ENABLE_EH=ON -DLLVM_ENABLE_RTTI=ON -DCMAKE_CXX_FLAGS="-I$PREFIX/stage2/libc++/include/c++/v1" -DCMAKE_EXE_LINKER_FLAGS="$CXXLDFLAGS" -DCMAKE_SHARED_LINKER_FLAGS="$CXXLDFLAGS" -DCMAKE_MODULE_LINKER_FLAGS="$CXXLDFLAGS" -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS_RELEASE="-O3 -fno-altivec" -DCMAKE_INSTALL_PREFIX=/opt/bgclang/r%{rev}-%{date} -DLLVM_BINUTILS_INCDIR=$BUINC -DCLANG_VENDOR="bgclang r%{rev}-%{date}" ../llvm)
(cd ../llvm-build && make -j32)

%install
PREFIX=$(rpm --dbpath %{_dbpath} -q --queryformat '%{INSTPREFIXES}' bgclang-binutils-r%{rev}-%{date} 2> /dev/null)

LD_LIBRARY_PATH="$PREFIX/stage2/libc++/lib:$LD_LIBRARY_PATH"
export LD_LIBRARY_PATH

cd ../../..
(cd ../llvm-build && make -j32 DESTDIR=%{buildroot} install)
cp -Rf %{_builddir}/llvm/tools/clang/tools/scan-{build,view} %{buildroot}/opt/bgclang/r%{rev}-%{date}/
(cd %{buildroot}/opt/bgclang/r%{rev}-%{date}/lib/clang/?.* && rm -f lib && ln -si ../../../compiler-rt/lib lib)
(cd %{buildroot}/opt/bgclang/r%{rev}-%{date}/lib/clang/?.*/include && rm -f sanitizer && ln -si ../../../../compiler-rt/include/sanitizer sanitizer)

(cd %{buildroot}/opt/bgclang/r%{rev}-%{date} && tar -xjvf %{_sourcedir}/bin-r%{rev}-%{date}.tar.bz2)
(cd %{buildroot}/opt/bgclang/r%{rev}-%{date} && tar -xjvf %{_sourcedir}/wbin-r%{rev}-%{date}.tar.bz2)
(cd %{buildroot}/opt/bgclang/r%{rev}-%{date} && tar -xjvf %{_sourcedir}/mpi-r%{rev}-%{date}.tar.bz2)
(cd %{buildroot}/opt/bgclang/r%{rev}-%{date} && tar -xjvf %{_sourcedir}/ppcfloor-fixup-r%{rev}-%{date}.tar.bz2)
(cd %{buildroot}/opt/bgclang/r%{rev}-%{date} && tar -xjvf %{_sourcedir}/c11threads-r%{rev}-%{date}.tar.bz2)

%files
/opt/bgclang/r%{rev}-%{date}

%post
cd ${RPM_INSTALL_PREFIX}

sed -i 's/\/home\/projects\/llvm\/r[0-9]\+-[0-9]\+/'$(echo ${RPM_INSTALL_PREFIX}/r%{rev}-%{date} |
	sed 's/\//\\\//g')'/g' r%{rev}-%{date}/bin/bgclang
sed -i 's/r[0-9]\+-[0-9]\+/r%{rev}-%{date}/g' r%{rev}-%{date}/bin/bgclang
find r%{rev}-%{date}/mpi -type f -exec sed -i 's/\/home\/projects\/llvm/'$(echo ${RPM_INSTALL_PREFIX}/r%{rev}-%{date} |
	sed 's/\//\\\//g')'/g' {} \;

if [ ! -e current ]; then
	ln -s r%{rev}-%{date} current
fi

for d in bin docs include lib scan-build scan-view share wbin mpi; do
	if [ ! -e $d ]; then
		ln -s current/$d $d
	fi
done

cd r%{rev}-%{date}
(cd binutils/lib && mkdir -p bfd-plugins && cd bfd-plugins && ln -sf ../../../lib/LLVMgold.so && ln -sf ../../../lib/libLTO.so && ln -sf ../../../lib/libLLVM-4.?svn.so && ln -sf ../../../../stage2/libc++/lib/libc++.so.1)
(cd binutils/bin && for f in ar nm ld* as ranlib strip; do (cd ../../wbin && ln -sf ../binutils/bin/$f bgclang-$f && ln -sf ../binutils/bin/$f powerpc64-bgq-linux-clang-$f); done)
(cd gdb/bin && for f in gdb; do (cd ../../wbin && ln -sf ../gdb/bin/$f bgclang-$f && ln -sf ../gdb/bin/$f powerpc64-bgq-linux-clang-$f); done)
(cd wbin && ln -sf ../bin/llvm-opt-report bgclang-opt-report)

