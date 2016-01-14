Summary:  	Rsync libraries
Name:     	librsync
Version:  	0.9.7
Release:  	1.%{dist}
License:	LGPL
Vendor: %{vendor}
Packager: %{packager}
ExclusiveArch:	x86_64
Group:    	System Environment/Libraries
Source:  	http://prdownloads.sourceforge.net/librsync/%{name}-%{version}.tar.gz
URL:       	http://www.sourceforge.net/projects/%{name}
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
librsync implements the "rsync" algorithm, which allows remote
differencing of binary files.  librsync computes a delta relative to a
file's checksum, so the two files need not both be present to generate
a delta.

This library was previously known as libhsync up to version 0.9.0.

The current version of this package does not implement the rsync
network protocol and uses a delta format slightly more efficient than
and incompatible with rsync 2.4.6.

%package devel
Summary: Headers and development libraries for librsync
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
librsync implements the "rsync" algorithm, which allows remote
differencing of binary files.  librsync computes a delta relative to a
file's checksum, so the two files need not both be present to generate
a delta.

This library was previously known as libhsync up to version 0.9.0.

The current version of this package does not implement the rsync
network protocol and uses a delta format slightly more efficient than
and incompatible with rsync 2.4.6.

This package contains header files necessary for developing programs
based on librsync.

%prep 
%setup
# The next line is only needed if there are any non-upstream patches.  In
# this distribution there are none.
#%patch 
%build
libtoolize --force
aclocal
autoheader
automake Makefile popt/Makefile
autoconf
./configure --prefix=/usr --mandir=/usr/share/man/ --libdir=%{_libdir}
make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
make  DESTDIR=$RPM_BUILD_ROOT install

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS COPYING COPYING NEWS README
%{_libdir}/%{name}.la
%{_bindir}/rdiff
%{_mandir}/man3/%{name}.3.gz
%{_mandir}/man1/rdiff.1.gz

%files devel
%defattr(-,root,root)
%{_prefix}/include/*
%{_libdir}/%{name}.a

%changelog
