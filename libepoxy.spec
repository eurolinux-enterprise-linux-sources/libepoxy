Summary: epoxy runtime library
Name: libepoxy
Version: 1.5.2
Release: 1%{?dist}
License: MIT
URL: http://github.com/anholt/libepoxy
Source0: %{url}/releases/download/%{version}/%{name}-%{version}.tar.xz

BuildRequires: automake autoconf libtool
BuildRequires: mesa-libGL-devel
BuildRequires: mesa-libEGL-devel
BuildRequires: mesa-libGLES-devel
BuildRequires: xorg-x11-util-macros
BuildRequires: python
BuildRequires: xorg-x11-server-Xvfb mesa-dri-drivers
BuildRequires: glx-utils xdpyinfo

%description
A library for handling OpenGL function pointer management.

%package devel
Summary: Development files for libepoxy
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
autoreconf -vif || exit 1
%configure --disable-silent-rules
make %{?_smp_mflags}

%install
%make_install DESTDIR=$RPM_BUILD_ROOT

# NOTE: We intentionally don't ship *.la files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete -print

%check
xvfb-run -d -s "-screen 0 640x480x24" make check || \
%ifarch s390 ppc
    (cat `find . -name test-suite.log` ; exit 0)
%else
    (cat `find . -name test-suite.log` ; exit 1)
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README.md
%{_libdir}/libepoxy.so.0
%{_libdir}/libepoxy.so.0.0.0

%files devel
%dir %{_includedir}/epoxy/
%{_includedir}/epoxy/*
%{_libdir}/libepoxy.so
%{_libdir}/pkgconfig/epoxy.pc

%changelog
* Tue May 22 2018 Adam Jackson <ajax@redhat.com> - 1.5.2-1
- epoxy 1.5.2

* Wed Apr 11 2018 Debarshi Ray <rishi@fedoraproject.org> - 1.3.1-2
- Prevent crash in epoxy_glx_version if GLX is not available
Resolves: #1566101

* Fri Jan 27 2017 Adam Jackson <ajax@redhat.com> - 1.3.1-1
- libepoxy 1.3.1

* Wed Mar 25 2015 Adam Jackson <ajax@redhat.com> 1.2-2
- Fix description to not talk about DRM
- Sync some small bugfixes from git

* Mon Oct 13 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.0-1
- Update to 1.2 GA
- Don't fail build on make check failure for some architectures

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.4.20140411git6eb075c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.3.20140411git6eb075c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 11 2014 Dave Airlie <airlied@redhat.com> 1.2-0.2.20140411git6eb075c
- update to latest git snapshot

* Thu Mar 27 2014 Dave Airlie <airlied@redhat.com> 1.2-0.1.20140307gitd4ad80f
- initial git snapshot

