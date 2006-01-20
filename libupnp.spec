Version: 1.2.1a
Summary: Universal Plug and Play (UPnP) SDK
Name: libupnp
Release: 4%{?dist}
License: BSD
Group: System Environment/Libraries
URL: http://upnp.sourceforge.net/
Source: http://ovh.dl.sourceforge.net/sourceforge/upnp/%{name}-%{version}.tar.gz
Patch0: libupnp_dsm_320.patch 
Patch1: libupnp_ixml_FC4.patch 
Patch2: libupnp_performance.patch
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The Universal Plug and Play (UPnP) SDK for Linux provides 
support for building UPnP-compliant control points, devices, 
and bridges on Linux.

%package devel
Group: Development/Libraries
Summary: Include files needed for development with libupnp
Requires: libupnp = %{version}-%{release}

%description devel
The libupnp-devel package contains the files necessary for development with
the UPnP SDK libraries.

%prep
%setup -q

%patch0 -p0
%patch1 -p0
%patch2 -p1
chmod 644 {LICENSE,README}

# Fix permissions for files in debuginfo package
find . -name '*.[ch]' | xargs chmod 644

# Fix libupnp.so symlink
sed -i -e 's#ln -s \$(PREFIX)/usr/lib/libupnp\.so#ln -s libupnp.so#' upnp/makefile

# Remove -Os optflag and add RPM optflags in makefiles
# Install libraries in correct directories
find . -name '[Mm]akefile' | xargs sed -i \
	-e 's/^\([[:space:]]*CFLAGS .*\) -Os/\1/' \
	-e 's/^\([[:space:]]*DEBUG_FLAGS .*\) -Os/\1/' \
	-e 's/^[[:space:]]*CFLAGS .*/& $(RPM_OPT_FLAGS)/' \
	-e 's#/usr/lib\([/ ;]\)#%{_libdir}\1#g' \
	-e 's#/usr/lib$#%{_libdir}#g'

%build
make -C upnp STRIP="echo Not stripping" %{?_smp_mflags}

%install
rm -rf %{buildroot}

## Install libupnp.so and headers
make -C upnp PREFIX=%{buildroot} install

## Install libixml.so and headers
make -C ixml PREFIX=%{buildroot} install
install -p ixml/inc/ixml.h %{buildroot}%{_includedir}/upnp

## Install libthreadutil.so and headers
make -C threadutil PREFIX=%{buildroot} install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE README
%{_libdir}/libixml.so*
%{_libdir}/libthreadutil.so*
%{_libdir}/libupnp.so*

%files devel
%defattr(0644,root,root,0755)
%{_includedir}/upnp/

%clean
rm -rf %{buildroot}

%changelog
* Mon Jan  9 2006 Eric Tanguy 1.2.1a-4
- Include libupnp.so symlink in package to take care of non versioning of libupnp.so.1.2.1

* Sun Jan  8 2006 Paul Howarth 1.2.1a-3
- Disable stripping of object code for sane debuginfo generation
- Edit makefiles to hnnor RPM optflags
- Install libraries in %%{_libdir} rather than hardcoded /usr/lib
- Fix libupnp.so symlink
- Own directory %%{_includedir}/upnp
- Fix permissions in -devel package

* Fri Jan 06 2006 Eric Tanguy 1.2.1a-2
- Use 'install -p' to preserve timestamps
- Devel now require full version-release of main package

* Thu Dec 22 2005 Eric Tanguy 1.2.1a-1
- Modify spec file from 
http://rpm.pbone.net/index.php3/stat/4/idpl/2378737/com/libupnp-1.2.1a_DSM320-3.i386.rpm.html
