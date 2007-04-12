%define name glade3
%define major 	5
%define libname %mklibname gladeui1_ %major

Summary: 	GTK+ / GNOME 2 widget builder
Name: 		%{name}
Version: 	3.2.0
Release: %mkrel 1
Epoch: 1
License: 	LGPL
Url: 		http://glade.gnome.org/
Group: 		Development/GNOME and GTK+
Source0: 	http://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root
BuildRequires: 	libxml2-devel
BuildRequires: 	libgnomeprintui-devel
BuildRequires: 	libgnomeui2-devel
BuildRequires: 	pygtk2.0-devel
BuildRequires: 	desktop-file-utils
BuildRequires: 	gtk-doc
BuildRequires: 	scrollkeeper
BuildRequires: 	gnome-doc-utils libxslt-proc
BuildRequires: 	perl-XML-Parser
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Requires: pygtk2.0

%description
Glade is a Widget builder for Gtk/gnome. 
It allows to create a gtk/gnome interface in C, C++, Ada and Perl

This version of Glade (Glade-3) is a complete rewrite of the original
Glade codebase.
It has useful new features (Undo/Redo, MultiProject support) and has a
cleaner architecture, note however that it is not ready yet for everyday
use and lacks support for additional widgets, as Gnome and Gnome-db widgets.
One of the main differnces from glade-2 is that C code generation has been
removed from glade-3: this has been done on purpose, since using generated
code is deprecated; the preferred way to use glade files is with libglade.
Another important thing to note is that the XML format has _not_ changed,
so you can work on the same project both with glade-3 and with glade-2.
For a more details on what has changed, what still needs work, etc. see
the NEWS, BUGS and TODO files.
Comments, bug reports and patches are more than welcome.

%package -n %{libname}
Summary:	Libraries required for glade-3
Group:		System/Libraries
Provides:	libgladeui = %epoch:%{version}

%description -n %{libname}
Libraries and file require to run program built with glade-3

%package -n %{libname}-devel
Summary:	Static libraries, include files for libgladeui (glade-3)
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %epoch:%{version}
Provides:	libgladeui-devel = %epoch:%{version}-%{release}
Provides:	libgladeui1-devel = %epoch:%{version}-%{release}
Provides:	glade3-devel = %epoch:%{version}-%{release}
Provides:	libgladeui%{major}-devel = %epoch:%{version}-%{release}

%description -n %{libname}-devel
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
install -m 755 -d %{buildroot}%{_menudir}
cat > %{buildroot}%{_menudir}/%{name} <<EOF
?package(%{name}): command="%{_bindir}/glade-3" needs="X11" icon="glade-3.png"\
  section="More Applications/Development/Development Environments" \
  title="Glade 3" longtitle="GTK/GNOME 3 Widget Builder" startup_notify="true" xdg="true"
EOF

perl -pi -e "s/Glade/Glade 3/" $RPM_BUILD_ROOT%{_datadir}/applications/*
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-MoreApplications-Development-DevelopmentEnvironments;GUIDesigner" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

find %buildroot -name \*.la|xargs chmod 644
rm -f %buildroot%_libdir/glade3/*/libglade*a

%post
%update_scrollkeeper
%update_menus
%update_desktop_database
%update_icon_cache hicolor

%postun
%clean_scrollkeeper
%clean_menus
%clean_desktop_database
%clean_icon_cache hicolor

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -fr %buildroot

%files -f %{name}-2.0.lang
%defattr(-, root, root)
%doc AUTHORS ChangeLog COPYING README TODO
%{_bindir}/glade-3
%dir %{_libdir}/glade3/
%dir %{_libdir}/glade3/modules/
%dir %{_libdir}/glade3/bindings
%{_libdir}/glade3/modules/libgladegtk.so
%{_libdir}/glade3/modules/libgladegnome.so
%{_libdir}/glade3/bindings/libgladepython.so
%dir %_datadir/omf/*
%_datadir/omf/*/*-C.omf
%{_datadir}/glade3
%{_datadir}/applications/glade-3.desktop
%_datadir/icons/hicolor/*/apps/glade*
%{_menudir}/%name

%files -n %{libname}
%{_libdir}/libgladeui-1.so.%{major}*

%files -n %{libname}-devel
%{_includedir}/libgladeui-1.0/
%{_libdir}/pkgconfig/gladeui-1.0.pc
%{_libdir}/*.la
%{_libdir}/*.so
%_datadir/gtk-doc/html/*


