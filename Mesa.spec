#
# TODO:
# - separate libGL/libGLU/libGLw,progs?
#
# Conditional build:
%bcond_with	glide	# with GLIDE (broken now)
%bcond_without	motif	# build static libGLw without Motif interface
#
Summary:	Free OpenGL implementation
Summary(pl):	Wolnodostêpna implementacja standardu OpenGL
Name:		Mesa
Version:	6.4
Release:	1
License:	MIT (core), LGPL (MesaGLU), SGI (GLU,libGLw) and others - see COPYRIGHT file
Group:		X11/Libraries
Source0:	http://dl.sourceforge.net/mesa3d/%{name}Lib-%{version}.tar.bz2
# Source0-md5:	85a84e47a3f718f752f306b9e0954ef6
Source1:	http://dl.sourceforge.net/mesa3d/%{name}Demos-%{version}.tar.bz2
# Source1-md5:	1a8c4d4fc699233f5fdb902b8753099e
URL:		http://www.mesa3d.org/
BuildRequires:	expat-devel
BuildRequires:	libdrm-devel >= 1.0.4-1.20051022
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.4d
%{?with_motif:BuildRequires:	motif-devel}
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	xorg-lib-libXp-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
BuildRequires:	xorg-proto-glproto-devel
BuildRequires:	xorg-util-makedepend
%if %{with glide}
BuildRequires:	Glide3-DRI-devel
Requires:	Glide3-DRI
%endif
Provides:	OpenGL = 1.5
Provides:	OpenGL-GLU = 1.3
# reports version 1.3, but supports glXGetProcAddress() from 1.4
Provides:	OpenGL-GLX = 1.4
Obsoletes:	XFree86-OpenGL-libGL
Obsoletes:	XFree86-OpenGL-libs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# avoid XFree86-OpenGL* dependency
# Glide3 can be provided by Glide_V3-DRI or Glide_V5-DRI
%define		_noautoreqdep	libGL.so.1 libGLU.so.1 libOSMesa.so.4   libglide3.so.3

%define		_sysconfdir	/etc/X11

%description
Mesa is a 3-D graphics library with an API which is very similar to
that of OpenGL(R). To the extent that Mesa utilizes the OpenGL command
syntax or state machine, it is being used with authorization from
Silicon Graphics, Inc. However, the author does not possess an OpenGL
license from SGI, and makes no claim that Mesa is in any way a
compatible replacement for OpenGL or associated with SGI.

%description -l pl
Mesa jest bibliotek± grafiki 3D z API bardzo podobnym do OpenGL(R). Do
tego stopnia, ¿e Mesa u¿ywa sk³adni i automatu OpenGL jest u¿ywana z
autoryzacj± Silicon Graphics, Inc. Jednak autor nie posiada licencji
OpenGL od SGI i nie twierdzi, ¿e Mesa jest kompatybilnym zamiennikiem
OpenGL ani powi±zana z SGI.

%package devel
Summary:	Development environment for Mesa
Summary(pl):	¦rodowisko programistyczne biblioteki Mesa
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	xorg-lib-libX11-devel
Requires:	xorg-lib-libXp-devel
Provides:	OpenGL-devel = 1.5
Provides:	OpenGL-GLU-devel = 1.3
Provides:	OpenGL-GLX-devel = 1.4
Obsoletes:	XFree86-OpenGL-devel
Obsoletes:	XFree86-OpenGL-devel-base

%description devel
Header files and documentation needed for development.

%description devel -l pl
Pliki nag³ówkowe i dokumentacja do Mesy.

%package static
Summary:	Mesa static libraries
Summary(pl):	Biblioteki statyczne Mesy
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	OpenGL-static = 1.5
Provides:	OpenGL-GLU-static = 1.3
Obsoletes:	XFree86-OpenGL-static

%description static
The static version of the Mesa libraries.

%description static -l pl
Biblioteki statyczne Mesy.

%package demos
Summary:	Mesa Demos
Summary(pl):	Demonstracje mo¿liwo¶ci bibliotek Mesa
Group:		Development/Libraries
Requires:	OpenGL-devel

%description demos
Demonstration programs for the Mesa libraries.

%description demos -l pl
Programy demonstracyjne dla bibliotek Mesa.

%package dri
Summary:	X.org DRI drivers
Summary(pl):	Sterowniki DRI dla X.org
Group:		Development/Libraries
Requires:	OpenGL

%description dri
X.org DRI drivers.

%description dri -l pl
Sterowniki DRI dla X.org.

%prep
%setup -q -n Mesa-%{version} -b 1

# fix demos
find progs -type f|xargs sed -i -e "s,\.\./images/,%{_examplesdir}/%{name}-%{version}/images/,g"

%build
%ifarch %{ix86}
targ=-x86
%else
targ=""
%endif

%{__make} linux${targ}-static \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	OPT_FLAGS="%{rpmcflags}" \
	XLIB_DIR=%{_libdir} \
	GLW_SOURCES="GLwDrawA.c%{?with_motif: GLwMDrawA.c}" \
	SRC_DIRS="mesa glu glw" \
	PROGRAM_DIRS=
mv -f lib lib-static
%{__make} clean

%{__make} linux-dri${targ} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	MKDEP=makedepend \
	OPT_FLAGS="%{rpmcflags}" \
	XLIB_DIR=%{_libdir} \
	SRC_DIRS="glx/x11 mesa glu glw" \
	PROGRAM_DIRS=
mv -f lib lib-dri
%{__make} clean \
	MKDEP=makedepend

%{__make} linux${targ} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	OPT_FLAGS="%{rpmcflags}" \
	XLIB_DIR=%{_libdir} \
	SRC_DIRS="mesa glu glw" \
	PROGRAM_DIRS=

%{__make} -C progs/xdemos \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	OPT_FLAGS="%{rpmcflags}" \
	XLIB_DIR=%{_libdir} \
	PROGS="glxgears" \
	APP_LIB_DEPS="-L\$(LIB_DIR) -lGL"

%{__make} -C progs/xdemos \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	OPT_FLAGS="%{rpmcflags}" \
	XLIB_DIR=%{_libdir} \
	PROGS="glxinfo" \
	APP_LIB_DEPS="-L\$(LIB_DIR) -lGLU -lGL"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}/GL,%{_examplesdir}/%{name}-%{version}}
install -d $RPM_BUILD_ROOT%{_libdir}/xorg/modules/dri

cp -df lib-static/lib* $RPM_BUILD_ROOT%{_libdir}
cp -df lib-dri/lib* $RPM_BUILD_ROOT%{_libdir}
cp -df lib/libOS* $RPM_BUILD_ROOT%{_libdir}
cp -rf include/GL/{gl[!u]*,glu.h,glu_*,osmesa.h,xmesa*} src/glw/GLw*.h $RPM_BUILD_ROOT%{_includedir}/GL
cp -df lib-dri/*_dri.so $RPM_BUILD_ROOT%{_libdir}/xorg/modules/dri

install progs/xdemos/{glxgears,glxinfo} $RPM_BUILD_ROOT%{_bindir}
for l in demos redbook samples xdemos ; do
	%{__make} -C progs/$l clean
done
for l in demos redbook samples util xdemos images ; do
	cp -Rf progs/$l $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/$l
done
rm -rf $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/*/{.deps,CVS,Makefile.{BeOS*,win,cygnus,DJ,dja}}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc docs/{*.html,README.{3DFX,GGI,MITS,QUAKE,THREADS,X11},RELNOTES*,VERSIONS}
%attr(755,root,root) %{_bindir}/glx*
%attr(755,root,root) %{_libdir}/libGL.so.*.*
%attr(755,root,root) %{_libdir}/libGLU.so.*.*
%attr(755,root,root) %{_libdir}/libGLw.so.*.*
%attr(755,root,root) %{_libdir}/libOSMesa.so.*.*
# symlink for binary apps which fail to conform Linux OpenGL ABI
# (and dlopen libGL.so instead of libGL.so.1)
%attr(755,root,root) %{_libdir}/libGL.so

%files devel
%defattr(644,root,root,755)
%doc docs/*.spec
%attr(755,root,root) %{_libdir}/libGLU.so
%attr(755,root,root) %{_libdir}/libGLw.so
%attr(755,root,root) %{_libdir}/libOSMesa.so
%dir %{_includedir}/GL
%{_includedir}/GL/GLwDrawA.h
%{_includedir}/GL/GLwDrawAP.h
%{_includedir}/GL/GLwMDrawA.h
%{_includedir}/GL/GLwMDrawAP.h
%{_includedir}/GL/gl.h
%{_includedir}/GL/glext.h
%{_includedir}/GL/gl_mangle.h
%{_includedir}/GL/glu.h
%{_includedir}/GL/glu_mangle.h
%{_includedir}/GL/glx.h
%{_includedir}/GL/glxext.h
%{_includedir}/GL/glx_mangle.h
%{_includedir}/GL/osmesa.h
%{_includedir}/GL/xmesa.h
%{_includedir}/GL/xmesa_x.h
%{_includedir}/GL/xmesa_xf86.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libGL.a
%{_libdir}/libGLU.a
%{_libdir}/libGLw.a
%{_libdir}/libOSMesa.a

%files demos
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

%files dri
%defattr(644,root,root,755)
%dir %{_libdir}/xorg/modules/dri
%attr(755,root,root) %{_libdir}/xorg/modules/dri/*_dri.so
