#
# _with_glide: with GLIDE
#
Summary:	Free OpenGL implementation
Summary(pl):	Bezpłatna implementacja standardu OpenGL
Name:		Mesa
Version:	5.0
Release:	1
License:	MIT (core), LGPL (MesaGLU), SGI (GLU,libGLw) and others - see COPYRIGHT file
Group:		X11/Libraries
Source0:	ftp://ftp.sourceforge.net/pub/sourceforge/mesa3d/%{name}Lib-%{version}.tar.bz2
Source1:	ftp://ftp.sourceforge.net/pub/sourceforge/mesa3d/%{name}Demos-%{version}.tar.bz2
Patch0:		%{name}-am.patch
Patch1:		%{name}-ac.patch
Patch2:		%{name}-libGLw.patch
URL:		http://www.mesa3d.org/
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	motif-devel
BuildRequires:	perl
%ifarch %{ix86} alpha
%{?_with_glide:BuildRequires:	Glide3-DRI-devel}
%{?_with_glide:Requires:	Glide3-DRI}
%endif
Provides:	OpenGL
Obsoletes:	XFree86-OpenGL-core XFree86-OpenGL-libs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# avoid XFree86-OpenGL* dependency
# Glide3 can be provided by Glide_V3-DRI or Glide_V5-DRI
%define		_noautoreqdep	libGL.so.1 libGLU.so.1 libOSMesa.so.4   libglide3.so.3

%define		_sysconfdir	/etc/X11

%description
Mesa is a 3-D graphics library with an API which is very similar to
that of OpenGL*. To the extent that Mesa utilizes the OpenGL command
syntax or state machine, it is being used with authorization from
Silicon Graphics, Inc. However, the author makes no claim that Mesa is
in any way a compatible replacement for OpenGL or associated with
Silicon Graphics, Inc. Those who want a licensed implementation of
OpenGL should contact a licensed vendor. This software is distributed
under the terms of the GNU Library General Public License, see the
LICENSE file for details.

- OpenGL(R) is a registered trademark of Silicon Graphics, Inc.

%description -l pl
Mesa jest biblioteką 3D będącą darmowym odpowiednikiem standardu
OpenGL(*).

- OpenGL jest zastrzeżonym znakiem towarowym firmy Silicon Graphics,
  Inc.

%package devel
Summary:	Development environment for Mesa
Summary(pl):	Środowisko programistyczne biblioteki Mesa
Group:		Development/Libraries
Requires:	%{name} = %{version}
Requires:	XFree86-devel
Provides:	OpenGL-devel
Obsoletes:	XFree86-OpenGL-devel

%description devel
Header files and documentation needed for development.

%description devel -l pl
Pliki nagłówkowe i dokumentacja do Mesy.

%package static
Summary:	Mesa static libraries
Summary(pl):	Biblioteki statyczne Mesy
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}
Provides:	OpenGL-static
Obsoletes:	XFree86-OpenGL-static

%description static
The static version of the Mesa libraries.

%description static -l pl
Biblioteki statyczne Mesy.

%package demos
Summary:	Mesa Demos
Summary(pl):	Demonstracje możliwości bibliotek Mesa
Group:		Development/Libraries
Requires:	OpenGL-devel

%description demos
Demonstration programs for the Mesa libraries.

%description demos -l pl
Programy demonstracyjne dla bibliotek Mesa.

%prep
%setup -q -n Mesa-%{version} -b 1
%patch0 -p1
%patch1 -p1
%patch2 -p1

# fix demos
perl -pi -e "s,\.\./images/,%{_examplesdir}/Mesa/images/,g" demos/*

%build
%configure \
	--enable-static \
	--enable-shared \
	--with-ggi="no" \
	--with-svga="no" \
	--disable-ggi-fbdev \
	--disable-ggi-genkgi \
	--enable-optimize \
	%{!?_with_glide:--without-glide} \
%ifarch %{ix86} \
	--enable-x86 \
  %ifarch i586 i686 k6 athlon \
	--enable-mmx \
	--enable-3dnow \
    %ifarch i686 athlon \
	--enable-katmai \
    %else \
	--disable-katmai \
    %endif \
  %else \
	--disable-mmx \
	--disable-3dnow \
  %endif \
%else \
%ifarch sparc \
	--enable-sparc \
%endif \
	--disable-x86 \
	--disable-mmx \
	--disable-3dnow
%endif

%{__make}
	
cd widgets-mesa
%{__autoconf}
%configure \
	--with-motif
%{__make} || :
cd ../widgets-sgi
touch depend
%{__make} dep
%{__make} linux OPTFLAGS="%{rpmcflags}"
cd ..

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_mandir}/man3

SPWD=`pwd`
cd widgets-mesa
%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir}/man3
# Mesa widgets are not binary compatible with SGI ones
cd $RPM_BUILD_ROOT%{_includedir}/GL
mkdir Mesa-widgets
mv -f GLw*.h Mesa*.h Mesa-widgets
cd $SPWD

install widgets-sgi/libGLw* $RPM_BUILD_ROOT%{_libdir}
install widgets-sgi/GLw*.h $RPM_BUILD_ROOT%{_includedir}/GL

install -d $RPM_BUILD_ROOT/usr/src/examples/Mesa
for l in book demos samples xdemos images ; do
	cp -Rf $l $RPM_BUILD_ROOT%{_examplesdir}/Mesa/$l
done
rm -rf $RPM_BUILD_ROOT%{_examplesdir}/Mesa/*/{.deps,CVS,Makefile.{BeOS*,win,cygnus,DJ,dja}}

rm -f docs/*~

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc docs/{CONFORM,COPYRIGHT,README,README.{3DFX,GGI,MITS,QUAKE,THREADS,X11},RELNOTES*,VERSIONS}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mesa.conf
%attr(755,root,root) %{_libdir}/libGL*.so.*.*
%attr(755,root,root) %{_libdir}/libGL.so
%attr(755,root,root) %{_libdir}/libOSMesa.so.*.*

%files devel
%defattr(644,root,root,755)
%doc docs/{DEVINFO,*.spec}
%{_libdir}/libGL.la
%attr(755,root,root) %{_libdir}/libGLU.so
%{_libdir}/libGLU.la
%attr(755,root,root) %{_libdir}/libOSMesa.so
%{_libdir}/libOSMesa.la
%{_libdir}/libGLw.a
%{_libdir}/libMesaGLw*.a
%dir %{_includedir}/GL
%{_includedir}/GL/Mesa-widgets
%{_includedir}/GL/GLwDrawA.h
%{_includedir}/GL/GLwDrawAP.h
%{_includedir}/GL/GLwMDrawA.h
%{_includedir}/GL/GLwMDrawAP.h
%{_includedir}/GL/gl.h
%{_includedir}/GL/glext.h
%{_includedir}/GL/gl_mangle.h
%{_includedir}/GL/glu.h
%{_includedir}/GL/glu_mangle.h
%{_includedir}/GL/glx.h
%{_includedir}/GL/glxext.h
%{_includedir}/GL/glx_mangle.h
%{_includedir}/GL/osmesa.h
%{_includedir}/GL/xmesa.h
%{_includedir}/GL/xmesa_x.h
%{_includedir}/GL/xmesa_xf86.h
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/libGL.a
%{_libdir}/libGLU.a
%{_libdir}/libOSMesa.a

%files demos
%defattr(644,root,root,755)
%{_examplesdir}/Mesa
