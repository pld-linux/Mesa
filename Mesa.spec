#
# bcond_off_glide: without GLIDE
#
# bcond_on_dri: add GLX/DRI support (taken from rawhide)
# (does it make any sense? we have XFree86-OpenGL-* packages...)
#
Summary:	Free OpenGL implementation
Summary(pl):	Bezpłatna implementacja standardu OpenGL
Name:		Mesa
Version:	3.4.1
Release:	1
License:	GPL
Group:		X11/Libraries
Group(de):	X11/Libraries
Group(es):	X11/Bibliotecas
Group(pl):	X11/Biblioteki
Source0:	ftp://download.sourceforge.net/pub/sourceforge/mesa3d/%{name}Lib-%{version}.tar.bz2
Source1:	ftp://download.sourceforge.net/pub/sourceforge/mesa3d/%{name}Demos-%{version}.tar.bz2
%{?bcond_on_dri:Source2:	XFree86-4.0.2-GLonly.tar.gz}
Patch0:		%{name}-paths.patch
Patch1:		%{name}-badlibtool.patch
Patch2:		%{name}-glibc-2.2.patch
Patch3:		%{name}-am.patch
%{?bcond_on_dri:Patch4:		%{name}-XF86DRI-4.0.2.patch}
#Patch5:	%{name}-3.3-glXcontext.patch
URL:		http://www.mesa3d.org/
BuildRequires:	XFree86-devel
%{!?bcond_off_glide:BuildRequires:	Glide_V3-DRI-devel}
BuildRequires:	perl
BuildRequires:	autoconf
BuildRequires:	automake
Provides:	OpenGL
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Mesa jest biblioteką 3D będącą darmowym odpowiednikiem standardu
OpenGL(*).

- OpenGL jest zastrzeżonym znakiem towarowym firmy Silicon Graphics,
  Inc.

%package devel
Summary:	Development environment for Mesa
Summary(pl):	Środowisko programistyczne biblioteki Mesa
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}
Provides:	OpenGL-devel

%description devel
Header files and documentation needed for development.

%description -l pl devel
Pliki nagłówkowe i dokumentacja do Mesy.

%package static
Summary:	Mesa static libraries
Summary(pl):	Biblioteki statyczne Mesy
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}
Provides:	OpenGL-static

%description static
The static version of the Mesa libraries

%description -l pl static
Biblioteki statyczne Mesy.

%package demos
Summary:	Mesa Demos
Summary(pl):	Demonstracje możliwości biblioteki MESA
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description demos
Demonstration programs for the Mesa libraries.

%description -l pl demos
Programy demonstracyjne dla biblioteki Mesa.

%prep
%setup -q -n Mesa-%{version} -b 1

%if %{?bcond_on_dri:1}%{!?bcond_on_dri:0}
	mkdir -p src/DRI/GL
	tar xzf %{SOURCE2}
	ln -f `find xc -type f` src/DRI
	mv -f src/DRI/glxmd.h src/DRI/GL/glxmd.h
%endif

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%{?bcond_on_dri:%patch4 -p1}
#%patch5 -p1
# fix demos
perl -pi -e "s,\.\./images/,%{_examplesdir}/Mesa/images/,g" demos/*

%build
aclocal -I .
autoheader
automake -a -c
autoconf
%configure \
	--enable-static \
	--enable-shared \
	--with-ggi="no" \
	--with-svga="no" \
	--disable-ggi-fbdev \
	--disable-ggi-genkgi \
	--enable-optimize \
	%{?bcond_off_glide:--without-glide} \
%ifarch %{ix86} \
	--enable-x86 \
  %ifarch i586 i686 \
	--enable-mmx \
	--enable-3dnow \
    %ifarch i686 \
	--enable-katmai \
    %else \
	--disable-katmai \
    %endif \
  %else \
    %ifarch k6 \
	--enable-mmx \
	--enable-3dnow \
    %else \
	--disable-mmx \
	--disable-3dnow \
    %endif \
  %endif \
%else \
	--disable-x86 \
	--disable-mmx \
	--disable-3dnow
%endif

%{__make}
	
(cd widgets-mesa
%configure
%{__make}
)

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_mandir}/man3

(cd widgets-mesa; \
%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir}/man3)

install -d $RPM_BUILD_ROOT/usr/src/examples/Mesa
for l in book demos samples xdemos images ; do
	cp -Rf $l $RPM_BUILD_ROOT%{_examplesdir}/Mesa/$l
done

gzip -9nf docs/*

# resolve conflict with XFree86-devel
rm -f $RPM_BUILD_ROOT%{_mandir}/man3/GLwCreateMDrawingArea.*
rm -f $RPM_BUILD_ROOT%{_mandir}/man3/GLwDrawingArea{,MakeCurrent,SwapBuffers}.*

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

%dir %{_includedir}/GL
%{_includedir}/GL/GLwDrawA.h
%{_includedir}/GL/GLwDrawAP.h
%{_includedir}/GL/GLwMDrawA.h
%{_includedir}/GL/GLwMDrawAP.h
%{_includedir}/GL/MesaDrawingArea.h
%{_includedir}/GL/MesaDrawingAreaP.h
%{_includedir}/GL/MesaMDrawingArea.h
%{_includedir}/GL/MesaMDrawingAreaP.h
%{_includedir}/GL/MesaWorkstation.h
%{_includedir}/GL/MesaWorkstationP.h
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
%{_libdir}/libGL*.a

%files demos
%defattr(644,root,root,755)
%dir /usr/src/examples/Mesa/book
%dir /usr/src/examples/Mesa/demos
%dir /usr/src/examples/Mesa/samples
%dir /usr/src/examples/Mesa/xdemos

%doc /usr/src/examples/Mesa/book/*
%doc /usr/src/examples/Mesa/demos/*
%doc /usr/src/examples/Mesa/samples/*
%doc /usr/src/examples/Mesa/xdemos/*
