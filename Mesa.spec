#
%bcond_with	glide	# with GLIDE
#
Summary:	Free OpenGL implementation
Summary(pl):	Bezp³atna implementacja standardu OpenGL
Name:		Mesa
Version:	6.0.1
Release:	1
License:	MIT (core), LGPL (MesaGLU), SGI (GLU,libGLw) and others - see COPYRIGHT file
Group:		X11/Libraries
Source0:	http://dl.sourceforge.net/mesa3d/%{name}Lib-%{version}.tar.bz2
# Source0-md5:	b7f14088c5c2f14490d2739a91102112
Source1:	http://dl.sourceforge.net/mesa3d/%{name}Demos-%{version}.tar.bz2
# Source1-md5:	dd6aadfd9ca8e1cfa90c6ee492bc6f43
Patch0:		%{name}-libGLw.patch
URL:		http://www.mesa3d.org/
%ifarch %{ix86} alpha
%{?with_glide:BuildRequires:	Glide3-DRI-devel}
%{?with_glide:Requires:	Glide3-DRI}
%endif
#BuildRequires:	XFree86-devel
BuildRequires:	libXmu-devel
BuildRequires:	libXp-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libtool >= 2:1.4d
BuildRequires:	motif-devel
BuildRequires:	perl-devel
Provides:	OpenGL
Obsoletes:	XFree86-OpenGL-core
Obsoletes:	XFree86-OpenGL-libs
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
Mesa jest bibliotek± 3D bêd±c± darmowym odpowiednikiem standardu
OpenGL(*).

- OpenGL jest zastrze¿onym znakiem towarowym firmy Silicon Graphics,
  Inc.

%package devel
Summary:	Development environment for Mesa
Summary(pl):	¦rodowisko programistyczne biblioteki Mesa
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
#Requires:	XFree86-devel
Requires:	libX11-devel
Requires:	libXp-devel
Provides:	OpenGL-devel
Obsoletes:	XFree86-OpenGL-devel

%description devel
Header files and documentation needed for development.

%description devel -l pl
Pliki nag³ówkowe i dokumentacja do Mesy.

%package static
Summary:	Mesa static libraries
Summary(pl):	Biblioteki statyczne Mesy
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	OpenGL-static
Obsoletes:	XFree86-OpenGL-static

%description static
The static version of the Mesa libraries.

%description static -l pl
Biblioteki statyczne Mesy.

%package demos
Summary:	Mesa Demos
Summary(pl):	Demonstracje mo¿liwo¶ci bibliotek Mesa
Group:		Development/Libraries
Requires:	OpenGL-devel

%description demos
Demonstration programs for the Mesa libraries.

%description demos -l pl
Programy demonstracyjne dla bibliotek Mesa.

%prep
%setup -q -n Mesa-%{version} -b 1
%patch0 -p1

# fix demos
%{__perl} -pi -e "s,\.\./images/,%{_examplesdir}/Mesa/images/,g" progs/demos/*

%build
# runtime detection, so safe to enable
ASM=
# asm is currently broken
#%ifarch %{ix86}
#ASM="$ASM -DUSE_X86_ASM"
#%endif
#%ifarch i586 i686 k6 athlon
#ASM="$ASM -DUSE_MMX_ASM"
#%endif
#%ifarch i686 athlon
#ASM="$ASM -DUSE_SSE_ASM"
#%endif
#%ifarch sparc sparc64 sparcv9
#ASM="$ASM -DUSE_SPARC_ASM"
#%endif

%{__make} linux-static \
	OPTFLAGS="%{rpmcflags} $ASM"
mv -f lib lib-static
%{__make} clean
%{__make} linux \
	OPTFLAGS="%{rpmcflags} $ASM"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/GL,%{_mandir}/man3,%{_examplesdir}/Mesa}

cp -df lib-static/lib[GO]* $RPM_BUILD_ROOT%{_libdir}
cp -df lib/lib[GO]* $RPM_BUILD_ROOT%{_libdir}
cp -rf include/GL/{gl*,osmesa.h,xmesa*} src/glw/GLw*.h $RPM_BUILD_ROOT%{_includedir}/GL
rm -f $RPM_BUILD_ROOT%{_includedir}/GL/glut*

for l in demos redbook samples xdemos ; do
	%{__make} -C progs/$l -f Makefile.X11 realclean
done
for l in demos redbook samples util xdemos images ; do
	cp -Rf progs/$l $RPM_BUILD_ROOT%{_examplesdir}/Mesa/$l
done
rm -rf $RPM_BUILD_ROOT%{_examplesdir}/Mesa/*/{.deps,CVS,Makefile.{BeOS*,win,cygnus,DJ,dja}}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc docs/{*.html,README.{3DFX,GGI,MITS,QUAKE,THREADS,X11},RELNOTES*,VERSIONS}
%attr(755,root,root) %{_libdir}/libGL*.so.*.*
%attr(755,root,root) %{_libdir}/libGL.so
%attr(755,root,root) %{_libdir}/libOSMesa.so.*.*

%files devel
%defattr(644,root,root,755)
%doc docs/*.spec
%attr(755,root,root) %{_libdir}/libGLU.so
%attr(755,root,root) %{_libdir}/libOSMesa.so
%{_libdir}/libGLw.a
%dir %{_includedir}/GL
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

%files static
%defattr(644,root,root,755)
%{_libdir}/libGL.a
%{_libdir}/libGLU.a
%{_libdir}/libOSMesa.a

%files demos
%defattr(644,root,root,755)
%{_examplesdir}/Mesa
