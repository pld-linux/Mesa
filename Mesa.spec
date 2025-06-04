# TODO:
# - libtizonia >= 0.10.0 as an alternative for bellagio?
# - bcond for perfetto peformance analysis? (BR: perfetto)
#
# Conditional build:
%bcond_without	gallium		# gallium drivers
%bcond_without	gallium_i915	# gallium i915 driver
%bcond_without	gallium_nouveau	# gallium nouveau driver
%bcond_without	gallium_radeon	# gallium radeon drivers
%bcond_without	gallium_rusticl	# gallium OpenCL frontend
%bcond_without	gallium_zink	# gallium zink driver (based on vulkan)
%bcond_without	egl		# EGL libraries
%bcond_without	gbm		# Graphics Buffer Manager
%bcond_without	nine		# Nine Direct3D 9+ state tracker (for Wine)
%bcond_without	opencl		# OpenCL support
%bcond_without	ocl_icd		# OpenCL as ICD (installable client driver)
%bcond_without	glvnd		# OpenGL vendor neutral dispatcher support
%bcond_without	va		# VA library
%bcond_without	wayland		# Wayland EGL
%bcond_without	xa		# XA state tracker (for vmwgfx xorg driver)
%bcond_without	nvk		# nvidia Vulkan driver
%bcond_without	radv		# radeon Vulkan driver
%bcond_without	intel_rt	# Intel Ray Tracing support
%bcond_with	sse2		# SSE2 instructions
%bcond_with	hud_extra	# HUD block/NIC I/O HUD stats support
%bcond_with	lm_sensors	# HUD lm_sensors support
%bcond_with	tests		# tests

%define		syn_crate_ver		2.0.68
%define		unicode_ident_crate_ver	1.0.12
%define		quote_crate_ver		1.0.33
%define		proc_macro2_crate_ver	1.0.86
%define		paste_crate_ver		1.0.14

%define		va_api_version		%(pkg-config --modversion libva 2> /dev/null || echo ERROR)
%define		va_api_major		%(echo %{va_api_version} | cut -d . -f 1)
%define		va_api_minor		%(echo %{va_api_version} | cut -d . -f 2)

#
# glapi version (glapi tables in dri drivers and libglx must be in sync);
# set to current Mesa version on ABI break, when xserver tables get regenerated
# (until they start to be somehow versioned themselves)
%define		glapi_ver		7.1.0
# other packages
%define		libdrm_ver		2.4.121
%define		dri2proto_ver		2.8
%define		glproto_ver		1.4.14
%define		zlib_ver		1.2.8
%define		wayland_ver		1.23
%define		libglvnd_ver		1.3.4-2
%define		llvm_ver		18.0.0
%define		gcc_ver 		6:8

%if %{without gallium}
%undefine	with_gallium_i915
%undefine	with_gallium_nouveau
%undefine	with_gallium_radeon
%undefine	with_gallium_rusticl
%undefine	with_nine
%undefine	with_opencl
%undefine	with_va
%undefine	with_xa
%endif

%if %{without egl}
%undefine	with_gbm
%undefine	with_wayland
%endif

%if %{without opencl}
%undefine	with_gallium_rusticl
%undefine	with_ocl_icd
%endif

%if %{with gallium}
%define		with_vdpau	1
%endif

%ifarch %{x86_with_sse2}
%define		with_sse2	1
%endif

%ifarch %{ix86} %{x8664} x32
%define		with_intel_vk	1
%endif

%ifnarch %{x8664}
%undefine	with_intel_rt
%endif

%if %{with intel_vk} || %{with gallium_rusticl}
%define		with_clc	1
%else
%ifarch %{ix86} %{x8664} x32
%if %{with gallium}
%define		with_clc	1
%endif
%endif
%ifarch aarch64
%define		with_clc	1
%endif
%endif

Summary:	Free OpenGL implementation
Summary(pl.UTF-8):	Wolnodostępna implementacja standardu OpenGL
Name:		Mesa
Version:	25.1.2
Release:	1
License:	MIT (core) and others - see license.html file
Group:		X11/Libraries
Source0:	https://archive.mesa3d.org/mesa-%{version}.tar.xz
# Source0-md5:	5237eaf9fa4691711d2fc03c63539523
Source1:	https://crates.io/api/v1/crates/syn/%{syn_crate_ver}/download?/syn-%{syn_crate_ver}.tar.gz
# Source1-md5:	01a9bc27d9bb67760e8736034737cd20
Source2:	https://crates.io/api/v1/crates/unicode-ident/%{unicode_ident_crate_ver}/download?/unicode-ident-%{unicode_ident_crate_ver}.tar.gz
# Source2-md5:	ca65153603a1a7240bbd9d2ce19f2d67
Source3:	https://crates.io/api/v1/crates/quote/%{quote_crate_ver}/download?/quote-%{quote_crate_ver}.tar.gz
# Source3-md5:	0ddb8bccd3198892d0dd0ec7151f7cd3
Source4:	https://crates.io/api/v1/crates/proc-macro2/%{proc_macro2_crate_ver}/download?/proc-macro2-%{proc_macro2_crate_ver}.tar.gz
# Source4-md5:	480a3b8e8201739e157bb648f9243962
Source5:	https://crates.io/api/v1/crates/paste/%{paste_crate_ver}/download?/paste-%{paste_crate_ver}.tar.gz
# Source5-md5:	1781b204ec7b6b1ef9232d429e6a973a
URL:		https://www.mesa3d.org/
%if %{with gallium_rusticl}
BuildRequires:	SPIRV-LLVM-Translator-devel >= 8.0.1.3
%endif
%{?with_gallium_zink:BuildRequires:	Vulkan-Loader-devel}
BuildRequires:	bison >= 2.4.1
%if %{with gallium_rusticl} || %{with nvk}
BuildRequires:	clang >= %{llvm_ver}
%endif
%{?with_opencl:BuildRequires:	clang-devel >= %{llvm_ver}}
BuildRequires:	elfutils-devel
BuildRequires:	expat-devel >= 1.95
BuildRequires:	flex >= 2.5.35
BuildRequires:	gcc >= %{gcc_ver}
BuildRequires:	glslang >= 11.3.0
%ifnarch %{arch_with_atomics64}
BuildRequires:	libatomic-devel
%endif
BuildRequires:	libdrm-devel >= %{libdrm_ver}
%{?with_glvnd:BuildRequires:	libglvnd-devel >= %{libglvnd_ver}}
BuildRequires:	libstdc++-devel >= %{gcc_ver}
BuildRequires:	libunwind-devel
%{?with_va:BuildRequires:	libva-devel}
%{?with_va:BuildRequires:	pkgconfig(libva) >= 1.8.0}
%{?with_vdpau:BuildRequires:	libvdpau-devel >= 1.5}
BuildRequires:	libxcb-devel >= 1.17
BuildRequires:	llvm-devel >= %{llvm_ver}
%if %{with opencl} || %{with clc}
BuildRequires:	llvm-libclc
%endif
BuildRequires:	meson >= 1.4.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(talloc) >= 2.0.1
BuildRequires:	pkgconfig(xcb-dri2) >= 1.8
BuildRequires:	pkgconfig(xcb-dri3) >= 1.17
BuildRequires:	pkgconfig(xcb-glx) >= 1.8.1
BuildRequires:	pkgconfig(xcb-present) >= 1.17
BuildRequires:	pkgconfig(xcb-randr) >= 1.12
BuildRequires:	python3 >= 1:3.2
BuildRequires:	python3-Mako >= 0.8.0
BuildRequires:	python3-PyYAML
%ifarch %{arm} aarch64
BuildRequires:	python3-pycparser >= 2.20
%endif
BuildRequires:	rpmbuild(macros) >= 2.042
%if %{with gallium_rusticl} || %{with nvk}
BuildRequires:	rust >= 1.76.0
%endif
%if %{with gallium_rusticl} || %{with nvk}
BuildRequires:	rust-bindgen >= 0.65.0
%endif
%{?with_nvk:BuildRequires:	rust-cbindgen >= 0.25}
BuildRequires:	sed >= 4.0
%if %{with clc}
BuildRequires:	spirv-tools-devel >= 2024.3
%endif
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel
# wayland-{client,server}
%{?with_wayland:BuildRequires:	wayland-devel >= %{wayland_ver}}
%{?with_wayland:BuildRequires:	wayland-protocols >= 1.41}
%{?with_wayland:BuildRequires:	wayland-egl-devel >= %{wayland_ver}}
BuildRequires:	xcb-util-keysyms-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel >= 1.0.5
BuildRequires:	xorg-lib-libXfixes-devel >= 2.0
BuildRequires:	xorg-lib-libXrandr-devel >= 1.3
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

# libGLESv1_CM, libGLESv2, libGL, libEGL:
#  _glapi_tls_Dispatch is defined in libglapi, but it's some kind of symbol ldd -r doesn't notice(?)
%define		skip_post_check_so	libGLESv1_CM.so.1.* libGLESv2.so.2.* libGL.so.1.* libEGL_mesa.so.0.* libGLX_mesa.so.0.*

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
Requires:	libdrm%{?_isa} >= %{libdrm_ver}
Requires:	libxcb%{?_isa} >= 1.17
%{?with_wayland:Requires:	wayland%{?_isa} >= %{wayland_ver}}
Requires:	%{name}-libgallium%{?_isa} = %{version}-%{release}
%if %{with gbm}
Requires:	%{name}-libgbm%{?_isa} = %{version}-%{release}
%endif
%if %{with glvnd}
Requires:	libglvnd-libEGL%{?_isa} >= %{libglvnd_ver}
%endif
Provides:	EGL = 1.5
%{?with_glvnd:Provides:	glvnd(EGL)%{?_isa}}

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
Requires:	%{name}-libEGL%{?_isa} = %{version}-%{release}
Requires:	xorg-lib-libX11-devel%{?_isa}
%if %{with glvnd}
Requires:	libglvnd-libEGL-devel%{?_isa} >= %{libglvnd_ver}
%else
Requires:	%{name}-khrplatform-devel%{?_isa} = %{version}-%{release}
Requires:	libdrm-devel%{?_isa} >= %{libdrm_ver}
Requires:	libxcb-devel%{?_isa} >= 1.17
Requires:	pkgconfig(xcb-dri2) >= 1.8
Requires:	pkgconfig(xcb-glx) >= 1.8.1
Requires:	xorg-lib-libXext-devel%{?_isa} >= 1.0.5
Requires:	xorg-lib-libXfixes-devel%{?_isa} >= 2.0
Requires:	xorg-lib-libXxf86vm-devel%{?_isa}
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
Requires:	%{name}-libgallium%{?_isa} = %{version}-%{release}
Requires:	libdrm%{?_isa} >= %{libdrm_ver}
Requires:	libxcb%{?_isa} >= 1.17
%if %{with glvnd}
Requires:	libglvnd-libGL%{?_isa} >= %{libglvnd_ver}
%endif
Provides:	OpenGL = 4.6
Provides:	OpenGL-GLX = 1.4
%{?with_glvnd:Provides:	glvnd(GL)%{?_isa}}
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
Requires:	libglvnd-libGL-devel%{?_isa} >= %{libglvnd_ver}
%else
Requires:	%{name}-khrplatform-devel%{?_isa} = %{version}-%{release}
Requires:	%{name}-libGL%{?_isa} = %{version}-%{release}
Requires:	libdrm-devel%{?_isa} >= %{libdrm_ver}
Requires:	libxcb-devel%{?_isa} >= 1.17
Requires:	pkgconfig(xcb-dri2) >= 1.8
Requires:	pkgconfig(xcb-glx) >= 1.8.1
Requires:	xorg-lib-libX11-devel%{?_isa}
Requires:	xorg-lib-libXext-devel%{?_isa} >= 1.0.5
Requires:	xorg-lib-libXfixes-devel%{?_isa} >= 2.0
Requires:	xorg-lib-libXxf86vm-devel%{?_isa}
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
%if %{with glvnd}
Requires:	libglvnd-libGLES%{?_isa} >= %{libglvnd_ver}
%endif
Provides:	OpenGLES
Provides:	OpenGLESv1 = 1.1
Provides:	OpenGLESv2 = 2.0
Provides:	OpenGLESv3 = 3.2
%{?with_glvnd:Provides:	glvnd(GLES)%{?_isa}}

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
Requires:	%{name}-libGLES%{?_isa} = %{version}-%{release}
%if %{with glvnd}
Requires:	libglvnd-libGLES-devel%{?_isa} >= %{libglvnd_ver}
%else
Requires:	%{name}-khrplatform-devel%{?_isa} = %{version}-%{release}
# <EGL/egl.h> for <GLES/egl.h>
Requires:	%{name}-libEGL-devel%{?_isa} = %{version}-%{release}
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

%package OpenCL-icd
Summary:	Mesa implementation of OpenCL (Compuing Language) API ICD
Summary(pl.UTF-8):	Implementacja Mesa API OpenCL (języka obliczeń) ICD
License:	MIT
Group:		Libraries
Requires:	filesystem >= 4.0-29
Requires:	libdrm%{?_isa} >= %{libdrm_ver}
Requires:	llvm-libclc
Requires:	zlib%{?_isa} >= %{zlib_ver}
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
Requires:	libdrm%{?_isa} >= %{libdrm_ver}
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
Requires:	%{name}-libOpenCL%{?_isa} = %{version}-%{release}
Provides:	OpenCL-devel = 1.2

%description libOpenCL-devel
Header files for Mesa OpenCL library.

%description libOpenCL-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Mesa OpenCL.

%package Rusticl-icd
Summary:	Rusticl implementation of OpenCL (Compuing Language) API ICD
Summary(pl.UTF-8):	Implementacja Rusticl API OpenCL (języka obliczeń) ICD
License:	MIT
Group:		Libraries
Requires:	filesystem >= 4.0-29
Requires:	libdrm%{?_isa} >= %{libdrm_ver}
Requires:	llvm-libclc
Requires:	zlib%{?_isa} >= %{zlib_ver}
Provides:	OpenCL = 3.0
Provides:	ocl-icd-driver

%description Rusticl-icd
This package contains Rusticl implementation of OpenCL - standard for
cross-platform, parallel programming of modern processors found in
personal computers, servers and handheld/embedded devices. OpenCL
specification can be found on Khronos Group site:
<http://www.khronos.org/opencl/>. Rusticl implements OpenCL 3.0.

The implementation is provided as an installable client driver (ICD)
for use with the ocl-icd loader.

%description Rusticl-icd -l pl.UTF-8
Ten pakiet zawiera implementację Rusticl standardu OpenCL - standardu
wieloplatformowego, równoległego programowania nowoczesnych
procesorów, jakie znajdują się w komputerach osobistych, serwerach
oraz urządzeniach przenośnych/wbudowanych. Specyfikację OpenCL można
znaleźć na stronie Khronos Group: <http://www.khronos.org/opencl/>.
Rusticl zawiera implementację OpenCL w wersji 3.0.

Implementacja dostarczona jest w postaci instalowalnego sterownika
klienta (ICD), który może być użyty z loaderem ocl-icd.

%package libgallium
Summary:	Common Mesa Gallium library
Summary(pl.UTF-8):	Wspólna biblioteka Mesa Gallium
Group:		Libraries
Requires:	libdrm%{?_isa} >= %{libdrm_ver}
Requires:	zlib%{?_isa} >= %{zlib_ver}
Provides:	Mesa-libglapi = %{version}-%{release}
Obsoletes:	Mesa-libglapi < 25.0.0

%description libgallium
Common Mesa Gallium library.

%description libgallium -l pl.UTF-8
Wspólna biblioteka Mesa Gallium.

%package libgbm
Summary:	Mesa Graphics Buffer Manager library
Summary(pl.UTF-8):	Biblioteka Mesa Graphics Buffer Manager
Group:		Libraries
Suggests:	libgbm(backend)%{?_isa}
Conflicts:	Mesa-libEGL < 8.0.1-2

%description libgbm
Mesa Graphics Buffer Manager library.

%description libgbm -l pl.UTF-8
Biblioteka Mesa Graphics Buffer Manager (zarządcy bufora graficznego).

%package libgbm-backend-dri
Summary:	DRI backend for libgbm library
Summary(pl.UTF-8):	Backend DRI dla biblioteki libgbm
Group:		Libraries
Requires:	%{name}-libgallium%{?_isa} = %{version}-%{release}
Provides:	libgbm(backend)%{?_isa}

%description libgbm-backend-dri
DRI backend for libgbm library.

%description libgbm-backend-dri -l pl.UTF-8
Backend DRI dla biblioteki libgbm.

%package libgbm-devel
Summary:	Header file for Mesa Graphics Buffer Manager library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki Mesa Graphics Buffer Manager
Group:		Development/Libraries
Requires:	%{name}-libgbm%{?_isa} = %{version}-%{release}

%description libgbm-devel
Header file for Mesa Graphics Buffer Manager library.

%description libgbm-devel -l pl.UTF-8
Plik nagłówkowy biblioteki Mesa Graphics Buffer Manager (zarządcy
bufora graficznego).

%package libxatracker
Summary:	Xorg Gallium3D accelleration library
Summary(pl.UTF-8):	Biblioteka akceleracji Gallium3D dla Xorg
Group:		X11/Libraries
Requires:	libdrm%{?_isa} >= %{libdrm_ver}
Requires:	zlib%{?_isa} >= %{zlib_ver}

%description libxatracker
Xorg Gallium3D accelleration library (used by new vmwgfx driver).

%description libxatracker -l pl.UTF-8
Biblioteka akceleracji Gallium3D dla Xorg (używana przez nowy
sterownik vmwgfx).

%package libxatracker-devel
Summary:	Header files for Xorg Gallium3D accelleration library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki akceleracji Gallium3D dla Xorg
Group:		X11/Development/Libraries
Requires:	%{name}-libxatracker%{?_isa} = %{version}-%{release}
Requires:	libdrm-devel%{?_isa} >= %{libdrm_ver}

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
Requires:	libdrm-devel%{?_isa} >= %{libdrm_ver}
# <GL/gl.h>
%if %{with glvnd}
Requires:	libglvnd-libGL-devel%{?_isa} >= %{libglvnd_ver}
Conflicts:	Mesa-libGL-devel < 21.1.0-2
%else
Requires:	Mesa-libGL-devel%{?_isa} = %{version}-%{release}
%endif

%description dri-devel
Direct Rendering Infrastructure interface header file.

%description dri-devel -l pl.UTF-8
Plik nagłówkowy interfejsu DRI (Direct Rendering Infrastructure).

%package d3d
Summary:	Nine Direct3D9 driver (for Wine)
Summary(pl.UTF-8):	Sterownik Direct3D9 Nine (dla Wine)
Group:		Libraries
Requires:	libdrm%{?_isa} >= %{libdrm_ver}
Requires:	zlib%{?_isa} >= %{zlib_ver}

%description d3d
Nine Direct3D9 driver (for Wine).

%description d3d -l pl.UTF-8
Sterownik Direct3D9 Nine (dla Wine).

%package d3d-devel
Summary:	Nine Direct3D9 driver API
Summary(pl.UTF-8):	API sterownika Direct3D9 Nine
Group:		Development/Libraries
Requires:	libdrm-devel%{?_isa} >= %{libdrm_ver}

%description d3d-devel
Nine Direct3D9 driver API.

%description d3d-devel -l pl.UTF-8
API sterownika Direct3D9 Nine.

%package dri-driver
Summary:	X.org DRI driver
Summary(pl.UTF-8):	Sterownik X.org DRI
License:	MIT
Group:		X11/Libraries
Requires:	zlib%{?_isa} >= %{zlib_ver}
%if %{with gallium_radeon}
Provides:	Mesa-dri-driver-ati-radeon-R300 = %{version}
Provides:	Mesa-dri-driver-ati-radeon-R600 = %{version}
Provides:	Mesa-dri-driver-ati-radeon-SI = %{version}
%endif
Provides:	Mesa-dri-driver-intel-crocus = %{version}
%if %{with gallium_i915}
Provides:	Mesa-dri-driver-intel-i915 = %{version}
%endif
Provides:	Mesa-dri-driver-intel-iris = %{version}
%if %{with gallium_nouveau}
Provides:	Mesa-dri-driver-nouveau = %{version}
%endif
Provides:	Mesa-dri-driver-swrast = %{version}
Provides:	Mesa-dri-driver-virgl = %{version}
Provides:	Mesa-dri-driver-vmwgfx = %{version}
%if %{with gallium_zink}
Provides:	Mesa-dri-driver-zink = %{version}
%endif
%ifarch %{arm} aarch64
Provides:	Mesa-dri-driver-etnaviv = %{version}
Provides:	Mesa-dri-driver-freedreno = %{version}
Provides:	Mesa-dri-driver-kmsro = %{version}
Provides:	Mesa-dri-driver-lima = %{version}
Provides:	Mesa-dri-driver-panfrost = %{version}
Provides:	Mesa-dri-driver-panthor = %{version}
%if %{with gallium_nouveau}
Provides:	Mesa-dri-driver-tegra = %{version}
%endif
Provides:	Mesa-dri-driver-v3d = %{version}
Provides:	Mesa-dri-driver-vc4 = %{version}
%endif
Obsoletes:	Mesa-dri-driver-ati-radeon-R300 < 24.2.0
Obsoletes:	Mesa-dri-driver-ati-radeon-R600 < 24.2.0
Obsoletes:	Mesa-dri-driver-ati-radeon-SI < 24.2.0
Obsoletes:	Mesa-dri-driver-etnaviv < 24.2.0
Obsoletes:	Mesa-dri-driver-freedreno < 24.2.0
Obsoletes:	Mesa-dri-driver-intel-crocus < 24.2.0
Obsoletes:	Mesa-dri-driver-intel-i830 < 6.5
Obsoletes:	Mesa-dri-driver-intel-i915 < 24.2.0
Obsoletes:	Mesa-dri-driver-intel-i965 < 22.0.0
Obsoletes:	Mesa-dri-driver-intel-iris < 24.2.0
Obsoletes:	Mesa-dri-driver-kmsro < 24.2.0
Obsoletes:	Mesa-dri-driver-lima < 24.2.0
Obsoletes:	Mesa-dri-driver-nouveau < 24.2.0
Obsoletes:	Mesa-dri-driver-panfrost < 24.2.0
Obsoletes:	Mesa-dri-driver-panthor < 24.2.0
Obsoletes:	Mesa-dri-driver-swrast < 24.2.0
Obsoletes:	Mesa-dri-driver-tegra < 24.2.0
Obsoletes:	Mesa-dri-driver-v3d < 24.2.0
Obsoletes:	Mesa-dri-driver-vc4 < 24.2.0
Obsoletes:	Mesa-dri-driver-virgl < 24.2.0
Obsoletes:	Mesa-dri-driver-vmwgfx < 24.2.0
Obsoletes:	Mesa-dri-driver-zink < 24.2.0
Obsoletes:	X11-driver-i810-dri < 1:7.0.0
Obsoletes:	X11-driver-radeon-dri < 1:7.0.0
Conflicts:	%{name}-libEGL%{?_isa} > %{version}
Conflicts:	%{name}-libEGL%{?_isa} < %{version}
Conflicts:	%{name}-libGL%{?_isa} > %{version}
Conflicts:	%{name}-libGL%{?_isa} < %{version}
Conflicts:	%{name}-libgbm%{?_isa} > %{version}
Conflicts:	%{name}-libgbm%{?_isa} < %{version}
Conflicts:	xorg-xserver-libglx(glapi) > %{glapi_ver}
Conflicts:	xorg-xserver-libglx(glapi) < %{glapi_ver}

%description dri-driver
X.org Gallium DRI driver.

%description dri-driver -l pl.UTF-8
Sterownik X.org DRI Gallium.

%package pipe-driver-crocus
Summary:	crocus driver for Mesa Gallium dynamic pipe loader
Summary(pl.UTF-8):	Sterownik crocus dla dynamicznego systemu potoków szkieletu Mesa Gallium
Group:		Libraries
Requires:	zlib%{?_isa} >= %{zlib_ver}

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
Requires:	zlib%{?_isa} >= %{zlib_ver}
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
Requires:	zlib%{?_isa} >= %{zlib_ver}

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
Requires:	zlib%{?_isa} >= %{zlib_ver}

%description pipe-driver-kmsro
kmsro driver for Mesa Gallium dynamic pipe loader.

%description pipe-driver-kmsro -l pl.UTF-8
Sterownik kmsro dla dynamicznego systemu potoków szkieletu Mesa
Gallium.

%package pipe-driver-msm
Summary:	msm (freedreno) driver for Mesa Gallium dynamic pipe loader
Summary(pl.UTF-8):	Sterownik msm (freedreno) dla dynamicznego systemu potoków szkieletu Mesa Gallium
Group:		Libraries
Requires:	zlib%{?_isa} >= %{zlib_ver}

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
Requires:	zlib%{?_isa} >= %{zlib_ver}
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
Requires:	zlib%{?_isa} >= %{zlib_ver}
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
Requires:	zlib%{?_isa} >= %{zlib_ver}
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
Requires:	zlib%{?_isa} >= %{zlib_ver}
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
Requires:	zlib%{?_isa} >= %{zlib_ver}
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
Requires:	zlib%{?_isa} >= %{zlib_ver}
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
Requires:	%{name}-libgallium%{?_isa} = %{version}-%{release}
Requires:	libva(va-api)%{?_isa} >= %{va_api_major}.%{va_api_minor}
%if %{with va}
%if %{with gallium_nouveau}
Provides:	libva-driver-nouveau = %{version}
%endif
%if %{with gallium_radeon}
Provides:	libva-driver-r600 = %{version}
Provides:	libva-driver-radeonsi = %{version}
%endif
Provides:	libva-driver-virtio = %{version}
%endif
Obsoletes:	libva-driver-nouveau < 24.2.0
Obsoletes:	libva-driver-r600 < 24.2.0
Obsoletes:	libva-driver-radeonsi < 24.2.0
Obsoletes:	libva-driver-virtio < 24.2.0

%description -n libva-driver-gallium
VA drivers for Gallium State Tracker.

%description -n libva-driver-gallium -l pl.UTF-8
Sterowniki VA do Gallium.

%package -n libvdpau-driver-gallium
Summary:	Mesa Gallium driver for the vdpau API
Summary(pl.UTF-8):	Sterownik Mesa Gallium dla API vdpau
License:	MIT
Group:		X11/Libraries
Requires:	%{name}-libgallium%{?_isa} = %{version}-%{release}
Requires:	libvdpau%{?_isa} >= 1.5
%if %{with vdpau}
%if %{with gallium_nouveau}
Provides:	libvdpau-driver-mesa-nouveau = %{version}
%endif
%if %{with gallium_radeon}
Provides:	libvdpau-driver-mesa-r600 = %{version}
Provides:	libvdpau-driver-mesa-radeonsi = %{version}
%endif
%endif
Provides:	libvdpau-driver-mesa-virtio = %{version}
Obsoletes:	libvdpau-driver-mesa-nouveau < 24.2.0
Obsoletes:	libvdpau-driver-mesa-r600 < 24.2.0
Obsoletes:	libvdpau-driver-mesa-radeonsi < 24.2.0
Obsoletes:	libvdpau-driver-mesa-virtio < 24.2.0

%description -n libvdpau-driver-gallium
Mesa Gallium driver for the vdpau API.

%description -n libvdpau-driver-gallium -l pl.UTF-8
Sterownik Mesa Gallium dla API vdpau.

%package vulkan-icd-asahi
Summary:	asahi - Mesa Vulkan driver for Apple M1
Summary(pl.UTF-8):	asahi - sterownik Vulkan dla Apple M1
License:	MIT
Group:		Libraries
Requires:	libdrm%{?_isa} >= %{libdrm_ver}
Requires:	libxcb%{?_isa} >= 1.17
Requires:	xorg-lib-libXrandr%{?_isa} >= 1.3
Requires:	xorg-lib-libxshmfence%{?_isa} >= 1.1
# wayland-client
Requires:	wayland%{?_isa} >= %{wayland_ver}
Requires:	zlib%{?_isa} >= %{zlib_ver}
Suggests:	vulkan(loader)
Provides:	vulkan(icd) = 1.0.289

%description vulkan-icd-asahi
asahi - Mesa Vulkan driver for Apple M1.

%description vulkan-icd-asahi -l pl.UTF-8
asahi - sterownik Vulkan dla Apple M1.

%package vulkan-icd-broadcom
Summary:	v3dv - Mesa Vulkan driver for Raspberry Pi 4
Summary(pl.UTF-8):	v3dv - sterownik Vulkan dla Raspberry Pi 4
License:	MIT
Group:		Libraries
Requires:	libdrm%{?_isa} >= %{libdrm_ver}
Requires:	libxcb%{?_isa} >= 1.17
Requires:	xorg-lib-libXrandr%{?_isa} >= 1.3
Requires:	xorg-lib-libxshmfence%{?_isa} >= 1.1
# wayland-client
Requires:	wayland%{?_isa} >= %{wayland_ver}
Requires:	zlib%{?_isa} >= %{zlib_ver}
Suggests:	vulkan(loader)
Provides:	vulkan(icd) = 1.2.289

%description vulkan-icd-broadcom
v3dv - Mesa Vulkan driver for Raspberry Pi 4.

%description vulkan-icd-broadcom -l pl.UTF-8
v3dv - sterownik Vulkan dla Raspberry Pi 4.

%package vulkan-icd-freedreno
Summary:	turnip - Mesa Vulkan driver for Adreno chips
Summary(pl.UTF-8):	turnip - sterownik Vulkan dla układów Adreno
License:	MIT
Group:		Libraries
Requires:	libdrm%{?_isa} >= %{libdrm_ver}
Requires:	libxcb%{?_isa} >= 1.17
Requires:	xorg-lib-libXrandr%{?_isa} >= 1.3
Requires:	xorg-lib-libxshmfence%{?_isa} >= 1.1
# wayland-client
Requires:	wayland%{?_isa} >= %{wayland_ver}
Requires:	zlib%{?_isa} >= %{zlib_ver}
Suggests:	vulkan(loader)
Provides:	vulkan(icd) = 1.1.289

%description vulkan-icd-freedreno
turnip - Mesa Vulkan driver for Adreno chips.

%description vulkan-icd-freedreno -l pl.UTF-8
turnip - sterownik Vulkan dla układów Adreno.

%package vulkan-icd-panfrost
Summary:	panfrost - Mesa Vulkan driver for Mali Midgard and Bifrost GPUs
Summary(pl.UTF-8):	panfrost - sterownik Vulkan dla układów Mali Midgard i Bifrost
License:	MIT
Group:		Libraries
Requires:	libdrm%{?_isa} >= %{libdrm_ver}
Requires:	libxcb%{?_isa} >= 1.17
Requires:	xorg-lib-libXrandr%{?_isa} >= 1.3
Requires:	xorg-lib-libxshmfence%{?_isa} >= 1.1
# wayland-client
Requires:	wayland%{?_isa} >= %{wayland_ver}
Requires:	zlib%{?_isa} >= %{zlib_ver}
Suggests:	vulkan(loader)
Provides:	vulkan(icd) = 1.0.289

%description vulkan-icd-panfrost
panfrost - Mesa Vulkan driver for Mali Midgard and Bifrost GPUs.

%description vulkan-icd-panfrost -l pl.UTF-8
panfrost - sterownik Vulkan dla układów Mali Midgard i Bifrost.

%package vulkan-icd-powervr
Summary:	powervr - Mesa Vulkan driver for Imagination Technologies Rogue GPUs
Summary(pl.UTF-8):	powervr - sterownik Vulkan dla układów Imagination Technologies Rogue
License:	MIT
Group:		Libraries
Requires:	libdrm%{?_isa} >= %{libdrm_ver}
Requires:	libxcb%{?_isa} >= 1.17
Requires:	xorg-lib-libXrandr%{?_isa} >= 1.3
Requires:	xorg-lib-libxshmfence%{?_isa} >= 1.1
# wayland-client
Requires:	wayland%{?_isa} >= %{wayland_ver}
Requires:	zlib%{?_isa} >= %{zlib_ver}
Suggests:	vulkan(loader)
Provides:	vulkan(icd) = 1.0.289

%description vulkan-icd-powervr
powervr - Mesa Vulkan driver for Imagination Technologies Rogue GPUs.

%description vulkan-icd-powervr -l pl.UTF-8
powervr - sterownik Vulkan dla układów Imagination Technologies Rogue.

%package vulkan-icd-intel
Summary:	Mesa Vulkan driver for Intel GPUs
Summary(pl.UTF-8):	Sterownik Vulkan dla GPU firmy Intel
License:	MIT
Group:		Libraries
Requires:	libdrm%{?_isa} >= %{libdrm_ver}
Requires:	libxcb%{?_isa} >= 1.17
Requires:	xorg-lib-libxshmfence%{?_isa} >= 1.1
# wayland-client
Requires:	wayland%{?_isa} >= %{wayland_ver}
Requires:	zlib%{?_isa} >= %{zlib_ver}
Suggests:	vulkan(loader)
Provides:	vulkan(icd) = 1.3.289
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
Requires:	libdrm%{?_isa} >= %{libdrm_ver}
Requires:	libxcb%{?_isa} >= 1.17
Requires:	xorg-lib-libXrandr%{?_isa} >= 1.3
Requires:	xorg-lib-libxshmfence%{?_isa} >= 1.1
# wayland-client
Requires:	wayland%{?_isa} >= %{wayland_ver}
Requires:	zlib%{?_isa} >= %{zlib_ver}
Suggests:	vulkan(loader)
Provides:	vulkan(icd) = 1.3.289

%description vulkan-icd-lavapipe
lavapipe - Mesa software Vulkan driver.

%description vulkan-icd-lavapipe -l pl.UTF-8
lavapipe - programowy sterownik Vulkan.

%package vulkan-icd-nouveau
Summary:	nvk - experimental Mesa Vulkan driver for NVIDIA GPUs
Summary(pl.UTF-8):	nvk - eksperymentalny sterownik Vulkan dla GPU firmy NVIDIA
License:	MIT
Group:		Libraries
Requires:	libdrm%{?_isa} >= %{libdrm_ver}
Requires:	libxcb%{?_isa} >= 1.17
Requires:	xorg-lib-libxshmfence%{?_isa} >= 1.1
# wayland-client
Requires:	wayland%{?_isa} >= %{wayland_ver}
Requires:	zlib%{?_isa} >= %{zlib_ver}
Suggests:	vulkan(loader)
Provides:	vulkan(icd) = 1.3.289

%description vulkan-icd-nouveau
nvk - experimental Mesa Vulkan driver for NVIDIA GPUs.

%description vulkan-icd-nouveau -l pl.UTF-8
nvk - eksperymentalny sterownik Vulkan dla GPU firmy NVIDIA.

%package vulkan-icd-radeon
Summary:	radv - Mesa Vulkan driver for AMD Radeon GPUs
Summary(pl.UTF-8):	radv - sterownik Vulkan dla GPU firmy AMD
License:	MIT
Group:		Libraries
Requires:	libdrm%{?_isa} >= %{libdrm_ver}
Requires:	libxcb%{?_isa} >= 1.17
Requires:	xorg-lib-libxshmfence%{?_isa} >= 1.1
# wayland-client
Requires:	wayland%{?_isa} >= %{wayland_ver}
Requires:	zlib%{?_isa} >= %{zlib_ver}
Suggests:	vulkan(loader)
Provides:	vulkan(icd) = 1.3.289

%description vulkan-icd-radeon
radv - Mesa Vulkan driver for AMD Radeon GPUs.

%description vulkan-icd-radeon -l pl.UTF-8
radv - sterownik Vulkan dla GPU firmy AMD.

%package vulkan-icd-virtio
Summary:	Mesa Vulkan driver for VirtIO adapters
Summary(pl.UTF-8):	Sterownik Vulkan dla kart VirtIO
License:	MIT
Group:		Libraries
Requires:	libdrm%{?_isa} >= %{libdrm_ver}
Requires:	libxcb%{?_isa} >= 1.17
Requires:	xorg-lib-libxshmfence%{?_isa} >= 1.1
# wayland-client
Requires:	wayland%{?_isa} >= %{wayland_ver}
Requires:	zlib%{?_isa} >= %{zlib_ver}
Suggests:	vulkan(loader)
Provides:	vulkan(icd) = 1.3.289

%description vulkan-icd-virtio
Mesa Vulkan driver for VirtIO adapters.

%description vulkan-icd-virtio -l pl.UTF-8
Sterownik Vulkan dla kart VirtIO.

%prep
%setup -q -n mesa-%{version}

install -d subprojects/packagecache
cp -p %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} subprojects/packagecache

%build
%if %{with opencl}
if [ "$(llvm-config --has-rtti)" != "YES" ] ; then
	echo "Clover (gallium OpenCL) requires LLVM with RTTI!"
	exit 1
fi
%endif


gallium_drivers="virgl llvmpipe softpipe %{?with_gallium_zink:zink} \
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
%ifarch aarch64
asahi
%endif
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

vulkan_drivers="swrast virtio %{?with_radv:amd} %{?with_intel_vk:intel intel_hasvk} %{?with_nvk:nouveau} \
%ifarch %{arm} aarch64
broadcom freedreno imagination-experimental panfrost \
%ifarch aarch64
asahi
%endif
%endif
"

vulkan_drivers=$(echo $vulkan_drivers | xargs | tr ' ' ',')

%if %{with gallium_rusticl}
%ifarch %{arm32_with_hf}
export BINDGEN_EXTRA_CLANG_ARGS="-mfloat-abi=hard"
%endif
%endif

export RUSTFLAGS="%{rpmrustflags} --target=%rust_target"
%meson \
	--force-fallback-for=syn,unicode-ident,quote,proc-macro2 \
	-Dplatforms=x11%{?with_wayland:,wayland} \
	-Dandroid-libbacktrace=disabled \
	-Ddri-drivers-path=%{_libdir}/xorg/modules/dri \
	-Degl=%{?with_egl:enabled}%{!?with_egl:disabled} \
	-Dexpat=enabled \
	-Dgallium-d3d12-video=disabled \
	-Dgallium-d3d12-graphics=disabled \
	-Dgallium-drivers=${gallium_drivers} \
	%{?with_hud_extra:-Dgallium-extra-hud=true} \
	-Dgallium-nine=%{?with_nine:true}%{!?with_nine:false} \
%if %{with opencl}
%if %{with ocl_icd}
	-Dgallium-opencl=icd \
%else
	-Dgallium-opencl=standalone \
%endif
	%{?with_gallium_rusticl:-Dgallium-rusticl=true -Drust_std=2021} \
%else
	-Dgallium-opencl=disabled \
%endif
	-Dgallium-va=%{?with_va:enabled}%{!?with_va:disabled} \
	%{?with_vdpau:-Dgallium-vdpau=enabled} \
	-Dgallium-xa=%{?with_xa:enabled}%{!?with_xa:disabled} \
	-Dgbm=%{?with_gbm:enabled}%{!?with_gbm:disabled} \
	-Dglvnd=%{?with_glvnd:enabled}%{!?with_glvnd:disabled} \
	-Dintel-rt=%{?with_intel_rt:enabled}%{!?with_intel_rt:disabled} \
	-Dlibunwind=enabled \
	-Dlmsensors=%{?with_lm_sensors:enabled}%{!?with_lm_sensors:disabled} \
	-Dmicrosoft-clc=disabled \
	-Dosmesa=true \
	-Dsse2=%{__true_false sse2} \
	-Dva-libs-path=%{_libdir}/libva/dri \
	-Dvideo-codecs=all \
	-Dvulkan-drivers=${vulkan_drivers} \
	-Dvulkan-icd-dir=/usr/share/vulkan/icd.d \
	-Dxmlconfig=enabled \
%ifarch %{arm} aarch64
	-Dfreedreno-kmds=msm,virtio \
	-Dimagination-srv=true
%endif

%meson_build

%{?with_tests:%meson_test}

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

install -d $RPM_BUILD_ROOT%{_libdir}/gbm

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

%post	OpenCL-icd -p /sbin/ldconfig
%postun	OpenCL-icd -p /sbin/ldconfig

%post	Rusticl-icd -p /sbin/ldconfig
%postun	Rusticl-icd -p /sbin/ldconfig

%post	libOpenCL -p /sbin/ldconfig
%postun	libOpenCL -p /sbin/ldconfig

%post	libgallium -p /sbin/ldconfig
%postun	libgallium -p /sbin/ldconfig

%post	libgbm -p /sbin/ldconfig
%postun	libgbm -p /sbin/ldconfig

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
%dir %{_includedir}/EGL
%{_includedir}/EGL/egl.h
%{_includedir}/EGL/eglext.h
%{_includedir}/EGL/eglplatform.h
%{_pkgconfigdir}/egl.pc
%endif
%{_includedir}/EGL/eglext_angle.h
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

%if %{with opencl}
%if %{with gallium_rusticl}
%files Rusticl-icd
%defattr(644,root,root,755)
/etc/OpenCL/vendors/rusticl.icd
%attr(755,root,root) %{_libdir}/libRusticlOpenCL.so
%attr(755,root,root) %{_libdir}/libRusticlOpenCL.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libRusticlOpenCL.so.1
%endif
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

%files libgallium
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgallium-%{version}.so

%if %{with gbm}
%files libgbm
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgbm.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libgbm.so.1
%dir %{_libdir}/gbm

%files libgbm-backend-dri
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gbm/dri_gbm.so

%files libgbm-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgbm.so
%{_includedir}/gbm.h
%{_includedir}/gbm_backend_abi.h
%{_pkgconfigdir}/gbm.pc
%endif

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

%files dri-driver
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/dri/libdril_dri.so
%if %{with gallium_radeon}
%attr(755,root,root) %{_libdir}/xorg/modules/dri/r300_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/r600_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/radeonsi_dri.so
%endif
%ifarch %{ix86} %{x8664} x32
%attr(755,root,root) %{_libdir}/xorg/modules/dri/i915_dri.so
%if %{with gallium}
%attr(755,root,root) %{_libdir}/xorg/modules/dri/crocus_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/iris_dri.so
%endif
%endif
%if %{with gallium_nouveau}
%attr(755,root,root) %{_libdir}/xorg/modules/dri/nouveau_dri.so
%endif
%if %{with gallium_zink}
%attr(755,root,root) %{_libdir}/xorg/modules/dri/zink_dri.so
%endif
%if %{with gallium}
%attr(755,root,root) %{_libdir}/xorg/modules/dri/kms_swrast_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/swrast_dri.so
%ifarch %{arm} aarch64
%ifarch aarch64
%attr(755,root,root) %{_libdir}/xorg/modules/dri/asahi_dri.so
%endif
%attr(755,root,root) %{_libdir}/xorg/modules/dri/etnaviv_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/kgsl_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/msm_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/apple_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/armada-drm_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/exynos_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/gm12u320_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/hdlcd_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/hx8357d_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/ili9163_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/ili9225_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/ili9341_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/ili9486_dri.so
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
%attr(755,root,root) %{_libdir}/xorg/modules/dri/panel-mipi-dbi_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/pl111_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/rcar-du_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/repaper_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/rockchip_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/rzg2l-du_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/ssd130x_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/st7586_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/st7735r_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/sti_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/stm_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/sun4i-drm_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/udl_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/vkms_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/zynqmp-dpsub_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/lima_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/panfrost_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/panthor_dri.so
%if %{with gallium_nouveau}
%attr(755,root,root) %{_libdir}/xorg/modules/dri/tegra_dri.so
%endif
%attr(755,root,root) %{_libdir}/xorg/modules/dri/v3d_dri.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/vc4_dri.so
%endif
%attr(755,root,root) %{_libdir}/xorg/modules/dri/virtio_gpu_dri.so
%ifarch %{ix86} %{x8664} x32
%attr(755,root,root) %{_libdir}/xorg/modules/dri/vmwgfx_dri.so
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
%attr(755,root,root) %{_libdir}/libva/dri/r600_drv_video.so
%attr(755,root,root) %{_libdir}/libva/dri/radeonsi_drv_video.so
%endif
%if %{with gallium_nouveau}
%attr(755,root,root) %{_libdir}/libva/dri/nouveau_drv_video.so
%endif
%attr(755,root,root) %{_libdir}/libva/dri/virtio_gpu_drv_video.so
%endif


%if %{with vdpau}
# ldconfig is not used in vdpau tree, so package all symlinks
%files -n libvdpau-driver-gallium
%defattr(644,root,root,755)
%if %{with gallium_nouveau}
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_nouveau.so.1.0.0
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_nouveau.so.1.0
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_nouveau.so.1
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_nouveau.so
%endif
%if %{with gallium_radeon}
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_r600.so.1.0.0
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_r600.so.1.0
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_r600.so.1
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_r600.so
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_radeonsi.so.1.0.0
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_radeonsi.so.1.0
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_radeonsi.so.1
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_radeonsi.so
%endif
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_virtio_gpu.so.1.0.0
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_virtio_gpu.so.1.0
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_virtio_gpu.so.1
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_virtio_gpu.so
%endif

### drivers: vulkan

%ifarch %{arm} aarch64
%ifarch aarch64
%files vulkan-icd-asahi
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvulkan_asahi.so
%{_datadir}/vulkan/icd.d/asahi_icd.*.json
%endif

%files vulkan-icd-broadcom
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvulkan_broadcom.so
%{_datadir}/vulkan/icd.d/broadcom_icd.*.json

%files vulkan-icd-freedreno
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvulkan_freedreno.so
%{_datadir}/vulkan/icd.d/freedreno_icd.*.json

%files vulkan-icd-panfrost
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvulkan_panfrost.so
%{_datadir}/vulkan/icd.d/panfrost_icd.*.json

%files vulkan-icd-powervr
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpowervr_rogue.so
%attr(755,root,root) %{_libdir}/libvulkan_powervr_mesa.so
%{_datadir}/vulkan/icd.d/powervr_mesa_icd.*.json
%endif

%ifarch %{ix86} %{x8664} x32
%files vulkan-icd-intel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvulkan_intel.so
%attr(755,root,root) %{_libdir}/libvulkan_intel_hasvk.so
%{_datadir}/vulkan/icd.d/intel_icd.*.json
%{_datadir}/vulkan/icd.d/intel_hasvk_icd.*.json
%endif

%files vulkan-icd-lavapipe
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvulkan_lvp.so
%{_datadir}/vulkan/icd.d/lvp_icd.*.json

%if %{with nvk}
%files vulkan-icd-nouveau
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvulkan_nouveau.so
%{_datadir}/vulkan/icd.d/nouveau_icd.*.json
%endif

%if %{with radv}
%files vulkan-icd-radeon
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvulkan_radeon.so
%{_datadir}/vulkan/icd.d/radeon_icd.*.json
%endif

%files vulkan-icd-virtio
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvulkan_virtio.so
%{_datadir}/vulkan/icd.d/virtio_icd.*.json
