#
# TODO:
# - check if gallium_intel note is still valid, switch the bcond if not
# - consider:
# - subpackage with non-dri libGL for use with X-servers with missing GLX extension?
# - resurrect static if it's useful (using plain xorg target? DRI doesn't support static)
#
# Conditional build:
%bcond_without	gallium		# gallium drivers
%bcond_with	gallium_intel	# gallium i915 driver (instead of plain dri; doesn't work with AIGLX)
%bcond_without	gallium_nouveau	# gallium nouveau driver
%bcond_without	egl		# EGL libraries
%bcond_without	gbm		# Graphics Buffer Manager
%bcond_without	opencl		# OpenCL library
%bcond_without	wayland		# Wayland EGL
%bcond_without	xa		# XA state tracker (for vmwgfx xorg driver)
%bcond_with	static_libs	# static libraries [not supported for DRI, thus broken currently]
#
# minimal supported xserver version
%define		xserver_ver	1.5.0
# glapi version (glapi tables in dri drivers and libglx must be in sync);
# set to current Mesa version on ABI break, when xserver tables get regenerated
# (until they start to be somehow versioned themselves)
%define		glapi_ver	7.1.0
#
%define		libdrm_ver	2.4.39
%define		dri2proto_ver	2.6
%define		glproto_ver	1.4.14
#
%define		snap		20120921
#
Summary:	Free OpenGL implementation
Summary(pl.UTF-8):	Wolnodostępna implementacja standardu OpenGL
Name:		Mesa
Version:	9.0.1
Release:	1
License:	MIT (core) and others - see license.html file
Group:		X11/Libraries
Source0:	ftp://ftp.freedesktop.org/pub/mesa/%{version}/%{name}Lib-%{version}.tar.bz2
# Source0-md5:	97d6554c05ea7449398afe3a0ede7018
Patch0:		%{name}-link.patch
URL:		http://www.mesa3d.org/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
%{?with_opencl:BuildRequires:	clang-devel >= 3.1}
BuildRequires:	expat-devel
BuildRequires:	gcc >= 5:3.3
%{?with_opencl:BuildRequires:	gcc >= 6:4.6}
BuildRequires:	libdrm-devel >= %{libdrm_ver}
BuildRequires:	libselinux-devel
BuildRequires:	libstdc++-devel >= 5:3.3.0
BuildRequires:	libtalloc-devel >= 2:2.0.1
BuildRequires:	libtool >= 2:2.2
BuildRequires:	libvdpau-devel >= 0.4.1
BuildRequires:	libxcb-devel >= 1.8.1
BuildRequires:	llvm-devel >= 3.1
BuildRequires:	perl-base
BuildRequires:	pixman-devel
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(talloc) >= 2.0.1
BuildRequires:	python >= 2
BuildRequires:	python-libxml2
BuildRequires:	python-modules >= 2
BuildRequires:	rpmbuild(macros) >= 1.470
BuildRequires:	sed >= 4.0
%{?with_egl:BuildRequires:	udev-devel >= 1:150}
# wayland-{client,server}
%{?with_wayland:BuildRequires:	wayland-devel >= 1.0.0}
BuildRequires:	xorg-lib-libXdamage-devel
BuildRequires:	xorg-lib-libXext-devel >= 1.0.5
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	xorg-lib-libXvMC-devel >= 1.0.6
BuildRequires:	xorg-lib-libXxf86vm-devel
BuildRequires:	xorg-proto-dri2proto-devel >= %{dri2proto_ver}
BuildRequires:	xorg-proto-glproto-devel >= %{glproto_ver}
BuildRequires:	xorg-util-makedepend
BuildRequires:	xorg-xserver-server-devel >= %{xserver_ver}
%if %{with gallium}
BuildRequires:	xorg-proto-xextproto-devel >= 7.0.99.1
BuildRequires:	xorg-xserver-server-devel >= 1.6.0
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{without gallium}
%undefine	with_gallium_intel
%undefine	with_gallium_nouveau
%undefine	with_opencl
%undefine	with_xa
%endif

%if %{without egl}
%undefine	with_gbm
%undefine	with_wayland
%endif

# libGLESv1_CM, libGLESv2, libGL, libOSMesa:
#  _glapi_tls_Dispatch is defined in libglapi, but it's some kind of symbol ldd -r doesn't notice(?)
# libdricore: internal library, not linked with libglapi
# libgbm: circular dependency with libEGL (wayland_buffer_is_drm symbol)
%define		skip_post_check_so      libGLESv1_CM.so.1.* libGLESv2.so.2.* libGL.so.1.* libOSMesa.so.* libdricore.*.so.* libgbm.*.so.*

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
Requires:	%{name}-libglapi = %{version}-%{release}
# glx driver in libEGL dlopens libGL.so
Requires:	OpenGL >= 1.2
Requires:	libdrm >= %{libdrm_ver}
%{?with_wayland:Requires:	wayland >= 1.0.0}
%if %{with gallium}
# for egl_gallium.so
Requires:	%{name}-libOpenVG = %{version}-%{release}
Requires:	udev-libs >= 1:150
%endif
%if %{with gbm}
Requires:	%{name}-libgbm = %{version}-%{release}
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
Requires:	%{name}-khrplatform-devel = %{version}-%{release}
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

%package libGL
Summary:	Free Mesa3D implementation of libGL OpenGL library
Summary(pl.UTF-8):	Wolnodostępna implementacja Mesa3D biblioteki libGL ze standardu OpenGL
License:	MIT
Group:		X11/Libraries
Requires:	%{name}-libglapi = %{version}-%{release}
Requires:	libdrm >= %{libdrm_ver}
Provides:	OpenGL = 3.1
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
Provides:	OpenGL-devel = 3.1
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
Provides:	OpenGL-static = 3.1
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
Requires:	%{name}-libglapi = %{version}-%{release}
Provides:	OpenGLES
Provides:	OpenGLESv1 = 1.1
Provides:	OpenGLESv2 = 2.0

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
Requires:	%{name}-khrplatform-devel = %{version}-%{release}
# <EGL/egl.h> for <GLES/egl.h>
Requires:	%{name}-libEGL-devel = %{version}-%{release}
Requires:	%{name}-libGLES = %{version}-%{release}
Provides:	OpenGLES-devel
Provides:	OpenGLESv1-devel = 1.1
Provides:	OpenGLESv2-devel = 2.0

%description libGLES-devel
Header files for Mesa GLES libraries.

%description libGLES-devel -l pl.UTF-8
Pliki nagłówkowe bibliotek Mesa GLES.

%package libOSMesa
Summary:	OSMesa (off-screen renderer) library
Summary(pl.UTF-8):	Biblioteka OSMesa (renderująca bitmapy w pamięci)
License:	MIT
Group:		Libraries

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

%package libOpenCL
Summary:	Mesa implementation of OpenCL (Compuing Language) API
Summary(pl.UTF-8):	Implementacja Mesa API OpenCL (języka obliczeń)
License:	MIT
Group:		Libraries
Requires:	libdrm >= %{libdrm_ver}
Requires:	udev-libs >= 1:150
Provides:	OpenCL = 1.1

%description libOpenCL
This package contains Mesa implementation of OpenCL - standard for
cross-platform, parallel programming of modern processors found in
personal computers, servers and handheld/embedded devices. OpenCL
specification can be found on Khronos Group site:
<http://www.khronos.org/opencl/>. Mesa implements OpenCL 1.1.

%description libOpenCL -l pl.UTF-8
Ten pakiet zawiera implementację Mesa standardu OpenCL - standardu
wieloplatformowego, równoległego programowania nowoczesnych
procesorów, jakie znajdują się w komputerach osobistych, serwerach
oraz urządzeniach przenośnych/wbudowanych. Specyfikację OpenCL można
znaleźć na stronie Khronos Group: <http://www.khronos.org/opencl/>.
Mesa zawiera implementację OpenCL w wersji 1.1.

%package libOpenCL-devel
Summary:	Header files for Mesa OpenCL library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Mesa OpenCL
License:	MIT
Group:		Development/Libraries
Requires:	%{name}-libOpenCL = %{version}-%{release}
Provides:	OpenCL-devel = 1.1

%description libOpenCL-devel
Header files for Mesa OpenCL library.

%description libOpenCL-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Mesa OpenCL.

%package opencl-driver-i915
Summary:	i915 driver for Mesa OpenCL implementation
Summary(pl.UTF-8):	Sterownik i915 dla implementacji Mesa OpenCL
Group:		Libraries
Requires:	%{name}-libOpenCL = %{version}-%{release}

%description opencl-driver-i915
i915 driver for Mesa OpenCL implementation. It supports Intel
915/945/G33/Q33/Q35/Pineview chips.

%description opencl-driver-i915 -l pl.UTF-8
Sterownik i915 dla implementacji Mesa standardu OpenCL. Obsługuje
układy Intela z serii 915/945/G33/Q33/Q35/Pineview.

%package opencl-driver-nouveau
Summary:	nouveau driver for Mesa OpenCL implementation
Summary(pl.UTF-8):	Sterownik nouveau dla implementacji Mesa OpenCL
Group:		Libraries
Requires:	%{name}-libOpenCL = %{version}-%{release}

%description opencl-driver-nouveau
nouveau driver for Mesa OpenCL implementation. It supports NVidia
adapters.

%description opencl-driver-nouveau -l pl.UTF-8
Sterownik nouveau dla implementacji Mesa standardu OpenCL. Obsługuje
karty graficzne firmy NVidia.

%package opencl-driver-r300
Summary:	r300 driver for Mesa OpenCL implementation
Summary(pl.UTF-8):	Sterownik r300 dla implementacji Mesa OpenCL
Group:		Libraries
Requires:	%{name}-libOpenCL = %{version}-%{release}

%description opencl-driver-r300
r300 driver for Mesa OpenCL implementation. It supports ATI Radeon
adapters based on R300/R400/RS690/R500 chips.

%description opencl-driver-r300 -l pl.UTF-8
Sterownik r300 dla implementacji Mesa standardu OpenCL. Obsługuje
karty graficzne ATI Radeon oparte na układach R300/R400/RS690/R500.

%package opencl-driver-r600
Summary:	r600 driver for Mesa OpenCL implementation
Summary(pl.UTF-8):	Sterownik r600 dla implementacji Mesa OpenCL
Group:		Libraries
Requires:	%{name}-libOpenCL = %{version}-%{release}

%description opencl-driver-r600
r600 driver for Mesa OpenCL implementation. It supports ATI Radeon
adapters based on R600/R700 chips.

%description opencl-driver-r600 -l pl.UTF-8
Sterownik r600 dla implementacji Mesa standardu OpenCL. Obsługuje
karty graficzne ATI Radeon oparte na układach R600/R700.

%package opencl-driver-radeonsi
Summary:	radeonsi driver for Mesa OpenCL implementation
Summary(pl.UTF-8):	Sterownik radeonsi dla implementacji Mesa OpenCL
Group:		Libraries
Requires:	%{name}-libOpenCL = %{version}-%{release}

%description opencl-driver-radeonsi
radeonsi driver for Mesa OpenCL implementation. It supports ATI
Radeon adapters based on Southern Islands chips.

%description opencl-driver-radeonsi -l pl.UTF-8
Sterownik radeonsi dla implementacji Mesa standardu OpenCL. Obsługuje
karty graficzne ATI Radeon oparte na układach Southern Islands.

%package opencl-driver-swrast
Summary:	Software (swrast) driver for Mesa OpenCL implementation
Summary(pl.UTF-8):	Sterownik programowy (swrast) dla implementacji Mesa OpenCL
Group:		Libraries
Requires:	%{name}-libOpenCL = %{version}-%{release}

%description opencl-driver-swrast
Software (swrast) driver for Mesa OpenCL implementation.

%description opencl-driver-swrast -l pl.UTF-8
Sterownik programowy (swrast) dla implementacji Mesa standardu OpenCL.

%package opencl-driver-vmwgfx
Summary:	vmwgfx driver for Mesa OpenCL implementation
Summary(pl.UTF-8):	Sterownik vmwgfx dla implementacji Mesa OpenCL
Group:		Libraries
Requires:	%{name}-libOpenCL = %{version}-%{release}

%description opencl-driver-vmwgfx
vmwgfx driver for Mesa OpenCL implementation. It supports VMware
virtual video adapter.

%description opencl-driver-vmwgfx -l pl.UTF-8
Sterownik vmwgfx dla implementacji Mesa standardu OpenCL. Obsługuje
wirtualną kartę graficzną VMware.

%package libOpenVG
Summary:	Mesa implementation of OpenVG (Vector Graphics Accelleration) API
Summary(pl.UTF-8):	Implementacja Mesa API OpenVG (akceleracji grafiki wektorowej)
License:	MIT
Group:		Libraries
Provides:	OpenVG = 1.1

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
Requires:	%{name}-khrplatform-devel = %{version}-%{release}
Requires:	%{name}-libOpenVG = %{version}-%{release}
Provides:	OpenVG-devel = 1.1

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
Requires:	xorg-lib-libXvMC >= 1.0.6
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
Requires:	xorg-lib-libXvMC >= 1.0.6
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
Requires:	xorg-lib-libXvMC >= 1.0.6
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
Requires:	xorg-lib-libXvMC >= 1.0.6
Conflicts:	Mesa-libXvMC

%description libXvMC-softpipe
Mesa softpipe implementation of XvMC API.

%description libXvMC-softpipe -l pl.UTF-8
Implementacja Mesa softpipe API XvMC.

%package libgbm
Summary:	Mesa Graphics Buffer Manager library
Summary(pl.UTF-8):	Biblioteka Mesa Graphics Buffer Manager
Group:		Libraries
Requires:	udev-libs >= 1:150
Conflicts:	Mesa-libEGL < 8.0.1-2

%description libgbm
Mesa Graphics Buffer Manager library.

%description libgbm -l pl.UTF-8
Biblioteka Mesa Graphics Buffer Manager (zarządcy bufora graficznego).

%package libgbm-devel
Summary:	Header file for Mesa Graphics Buffer Manager library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki Mesa Graphics Buffer Manager
Group:		Development/Libraries
Requires:	%{name}-libgbm = %{version}-%{release}
Requires:	udev-devel >= 1:150

%description libgbm-devel
Header file for Mesa Graphics Buffer Manager library.

%description libgbm-devel -l pl.UTF-8
Plik nagłówkowy biblioteki Mesa Graphics Buffer Manager (zarządcy
bufora graficznego).

%package gbm-driver-i915
Summary:	i915 driver for Mesa GBM framework
Summary(pl.UTF-8):	Sterownik i915 dla szkieletu Mesa GBM
Group:		Libraries
Requires:	%{name}-libgbm = %{version}-%{release}

%description gbm-driver-i915
i915 driver for Mesa Graphics Buffer Manager. It supports Intel
915/945/G33/Q33/Q35/Pineview chips.

%description gbm-driver-i915 -l pl.UTF-8
Sterownik i915 dla szkieletu Mesa Graphics Buffer Manager (zarządcy
bufora graficznego). Obsługuje układy Intela z serii
915/945/G33/Q33/Q35/Pineview.

%package gbm-driver-nouveau
Summary:	nouveau driver for Mesa GBM framework
Summary(pl.UTF-8):	Sterownik nouveau dla szkieletu Mesa GBM
Group:		Libraries
Requires:	%{name}-libgbm = %{version}-%{release}

%description gbm-driver-nouveau
nouveau driver for Mesa Graphics Buffer Manager. It supports NVidia
adapters.

%description gbm-driver-nouveau -l pl.UTF-8
Sterownik nouveau dla szkieletu Mesa Graphics Buffer Manager (zarządcy
bufora graficznego). Obsługuje karty graficzne firmy NVidia.

%package gbm-driver-r300
Summary:	r300 driver for Mesa GBM framework
Summary(pl.UTF-8):	Sterownik r300 dla szkieletu Mesa GBM
Group:		Libraries
Requires:	%{name}-libgbm = %{version}-%{release}

%description gbm-driver-r300
r300 driver for Mesa Graphics Buffer Manager. It supports ATI Radeon
adapters based on R300/R400/RS690/R500 chips.

%description gbm-driver-r300 -l pl.UTF-8
Sterownik r300 dla szkieletu Mesa Graphics Buffer Manager (zarządcy
bufora graficznego). Obsługuje karty graficzne ATI Radeon oparte na
układach R300/R400/RS690/R500.

%package gbm-driver-r600
Summary:	r600 driver for Mesa GBM framework
Summary(pl.UTF-8):	Sterownik r600 dla szkieletu Mesa GBM
Group:		Libraries
Requires:	%{name}-libgbm = %{version}-%{release}

%description gbm-driver-r600
r600 driver for Mesa Graphics Buffer Manager. It supports ATI Radeon
adapters based on R600/R700 chips.

%description gbm-driver-r600 -l pl.UTF-8
Sterownik r600 dla szkieletu Mesa Graphics Buffer Manager (zarządcy
bufora graficznego). Obsługuje karty graficzne ATI Radeon oparte na
układach R600/R700.

%package gbm-driver-radeonsi
Summary:	radeonsi driver for Mesa GBM framework
Summary(pl.UTF-8):	Sterownik radeonsi dla szkieletu Mesa GBM
Group:		Libraries
Requires:	%{name}-libgbm = %{version}-%{release}

%description gbm-driver-radeonsi
radeonsi driver for Mesa Graphics Buffer Manager. It supports ATI
Radeon adapters based on Southern Islands chips.

%description gbm-driver-radeonsi -l pl.UTF-8
Sterownik radeonsi dla szkieletu Mesa Graphics Buffer Manager
(zarządcy bufora graficznego). Obsługuje karty graficzne ATI Radeon
oparte na układach Southern Islands.

%package gbm-driver-swrast
Summary:	Software (swrast) driver for Mesa GBM framework
Summary(pl.UTF-8):	Sterownik programowy (swrast) dla szkieletu Mesa GBM
Group:		Libraries
Requires:	%{name}-libgbm = %{version}-%{release}

%description gbm-driver-swrast
Software (swrast) driver for Mesa Graphics Buffer Manager.

%description gbm-driver-swrast -l pl.UTF-8
Sterownik programowy (swrast) dla szkieletu Mesa Graphics Buffer
Manager (zarządcy bufora graficznego).

%package gbm-driver-vmwgfx
Summary:	vmwgfx driver for Mesa GBM framework
Summary(pl.UTF-8):	Sterownik vmwgfx dla szkieletu Mesa GBM
Group:		Libraries
Requires:	%{name}-libgbm = %{version}-%{release}

%description gbm-driver-vmwgfx
vmwgfx driver for Mesa Graphics Buffer Manager. It supports VMware
virtual video adapter.

%description gbm-driver-vmwgfx -l pl.UTF-8
Sterownik vmwgfx dla szkieletu Mesa Graphics Buffer Manager (zarządcy
bufora graficznego). Obsługuje wirtualną kartę graficzną VMware.

%package libglapi
Summary:	Mesa GL API shared library
Summary(pl.UTF-8):	Biblioteka współdzielona Mesa GL API
Group:		Libraries
Conflicts:	Mesa-libEGL < 8.0.1-2

%description libglapi
Mesa GL API shared library, common for various APIs (EGL, GL, GLES).

%description libglapi -l pl.UTF-8
Biblioteka współdzielona Mesa GL API, wspólna dla różnych API (EGL,
GL, GLES).

%package libwayland-egl
Summary:	Wayland EGL library
Summary(pl.UTF-8):	Biblioteka Wayland EGL
Group:		Libraries
Requires:	libdrm >= %{libdrm_ver}

%description libwayland-egl
Wayland EGL platform library.

%description libwayland-egl -l pl.UTF-8
Biblioteka platformy EGL Wayland.

%package libwayland-egl-devel
Summary:	Development files for Wayland EGL library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki Wayland EGL
Group:		Development/Libraries
Requires:	%{name}-libwayland-egl = %{version}-%{release}
Requires:	libdrm-devel >= %{libdrm_ver}

%description libwayland-egl-devel
Development files for Wayland EGL platform library.

%description libwayland-egl-devel -l pl.UTF-8
Pliki programistyczne biblioteki platformy EGL Wayland.

%package libxatracker
Summary:	Xorg Gallium3D accelleration library
Summary(pl.UTF-8):	Biblioteka akceleracji Gallium3D dla Xorg
Group:		X11/Libraries
Requires:	libdrm >= %{libdrm_ver}

%description libxatracker
Xorg Gallium3D accelleration library (used by new vmwgfx driver).

%description libxatracker -l pl.UTF-8
Biblioteka akceleracji Gallium3D dla Xorg (używana przez nowy
sterownik vmwgfx).

%package libxatracker-devel
Summary:	Header files for Xorg Gallium3D accelleration library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki akceleracji Gallium3D dla Xorg
Group:		X11/Development/Libraries
Requires:	%{name}-libxatracker = %{version}-%{release}
Requires:	libdrm-devel >= %{libdrm_ver}

%description libxatracker-devel
Header files for Xorg Gallium3D accelleration library.

%description libxatracker-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki akceleracji Gallium3D dla Xorg.

%package khrplatform-devel
Summary:	Khronos platform header file
Summary(pl.UTF-8):	Plik nagłówkowy platformy Khronos
Group:		Development/Libraries
Conflicts:	Mesa-libEGL-devel < 8.0.1-2

%description khrplatform-devel
Khronos platform header file.

%description khrplatform-devel -l pl.UTF-8
Plik nagłówkowy platformy Khronos.

%package dri-core
Summary:	X.org DRI core library
Summary(pl.UTF-8):	Biblioteka X.org DRI core
License:	MIT
Group:		X11/Libraries
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}

%description dri-core
X.org DRI core library.

%description dri-core -l pl.UTF-8
Biblioteka X.org DRI core.

%package dri-driver-ati-radeon-R100
Summary:	X.org DRI driver for ATI R100 card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart ATI R100
License:	MIT
Group:		X11/Libraries
Requires:	%{name}-dri-core = %{version}-%{release}
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
Requires:	%{name}-dri-core = %{version}-%{release}
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

%package dri-driver-ati-radeon-SI
Summary:	X.org DRI driver for ATI Southern Islands card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart ATI Southern Islands
License:	MIT
Group:		X11/Libraries
Requires:	radeon-ucode
Requires:	xorg-driver-video-ati
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}

%description dri-driver-ati-radeon-SI
X.org DRI driver for ATI Southern Islands card family.

%description dri-driver-ati-radeon-SI -l pl.UTF-8
Sterownik X.org DRI dla rodziny kart ATI Southern Islands.

%package dri-driver-intel-i915
Summary:	X.org DRI driver for Intel i915 card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart Intel i915
License:	MIT
Group:		X11/Libraries
%if %{without gallium_intel}
Requires:	%{name}-dri-core = %{version}-%{release}
%endif
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
Requires:	%{name}-dri-core = %{version}-%{release}
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
Requires:	%{name}-dri-core = %{version}-%{release}
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
Requires:	%{name}-dri-core = %{version}-%{release}
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

%package -n libvdpau-driver-mesa-radeonsi
Summary:	Mesa radeonsi driver for the vdpau API
Summary(pl.UTF-8):	Sterownik Mesa radeonsi dla API vdpau
License:	MIT
Group:		X11/Libraries
Requires:	libdrm >= %{libdrm_ver}
Requires:	libvdpau >= 0.4.1
Conflicts:	libvdpau-driver-mesa

%description -n libvdpau-driver-mesa-radeonsi
Mesa radeonsi driver for the vdpau API. It supports ATI Radeon
adapters based on Southern Islands chips.

%description -n libvdpau-driver-mesa-radeonsi -l pl.UTF-8
Sterownik Mesa radeonsi dla API vdpau. Obsługuje karty ATI Radeon
oparte na układach Southern Islands.

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
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}

dri_drivers="r200 radeon \
%if %{without gallium_intel}
i915 \
%endif
i965
nouveau
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
radeonsi \
%if %{with gallium_nouveau}
nouveau
%endif
"

gallium_drivers=$(echo $gallium_drivers | xargs | tr ' ' ',')

%configure \
	--disable-silent-rules \
	--enable-shared \
	--enable-glx-tls \
	--enable-pic \
	--enable-selinux \
	%{?with_static_libs:--enable-static} \
	%{__enable gbm} \
	--enable-osmesa \
	--enable-shared-glapi \
%if %{with egl}
	--enable-egl \
	--enable-gles1 \
	--enable-gles2 \
	--with-egl-platforms=x11%{?with_gbm:,drm}%{?with_wayland:,wayland} \
%endif
%if %{with gallium}
	--enable-gallium-llvm \
	--with-llvm-shared-libs \ \
	%{__enable egl gallium-egl} \
	%{__enable gbm gallium-gbm} \
	%{?with_opencl:--enable-opencl} \
	%{?with_egl:--enable-openvg} \
	--enable-vdpau \
	%{?with_xa:--enable-xa} \
	--enable-xvmc \
	--with-gallium-drivers=${gallium_drivers} \
%else
	--without-gallium-drivers \
%endif
	--with-dri-drivers=${dri_drivers} \
	--with-dri-driverdir=%{_libdir}/xorg/modules/dri

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# omitted by make install (as of 9.0)
cp -pr include/CL $RPM_BUILD_ROOT%{_includedir}
# strip out undesirable headers
%{__rm} $RPM_BUILD_ROOT%{_includedir}/GL/{vms_x_fix,wglext,wmesa}.h
# dlopened by soname
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libXvMC*.so
# not used externally
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib{dricore%{version},glapi}.so
# dlopened
%{__rm} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/dri/*.la
# not defined by standards; and not needed, there is pkg-config support
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

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

%post	libOSMesa -p /sbin/ldconfig
%postun	libOSMesa -p /sbin/ldconfig

%post	libOpenCL -p /sbin/ldconfig
%postun	libOpenCL -p /sbin/ldconfig

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

%post	libgbm -p /sbin/ldconfig
%postun	libgbm -p /sbin/ldconfig

%post	libglapi -p /sbin/ldconfig
%postun	libglapi -p /sbin/ldconfig

%post	libwayland-egl -p /sbin/ldconfig
%postun	libwayland-egl -p /sbin/ldconfig

%post	libxatracker -p /sbin/ldconfig
%postun	libxatracker -p /sbin/ldconfig

%post	dri-core -p /sbin/ldconfig
%postun	dri-core -p /sbin/ldconfig

%if %{with egl}
%files libEGL
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libEGL.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libEGL.so.1
%if %{with gallium}
%dir %{_libdir}/egl
%attr(755,root,root) %{_libdir}/egl/egl_gallium.so
%endif

%files libEGL-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libEGL.so
%dir %{_includedir}/EGL
%{_includedir}/EGL/egl.h
%{_includedir}/EGL/eglext.h
%{_includedir}/EGL/eglmesaext.h
%{_includedir}/EGL/eglplatform.h
%{_pkgconfigdir}/egl.pc

%if %{with static_libs}
%files libEGL-static
%defattr(644,root,root,755)
%{_libdir}/libEGL.a
%endif
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

%if %{with opencl}
%files libOpenCL
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOpenCL.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libOpenCL.so.1
%dir %{_libdir}/opencl

%files libOpenCL-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOpenCL.so
%{_includedir}/CL

%if %{with gallium_intel}
%files opencl-driver-i915
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/opencl/pipe_i915.so
%endif

%if %{with gallium_nouveau}
%files opencl-driver-nouveau
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/opencl/pipe_nouveau.so
%endif

%files opencl-driver-r300
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/opencl/pipe_r300.so

%files opencl-driver-r600
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/opencl/pipe_r600.so

%files opencl-driver-radeonsi
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/opencl/pipe_radeonsi.so

%files opencl-driver-swrast
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/opencl/pipe_swrast.so

%files opencl-driver-vmwgfx
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/opencl/pipe_vmwgfx.so
%endif

%if %{with egl} && %{with gallium}
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
%if %{with gallium_nouveau}
%files libXvMC-nouveau
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libXvMCnouveau.so.1.0
%attr(755,root,root) %ghost %{_libdir}/libXvMCnouveau.so.1
%endif

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

%if %{with gbm}
%files libgbm
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgbm.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libgbm.so.1
%if %{with gallium}
%dir %{_libdir}/gbm
%attr(755,root,root) %{_libdir}/gbm/gbm_gallium_drm.so
%endif

%files libgbm-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgbm.so
%{_includedir}/gbm.h
%{_pkgconfigdir}/gbm.pc
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

%files gbm-driver-radeonsi
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gbm/pipe_radeonsi.so

%files gbm-driver-swrast
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gbm/pipe_swrast.so

%files gbm-driver-vmwgfx
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gbm/pipe_vmwgfx.so
%endif

%files libglapi
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libglapi.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libglapi.so.0
# libglapi-devel? nothing seems to need it atm.
#%attr(755,root,root) %{_libdir}/libglapi.so

%if %{with wayland}
%files libwayland-egl
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libwayland-egl.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libwayland-egl.so.1

%files libwayland-egl-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libwayland-egl.so
%{_pkgconfigdir}/wayland-egl.pc
%endif

%if %{with xa}
%files libxatracker
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxatracker.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libxatracker.so.1

%files libxatracker-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxatracker.so
%{_includedir}/xa_composite.h
%{_includedir}/xa_context.h
%{_includedir}/xa_tracker.h
%{_pkgconfigdir}/xatracker.pc
%endif

%if %{with egl}
%files khrplatform-devel
%defattr(644,root,root,755)
%dir %{_includedir}/KHR
%{_includedir}/KHR/khrplatform.h
%endif

%files dri-core
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdricore%{version}.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libdricore%{version}.so.1
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/drirc

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
%endif

%files dri-driver-ati-radeon-SI
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/radeonsi_dri.so

%files dri-driver-intel-i915
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/i915_dri.so

%files dri-driver-intel-i965
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/i965_dri.so

%files dri-driver-nouveau
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/nouveau_vieux_dri.so
%if %{with gallium_nouveau}
%attr(755,root,root) %{_libdir}/xorg/modules/dri/nouveau_dri.so
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

%files -n libvdpau-driver-mesa-radeonsi
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_radeonsi.so.1.0
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_radeonsi.so.1
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_radeonsi.so

%files -n libvdpau-driver-mesa-softpipe
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_softpipe.so.1.0
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_softpipe.so.1
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_softpipe.so
%endif
