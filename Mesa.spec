Summary:	Free OpenGL implementation. Runtime environment
Summary(pl):	Bezp³atna implementacja standardu OpenGL
Name:		Mesa
Version:	3.0
Release:	2d
Copyright:	GPL
Group:		X11/Libraries
Group(pl):	X11/Biblioteki
Source0:	ftp://iris.ssec.wisc.edu/pub/Mesa/%{name}Lib-%{version}.tar.gz
Source1:	ftp://iris.ssec.wisc.edu/pub/Mesa/%{name}Demos-%{version}.tar.gz
Patch:		Mesa-misc.diff
URL:		http://www.ssec.wisc.edu/~brianp/Mesa.html
BuildRoot:	/tmp/%{name}-%{version}-root

%description
Mesa is a 3-D graphics library with an API which is very similar to that
of OpenGL*.  To the extent that Mesa utilizes the OpenGL command syntax
or state machine, it is being used with authorization from Silicon Graphics,
Inc.  However, the author makes no claim that Mesa is in any way a
compatible replacement for OpenGL or associated with Silicon Graphics, Inc.
Those who want a licensed implementation of OpenGL should contact a licensed
vendor.  This software is distributed under the terms of the GNU Library
General Public License, see the LICENSE file for details.

* OpenGL(R) is a registered trademark of Silicon Graphics, Inc.

%description -l pl
Mesa jest bibliotek± 3D bêd±c± darmowym odpowiednikiem standartu OpenGL(*).
* OpenGL jest zastrze¿onym znakiem towarowym firmy Silicon Graphics, Inc.

%package devel
Summary:	Development environment for Mesa
Summary(pl):	¦rodowisko programistyczne biblioteki MESA
Group:		Development/Libraries
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
The static version of the Mesa libraries and include files needed for
development.

%description -l pl devel
Wersja biblioteki MESA linkowana statycznie wraz z plikami nag³ówkowymi.

%package glut
Summary:	GLUT library for Mesa
Summary(pl):	Biblioteka GLUT dla Mesy
Group:		X11/Libraries
Group(pl):	X11/Biblioteki
Requires:	%{name} = %{version}
Obsoletes:	glut

%description glut
The GLUT library.

%description -l pl glut
Biblioteka GLUT

%package glut-devel
Summary:	GLUT Development environment for Mesa
Summary(pl):	¦rodowisko programistyczne 'GLUT' dla biblioteki MESA.
Group:		Development/Libraries
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}
Obsoletes: 	glut-devel

%description glut-devel
The static version of the GLUT library and include files needed for
development.

%description -l pl glut-devel
Statycznie linkowana wersja biblioteki GLUT wraz z plikami naglowkowymi
potrzebnymi do pisania programow.

%package demos
Summary:	Mesa Demos
Summary(pl):	Demonstrace mo¿liwo¶ci biblioteki MESA.
Group:		Development/Libraries
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description demos
Demonstration programs for the Mesa libraries.

%description -l pl demos
Programy demonstracyjne dla biblioteki Mesa.

%prep
%setup -q -n Mesa-%{version} -b 1
%patch -p1

%build
%ifarch alpha
make LIBS_ONLY=YES linux-alpha
make clean
make linux-alpha-elf
%endif

%ifarch ppc
make linux-ppc
%endif

%ifarch i386
make clean
make LIBS_ONLY=YES linux-386
make clean
make linux-386-elf
%endif

%ifarch sparc sparc64
make  linux-elf
%endif

(cd widgets-mesa; CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s" \
./configure \
	--prefix=/usr/X11R6/
make)

%install
rm -fr $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/usr/X11R6/{lib/Mesa,include,man/man3}

cp -dpr lib include $RPM_BUILD_ROOT/usr/X11R6
cp -dpr book demos xdemos samples util $RPM_BUILD_ROOT/usr/X11R6/lib/Mesa
install Make-config $RPM_BUILD_ROOT/usr/X11R6/lib/Mesa

(cd widgets-mesa; make prefix=$RPM_BUILD_ROOT/usr/X11R6 install )

install */lib*.a $RPM_BUILD_ROOT/usr/X11R6/lib

strip $RPM_BUILD_ROOT/usr/X11R6/lib/{lib*so.*.*,Mesa/*/*} ||

gzip -9nf * $RPM_BUILD_ROOT/usr/X11R6/man/man3/*

%clean
rm -fr $RPM_BUILD_ROOT $RPM_BUILD_DIR/%name-%version

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc FUTURE IAFA-PACKAGE LICENSE README* RELNOTES VERSIONS

%ifnarch ppc
%attr(755,root,root) /usr/X11R6/lib/libMesa*.so.*.*
%else
/usr/X11R6/lib/libMesa*.a
%endif

%files glut
%defattr(644,root,root,755)
%ifnarch ppc
%attr(755,root,root) /usr/X11R6/lib/libglut.so.*
%else
/usr/X11R6/lib/libglut.a
%endif

%files glut-devel
%defattr(644,root,root,755)
%ifnarch ppc
%attr(755,root,root) /usr/X11R6/lib/libglut.so
/usr/X11R6/lib/libglut.a
%endif
/usr/X11R6/include/GL/glut.h

%files devel
%defattr(644,root,root,755)
%ifnarch ppc
%attr(755,root,root) /usr/X11R6/lib/libMesa*.so
/usr/X11R6/lib/libMesa*.a
%endif

%dir /usr/X11R6/lib/Mesa
/usr/X11R6/lib/Mesa/Make-config
%dir /usr/X11R6/lib/Mesa/util
/usr/X11R6/lib/Mesa/util/*

%dir /usr/X11R6/include/GL
/usr/X11R6/include/GL/*.h
%attr(644,root, man) /usr/X11R6/man/man3/*

%files demos
%defattr(644,root,root,755)
%dir /usr/X11R6/lib/Mesa/book
%dir /usr/X11R6/lib/Mesa/demos
%dir /usr/X11R6/lib/Mesa/samples
%dir /usr/X11R6/lib/Mesa/xdemos

%attr(-,root,root)/usr/X11R6/lib/Mesa/book/*
%attr(-,root,root)/usr/X11R6/lib/Mesa/demos/*
%attr(-,root,root)/usr/X11R6/lib/Mesa/samples/*
%attr(-,root,root)/usr/X11R6/lib/Mesa/xdemos/*

%changelog
* Sat Jan 30 1999 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [3.0-2d]
- added LDFLAGS="-s" to ./configure enviroment,
- fixed permission on lib*so* files (must be 755),
- removed RPM_OPT_FLAGS="$RPM_OPT_FLAGS" make parameters
  (this is redundant).

* Sat Jan 23 1999 Wojciech "Sas" Cieciwa <cieciwa@alpha.zarz.agh.edu.pl>
- gzipped man page.

* Thu Jan 12 1999 Wojciech "Sas" Cieciwa <cieciwa@alpha.zarz.agh.edu.pl>
- fixing library location.

* Thu Oct  1 1998 Wojciech "Sas" Cieciwa <cieciwa@alpha.zarz.agh.edu.pl>
  [3.0-1]
- fixing access permision.

* Wed May  5 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
- removed declarate %%{version}, %%{name}, %%{release} macros because
  all are predefined,
- removed check $RPM_BUILD_ROOT in %clean and %install,
- added "Requires: Mesa = %%{version}" for all subpackages (for
  keeping corectly dependences),
- in Mesa-glut* packages changed "Conflict:" to "Obsoletes:",
- added striping shared libs and demos,
- added modification in %build wihch allow build Mesa on sparc[64]
  architecture,
- all utils and demos instaled in /usr/lib/Mesa,
- added %defattr macros in %files (on rebuild require rpm >= 2.4.99),
- added -q %setup parameter.

* Thu Feb 12 1998 Christian 'Dr. Disk' Hechelmann <drdisk@ds9.au.s.shuttle.de>
- updated to final version 2.6

* Thu Feb 05 1998 Christian 'Dr. Disk' Hechelmann <drdisk@ds9.au.s.shuttle.de>
- Fixed thinko in misc patch
- build against glibc

* Sat Jan 31 1998 Christian 'Dr. Disk' Hechelmann <drdisk@ds9.au.s.shuttle.de>
- updated to version 2.6beta5
- added widget-mesa to the things to be build.

* Mon Jan 26 1998 Christian 'Dr. Disk' Hechelmann <drdisk@ds9.au.s.shuttle.de>
- updated to version 2.6beta4

* Sun Dec 14 1997 Christian 'Dr. Disk' Hechelmann <drdisk@ds9.au.s.shuttle.de>
- updated to version 2.6beta1

* Sat Dec 13 1997 Christian 'Dr. Disk' Hechelmann <drdisk@ds9.au.s.shuttle.de>
- Moved GLUT into a separate subpackage and added an Obsoletes tag to this
  subpackage
- Moved lib*.so to the devel package, they are only needed for development,
  not for a runtime environment.

* Sat Nov 29 1997 Christian 'Dr. Disk' Hechelmann <drdisk@ds9.au.s.shuttle.de>
- added patches from ftp://iris.ssec.wisc.edu/pub/Mesa/patches_to_2.5
- BuildRoot'ed
- Prefix'ed
- added static versions of the libraries. (PPC version seems not to have
  support for shared versions of the library)
- moved static versions of the library and the includes to the new subpackage
  'devel'
- targets other than linux-x86 still untested.
- added Conflitcs tag
- added %postun
- added patch for RPM_OPT_FLAGS support

* Fri Nov 21 1997 Karsten Weiss <karsten@addx.au.s.shuttle.de>
- Upgraded to Mesa 2.5
- Multiarch destinations (untested).
- Included GLUT.
- Removed some of the READMEs for other platforms from the binary RPM.
