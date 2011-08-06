#
# TODO:
# - subpackage with non-dri libGL for use with X-servers with missing GLX extension?
# - resurrect static if it's useful
#
# Conditional build:
%bcond_without	egl	# build egl
%bcond_without	gallium	# don't build gallium
%bcond_with	gallium_intel	# gallium i915 driver (but doesn't work with AIGLX)
%bcond_with	gallium_radeon	# gallium radeon driver
%bcond_without	gallium_nouveau	# gallium nouveau driver
%bcond_without	motif	# build static libGLw without Motif interface
%bcond_with	multigl	# package libGL in a way allowing concurrent install with nvidia/fglrx drivers
%bcond_without	osmesa	# don't build osmesa
%bcond_with	static	# static libraries
#
# minimal supported xserver version
%define		xserver_ver	1.5.0
# glapi version (glapi tables in dri drivers and libglx must be in sync);
# set to current Mesa version on ABI break, when xserver tables get regenerated
# (until they start to be somehow versioned themselves)
%define		glapi_ver	7.1.0
#
%define		libdrm_ver	2.4.25
%define		dri2proto_ver	2.6
%define		glproto_ver	1.4.11
#
%define		snap		20110805
#
Summary:	Free OpenGL implementation
Summary(pl.UTF-8):	Wolnodostępna implementacja standardu OpenGL
Name:		Mesa
Version:	7.12
Release:	0.%{snap}.1%{?with_multigl:.mgl}
License:	MIT (core), SGI (GLU,libGLw) and others - see license.html file
Group:		X11/Libraries
Source0:	%{name}Lib-%{snap}.tar.bz2
# Source0-md5:	b454306ccfd7510643e0fe1100b392f8
Patch0:		%{name}-realclean.patch
Patch1:		%{name}-git.patch
Patch2:		%{name}-selinux.patch
URL:		http://www.mesa3d.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	expat-devel
BuildRequires:	libdrm-devel >= %{libdrm_ver}
# drop when 2.4.24 is released
%{?with_nouveau:BuildRequires:	libdrm-devel >= 2.4.24}
BuildRequires:	libselinux-devel
BuildRequires:	libstdc++-devel >= 5:3.3.0
BuildRequires:	libtalloc-devel >= 2:2.0.1
BuildRequires:	libtool >= 2:1.4d
BuildRequires:	llvm-devel >= 2.9
%{?with_motif:BuildRequires:	motif-devel}
BuildRequires:	pixman-devel
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(talloc) >= 2.0.1
BuildRequires:	python
BuildRequires:	python-libxml2
BuildRequires:	python-modules
BuildRequires:	rpmbuild(macros) >= 1.470
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libXdamage-devel
BuildRequires:	xorg-lib-libXext-devel >= 1.0.5
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
BuildRequires:	xorg-proto-dri2proto-devel >= %{dri2proto_ver}
BuildRequires:	xorg-proto-glproto-devel >= %{glproto_ver}
BuildRequires:	xorg-util-makedepend
BuildRequires:	xorg-xserver-server-devel
%if %{with egl}
BuildRequires:	libxcb-devel
BuildRequires:	udev-devel >= 150
%endif
%if %{with gallium}
BuildRequires:	xorg-proto-xextproto-devel >= 7.0.99.1
BuildRequires:	xorg-xserver-server-devel >= 1.6.0
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{without gallium}
%undefine	with_gallium_intel
%undefine	with_gallium_radeon
%endif

# unresolved symbol _glapi_tls_Dispatch
%define		skip_post_check_so	libGLESv1_CM.so.1.* libGLESv2.so.2.*

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

%package libEGL
Summary:	Mesa implementation of EGL Native Platform Graphics Interface library
Summary(pl.UTF-8):	Implementacja Mesa biblioteki interfejsu EGL
License:	MIT
Group:		Libraries
Requires:	OpenGL >= 1.2
Requires:	udev-libs >= 150
Provides:	EGL = 1.4

%description libEGL
This package contains shared libEGL - Mesa implementation of EGL
Native Platform Graphics Interface as specified by Khronos Group:
<http://www.khronos.org/egl/>.

%description libEGL -l pl.UTF-8
Ten pakiet zawiera bibliotekę współdzieloną libEGL - implementację
Mesa standardu EGL Native Platform Graphics Interface (interfejsu
graficznego platformy natywnej) wg specyfikacji Khronos Group:
<http://www.khronos.org/egl/>.

%package libEGL-devel
Summary:	Header files for Mesa implementation of EGL library
Summary(pl.UTF-8):	Pliki nagłówkowe implementacji Mesa biblioteki EGL
License:	MIT
Group:		Development/Libraries
Requires:	%{name}-libEGL = %{version}-%{release}
Requires:	OpenGL-devel >= 1.2
Requires:	libstdc++-devel
Provides:	EGL-devel = 1.4

%description libEGL-devel
Header files for Mesa implementation of EGL library.

%description libEGL-devel -l pl.UTF-8
Pliki nagłówkowe implementacji Mesa biblioteki EGL.

%package libEGL-static
Summary:	Static SGI libEGL library
Summary(pl.UTF-8):	Statyczna biblioteka SGI libEGL
License:	MIT
Group:		Development/Libraries
Requires:	%{name}-libEGL-devel = %{version}-%{release}
Provides:	EGL-static = 1.4

%description libEGL-static
Static Mesa libEGL library.

%description libEGL-static -l pl.UTF-8
Statyczna biblioteka Mesa libEGL.

%package libGLES
Summary:	Mesa libGLES runtime libraries
Group:		Libraries

%description libGLES
Mesa GLES runtime libraries.

%description libGLES -l pl.UTF-8
Biblioteka Mesa GLES.

%package libGLES-devel
Summary:	Header files for libGLES library
Group:		Development/Libraries
Requires:	%{name}-libGLES = %{version}-%{release}

%description libGLES-devel
Header files for libGLES library.

%description libGLES-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libGLES.

%package libGL
Summary:	Free Mesa3D implementation of libGL OpenGL library
Summary(pl.UTF-8):	Wolnodostępna implementacja Mesa3D biblioteki libGL ze standardu OpenGL
License:	MIT
Group:		X11/Libraries
Requires:	libdrm >= %{libdrm_ver}
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
Requires:	libdrm-devel >= %{libdrm_ver}
Requires:	xorg-lib-libX11-devel
Requires:	xorg-lib-libXdamage-devel
Requires:	xorg-lib-libXext-devel
Requires:	xorg-lib-libXxf86vm-devel
Requires:	xorg-proto-dri2proto-devel >= %{dri2proto_ver}
Requires:	xorg-proto-glproto-devel >= %{glproto_ver}
Suggests:	OpenGL-doc-man
Provides:	OpenGL-GLX-devel = 1.4
Provides:	OpenGL-devel = 2.1
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

%description libGLw -l pl.UTF-8
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

%package libOpenVG
Summary:	OpenVG API implementation
Summary(pl.UTF-8):	Implementacja API OpenVG
License:	MIT
Group:		Libraries
# doesn't require base

%description libOpenVG
OpenVG API implementation.

%description libOpenVG -l pl.UTF-8
Implementacja API OpenVG.

%package libOpenVG-devel
Summary:	Header file for libOpenVG library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki libOpenVG
License:	MIT
Group:		Development/Libraries
# for <KHR/khrplatform.h>
Requires:	%{name}-libEGL-devel = %{version}-%{release}
Requires:	%{name}-libOpenVG = %{version}-%{release}

%description libOpenVG-devel
Header file for libOpenVG library.

%description libOpenVG-devel -l pl.UTF-8
Plik nagłówkowy biblioteki libOpenVG.

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

%package dri-driver-ati-radeon-R600
Summary:	X.org DRI driver for ATI R600 card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart ATI R600
License:	MIT
Group:		X11/Libraries
Requires:	radeon-ucode
Requires:	xorg-driver-video-ati
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}

%description dri-driver-ati-radeon-R600
X.org DRI driver for ATI R600 card family.

%description dri-driver-ati-radeon-R600 -l pl.UTF-8
Sterownik X.org DRI dla rodziny kart ATI R600.

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

%package dri-driver-nouveau
Summary:	X.org DRI driver for NVIDIA card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart NVIDIA
License:	MIT
Group:		X11/Libraries
Requires:	xorg-driver-video-nouveau
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}

%description dri-driver-nouveau
X.org DRI drivers for NVIDIA card family.

%description dri-driver-nouveau -l pl.UTF-8
Sterowniki X.org DRI dla rodziny kart NVIDIA.

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

%package dri-driver-via-unichrome
Summary:	X.org DRI driver for VIA Unichrome card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart VIA Unichrome
License:	MIT
Group:		X11/Libraries
Requires:	xorg-driver-video-openchrome
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}

%description dri-driver-via-unichrome
X.org DRI driver for VIA Unichrome card family.

%description dri-driver-via-unichrome -l pl.UTF-8
Sterownik X.org DRI dla rodziny kart VIA Unichrome.

%package dri-driver-vmwgfx
Summary:	X.org DRI driver for VMware
Summary(pl.UTF-8):	Sterownik X.org DRI dla VMware
License:	MIT
Group:		X11/Libraries
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}

%description dri-driver-vmwgfx
X.org DRI driver for VMWare.

%description dri-driver-vmwgfx -l pl.UTF-8
Sterownik X.org DRI dla VMware.

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p1

%build
%{__aclocal}
%{__autoconf}

dri_drivers="i810 mach64 mga r128 r200 radeon \
%if %{without gallium_radeon}
r300 r600 \
%endif
savage \
%if %{without gallium_intel}
i915 i965 \
%endif
%ifarch sparc sparcv9 sparc64
ffb \
%endif
%ifarch %{ix86} %{x8664}
sis \
%endif
swrast tdfx unichrome"

dri_drivers=$(echo $dri_drivers | xargs | tr ' ' ',')

gallium_drivers="svga swrast \
%if %{with gallium_intel}
i915 \
i965 \
%endif
%if %{with gallium_radeon}
radeon \
r600 \
%endif
%if %{with gallium_nouveau}
nouveau \
%endif
"

gallium_drivers=$(echo $gallium_drivers | xargs | tr ' ' ',')

common_flags="\
	--enable-shared \
	--enable-selinux \
	--enable-pic \
	--enable-glx-tls \
%if %{with egl}
	--enable-egl \
	--enable-gles1 \
	--enable-gles2 \
%endif
"

osmesa_common_flags="\
	--with-driver=osmesa \
	--disable-asm \
	--disable-glu \
	--disable-egl"

%if %{with osmesa}
%configure $common_flags $osmesa_common_flags \
	--with-osmesa-bits=8
%{__make}
mv %{_lib} osmesa8
%{__make} clean
%endif

%configure $common_flags \
%if %{with gallium}
	--enable-openvg \
	--enable-gallium-egl \
	--with-gallium-drivers=${gallium_drivers} \
%else
	--disable-gallium \
%endif
	--with-driver=dri \
	--with-dri-drivers=${dri_drivers} \
	--with-dri-driverdir=%{_libdir}/xorg/modules/dri

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# libs without drivers
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with osmesa}
cp -Pp osmesa*/*OSMesa* $RPM_BUILD_ROOT%{_libdir}
%endif

rm -rf $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/*/{.deps,CVS,Makefile.{BeOS*,win,cygnus,DJ,dja}}

# strip out undesirable headers
olddir=$(pwd)
cd $RPM_BUILD_ROOT%{_includedir}/GL
rm [a-fh-np-wyz]*.h glf*.h
cd $RPM_BUILD_ROOT%{_libdir}
cd $olddir

%if %{with multigl}
install -d $RPM_BUILD_ROOT{%{_libdir}/Mesa,%{_sysconfdir}/ld.so.conf.d}

mv -f $RPM_BUILD_ROOT%{_libdir}/libGL.so.* $RPM_BUILD_ROOT%{_libdir}/Mesa
ln -sf Mesa/libGL.so.1 $RPM_BUILD_ROOT%{_libdir}/libGL.so

echo %{_libdir}/Mesa >$RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/Mesa.conf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	libEGL -p /sbin/ldconfig
%postun	libEGL -p /sbin/ldconfig

%post	libGL -p /sbin/ldconfig
%postun	libGL -p /sbin/ldconfig

%post	libGLES -p /sbin/ldconfig
%postun	libGLES -p /sbin/ldconfig

%post	libGLU -p /sbin/ldconfig
%postun	libGLU -p /sbin/ldconfig

%post	libGLw -p /sbin/ldconfig
%postun	libGLw -p /sbin/ldconfig

%post	libOSMesa -p /sbin/ldconfig
%postun	libOSMesa -p /sbin/ldconfig

%post	libOpenVG -p /sbin/ldconfig
%postun	libOpenVG -p /sbin/ldconfig

%if %{with egl}
%files libEGL
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libEGL.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libEGL.so.1
%attr(755,root,root) %{_libdir}/libglapi.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libglapi.so.0
%if %{with gallium}
%dir %{_libdir}/egl
%attr(755,root,root) %{_libdir}/egl/egl_gallium.so
%attr(755,root,root) %{_libdir}/egl/st_GL.so
%if %{with gallium_radeon}
%attr(755,root,root) %{_libdir}/egl/pipe_r300.so
%attr(755,root,root) %{_libdir}/egl/pipe_r600.so
%endif
%if %{with gallium_intel}
%attr(755,root,root) %{_libdir}/egl/pipe_i915.so
%attr(755,root,root) %{_libdir}/egl/pipe_i965.so
%endif
%endif

%files libEGL-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libEGL.so
%attr(755,root,root) %{_libdir}/libglapi.so
%dir %{_includedir}/EGL
%{_includedir}/EGL/egl.h
%{_includedir}/EGL/eglext.h
%{_includedir}/EGL/eglplatform.h
%dir %{_includedir}/KHR
%{_includedir}/KHR/khrplatform.h
%{_pkgconfigdir}/egl.pc

%if %{with static}
%files libEGL-static
%defattr(644,root,root,755)
%{_libdir}/libEGL.a
%endif
%endif

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
%{_pkgconfigdir}/dri.pc
%{_pkgconfigdir}/gl.pc

%files libGLES
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libGLES*.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libGLES*.so.[0-9]

%files libGLES-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libGLES*.so
%{_includedir}/GLES
%{_includedir}/GLES2
%{_pkgconfigdir}/gles*.pc

%if %{with static}
%files libGL-static
%defattr(644,root,root,755)
%{_libdir}/libGL.a
%endif

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

%if %{with static}
%files libGLU-static
%defattr(644,root,root,755)
%{_libdir}/libGLU.a
%endif

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

%if %{with static}
%files libGLw-static
%defattr(644,root,root,755)
%{_libdir}/libGLw.a
%endif

%if %{with osmesa}
%files libOSMesa
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOSMesa*.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libOSMesa*.so.7

%files libOSMesa-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOSMesa*.so
%{_includedir}/GL/osmesa.h

%if %{with static}
%files libOSMesa-static
%defattr(644,root,root,755)
%{_libdir}/libOSMesa*.a
%endif
%endif

%if %{with gallium}
%files libOpenVG
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libOpenVG.so.1
%attr(755,root,root) %{_libdir}/libOpenVG.so.1.0.0

%files libOpenVG-devel
%defattr(644,root,root,755)
%{_includedir}/VG
%{_libdir}/libOpenVG.so
%{_pkgconfigdir}/vg.pc
%endif

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

%files dri-driver-ati-radeon-R600
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/r600_dri.so

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
%if %{with gallium_intel}
%attr(755,root,root) %{_libdir}/xorg/modules/drivers/i965g_drv.so
%endif

%files dri-driver-matrox
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/mga_dri.so

%if %{with gallium}
%if %{with gallium_nouveau}
%files dri-driver-nouveau
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/nouveau_dri.so
%endif
%endif

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

%files dri-driver-via-unichrome
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/unichrome_dri.so

%if %{with gallium}
%files dri-driver-vmwgfx
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/vmwgfx_dri.so
%endif
