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
Release:	1.1
License:	MIT (core), SGI (GLU,libGLw) and others - see COPYRIGHT file
Group:		X11/Libraries
Source0:	http://dl.sourceforge.net/mesa3d/%{name}Lib-%{version}.tar.bz2
# Source0-md5:	85a84e47a3f718f752f306b9e0954ef6
Source1:	http://dl.sourceforge.net/mesa3d/%{name}Demos-%{version}.tar.bz2
# Source1-md5:	1a8c4d4fc699233f5fdb902b8753099e
URL:		http://www.mesa3d.org/
%{?with_glide:BuildRequires:	Glide3-DRI-devel}
BuildRequires:	expat-devel
BuildRequires:	libdrm-devel >= 1.0.4-1.20051022
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.4d
%{?with_motif:BuildRequires:	motif-devel}
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libXxf86vm-devel
BuildRequires:	xorg-proto-glproto-devel
BuildRequires:	xorg-util-makedepend
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

%package libGL
Summary:	Free Mesa3D implementation of libGL OpenGL library
Summary(pl):	Wolnodostêpna implementacja Mesa3D biblioteki libGL ze standardu OpenGL
License:	MIT
Group:		X11/Libraries
%{?with_glide:Requires:	Glide3-DRI}
Provides:	OpenGL = 1.5
# reports version 1.3, but supports glXGetProcAddress() from 1.4
Provides:	OpenGL-GLX = 1.4
Obsoletes:	XFree86-OpenGL-libGL

%description libGL
Mesa is a 3-D graphics library with an API which is very similar to
that of OpenGL(R). To the extent that Mesa utilizes the OpenGL command
syntax or state machine, it is being used with authorization from
Silicon Graphics, Inc. However, the author does not possess an OpenGL
license from SGI, and makes no claim that Mesa is in any way a
compatible replacement for OpenGL or associated with SGI.

This package contains libGL which implements OpenGL 1.5 and GLX 1.4
specifications. It uses DRI for rendering.

%description libGL -l pl
Mesa jest bibliotek± grafiki 3D z API bardzo podobnym do OpenGL(R). Do
tego stopnia, ¿e Mesa u¿ywa sk³adni i automatu OpenGL jest u¿ywana z
autoryzacj± Silicon Graphics, Inc. Jednak autor nie posiada licencji
OpenGL od SGI i nie twierdzi, ¿e Mesa jest kompatybilnym zamiennikiem
OpenGL ani powi±zana z SGI.

Ten pakiet zawiera libGL implementuj±c± specyfikacje OpenGL 1.5 oraz
GLX 1.4. U¿ywa DRI do renderowania.

%package libGL-devel
Summary:	Header files for Mesa3D libGL library
Summary(pl):	Pliki nag³ówkowe biblioteki libGL z projektu Mesa3D
License:	MIT
Group:		X11/Development/Libraries
# loose dependency on libGL to use with other libGL binaries
Requires:	OpenGL >= 1.5
Requires:	xorg-lib-libX11-devel
Provides:	OpenGL-devel = 1.5
Provides:	OpenGL-GLX-devel = 1.4
Obsoletes:	Mesa-devel
Obsoletes:	XFree86-OpenGL-devel
Obsoletes:	XFree86-OpenGL-devel-base

%description libGL-devel
Header files for Mesa3D libGL library.

%description libGL-devel -l pl
Pliki nag³ówkowe biblioteki libGL z projektu Mesa3D.

%package libGL-static
Summary:	Static Mesa3D libGL library
Summary(pl):	Statyczna biblioteka libGL z projektu Mesa3D
License:	MIT
Group:		X11/Development/Libraries
Requires:	%{name}-libGL-devel = %{version}-%{release}
Provides:	OpenGL-static = 1.5
Obsoletes:	Mesa-static

%description libGL-static
Static Mesa3D libGL library. It uses software renderer.

%description libGL-static -l pl
Statyczna biblioteka libGL z projektu Mesa3D. U¿ywa programowego
renderingu.

%package libGLU
Summary:	SGI implementation of libGLU OpenGL library
Summary(pl):	Implementacja SGI biblioteki libGLU ze standardu OpenGL
License:	SGI Free Software License B v1.1
Group:		Libraries
# loose dependency on libGL.so.1 to use with other libGL binaries
Requires:	OpenGL >= 1.2
Provides:	OpenGL-GLU = 1.3
Obsoletes:	Mesa-devel
Obsoletes:	XFree86-OpenGL-libs

%description libGLU
SGI implementation of libGLU OpenGL library. It implements OpenGL GLU
1.3 specifications.

%description libGLU -l pl
Implementacja SGI biblioteki libGLU ze standardu OpenGL. Implementuje
specyfikacjê OpenGL GLU 1.3.

%package libGLU-devel
Summary:	Header files for SGI libGLU library
Summary(pl):	Pliki nag³ówkowe biblioteki SGI libGLU
License:	SGI Free Software License B v1.1
Group:		Development/Libraries
Requires:	%{name}-libGLU = %{version}-%{release}
Requires:	OpenGL-devel >= 1.2
Requires:	libstdc++-devel
Provides:	OpenGL-GLU-devel = 1.3

%description libGLU-devel
Header files for SGI libGLU library.

%description libGLU-devel -l pl
Pliki nag³ówkowe biblioteki SGI libGLU.

%package libGLU-static
Summary:	Static SGI libGLU library
Summary(pl):	Statyczna biblioteka SGI libGLU
License:	SGI Free Software License B v1.1
Group:		Development/Libraries
Requires:	%{name}-libGLU-devel = %{version}-%{release}
Provides:	OpenGL-GLU-static = 1.3

%description libGLU-static
Static SGI libGLU library.

%description libGLU-static -l pl
Statyczna biblioteka SGI libGLU.

%package libGLw
Summary:	SGI OpenGL Xt widgets library
Summary(pl):	Biblioteka SGI widgetów Xt dla OpenGL-a
License:	SGI MIT-like
Group:		Libraries
# loose dependency on libGL.so.1 to use with other libGL binaries
Requires:	OpenGL >= 1.1
Provides:	OpenGL-GLw

%description libGLw
SGI OpenGL Xt widgets library.

%description libGLU -l pl
Biblioteka SGI widgetów Xt dla OpenGL-a.

%package libGLw-devel
Summary:	Header files for SGI libGLw library
Summary(pl):	Pliki nag³ówkowe biblioteki SGI libGLw
License:	SGI Free Software License B v1.1
Group:		Development/Libraries
Requires:	%{name}-libGLw = %{version}-%{release}
Requires:	OpenGL-devel >= 1.2
Provides:	OpenGL-GLw-devel

%description libGLw-devel
Header files for SGI libGLw library.

%description libGLw-devel -l pl
Pliki nag³ówkowe biblioteki SGI libGLw.

%package libGLw-static
Summary:	Static SGI libGLw library
Summary(pl):	Statyczna biblioteka SGI libGLw
License:	SGI Free Software License B v1.1
Group:		Development/Libraries
Requires:	%{name}-libGLw-devel = %{version}-%{release}
Provides:	OpenGL-GLw-static

%description libGLw-static
Static SGI libGLw library.

%description libGLw-static -l pl
Statyczna biblioteka SGI libGLw.

%package utils
Summary:	OpenGL utilities from Mesa3D
Summary(pl):	Programy narzêdziowe OpenGL z projektu Mesa3D
Group:		X11/Applications/Graphisc
# loose deps on libGL/libGLU

%description utils
OpenGL utilities from Mesa3D: glxgears and glxinfo.

%description utils -l pl
Programy narzêdziowe OpenGL z projektu Mesa3D: glxgears i glxinfo.

%package demos
Summary:	Mesa Demos
Summary(pl):	Programy demonstruj±ce mo¿liwo¶ci bibliotek Mesa
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
Requires:	xorg-xserver-server

%description dri
X.org DRI drivers.

%description dri -l pl
Sterowniki DRI dla X.org.

#%package dri-driver-ffb ...

%prep
%setup -q -n Mesa-%{version} -b 1

# fix demos
find progs -type f|xargs sed -i -e "s,\.\./images/,%{_examplesdir}/%{name}-%{version}/images/,g"

%ifnarch sparc sparcv9 sparc64
# for sunffb driver - useful on sparc only
sed -i -e 's/ ffb$//' configs/linux-dri
%endif

%build
%ifarch %{ix86}
targ=-x86
%else
targ=""
%endif

%{__make} linux${targ}-static \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	OPT_FLAGS="%{rpmcflags} -fno-strict-aliasing" \
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
	OPT_FLAGS="%{rpmcflags} -fno-strict-aliasing" \
	XLIB_DIR=%{_libdir} \
	SRC_DIRS="glx/x11 mesa glu glw" \
	PROGRAM_DIRS=
mv -f lib lib-dri
%{__make} clean \
	MKDEP=makedepend

%{__make} linux${targ} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	OPT_FLAGS="%{rpmcflags} -fno-strict-aliasing" \
	XLIB_DIR=%{_libdir} \
	SRC_DIRS="mesa" \
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
cp -df lib/libOSMesa* $RPM_BUILD_ROOT%{_libdir}
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

%post	libGL -p /sbin/ldconfig
%postun	libGL -p /sbin/ldconfig

%post	libGLU -p /sbin/ldconfig
%postun	libGLU -p /sbin/ldconfig

%post	libGLw -p /sbin/ldconfig
%postun	libGLw -p /sbin/ldconfig

%files libGL
%defattr(644,root,root,755)
%doc docs/{*.html,README.{3DFX,GGI,MITS,QUAKE,THREADS,X11},RELNOTES*,VERSIONS}
%attr(755,root,root) %{_libdir}/libGL.so.*.*
%attr(755,root,root) %{_libdir}/libOSMesa.so.*.*
# symlink for binary apps which fail to conform Linux OpenGL ABI
# (and dlopen libGL.so instead of libGL.so.1)
%attr(755,root,root) %{_libdir}/libGL.so

%files libGL-devel
%defattr(644,root,root,755)
%doc docs/*.spec
%attr(755,root,root) %{_libdir}/libOSMesa.so
%dir %{_includedir}/GL
%{_includedir}/GL/gl.h
%{_includedir}/GL/glext.h
%{_includedir}/GL/gl_mangle.h
%{_includedir}/GL/glx.h
%{_includedir}/GL/glxext.h
%{_includedir}/GL/glx_mangle.h
%{_includedir}/GL/osmesa.h
%{_includedir}/GL/xmesa.h
%{_includedir}/GL/xmesa_x.h
%{_includedir}/GL/xmesa_xf86.h

%files libGL-static
%defattr(644,root,root,755)
%{_libdir}/libGL.a
%{_libdir}/libOSMesa.a

%files libGLU
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libGLU.so.*.*

%files libGLU-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libGLU.so
%{_includedir}/GL/glu.h
%{_includedir}/GL/glu_mangle.h

%files libGLU-static
%defattr(644,root,root,755)
%{_libdir}/libGLU.a

%files libGLw
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libGLw.so.*.*

%files libGLw-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libGLw.so
%{_includedir}/GL/GLwDrawA.h
%{_includedir}/GL/GLwDrawAP.h
%{_includedir}/GL/GLwMDrawA.h
%{_includedir}/GL/GLwMDrawAP.h

%files libGLw-static
%defattr(644,root,root,755)
%{_libdir}/libGLw.a

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/glxgears
%attr(755,root,root) %{_bindir}/glxinfo

%files dri
%defattr(644,root,root,755)
%dir %{_libdir}/xorg/modules/dri
# XXX: split
%ifarch sparc sparcv9 sparc64
# sunffb (sparc only)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/ffb_dri.so
%endif
# i810
%attr(755,root,root) %{_libdir}/xorg/modules/dri/i810_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/i830_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/i915_dri.so
# ati
%attr(755,root,root) %{_libdir}/xorg/modules/dri/mach64_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/r128_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/r200_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/r300_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/radeon_dri.so
# glint (requires update)
#%attr(755,root,root) %{_libdir}/xorg/modules/dri/gamma_dri.so
# mga
%attr(755,root,root) %{_libdir}/xorg/modules/dri/mga_dri.so
# s3virge (but driver not ready?)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/s3v_dri.so
# savage
%attr(755,root,root) %{_libdir}/xorg/modules/dri/savage_dri.so
# sis
%attr(755,root,root) %{_libdir}/xorg/modules/dri/sis_dri.so
# tdfx
%attr(755,root,root) %{_libdir}/xorg/modules/dri/tdfx_dri.so
# trident
%attr(755,root,root) %{_libdir}/xorg/modules/dri/trident_dri.so
# via
%attr(755,root,root) %{_libdir}/xorg/modules/dri/unichrome_dri.so

%files demos
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
