Summary:	Instant messaging client for Windows Live Messenger (tm) network
Name:		emesene
Version:	2.12.1
Release:	0.1
License:	GPL v3 (emesene), GPL v2 (themes), LGPL (the rest)
Group:		Applications/Networking
URL:		http://www.emesene.org/
Source0:	https://github.com/emesene/emesene/tarball/v%{version}/%{name}-%{version}.tgz
# Source0-md5:	45dc07dd50e4748d4b2725a8c8d4c227
Patch0:		%{name}-desktop.patch
Patch2:		plugins-pyc.patch
Patch3:		pythonpath.patch
BuildRequires:	gettext
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.553
Requires:	%{name}-gui = %{version}-%{release}
Requires:	alsa-utils
Requires:	python
Requires:	python
Requires:	python-dbus
Requires:	python-gnome-extras
Requires:	python-modules-sqlite
Requires:	python-papyon >= 0.5.5
Requires:	python-pydns
Requires:	python-pynotify
Requires:	python-xmpppy
Suggests:	python-gnome-extras-gtkspell
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Emesene is a MSN Messenger client written in Python and GTK. The main
idea is to make a client similar to the official MSN Messenger client
but keeping it simple and with a nice GUI.

Emesene is a Python/GTK MSN messenger clone, it uses msnlib (MSNP9)
and try to be a nice looking and simple MSN client.

You can login, send formatted messages, smilies, use autoreply, change
status, change nick, send nudges and all the stuff you can do in a
normal MSN client except, file transfers, custom emoticons and display
picture.

%package gtk2
Summary:	emesene GTK interface for emesene client
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}
Requires:	gtk+2
Requires:	python-pygtk-gtk >= 2:2.12
Provides:	emesene-gui = %{version}-%{release}

%description gtk2
This contains the GTK interface for emesene.

%package qt4
Summary:	emesene Qt4 interface for emesene client
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}
Requires:	python-PyQt4 >= 4.6
Provides:	emesene-gui = %{version}-%{release}

%description qt4
This contains the Qt4 interface for emesene.

%prep
%setup -qc
mv *-emesene-*/* .
%undos -f py
%patch0 -p1
%patch2 -p1
%patch3 -p1

# remove shebang
%{__sed} -i -e '/^#!\//, 1d' emesene/test/e3_example.py emesene/extension.py \
	emesene/SingleInstance.py emesene/debugger.py emesene/emesene.py \
	emesene/pluginmanager.py emesene/plugin_base.py

# skip debug provider
%{__sed} -i -e '/import e3dummy/d' emesene/emesene.py

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

cat <<'EOF' > emesene.sh
#!/bin/sh
exec %{__python} %{_datadir}/%{name}/%{name} "$@"
EOF

# fix #!%{_bindir}/env python -> #!%{__python}:
%{__sed} -i -e '1s,^#!.*python,#!%{__python},' emesene/emesene
# lib64 path
%{__sed} -i -e 's,/usr/lib/emesene,%{_libdir}/%{name},' emesene/emesene

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/%{name},%{_bindir}}

%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

install -p %{name}.sh $RPM_BUILD_ROOT%{_bindir}/%{name}
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/%{name}-*.egg-info
mv $RPM_BUILD_ROOT{%{py_sitescriptdir}/%{name}/*,%{_datadir}/%{name}}

# unwanted
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}/test
%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/documentation.epydoc
%{__rm} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/lintreport.sh
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/%{name}/.doxygen

# duplicates
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}/data/pixmaps
%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/data/icons/hicolor/*/apps/%{name}.png
%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/data/icons/hicolor/scalable/apps/%{name}.svg
%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/data/share/applications/%{name}.desktop

# TODO: relocate
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}/po

#%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

#%files -f %{name}.lang
%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS COPYING README.developers README.markdown
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/data
%attr(755,root,root) %{_datadir}/%{name}/%{name}
%{_datadir}/%{name}/*.py[co]
%{_datadir}/%{name}/data/hotmlog.htm

%dir %{_datadir}/%{name}/e3
%{_datadir}/%{name}/e3/*.py[co]
%{_datadir}/%{name}/e3/msn
%{_datadir}/%{name}/e3/papylib
%{_datadir}/%{name}/e3/base
%{_datadir}/%{name}/e3/cache
%{_datadir}/%{name}/e3/common
%{_datadir}/%{name}/e3/dummy
%{_datadir}/%{name}/e3/jabber
%{_datadir}/%{name}/e3/synch

%dir %{_datadir}/%{name}/gui
%{_datadir}/%{name}/gui/*.py[co]
%{_datadir}/%{name}/gui/base
%{_datadir}/%{name}/gui/common

%{_datadir}/%{name}/interfaces
%{_datadir}/%{name}/plugins

%dir %{_datadir}/%{name}/themes
%{_datadir}/%{name}/themes/conversations
%{_datadir}/%{name}/themes/emotes
%{_datadir}/%{name}/themes/images
%{_datadir}/%{name}/themes/sounds

%{_mandir}/man1/%{name}.1*
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png
%{_pixmapsdir}/%{name}.xpm
%{_iconsdir}/hicolor/*/apps/%{name}.png

%files gtk2
%defattr(644,root,root,755)
%{_datadir}/%{name}/gui/gtkui

%files qt4
%defattr(644,root,root,755)
%{_datadir}/%{name}/gui/qt4ui
