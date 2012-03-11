#
# TODO:
# - consider:
#   --enable-shared-dricore
# - subpackage with non-dri libGL for use with X-servers with missing GLX extension?
# - resurrect static if it's useful
#
# Conditional build:
%bcond_without	egl		# EGL libraries
%bcond_without	gallium		# gallium drivers
%bcond_with	gallium_intel	# gallium i915 driver (but doesn't work with AIGLX)
%bcond_without	gallium_nouveau	# gallium nouveau driver
%bcond_without	osmesa		# OSMesa libraries
%bcond_without	gbm		# with Graphics Buffer Manager
%bcond_with	static_libs	# static libraries
#
# minimal supported xserver version
%define		xserver_ver	1.5.0
# glapi version (glapi tables in dri drivers and libglx must be in sync);
# set to current Mesa version on ABI break, when xserver tables get regenerated
# (until they start to be somehow versioned themselves)
%define		glapi_ver	7.1.0
#
%define		libdrm_ver	2.4.30
%define		dri2proto_ver	2.6
%define		glproto_ver	1.4.14
#
Summary:	Free OpenGL implementation
Summary(pl.UTF-8):	Wolnodostępna implementacja standardu OpenGL
Name:		Mesa
Version:	8.0.1
Release:	1
License:	MIT (core), SGI (GLU) and others - see license.html file
Group:		X11/Libraries
Source0:	ftp://ftp.freedesktop.org/pub/mesa/%{version}/%{name}Lib-%{version}.tar.bz2
# Source0-md5:	24eeebf66971809d8f40775a379b36c9
Patch0:		%{name}-realclean.patch
URL:		http://www.mesa3d.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	expat-devel
BuildRequires:	gcc >= 5:3.3
BuildRequires:	libdrm-devel >= %{libdrm_ver}
BuildRequires:	libselinux-devel
BuildRequires:	libstdc++-devel >= 5:3.3.0
BuildRequires:	libtalloc-devel >= 2:2.0.1
BuildRequires:	libtool >= 2:1.4d
BuildRequires:	libvdpau-devel >= 0.4.1
BuildRequires:	llvm-devel >= 2.9
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
BuildRequires:	xorg-lib-libXvMC-devel >= 1.0.6
BuildRequires:	xorg-lib-libXxf86vm-devel
BuildRequires:	xorg-proto-dri2proto-devel >= %{dri2proto_ver}
BuildRequires:	xorg-proto-glproto-devel >= %{glproto_ver}
BuildRequires:	xorg-util-makedepend
BuildRequires:	xorg-xserver-server-devel
%if %{with egl}
BuildRequires:	libxcb-devel
BuildRequires:	udev-devel >= 1:150
%endif
%if %{with gallium}
BuildRequires:	xorg-proto-xextproto-devel >= 7.0.99.1
BuildRequires:	xorg-xserver-server-devel >= 1.6.0
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{without gallium}
%undefine	with_gallium_intel
%undefine	with_gallium_nouveau
%endif

%if %{without egl}
%undefine	with_gbm
%endif

# _glapi_tls_Dispatch is defined in libglapi, but it's some kind of symbol ldd -r doesn't notice(?)
%define		skip_post_check_so      libGLESv1_CM.so.1.* libGLESv2.so.2.* libGL.so.1.* libXvMCnouveau.so.1.* libXvMCr300.so.1.*  libXvMCr600.so.1.* libXvMCsoftpipe.so.1.* libvdpau_nouveau.so.1.*

# llvm build broken
%define		filterout_ld    -Wl,--as-needed

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
# glx driver in libEGL dlopens libGL.so
Requires:	OpenGL >= 1.2
Requires:	libdrm >= %{libdrm_ver}
%if %{with gallium}
# for egl_gallium.so
Requires:	Mesa-libOpenVG = %{version}-%{release}
Requires:	udev-libs >= 1:150
%endif
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
Requires:	libdrm-devel >= %{libdrm_ver}
Requires:	xorg-lib-libX11-devel
Requires:	xorg-lib-libXdamage-devel
Requires:	xorg-lib-libXext-devel
Requires:	xorg-lib-libXfixes-devel
Requires:	xorg-lib-libXxf86vm-devel
Requires:	xorg-proto-dri2proto-devel >= %{dri2proto_ver}
Requires:	xorg-proto-glproto-devel >= %{glproto_ver}
Provides:	EGL-devel = 1.4

%description libEGL-devel
Header files for Mesa implementation of EGL library.

%description libEGL-devel -l pl.UTF-8
Pliki nagłówkowe implementacji Mesa biblioteki EGL.

%package libEGL-static
Summary:	Static Mesa EGL library
Summary(pl.UTF-8):	Statyczna biblioteka Mesa EGL
License:	MIT
Group:		Development/Libraries
Requires:	%{name}-libEGL-devel = %{version}-%{release}
Provides:	EGL-static = 1.4

%description libEGL-static
Static Mesa EGL library.

%description libEGL-static -l pl.UTF-8
Statyczna biblioteka Mesa EGL.

%package gbm-driver-i915
Summary:	i915 driver for Mesa GBM framework (used by EGL and OpenVG APIs)
Summary(pl.UTF-8):	Sterownik i915 dla szkieletu Mesa GBM (wykorzystywanego przez API EGL i OpenVG)
Group:		Libraries
Requires:	%{name}-libEGL = %{version}-%{release}

%description gbm-driver-i915
i915 driver for Mesa Graphics Buffer Manager (used by EGL and OpenVG
APIs). It supports Intel 915/945/G33/Q33/Q35/Pineview chips.

%description gbm-driver-i915 -l pl.UTF-8
Sterownik i915 dla szkieletu Mesa Graphics Buffer Manager (zarządcy
bufora graficznego, wykorzystywanego przez API EGL i OpenVG).
Obsługuje układy Intel 915/945/G33/Q33/Q35/Pineview.

%package gbm-driver-nouveau
Summary:	nouveau driver for Mesa GBM framework (used by EGL and OpenVG APIs)
Summary(pl.UTF-8):	Sterownik nouveau dla szkieletu Mesa GBM (wykorzystywanego przez API EGL i OpenVG)
Group:		Libraries
Requires:	%{name}-libEGL = %{version}-%{release}

%description gbm-driver-nouveau
nouveau driver for Mesa Graphics Buffer Manager (used by EGL and
OpenVG APIs). It supports NVidia adapters.

%description gbm-driver-nouveau -l pl.UTF-8
Sterownik nouveau dla szkieletu Mesa Graphics Buffer Manager (zarządcy
bufora graficznego, wykorzystywanego przez API EGL i OpenVG).
Obsługuje karty graficzne firmy NVidia.

%package gbm-driver-r300
Summary:	r300 driver for Mesa GBM framework (used by EGL and OpenVG APIs)
Summary(pl.UTF-8):	Sterownik r300 dla szkieletu Mesa GBM (wykorzystywanego przez API EGL i OpenVG)
Group:		Libraries
Requires:	%{name}-libEGL = %{version}-%{release}

%description gbm-driver-r300
r300 driver for Mesa Graphics Buffer Manager (used by EGL and
OpenVG APIs). It supports ATI Radeon adapters based on
R300/R400/RS690/R500 chips.

%description gbm-driver-r300 -l pl.UTF-8
Sterownik r300 dla szkieletu Mesa Graphics Buffer Manager (zarządcy
bufora graficznego, wykorzystywanego przez API EGL i OpenVG).
Obsługuje karty graficzne ATI Radeon oparte na układach
R300/R400/RS690/R500.

%package gbm-driver-r600
Summary:	r600 driver for Mesa GBM framework (used by EGL and OpenVG APIs)
Summary(pl.UTF-8):	Sterownik r600 dla szkieletu Mesa GBM (wykorzystywanego przez API EGL i OpenVG)
Group:		Libraries
Requires:	%{name}-libEGL = %{version}-%{release}

%description gbm-driver-r600
r600 driver for Mesa Graphics Buffer Manager (used by EGL and
OpenVG APIs). It supports ATI Radeon adapters based on R600/R700
chips.

%description gbm-driver-r600 -l pl.UTF-8
Sterownik r600 dla szkieletu Mesa Graphics Buffer Manager (zarządcy
bufora graficznego, wykorzystywanego przez API EGL i OpenVG).
Obsługuje karty graficzne ATI Radeon oparte na układach R600/R700.

%package gbm-driver-vmwgfx
Summary:	vmwgfx driver for Mesa GBM framework (used by EGL and OpenVG APIs)
Summary(pl.UTF-8):	Sterownik vmwgfx dla szkieletu Mesa GBM (wykorzystywanego przez API EGL i OpenVG)
Group:		Libraries
Requires:	%{name}-libEGL = %{version}-%{release}

%description gbm-driver-vmwgfx
vmwgfx driver for Mesa Graphics Buffer Manager (used by EGL and
OpenVG APIs). It supports VMware virtual video adapter.

%description gbm-driver-vmwgfx -l pl.UTF-8
Sterownik vmwgfx dla szkieletu Mesa Graphics Buffer Manager (zarządcy
bufora graficznego, wykorzystywanego przez API EGL i OpenVG).
Obsługuje wirtualną kartę graficzną VMware.

%package libGL
Summary:	Free Mesa3D implementation of libGL OpenGL library
Summary(pl.UTF-8):	Wolnodostępna implementacja Mesa3D biblioteki libGL ze standardu OpenGL
License:	MIT
Group:		X11/Libraries
Requires:	libdrm >= %{libdrm_ver}
Provides:	OpenGL = 2.1
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

%package libGLES
Summary:	Mesa implementation of GLES (OpenGL ES) libraries
Summary(pl.UTF-8):	Implementacja Mesa bibliotek GLES (OpenGL ES)
Group:		Libraries
# only for libglapi.so.0
Requires:	%{name}-libEGL = %{version}-%{release}

%description libGLES
This package contains shared libraries of Mesa implementation of GLES
(OpenGL ES) - cross-platform API for full-function 2D and 3D graphics
on embedded systems. OpenGL ES specification can be found on Khronos
Group site: <http://www.khronos.org/opengles/>. Mesa implements OpenGL
ES 1.1 and 2.0.

%description libGLES -l pl.UTF-8
Ten pakiet zawiera biblioteki współdzielone implementacji Mesa
standardu GLES (OpenGL ES) - wieloplatformowego API do w pełni
funkcjonalnej grafiki 2D i 3D na systemach wbudowanych. Specyfikację
OpenGL ES można znaleźć na stronie Khronos Group:
<http://www.khronos.org/opengles/>. Mesa zawiera implementacją OpenGL
ES 1.1 i 2.0.

%package libGLES-devel
Summary:	Header files for Mesa GLES libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Mesa GLES
Group:		Development/Libraries
# EGL for libglapi.so, <KHR/khrplatform.h> always required, <EGL/egl.h> for <GLES/egl.h>
Requires:	%{name}-libEGL-devel = %{version}-%{release}
Requires:	%{name}-libGLES = %{version}-%{release}

%description libGLES-devel
Header files for Mesa GLES libraries.

%description libGLES-devel -l pl.UTF-8
Pliki nagłówkowe bibliotek Mesa GLES.

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
Requires:	libselinux-devel

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
Summary:	Mesa implementation of OpenVG (Vector Graphics Accelleration) API
Summary(pl.UTF-8):	Implementacja Mesa API OpenVG (akceleracji grafiki wektorowej)
License:	MIT
Group:		Libraries
# doesn't require base

%description libOpenVG
This package contains Mesa implementation of OpenVG - cross-platform
API that provides a low-level hardware acceleration interface for
vector graphics libraries such as Flash and SVG. OpenVG specification
can be found on Khronos Group site: <http://www.khronos.org/openvg/>.
Mesa implements OpenVG 1.1.

%description libOpenVG -l pl.UTF-8
Ten pakiet zawiera implementację Mesa standardu OpenVG -
wieloplatfomowego API zapewniającego niskopoziomowy interfejs
akceleracji sprzętowej dla bibliotek grafiki wektorowej, takiej jak
Flash czy SVG. Specyfikację OpenVG można znaleźć na stronie Khronos
Group: <http://www.khronos.org/openvg/>. Mesa zawiera implementację
OpenVG w wersji 1.1.

%package libOpenVG-devel
Summary:	Header file for Mesa OpenVG library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki Mesa OpenVG
License:	MIT
Group:		Development/Libraries
# EGL headers for <KHR/khrplatform.h>
Requires:	%{name}-libEGL-devel = %{version}-%{release}
Requires:	%{name}-libOpenVG = %{version}-%{release}

%description libOpenVG-devel
Header file for Mesa OpenVG library.

%description libOpenVG-devel -l pl.UTF-8
Plik nagłówkowy biblioteki Mesa OpenVG.

%package libXvMC-nouveau
Summary:	Mesa implementation of XvMC API for NVidia adapters
Summary(pl.UTF-8):	Implementacja Mesa API XvMC dla kart NVidia
License:	MIT
Group:		Libraries
Requires:	libdrm >= %{libdrm_ver}
Conflicts:	Mesa-libXvMC

%description libXvMC-nouveau
Mesa implementation of XvMC API for NVidia adapters (NV40-NV96, NVa0).

%description libXvMC-nouveau -l pl.UTF-8
Implementacja Mesa API XvMC dla kart NVidia (NV40-NV96, NVa0).

%package libXvMC-r300
Summary:	Mesa implementation of XvMC API for ATI Radeon R300 series adapters
Summary(pl.UTF-8):	Implementacja Mesa API XvMC dla kart ATI Radeon z serii R300
License:	MIT
Group:		Libraries
Requires:	libdrm >= %{libdrm_ver}
Conflicts:	Mesa-libXvMC

%description libXvMC-r300
Mesa implementation of XvMC API for ATI Radeon adapters based on
R300/R400/RS690/R500 chips.

%description libXvMC-r300 -l pl.UTF-8
Implementacja Mesa API XvMC dla kart ATI Radeon opartych na układach
R300/R400/RS690/R500.

%package libXvMC-r600
Summary:	Mesa implementation of XvMC API for ATI Radeon R600 series adapters
Summary(pl.UTF-8):	Implementacja Mesa API XvMC dla kart ATI Radeon z serii R600
License:	MIT
Group:		Libraries
Requires:	libdrm >= %{libdrm_ver}
Conflicts:	Mesa-libXvMC

%description libXvMC-r600
Mesa implementation of XvMC API for ATI Radeon adapters based on
R600/R700 chips.

%description libXvMC-r600 -l pl.UTF-8
Implementacja Mesa API XvMC dla kart ATI Radeon opartych na układach
R600/R700.

%package libXvMC-softpipe
Summary:	Mesa softpipe implementation of XvMC API
Summary(pl.UTF-8):	Implementacja Mesa softpipe API XvMC
License:	MIT
Group:		Libraries
Requires:	libdrm >= %{libdrm_ver}
Conflicts:	Mesa-libXvMC

%description libXvMC-softpipe
Mesa softpipe implementation of XvMC API.

%description libXvMC-softpipe -l pl.UTF-8
Implementacja Mesa softpipe API XvMC.

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
X.org DRI driver for ATI R300/R400/RS690/R500 card family.

%description dri-driver-ati-radeon-R300 -l pl.UTF-8
Sterownik X.org DRI dla rodziny kart ATI R300/R400/RS690/R500.

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
X.org DRI driver for ATI R600/R700 card family.

%description dri-driver-ati-radeon-R600 -l pl.UTF-8
Sterownik X.org DRI dla rodziny kart ATI R600/R700.

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
X.org DRI driver for Intel i915 card family (915, 945, G33, Q33, Q35,
Pineview).

%description dri-driver-intel-i915 -l pl.UTF-8
Sterownik X.org DRI dla rodziny kart Intel i915 (915, 945, G33, Q33,
Q35, Pineview).

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
X.org DRI driver for Intel i965 card family (946GZ, 965G, 965Q, 965GM,
965GME, GM45, G41, B43, Q45, G45);

%description dri-driver-intel-i965 -l pl.UTF-8
Sterownik X.org DRI dla rodziny kart Intel i965 (946GZ, 965G, 965Q,
965GM, 965GME, GM45, G41, B43, Q45, G45).

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

%package dri-driver-vmwgfx
Summary:	X.org DRI driver for VMware
Summary(pl.UTF-8):	Sterownik X.org DRI dla VMware
License:	MIT
Group:		X11/Libraries
Requires:	xorg-driver-video-vmware
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}

%description dri-driver-vmwgfx
X.org DRI driver for VMWare.

%description dri-driver-vmwgfx -l pl.UTF-8
Sterownik X.org DRI dla VMware.

%package -n libvdpau-driver-mesa-nouveau
Summary:	Mesa nouveau driver for the vdpau API
Summary(pl.UTF-8):	Sterownik Mesa nouveau dla API vdpau
License:	MIT
Group:		X11/Libraries
Requires:	libdrm >= %{libdrm_ver}
Requires:	libvdpau >= 0.4.1
Conflicts:	libvdpau-driver-mesa

%description -n libvdpau-driver-mesa-nouveau
Mesa nouveau driver for the vdpau API. It supports NVidia adapters
(NV40-NV96, NVa0).

%description -n libvdpau-driver-mesa-nouveau -l pl.UTF-8
Sterownik Mesa nouveau dla API vdpau. Obsługuje karty NVidia
(NV40-NV96, NVa0).

%package -n libvdpau-driver-mesa-r300
Summary:	Mesa r300 driver for the vdpau API
Summary(pl.UTF-8):	Sterownik Mesa r300 dla API vdpau
License:	MIT
Group:		X11/Libraries
Requires:	libdrm >= %{libdrm_ver}
Requires:	libvdpau >= 0.4.1
Conflicts:	libvdpau-driver-mesa

%description -n libvdpau-driver-mesa-r300
Mesa r300 driver for the vdpau API. It supports ATI Radeon adapters
based on R300/R400/RS690/R500 chips.

%description -n libvdpau-driver-mesa-r300 -l pl.UTF-8
Sterownik Mesa r300 dla API vdpau. Obsługuje karty ATI Radeon oparte
na układach R300/R400/RS690/R500.

%package -n libvdpau-driver-mesa-r600
Summary:	Mesa r600 driver for the vdpau API
Summary(pl.UTF-8):	Sterownik Mesa r600 dla API vdpau
License:	MIT
Group:		X11/Libraries
Requires:	libdrm >= %{libdrm_ver}
Requires:	libvdpau >= 0.4.1
Conflicts:	libvdpau-driver-mesa

%description -n libvdpau-driver-mesa-r600
Mesa r600 driver for the vdpau API. It supports ATI Radeon adapters
based on R600/R700 chips.

%description -n libvdpau-driver-mesa-r600 -l pl.UTF-8
Sterownik Mesa r600 dla API vdpau. Obsługuje karty ATI Radeon oparte
na układach R600/R700.

%package -n libvdpau-driver-mesa-softpipe
Summary:	Mesa softpipe driver for the vdpau API
Summary(pl.UTF-8):	Sterownik Mesa softpipe dla API vdpau
License:	MIT
Group:		X11/Libraries
Requires:	libdrm >= %{libdrm_ver}
Requires:	libvdpau >= 0.4.1
Conflicts:	libvdpau-driver-mesa

%description -n libvdpau-driver-mesa-softpipe
Mesa softpipe driver for the vdpau API.

%description -n libvdpau-driver-mesa-softpipe -l pl.UTF-8
Sterownik Mesa softpipe dla API vdpau.

%prep
%setup -q
%patch0 -p0

%build
%{__aclocal}
%{__autoconf}

dri_drivers="r200 radeon \
%if %{without gallium_intel}
i915 \
%endif
i965
%ifarch sparc sparcv9 sparc64
ffb \
%endif
swrast"

dri_drivers=$(echo $dri_drivers | xargs | tr ' ' ',')

gallium_drivers="svga swrast \
%if %{with gallium_intel}
i915 \
%endif
r300 \
r600 \
%if %{with gallium_nouveau}
nouveau \
%endif
"

gallium_drivers=$(echo $gallium_drivers | xargs | tr ' ' ',')

common_flags="\
	--enable-shared \
	--enable-glx-tls \
	--enable-pic \
	--enable-selinux \
	%{?with_static_libs:--enable-static} \
"

osmesa_common_flags="\
	--with-driver=osmesa \
	--disable-asm \
	--disable-egl \
	--disable-glu"

%if %{with osmesa}
%configure $common_flags $osmesa_common_flags \
	--with-osmesa-bits=8
%{__make}
%{__make} -C src/mesa osmesa.pc
mv %{_lib} osmesa8
cp -p src/mesa/osmesa.pc osmesa8
%{__make} clean
%endif

%configure $common_flags \
	%{__enable gbm} \
	--enable-shared-glapi \
%if %{with egl}
	--enable-egl \
	--enable-gles1 \
	--enable-gles2 \
%endif
%if %{with gallium}
	--enable-gallium-llvm \
	%{__enable egl gallium-egl} \
	%{__enable gbm gallium-gbm} \
	--enable-openvg \
	--enable-vdpau \
	--enable-xvmc \
	--with-gallium-drivers=${gallium_drivers} \
%else
	--without-gallium-drivers \
%endif
	--with-driver=dri \
	--with-dri-drivers=${dri_drivers} \
	--with-dri-driverdir=%{_libdir}/xorg/modules/dri

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with osmesa}
cp -dp osmesa8/libOSMesa* $RPM_BUILD_ROOT%{_libdir}
cp -p osmesa8/osmesa.pc $RPM_BUILD_ROOT%{_pkgconfigdir}
%endif

# strip out undesirable headers
%{__rm} $RPM_BUILD_ROOT%{_includedir}/GL/{vms_x_fix,wglext,wmesa}.h

# remove "OS ABI: Linux 2.4.20" tag, so private copies (nvidia or fglrx),
# set up via /etc/ld.so.conf.d/*.conf will be preferred over this
strip -R .note.ABI-tag $RPM_BUILD_ROOT%{_libdir}/libGL.so.*.*

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

%post	libOSMesa -p /sbin/ldconfig
%postun	libOSMesa -p /sbin/ldconfig

%post	libOpenVG -p /sbin/ldconfig
%postun	libOpenVG -p /sbin/ldconfig

%post	libXvMC-nouveau -p /sbin/ldconfig
%postun	libXvMC-nouveau -p /sbin/ldconfig
%post	libXvMC-r300 -p /sbin/ldconfig
%postun	libXvMC-r300 -p /sbin/ldconfig
%post	libXvMC-r600 -p /sbin/ldconfig
%postun	libXvMC-r600 -p /sbin/ldconfig
%post	libXvMC-softpipe -p /sbin/ldconfig
%postun	libXvMC-softpipe -p /sbin/ldconfig

%if %{with egl}
%files libEGL
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libEGL.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libEGL.so.1
%attr(755,root,root) %{_libdir}/libglapi.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libglapi.so.0
%if %{with gbm}
%attr(755,root,root) %{_libdir}/libgbm.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libgbm.so.1
%endif
%if %{with gallium}
%dir %{_libdir}/egl
%attr(755,root,root) %{_libdir}/egl/egl_gallium.so
%if %{with gbm}
%dir %{_libdir}/gbm
%attr(755,root,root) %{_libdir}/gbm/gbm_gallium_drm.so
%endif
%endif

%files libEGL-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libEGL.so
%attr(755,root,root) %{_libdir}/libglapi.so
%dir %{_includedir}/EGL
%{_includedir}/EGL/egl.h
%{_includedir}/EGL/eglext.h
%{_includedir}/EGL/eglmesaext.h
%{_includedir}/EGL/eglplatform.h
%dir %{_includedir}/KHR
%{_includedir}/KHR/khrplatform.h
%{_pkgconfigdir}/egl.pc
%if %{with gbm}
%attr(755,root,root) %{_libdir}/libgbm.so
%{_includedir}/gbm.h
%{_pkgconfigdir}/gbm.pc
%endif

%if %{with static_libs}
%files libEGL-static
%defattr(644,root,root,755)
%{_libdir}/libEGL.a
%endif
%endif

%if %{with gallium}
%if %{with gallium_intel}
%files gbm-driver-i915
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gbm/pipe_i915.so
%endif

%if %{with gallium_nouveau}
%files gbm-driver-nouveau
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gbm/pipe_nouveau.so
%endif

%files gbm-driver-r300
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gbm/pipe_r300.so

%files gbm-driver-r600
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gbm/pipe_r600.so

%files gbm-driver-vmwgfx
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gbm/pipe_vmwgfx.so
%endif

%files libGL
%defattr(644,root,root,755)
%doc docs/{*.html,README.{MITS,QUAKE,THREADS},RELNOTES*}
%attr(755,root,root) %{_libdir}/libGL.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libGL.so.1
# symlink for binary apps which fail to conform Linux OpenGL ABI
# (and dlopen libGL.so instead of libGL.so.1; the same does Mesa libEGL)
%attr(755,root,root) %{_libdir}/libGL.so

%files libGL-devel
%defattr(644,root,root,755)
%doc docs/*.spec
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

%if %{with static_libs}
%files libGL-static
%defattr(644,root,root,755)
%{_libdir}/libGL.a
%endif

%files libGLES
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libGLESv1_CM.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libGLESv1_CM.so.1
%attr(755,root,root) %{_libdir}/libGLESv2.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libGLESv2.so.2

%files libGLES-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libGLESv1_CM.so
%attr(755,root,root) %{_libdir}/libGLESv2.so
%{_includedir}/GLES
%{_includedir}/GLES2
%{_pkgconfigdir}/glesv1_cm.pc
%{_pkgconfigdir}/glesv2.pc

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

%if %{with static_libs}
%files libGLU-static
%defattr(644,root,root,755)
%{_libdir}/libGLU.a
%endif

%if %{with osmesa}
%files libOSMesa
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOSMesa.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libOSMesa.so.8

%files libOSMesa-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOSMesa.so
%{_includedir}/GL/osmesa.h
%{_pkgconfigdir}/osmesa.pc

%if %{with static_libs}
%files libOSMesa-static
%defattr(644,root,root,755)
%{_libdir}/libOSMesa.a
%endif
%endif

%if %{with gallium}
%files libOpenVG
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOpenVG.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libOpenVG.so.1

%files libOpenVG-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOpenVG.so
%{_includedir}/VG
%{_pkgconfigdir}/vg.pc
%endif

%if %{with gallium}
%files libXvMC-nouveau
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libXvMCnouveau.so.1.0
%attr(755,root,root) %ghost %{_libdir}/libXvMCnouveau.so.1

%files libXvMC-r300
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libXvMCr300.so.1.0
%attr(755,root,root) %ghost %{_libdir}/libXvMCr300.so.1

%files libXvMC-r600
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libXvMCr600.so.1.0
%attr(755,root,root) %ghost %{_libdir}/libXvMCr600.so.1

%files libXvMC-softpipe
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libXvMCsoftpipe.so.1.0
%attr(755,root,root) %ghost %{_libdir}/libXvMCsoftpipe.so.1
%endif

%files dri-driver-ati-radeon-R100
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/radeon_dri.so

%files dri-driver-ati-radeon-R200
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/r200_dri.so

%if %{with gallium}
%files dri-driver-ati-radeon-R300
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/r300_dri.so

%files dri-driver-ati-radeon-R600
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/r600_dri.so

%files dri-driver-intel-i915
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/i915_dri.so

%files dri-driver-intel-i965
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/i965_dri.so

%if %{with gallium_nouveau}
%files dri-driver-nouveau
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/nouveau_dri.so
%endif
%endif

%files dri-driver-swrast
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/swrast_dri.so

%if %{with gallium}
%files dri-driver-vmwgfx
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/vmwgfx_dri.so
%endif

%if %{with gallium}
# ldconfig is not used in vdpau tree, so package all symlinks
%if %{with gallium_nouveau}
%files -n libvdpau-driver-mesa-nouveau
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_nouveau.so.1.0
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_nouveau.so.1
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_nouveau.so
%endif

%files -n libvdpau-driver-mesa-r300
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_r300.so.1.0
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_r300.so.1
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_r300.so

%files -n libvdpau-driver-mesa-r600
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_r600.so.1.0
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_r600.so.1
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_r600.so

%files -n libvdpau-driver-mesa-softpipe
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_softpipe.so.1.0
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_softpipe.so.1
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_softpipe.so
%endif
