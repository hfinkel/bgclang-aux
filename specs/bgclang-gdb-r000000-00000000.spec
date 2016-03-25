BuildRoot: /tmp
Prefix: /opt/bgclang

%define debug_package %{nil}
%define __strip /bin/true

%define rev 000000
%define date 00000000

Name: bgclang-gdb-r%{rev}-%{date}
Version: 1
Release: 1
Summary: GNU gdb for the BG/Q
License: GPLv3+
Vendor: ALCF (Argonne Leadership Computing Facility)
Group: Development/Compilers
URL: http://trac.alcf.anl.gov/projects/llvm-bgq/
Source0: gdb-7.11.tar.gz
Patch0: gdb-7.11-bgq.patch
AutoReqProv: no

%description
GNU gdb, patched for the BG/Q. This package is intended as a companion to
the bgclang package set.

%prep
%setup -q -n gdb-7.11
%patch -P 0 -p1

%build
mkdir -p gdb-build
cd gdb-build

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

	#define _GL_INLINE_HEADER_BEGIN
	#define _GL_INLINE_HEADER_END

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
for CF in $(find .. -name config.in | grep -v libdecnumber | grep -v gnulib); do
	echo '#include "dchange.h"' >> $CF
done
set +x

# Note: Currently the gas BG/Q patches are not clean, so we need --enable-checking=no
# TODO: Once the toolchain and libs are new enough for ld.gold, add --enable-gold=default 
../configure --without-auto-load-safe-path --prefix=/opt/bgclang/r%{rev}-%{date}/gdb --enable-checking=no --with-python=no

make -j32
cd ..

%install
cd gdb-build
make DESTDIR=%{buildroot} install
cd ..

%files
/opt/bgclang/r%{rev}-%{date}/gdb

