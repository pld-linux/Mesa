#
# TODO:
# - subpackage with non-dri libGL for use with X-servers with missing GLX extension?
# - package OpenGL man pages (from monolith or SGI) somewhere
#
# Conditional build:
%bcond_with	glide	# with GLIDE (broken now)
%bcond_without	motif	# build static libGLw without Motif interface
#
Summary:	Free OpenGL implementation
Summary(pl):	Wolnodostêpna implementacja standardu OpenGL
Name:		Mesa
Version:	6.5
%define	snap	20060701
Release:	1.%{snap}.1
License:	MIT (core), SGI (GLU,libGLw) and others - see COPYRIGHT file
Group:		X11/Libraries
Source0:	%{name}-%{snap}.tar.gz
# Source0-md5:	f0ac5dadac7ecba3672c2906f79dd62f
#Source0:	http://dl.sourceforge.net/mesa3d/%{name}Lib-%{version}.tar.bz2
#Source1:	http://dl.sourceforge.net/mesa3d/%{name}Demos-%{version}.tar.bz2
Patch0:		%{name}-modules_dir.patch
URL:		http://www.mesa3d.org/
%{?with_glide:BuildRequires:	Glide3-DRI-devel}
BuildRequires:	expat-devel
BuildRequires:	libdrm-devel >= 2.0.2
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.4d
%{?with_motif:BuildRequires:	motif-devel}
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
BuildRequires:	xorg-proto-glproto-devel
BuildRequires:	xorg-util-makedepend
Obsoletes:	Mesa-dri
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
Obsoletes:	Mesa
Obsoletes:	X11-OpenGL-libGL
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
Obsoletes:	X11-OpenGL-devel
Obsoletes:	X11-OpenGL-devel-base
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
Obsoletes:	X11-OpenGL-static
Obsoletes:	XFree86-OpenGL-static

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
Obsoletes:	X11-OpenGL-libs
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
Group:		X11/Applications/Graphics
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

%package dri-driver-ati-mach64
Summary:	X.org DRI drivers
Summary(pl):	Sterowniki DRI dla X.org
Group:		X11/Libraries
Requires:	xorg-xserver-server

%description dri-driver-ati-mach64
X.org DRI drivers for ATI mach64 card family.

%description dri-driver-ati-mach64 -l pl
Sterowniki X.org DRI dla rodziny kart ATI mach64.

%package dri-driver-ati-radeon-R100
Summary:	X.org DRI drivers
Summary(pl):	Sterowniki DRI dla X.org
Group:		X11/Libraries
Requires:	xorg-xserver-server

%description dri-driver-ati-radeon-R100
X.org DRI drivers for ATI R100 card family (Radeon 7000-7500).

%description dri-driver-ati-radeon-R100 -l pl
Sterowniki X.org DRI dla rodziny kart ATI R100 (Radeon 7000-7500).

%package dri-driver-ati-radeon-R200
Summary:	X.org DRI drivers
Summary(pl):	Sterowniki DRI dla X.org
Group:		X11/Libraries
Requires:	xorg-xserver-server

%description dri-driver-ati-radeon-R200
X.org DRI drivers for ATI R200 card family (Radeon 8500-92xx)

%description dri-driver-ati-radeon-R200 -l pl
Sterowniki X.org DRI dla rodziny kart ATI R200 (Radeon 8500-92xx).

%package dri-driver-ati-radeon-R300
Summary:	X.org DRI drivers
Summary(pl):	Sterowniki DRI dla X.org
Group:		X11/Libraries
Requires:	xorg-xserver-server

%description dri-driver-ati-radeon-R300
X.org DRI drivers for ATI R300 card family.

%description dri-driver-ati-radeon-R300 -l pl
Sterowniki X.org DRI dla rodziny kart ATI R300.

%package dri-driver-ati-rage128
Summary:	X.org DRI drivers
Summary(pl):	Sterowniki DRI dla X.org
Group:		X11/Libraries
Requires:	xorg-xserver-server

%description dri-driver-ati-rage128
X.org DRI drivers for ATI rage128 card family.

%description dri-driver-ati-rage128 -l pl
Sterowniki X.org DRI dla rodziny kart ATI rage128.

%package dri-driver-ffb
Summary:	X.org DRI drivers
Summary(pl):	Sterowniki DRI dla X.org
Group:		X11/Libraries
Requires:	xorg-xserver-server

%description dri-driver-ffb
X.org DRI drivers for SUN Creator3D and Elite3D card family.

%description dri-driver-ffb -l pl
Sterowniki X.org DRI dla rodziny kart SUN Creator3D and Elite3D.

%package dri-driver-glint
Summary:	X.org DRI drivers
Summary(pl):	Sterowniki DRI dla X.org
Group:		X11/Libraries
Requires:	xorg-xserver-server

%description dri-driver-glint
X.org DRI drivers for GLINT/Permedia card family.

%description dri-driver-glint -l pl
Sterowniki X.org DRI dla rodziny kart GLINT/Permedia.

%package dri-driver-intel-i810
Summary:	X.org DRI drivers
Summary(pl):	Sterowniki DRI dla X.org
Group:		X11/Libraries
Requires:	xorg-xserver-server

%description dri-driver-intel-i810
X.org DRI drivers for Intel i810 card family.

%description dri-driver-intel-i810 -l pl
Sterowniki X.org DRI dla rodziny kart i810.

%package dri-driver-intel-i830
Summary:	X.org DRI drivers
Summary(pl):	Sterowniki DRI dla X.org
Group:		X11/Libraries
Requires:	xorg-xserver-server

%description dri-driver-intel-i830
X.org DRI drivers for Intel i830 card family.

%description dri-driver-intel-i830 -l pl
Sterowniki X.org DRI dla rodziny kart i830.

%package dri-driver-intel-i915
Summary:	X.org DRI drivers
Summary(pl):	Sterowniki DRI dla X.org
Group:		X11/Libraries
Requires:	xorg-xserver-server
Obsoletes:	Mesa-dri-driver-intel-i830

%description dri-driver-intel-i915
X.org DRI drivers for Intel i915 card family.

%description dri-driver-intel-i915 -l pl
Sterowniki X.org DRI dla rodziny kart i915.

%package dri-driver-matrox
Summary:	X.org DRI drivers
Summary(pl):	Sterowniki DRI dla X.org
Group:		X11/Libraries
Requires:	xorg-xserver-server

%description dri-driver-matrox
X.org DRI drivers for Matrox G card family.

%description dri-driver-matrox -l pl
Sterowniki X.org DRI dla rodziny kart Matrox G.

%package dri-driver-s3virge
Summary:	X.org DRI drivers
Summary(pl):	Sterowniki DRI dla X.org
Group:		X11/Libraries
Requires:	xorg-xserver-server

%description dri-driver-s3virge
X.org DRI drivers for S3 Virge card family.

%description dri-driver-s3virge -l pl
Sterowniki X.org DRI dla rodziny kart S3 Virge.

%package dri-driver-savage
Summary:	X.org DRI drivers
Summary(pl):	Sterowniki DRI dla X.org
Group:		X11/Libraries
Requires:	xorg-xserver-server

%description dri-driver-savage
X.org DRI drivers for S3 Savage card family.

%description dri-driver-savage -l pl
Sterowniki X.org DRI dla rodziny kart S3 Savage.

%package dri-driver-sis
Summary:	X.org DRI drivers
Summary(pl):	Sterowniki DRI dla X.org
Group:		X11/Libraries
Requires:	xorg-xserver-server

%description dri-driver-sis
X.org DRI drivers for SiS card family.

%description dri-driver-sis -l pl
Sterowniki X.org DRI dla rodziny kart SiS.

%package dri-driver-tdfx
Summary:	X.org DRI drivers
Summary(pl):	Sterowniki DRI dla X.org
Group:		X11/Libraries
Requires:	xorg-xserver-server

%description dri-driver-tdfx
X.org DRI drivers for 3DFX Voodoo card family (Voodoo 3,4,5, Banshee
and Velocity 100/200).

%description dri-driver-tdfx -l pl
Sterowniki X.org DRI dla rodziny kart 3DFX Voodoo. (Voodoo 3,4,5,
Banshee and Velocity 100/200).

%package dri-driver-trident
Summary:	X.org DRI drivers
Summary(pl):	Sterowniki DRI dla X.org
Group:		X11/Libraries
Requires:	xorg-xserver-server

%description dri-driver-trident
X.org DRI drivers for Trident card family.

%description dri-driver-trident -l pl
Sterowniki X.org DRI dla rodziny kart Trident.

%package dri-driver-via-unichrome
Summary:	X.org DRI drivers
Summary(pl):	Sterowniki DRI dla X.org
Group:		X11/Libraries
Requires:	xorg-xserver-server

%description dri-driver-via-unichrome
X.org DRI drivers for VIA Unichrome card family.

%description dri-driver-via-unichrome -l pl
Sterowniki X.org DRI dla rodziny kart VIA Unichrome.

%prep
%setup -q -n Mesa
#setup -q -n Mesa-%{version} -b 1
%patch0 -p1

# fix dri path
sed -i -e 's#/usr/lib/xorg/modules/dri#%{_libdir}/xorg/modules/dri#g' src/glx/x11/dri_glx.c

# fix demos
find progs -type f|xargs sed -i -e "s,\.\./images/,%{_examplesdir}/%{name}-%{version}/images/,g"

%ifnarch sparc sparcv9 sparc64
# for sunffb driver - useful on sparc only
sed -i -e 's/ ffb$//' configs/linux-dri
%endif

%ifnarch %{ix86} %{x8664}
# sis needs write-memory barrier
sed -i -e 's/ sis / /' configs/linux-dri
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
	APP_LIB_DEPS="-L\$(LIB_DIR) -lGL -L../../lib-dri -lGLU"

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

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}/GL,%{_examplesdir}/%{name}-%{version}}
install -d $RPM_BUILD_ROOT%{_libdir}/xorg/modules/dri

cp -df lib-static/lib* $RPM_BUILD_ROOT%{_libdir}
cp -df lib-dri/lib* $RPM_BUILD_ROOT%{_libdir}
cp -df lib/libOSMesa* $RPM_BUILD_ROOT%{_libdir}
cp -rf include/GL/{gl[!u]*,glu.h,glu_*,osmesa.h,xmesa*} src/glw/GLw*.h $RPM_BUILD_ROOT%{_includedir}/GL
cp -df lib-dri/*_dri.so $RPM_BUILD_ROOT%{_libdir}/xorg/modules/dri

# keep for -bi --short-circuit
cp -a progs progs.org
install progs/xdemos/{glxgears,glxinfo} $RPM_BUILD_ROOT%{_bindir}
for l in demos redbook samples xdemos ; do
	%{__make} -C progs/$l clean
done
for l in demos redbook samples util xdemos images ; do
	cp -Rf progs/$l $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/$l
done
rm -rf progs && mv -f progs.org progs
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
%doc docs/{*.html,README.{3DFX,GGI,MITS,QUAKE,THREADS},RELNOTES*,VERSIONS}
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
%{_includedir}/GL/glfbdev.h
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

%files dri-driver-ati-mach64
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/mach64_dri.so

%files dri-driver-ati-radeon-R100
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/radeon_dri.so

%files dri-driver-ati-radeon-R200
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/r200_dri.so

%files dri-driver-ati-radeon-R300
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/r300_dri.so

%files dri-driver-ati-rage128
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/r128_dri.so

# sunffb (sparc only)
%ifarch sparc sparcv9 sparc64
%files dri-driver-ffb
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/ffb_dri.so
%endif

# glint (requires update)
%if 0
%files dri-driver-glint
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/gamma_dri.so
%endif

%files dri-driver-intel-i810
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/i810_dri.so

%if 0
%files dri-driver-intel-i830
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/i830_dri.so
%endif

%files dri-driver-intel-i915
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/i915_dri.so

%files dri-driver-matrox
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/mga_dri.so

%files dri-driver-s3virge
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/s3v_dri.so

%files dri-driver-savage
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/savage_dri.so

%ifarch %{ix86} %{x8664}
%files dri-driver-sis
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/sis_dri.so
%endif

%files dri-driver-tdfx
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/tdfx_dri.so

%files dri-driver-trident
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/trident_dri.so

%files dri-driver-via-unichrome
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/unichrome_dri.so

%files demos
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
