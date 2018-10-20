#
# TODO:
# - check if gallium_i915 note is still valid, switch the bcond if not
#
# Conditional build:
%bcond_without	gallium		# gallium drivers
%bcond_with	gallium_i915	# gallium i915 Intel driver (instead of plain dri; doesn't work with AIGLX)
%bcond_without	gallium_nouveau	# gallium nouveau driver
%bcond_without	gallium_radeon	# gallium radeon drivers
%bcond_without	egl		# EGL libraries
%bcond_with	openvg		# OpenVG library [not building since 10.4, dropped in 10.6]
%bcond_without	gbm		# Graphics Buffer Manager
%bcond_without	nine		# Nine Direct3D 9+ state tracker (for Wine)
%bcond_without	opencl		# OpenCL support
%bcond_without	ocl_icd		# OpenCL as ICD (installable client driver)
%bcond_with	glvnd		# OpenGL vendor neutral dispatcher support
%bcond_without	omx		# OpenMAX (Bellagio OMXIL) support
%bcond_without	va		# VA library
%bcond_without	wayland		# Wayland EGL
%bcond_without	xa		# XA state tracker (for vmwgfx xorg driver)
%bcond_with	hud_extra	# HUD block/NIC I/O HUD stats support
%bcond_with	lm_sensors	# HUD lm_sensors support
%bcond_with	texture_float	# floating-point textures and renderbuffers (SGI patent in US)
%bcond_with	static_libs	# static libraries [not supported for DRI, thus broken currently]
%bcond_with	tests		# tests
%bcond_without	shared_llvm	# disable use of the shared LLVM libs
%bcond_without	radv		# disable build of the radeon Vulkan driver
#
# glapi version (glapi tables in dri drivers and libglx must be in sync);
# set to current Mesa version on ABI break, when xserver tables get regenerated
# (until they start to be somehow versioned themselves)
%define		glapi_ver		7.1.0
# minimal supported xserver version
%define		xserver_ver		1.5.0
# other packages
%define		libdrm_ver		2.4.92
%define		dri2proto_ver		2.8
%define		dri3proto_ver		1.0
%define		glproto_ver		1.4.14
%define		presentproto_ver	1.0
%define		zlib_ver		1.2.8
%define		wayland_ver		1.11

%if %{without gallium}
%undefine	with_gallium_i915
%undefine	with_gallium_nouveau
%undefine	with_gallium_radeon
%undefine	with_nine
%undefine	with_ocl_icd
%undefine	with_omx
%undefine	with_opencl
%undefine	with_xa
%endif

%if %{without egl}
%undefine	with_gbm
%undefine	with_wayland
%endif

Summary:	Free OpenGL implementation
Summary(pl.UTF-8):	Wolnodostępna implementacja standardu OpenGL
Name:		Mesa
Version:	18.2.3
Release:	1
License:	MIT (core) and others - see license.html file
Group:		X11/Libraries
#Source0:	ftp://ftp.freedesktop.org/pub/mesa/mesa-%{version}.tar.xz
# https://bugs.freedesktop.org/show_bug.cgi?id=107865
Source0:	https://gitlab.freedesktop.org/mesa/mesa/-/archive/mesa-%{version}/mesa-mesa-%{version}.tar.bz2
# Source0-md5:	68f253f5825ee9ebac2f5506d364e114
Patch0:		%{name}-link.patch
URL:		http://www.mesa3d.org/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
%{?with_opencl:BuildRequires:	clang-devel >= 3.1}
BuildRequires:	elfutils-devel
BuildRequires:	expat-devel >= 1.95
BuildRequires:	gcc >= 6:4.2.0
%{?with_nine:BuildRequires:	gcc-c++ >= 6:4.6}
%{?with_opencl:BuildRequires:	gcc-c++ >= 6:4.7}
BuildRequires:	libdrm-devel >= %{libdrm_ver}
%{?with_glvnd:BuildRequires:	libglvnd-devel >= 0.2.0}
BuildRequires:	libselinux-devel
BuildRequires:	libstdc++-devel >= 6:4.2.0
BuildRequires:	libtalloc-devel >= 2:2.0.1
BuildRequires:	libtool >= 2:2.2
%{?with_va:BuildRequires:	libva-devel >= 1.6.0}
%{?with_va:BuildRequires:	pkgconfig(libva) >= 0.39.0}
BuildRequires:	libvdpau-devel >= 1.1
BuildRequires:	libxcb-devel >= 1.13
# gallium core requires 3.3.0, OpenCL/r600 require 3.9.0, swr/radeonsi/radv 4.0.0
%{?with_gallium:BuildRequires:	llvm-devel >= 5.0}
%{?with_radv:BuildRequires:	llvm-devel >= 5.0}
%{?with_opencl:BuildRequires:	llvm-libclc}
# for SHA1 (could use also libmd/libsha1/libgcrypt/openssl instead)
BuildRequires:	nettle-devel
%{?with_ocl_icd:BuildRequires:	ocl-icd-devel}
%{?with_omx:BuildRequires:	libomxil-bellagio-devel}
BuildRequires:	perl-base
BuildRequires:	pixman-devel
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(talloc) >= 2.0.1
BuildRequires:	pkgconfig(xcb-dri2) >= 1.8
BuildRequires:	pkgconfig(xcb-dri3) >= 1.13
BuildRequires:	pkgconfig(xcb-glx) >= 1.8.1
BuildRequires:	pkgconfig(xcb-present) >= 1.13
BuildRequires:	python >= 2
BuildRequires:	python-Mako >= 0.8.0
BuildRequires:	python-modules >= 2
BuildRequires:	rpmbuild(macros) >= 1.470
BuildRequires:	sed >= 4.0
# wayland-{client,server}
%{?with_wayland:BuildRequires:	wayland-devel >= %{wayland_ver}}
%{?with_wayland:BuildRequires:	wayland-protocols >= 1.8}
%{?with_wayland:BuildRequires:	wayland-egl-devel >= %{wayland_ver}}
BuildRequires:	xorg-lib-libXdamage-devel >= 1.1
BuildRequires:	xorg-lib-libXext-devel >= 1.0.5
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	xorg-lib-libXvMC-devel >= 1.0.6
BuildRequires:	xorg-lib-libXxf86vm-devel
BuildRequires:	xorg-lib-libxshmfence-devel >= 1.1
BuildRequires:	xorg-proto-dri2proto-devel >= %{dri2proto_ver}
BuildRequires:	xorg-proto-dri3proto-devel >= %{dri3proto_ver}
BuildRequires:	xorg-proto-glproto-devel >= %{glproto_ver}
BuildRequires:	xorg-proto-presentproto-devel >= %{presentproto_ver}
BuildRequires:	xorg-util-makedepend
%if %{with gallium}
%{?with_lm_sensors:BuildRequires:	lm_sensors-devel >= 4.0}
BuildRequires:	xorg-proto-xextproto-devel >= 7.0.99.1
BuildRequires:	xorg-xserver-server-devel >= %{xserver_ver}
%endif
BuildRequires:	zlib-devel >= %{zlib_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# libGLESv1_CM, libGLESv2, libGL, libOSMesa:
#  _glapi_tls_Dispatch is defined in libglapi, but it's some kind of symbol ldd -r doesn't notice(?)
# libgbm: circular dependency with libEGL (wayland_buffer_is_drm symbol)
%define		skip_post_check_so      libGLESv1_CM.so.1.* libGLESv2.so.2.* libGL.so.1.* libOSMesa.so.* libgbm.*.so.* libGLX_mesa.so.0.*

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
Requires:	libxcb >= 1.13
%{?with_wayland:Requires:	wayland >= 1.11.0}
%if %{with gbm}
Requires:	%{name}-libgbm = %{version}-%{release}
%endif
Provides:	EGL = 1.5

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
Requires:	xorg-lib-libXdamage-devel >= 1.1
Requires:	xorg-lib-libXext-devel >= 1.0.5
Requires:	xorg-lib-libXfixes-devel
Requires:	xorg-lib-libXxf86vm-devel
Requires:	xorg-proto-dri2proto-devel >= %{dri2proto_ver}
Requires:	xorg-proto-glproto-devel >= %{glproto_ver}
Provides:	EGL-devel = 1.5

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
Provides:	EGL-static = 1.5

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
Requires:	libxcb >= 1.13
Requires:	xorg-lib-libXdamage >= 1.1
Provides:	OpenGL = 4.5
Provides:	OpenGL-GLX = 1.4
Obsoletes:	Mesa
Obsoletes:	Mesa-dri
Obsoletes:	Mesa-dri-core < 10.0.0
Obsoletes:	X11-OpenGL-libGL < 1:7.0.0
Obsoletes:	XFree86-OpenGL-libGL < 1:7.0.0

%description libGL
Mesa is a 3-D graphics library with an API which is very similar to
that of OpenGL(R). To the extent that Mesa utilizes the OpenGL command
syntax or state machine, it is being used with authorization from
Silicon Graphics, Inc. However, the author does not possess an OpenGL
license from SGI, and makes no claim that Mesa is in any way a
compatible replacement for OpenGL or associated with SGI.

This package contains libGL which implements OpenGL 4.5 and GLX 1.4
specifications. It uses DRI for rendering.

%description libGL -l pl.UTF-8
Mesa jest biblioteką grafiki 3D z API bardzo podobnym do OpenGL(R). Do
tego stopnia, że Mesa używa składni i automatu OpenGL jest używana z
autoryzacją Silicon Graphics, Inc. Jednak autor nie posiada licencji
OpenGL od SGI i nie twierdzi, że Mesa jest kompatybilnym zamiennikiem
OpenGL ani powiązana z SGI.

Ten pakiet zawiera libGL implementującą specyfikacje OpenGL 4.5 oraz
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
Requires:	xorg-lib-libXdamage-devel >= 1.1
Requires:	xorg-lib-libXext-devel >= 1.0.5
Requires:	xorg-lib-libXxf86vm-devel
Requires:	xorg-proto-dri2proto-devel >= %{dri2proto_ver}
Requires:	xorg-proto-glproto-devel >= %{glproto_ver}
Suggests:	OpenGL-doc-man
Provides:	OpenGL-GLX-devel = 1.4
Provides:	OpenGL-devel = 4.5
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
Provides:	OpenGL-static = 4.5
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
Provides:	OpenGLESv3 = 3.2

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
Provides:	OpenGLESv3-devel = 3.2

%description libGLES-devel
Header files for Mesa GLES libraries.

%description libGLES-devel -l pl.UTF-8
Pliki nagłówkowe bibliotek Mesa GLES.

%package libOSMesa
Summary:	OSMesa (off-screen renderer) library
Summary(pl.UTF-8):	Biblioteka OSMesa (renderująca bitmapy w pamięci)
License:	MIT
Group:		Libraries
Requires:	zlib >= %{zlib_ver}

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

%package OpenCL-icd
Summary:	Mesa implementation of OpenCL (Compuing Language) API ICD
Summary(pl.UTF-8):	Implementacja Mesa API OpenCL (języka obliczeń) ICD
License:	MIT
Group:		Libraries
Requires:	filesystem >= 4.0-29
Requires:	libdrm >= %{libdrm_ver}
Requires:	llvm-libclc
Requires:	zlib >= %{zlib_ver}
Provides:	OpenCL = 1.1
Provides:	ocl-icd-driver

%description OpenCL-icd
This package contains Mesa implementation of OpenCL - standard for
cross-platform, parallel programming of modern processors found in
personal computers, servers and handheld/embedded devices. OpenCL
specification can be found on Khronos Group site:
<http://www.khronos.org/opencl/>. Mesa implements OpenCL 1.1.

The implementation is provided as an installable client driver (ICD)
for use with the ocl-icd loader.

%description OpenCL-icd -l pl.UTF-8
Ten pakiet zawiera implementację Mesa standardu OpenCL - standardu
wieloplatformowego, równoległego programowania nowoczesnych
procesorów, jakie znajdują się w komputerach osobistych, serwerach
oraz urządzeniach przenośnych/wbudowanych. Specyfikację OpenCL można
znaleźć na stronie Khronos Group: <http://www.khronos.org/opencl/>.
Mesa zawiera implementację OpenCL w wersji 1.1.

Implementacja dostarczona jest w postaci instalowalnego sterownika klienta
(ICD), który może być użyty z loaderem ocl-icd.

%package libOpenCL
Summary:	Mesa implementation of OpenCL (Compuing Language) API
Summary(pl.UTF-8):	Implementacja Mesa API OpenCL (języka obliczeń)
License:	MIT
Group:		Libraries
Requires:	libdrm >= %{libdrm_ver}
Requires:	llvm-libclc
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
Provides:	OpenCL-devel = 1.2

%description libOpenCL-devel
Header files for Mesa OpenCL library.

%description libOpenCL-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Mesa OpenCL.

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
Requires:	zlib >= %{zlib_ver}
Conflicts:	Mesa-libXvMC

%description libXvMC-nouveau
Mesa implementation of XvMC API for NVidia adapters (NV40-NV96, NVa0).

%description libXvMC-nouveau -l pl.UTF-8
Implementacja Mesa API XvMC dla kart NVidia (NV40-NV96, NVa0).

%package libXvMC-r600
Summary:	Mesa implementation of XvMC API for ATI Radeon R600 series adapters
Summary(pl.UTF-8):	Implementacja Mesa API XvMC dla kart ATI Radeon z serii R600
License:	MIT
Group:		Libraries
Requires:	libdrm >= %{libdrm_ver}
Requires:	xorg-lib-libXvMC >= 1.0.6
Requires:	zlib >= %{zlib_ver}
Conflicts:	Mesa-libXvMC

%description libXvMC-r600
Mesa implementation of XvMC API for ATI Radeon adapters based on
R600/R700 chips.

%description libXvMC-r600 -l pl.UTF-8
Implementacja Mesa API XvMC dla kart ATI Radeon opartych na układach
R600/R700.

%package -n libva-driver-gallium
Summary:	VA driver for Gallium State Tracker
Summary(pl.UTF-8):	Sterowniki VA do Gallium
Group:		Libraries
%if %{with gallium_radeon}
Requires:	libva-driver-r600
Requires:	libva-driver-radeonsi
%endif
%if %{with gallium_nouveau}
Requires:	libva-driver-nouveau
%endif

%description -n libva-driver-gallium
VA drivers for Gallium State Tracker (r600, radeonsi & nouveau).

%description -n libva-driver-gallium -l pl.UTF-8
Sterowniki VA do Gallium (r600, radeonsi & nouveau).

%package -n libva-driver-r600
Summary:	VA driver for ATI Radeon R600 series adapters
Summary(pl.UTF-8):	Sterownik VA dla kart ATI Radeon z serii R600
Group:		Libraries
Requires:	libva >= 1.6.0
Requires:	zlib >= %{zlib_ver}

%description -n libva-driver-r600
VA driver for ATI Radeon R600 series adapters.

%description -n libva-driver-r600 -l pl.UTF-8
Sterownik VA dla kart ATI Radeon z serii R600.

%package -n libva-driver-radeonsi
Summary:	VA driver for ATI Radeon SI adapters
Summary(pl.UTF-8):	Sterownik VA dla kart ATI Radeon SI
Group:		Libraries
Requires:	libva >= 1.6.0
Requires:	zlib >= %{zlib_ver}

%description -n libva-driver-radeonsi
VA driver for ATI Radeon adapters based on Southern Islands chips.

%description -n libva-driver-radeonsi -l pl.UTF-8
Sterownik VA dla kart ATI Radeon opartych na układach Southern
Islands.

%package -n libva-driver-nouveau
Summary:	VA driver for NVidia adapters
Summary(pl.UTF-8):	Sterownik VA dla kart NVidia
Group:		Libraries
Requires:	libva >= 1.6.0
Requires:	zlib >= %{zlib_ver}

%description -n libva-driver-nouveau
VA driver for NVidia adapters.

%description -n libva-driver-nouveau -l pl.UTF-8
Sterownik VA dla kart NVidia.

%package libgbm
Summary:	Mesa Graphics Buffer Manager library
Summary(pl.UTF-8):	Biblioteka Mesa Graphics Buffer Manager
Group:		Libraries
Requires:	%{name}-libglapi = %{version}-%{release}
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

%description libgbm-devel
Header file for Mesa Graphics Buffer Manager library.

%description libgbm-devel -l pl.UTF-8
Plik nagłówkowy biblioteki Mesa Graphics Buffer Manager (zarządcy
bufora graficznego).

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

%package libxatracker
Summary:	Xorg Gallium3D accelleration library
Summary(pl.UTF-8):	Biblioteka akceleracji Gallium3D dla Xorg
Group:		X11/Libraries
Requires:	libdrm >= %{libdrm_ver}
Requires:	zlib >= %{zlib_ver}

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

%package dri-driver-ati-radeon-R100
Summary:	X.org DRI driver for ATI R100 card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart ATI R100
License:	MIT
Group:		X11/Libraries
Requires:	xorg-driver-video-ati
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}
Requires:	zlib >= %{zlib_ver}
Obsoletes:	X11-driver-radeon-dri < 1:7.0.0

%description dri-driver-ati-radeon-R100
X.org DRI driver for ATI R100 card family (Radeon 7000-7500). It
supports R100, RV100, RS100, RV200, RS200, RS250.

%description dri-driver-ati-radeon-R100 -l pl.UTF-8
Sterownik X.org DRI dla rodziny kart ATI R100 (Radeon 7000-7500).
Obsługuje układy R100, RV100, RS100, RV200, RS200, RS250.

%package dri-driver-ati-radeon-R200
Summary:	X.org DRI driver for ATI R200 card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart ATI R200
License:	MIT
Group:		X11/Libraries
Requires:	xorg-driver-video-ati
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}
Requires:	zlib >= %{zlib_ver}
Obsoletes:	X11-driver-radeon-dri < 1:7.0.0

%description dri-driver-ati-radeon-R200
X.org DRI driver for ATI R200 card family (Radeon 8500-92xx). It
supports R200, RV250, RV280, RS300, RS350 chips.

%description dri-driver-ati-radeon-R200 -l pl.UTF-8
Sterownik X.org DRI dla rodziny kart ATI R200 (Radeon 8500-92xx).
Obsługuje układy R200, RV250, RV280, RS300, RS350.

%package dri-driver-ati-radeon-R300
Summary:	X.org DRI driver for ATI R300 card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart ATI R300
License:	MIT
Group:		X11/Libraries
Requires:	xorg-driver-video-ati
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}
Requires:	zlib >= %{zlib_ver}
Obsoletes:	X11-driver-radeon-dri < 1:7.0.0

%description dri-driver-ati-radeon-R300
X.org Gallium DRI driver for ATI R300/R400/RS690/R500 card family
(Radeon 9600-9800, X300-X2300). It supports R300, R350, R360, RV350,
RV370, RV380, R420, R423, R430, R480, R481, RV410, RS400, RC410,
RS480, RS482, R520, RV515, RV530, RV560, RV570, R580, RS600, RS690,
RS740 chips.

%description dri-driver-ati-radeon-R300 -l pl.UTF-8
Sterownik X.org DRI Gallium dla rodziny kart ATI R300/R400/RS690/R500
(Radeon 9600-9800, X300-X2300). Obsługuje układy R300, R350, R360,
RV350, RV370, RV380, R420, R423, R430, R480, R481, RV410, RS400,
RC410, RS480, RS482, R520, RV515, RV530, RV560, RV570, R580, RS600,
RS690, RS740.

%package dri-driver-ati-radeon-R600
Summary:	X.org DRI driver for ATI R600 card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart ATI R600
License:	MIT
Group:		X11/Libraries
Requires:	radeon-ucode
Requires:	xorg-driver-video-ati
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}
Requires:	zlib >= %{zlib_ver}

%description dri-driver-ati-radeon-R600
X.org Gallium DRI driver for ATI R600/R700 card family (Radeon HD
2400-7000). It supports R600, RV610, RV630, RV670, RV620, RV635,
RS780, RS880, RV770, RV730, RV710, RV740, CEDAR, REDWOOD, JUNIPER,
CYPRESS, HEMLOCK, PALM, SUMO/SUMO2, CAYMAN, BARTS, TURKS, CAICOS,
ARUBA chips.

%description dri-driver-ati-radeon-R600 -l pl.UTF-8
Sterownik X.org DRI Gallium dla rodziny kart ATI R600/R700 (Radeon HD
2400-7000). Obsługuje układy R600, RV610, RV630, RV670, RV620, RV635,
RS780, RS880, RV770, RV730, RV710, RV740, CEDAR, REDWOOD, JUNIPER,
CYPRESS, HEMLOCK, PALM, SUMO/SUMO2, CAYMAN, BARTS, TURKS, CAICOS,
ARUBA.

%package dri-driver-ati-radeon-SI
Summary:	X.org DRI driver for ATI Southern Islands card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart ATI Southern Islands
License:	MIT
Group:		X11/Libraries
Requires:	radeon-ucode
Requires:	xorg-driver-video-ati
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}
Requires:	zlib >= %{zlib_ver}

%description dri-driver-ati-radeon-SI
X.org Gallium DRI driver for ATI Southern Islands card family (Radeon
HD 7700-8000, R9, APU). It supports TAHITI, PITCAIRN, VERDE, OLAND,
HAINAN, BONAIRE, KABINI, MULLINS, KAVERI, HAWAII, ICELAND, TONGA,
CARRIZO, FIJI, POLARIS, STONEY chips.

%description dri-driver-ati-radeon-SI -l pl.UTF-8
Sterownik X.org DRI Gallium dla rodziny kart ATI Southern Islands
(Radeon HD 7700-8000, R9, APU). Obsługuje układy TAHITI, PITCAIRN,
VERDE, OLAND, HAINAN, BONAIRE, KABINI, MULLINS, KAVERI, HAWAII,
ICELAND, TONGA, CARRIZO, FIJI, POLARIS, STONEY.

%package dri-driver-etnaviv
Summary:	X.org DRI driver for Vivante 3D chips
Summary(pl.UTF-8):	Sterownik X.org DRI dla układów Vivante 3D
License:	MIT
Group:		X11/Libraries
#Requires:	xorg-driver-video-?
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}
Requires:	zlib >= %{zlib_ver}

%description dri-driver-etnaviv
X.org DRI driver for Vivante 3D chips.

%description dri-driver-etnaviv -l pl.UTF-8
Sterownik X.org DRI dla układów Vivante 3D.

%package dri-driver-freedreno
Summary:	X.org DRI driver for Adreno chips
Summary(pl.UTF-8):	Sterownik X.org DRI dla układów Adreno
License:	MIT
Group:		X11/Libraries
Requires:	xorg-driver-video-freedreno
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}
Requires:	zlib >= %{zlib_ver}

%description dri-driver-freedreno
X.org DRI driver for Adreno chips.

%description dri-driver-freedreno -l pl.UTF-8
Sterownik X.org DRI dla układów Adreno.

%package dri-driver-intel-i915
Summary:	X.org DRI driver for Intel i915 card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart Intel i915
License:	MIT
Group:		X11/Libraries
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}
Requires:	zlib >= %{zlib_ver}
Obsoletes:	Mesa-dri-driver-intel-i830
Obsoletes:	X11-driver-i810-dri < 1:7.0.0

%description dri-driver-intel-i915
X.org DRI driver for Intel i915 card family (830, 845, 852/855, 865,
915, 945, G33, Q33, Q35, Pineview).

%description dri-driver-intel-i915 -l pl.UTF-8
Sterownik X.org DRI dla rodziny kart Intel i915 (830, 845, 852/855,
865, 915, 945, G33, Q33, Q35, Pineview).

%package dri-driver-intel-i965
Summary:	X.org DRI driver for Intel i965 card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart Intel i965
License:	MIT
Group:		X11/Libraries
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}
Requires:	zlib >= %{zlib_ver}
Obsoletes:	Mesa-dri-driver-intel-i830
Obsoletes:	X11-driver-i810-dri < 1:7.0.0

%description dri-driver-intel-i965
X.org (non-Gallium) DRI driver for Intel i965 card family (946GZ,
965G, 965Q, 965GM, 965GME, GM45, G41, B43, Q45/Q43, G45/G43, Ironlake,
Sandybridge, Ivybridge, Haswell, Ray Trail, Broadwell, Cherrytrail,
Braswell, Cherryview, Skylake, Broxton, Kabylake, Geminilake);

%description dri-driver-intel-i965 -l pl.UTF-8
Sterownik X.org DRI (nie Gallium) dla rodziny kart Intel i965 (946GZ,
965G, 965Q, 965GM, 965GME, GM45, G41, B43, Q45/Q43, G45/G43, Ironlake,
Sandybridge, Ivybridge, Haswell, Ray Trail, Broadwell, Cherrytrail,
Braswell, Cherryview, Skylake, Broxton, Kabylake, Geminilake);

%package dri-driver-nouveau
Summary:	X.org DRI driver for NVIDIA card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart NVIDIA
License:	MIT
Group:		X11/Libraries
Requires:	xorg-driver-video-nouveau
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}
Requires:	zlib >= %{zlib_ver}

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
Requires:	zlib >= %{zlib_ver}

%description dri-driver-swrast
X.org DRI software rasterizer driver.

%description dri-driver-swrast -l pl.UTF-8
Sterownik X.org DRI obsługujący rysowanie programowe.

%package dri-driver-vc4
Summary:	X.org DRI driver for Broadcom VC4 chips
Summary(pl.UTF-8):	Sterownik X.org DRI dla układów Broadcom VC4
License:	MIT
Group:		X11/Libraries
Requires:	xorg-driver-video-modesetting
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}
Requires:	zlib >= %{zlib_ver}

%description dri-driver-vc4
X.org DRI driver for Broadcom VC4 chips.

%description dri-driver-vc4 -l pl.UTF-8
Sterownik X.org DRI dla układów Broadcom VC4.

%package dri-driver-virgl
Summary:	X.org DRI driver for QEMU VirGL
Summary(pl.UTF-8):	Sterownik X.org DRI dla QEMU VirGL
License:	MIT
Group:		X11/Libraries
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}
Requires:	zlib >= %{zlib_ver}

%description dri-driver-virgl
X.org DRI driver for QEMU VirGL.

%description dri-driver-virgl -l pl.UTF-8
Sterownik X.org DRI dla QEMU VirGL.

%package dri-driver-vmwgfx
Summary:	X.org DRI driver for VMware
Summary(pl.UTF-8):	Sterownik X.org DRI dla VMware
License:	MIT
Group:		X11/Libraries
Requires:	xorg-driver-video-vmware
Requires:	xorg-xserver-libglx(glapi) = %{glapi_ver}
Requires:	xorg-xserver-server >= %{xserver_ver}
Requires:	zlib >= %{zlib_ver}

%description dri-driver-vmwgfx
X.org DRI driver for VMWare.

%description dri-driver-vmwgfx -l pl.UTF-8
Sterownik X.org DRI dla VMware.

%package pipe-driver-i915
Summary:	i915 driver for Mesa Gallium dynamic pipe loader
Summary(pl.UTF-8):	Sterownik i915 dla dynamicznego systemu potoków szkieletu Mesa Gallium
Group:		Libraries
Requires:	zlib >= %{zlib_ver}
Obsoletes:	Mesa-gbm-driver-i915
Obsoletes:	Mesa-opencl-driver-i915

%description pipe-driver-i915
i915 driver for Mesa Gallium dynamic pipe loader. It supports Intel
915/945/G33/Q33/Q35/Pineview chips.

%description pipe-driver-i915 -l pl.UTF-8
Sterownik i915 dla dynamicznego systemu potoków szkieletu Mesa
Gallium. Obsługuje układy Intela z serii 915/945/G33/Q33/Q35/Pineview.

%package pipe-driver-msm
Summary:	msm (freedreno) driver for Mesa Gallium dynamic pipe loader
Summary(pl.UTF-8):	Sterownik msm (freedreno) dla dynamicznego systemu potoków szkieletu Mesa Gallium
Group:		Libraries
Requires:	zlib >= %{zlib_ver}

%description pipe-driver-msm
msm (freedreno) driver for Mesa Gallium dynamic pipe loader. It
supports Adreno chips.

%description pipe-driver-msm -l pl.UTF-8
Sterownik msm (freedreno) dla dynamicznego systemu potoków szkieletu
Mesa Gallium. Obsługuje układy Adreno.

%package pipe-driver-nouveau
Summary:	nouveau driver for Mesa Gallium dynamic pipe loader
Summary(pl.UTF-8):	Sterownik nouveau dla dynamicznego systemu potoków szkieletu Mesa Gallium
Group:		Libraries
Requires:	zlib >= %{zlib_ver}
Obsoletes:	Mesa-gbm-driver-nouveau
Obsoletes:	Mesa-opencl-driver-nouveau

%description pipe-driver-nouveau
nouveau driver for Mesa Gallium dynamic pipe loader. It supports
NVidia adapters.

%description pipe-driver-nouveau -l pl.UTF-8
Sterownik nouveau dla dynamicznego systemu potoków szkieletu Mesa
Gallium. Obsługuje karty graficzne firmy NVidia.

%package pipe-driver-r300
Summary:	r300 driver for Mesa Gallium dynamic pipe loader
Summary(pl.UTF-8):	Sterownik r300 dla dynamicznego systemu potoków szkieletu Mesa Gallium
Group:		Libraries
Requires:	zlib >= %{zlib_ver}
Obsoletes:	Mesa-gbm-driver-r300
Obsoletes:	Mesa-opencl-driver-r300

%description pipe-driver-r300
r300 driver for Mesa Gallium dynamic pipe loader. It supports ATI
Radeon adapters based on R300/R400/RS690/R500 chips.

%description pipe-driver-r300 -l pl.UTF-8
Sterownik r300 dla dynamicznego systemu potoków szkieletu Mesa
Gallium. Obsługuje karty graficzne ATI Radeon oparte na układach
R300/R400/RS690/R500.

%package pipe-driver-r600
Summary:	r600 driver for Mesa Gallium dynamic pipe loader
Summary(pl.UTF-8):	Sterownik r600 dla dynamicznego systemu potoków szkieletu Mesa Gallium
Group:		Libraries
Requires:	zlib >= %{zlib_ver}
Obsoletes:	Mesa-gbm-driver-r600
Obsoletes:	Mesa-libllvmradeon
Obsoletes:	Mesa-opencl-driver-r600

%description pipe-driver-r600
r600 driver for Mesa Gallium dynamic pipe loader. It supports ATI
Radeon adapters based on R600/R700 chips.

%description pipe-driver-r600 -l pl.UTF-8
Sterownik r600 dla dynamicznego systemu potoków szkieletu Mesa
Gallium. Obsługuje karty graficzne ATI Radeon oparte na układach
R600/R700.

%package pipe-driver-radeonsi
Summary:	radeonsi driver for Mesa Gallium dynamic pipe loader
Summary(pl.UTF-8):	Sterownik radeonsi dla dynamicznego systemu potoków szkieletu Mesa Gallium
Group:		Libraries
Requires:	zlib >= %{zlib_ver}
Obsoletes:	Mesa-gbm-driver-radeonsi
Obsoletes:	Mesa-libllvmradeon
Obsoletes:	Mesa-opencl-driver-radeonsi

%description pipe-driver-radeonsi
radeonsi driver for Mesa Gallium dynamic pipe loader. It supports ATI
Radeon adapters based on Southern Islands chips.

%description pipe-driver-radeonsi -l pl.UTF-8
Sterownik radeonsi dla dynamicznego systemu potoków szkieletu Mesa
Gallium. Obsługuje karty graficzne ATI Radeon oparte na układach
Southern Islands.

%package pipe-driver-swrast
Summary:	Software (swrast) driver for Mesa Gallium dynamic pipe loader
Summary(pl.UTF-8):	Sterownik programowy (swrast) dla dynamicznego systemu potoków szkieletu Mesa Gallium
Group:		Libraries
Requires:	zlib >= %{zlib_ver}
Obsoletes:	Mesa-gbm-driver-swrast
Obsoletes:	Mesa-opencl-driver-swrast

%description pipe-driver-swrast
Software (swrast) driver for Mesa Gallium dynamic pipe loader.

%description pipe-driver-swrast -l pl.UTF-8
Sterownik programowy (swrast) dla dynamicznego systemu potoków
szkieletu Mesa Gallium.

%package pipe-driver-vmwgfx
Summary:	vmwgfx driver for Mesa Gallium dynamic pipe loader
Summary(pl.UTF-8):	Sterownik vmwgfx dla dynamicznego systemu potoków szkieletu Mesa Gallium
Group:		Libraries
Requires:	zlib >= %{zlib_ver}
Obsoletes:	Mesa-gbm-driver-vmwgfx
Obsoletes:	Mesa-opencl-driver-vmwgfx

%description pipe-driver-vmwgfx
vmwgfx driver for Mesa Gallium dynamic pipe loader. It supports VMware
virtual video adapter.

%description pipe-driver-vmwgfx -l pl.UTF-8
Sterownik vmwgfx dla dynamicznego systemu potoków szkieletu Mesa
Gallium. Obsługuje wirtualną kartę graficzną VMware.

%package swr
Summary:	OpenSWR software rasterizer modules for Mesa
Summary(pl.UTF-8):	Moduły programowego rasteryzera OpenSWR dla Mesy
Group:		Libraries
Requires:	cpuinfo(avx)
Requires:	zlib >= %{zlib_ver}

%description swr
OpenSWR software rasterizer modules for Mesa, utilizing x86 AVX or
VX2 instruction sets. They can be loaded by swrast pipe driver or
OSMesa library.

%description swr -l pl.UTF-8
Moduły programowego rasteryzera OpenSWR dla Mesy, wykorzystujące
zestawy instrukcji x86 AVX lub AVX2. Mogą być wczytywane przez
sterownik potoków swrast lub bibliotekę OSMesa.

%package d3d
Summary:	Nine Direct3D9 driver (for Wine)
Summary(pl.UTF-8):	Sterownik Direct3D9 Nine (dla Wine)
Group:		Libraries
Requires:	libdrm >= %{libdrm_ver}
Requires:	zlib >= %{zlib_ver}

%description d3d
Nine Direct3D9 driver (for Wine).

%description d3d -l pl.UTF-8
Sterownik Direct3D9 Nine (dla Wine).

%package d3d-devel
Summary:	Nine Direct3D9 driver API
Summary(pl.UTF-8):	API sterownika Direct3D9 Nine
Group:		Development/Libraries
Requires:	libdrm-devel >= %{libdrm_ver}

%description d3d-devel
Nine Direct3D9 driver API.

%description d3d-devel -l pl.UTF-8
API sterownika Direct3D9 Nine.

%package -n libvdpau-driver-mesa-nouveau
Summary:	Mesa nouveau driver for the vdpau API
Summary(pl.UTF-8):	Sterownik Mesa nouveau dla API vdpau
License:	MIT
Group:		X11/Libraries
Requires:	libdrm >= %{libdrm_ver}
Requires:	libvdpau >= 1.1
Requires:	zlib >= %{zlib_ver}
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
Requires:	libvdpau >= 1.1
Requires:	zlib >= %{zlib_ver}
Conflicts:	libvdpau-driver-mesa

%description -n libvdpau-driver-mesa-r300
Mesa r300 driver for the vdpau API. It supports ATI Radeon adapters
based on R300 chips.

%description -n libvdpau-driver-mesa-r300 -l pl.UTF-8
Sterownik Mesa r300 dla API vdpau. Obsługuje karty ATI Radeon oparte
na układach R300.

%package -n libvdpau-driver-mesa-r600
Summary:	Mesa r600 driver for the vdpau API
Summary(pl.UTF-8):	Sterownik Mesa r600 dla API vdpau
License:	MIT
Group:		X11/Libraries
Requires:	libdrm >= %{libdrm_ver}
Requires:	libvdpau >= 1.1
Requires:	zlib >= %{zlib_ver}
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
Requires:	libvdpau >= 1.1
Requires:	zlib >= %{zlib_ver}
Conflicts:	libvdpau-driver-mesa
Obsoletes:	Mesa-libllvmradeon

%description -n libvdpau-driver-mesa-radeonsi
Mesa radeonsi driver for the vdpau API. It supports ATI Radeon
adapters based on Southern Islands chips.

%description -n libvdpau-driver-mesa-radeonsi -l pl.UTF-8
Sterownik Mesa radeonsi dla API vdpau. Obsługuje karty ATI Radeon
oparte na układach Southern Islands.

%package -n omxil-mesa
Summary:	Mesa driver for Bellagio OpenMAX IL API
Summary(pl.UTF-8):	Sterownik Mesa nouveau dla API Bellagio OpenMAX IL
License:	MIT
Group:		X11/Libraries
Requires:	libdrm >= %{libdrm_ver}
Requires:	libxcb >= 1.13
Requires:	libomxil-bellagio
Requires:	zlib >= %{zlib_ver}
Obsoletes:	omxil-mesa-nouveau
Obsoletes:	omxil-mesa-r600
Obsoletes:	omxil-mesa-radeonsi

%description -n omxil-mesa
Mesa driver for Bellagio OpenMAX IL API.

%description -n omxil-mesa -l pl.UTF-8
Sterownik Mesa dla API Bellagio OpenMAX IL.

%package vulkan-icd-intel
Summary:	Mesa Vulkan driver for Intel GPUs
Summary(pl.UTF-8):	Sterownik Vulkan dla GPU firmy Intel
License:	MIT
Group:		Libraries
Requires:	libdrm >= %{libdrm_ver}
Requires:	libxcb >= 1.13
Requires:	xorg-lib-libxshmfence >= 1.1
# wayland-client
Requires:	wayland >= %{wayland_ver}
Requires:	zlib >= %{zlib_ver}
Suggests:	vulkan(loader)
Provides:	vulkan(icd) = 1.0.3

%description vulkan-icd-intel
Mesa Vulkan driver for Intel GPUs.

%description vulkan-icd-intel -l pl.UTF-8
Sterownik Vulkan dla GPU Intela.

%package vulkan-icd-intel-devel
Summary:	Header files for Mesa Intel GPU Vulkan driver
Summary(pl.UTF-8):	Pliki nagłówkowe sterownika Vulkan dla GPU Intela
License:	MIT
Group:		Development/Libraries
Requires:	%{name}-vulkan-icd-intel = %{version}-%{release}

%description vulkan-icd-intel-devel
eader files for Mesa Intel GPU Vulkan driver.

%description vulkan-icd-intel-devel -l pl.UTF-8
Pliki nagłówkowe sterownika Vulkan dla GPU Intel.

%package vulkan-icd-radeon
Summary:	radv - experimental Mesa Vulkan driver for AMD Radeon GPUs
Summary(pl.UTF-8):	radv - eksperymentalny sterownik Vulkan dla GPU firmy AMD
License:	MIT
Group:		Libraries
Requires:	libdrm >= %{libdrm_ver}
Requires:	libxcb >= 1.13
Requires:	xorg-lib-libxshmfence >= 1.1
# wayland-client
Requires:	wayland >= %{wayland_ver}
Requires:	zlib >= %{zlib_ver}
Suggests:	vulkan(loader)
Provides:	vulkan(icd) = 1.0.3

%description vulkan-icd-radeon
radv - experimental Mesa Vulkan driver for AMD Radeon GPUs.

%description vulkan-icd-radeon -l pl.UTF-8
radv - eksperymentalny sterownik Vulkan dla GPU firmy AMD.

%prep
%setup -q -n mesa-mesa-%{version}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}

dri_drivers="nouveau r200 radeon swrast \
%ifarch %{ix86} %{x8664} x32
i965 %{!?with_gallium_i915:i915} \
%endif
"

dri_drivers=$(echo $dri_drivers | xargs | tr ' ' ',')

gallium_drivers="svga swrast virgl \
%ifarch %{x8664}
swr
%endif
%ifarch %{ix86} %{x8664} x32
%{?with_gallium_i915:i915} \
%endif
%if %{with gallium_radeon}
r300 r600 radeonsi \
%endif
%if %{with gallium_nouveau}
nouveau
%endif
%ifarch %{arm}
etnaviv \
freedreno \
imx \
vc4 \
%endif
"

gallium_drivers=$(echo $gallium_drivers | xargs | tr ' ' ',')

vulkan_drivers="%{?with_radv:radeon} \
%ifarch %{ix86} %{x8664} x32
intel \
%endif
"

vulkan_drivers=$(echo $vulkan_drivers | xargs | tr ' ' ',')

%configure \
	--disable-silent-rules \
	%{__enable gbm} \
	--enable-glx-tls \
	%{?with_glvnd:--enable-libglvnd} \
	--enable-osmesa \
	--enable-selinux \
	--enable-shared \
	--enable-shared-glapi \
	%{?with_static_libs:--enable-static} \
	%{?with_texture_float:--enable-texture-float} \
%if %{with egl}
	--enable-egl \
	--enable-gles1 \
	--enable-gles2 \
	--with-platforms=x11%{?with_gbm:,drm}%{?with_wayland:,wayland} \
%endif
%if %{with gallium}
	%{?with_hud_extra:--enable-gallium-extra-hud} \
	--enable-llvm \
	%{__enable_disable shared_llvm llvm-shared-libs} \
	%{__enable ocl_icd opencl-icd} \
	%{?with_lm_sensors:--enable-lmsensors} \
	%{?with_nine:--enable-nine} \
	%{__enable opencl} \
	%{__enable va} \
	--enable-vdpau \
	%{?with_omx:--enable-omx-bellagio} \
	%{?with_xa:--enable-xa} \
	--enable-xvmc \
	--with-gallium-drivers=${gallium_drivers} \
%else
	--without-gallium-drivers \
%endif
	--with-dri-drivers=${dri_drivers} \
	--with-dri-driverdir=%{_libdir}/xorg/modules/dri \
	--with-vulkan-drivers=${vulkan_drivers} \
	--with-vulkan-icddir=/usr/share/vulkan/icd.d \
	--with-sha1=libnettle \
	--with-va-libdir=%{_libdir}/libva/dri

%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# dlopened by soname
%{?with_gallium:%{__rm} $RPM_BUILD_ROOT%{_libdir}/libXvMC*.so}
%{?with_gallium:%{__rm} $RPM_BUILD_ROOT%{_libdir}/libXvMC*.so.1.0}
# dlopened by soname or .so link
%{?with_gallium:%{__rm} $RPM_BUILD_ROOT%{_libdir}/vdpau/libvdpau_*.so.1.0}
# not used externally
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libglapi.so
# dlopened
%{?with_omx:%{__rm} $RPM_BUILD_ROOT%{_libdir}/bellagio/libomx_*.la}
%{?with_nine:%{__rm} $RPM_BUILD_ROOT%{_libdir}/d3d/d3dadapter9.la}
%{?with_gallium:%{__rm} $RPM_BUILD_ROOT%{_libdir}/gallium-pipe/pipe_*.la}
# not defined by standards; and not needed, there is pkg-config support
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%if %{without glvnd}
# remove "OS ABI: Linux 2.4.20" tag, so private copies (nvidia or fglrx),
# set up via /etc/ld.so.conf.d/*.conf will be preferred over this
strip -R .note.ABI-tag $RPM_BUILD_ROOT%{_libdir}/libGL.so.*.*
%endif

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
%post	libXvMC-r600 -p /sbin/ldconfig
%postun	libXvMC-r600 -p /sbin/ldconfig

%post	libgbm -p /sbin/ldconfig
%postun	libgbm -p /sbin/ldconfig

%post	libglapi -p /sbin/ldconfig
%postun	libglapi -p /sbin/ldconfig

%post	libxatracker -p /sbin/ldconfig
%postun	libxatracker -p /sbin/ldconfig

%if %{with egl}
%files libEGL
%defattr(644,root,root,755)
%if %{with glvnd}
%attr(755,root,root) %{_libdir}/libEGL_mesa.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libEGL_mesa.so.0
%{_datadir}/glvnd/egl_vendor.d/50_mesa.json
%else
%attr(755,root,root) %{_libdir}/libEGL.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libEGL.so.1
%endif

%files libEGL-devel
%defattr(644,root,root,755)
%if %{with glvnd}
%attr(755,root,root) %{_libdir}/libEGL_mesa.so
%else
%attr(755,root,root) %{_libdir}/libEGL.so
%endif
%dir %{_includedir}/EGL
%{_includedir}/EGL/egl.h
%{_includedir}/EGL/eglext.h
%{_includedir}/EGL/eglextchromium.h
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
%doc docs/{*.html,README.UVD,features.txt,relnotes/*.html}
%if %{with glvnd}
%attr(755,root,root) %{_libdir}/libGLX_mesa.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libGLX_mesa.so.0
%attr(755,root,root) %{_libdir}/libGLX_mesa.so
%else
%attr(755,root,root) %{_libdir}/libGL.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libGL.so.1
# symlink for binary apps which fail to conform Linux OpenGL ABI
# (and dlopen libGL.so instead of libGL.so.1; the same does Mesa libEGL)
%attr(755,root,root) %{_libdir}/libGL.so
%endif
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/drirc

%files libGL-devel
%defattr(644,root,root,755)
%doc docs/specs/*
%dir %{_includedir}/GL
%{_includedir}/GL/gl.h
%{_includedir}/GL/glcorearb.h
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
%{_includedir}/GLES3
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
%if %{with ocl_icd}
%files OpenCL-icd
%defattr(644,root,root,755)
/etc/OpenCL/vendors/mesa.icd
%attr(755,root,root) %{_libdir}/libMesaOpenCL.so
%attr(755,root,root) %{_libdir}/libMesaOpenCL.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libMesaOpenCL.so.1
# currently only OpenCL uses dynamic pipe loader
%dir %{_libdir}/gallium-pipe
%else
%files libOpenCL
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOpenCL.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libOpenCL.so.1
# currently only OpenCL uses dynamic pipe loader
%dir %{_libdir}/gallium-pipe

%files libOpenCL-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOpenCL.so
%{_includedir}/CL
%endif
%endif

%if %{with egl} && %{with openvg} && %{with gallium}
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
%attr(755,root,root) %{_libdir}/libXvMCnouveau.so.1.0.0
%attr(755,root,root) %ghost %{_libdir}/libXvMCnouveau.so.1
%endif

%if %{with gallium_radeon}
%files libXvMC-r600
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libXvMCr600.so.1.0.0
%attr(755,root,root) %ghost %{_libdir}/libXvMCr600.so.1
%endif

%if %{with va}
%files -n libva-driver-gallium
%defattr(644,root,root,755)

%if %{with gallium_radeon}
%files -n libva-driver-r600
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libva/dri/r600_drv_video.so

%files -n libva-driver-radeonsi
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libva/dri/radeonsi_drv_video.so
%endif

%if %{with gallium_nouveau}
%files -n libva-driver-nouveau
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libva/dri/nouveau_drv_video.so
%endif
%endif
%endif

%if %{with gbm}
%files libgbm
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgbm.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libgbm.so.1

%files libgbm-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgbm.so
%{_includedir}/gbm.h
%{_pkgconfigdir}/gbm.pc
%endif

%files libglapi
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libglapi.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libglapi.so.0
# libglapi-devel? nothing seems to need it atm.
#%attr(755,root,root) %{_libdir}/libglapi.so

%if %{with xa}
%files libxatracker
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxatracker.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libxatracker.so.2

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

%files dri-driver-ati-radeon-R100
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/radeon_dri.so

%files dri-driver-ati-radeon-R200
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/r200_dri.so

%if %{with gallium}
%if %{with gallium_radeon}
%files dri-driver-ati-radeon-R300
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/r300_dri.so

%files dri-driver-ati-radeon-R600
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/r600_dri.so

%files dri-driver-ati-radeon-SI
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/radeonsi_dri.so
%endif
%endif

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
%if %{with gallium}
%attr(755,root,root) %{_libdir}/xorg/modules/dri/kms_swrast_dri.so
%endif
%attr(755,root,root) %{_libdir}/xorg/modules/dri/swrast_dri.so

%if %{with gallium}
%ifarch %{arm}
%files dri-driver-etnaviv
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/etnaviv_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/imx-drm_dri.so

%files dri-driver-freedreno
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/kgsl_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/msm_dri.so

%files dri-driver-vc4
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/vc4_dri.so
%endif

%files dri-driver-virgl
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/virtio_gpu_dri.so

%files dri-driver-vmwgfx
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/vmwgfx_dri.so
%endif

%if %{with gallium}
%if %{with gallium_i915}
%files pipe-driver-i915
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gallium-pipe/pipe_i915.so
%endif

%ifarch %{arm}
%files pipe-driver-msm
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gallium-pipe/pipe_msm.so
%endif

%if %{with gallium_nouveau}
%files pipe-driver-nouveau
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gallium-pipe/pipe_nouveau.so
%endif

%if %{with gallium_radeon}
%files pipe-driver-r300
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gallium-pipe/pipe_r300.so

%files pipe-driver-r600
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gallium-pipe/pipe_r600.so

%files pipe-driver-radeonsi
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gallium-pipe/pipe_radeonsi.so
%endif

%files pipe-driver-swrast
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gallium-pipe/pipe_swrast.so

%files pipe-driver-vmwgfx
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gallium-pipe/pipe_vmwgfx.so

%ifarch %{x8664}
%files swr
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libswrAVX.so
%attr(755,root,root) %{_libdir}/libswrAVX2.so
%endif
%endif

%if %{with nine}
%files d3d
%defattr(644,root,root,755)
%dir %{_libdir}/d3d
%attr(755,root,root) %{_libdir}/d3d/d3dadapter9.so*

%files d3d-devel
%defattr(644,root,root,755)
%{_includedir}/d3dadapter
%{_pkgconfigdir}/d3d.pc
%endif

%if %{with gallium}
# ldconfig is not used in vdpau tree, so package all symlinks
%if %{with gallium_nouveau}
%files -n libvdpau-driver-mesa-nouveau
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_nouveau.so.1.0.0
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_nouveau.so.1
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_nouveau.so
%endif

%if %{with gallium_radeon}
%files -n libvdpau-driver-mesa-r300
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_r300.so.1.0.0
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_r300.so.1
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_r300.so

%files -n libvdpau-driver-mesa-r600
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_r600.so.1.0.0
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_r600.so.1
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_r600.so

%files -n libvdpau-driver-mesa-radeonsi
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_radeonsi.so.1.0.0
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_radeonsi.so.1
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_radeonsi.so
%endif
%endif

%if %{with gallium} && %{with omx}
%files -n omxil-mesa
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/bellagio/libomx_mesa.so
%endif

%files vulkan-icd-intel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvulkan_intel.so
%{_datadir}/vulkan/icd.d/intel_icd.*.json

%files vulkan-icd-intel-devel
%defattr(644,root,root,755)
%{_includedir}/vulkan/vulkan_intel.h

%if %{with radv}
%files vulkan-icd-radeon
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvulkan_radeon.so
%{_datadir}/vulkan/icd.d/radeon_icd.*.json
%endif
