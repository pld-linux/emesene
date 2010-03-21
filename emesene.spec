Summary:	Instant messaging client for Windows Live Messenger (tm) network
Name:		emesene
Version:	1.6
Release:	0.17
License:	GPL v2+
Group:		Applications/Networking
URL:		http://www.emesene.org/
Source0:	http://downloads.sourceforge.net/project/emesene/%{name}-%{version}/emesene-%{version}.tar.gz
# Source0-md5:	ea4d3f4097265daac6823d8288979d02
Patch0:		%{name}-desktop.patch
Patch1:		setup-install.patch
Patch2:		plugins-pyc.patch
Patch3:		pythonpath.patch
BuildRequires:	gettext
BuildRequires:	python-devel
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	alsa-utils
Requires:	gtk+2
Requires:	python
Requires:	python
Requires:	python-dbus
Requires:	python-gnome-extras
Requires:	python-pygtk-gtk
Requires:	python-pynotify
Suggests:	python-gnome-extras-gtkspell
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

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

cat <<'EOF' > emesene.sh
#!/bin/sh
exec %{__python} %{_datadir}/%{name}/%{name} "$@"
EOF

# fix #!%{_bindir}/env python -> #!%{__python}:
%{__sed} -i -e '1s,^#!.*python,#!%{__python},' emesene Controller.py
# lib64 path
%{__sed} -i -e 's,/usr/lib/emesene,%{_libdir}/%{name},' emesene

# po/nb already exists, so just rm
rm -r po/nb_NO

%build
%{__python} setup.py build_ext -i

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/%{name},%{_libdir}/%{name}}

%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

mv $RPM_BUILD_ROOT{%{py_sitedir}/libmimic.so,%{_libdir}/%{name}}
mv $RPM_BUILD_ROOT{%{_bindir}/%{name},%{_datadir}/%{name}}
rm $RPM_BUILD_ROOT%{py_sitedir}/emesene-*.egg-info
mv $RPM_BUILD_ROOT{%{py_sitedir}/*,%{_datadir}/%{name}}
rm $RPM_BUILD_ROOT%{_iconsdir}/hicolor/scalable/apps/emesene.svg
install -p %{name}.sh $RPM_BUILD_ROOT%{_bindir}/%{name}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc COPYING
%attr(755,root,root) %{_bindir}/emesene
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/libmimic.so
%dir %{_datadir}/%{name}
%attr(755,root,root) %{_datadir}/%{name}/emesene
%{_datadir}/%{name}/*.py[co]
%{_datadir}/%{name}/hotmlog.htm
%{_datadir}/%{name}/plugins_base
%{_datadir}/%{name}/abstract
%{_datadir}/%{name}/emesenelib
%dir %{_datadir}/%{name}/conversation_themes
%{_datadir}/%{name}/conversation_themes/default
%{_datadir}/%{name}/conversation_themes/gtalk
%{_datadir}/%{name}/conversation_themes/irc
%{_datadir}/%{name}/conversation_themes/messenger
%{_datadir}/%{name}/conversation_themes/pidgin
%dir %{_datadir}/%{name}/smilies
%{_datadir}/%{name}/smilies/default
%dir %{_datadir}/%{name}/sound_themes
%{_datadir}/%{name}/sound_themes/default
%{_datadir}/%{name}/sound_themes/freedesktop
%dir %{_datadir}/%{name}/themes
%{_datadir}/%{name}/themes/default
%{_datadir}/%{name}/themes/gnomecolors
%{_datadir}/%{name}/themes/inthemargins
%{_datadir}/%{name}/themes/tango
%{_mandir}/man1/emesene.1*
%{_desktopdir}/emesene.desktop
%{_pixmapsdir}/emesene.png
