Summary:	Free OpenGL implementation. Runtime environment
Summary(pl):	Bezp³atna implementacja standardu OpenGL
Name:		Mesa
Version:	3.0
Release:	8
Copyright:	GPL
Group:		X11/Libraries
Group(pl):	X11/Biblioteki
Source0:	ftp://iris.ssec.wisc.edu/pub/Mesa/%{name}Lib-%{version}.tar.gz
Source1:	ftp://iris.ssec.wisc.edu/pub/Mesa/%{name}Demos-%{version}.tar.gz
Patch:		Mesa-misc.diff
URL:		http://www.mesa3d.org/
BuildPrereq:	XFree86-devel
BuildRoot:	/tmp/%{name}-%{version}-root

%define _prefix /usr/X11R6

%description
Mesa is a 3-D graphics library with an API which is very similar to that
of OpenGL*.  To the extent that Mesa utilizes the OpenGL command syntax
or state machine, it is being used with authorization from Silicon Graphics,
Inc.  However, the author makes no claim that Mesa is in any way a
compatible replacement for OpenGL or associated with Silicon Graphics, Inc.
Those who want a licensed implementation of OpenGL should contact a licensed
vendor.  This software is distributed under the terms of the GNU Library
General Public License, see the LICENSE file for details.

* OpenGL(R) is a registered trademark of Silicon Graphics, Inc.

%description -l pl
Mesa jest bibliotek± 3D bêd±c± darmowym odpowiednikiem standartu OpenGL(*).
* OpenGL jest zastrze¿onym znakiem towarowym firmy Silicon Graphics, Inc.

%package devel
Summary:	Development environment for Mesa
Summary(pl):	¦rodowisko programistyczne biblioteki Mesa
Group:		Development/Libraries
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
Header files and documentation needed for development.

%description -l pl devel
Pliki nag³ówkowe i dokumentacja do Mesy.

%package static
Summary:	Mesa static libraries
Summary(pl):	Biblioteki statyczne Mesy
Group:		Development/Libraries
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}

%description static
The static version of the Mesa libraries

%description -l pl static
Biblioteki statyczne Mesy.

%package glut
Summary:	GLUT library for Mesa
Summary(pl):	Biblioteka GLUT dla Mesy
Group:		X11/Libraries
Group(pl):	X11/Biblioteki
Requires:	%{name} = %{version}
Obsoletes:	glut

%description glut
The GLUT library.

%description -l pl glut
Biblioteka GLUT

%package glut-devel
Summary:	GLUT Development environment for Mesa
Summary(pl):	¦rodowisko programistyczne 'GLUT' dla biblioteki MESA.
Group:		Development/Libraries
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}
Obsoletes: 	glut-devel

%description glut-devel
Header files needed for development aplications using GLUT library.

%description -l pl glut-devel
Pliki nag³ówkowe do biblioteki GLUT.

%package glut-static
Summary:	GLUT static libraries
Summary(pl):	Biblioteki statyczne do biblioteki GLUT
Group:		Development/Libraries
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-glut-devel = %{version}
Obsoletes: 	glut-devel

%description glut-static
The static version of the GLUT library.

%description -l pl glut-static
Biblioteki statyczne GLUT.

%package demos
Summary:	Mesa Demos
Summary(pl):	Demonstracje mo¿liwo¶ci biblioteki MESA.
Group:		Development/Libraries
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description demos
Demonstration programs for the Mesa libraries.

%description -l pl demos
Programy demonstracyjne dla biblioteki Mesa.

%prep
%setup -q -n Mesa-%{version} -b 1
%patch -p1

%build
%ifarch alpha
make LIBS_ONLY=YES linux-alpha
make clean
make linux-alpha-elf
%endif

%ifarch ppc
make linux-ppc
%endif

%ifarch %{ix86}
make clean
make LIBS_ONLY=YES linux-386
make clean
make linux-386-elf
%endif

%ifarch sparc sparc64
make  linux-elf
%endif

(cd widgets-mesa; autoconf; \
CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s" \
./configure \
	--prefix=%{_prefix} \
	--target=%{_target_platform} \
	--host=%{_host}
make)

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/Mesa,%{_includedir},%{_mandir}/man3} \
	$RPM_BUILD_ROOT/usr/src/examples/Mesa

cp -dpr lib include $RPM_BUILD_ROOT%{_prefix}
cp -dpr util $RPM_BUILD_ROOT%{_libdir}/Mesa
cp -dpr book demos xdemos samples $RPM_BUILD_ROOT/usr/src/examples/Mesa
install Make-config $RPM_BUILD_ROOT%{_libdir}/Mesa

(cd widgets-mesa; \
make install \
	prefix=$RPM_BUILD_ROOT/usr/X11R6 \
	mandir=$RPM_BUILD_ROOT%{_mandir}/man3)

install */lib*.a $RPM_BUILD_ROOT%{_libdir}

strip $RPM_BUILD_ROOT%{_libdir}/{lib*so.*.*,Mesa/*/*} ||

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man3/* \
	FUTURE IAFA-PACKAGE LICENSE README* RELNOTES VERSIONS

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post   -p /sbin/ldconfig glut
%postun -p /sbin/ldconfig glut

%clean
rm -fr $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)

%ifnarch ppc
%attr(755,root,root) %{_libdir}/libMesa*.so.*.*
%else
%{_libdir}/libMesa*.a
%endif

%files glut
%defattr(644,root,root,755)
%ifnarch ppc
%attr(755,root,root) %{_libdir}/libglut.so.*
%else
%{_libdir}/libglut.a
%endif

%files glut-devel
%defattr(644,root,root,755)
%{_includedir}/GL/glut.h
%ifnarch ppc
%attr(755,root,root) %{_libdir}/libglut.so
%endif

%ifnarch ppc
%files glut-static
%defattr(644,root,root,755)
%{_libdir}/libglut.a
%endif

%files devel
%defattr(644,root,root,755)
%doc {FUTURE,IAFA-PACKAGE,LICENSE,RELNOTES,VERSIONS,README}.gz
%doc README.{3DFX,GGI,MGL,QUAKE,VIRGE,X11}.gz

%ifnarch ppc
%attr(755,root,root) %{_libdir}/libMesa*.so
%endif

%dir %{_libdir}/Mesa
%{_libdir}/Mesa/Make-config
%{_libdir}/Mesa/util

%dir /usr/X11R6/include/GL
%{_includedir}/GL/*.h
%{_mandir}/man3/*

%ifnarch ppc
%files static
%defattr(644,root,root,755)
%endif
%{_libdir}/libMesa*.a

%files demos
%defattr(644,root,root,755)
%dir /usr/src/examples/Mesa/book
%dir /usr/src/examples/Mesa/demos
%dir /usr/src/examples/Mesa/samples
%dir /usr/src/examples/Mesa/xdemos

%attr(-,root,root)/usr/src/examples/Mesa/book/*
%attr(-,root,root)/usr/src/examples/Mesa/demos/*
%attr(-,root,root)/usr/src/examples/Mesa/samples/*
%attr(-,root,root)/usr/src/examples/Mesa/xdemos/*
