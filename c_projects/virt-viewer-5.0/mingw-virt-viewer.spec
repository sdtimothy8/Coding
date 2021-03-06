%{?mingw_package_header}

%define relver 1%{?dist}

# We want the 1st part of the release number, and
# the 3rd part (or 0 if not present). We want to
# avoid the autobuild magic 'extra_release' too
# which is not purely numeric and larger than 255.
# This scheme lets us cope with RHEL-style z-stream
# versioning when creating Win product versions
%define rel0 %(echo %{relver} | cut -d. -f1)
%define rel1 %(test -z "`echo %{relver} | cut -d. -f3`" && echo 0 || (echo %{relver} | cut -d. -f3))
%define buildid %(expr %{rel0} \\* 256 + %{rel1})

Name:           mingw-virt-viewer
Version:        5.0
Release:        %{relver}%{?extra_release}
Summary:        MinGW Windows virt-viewer console application

License:        GPLv2+
Group:          Applications/Internet
URL:            http://virt-manager.org/
Source0:        ftp://virt-manager.org/downloads/virt-viewer/virt-viewer-%{version}.tar.gz

BuildRequires:  mingw32-adwaita-icon-theme
BuildRequires:  mingw64-adwaita-icon-theme
BuildRequires:  mingw32-filesystem >= 23
BuildRequires:  mingw64-filesystem >= 23
BuildRequires:  mingw32-glib2 >= 2.38
BuildRequires:  mingw64-glib2 >= 2.38
BuildRequires:  mingw32-glib-networking
BuildRequires:  mingw64-glib-networking
BuildRequires:  mingw32-gstreamer1-plugins-bad-free
BuildRequires:  mingw64-gstreamer1-plugins-bad-free
BuildRequires:  mingw32-gstreamer1-plugins-good
BuildRequires:  mingw64-gstreamer1-plugins-good
BuildRequires:  mingw32-gtk3 >= 3.12
BuildRequires:  mingw64-gtk3 >= 3.12
BuildRequires:  mingw32-libgovirt
BuildRequires:  mingw64-libgovirt
BuildRequires:  mingw32-libusbx
BuildRequires:  mingw64-libusbx
BuildRequires:  mingw32-libvirt >= 0.10.0
BuildRequires:  mingw64-libvirt >= 0.10.0
BuildRequires:  mingw32-libvirt-glib >= 0.1.8
BuildRequires:  mingw64-libvirt-glib >= 0.1.8
BuildRequires:  mingw32-libxml2 >= 2.6.0
BuildRequires:  mingw64-libxml2 >= 2.6.0
BuildRequires:  mingw32-gtk-vnc2 >= 0.4.0
BuildRequires:  mingw64-gtk-vnc2 >= 0.4.0
BuildRequires:  mingw32-readline
BuildRequires:  mingw64-readline
BuildRequires:  mingw32-rest
BuildRequires:  mingw64-rest
BuildRequires:  mingw32-spice-glib
BuildRequires:  mingw64-spice-glib
BuildRequires:  mingw32-spice-gtk3 >= 0.33
BuildRequires:  mingw64-spice-gtk3 >= 0.33
BuildRequires:  mingw32-usbredir
BuildRequires:  mingw64-usbredir
BuildRequires:  pkgconfig
BuildRequires:  /usr/bin/pod2man
BuildRequires:  intltool
BuildRequires:  icoutils
BuildRequires:  dos2unix
BuildRequires:  hicolor-icon-theme
BuildRequires:  hwdata
BuildRequires:  msitools >= 0.95-5

BuildArch:      noarch

%package -n mingw32-virt-viewer
Summary:        MinGW Windows virt-viewer console application
Group:          Applications/Internet

%package -n mingw64-virt-viewer
Summary:        MinGW Windows virt-viewer console application
Group:          Applications/Internet

%package -n mingw64-virt-viewer-msi
Summary:        MinGW Windows virt-viewer MSI
Group:          Applications/Internet

%package -n mingw32-virt-viewer-msi
Summary:        MinGW Windows virt-viewer MSI
Group:          Applications/Internet

%description
MinGW Windows virt-viewer console application

%description -n mingw32-virt-viewer
MinGW Windows virt-viewer console application

%description -n mingw64-virt-viewer
MinGW Windows virt-viewer console application

%description -n mingw64-virt-viewer-msi
MinGW Windows virt-viewer MSI

%description -n mingw32-virt-viewer-msi
MinGW Windows virt-viewer MSI

%{mingw_debug_package}

%prep
%setup -q -n virt-viewer-%{version}

%build
%mingw_configure --with-gtk=3.0 --with-buildid=%{buildid}

%mingw_make %{?_smp_mflags} V=1
%mingw_make %{?_smp_mflags} V=1 -C data msi

%install
%mingw_make_install DESTDIR=$RPM_BUILD_ROOT

%if 0%{?mingw_build_win32} == 1
mkdir $RPM_BUILD_ROOT/%{mingw32_datadir}/virt-viewer
cp build_win32$MINGW_BUILDDIR_SUFFIX/data/virt-viewer-x86-5.0.msi $RPM_BUILD_ROOT/%{mingw32_datadir}/virt-viewer
%endif

%if 0%{?mingw_build_win64} == 1
mkdir $RPM_BUILD_ROOT/%{mingw64_datadir}/virt-viewer
cp build_win64$MINGW_BUILDDIR_SUFFIX/data/virt-viewer-x64-5.0.msi $RPM_BUILD_ROOT/%{mingw64_datadir}/virt-viewer
%endif

%find_lang virt-viewer

# Don't need the XDG desktop files on Windows
find $RPM_BUILD_ROOT -name "*.desktop" -delete

%clean
rm -rf $RPM_BUILD_ROOT


%files -n mingw32-virt-viewer -f virt-viewer.lang
%defattr(-,root,root)
%{mingw32_bindir}/virt-viewer.exe
%{mingw32_bindir}/remote-viewer.exe
%{mingw32_bindir}/windows-cmdline-wrapper.exe
%{mingw32_bindir}/debug-helper.exe

%dir %{mingw32_datadir}/virt-viewer/
%{mingw32_datadir}/icons/hicolor/*/apps/*
%{mingw32_datadir}/icons/hicolor/*/devices/*

%{mingw32_mandir}/man1/virt-viewer.1*
%{mingw32_mandir}/man1/remote-viewer.1*

%files -n mingw32-virt-viewer-msi
%{mingw32_datadir}/virt-viewer/virt-viewer-x86-5.0.msi

%files -n mingw64-virt-viewer -f virt-viewer.lang
%defattr(-,root,root)
%{mingw64_bindir}/virt-viewer.exe
%{mingw64_bindir}/remote-viewer.exe
%{mingw64_bindir}/windows-cmdline-wrapper.exe
%{mingw64_bindir}/debug-helper.exe

%dir %{mingw64_datadir}/virt-viewer/
%{mingw64_datadir}/icons/hicolor/*/apps/*
%{mingw64_datadir}/icons/hicolor/*/devices/*

%{mingw64_mandir}/man1/virt-viewer.1*
%{mingw64_mandir}/man1/remote-viewer.1*

%files -n mingw64-virt-viewer-msi
%{mingw64_datadir}/virt-viewer/virt-viewer-x64-5.0.msi

%changelog
