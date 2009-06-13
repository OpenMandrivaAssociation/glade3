%define name glade3
%define major 	9
%define libname %mklibname gladeui1_ %major
%define libnamedev %mklibname -d gladeui1_

Summary: 	GTK+ / GNOME 2 widget builder
Name: 		%{name}
Version: 	3.6.5
Release: %mkrel 1
Epoch: 1
License: 	GPLv2+
Url: 		http://glade.gnome.org/
Group: 		Development/GNOME and GTK+
Source0: 	http://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root
BuildRequires: 	libxml2-devel
BuildRequires: 	libgnomeprintui-devel
BuildRequires: 	libgnomeui2-devel
BuildRequires:	desktop-file-utils
BuildRequires: 	pygtk2.0-devel
BuildRequires: 	gtk-doc
BuildRequires: 	scrollkeeper
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
Provides:	libgladeui = %epoch:%{version}

%description -n %{libname}
Libraries and file require to run program built with glade-3

%package -n %{libnamedev}
Summary:	Static libraries, include files for libgladeui (glade-3)
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %epoch:%{version}
Provides:	libgladeui-devel = %epoch:%{version}-%{release}
Provides:	libgladeui1-devel = %epoch:%{version}-%{release}
Provides:	glade3-devel = %epoch:%{version}-%{release}
Provides:	libgladeui%{major}-devel = %epoch:%{version}-%{release}
Conflicts: %mklibname -d gladeui1_ 6

%description -n %{libnamedev}
Static library, headers files and documentation needed in order
to develop applications using libgladeui (glade-3).

%prep
%setup -q -n %{name}-%version
#./autogen.sh

%build
%configure2_5x --enable-gtk-doc --disable-scrollkeeper
%make

%install
rm -fr %buildroot
%makeinstall_std
%{find_lang} %{name}-2.0 --with-gnome --all-name
for omf in %buildroot%_datadir/omf/*/{*-??,*-??_??}.omf;do
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %name-2.0.lang
done


# menu
perl -pi -e "s/Glade/Glade 3/" $RPM_BUILD_ROOT%{_datadir}/applications/*
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="GUIDesigner" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

find %buildroot -name \*.la|xargs chmod 644
rm -f %buildroot%_libdir/glade3/*/libglade*a

%if %mdkversion < 200900
%post
%update_scrollkeeper
%update_menus
%update_desktop_database
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%clean_scrollkeeper
%clean_menus
%clean_desktop_database
%clean_icon_cache hicolor
%endif

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -fr %buildroot

%files -f %{name}-2.0.lang
%defattr(-, root, root)
%doc AUTHORS COPYING README TODO
%{_bindir}/glade-3
%dir %{_libdir}/glade3/
%dir %{_libdir}/glade3/modules/
#gw not found by find_lang
%lang(en_GB)  %_datadir/gnome/help/glade/en_GB/
%{_libdir}/glade3/modules/libgladepython.so
%{_libdir}/glade3/modules/libgladegtk.so
%{_libdir}/glade3/modules/libgladegnome.so
%dir %_datadir/omf/*
%_datadir/omf/*/*-C.omf
%{_datadir}/glade3
%{_datadir}/applications/glade-3.desktop
%_datadir/icons/hicolor/*/apps/glade*

%files -n %{libname}
%{_libdir}/libgladeui-1.so.%{major}*

%files -n %{libnamedev}
%doc ChangeLog
%{_includedir}/libgladeui-1.0/
%{_libdir}/pkgconfig/gladeui-1.0.pc
%{_libdir}/*.la
%{_libdir}/*.so
%_datadir/gtk-doc/html/*
