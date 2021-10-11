%define _disable_ld_no_undefined 1
%define url_ver %(echo %{version}|cut -d. -f1,2)

%define api 	1
%define major 	11
%define libname %mklibname gladeui %{api} %{major}
%define devname %mklibname -d gladeui %{api}

Summary:	GTK+ / GNOME 2 widget builder
Name:		glade3
Epoch:		1
Version:	3.8.5
Release:	5
License:	GPLv2+
Group:		Development/GNOME and GTK+
Url:		http://glade.gnome.org
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
Patch0:                glade3-3.8.2-fix-linking.patch
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	gettext-devel
#gw autoreconf needs this:
BuildRequires:	gnome-common
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
#BuildRequires:	pkgconfig(pygtk-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	glib-gettextize
BuildRequires:	python2-devel
Requires(post,postun):	desktop-file-utils
#Requires:	pygtk2.0

%description
Glade is a RAD tool to enable quick & easy development of user interfaces
for the Gtk+ toolkit and the GNOME desktop environment.
The user interfaces designed in Glade are stored in XML format,
enabling easy integration with external tools.
In particular libglade can load the XML files and create the interfaces
at runtime. The DTD for the XML files is included with libglade, and is
also at http://glade.gnome.org/glade-2.0.dtd.
Other tools are available which can turn the XML files into source code
in languages such as C++, Perl and Python.

%package -n %{libname}
Summary:	Libraries required for glade-3
Group:		System/Libraries

%description -n %{libname}
Libraries and file require to run program built with glade-3

%package -n %{devname}
Summary:	Development libraries, include files for libgladeui (glade-3)
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %{EVRD}
Provides:	glade3-devel = %{EVRD}

%description -n %{devname}
Development library, headers files and documentation needed in order
to develop applications using libgladeui (glade-3).

%prep
%setup -q %{name}
%autopatch -p1
autoreconf -fi

%build
%configure \
	--enable-gtk-doc \
	--disable-gnome \
	--disable-compile-warnings PYTHON=python2

%make LIBS='-lgmodule-2.0'

%install
%makeinstall_std
%find_lang %{name}-2.0 --with-gnome --all-name

# menu
perl -pi -e "s/Glade/Glade 3/" %{buildroot}%{_datadir}/applications/*
desktop-file-install --vendor="" \
	--remove-category="Application" \
	--add-category="GUIDesigner" \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/*


%files -f %{name}-2.0.lang
%doc AUTHORS COPYING README TODO
%{_bindir}/glade-3
%dir %{_libdir}/glade3/
%dir %{_libdir}/glade3/modules/
#{_libdir}/glade3/modules/libgladepython.so
%{_libdir}/glade3/modules/libgladegtk.so
%{_datadir}/glade3
%{_datadir}/applications/glade-3.desktop
%{_datadir}/icons/hicolor/*/apps/glade*

%files -n %{libname}
%{_libdir}/libgladeui-%{api}.so.%{major}*

%files -n %{devname}
%doc ChangeLog
%{_includedir}/libgladeui-1.0/
%{_libdir}/pkgconfig/gladeui-1.0.pc
%{_libdir}/*.so
%{_datadir}/gtk-doc/html/*

