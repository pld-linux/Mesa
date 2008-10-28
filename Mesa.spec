#
# TODO:
# - subpackage with non-dri libGL for use with X-servers with missing GLX extension?
#
# Conditional build:
%bcond_without	motif	# build static libGLw without Motif interface
%bcond_with	multigl	# package libGL in a way allowing concurrent install with nvidia/fglrx drivers
%bcond_with	ttm	# enable TTM API
#
# minimal supported xserver version
%define		xserver_ver	1.5.0
# glapi version (glapi tables in dri drivers and libglx must be in sync);
# set to current Mesa version on ABI break, when xserver tables get regenerated
# (until they start to be somehow versioned themselves)
%define		glapi_ver	7.1.0
Summary:	Free OpenGL implementation
Summary(pl.UTF-8):	Wolnodostępna implementacja standardu OpenGL
Name:		Mesa
Version:	7.2
Release:	2%{?with_multigl:.mgl}
License:	MIT (core), SGI (GLU,libGLw) and others - see license.html file
Group:		X11/Libraries
Source0:	http://dl.sourceforge.net/mesa3d/%{name}Lib-%{version}.tar.bz2
# Source0-md5:	04d379292e023df0b0266825cb0dbde5
Source1:	http://dl.sourceforge.net/mesa3d/%{name}Demos-%{version}.tar.bz2
# Source1-md5:	22e03dc4038cd63f32c21eb60994892b
Patch0:		%{name}-realclean.patch
Patch1:		%{name}-dri_mm.patch
URL:		http://www.mesa3d.org/
BuildRequires:	expat-devel
BuildRequires:	libdrm-devel >= 2.3.1
%{?with_ttm:BuildRequires:	libdrm-devel >= 2.4.0}
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.4d
%{?with_motif:BuildRequires:	motif-devel}
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libXdamage-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
BuildRequires:	xorg-proto-dri2proto-devel
BuildRequires:	xorg-proto-glproto-devel
BuildRequires:	xorg-proto-printproto-devel
BuildRequires:	xorg-util-makedepend
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mesa is a 3-D graphics library with an API which is very similar to
that of OpenGL(R). To the extent that Mesa utilizes the OpenGL command
syntax or state machine, it is being used with authorization from
Silicon Graphics, Inc. However, the author does not possess an OpenGL
license from SGI, and makes no claim that Mesa is in any way a
compatible replacement for OpenGL or associated with SGI.

%description -l pl.UTF-8
Mesa jest biblioteką grafiki 3D z API bardzo podobnym do OpenGL(R). Do
tego stopnia, że Mesa używa składni i automatu OpenGL jest używana z
autoryzacją Silicon Graphics, Inc. Jednak autor nie posiada licencji
OpenGL od SGI i nie twierdzi, że Mesa jest kompatybilnym zamiennikiem
OpenGL ani powiązana z SGI.

%package libGL
Summary:	Free Mesa3D implementation of libGL OpenGL library
Summary(pl.UTF-8):	Wolnodostępna implementacja Mesa3D biblioteki libGL ze standardu OpenGL
License:	MIT
Group:		X11/Libraries
Requires:	libdrm >= 2.2.0
Provides:	OpenGL = 2.1
# reports version 1.3, but supports glXGetProcAddress() from 1.4
Provides:	OpenGL-GLX = 1.4
Obsoletes:	Mesa
Obsoletes:	Mesa-dri
Obsoletes:	X11-OpenGL-libGL < 1:7.0.0
Obsoletes:	XFree86-OpenGL-libGL < 1:7.0.0

%description libGL
Mesa is a 3-D graphics library with an API which is very similar to
that of OpenGL(R). To the extent that Mesa utilizes the OpenGL command
syntax or state machine, it is being used with authorization from
Silicon Graphics, Inc. However, the author does not possess an OpenGL
license from SGI, and makes no claim that Mesa is in any way a
compatible replacement for OpenGL or associated with SGI.

This package contains libGL which implements OpenGL 1.5 and GLX 1.4
specifications. It uses DRI for rendering.

%description libGL -l pl.UTF-8
Mesa jest biblioteką grafiki 3D z API bardzo podobnym do OpenGL(R). Do
tego stopnia, że Mesa używa składni i automatu OpenGL jest używana z
autoryzacją Silicon Graphics, Inc. Jednak autor nie posiada licencji
OpenGL od SGI i nie twierdzi, że Mesa jest kompatybilnym zamiennikiem
OpenGL ani powiązana z SGI.

Ten pakiet zawiera libGL implementującą specyfikacje OpenGL 1.5 oraz
GLX 1.4. Używa DRI do renderowania.

%package libGL-devel
Summary:	Header files for Mesa3D libGL library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libGL z projektu Mesa3D
License:	MIT
Group:		X11/Development/Libraries
# loose dependency on libGL to use with other libGL binaries
Requires:	OpenGL >= 1.5
Requires:	xorg-lib-libX11-devel
Provides:	OpenGL-devel = 2.1
Provides:	OpenGL-GLX-devel = 1.4
Obsoletes:	Mesa-devel
Obsoletes:	X11-OpenGL-devel < 1:7.0.0
Obsoletes:	X11-OpenGL-devel-base < 1:7.0.0
Obsoletes:	XFree86-OpenGL-devel < 1:7.0.0
Obsoletes:	XFree86-OpenGL-devel-base < 1:7.0.0

%description libGL-devel
Header files for Mesa3D libGL library.

%description libGL-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libGL z projektu Mesa3D.

%package libGL-static
Summary:	Static Mesa3D libGL library
Summary(pl.UTF-8):	Statyczna biblioteka libGL z projektu Mesa3D
License:	MIT
Group:		X11/Development/Libraries
Requires:	%{name}-libGL-devel = %{version}-%{release}
Provides:	OpenGL-static = 2.1
Obsoletes:	Mesa-static
Obsoletes:	X11-OpenGL-static < 1:7.0.0
Obsoletes:	XFree86-OpenGL-static < 1:7.0.0

%description libGL-static
Static Mesa3D libGL library. It uses software renderer.

%description libGL-static -l pl.UTF-8
Statyczna biblioteka libGL z projektu Mesa3D. Używa programowego
renderingu.

%package libGLU
Summary:	SGI implementation of libGLU OpenGL library
Summary(pl.UTF-8):	Implementacja SGI biblioteki libGLU ze standardu OpenGL
License:	SGI Free Software License B v2.0 (MIT-like)
Group:		Libraries
# loose dependency on libGL.so.1 to use with other libGL binaries
Requires:	OpenGL >= 1.2
Provides:	OpenGL-GLU = 1.3
Obsoletes:	Mesa-devel
Obsoletes:	X11-OpenGL-libs < 1:7.0.0
Obsoletes:	XFree86-OpenGL-libs < 1:7.0.0

%description libGLU
SGI implementation of libGLU OpenGL library. It implements OpenGL GLU
1.3 specifications.

%description libGLU -l pl.UTF-8
Implementacja SGI biblioteki libGLU ze standardu OpenGL. Implementuje
specyfikację OpenGL GLU 1.3.

%package libGLU-devel
Summary:	Header files for SGI libGLU library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki SGI libGLU
License:	SGI Free Software License B v2.0 (MIT-like)
Group:		Development/Libraries
Requires:	%{name}-libGLU = %{version}-%{release}
Requires:	OpenGL-devel >= 1.2
Requires:	libstdc++-devel
Provides:	OpenGL-GLU-devel = 1.3

%description libGLU-devel
Header files for SGI libGLU library.

%description libGLU-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki SGI libGLU.

%package libGLU-static
Summary:	Static SGI libGLU library
Summary(pl.UTF-8):	Statyczna biblioteka SGI libGLU
License:	SGI Free Software License B v2.0 (MIT-like)
Group:		Development/Libraries
Requires:	%{name}-libGLU-devel = %{version}-%{release}
Provides:	OpenGL-GLU-static = 1.3

%description libGLU-static
Static SGI libGLU library.

%description libGLU-static -l pl.UTF-8
Statyczna biblioteka SGI libGLU.

%package libGLw
Summary:	SGI OpenGL Xt widgets library
Summary(pl.UTF-8):	Biblioteka SGI widgetów Xt dla OpenGL-a
License:	SGI MIT-like
Group:		Libraries
# loose dependency on libGL.so.1 to use with other libGL binaries
Requires:	OpenGL >= 1.1
Provides:	OpenGL-GLw

%description libGLw
SGI OpenGL Xt widgets library.

%description libGLU -l pl.UTF-8
Biblioteka SGI widgetów Xt dla OpenGL-a.

%package libGLw-devel
Summary:	Header files for SGI libGLw library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki SGI libGLw
License:	SGI MIT-like
Group:		Development/Libraries
Requires:	%{name}-libGLw = %{version}-%{release}
Requires:	OpenGL-devel >= 1.2
Provides:	OpenGL-GLw-devel

%description libGLw-devel
Header files for SGI libGLw library.

%description libGLw-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki SGI libGLw.

%package libGLw-static
Summary:	Static SGI libGLw library
Summary(pl.UTF-8):	Statyczna biblioteka SGI libGLw
License:	SGI MIT-like
Group:		Development/Libraries
Requires:	%{name}-libGLw-devel = %{version}-%{release}
Provides:	OpenGL-GLw-static

%description libGLw-static
Static SGI libGLw library.

%description libGLw-static -l pl.UTF-8
Statyczna biblioteka SGI libGLw.

%package libOSMesa
Summary:	OSMesa (off-screen renderer) library
Summary(pl.UTF-8):	Biblioteka OSMesa (renderująca bitmapy w pamięci)
License:	MIT
Group:		Libraries
# doesn't require base

%description libOSMesa
OSMesa (off-screen renderer) library.

%description libOSMesa -l pl.UTF-8
Biblioteka OSMesa (renderująca bitmapy w pamięci).

%package libOSMesa-devel
Summary:	Header file for OSMesa (off-screen renderer) library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki OSMesa (renderującej bitmapy w pamięci)
License:	MIT
Group:		Development/Libraries
Requires:	%{name}-libOSMesa = %{version}-%{release}
# for <GL/gl.h> only
Requires:	OpenGL-devel

%description libOSMesa-devel
Header file for OSMesa (off-screen renderer) library.

%description libOSMesa-devel -l pl.UTF-8
Plik nagłówkowy biblioteki OSMesa (renderującej bitmapy w pamięci).

%package libOSMesa-static
Summary:	Static OSMesa (off-screen renderer) library
Summary(pl.UTF-8):	Biblioteka statyczna OSMesa (renderująca bitmapy w pamięci)
License:	MIT
Group:		Development/Libraries
Requires:	%{name}-libOSMesa-devel = %{version}-%{release}
# this static build of OSMesa needs static non-dri Mesa implementation
Requires:	%{name}-libGL-static = %{version}-%{release}

%description libOSMesa-static
Static OSMesa (off-screen renderer) library.

%description libOSMesa-static -l pl.UTF-8
Biblioteka statyczna OSMesa (renderująca bitmapy w pamięci).

%package utils
Summary:	OpenGL utilities from Mesa3D
Summary(pl.UTF-8):	Programy narzędziowe OpenGL z projektu Mesa3D
License:	MIT
Group:		X11/Applications/Graphics
# loose deps on libGL/libGLU

%description utils
OpenGL utilities from Mesa3D: glxgears and glxinfo.

%description utils -l pl.UTF-8
Programy narzędziowe OpenGL z projektu Mesa3D: glxgears i glxinfo.

%package demos
Summary:	Mesa Demos source code
Summary(pl.UTF-8):	Kod źródłowy programów demonstrujących dla bibliotek Mesa
License:	various (MIT, SGI, GPL - see copyright notes in sources)
Group:		Development/Libraries
Requires:	OpenGL-devel

%description demos
Demonstration programs for the Mesa libraries in source code form.

%description demos -l pl.UTF-8
Kod źródłowy programów demonstracyjnych dla bibliotek Mesa.

%package dri-driver-ati-mach64
Summary:	X.org DRI driver for ATI Mach64 card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart ATI Mach64
License:	MIT
Group:		X11/Libraries
Requires:	xorg-driver-video-mach64
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}

%description dri-driver-ati-mach64
X.org DRI driver for ATI Mach64 card family.

%description dri-driver-ati-mach64 -l pl.UTF-8
Sterownik X.org DRI dla rodziny kart ATI Mach64.

%package dri-driver-ati-radeon-R100
Summary:	X.org DRI driver for ATI R100 card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart ATI R100
License:	MIT
Group:		X11/Libraries
Requires:	xorg-driver-video-ati
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}
Obsoletes:	X11-driver-radeon-dri < 1:7.0.0

%description dri-driver-ati-radeon-R100
X.org DRI driver for ATI R100 card family (Radeon 7000-7500).

%description dri-driver-ati-radeon-R100 -l pl.UTF-8
Sterownik X.org DRI dla rodziny kart ATI R100 (Radeon 7000-7500).

%package dri-driver-ati-radeon-R200
Summary:	X.org DRI driver for ATI R200 card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart ATI R200
License:	MIT
Group:		X11/Libraries
Requires:	xorg-driver-video-ati
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}
Obsoletes:	X11-driver-radeon-dri < 1:7.0.0

%description dri-driver-ati-radeon-R200
X.org DRI driver for ATI R200 card family (Radeon 8500-92xx)

%description dri-driver-ati-radeon-R200 -l pl.UTF-8
Sterownik X.org DRI dla rodziny kart ATI R200 (Radeon 8500-92xx).

%package dri-driver-ati-radeon-R300
Summary:	X.org DRI driver for ATI R300 card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart ATI R300
License:	MIT
Group:		X11/Libraries
Requires:	xorg-driver-video-ati
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}
Obsoletes:	X11-driver-radeon-dri < 1:7.0.0

%description dri-driver-ati-radeon-R300
X.org DRI driver for ATI R300 card family.

%description dri-driver-ati-radeon-R300 -l pl.UTF-8
Sterownik X.org DRI dla rodziny kart ATI R300.

%package dri-driver-ati-rage128
Summary:	X.org DRI driver for ATI Rage128 card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart ATI Rage128
License:	MIT
Group:		X11/Libraries
Requires:	xorg-driver-video-r128
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}
Obsoletes:	X11-driver-r128-dri < 1:7.0.0

%description dri-driver-ati-rage128
X.org DRI driver for ATI Rage128 card family.

%description dri-driver-ati-rage128 -l pl.UTF-8
Sterownik X.org DRI dla rodziny kart ATI Rage128.

%package dri-driver-ffb
Summary:	X.org DRI driver for Sun FFB card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart Sun FFB
License:	MIT
Group:		X11/Libraries
Requires:	xorg-driver-video-sunffb
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}

%description dri-driver-ffb
X.org DRI driver for SUN Creator3D and Elite3D card family.

%description dri-driver-ffb -l pl.UTF-8
Sterownik X.org DRI dla rodziny kart SUN Creator3D i Elite3D.

%package dri-driver-glint
Summary:	X.org DRI driver for GLINT/Permedia card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart GLINT/Permedia
License:	MIT
Group:		X11/Libraries
Requires:	xorg-driver-video-glint
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}
Obsoletes:	X11-driver-glint-dri < 1:7.0.0

%description dri-driver-glint
X.org DRI driver for GLINT/Permedia card family.

%description dri-driver-glint -l pl.UTF-8
Sterownik X.org DRI dla rodziny kart GLINT/Permedia.

%package dri-driver-intel-i810
Summary:	X.org DRI driver for Intel i810 card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart Intel i810
License:	MIT
Group:		X11/Libraries
Requires:	xorg-driver-video-intel
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}
Obsoletes:	X11-driver-i810-dri < 1:7.0.0

%description dri-driver-intel-i810
X.org DRI driver for Intel i810 card family.

%description dri-driver-intel-i810 -l pl.UTF-8
Sterownik X.org DRI dla rodziny kart Intel i810.

%package dri-driver-intel-i915
Summary:	X.org DRI driver for Intel i915 card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart Intel i915
License:	MIT
Group:		X11/Libraries
Requires:	xorg-driver-video-intel
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}
Obsoletes:	Mesa-dri-driver-intel-i830
Obsoletes:	X11-driver-i810-dri < 1:7.0.0

%description dri-driver-intel-i915
X.org DRI driver for Intel i915 card family.

%description dri-driver-intel-i915 -l pl.UTF-8
Sterownik X.org DRI dla rodziny kart Intel i915.

%package dri-driver-intel-i965
Summary:	X.org DRI driver for Intel i965 card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart Intel i965
License:	MIT
Group:		X11/Libraries
Requires:	xorg-driver-video-intel
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}
Obsoletes:	Mesa-dri-driver-intel-i830
Obsoletes:	X11-driver-i810-dri < 1:7.0.0

%description dri-driver-intel-i965
X.org DRI driver for Intel i965 card family.

%description dri-driver-intel-i965 -l pl.UTF-8
Sterownik X.org DRI dla rodziny kart Intel i965.

%package dri-driver-matrox
Summary:	X.org DRI driver for Matrox G card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart Matrox G
License:	MIT
Group:		X11/Libraries
Requires:	xorg-driver-video-mga
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}
Obsoletes:	X11-driver-mga-dri < 1:7.0.0

%description dri-driver-matrox
X.org DRI drivers for Matrox G card family.

%description dri-driver-matrox -l pl.UTF-8
Sterowniki X.org DRI dla rodziny kart Matrox G.

%package dri-driver-s3virge
Summary:	X.org DRI driver for S3 Virge card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart S3 Virge
License:	MIT
Group:		X11/Libraries
Requires:	xorg-driver-video-s3virge
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}

%description dri-driver-s3virge
X.org DRI driver for S3 Virge card family.

%description dri-driver-s3virge -l pl.UTF-8
Sterownik X.org DRI dla rodziny kart S3 Virge.

%package dri-driver-savage
Summary:	X.org DRI driver for S3 Savage card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart S3 Savage
License:	MIT
Group:		X11/Libraries
Requires:	xorg-driver-video-savage
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}

%description dri-driver-savage
X.org DRI driver for S3 Savage card family.

%description dri-driver-savage -l pl.UTF-8
Sterownik X.org DRI dla rodziny kart S3 Savage.

%package dri-driver-sis
Summary:	X.org DRI driver for SiS card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart SiS
License:	MIT
Group:		X11/Libraries
Requires:	xorg-driver-video-sis
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}
Obsoletes:	X11-driver-sis-dri < 1:7.0.0

%description dri-driver-sis
X.org DRI driver for SiS card family.

%description dri-driver-sis -l pl.UTF-8
Sterownik X.org DRI dla rodziny kart SiS.

%package dri-driver-swrast
Summary:	X.org DRI software rasterizer driver
Summary(pl.UTF-8):	Sterownik X.org DRI obsługujący rysowanie programowe
License:	MIT
Group:		X11/Libraries
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}

%description dri-driver-swrast
X.org DRI software rasterizer driver.

%description dri-driver-swrast -l pl.UTF-8
Sterownik X.org DRI obsługujący rysowanie programowe.

%package dri-driver-tdfx
Summary:	X.org DRI driver for 3DFX Voodoo card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart 3DFX Voodoo
License:	MIT
Group:		X11/Libraries
Requires:	Glide3-DRI
Requires:	xorg-driver-video-tdfx
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}
Obsoletes:	X11-driver-tdfx-dri < 1:7.0.0

%description dri-driver-tdfx
X.org DRI driver for 3DFX Voodoo card family (Voodoo 3,4,5, Banshee
and Velocity 100/200).

%description dri-driver-tdfx -l pl.UTF-8
Sterownik X.org DRI dla rodziny kart 3DFX Voodoo. (Voodoo 3,4,5,
Banshee i Velocity 100/200).

%package dri-driver-trident
Summary:	X.org DRI driver for Trident card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart Trident
License:	MIT
Group:		X11/Libraries
Requires:	xorg-driver-video-trident
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}

%description dri-driver-trident
X.org DRI drivers for Trident card family.

%description dri-driver-trident -l pl.UTF-8
Sterowniki X.org DRI dla rodziny kart Trident.

%prep
%setup -q -b1
%patch0 -p0
%patch1 -p1

# fix demos
find progs -type f|xargs sed -i -e "s,\.\./images/,%{_examplesdir}/%{name}-%{version}/images/,g"

# s3v, sis, trident missing there - don't override list from linux-dri
sed -i -e '/^DRI_DIRS/d' configs/linux-dri-x86-64

# add swrast driver
sed -i -e 's/ i810 / swrast i810 /' configs/linux-dri

%ifnarch sparc sparcv9 sparc64
# for sunffb driver - useful on sparc only
sed -i -e 's/ ffb\>//' configs/linux-dri
%endif

%ifnarch %{ix86} %{x8664}
# sis needs write-memory barrier
sed -i -e 's/ sis / /' configs/linux-dri
%endif

%build
# use $lib, not %{_lib} as Mesa uses lib64 only for *-x86-64* targets
%ifarch %{x8664}
targ=-x86-64
lib=lib64
%else
lib=lib
%ifarch %{ix86}
targ=-x86
%else
targ=""
%endif
%endif

# required for -bc --short-circuit
%{__make} realclean
# as above - existing directory makes mv move into instead of rename
rm -rf lib-{dri,osmesa,static}

%{__make} linux${targ}-static \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	OPT_FLAGS="%{rpmcppflags} %{rpmcflags} -fno-strict-aliasing" \
	XLIB_DIR=%{_libdir} \
	GLW_SOURCES="GLwDrawA.c%{?with_motif: GLwMDrawA.c}" \
	SRC_DIRS="mesa glu glw" \
	PROGRAM_DIRS=
mv -f ${lib} lib-static
%{__make} realclean

%{__make} linux-osmesa \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcppflags} %{rpmcflags} -fno-strict-aliasing -fPIC" \
	XLIB_DIR=%{_libdir} \
	SRC_DIRS="mesa" \
	PROGRAM_DIRS=
mv -f lib lib-osmesa
%{__make} realclean

%{__make} linux-dri${targ} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	MKDEP=makedepend \
	OPT_FLAGS="%{rpmcppflags} %{rpmcflags} -fno-strict-aliasing %{?with_ttm:-DTTM_API}" \
	XLIB_DIR=%{_libdir} \
	DRI_DRIVER_SEARCH_DIR=%{_libdir}/xorg/modules/dri \
	SRC_DIRS="glx/x11 mesa glu glw" \
	PROGRAM_DIRS=

%{__make} -C progs/xdemos \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	OPT_FLAGS="%{rpmcppflags} %{rpmcflags}" \
	XLIB_DIR=%{_libdir} \
	PROGS="glxgears" \
	APP_LIB_DEPS="-L../../${lib} -lGL"

%{__make} -C progs/xdemos \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	OPT_FLAGS="%{rpmcppflags} %{rpmcflags}" \
	XLIB_DIR=%{_libdir} \
	PROGS="glxinfo" \
	APP_LIB_DEPS="-L../../${lib} -lGL -lGLU"

mv -f ${lib} lib-dri

for d in mesa glu glw ; do
	%{__make} -C src/$d `basename src/$d/*.pc.in .in` \
		INSTALL_DIR=%{_prefix} \
		LIB_DIR=%{_lib}
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}/GL/internal,%{_pkgconfigdir},%{_examplesdir}/%{name}-%{version}}
install -d $RPM_BUILD_ROOT%{_libdir}/xorg/modules/dri

cp -df lib-static/lib* $RPM_BUILD_ROOT%{_libdir}
cp -df lib-osmesa/libOSMesa* $RPM_BUILD_ROOT%{_libdir}
cp -df lib-dri/lib* $RPM_BUILD_ROOT%{_libdir}
cp -rf include/GL/{gl[!f]*,osmesa.h,xmesa*} src/glw/GLw*.h $RPM_BUILD_ROOT%{_includedir}/GL
cp -rf include/GL/internal/dri_interface.h $RPM_BUILD_ROOT%{_includedir}/GL/internal
cp -df lib-dri/*_dri.so $RPM_BUILD_ROOT%{_libdir}/xorg/modules/dri

install src/mesa/gl.pc $RPM_BUILD_ROOT%{_pkgconfigdir}
install src/glu/glu.pc $RPM_BUILD_ROOT%{_pkgconfigdir}
install src/glw/glw.pc $RPM_BUILD_ROOT%{_pkgconfigdir}

install progs/xdemos/{glxgears,glxinfo} $RPM_BUILD_ROOT%{_bindir}
# work on copy to keep -bi --short-circuit working
rm -rf progs-clean
install -d progs-clean
for l in demos glsl osdemos redbook samples xdemos ; do
	cp -a progs/$l progs-clean/$l
	%{__make} -C progs-clean/$l clean
	cp -Rf progs-clean/$l $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/$l
done
rm -rf progs-clean
for l in util images ; do
	cp -Rf progs/$l $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/$l
done
rm -rf $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/*/{.deps,CVS,Makefile.{BeOS*,win,cygnus,DJ,dja}}

%if %{with multigl}
install -d $RPM_BUILD_ROOT{%{_libdir}/Mesa,%{_sysconfdir}/ld.so.conf.d}

mv -f $RPM_BUILD_ROOT%{_libdir}/libGL.so.* $RPM_BUILD_ROOT%{_libdir}/Mesa
ln -sf Mesa/libGL.so.1 $RPM_BUILD_ROOT%{_libdir}/libGL.so

echo %{_libdir}/Mesa >$RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/Mesa.conf
%endif

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
%doc docs/{*.html,README.{3DFX,GGI,MITS,QUAKE,THREADS},RELNOTES*}
%if %{with multigl}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ld.so.conf.d/Mesa.conf
%dir %{_libdir}/Mesa
%attr(755,root,root) %{_libdir}/Mesa/libGL.so.*.*
%attr(755,root,root) %ghost %{_libdir}/Mesa/libGL.so.1
%else
%attr(755,root,root) %{_libdir}/libGL.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libGL.so.1
# symlink for binary apps which fail to conform Linux OpenGL ABI
# (and dlopen libGL.so instead of libGL.so.1)
%attr(755,root,root) %{_libdir}/libGL.so
%endif

%files libGL-devel
%defattr(644,root,root,755)
%doc docs/*.spec
%if %{with multigl}
%attr(755,root,root) %{_libdir}/libGL.so
%endif
%dir %{_includedir}/GL
%{_includedir}/GL/gl.h
%{_includedir}/GL/glext.h
%{_includedir}/GL/gl_mangle.h
%{_includedir}/GL/glx.h
%{_includedir}/GL/glxext.h
%{_includedir}/GL/glx_mangle.h
%dir %{_includedir}/GL/internal
%{_includedir}/GL/internal/dri_interface.h
%{_pkgconfigdir}/gl.pc

%files libGL-static
%defattr(644,root,root,755)
%{_libdir}/libGL.a
# x11 (non-dri) Mesa API
%{_includedir}/GL/xmesa.h
%{_includedir}/GL/xmesa_x.h
%{_includedir}/GL/xmesa_xf86.h

%files libGLU
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libGLU.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libGLU.so.1

%files libGLU-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libGLU.so
%{_includedir}/GL/glu.h
%{_includedir}/GL/glu_mangle.h
%{_pkgconfigdir}/glu.pc

%files libGLU-static
%defattr(644,root,root,755)
%{_libdir}/libGLU.a

%files libGLw
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libGLw.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libGLw.so.1

%files libGLw-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libGLw.so
%{_includedir}/GL/GLwDrawA.h
%{_includedir}/GL/GLwDrawAP.h
%{_includedir}/GL/GLwMDrawA.h
%{_includedir}/GL/GLwMDrawAP.h
%{_pkgconfigdir}/glw.pc

%files libGLw-static
%defattr(644,root,root,755)
%{_libdir}/libGLw.a

%files libOSMesa
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOSMesa.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libOSMesa.so.[0-9]

%files libOSMesa-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOSMesa.so
%{_includedir}/GL/osmesa.h

%files libOSMesa-static
%defattr(644,root,root,755)
%{_libdir}/libOSMesa.a

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

%files dri-driver-intel-i915
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/i915_dri.so

%files dri-driver-intel-i965
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/i965_dri.so

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

%files dri-driver-swrast
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/swrast_dri.so

%files dri-driver-tdfx
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/tdfx_dri.so

%files dri-driver-trident
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/trident_dri.so

%files demos
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
