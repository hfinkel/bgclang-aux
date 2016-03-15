BuildRoot: /tmp
Prefix: /opt/bgclang

%define debug_package %{nil}
%define __strip /bin/true

%define rev 000000
%define date 00000000

Name: bgclang-binutils-r%{rev}-%{date}
Version: 1
Release: 1
Summary: GNU binutils for the BG/Q
License: GPLv3+
Vendor: ALCF (Argonne Leadership Computing Facility)
Group: Development/Compilers
URL: http://trac.alcf.anl.gov/projects/llvm-bgq/
Source0: binutils-2.26.tar.bz2
Patch0: binutils-2.26-bgq.patch
AutoReqProv: no

%description
GNU binutils, patched for the BG/Q. This package is intended as a companion to
the bgclang package set.

%prep
%setup -q -n binutils-2.26
%patch -P 0 -p1

%build
mkdir -p build
cd build

cat >> ../include/dchange.h <<-EOF;
	#ifndef DCHANGE
	#define DCHANGE

	#undef LOCALEDIR
	#undef BINDIR
	#undef TOOLBINDIR
	#undef TOOLLIBDIR

	#define LOCALEDIR_ "/../share/locale"
	#define BINDIR_    "/../bin"
	#define TOOLBINDIR_ "/../powerpc64-unknown-linux-gnu/bin"
	#define TOOLLIBDIR_ "/../powerpc64-unknown-linux-gnu/lib"

	#include <unistd.h>
	#include <string.h>
	#include <stdlib.h>

	#pragma GCC system_header

	extern char *xdirname(char *path) asm("dirname");
	static char *__exedir(const char *suf) {
		char exe[4096];
		ssize_t exelen;
		char *exedir, *dir;
		if ((exelen = readlink("/proc/self/exe", exe, 4096-1)) != -1)
			exe[exelen] = '\0';
		else
			exit(-1);

		exedir = xdirname(exe);
		dir = (char *) calloc(1, strlen(exedir) + strlen(suf) + 1);
		strcat(dir, exedir);
		strcat(dir, suf);
		return dir;
	}

	#define LOCALEDIR  __exedir(LOCALEDIR_)
	#define BINDIR     __exedir(BINDIR_)
	#define TOOLBINDIR __exedir(TOOLBINDIR_)
	#define TOOLLIBDIR __exedir(TOOLLIBDIR_)

	#endif
EOF

set -x
for CF in $(find .. -name config.in); do
	echo '#include "dchange.h"' >> $CF
done
set +x

# Note: Currently the gas BG/Q patches are not clean, so we need --enable-checking=no
# TODO: Once the toolchain and libs are new enough for ld.gold, add --enable-gold=default 
../configure --enable-gold --enable-plugins --prefix=/opt/bgclang/r%{rev}-%{date}/binutils --enable-checking=no

make -j16 all-gold
make -j16
cd ..

%install
cd build
make DESTDIR=%{buildroot} install
cd ..

%files
/opt/bgclang/r%{rev}-%{date}/binutils

