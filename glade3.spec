%define name glade3
%define api 	1
%define major 	11
%define libname %mklibname gladeui %{api} %{major}
%define libnamedev %mklibname -d gladeui %{api}

Summary: 	GTK+ / GNOME 2 widget builder
Name: 		%{name}
Epoch:		1
Version: 	3.8.1
Release:	2
License: 	GPLv2+
Url: 		http://glade.gnome.org/
Group: 		Development/GNOME and GTK+
Source0: 	http://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2

BuildRequires: 	libxml2-devel
BuildRequires: 	libgnomeui2-devel
BuildRequires:	desktop-file-utils
BuildRequires: 	pygtk2.0-devel
BuildRequires: 	gtk-doc
BuildRequires: 	gnome-doc-utils
BuildRequires: 	intltool
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Requires: pygtk2.0

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

%package -n %{libnamedev}
Summary:	Development libraries, include files for libgladeui (glade-3)
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %{EVRD}
Provides:	glade3-devel = %{EVRD}
Provides:	libgladeui%{major}-devel = %{EVRD}
Conflicts: %mklibname -d gladeui1_ 6
Obsoletes: %mklibname -d gladeui1_

%description -n %{libnamedev}
Static library, headers files and documentation needed in order
to develop applications using libgladeui (glade-3).

%prep
%setup -q -n %{name}-%version

%build
%configure2_5x \
	--disable-static \
	--enable-gtk-doc \
	--disable-scrollkeeper

%make

%install
rm -fr %buildroot
%makeinstall_std
%{find_lang} %{name}-2.0 --with-gnome --all-name
for omf in %buildroot%_datadir/omf/*/{*-??,*-??_??}.omf;do
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %name-2.0.lang
done

# menu
perl -pi -e "s/Glade/Glade 3/" %{buildroot}%{_datadir}/applications/*
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="GUIDesigner" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

find %buildroot -name \*.la|xargs chmod 644
rm -f %buildroot%_libdir/glade3/*/libglade*a

%files -f %{name}-2.0.lang
%doc AUTHORS COPYING README TODO
%{_bindir}/glade-3
%dir %{_libdir}/glade3/
%dir %{_libdir}/glade3/modules/
%{_libdir}/glade3/modules/libgladepython.so
%{_libdir}/glade3/modules/libgladegtk.so
%{_libdir}/glade3/modules/libgladegnome.so
%dir %_datadir/omf/*
%_datadir/omf/*/*-C.omf
%{_datadir}/glade3
%{_datadir}/applications/glade-3.desktop
%_datadir/icons/hicolor/*/apps/glade*

%files -n %{libname}
%{_libdir}/libgladeui-%{api}.so.%{major}*

%files -n %{libnamedev}
%doc ChangeLog
%{_includedir}/libgladeui-1.0/
%{_libdir}/pkgconfig/gladeui-1.0.pc
%{_libdir}/*.so
%_datadir/gtk-doc/html/*

