Summary:	Free OpenGL implementation. Runtime environment
Summary(pl):	Bezp³atna implementacja standardu OpenGL
Name:		Mesa
Version:	3.2
Release:	1
License:	GPL
Group:		X11/Libraries
Group(pl):	X11/Biblioteki
Source0:	ftp://ftp.mesa3d.org/mesa/%{name}Lib-%{version}.tar.bz2
Source1:	ftp://ftp.mesa3d.org/mesa/%{name}Demos-%{version}.tar.bz2
Patch0:		Mesa-paths.patch
URL:		http://www.mesa3d.org/
BuildRequires:	XFree86-devel
Provides:	OpenGL
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
Mesa is a 3-D graphics library with an API which is very similar to that of
OpenGL*. To the extent that Mesa utilizes the OpenGL command syntax or
state machine, it is being used with authorization from Silicon Graphics,
Inc. However, the author makes no claim that Mesa is in any way a
compatible replacement for OpenGL or associated with Silicon Graphics, Inc.
Those who want a licensed implementation of OpenGL should contact a
licensed vendor. This software is distributed under the terms of the GNU
Library General Public License, see the LICENSE file for details.

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
Provides:	OpenGL-devel

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
Provides:	OpenGL-static

%description static
The static version of the Mesa libraries

%description -l pl static
Biblioteki statyczne Mesy.

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
%patch0 -p1

%build
LDFLAGS="-s"; export LDFLAGS
CFLAGS="$RPM_OPT_FLAGS"; export CFLAGS
%configure \
	--enable-static \
	--enable-shared \
	--with-ggi="no" \
	--with-svga="no" \
	--disable-ggi-fbdev \
	--disable-ggi-genkgi \
%ifarch %{ix86} \
	--enable-x86 \
  %ifarch i686 \
	--enable-mmx \
	--enable-3dnow \
  %else \
    %ifarch k6 \
	--enable-mmx \
	--enable-3dnow" \
    %else \
	--disable-mmx \
	--disable-3dnow \
    %endif \
  %endif \
%else \
	--disable-x86 \
	--disable-mmx \
	--diable-3dnow \
%endif
	--host=%{_host}

make
	
(cd widgets-mesa; autoconf; \
LDFLAGS="-s"; export LDFLAGS
%configure \
	--host=%{_host}
make)

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_mandir}/man3

(cd widgets-mesa; \
make install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir}/man3)

install -d $RPM_BUILD_ROOT/usr/src/examples/Mesa
for l in book demos samples xdemos ; do
	cp -R $l $RPM_BUILD_ROOT/usr/src/examples/Mesa/$l
done

gzip -9nf docs/* || :
	
%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -fr $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/CONFIG.gz
%attr(755,root,root) %{_libdir}/libGL*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc docs/{IAFA-PACKAGE,README,RELNOTES-*,VERSIONS,CONFORM,COPYRIGHT,DEVINFO,*.spec}.gz
%doc docs/README.{3DFX,GGI,MGL,QUAKE,X11,THREADS}.gz
%attr(755,root,root) %{_libdir}/libGL*.so

%dir /usr/X11R6/include/GL
%{_includedir}/GL/*.h
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/libGL*.a

%files demos
%defattr(644,root,root,755)
%dir /usr/src/examples/Mesa/book
%dir /usr/src/examples/Mesa/demos
%dir /usr/src/examples/Mesa/samples
%dir /usr/src/examples/Mesa/xdemos

%doc /usr/src/examples/Mesa/book/*
%doc /usr/src/examples/Mesa/demos/*
%doc /usr/src/examples/Mesa/samples/*
%doc /usr/src/examples/Mesa/xdemos/*
