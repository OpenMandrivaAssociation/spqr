%define	NAME	SPQR
%define	major	1
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname %{name} -d

Name:		spqr
Version:	1.3.1
Release:	2
Epoch:		1
Summary:	Implementation of the multifrontal sparse QR factorization
Group:		System/Libraries
License:	GPLv2+
URL:		https://www.cise.ufl.edu/research/sparse/SPQR/
Source0:	http://www.cise.ufl.edu/research/sparse/SPQR/%{NAME}-%{version}.tar.gz
BuildRequires:	blas-devel
BuildRequires:	colamd-devel
BuildRequires:	cholmod-devel
BuildRequires:	libatlas-devel
BuildRequires:	suitesparseconfig-devel >= 4.2.1-3
BuildRequires:	tbb-devel

%description
SuiteSparseQR is an implementation of the multifrontal sparse QR factorization
method.
Parallelism is exploited both in the BLAS and across different frontal matrices
using Intel's Threading Building Blocks, a shared-memory programming model
for modern multicore architectures. It can obtain a substantial fraction of the
theoretical peak performance of a multicore computer. The package is written in
C++ with user interfaces for MATLAB, C, and C++.

%package -n %{libname}
Summary:	Library of routines for multifrontal sparse QR factorization
Group:		System/Libraries

%description -n %{libname}
SuiteSparseQR is an implementation of the multifrontal sparse QR factorization
method.
Parallelism is exploited both in the BLAS and across different frontal matrices
using Intel's Threading Building Blocks, a shared-memory programming model
for modern multicore architectures. It can obtain a substantial fraction of the
theoretical peak performance of a multicore computer. The package is written in
C++ with user interfaces for MATLAB, C, and C++.

%package -n %{devname}
Summary:	C routines for permuting sparse matricies prior to factorization
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
SuiteSparseQR is an implementation of the multifrontal sparse QR factorization
method.
Parallelism is exploited both in the BLAS and across different frontal matrices
using Intel's Threading Building Blocks, a shared-memory programming model
for modern multicore architectures. It can obtain a substantial fraction of the
theoretical peak performance of a multicore computer. The package is written in
C++ with user interfaces for MATLAB, C, and C++.

This package contains the files needed to develop applications that 
use %{NAME}.

%prep
%setup -q -c -n %{name}-%{version}
cd %{NAME}
find . -perm 640 | xargs chmod 644
mkdir ../SuiteSparse_config
ln -sf %{_includedir}/suitesparse/SuiteSparse_config.* ../SuiteSparse_config

%build
cd %{NAME}
pushd Lib
    %make CC=gcc CONFIG="" CFLAGS="%{optflags} -fPIC -I%{_includedir}/suitesparse" INC=
    gcc %{ldflags} -shared -Wl,-soname,lib%{name}.so.%{major} -o lib%{name}.so.%{version} *.o -L%{_libdir}/atlas -lcblas -lblas -llapack -lcolamd -lcholmod -lsuitesparseconfig -ltbb -ltbbmalloc -lm
popd

%install
cd %{NAME}
for f in Lib/*.so*; do
    install -m755 $f -D %{buildroot}%{_libdir}/`basename $f`
done
for f in Lib/*.a; do
    install -m644 $f -D %{buildroot}%{_libdir}/`basename $f`
done
for f in Include/*.h; do
    install -m644 $f -D %{buildroot}%{_includedir}/suitesparse/`basename $f`
done

ln -s lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so

install -d -m 755 %{buildroot}%{_docdir}/%{name}
install -m 644 Doc/README.txt Doc/*.pdf Doc/ChangeLog %{buildroot}%{_docdir}/%{name}

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{devname}
%{_docdir}/%{name}
%{_includedir}/suitesparse/*.h
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}.a

%changelog
* Fri Feb 28 2014 Per Øyvind Karlsen <proyvind@moondrake.org> 1.3.1-1
- initial mdk release
