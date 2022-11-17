# TODO:
# - libtizonia >= 0.10.0 as an alternative for bellagio?
# - bcond for perfetto peformance analysis? (BR: perfetto)
#
# Conditional build:
%bcond_without	gallium		# gallium drivers
%bcond_without	gallium_i915	# gallium i915 driver
%bcond_without	gallium_nouveau	# gallium nouveau driver
%bcond_without	gallium_radeon	# gallium radeon drivers
%bcond_without	gallium_zink	# gallium zink driver (based on vulkan)
%bcond_without	egl		# EGL libraries
%bcond_without	gbm		# Graphics Buffer Manager
%bcond_without	nine		# Nine Direct3D 9+ state tracker (for Wine)
%bcond_without	opencl		# OpenCL support
%bcond_without	opencl_spirv	# OpenCL SPIRV support
%bcond_without	ocl_icd		# OpenCL as ICD (installable client driver)
%bcond_without	glvnd		# OpenGL vendor neutral dispatcher support
%bcond_without	omx		# OpenMAX (Bellagio OMXIL) support
%bcond_without	va		# VA library
%bcond_without	wayland		# Wayland EGL
%bcond_without	xa		# XA state tracker (for vmwgfx xorg driver)
%bcond_without	radv		# disable build of the radeon Vulkan driver
%bcond_with	sse2		# SSE2 instructions
%bcond_with	hud_extra	# HUD block/NIC I/O HUD stats support
%bcond_with	lm_sensors	# HUD lm_sensors support
%bcond_with	tests		# tests
#
# glapi version (glapi tables in dri drivers and libglx must be in sync);
# set to current Mesa version on ABI break, when xserver tables get regenerated
# (until they start to be somehow versioned themselves)
%define		glapi_ver		7.1.0
# other packages
%define		libdrm_ver		2.4.110
%define		dri2proto_ver		2.8
%define		glproto_ver		1.4.14
%define		zlib_ver		1.2.8
%define		wayland_ver		1.18
%define		libglvnd_ver		1.3.4-2
%define		llvm_ver		11.0.0
%define		gcc_ver 		6:4.8.0

%if %{without gallium}
%undefine	with_gallium_i915
%undefine	with_gallium_nouveau
%undefine	with_gallium_radeon
%undefine	with_nine
%undefine	with_omx
%undefine	with_opencl
%undefine	with_va
%undefine	with_xa
%endif

%if %{without egl}
%undefine	with_gbm
%undefine	with_wayland
%endif

%if %{without opencl}
%undefine	with_ocl_icd
%endif

%if %{with gallium_radeon} || %{with gallium_nouveau}
%define		with_vdpau	1
%define		with_xvmc	1
%endif

%ifarch %{x86_with_sse2}
%define		with_sse2	1
%endif

Summary:	Free OpenGL implementation
Summary(pl.UTF-8):	Wolnodostępna implementacja standardu OpenGL
Name:		Mesa
Version:	22.2.4
Release:	1
License:	MIT (core) and others - see license.html file
Group:		X11/Libraries
#Source0:	ftp://ftp.freedesktop.org/pub/mesa/mesa-%{version}.tar.xz
## Source0-md5:	7c61a801311fb8d2f7b3cceb7b5cf308
Source0:	https://archive.mesa3d.org/mesa-%{version}.tar.xz
# Source0-md5:	a258a3d590d76bc1ff89a204f063e3b8
URL:		https://www.mesa3d.org/
%{?with_opencl_spirv:BuildRequires:	SPIRV-LLVM-Translator-devel >= 8.0.1.3}
%{?with_gallium_zink:BuildRequires:	Vulkan-Loader-devel}
BuildRequires:	bison > 2.3
%{?with_opencl:BuildRequires:	clang-devel >= %{llvm_ver}}
BuildRequires:	elfutils-devel
BuildRequires:	expat-devel >= 1.95
BuildRequires:	flex
BuildRequires:	gcc >= %{gcc_ver}
%ifarch %{armv6}
BuildRequires:	libatomic-devel
%endif
BuildRequires:	libdrm-devel >= %{libdrm_ver}
%{?with_glvnd:BuildRequires:	libglvnd-devel >= %{libglvnd_ver}}
BuildRequires:	libselinux-devel
BuildRequires:	libstdc++-devel >= %{gcc_ver}
BuildRequires:	libunwind-devel
%{?with_va:BuildRequires:	libva-devel}
%{?with_va:BuildRequires:	pkgconfig(libva) >= 1.8.0}
%{?with_vdpau:BuildRequires:	libvdpau-devel >= 1.1}
BuildRequires:	libxcb-devel >= 1.13
%{?with_gallium:BuildRequires:	llvm-devel >= %{llvm_ver}}
%{?with_radv:BuildRequires:	llvm-devel >= %{llvm_ver}}
%{?with_opencl:BuildRequires:	llvm-libclc}
%{?with_omx:BuildRequires:	libomxil-bellagio-devel}
BuildRequires:	meson >= 0.53
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(talloc) >= 2.0.1
BuildRequires:	pkgconfig(xcb-dri2) >= 1.8
BuildRequires:	pkgconfig(xcb-dri3) >= 1.13
BuildRequires:	pkgconfig(xcb-glx) >= 1.8.1
BuildRequires:	pkgconfig(xcb-present) >= 1.13
BuildRequires:	pkgconfig(xcb-randr) >= 1.12
BuildRequires:	python3 >= 1:3.2
BuildRequires:	python3-Mako >= 0.8.0
BuildRequires:	rpmbuild(macros) >= 2.007
BuildRequires:	sed >= 4.0
%{?with_opencl_spirv:BuildRequires:	spirv-tools-devel >= 2018.0}
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel
# wayland-{client,server}
%{?with_wayland:BuildRequires:	wayland-devel >= %{wayland_ver}}
%{?with_wayland:BuildRequires:	wayland-protocols >= 1.24}
%{?with_wayland:BuildRequires:	wayland-egl-devel >= %{wayland_ver}}
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel >= 1.0.5
BuildRequires:	xorg-lib-libXfixes-devel >= 2.0
BuildRequires:	xorg-lib-libXrandr-devel >= 1.3
BuildRequires:	xorg-lib-libXv-devel
%{?with_xvmc:BuildRequires:	xorg-lib-libXvMC-devel >= 1.0.6}
BuildRequires:	xorg-lib-libXxf86vm-devel
BuildRequires:	xorg-lib-libxshmfence-devel >= 1.1
BuildRequires:	xorg-proto-dri2proto-devel >= %{dri2proto_ver}
BuildRequires:	xorg-proto-glproto-devel >= %{glproto_ver}
%if %{with gallium}
%{?with_lm_sensors:BuildRequires:	lm_sensors-devel}
BuildRequires:	xz
%endif
BuildRequires:	zlib-devel >= %{zlib_ver}
BuildRequires:	zstd-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# libGLESv1_CM, libGLESv2, libGL, libOSMesa:
#  _glapi_tls_Dispatch is defined in libglapi, but it's some kind of symbol ldd -r doesn't notice(?)
%define		skip_post_check_so	libGLESv1_CM.so.1.* libGLESv2.so.2.* libGL.so.1.* libOSMesa.so.* libGLX_mesa.so.0.*

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
%{?with_wayland:Requires:	wayland >= %{wayland_ver}}
%if %{with gbm}
Requires:	%{name}-libgbm = %{version}-%{release}
%endif
%if %{with glvnd}
Requires:	libglvnd-libEGL >= %{libglvnd_ver}
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
Requires:	%{name}-libEGL = %{version}-%{release}
Requires:	xorg-lib-libX11-devel
%if %{with glvnd}
Requires:	libglvnd-libEGL-devel >= %{libglvnd_ver}
%else
Requires:	%{name}-khrplatform-devel = %{version}-%{release}
Requires:	libdrm-devel >= %{libdrm_ver}
Requires:	libxcb-devel >= 1.13
Requires:	pkgconfig(xcb-dri2) >= 1.8
Requires:	pkgconfig(xcb-glx) >= 1.8.1
Requires:	xorg-lib-libXext-devel >= 1.0.5
Requires:	xorg-lib-libXfixes-devel >= 2.0
Requires:	xorg-lib-libXxf86vm-devel
%endif
%if %{without glvnd}
Provides:	EGL-devel = 1.5
%endif
Obsoletes:	Mesa-libEGL-static < 18.3

%description libEGL-devel
Header files for Mesa implementation of EGL library.

%description libEGL-devel -l pl.UTF-8
Pliki nagłówkowe implementacji Mesa biblioteki EGL.

%package libGL
Summary:	Free Mesa3D implementation of libGL OpenGL library
Summary(pl.UTF-8):	Wolnodostępna implementacja Mesa3D biblioteki libGL ze standardu OpenGL
License:	MIT
Group:		X11/Libraries
Requires:	%{name}-libglapi = %{version}-%{release}
Requires:	libdrm >= %{libdrm_ver}
Requires:	libxcb >= 1.13
%if %{with glvnd}
Requires:	libglvnd-libGL >= %{libglvnd_ver}
%endif
Provides:	OpenGL = 4.6
Provides:	OpenGL-GLX = 1.4
Obsoletes:	Mesa < 6.4-2
Obsoletes:	Mesa-dri < 6.4.1-3
Obsoletes:	Mesa-dri-core < 10.0.0
Obsoletes:	Mesa-swr < 22
Obsoletes:	X11-OpenGL-libGL < 1:7.0.0
Obsoletes:	XFree86-OpenGL-libGL < 1:7.0.0

%description libGL
Mesa is a 3-D graphics library with an API which is very similar to
that of OpenGL(R). To the extent that Mesa utilizes the OpenGL command
syntax or state machine, it is being used with authorization from
Silicon Graphics, Inc. However, the author does not possess an OpenGL
license from SGI, and makes no claim that Mesa is in any way a
compatible replacement for OpenGL or associated with SGI.

This package contains libGL which implements OpenGL 4.6 and GLX 1.4
specifications. It uses DRI for rendering.

%description libGL -l pl.UTF-8
Mesa jest biblioteką grafiki 3D z API bardzo podobnym do OpenGL(R). Do
tego stopnia, że Mesa używa składni i automatu OpenGL jest używana z
autoryzacją Silicon Graphics, Inc. Jednak autor nie posiada licencji
OpenGL od SGI i nie twierdzi, że Mesa jest kompatybilnym zamiennikiem
OpenGL ani powiązana z SGI.

Ten pakiet zawiera libGL implementującą specyfikacje OpenGL 4.6 oraz
GLX 1.4. Używa DRI do renderowania.

%package libGL-devel
Summary:	Header files for Mesa3D libGL library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libGL z projektu Mesa3D
License:	MIT
Group:		X11/Development/Libraries
%if %{with glvnd}
Requires:	libglvnd-libGL-devel >= %{libglvnd_ver}
%else
Requires:	%{name}-khrplatform-devel = %{version}-%{release}
Requires:	%{name}-libGL = %{version}-%{release}
Requires:	libdrm-devel >= %{libdrm_ver}
Requires:	libxcb-devel >= 1.13
Requires:	pkgconfig(xcb-dri2) >= 1.8
Requires:	pkgconfig(xcb-glx) >= 1.8.1
Requires:	xorg-lib-libX11-devel
Requires:	xorg-lib-libXext-devel >= 1.0.5
Requires:	xorg-lib-libXfixes-devel >= 2.0
Requires:	xorg-lib-libXxf86vm-devel
%endif
Suggests:	OpenGL-doc-man
%if %{without glvnd}
Provides:	OpenGL-GLX-devel = 1.4
Provides:	OpenGL-devel = 4.6
%endif
Obsoletes:	Mesa-devel < 6.4-2
Obsoletes:	Mesa-libGL-static < 18.3
Obsoletes:	Mesa-static < 6.4-2
Obsoletes:	X11-OpenGL-devel < 1:7.0.0
Obsoletes:	X11-OpenGL-devel-base < 1:7.0.0
Obsoletes:	X11-OpenGL-static < 1:7.0.0
Obsoletes:	XFree86-OpenGL-devel < 1:7.0.0
Obsoletes:	XFree86-OpenGL-devel-base < 1:7.0.0
Obsoletes:	XFree86-OpenGL-static < 1:7.0.0

%description libGL-devel
Header files for Mesa3D libGL library.

%description libGL-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libGL z projektu Mesa3D.

%package libGLES
Summary:	Mesa implementation of GLES (OpenGL ES) libraries
Summary(pl.UTF-8):	Implementacja Mesa bibliotek GLES (OpenGL ES)
Group:		Libraries
Requires:	%{name}-libglapi = %{version}-%{release}
%if %{with glvnd}
Requires:	libglvnd-libGLES >= %{libglvnd_ver}
%endif
Provides:	OpenGLES
Provides:	OpenGLESv1 = 1.1
Provides:	OpenGLESv2 = 2.0
Provides:	OpenGLESv3 = 3.2

%description libGLES
This package contains shared libraries of Mesa implementation of GLES
(OpenGL ES) - cross-platform API for full-function 2D and 3D graphics
on embedded systems. OpenGL ES specification can be found on Khronos
Group site: <http://www.khronos.org/opengles/>. Mesa implements OpenGL
ES 1.1 and 2.0/3.2.

%description libGLES -l pl.UTF-8
Ten pakiet zawiera biblioteki współdzielone implementacji Mesa
standardu GLES (OpenGL ES) - wieloplatformowego API do w pełni
funkcjonalnej grafiki 2D i 3D na systemach wbudowanych. Specyfikację
OpenGL ES można znaleźć na stronie Khronos Group:
<http://www.khronos.org/opengles/>. Mesa zawiera implementacją OpenGL
ES 1.1 i 2.0/3.2.

%package libGLES-devel
Summary:	Header files for Mesa GLES libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Mesa GLES
Group:		Development/Libraries
Requires:	%{name}-libGLES = %{version}-%{release}
%if %{with glvnd}
Requires:	libglvnd-libGLES-devel >= %{libglvnd_ver}
%else
Requires:	%{name}-khrplatform-devel = %{version}-%{release}
# <EGL/egl.h> for <GLES/egl.h>
Requires:	%{name}-libEGL-devel = %{version}-%{release}
%endif
%if %{without glvnd}
Provides:	OpenGLES-devel
Provides:	OpenGLESv1-devel = 1.1
Provides:	OpenGLESv2-devel = 2.0
Provides:	OpenGLESv3-devel = 3.2
%endif

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
Obsoletes:	Mesa-libOSMesa-static < 18.3

%description libOSMesa-devel
Header file for OSMesa (off-screen renderer) library.

%description libOSMesa-devel -l pl.UTF-8
Plik nagłówkowy biblioteki OSMesa (renderującej bitmapy w pamięci).

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

Implementacja dostarczona jest w postaci instalowalnego sterownika
klienta (ICD), który może być użyty z loaderem ocl-icd.

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
Provides:	khrplatform-devel
Conflicts:	Mesa-libEGL-devel < 8.0.1-2

%description khrplatform-devel
Khronos platform header file.

%description khrplatform-devel -l pl.UTF-8
Plik nagłówkowy platformy Khronos.

%package dri-devel
Summary:	Direct Rendering Infrastructure interface header file
Summary(pl.UTF-8):	Plik nagłówkowy interfejsu DRI (Direct Rendering Infrastructure)
Group:		Development/Libraries
Requires:	libdrm-devel >= %{libdrm_ver}
# <GL/gl.h>
%if %{with glvnd}
Requires:	libglvnd-libGL-devel >= %{libglvnd_ver}
Conflicts:	Mesa-libGL-devel < 21.1.0-2
%else
Requires:	Mesa-libGL-devel = %{version}-%{release}
%endif

%description dri-devel
Direct Rendering Infrastructure interface header file.

%description dri-devel -l pl.UTF-8
Plik nagłówkowy interfejsu DRI (Direct Rendering Infrastructure).

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

%package dri-driver-ati-radeon-R300
Summary:	X.org DRI driver for ATI R300 card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart ATI R300
License:	MIT
Group:		X11/Libraries
Requires:	zlib >= %{zlib_ver}
Suggests:	xorg-driver-video-amdgpu
Suggests:	xorg-driver-video-ati
Obsoletes:	X11-driver-radeon-dri < 1:7.0.0
Conflicts:	xorg-xserver-libglx(glapi) > %{glapi_ver}
Conflicts:	xorg-xserver-libglx(glapi) < %{glapi_ver}

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
Requires:	zlib >= %{zlib_ver}
Suggests:	xorg-driver-video-amdgpu
Suggests:	xorg-driver-video-ati
Conflicts:	xorg-xserver-libglx(glapi) > %{glapi_ver}
Conflicts:	xorg-xserver-libglx(glapi) < %{glapi_ver}

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
Requires:	zlib >= %{zlib_ver}
Suggests:	xorg-driver-video-amdgpu
Suggests:	xorg-driver-video-ati
Conflicts:	xorg-xserver-libglx(glapi) > %{glapi_ver}
Conflicts:	xorg-xserver-libglx(glapi) < %{glapi_ver}

%description dri-driver-ati-radeon-SI
X.org Gallium DRI driver for ATI Southern Islands card family (Radeon
HD 7700-8000, R9, APU). It supports TAHITI, PITCAIRN, VERDE, OLAND,
HAINAN, BONAIRE, KABINI, MULLINS, KAVERI, HAWAII, ICELAND, TONGA,
CARRIZO, FIJI, POLARIS, STONEY, VEGA, RAVEN chips.

%description dri-driver-ati-radeon-SI -l pl.UTF-8
Sterownik X.org DRI Gallium dla rodziny kart ATI Southern Islands
(Radeon HD 7700-8000, R9, APU). Obsługuje układy TAHITI, PITCAIRN,
VERDE, OLAND, HAINAN, BONAIRE, KABINI, MULLINS, KAVERI, HAWAII,
ICELAND, TONGA, CARRIZO, FIJI, POLARIS, STONEY, VEGA, RAVEN.

%package dri-driver-etnaviv
Summary:	X.org DRI driver for Vivante 3D chips
Summary(pl.UTF-8):	Sterownik X.org DRI dla układów Vivante 3D
License:	MIT
Group:		X11/Libraries
Requires:	zlib >= %{zlib_ver}
#Suggests:	xorg-driver-video-?
Conflicts:	xorg-xserver-libglx(glapi) > %{glapi_ver}
Conflicts:	xorg-xserver-libglx(glapi) < %{glapi_ver}

%description dri-driver-etnaviv
X.org Gallium DRI driver for Vivante 3D chips.

%description dri-driver-etnaviv -l pl.UTF-8
Sterownik X.org DRI Gallium dla układów Vivante 3D.

%package dri-driver-freedreno
Summary:	X.org DRI driver for Adreno chips
Summary(pl.UTF-8):	Sterownik X.org DRI dla układów Adreno
License:	MIT
Group:		X11/Libraries
Requires:	zlib >= %{zlib_ver}
Suggests:	xorg-driver-video-freedreno
Conflicts:	xorg-xserver-libglx(glapi) > %{glapi_ver}
Conflicts:	xorg-xserver-libglx(glapi) < %{glapi_ver}

%description dri-driver-freedreno
X.org Gallium DRI driver for Adreno chips.

%description dri-driver-freedreno -l pl.UTF-8
Sterownik X.org DRI Gallium dla układów Adreno.

%package dri-driver-intel-crocus
Summary:	X.org DRI driver for Intel Gen4-Gen7 chips
Summary(pl.UTF-8):	Sterownik X.org DRI dla układów Intel Gen4-Gen7
License:	MIT
Group:		X11/Libraries
Requires:	zlib >= %{zlib_ver}
Obsoletes:	Mesa-dri-driver-intel-i965 < 22.0.0
Conflicts:	xorg-xserver-libglx(glapi) > %{glapi_ver}
Conflicts:	xorg-xserver-libglx(glapi) < %{glapi_ver}

%description dri-driver-intel-crocus
X.org Gallium DRI driver for Intel Gen4/Gen5/Gen6/Gen7 chips.

%description dri-driver-intel-crocus -l pl.UTF-8
Sterownik X.org DRI dla układów Intel Gen4/Gen5/Gen6/Gen7.

%package dri-driver-intel-i915
Summary:	X.org DRI driver for Intel i915 card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart Intel i915
License:	MIT
Group:		X11/Libraries
Requires:	zlib >= %{zlib_ver}
Obsoletes:	Mesa-dri-driver-intel-i830 < 6.5
Obsoletes:	X11-driver-i810-dri < 1:7.0.0
Conflicts:	xorg-xserver-libglx(glapi) > %{glapi_ver}
Conflicts:	xorg-xserver-libglx(glapi) < %{glapi_ver}

%description dri-driver-intel-i915
X.org DRI driver for Intel i915 card family (830, 845, 852/855, 865,
915, 945, G33, Q33, Q35, Pineview).

%description dri-driver-intel-i915 -l pl.UTF-8
Sterownik X.org DRI dla rodziny kart Intel i915 (830, 845, 852/855,
865, 915, 945, G33, Q33, Q35, Pineview).

%package dri-driver-intel-iris
Summary:	X.org DRI driver for Intel Iris (Gen8+) card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart Intel Iris (Gen8+)
License:	MIT
Group:		X11/Libraries
Requires:	zlib >= %{zlib_ver}
Conflicts:	xorg-xserver-libglx(glapi) > %{glapi_ver}
Conflicts:	xorg-xserver-libglx(glapi) < %{glapi_ver}

%description dri-driver-intel-iris
X.org Gallium DRI driver for Intel Iris (Gen8+) card family
(Broadwell, Skylake, Broxton, Kabylake, Coffeelake, Geminilake,
Whiskey Lake, Comet Lake, Cannonlake, Ice Lake, Elkhart Lake).

%description dri-driver-intel-iris -l pl.UTF-8
Sterownik X.org DRI Gallium dla rodziny kart Intel Iris (Gen8+:
Broadwell, Skylake, Broxton, Kabylake, Coffeelake, Geminilake,
Whiskey Lake, Comet Lake, Cannonlake, Ice Lake, Elkhart Lake).

%package dri-driver-kmsro
Summary:	X.org Gallium DRI driver using KMS Render-Only architecture
Summary(pl.UTF-8):	Sterownik X.org DRI Gallium wykorzystujący architekturę KMS Render-Only
License:	MIT
Group:		X11/Libraries
Requires:	zlib >= %{zlib_ver}
#Suggests:	xorg-driver-video-?
Conflicts:	xorg-xserver-libglx(glapi) > %{glapi_ver}
Conflicts:	xorg-xserver-libglx(glapi) < %{glapi_ver}

%description dri-driver-kmsro
X.org Gallium DRI driver using KMS Render-Only architecture.

%description dri-driver-kmsro -l pl.UTF-8
Sterownik X.org DRI Gallium wykorzystujący architekturę KMS
Render-Only.

%package dri-driver-lima
Summary:	X.org DRI driver for Mali Utgard chips
Summary(pl.UTF-8):	Sterownik X.org DRI dla układów Mali Utgard
License:	MIT
Group:		X11/Libraries
Requires:	zlib >= %{zlib_ver}
#Suggests:	xorg-driver-video-???
Conflicts:	xorg-xserver-libglx(glapi) > %{glapi_ver}
Conflicts:	xorg-xserver-libglx(glapi) < %{glapi_ver}

%description dri-driver-lima
X.org Gallium DRI driver for Mali Utgard chips.

%description dri-driver-lima -l pl.UTF-8
Sterownik X.org DRI Gallium dla układów Mali Utgard.

%package dri-driver-nouveau
Summary:	X.org DRI driver for NVIDIA card family
Summary(pl.UTF-8):	Sterownik X.org DRI dla rodziny kart NVIDIA
License:	MIT
Group:		X11/Libraries
Requires:	zlib >= %{zlib_ver}
Suggests:	xorg-driver-video-nouveau
Conflicts:	xorg-xserver-libglx(glapi) > %{glapi_ver}
Conflicts:	xorg-xserver-libglx(glapi) < %{glapi_ver}

%description dri-driver-nouveau
X.org DRI drivers for NVIDIA card family.

%description dri-driver-nouveau -l pl.UTF-8
Sterowniki X.org DRI dla rodziny kart NVIDIA.

%package dri-driver-panfrost
Summary:	X.org DRI driver for Mali Midgard/Bifrost chips
Summary(pl.UTF-8):	Sterownik X.org DRI dla układów Mali Midgard/Bifrost
License:	MIT
Group:		X11/Libraries
Requires:	zlib >= %{zlib_ver}
#Suggests:	xorg-driver-video-???
Conflicts:	xorg-xserver-libglx(glapi) > %{glapi_ver}
Conflicts:	xorg-xserver-libglx(glapi) < %{glapi_ver}

%description dri-driver-panfrost
X.org Gallium DRI driver for Mali Midgard/Bifrost chips.

%description dri-driver-panfrost -l pl.UTF-8
Sterownik X.org DRI Gallium dla układów Mali Midgard/Bifrost.

%package dri-driver-swrast
Summary:	X.org DRI software rasterizer driver
Summary(pl.UTF-8):	Sterownik X.org DRI obsługujący rysowanie programowe
License:	MIT
Group:		X11/Libraries
Requires:	zlib >= %{zlib_ver}
Conflicts:	xorg-xserver-libglx(glapi) > %{glapi_ver}
Conflicts:	xorg-xserver-libglx(glapi) < %{glapi_ver}

%description dri-driver-swrast
X.org DRI software rasterizer driver.

%description dri-driver-swrast -l pl.UTF-8
Sterownik X.org DRI obsługujący rysowanie programowe.

%package dri-driver-tegra
Summary:	X.org DRI driver for Tegra SoC chips
Summary(pl.UTF-8):	Sterownik X.org DRI dla układów SoC Tegra
License:	MIT
Group:		X11/Libraries
Requires:	zlib >= %{zlib_ver}
#Suggests:	xorg-driver-video-???
Conflicts:	xorg-xserver-libglx(glapi) > %{glapi_ver}
Conflicts:	xorg-xserver-libglx(glapi) < %{glapi_ver}

%description dri-driver-tegra
X.org Gallium DRI driver for Tegra SoC chips.

%description dri-driver-tegra -l pl.UTF-8
Sterownik X.org DRI Gallium dla układów Tegra SoC.

%package dri-driver-v3d
Summary:	X.org DRI driver for Broadcom VC5 chips
Summary(pl.UTF-8):	Sterownik X.org DRI dla układów Broadcom VC5
License:	MIT
Group:		X11/Libraries
Requires:	zlib >= %{zlib_ver}
Suggests:	xorg-driver-video-modesetting
Conflicts:	xorg-xserver-libglx(glapi) > %{glapi_ver}
Conflicts:	xorg-xserver-libglx(glapi) < %{glapi_ver}

%description dri-driver-v3d
X.org Gallium DRI driver for Broadcom VC5 chips.

%description dri-driver-v3d -l pl.UTF-8
Sterownik X.org DRI Gallium dla układów Broadcom VC5.

%package dri-driver-vc4
Summary:	X.org DRI driver for Broadcom VC4 chips
Summary(pl.UTF-8):	Sterownik X.org DRI dla układów Broadcom VC4
License:	MIT
Group:		X11/Libraries
Requires:	zlib >= %{zlib_ver}
Suggests:	xorg-driver-video-modesetting
Conflicts:	xorg-xserver-libglx(glapi) > %{glapi_ver}
Conflicts:	xorg-xserver-libglx(glapi) < %{glapi_ver}

%description dri-driver-vc4
X.org Gallium DRI driver for Broadcom VC4 chips.

%description dri-driver-vc4 -l pl.UTF-8
Sterownik X.org DRI Gallium dla układów Broadcom VC4.

%package dri-driver-virgl
Summary:	X.org DRI driver for QEMU VirGL
Summary(pl.UTF-8):	Sterownik X.org DRI dla QEMU VirGL
License:	MIT
Group:		X11/Libraries
Requires:	zlib >= %{zlib_ver}
Conflicts:	xorg-xserver-libglx(glapi) > %{glapi_ver}
Conflicts:	xorg-xserver-libglx(glapi) < %{glapi_ver}

%description dri-driver-virgl
X.org Gallium DRI driver for QEMU VirGL.

%description dri-driver-virgl -l pl.UTF-8
Sterownik X.org DRI Gallium dla QEMU VirGL.

%package dri-driver-vmwgfx
Summary:	X.org DRI driver for VMware
Summary(pl.UTF-8):	Sterownik X.org DRI dla VMware
License:	MIT
Group:		X11/Libraries
Requires:	zlib >= %{zlib_ver}
Suggests:	xorg-driver-video-vmware
Conflicts:	xorg-xserver-libglx(glapi) > %{glapi_ver}
Conflicts:	xorg-xserver-libglx(glapi) < %{glapi_ver}

%description dri-driver-vmwgfx
X.org Gallium DRI driver for VMWare.

%description dri-driver-vmwgfx -l pl.UTF-8
Sterownik X.org DRI Gallium dla VMware.

%package dri-driver-zink
Summary:	X.org DRI driver based on Vulkan
Summary(pl.UTF-8):	Sterownik X.org DRI oparty na Vulkanie
License:	MIT
Group:		X11/Libraries
Requires:	zlib >= %{zlib_ver}
Conflicts:	xorg-xserver-libglx(glapi) > %{glapi_ver}
Conflicts:	xorg-xserver-libglx(glapi) < %{glapi_ver}

%description dri-driver-zink
X.org Gallium DRI driver based on Vulkan.

%description dri-driver-zink -l pl.UTF-8
Sterownik X.org DRI Gallium oparty na Vulkanie.

%package pipe-driver-crocus
Summary:	crocus driver for Mesa Gallium dynamic pipe loader
Summary(pl.UTF-8):	Sterownik crocus dla dynamicznego systemu potoków szkieletu Mesa Gallium
Group:		Libraries
Requires:	zlib >= %{zlib_ver}

%description pipe-driver-crocus
crocus driver for Mesa Gallium dynamic pipe loader. It supports Intel
Gen4/Gen5/Gen6/Gen7 chips.

%description pipe-driver-crocus -l pl.UTF-8
Sterownik crocus dla dynamicznego systemu potoków szkieletu Mesa
Gallium. Obsługuje układy Intela Gen4/Gen5/Gen6/Gen7.

%package pipe-driver-i915
Summary:	i915 driver for Mesa Gallium dynamic pipe loader
Summary(pl.UTF-8):	Sterownik i915 dla dynamicznego systemu potoków szkieletu Mesa Gallium
Group:		Libraries
Requires:	zlib >= %{zlib_ver}
Obsoletes:	Mesa-gbm-driver-i915 < 11.1.1
Obsoletes:	Mesa-opencl-driver-i915 < 9.1

%description pipe-driver-i915
i915 driver for Mesa Gallium dynamic pipe loader. It supports Intel
915/945/G33/Q33/Q35/Pineview chips.

%description pipe-driver-i915 -l pl.UTF-8
Sterownik i915 dla dynamicznego systemu potoków szkieletu Mesa
Gallium. Obsługuje układy Intela z serii 915/945/G33/Q33/Q35/Pineview.

%package pipe-driver-iris
Summary:	iris driver for Mesa Gallium dynamic pipe loader
Summary(pl.UTF-8):	Sterownik iris dla dynamicznego systemu potoków szkieletu Mesa Gallium
Group:		Libraries
Requires:	zlib >= %{zlib_ver}

%description pipe-driver-iris
iris driver for Mesa Gallium dynamic pipe loader. It supports Intel
Iris (Gen8+) card family (Broadwell, Skylake, Broxton, Kabylake,
Coffeelake, Geminilake, Whiskey Lake, Comet Lake, Cannonlake, Ice
Lake, Elkhart Lake).

%description pipe-driver-iris -l pl.UTF-8
Sterownik iris dla dynamicznego systemu potoków szkieletu Mesa
Gallium. Obsługuje układy Intela z rodziny kart Intel Iris (Gen8+:
Broadwell, Skylake, Broxton, Kabylake, Coffeelake, Geminilake, Whiskey
Lake, Comet Lake, Cannonlake, Ice Lake, Elkhart Lake).

%package pipe-driver-kmsro
Summary:	kmsro driver for Mesa Gallium dynamic pipe loader
Summary(pl.UTF-8):	Sterownik kmsro dla dynamicznego systemu potoków szkieletu Mesa Gallium
Group:		Libraries
Requires:	zlib >= %{zlib_ver}

%description pipe-driver-kmsro
kmsro driver for Mesa Gallium dynamic pipe loader.

%description pipe-driver-kmsro -l pl.UTF-8
Sterownik kmsro dla dynamicznego systemu potoków szkieletu Mesa
Gallium.

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
Obsoletes:	Mesa-gbm-driver-nouveau < 11.1.1
Obsoletes:	Mesa-opencl-driver-nouveau < 9.1

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
Obsoletes:	Mesa-gbm-driver-r300 < 11.1.1
Obsoletes:	Mesa-opencl-driver-r300 < 9.1

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
Obsoletes:	Mesa-gbm-driver-r600 < 11.1.1
Obsoletes:	Mesa-libllvmradeon < 9.2
Obsoletes:	Mesa-opencl-driver-r600 < 9.1

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
Obsoletes:	Mesa-gbm-driver-radeonsi < 11.1.1
Obsoletes:	Mesa-libllvmradeon < 9.2
Obsoletes:	Mesa-opencl-driver-radeonsi < 9.1

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
Obsoletes:	Mesa-gbm-driver-swrast < 11.1.1
Obsoletes:	Mesa-opencl-driver-swrast < 9.1

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
Obsoletes:	Mesa-gbm-driver-vmwgfx < 11.1.1
Obsoletes:	Mesa-opencl-driver-vmwgfx < 9.1

%description pipe-driver-vmwgfx
vmwgfx driver for Mesa Gallium dynamic pipe loader. It supports VMware
virtual video adapter.

%description pipe-driver-vmwgfx -l pl.UTF-8
Sterownik vmwgfx dla dynamicznego systemu potoków szkieletu Mesa
Gallium. Obsługuje wirtualną kartę graficzną VMware.

%package -n libva-driver-gallium
Summary:	VA driver for Gallium State Tracker
Summary(pl.UTF-8):	Sterowniki VA do Gallium
Group:		Libraries
%if %{with gallium_radeon}
Requires:	libva-driver-r600 = %{version}-%{release}
Requires:	libva-driver-radeonsi = %{version}-%{release}
%endif
%if %{with gallium_nouveau}
Requires:	libva-driver-nouveau = %{version}-%{release}
%endif

%description -n libva-driver-gallium
VA drivers for Gallium State Tracker (r600, radeonsi & nouveau).

%description -n libva-driver-gallium -l pl.UTF-8
Sterowniki VA do Gallium (r600, radeonsi & nouveau).

%package -n libva-driver-r600
Summary:	VA driver for ATI Radeon R600 series adapters
Summary(pl.UTF-8):	Sterownik VA dla kart ATI Radeon z serii R600
Group:		Libraries
Requires:	libva >= 1.8.0
Requires:	zlib >= %{zlib_ver}

%description -n libva-driver-r600
VA driver for ATI Radeon R600 series adapters.

%description -n libva-driver-r600 -l pl.UTF-8
Sterownik VA dla kart ATI Radeon z serii R600.

%package -n libva-driver-radeonsi
Summary:	VA driver for ATI Radeon SI adapters
Summary(pl.UTF-8):	Sterownik VA dla kart ATI Radeon SI
Group:		Libraries
Requires:	libva >= 1.8.0
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
Requires:	libva >= 1.8.0
Requires:	zlib >= %{zlib_ver}

%description -n libva-driver-nouveau
VA driver for NVidia adapters.

%description -n libva-driver-nouveau -l pl.UTF-8
Sterownik VA dla kart NVidia.

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
Obsoletes:	Mesa-libllvmradeon < 9.2
Conflicts:	libvdpau-driver-mesa

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
Requires:	libomxil-bellagio
Requires:	libxcb >= 1.13
Requires:	zlib >= %{zlib_ver}
Obsoletes:	omxil-mesa-nouveau < 10.3
Obsoletes:	omxil-mesa-r600 < 10.3
Obsoletes:	omxil-mesa-radeonsi < 10.3

%description -n omxil-mesa
Mesa driver for Bellagio OpenMAX IL API.

%description -n omxil-mesa -l pl.UTF-8
Sterownik Mesa dla API Bellagio OpenMAX IL.

%package vulkan-icd-broadcom
Summary:	v3dv - Mesa Vulkan driver for Raspberry Pi 4
Summary(pl.UTF-8):	v3dv - sterownik Vulkan dla Raspberry Pi 4
License:	MIT
Group:		Libraries
Requires:	libdrm >= %{libdrm_ver}
Requires:	libxcb >= 1.13
Requires:	xorg-lib-libXrandr >= 1.3
Requires:	xorg-lib-libxshmfence >= 1.1
# wayland-client
Requires:	wayland >= %{wayland_ver}
Requires:	zlib >= %{zlib_ver}
Suggests:	vulkan(loader)
Provides:	vulkan(icd) = 1.1.204

%description vulkan-icd-broadcom
v3dv - Mesa Vulkan driver for Raspberry Pi 4.

%description vulkan-icd-broadcom -l pl.UTF-8
v3dv - sterownik Vulkan dla Raspberry Pi 4.

%package vulkan-icd-freedreno
Summary:	turnip - Mesa Vulkan driver for Adreno chips
Summary(pl.UTF-8):	turnip - sterownik Vulkan dla układów Adreno
License:	MIT
Group:		Libraries
Requires:	libdrm >= %{libdrm_ver}
Requires:	libxcb >= 1.13
Requires:	xorg-lib-libXrandr >= 1.3
Requires:	xorg-lib-libxshmfence >= 1.1
# wayland-client
Requires:	wayland >= %{wayland_ver}
Requires:	zlib >= %{zlib_ver}
Suggests:	vulkan(loader)
Provides:	vulkan(icd) = 1.1.204

%description vulkan-icd-freedreno
turnip - Mesa Vulkan driver for Adreno chips.

%description vulkan-icd-freedreno -l pl.UTF-8
turnip - sterownik Vulkan dla układów Adreno.

%package vulkan-icd-powervr
Summary:	powervr - Mesa Vulkan driver for Imagination Technologies Rogue GPUs
Summary(pl.UTF-8):	powervr - sterownik Vulkan dla układów Imagination Technologies Rogue
License:	MIT
Group:		Libraries
Requires:	libdrm >= %{libdrm_ver}
Requires:	libxcb >= 1.13
Requires:	xorg-lib-libXrandr >= 1.3
Requires:	xorg-lib-libxshmfence >= 1.1
# wayland-client
Requires:	wayland >= %{wayland_ver}
Requires:	zlib >= %{zlib_ver}
Suggests:	vulkan(loader)
Provides:	vulkan(icd) = 1.1.204

%description vulkan-icd-powervr
powervr - Mesa Vulkan driver for Imagination Technologies Rogue GPUs.

%description vulkan-icd-powervr -l pl.UTF-8
powervr - sterownik Vulkan dla układów Imagination Technologies Rogue.

%package vulkan-icd-intel
Summary:	Mesa Vulkan driver for Intel GPUs
Summary(pl.UTF-8):	Sterownik Vulkan dla GPU firmy Intel
License:	MIT
Group:		Libraries
Requires:	libdrm >= %{libdrm_ver}
Requires:	libxcb >= 1.13
Requires:	xorg-lib-libXrandr >= 1.3
Requires:	xorg-lib-libxshmfence >= 1.1
# wayland-client
Requires:	wayland >= %{wayland_ver}
Requires:	zlib >= %{zlib_ver}
Suggests:	vulkan(loader)
Provides:	vulkan(icd) = 1.3.204
Obsoletes:	Mesa-vulkan-icd-intel-devel < 21.1.0

%description vulkan-icd-intel
Mesa Vulkan driver for Intel GPUs.

%description vulkan-icd-intel -l pl.UTF-8
Sterownik Vulkan dla GPU Intela.

%package vulkan-icd-lavapipe
Summary:	lavapipe - Mesa software Vulkan driver
Summary(pl.UTF-8):	lavapipe - programowy sterownik Vulkan
License:	MIT
Group:		Libraries
Requires:	libdrm >= %{libdrm_ver}
Requires:	libxcb >= 1.13
Requires:	xorg-lib-libXrandr >= 1.3
Requires:	xorg-lib-libxshmfence >= 1.1
# wayland-client
Requires:	wayland >= %{wayland_ver}
Requires:	zlib >= %{zlib_ver}
Suggests:	vulkan(loader)
Provides:	vulkan(icd) = 1.1.204

%description vulkan-icd-lavapipe
lavapipe - Mesa software Vulkan driver.

%description vulkan-icd-lavapipe -l pl.UTF-8
lavapipe - programowy sterownik Vulkan.

%package vulkan-icd-panfrost
Summary:	panfrost - Mesa Vulkan driver for Mali Midgard and Bifrost GPUs
Summary(pl.UTF-8):	panfrost - sterownik Vulkan dla układów Mali Midgard i Bifrost
License:	MIT
Group:		Libraries
Requires:	libdrm >= %{libdrm_ver}
Requires:	libxcb >= 1.13
Requires:	xorg-lib-libXrandr >= 1.3
Requires:	xorg-lib-libxshmfence >= 1.1
# wayland-client
Requires:	wayland >= %{wayland_ver}
Requires:	zlib >= %{zlib_ver}
Suggests:	vulkan(loader)
Provides:	vulkan(icd) = 1.1.204

%description vulkan-icd-panfrost
panfrost - Mesa Vulkan driver for Mali Midgard and Bifrost GPUs.

%description vulkan-icd-panfrost -l pl.UTF-8
panfrost - sterownik Vulkan dla układów Mali Midgard i Bifrost.

%package vulkan-icd-radeon
Summary:	radv - experimental Mesa Vulkan driver for AMD Radeon GPUs
Summary(pl.UTF-8):	radv - eksperymentalny sterownik Vulkan dla GPU firmy AMD
License:	MIT
Group:		Libraries
Requires:	libdrm >= %{libdrm_ver}
Requires:	libxcb >= 1.13
Requires:	xorg-lib-libXrandr >= 1.3
Requires:	xorg-lib-libxshmfence >= 1.1
# wayland-client
Requires:	wayland >= %{wayland_ver}
Requires:	zlib >= %{zlib_ver}
Suggests:	vulkan(loader)
Provides:	vulkan(icd) = 1.3.204

%description vulkan-icd-radeon
radv - experimental Mesa Vulkan driver for AMD Radeon GPUs.

%description vulkan-icd-radeon -l pl.UTF-8
radv - eksperymentalny sterownik Vulkan dla GPU firmy AMD.

%prep
%setup -q -n mesa-%{version}

%build
%if %{with opencl}
if [ "$(llvm-config --has-rtti)" != "YES" ] ; then
	echo "Clover (gallium OpenCL) requires LLVM with RTTI!"
	exit 1
fi
%endif


gallium_drivers="virgl swrast %{?with_gallium_zink:zink} \
%ifarch %{ix86} %{x8664} x32
svga iris %{?with_gallium_i915:i915} crocus \
%endif
%if %{with gallium_radeon}
r300 r600 radeonsi \
%endif
%if %{with gallium_nouveau}
nouveau
%endif
%ifarch %{arm} aarch64
etnaviv \
freedreno \
lima \
panfrost \
%{?with_gallium_nouveau:tegra} \
v3d \
vc4 \
%endif
"
# TODO: asahi (Apple Silicon) - arm/aarch64?

gallium_drivers=$(echo $gallium_drivers | xargs | tr ' ' ',')

vulkan_drivers="swrast %{?with_radv:amd} \
%ifarch %{ix86} %{x8664} x32
intel \
%endif
%ifarch %{arm} aarch64
freedreno broadcom imagination-experimental panfrost \
%endif
"

vulkan_drivers=$(echo $vulkan_drivers | xargs | tr ' ' ',')

%meson build \
	-Dplatforms=x11%{?with_wayland:,wayland} \
	-Ddri3=enabled \
	-Ddri-drivers-path=%{_libdir}/xorg/modules/dri \
	-Degl=%{?with_egl:enabled}%{!?with_egl:disabled} \
	-Dgallium-drivers=${gallium_drivers} \
	%{?with_hud_extra:-Dgallium-extra-hud=true} \
	-Dgallium-nine=%{?with_nine:true}%{!?with_nine:false} \
	-Dgallium-omx=%{?with_omx:bellagio}%{!?with_omx:disabled} \
%if %{with opencl}
%if %{with ocl_icd}
	-Dgallium-opencl=icd \
%else
	-Dgallium-opencl=standalone \
%endif
%else
	-Dgallium-opencl=disabled \
%endif
	-Dgallium-va=%{?with_va:enabled}%{!?with_va:disabled} \
	%{?with_vdpau:-Dgallium-vdpau=enabled} \
	%{?with_xvmc:-Dgallium-xvmc=enabled} \
	-Dgallium-xa=%{?with_xa:enabled}%{!?with_xa:disabled} \
	-Dgbm=%{?with_gbm:enabled}%{!?with_gbm:disabled} \
	-Dglvnd=%{?with_glvnd:true}%{!?with_glvnd:false} \
	-Dlibunwind=enabled \
	-Dlmsensors=%{?with_lm_sensors:enabled}%{!?with_lm_sensors:disabled} \
	%{?with_opencl_spirv:-Dopencl-spirv=true} \
	-Dosmesa=true \
	-Dselinux=true \
	-Dsse2=%{__true_false sse2} \
	-Dva-libs-path=%{_libdir}/libva/dri \
	-Dvideo-codecs=h264dec,h264enc,h265dec,h265enc,vc1dec \
	-Dvulkan-drivers=${vulkan_drivers} \
	-Dvulkan-icd-dir=/usr/share/vulkan/icd.d \
%ifarch %{arm} aarch64
	-Dfreedreno-virtio=true \
	-Dimagination-srv=true
%endif

%ninja_build -C build

%{?with_tests:%ninja_test -C build}

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

install -d $RPM_BUILD_ROOT%{_libdir}/gbm

# not used externally
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libglapi.so

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

%post	OpenCL-icd -p /sbin/ldconfig
%postun	OpenCL-icd -p /sbin/ldconfig

%post	libOpenCL -p /sbin/ldconfig
%postun	libOpenCL -p /sbin/ldconfig

%post	libgbm -p /sbin/ldconfig
%postun	libgbm -p /sbin/ldconfig

%post	libglapi -p /sbin/ldconfig
%postun	libglapi -p /sbin/ldconfig

%post	libxatracker -p /sbin/ldconfig
%postun	libxatracker -p /sbin/ldconfig

%post	libXvMC-nouveau -p /sbin/ldconfig
%postun	libXvMC-nouveau -p /sbin/ldconfig
%post	libXvMC-r600 -p /sbin/ldconfig
%postun	libXvMC-r600 -p /sbin/ldconfig

### libraries

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
%dir %{_includedir}/EGL
%{_includedir}/EGL/egl.h
%{_includedir}/EGL/eglext.h
%{_includedir}/EGL/eglplatform.h
%{_pkgconfigdir}/egl.pc
%endif
%{_includedir}/EGL/eglextchromium.h
%{_includedir}/EGL/eglmesaext.h
%endif

%files libGL
%defattr(644,root,root,755)
%doc docs/{*.rst,README.UVD,features.txt,relnotes/*.rst}
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
%{_datadir}/drirc.d

%files libGL-devel
%defattr(644,root,root,755)
%doc docs/_extra/specs/*
%if %{without glvnd}
%dir %{_includedir}/GL
%{_includedir}/GL/gl.h
%{_includedir}/GL/glcorearb.h
%{_includedir}/GL/glext.h
%{_includedir}/GL/glx.h
%{_includedir}/GL/glxext.h
%{_pkgconfigdir}/gl.pc
%endif

%files libGLES
%defattr(644,root,root,755)
%if %{without glvnd}
%attr(755,root,root) %{_libdir}/libGLESv1_CM.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libGLESv1_CM.so.1
%attr(755,root,root) %{_libdir}/libGLESv2.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libGLESv2.so.2
%endif

%files libGLES-devel
%defattr(644,root,root,755)
%if %{without glvnd}
%attr(755,root,root) %{_libdir}/libGLESv1_CM.so
%attr(755,root,root) %{_libdir}/libGLESv2.so
%{_includedir}/GLES
%{_includedir}/GLES2
%{_includedir}/GLES3
%{_pkgconfigdir}/glesv1_cm.pc
%{_pkgconfigdir}/glesv2.pc
%endif

%files libOSMesa
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOSMesa.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libOSMesa.so.8

%files libOSMesa-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOSMesa.so
%{_includedir}/GL/osmesa.h
%{_pkgconfigdir}/osmesa.pc

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

%if %{with gbm}
%files libgbm
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgbm.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libgbm.so.1
%dir %{_libdir}/gbm

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

%if %{with egl} && %{without glvnd}
%files khrplatform-devel
%defattr(644,root,root,755)
%dir %{_includedir}/KHR
%{_includedir}/KHR/khrplatform.h
%endif

%files dri-devel
%defattr(644,root,root,755)
%dir %{_includedir}/GL/internal
%{_includedir}/GL/internal/dri_interface.h
%{_pkgconfigdir}/dri.pc

### drivers: XvMC

%if %{with gallium_nouveau}
%files libXvMC-nouveau
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libXvMCnouveau.so.1.*.*
%attr(755,root,root) %ghost %{_libdir}/libXvMCnouveau.so.1
%attr(755,root,root) %{_libdir}/libXvMCnouveau.so
%endif

%if %{with gallium_radeon}
%files libXvMC-r600
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libXvMCr600.so.1.*.*
%attr(755,root,root) %ghost %{_libdir}/libXvMCr600.so.1
%attr(755,root,root) %{_libdir}/libXvMCr600.so
%endif

### drivers: d3d

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

### drivers: dri

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

%ifarch %{ix86} %{x8664} x32
%files dri-driver-intel-i915
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/i915_dri.so

%if %{with gallium}
%files dri-driver-intel-crocus
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/crocus_dri.so

%files dri-driver-intel-iris
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/iris_dri.so
%endif
%endif

%files dri-driver-nouveau
%defattr(644,root,root,755)
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
%ifarch %{arm} aarch64
%files dri-driver-etnaviv
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/etnaviv_dri.so

%files dri-driver-freedreno
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/kgsl_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/msm_dri.so

%files dri-driver-kmsro
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/armada-drm_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/exynos_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/hx8357d_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/ili9225_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/ili9341_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/imx-dcss_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/imx-drm_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/imx-lcdif_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/ingenic-drm_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/kirin_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/komeda_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/mali-dp_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/mcde_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/mediatek_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/meson_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/mi0283qt_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/mxsfb-drm_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/pl111_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/rcar-du_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/repaper_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/rockchip_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/st7586_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/st7735r_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/stm_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/sun4i-drm_dri.so

%files dri-driver-lima
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/lima_dri.so

%files dri-driver-panfrost
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/panfrost_dri.so

%if %{with gallium_nouveau}
%files dri-driver-tegra
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/tegra_dri.so
%endif

%files dri-driver-v3d
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/v3d_dri.so

%files dri-driver-vc4
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/vc4_dri.so
%endif

%files dri-driver-virgl
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/virtio_gpu_dri.so

%ifarch %{ix86} %{x8664} x32
%files dri-driver-vmwgfx
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/vmwgfx_dri.so
%endif

%if %{with gallium_zink}
%files dri-driver-zink
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/zink_dri.so
%endif
%endif

### drivers: pipe

%if %{with gallium}
%if %{with opencl}
%ifarch %{ix86} %{x8664} x32
%files pipe-driver-crocus
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gallium-pipe/pipe_crocus.so

%if %{with gallium_i915}
%files pipe-driver-i915
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gallium-pipe/pipe_i915.so
%endif

%files pipe-driver-iris
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gallium-pipe/pipe_iris.so
%endif

%ifarch %{arm} aarch64
%files pipe-driver-kmsro
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gallium-pipe/pipe_kmsro.so

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

%ifarch %{ix86} %{x8664} x32
%files pipe-driver-vmwgfx
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gallium-pipe/pipe_vmwgfx.so
%endif
%endif
%endif

### drivers: va

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

### drivers: vdpau

%if %{with vdpau}
# ldconfig is not used in vdpau tree, so package all symlinks
%if %{with gallium_nouveau}
%files -n libvdpau-driver-mesa-nouveau
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_nouveau.so.1.0.0
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_nouveau.so.1.0
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_nouveau.so.1
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_nouveau.so
%endif

%if %{with gallium_radeon}
%files -n libvdpau-driver-mesa-r300
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_r300.so.1.0.0
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_r300.so.1.0
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_r300.so.1
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_r300.so

%files -n libvdpau-driver-mesa-r600
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_r600.so.1.0.0
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_r600.so.1.0
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_r600.so.1
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_r600.so

%files -n libvdpau-driver-mesa-radeonsi
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_radeonsi.so.1.0.0
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_radeonsi.so.1.0
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_radeonsi.so.1
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_radeonsi.so
%endif
%endif

### drivers: omxil

%if %{with omx}
%files -n omxil-mesa
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/bellagio/libomx_mesa.so
%endif

### drivers: vulkan

%ifarch %{arm} aarch64
%files vulkan-icd-broadcom
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvulkan_broadcom.so
%{_datadir}/vulkan/icd.d/broadcom_icd.*.json

%files vulkan-icd-freedreno
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvulkan_freedreno.so
%{_datadir}/vulkan/icd.d/freedreno_icd.*.json

%files vulkan-icd-powervr
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpowervr_rogue.so
%attr(755,root,root) %{_libdir}/libvulkan_powervr_mesa.so
%{_datadir}/vulkan/icd.d/powervr_mesa_icd.*.json

%files vulkan-icd-panfrost
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvulkan_panfrost.so
%{_datadir}/vulkan/icd.d/panfrost_icd.*.json
%endif

%ifarch %{ix86} %{x8664} x32
%files vulkan-icd-intel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvulkan_intel.so
%{_datadir}/vulkan/icd.d/intel_icd.*.json
%endif

%files vulkan-icd-lavapipe
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvulkan_lvp.so
%{_datadir}/vulkan/icd.d/lvp_icd.*.json

%if %{with radv}
%files vulkan-icd-radeon
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvulkan_radeon.so
%{_datadir}/vulkan/icd.d/radeon_icd.*.json
%endif
