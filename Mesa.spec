#
# _without_glide: without GLIDE
#
# _with_dri: add GLX/DRI support (taken from rawhide)
# (does it make any sense? we have XFree86-OpenGL-* packages...)
#
Summary:	Free OpenGL implementation
Summary(pl):	Bezp≥atna implementacja standardu OpenGL
Name:		Mesa
Version:	3.4.2
Release:	4
License:	MIT (core), LGPL (libGLU), SGI (libGLw) and others - see COPYRIGHT file
Group:		X11/Libraries
Group(de):	X11/Libraries
Group(es):	X11/Bibliotecas
Group(fr):	X11/Librairies
Group(pl):	X11/Biblioteki
Group(pt_BR):	X11/Bibliotecas
Group(ru):	X11/‚…¬Ã…œ‘≈À…
Group(uk):	X11/‚¶¬Ã¶œ‘≈À…
Source0:	ftp://ftp.sourceforge.net/pub/sourceforge/mesa3d/%{name}Lib-%{version}.tar.bz2
Source1:	ftp://ftp.sourceforge.net/pub/sourceforge/mesa3d/%{name}Demos-%{version}.tar.bz2
%{?_with_dri:Source2:	XFree86-4.0.2-GLonly.tar.gz}
Patch0:		%{name}-paths.patch
Patch1:		%{name}-badlibtool.patch
Patch2:		%{name}-glibc-2.2.patch
Patch3:		%{name}-am.patch
Patch4:		%{name}-libGLw.patch
%{?_with_dri:Patch5: %{name}-XF86DRI-4.0.2.patch}
Patch6:		%{name}-ac.patch
#PatchX:	%{name}-3.3-glXcontext.patch
URL:		http://www.mesa3d.org/
BuildRequires:	XFree86-devel
BuildRequires:	motif-devel
%{!?_without_glide:BuildRequires:	Glide_V3-DRI-devel}
BuildRequires:	perl
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
Provides:	OpenGL
Obsoletes:	XFree86-OpenGL-core XFree86-OpenGL-libs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libGL.so.1 libGLU.so.1

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

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
Mesa jest bibliotek± 3D bÍd±c± darmowym odpowiednikiem standardu
OpenGL(*).

- OpenGL jest zastrzeøonym znakiem towarowym firmy Silicon Graphics,
  Inc.

%package devel
Summary:	Development environment for Mesa
Summary(pl):	¶rodowisko programistyczne biblioteki Mesa
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Ú¡⁄“¡¬œ‘À¡/‚…¬Ã…œ‘≈À…
Group(uk):	Úœ⁄“œ¬À¡/‚¶¬Ã¶œ‘≈À…
Requires:	%{name} = %{version}
Requires:	XFree86-devel
Provides:	OpenGL-devel
Obsoletes:	XFree86-OpenGL-devel

%description devel
Header files and documentation needed for development.

%description devel -l pl
Pliki nag≥Ûwkowe i dokumentacja do Mesy.

%package static
Summary:	Mesa static libraries
Summary(pl):	Biblioteki statyczne Mesy
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Ú¡⁄“¡¬œ‘À¡/‚…¬Ã…œ‘≈À…
Group(uk):	Úœ⁄“œ¬À¡/‚¶¬Ã¶œ‘≈À…
Requires:	%{name}-devel = %{version}
Provides:	OpenGL-static
Obsoletes:	XFree86-OpenGL-static

%description static
The static version of the Mesa libraries.

%description static -l pl
Biblioteki statyczne Mesy.

%package demos
Summary:	Mesa Demos
Summary(pl):	Demonstracje moøliwo∂ci bibliotek Mesa
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Ú¡⁄“¡¬œ‘À¡/‚…¬Ã…œ‘≈À…
Group(uk):	Úœ⁄“œ¬À¡/‚¶¬Ã¶œ‘≈À…
Requires:	OpenGL-devel

%description demos
Demonstration programs for the Mesa libraries.

%description demos -l pl
Programy demonstracyjne dla bibliotek Mesa.

%prep
%setup -q -n Mesa-%{version} -b 1

%if %{?_with_dri:1}%{!?_with_dri:0}
	mkdir -p src/DRI/GL
	tar xzf %{SOURCE2}
	ln -f `find xc -type f` src/DRI
	mv -f src/DRI/glxmd.h src/DRI/GL/glxmd.h
%endif

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%{?_with_dri:%patch5 -p1}
%patch6 -p1
# fix demos
perl -pi -e "s,\.\./images/,%{_examplesdir}/Mesa/images/,g" demos/*

%build
rm -f missing acinclude.m4
libtoolize --copy --force
aclocal
autoheader
autoconf
automake -a -c
%configure \
	CFLAGS="%{rpmcflags} -I%{_includedir} -I. -I../" \
	AS='%{__cc}' \
	--enable-static \
	--enable-shared \
	--with-ggi="no" \
	--with-svga="no" \
	--disable-ggi-fbdev \
	--disable-ggi-genkgi \
	--enable-optimize \
	%{?_without_glide:--without-glide} \
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
	--disable-x86 \
	--disable-mmx \
	--disable-3dnow
%endif

%{__make}
	
(cd widgets-mesa
%configure \
	--with-motif
%{__make}
)

(cd widgets-sgi
touch depend
%{__make} dep
%{__make} linux OPTFLAGS="%{rpmcflags}"
)

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_mandir}/man3

(cd widgets-mesa
%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir}/man3
# Mesa widgets are not binary compatible with SGI ones
cd $RPM_BUILD_ROOT%{_includedir}/GL
mkdir Mesa-widgets
mv -f GLw*.h Mesa*.h Mesa-widgets
)

install widgets-sgi/libGLw* $RPM_BUILD_ROOT%{_libdir}
install widgets-sgi/GLw*.h $RPM_BUILD_ROOT%{_includedir}/GL

install -d $RPM_BUILD_ROOT/usr/src/examples/Mesa
for l in book demos samples xdemos images ; do
	cp -Rf $l $RPM_BUILD_ROOT%{_examplesdir}/Mesa/$l
done

gzip -9nf docs/*

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -fr $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/CONFIG.gz
%attr(755,root,root) %{_libdir}/libGL*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc docs/{IAFA-PACKAGE,README,RELNOTES-*,VERSIONS,CONFORM,COPYRIGHT,DEVINFO,*.spec}.gz
%doc docs/README.{3DFX,GGI,MITS,QUAKE,X11,THREADS}.gz
%attr(755,root,root) %{_libdir}/libGL*.so
%{_libdir}/libMesaGLw*.a
%{_libdir}/libGLw.a
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

%files demos
%defattr(644,root,root,755)
%dir /usr/src/examples/Mesa
%dir /usr/src/examples/Mesa/book
%dir /usr/src/examples/Mesa/demos
%dir /usr/src/examples/Mesa/samples
%dir /usr/src/examples/Mesa/xdemos

%doc /usr/src/examples/Mesa/book/*
%doc /usr/src/examples/Mesa/demos/*
%doc /usr/src/examples/Mesa/samples/*
%doc /usr/src/examples/Mesa/xdemos/*
