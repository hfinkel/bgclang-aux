BuildRoot: /tmp
Prefix: /opt/bgclang

%define debug_package %{nil}
%define __strip /bin/true

%define rev 000000
%define date 00000000

Name: bgclang-mpich3-r%{rev}-%{date}
Version: 1
Release: 1
Summary: MPICH v3 for the BG/Q
License: BSD
Vendor: ALCF (Argonne Leadership Computing Facility)
Group: Development/Compilers
URL: http://trac.alcf.anl.gov/projects/llvm-bgq/
Source0: MPICH-BlueGene.tar.bz2
Patch0: mpich3-bg-dt-noassert.patch
AutoReqProv: no

%description
MPICH v3 for the BG/Q, based on Rob Latham's MPICH-BlueGene fork:

  https://xgitlab.cels.anl.gov/robl/MPICH-BlueGene

which is mostly mpich-3.1.4 plus BG/Q I/O work from mpich-3.2.

%prep
%setup -q -n MPICH-BlueGene
%patch -P 0 -p1

%build
export PATH=/bgsys/drivers/ppcfloor/gnu-linux/bin:$PATH

COMPILERS="CC=powerpc64-bgq-linux-gcc CXX=powerpc64-bgq-linux-g++ F77=powerpc64-bgq-linux-gfortran FC=powerpc64-bgq-linux-gfortran"
BASEFLAGS="--host=powerpc64-bgq-linux --with-device=pamid --with-file-system=gpfs:BGQ --with-pm=no --with-namepublisher=no --enable-timer-type=device --enable-fortran=no"

NDEBUGFLAGS="--enable-fast=nochkmsg,notiming,O3 --with-assert-level=0 --disable-error-messages --disable-debuginfo"
NONLEGFLAGFS="--enable-thread-cs=per-object --with-atomic-primitives --enable-handle-allocation=tls --enable-refcount=lock-free --disable-predefined-refcount"

cd ..

mkdir -p MPICH-BlueGene-build.legacy
cd MPICH-BlueGene-build.legacy

../MPICH-BlueGene/configure --prefix=/opt/bgclang/r%{rev}-%{date}/mpi/bgclang-mpi3.legacy $BASEFLAGS $COMPILERS

make -j32
cd ..

mkdir -p MPICH-BlueGene-build.legacy.ndebug
cd MPICH-BlueGene-build.legacy.ndebug

../MPICH-BlueGene/configure --prefix=/opt/bgclang/r%{rev}-%{date}/mpi/bgclang-mpi3.legacy.ndebug $BASEFLAGS $NDEBUGFLAGS $COMPILERS

make -j32
cd ..

mkdir -p MPICH-BlueGene-build
cd MPICH-BlueGene-build

../MPICH-BlueGene/configure --prefix=/opt/bgclang/r%{rev}-%{date}/mpi/bgclang-mpi3 $BASEFLAGS $NONLEGFLAGFS $COMPILERS

make -j32
cd ..

mkdir -p MPICH-BlueGene-build.ndebug
cd MPICH-BlueGene-build.ndebug

../MPICH-BlueGene/configure --prefix=/opt/bgclang/r%{rev}-%{date}/mpi/bgclang-mpi3.ndebug $BASEFLAGS $NONLEGFLAGFS $NDEBUGFLAGS $COMPILERS

make -j32
cd ..

%install
export PATH=/bgsys/drivers/ppcfloor/gnu-linux/bin:$PATH

cd ..

cd MPICH-BlueGene-build.legacy
make DESTDIR=%{buildroot} install
cd ..

cd MPICH-BlueGene-build.legacy.ndebug
make DESTDIR=%{buildroot} install
cd ..

cd MPICH-BlueGene-build
make DESTDIR=%{buildroot} install
cd ..

cd MPICH-BlueGene-build.ndebug
make DESTDIR=%{buildroot} install
cd ..

for d in bgclang-mpi3 bgclang-mpi3.ndebug bgclang-mpi3.legacy bgclang-mpi3.legacy.ndebug; do
	cd %{buildroot}/opt/bgclang/r%{rev}-%{date}/mpi/$d/bin
	ln -s mpicc mpiclang
	ln -s mpicxx mpic++11
	ln -s mpicxx mpiclang++
	ln -s mpicxx mpiclang++11
	rm -f mpichversion mpivars parkill
	cd -

	cd %{buildroot}/opt/bgclang/r%{rev}-%{date}/mpi/$d/lib
	rm -rf pkgconfig
	rm -f *.la
	cd -
done

%files
/opt/bgclang/r%{rev}-%{date}/mpi/*/include
/opt/bgclang/r%{rev}-%{date}/mpi/*/bin
/opt/bgclang/r%{rev}-%{date}/mpi/*/lib

%post
cd ${RPM_INSTALL_PREFIX}

for d in bgclang-mpi3 bgclang-mpi3.ndebug bgclang-mpi3.legacy bgclang-mpi3.legacy.ndebug; do
	find r%{rev}-%{date}/mpi/$d/bin -type f -exec sed -i 's/powerpc64-bgq-linux-gcc/'$(echo ${RPM_INSTALL_PREFIX}/r%{rev}-%{date}/bin/bgclang |
		sed 's/\//\\\//g')'/g' {} \;
	find r%{rev}-%{date}/mpi/$d/bin -type f -exec sed -i 's/powerpc64-bgq-linux-g++/'$(echo ${RPM_INSTALL_PREFIX}/r%{rev}-%{date}/bin/bgclang++ |
		sed 's/\//\\\//g')'/g' {} \;
	find r%{rev}-%{date}/mpi/$d/bin -type f -exec sed -i '/Directory locations:/a \
ppcflr=$(readlink /bgsys/drivers/ppcfloor)' {} \;
	find r%{rev}-%{date}/mpi/$d/bin -type f -exec sed -i '/^CXX=/a \
if basename $0 | grep -q '"'"'11$'"'"'; then \
	CXX="${CXX}11" \
fi
' {} \;
	find r%{rev}-%{date}/mpi/$d/bin -type f -exec sed -i 's/\/bgsys\/drivers\/V[A-Z0-9]*\/ppc64/${ppcflr}/g' {} \;
	find r%{rev}-%{date}/mpi/$d/bin -type f -exec sed -i 's/--enable-new-dtags/--enable-new-dtags -Wl,-rpath -Wl,${ppcflr}\/comm\/lib/g' {} \;
	find r%{rev}-%{date}/mpi/$d/bin -type f -exec sed -i 's/\/opt\/bgclang/'$(echo ${RPM_INSTALL_PREFIX} |
		sed 's/\//\\\//g')'/g' {} \;
done

