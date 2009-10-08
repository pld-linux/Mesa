#
# TODO:
# - subpackage with non-dri libGL for use with X-servers with missing GLX extension?
# - resurrect static if it's useful
#
# Conditional build:
%bcond_without	demos	# don't build demos
%bcond_without	motif	# build static libGLw without Motif interface
%bcond_without	gallium
%bcond_with	gallium_intel # gallium i915 driver (but doesn't work with AIGLX)
%bcond_with	multigl	# package libGL in a way allowing concurrent install with nvidia/fglrx drivers
%bcond_with	static
#
# minimal supported xserver version
%define		xserver_ver	1.5.0
# glapi version (glapi tables in dri drivers and libglx must be in sync);
# set to current Mesa version on ABI break, when xserver tables get regenerated
# (until they start to be somehow versioned themselves)
%define		glapi_ver	7.1.0
#
Summary:	Free OpenGL implementation
Summary(pl.UTF-8):	Wolnodostępna implementacja standardu OpenGL
Name:		Mesa
Version:	7.6
Release:	2%{?with_multigl:.mgl}
License:	MIT (core), SGI (GLU,libGLw) and others - see license.html file
Group:		X11/Libraries
Source0:	ftp://ftp.freedesktop.org/pub/mesa/%{version}/%{name}Lib-%{version}.tar.bz2
# Source0-md5:	8c75f90cd0303cfac9e4b6d54f6759ca
Source1:	ftp://ftp.freedesktop.org/pub/mesa/%{version}/%{name}Demos-%{version}.tar.bz2
# Source1-md5:	0ede7adf217951acd90dbe4551210c07
Source2:	http://www.archlinux.org/~jgc/gl-manpages-1.0.1.tar.bz2
# Source2-md5:	6ae05158e678f4594343f32c2ca50515
Patch0:		%{name}-realclean.patch
Patch1:		%{name}-sparc64.patch
Patch2:		%{name}-git.patch
URL:		http://www.mesa3d.org/
BuildRequires:	expat-devel
%{?with_demos:BuildRequires:	glew-devel}
BuildRequires:	libdrm-devel >= 2.4.12-3
BuildRequires:	libselinux-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.4d
%{?with_motif:BuildRequires:	motif-devel}
BuildRequires:	rpmbuild(macros) >= 1.470
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libXdamage-devel
BuildRequires:	xorg-lib-libXext-devel >= 1.0.5
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
BuildRequires:	xorg-proto-dri2proto-devel >= 1.99.3
BuildRequires:	xorg-proto-glproto-devel
BuildRequires:	xorg-proto-printproto-devel
BuildRequires:	xorg-util-makedepend
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{without gallium}
%undefine	with_gallium_intel
%endif

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
Requires:	libdrm >= 2.4.5
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

%prep
%setup -q -b1 -a2
%patch0 -p0
%patch1 -p1
%patch2 -p1

# fix demos
find progs -type f|xargs sed -i -e "s,\.\./images/,%{_examplesdir}/%{name}-%{version}/images/,g"

%build
[ ! -f configure ] && ./autogen.sh

dri_drivers="i810 i965 mach64 mga r128 r200 r300 radeon savage s3v trident \
%if %{without gallium_intel}
i915 \
%endif
%ifarch sparc sparcv9 sparc64
ffb \
%endif
%ifarch %{ix86} %{x8664}
sis \
%endif
swrast tdfx unichrome"

dri_drivers=$(echo $dri_drivers | xargs | tr ' ' ',')

common_flags="\
	--enable-shared \
	--enable-selinux \
	--enable-pic \
	--enable-glx-tls \
	--disable-egl \
	--with%{!?with_demos:out}-demos"

# osmesa variants
%configure $common_flags \
	--with-driver=osmesa \
	--disable-asm \
	--with-osmesa-bits=8
%{__make} \
	SRC_DIRS=mesa
mv %{_lib} osmesa8
%{__make} clean

%configure $common_flags \
	--with-driver=osmesa \
	--disable-asm \
	--with-osmesa-bits=16
%{__make} \
	SRC_DIRS=mesa
mv %{_lib} osmesa16
%{__make} clean

%configure $common_flags \
	--with-driver=osmesa \
	--disable-asm \
	--with-osmesa-bits=32
%{__make} \
	SRC_DIRS=mesa
mv %{_lib} osmesa32
%{__make} clean

%configure $common_flags \
	--enable-glu \
	--enable-glw \
	--disable-glut \
%if %{with gallium}
	--enable-gallium \
	--%{?with_gallium_intel:en}%{!?with_gallium_intel:dis}able-gallium-intel \
	--enable-gallium-nouveau \
	--with-state-trackers=dri \
%else
	--disable-gallium \
%endif
	--with-driver=dri \
	--with-dri-drivers=${dri_drivers} \
	--with-dri-driverdir=%{_libdir}/xorg/modules/dri

%{__make}
%{__make} -C progs/xdemos glxgears glxinfo
%if %{with demos}
%{__make} -C progs/demos
%endif

cd gl-manpages-*
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_examplesdir}/%{name}-%{version}}

# libs without drivers
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cd gl-manpages-*
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
cd ..

install osmesa*/* $RPM_BUILD_ROOT%{_libdir}

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

# strip out undesirable headers
olddir=$(pwd)
cd $RPM_BUILD_ROOT%{_includedir}/GL
rm [a-fh-np-wyz]*.h gg*.h glf*.h
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
%{_pkgconfigdir}/dri.pc
%{_pkgconfigdir}/gl.pc
%{_mandir}/man3/gl[^uX]*.3gl*
%{_mandir}/man3/glX*.3gl*

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
%{_mandir}/man3/glu*.3gl*

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

%files libOSMesa
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOSMesa*.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libOSMesa*.so.[0-9]

%files libOSMesa-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOSMesa*.so
%{_includedir}/GL/osmesa.h

%if %{with static}
%files libOSMesa-static
%defattr(644,root,root,755)
%{_libdir}/libOSMesa*.a
%endif

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

%if %{with gallium}
%files dri-driver-nouveau
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/nouveau_dri.so
%endif

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

%files dri-driver-via-unichrome
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/unichrome_dri.so

%if %{with demos}
%files demos
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
%endif
