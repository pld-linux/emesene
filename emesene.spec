# TODO
# - locales to glibc dirs
# - make py[co] and install to python dir
Summary:	Instant messaging client for Windows Live Messenger (tm) network
Name:		emesene
Version:	1.6
Release:	0.8
License:	GPL v2+
Group:		Applications/Networking
URL:		http://www.emesene.org/
Source0:	http://downloads.sourceforge.net/project/emesene/%{name}-%{version}/emesene-%{version}.tar.gz
# Source0-md5:	ea4d3f4097265daac6823d8288979d02
Source1:	%{name}.desktop
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	python-devel
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

cat <<'EOF' > emesene.sh
#!/bin/sh
exec %{__python} %{_datadir}/%{name}/%{name} "$@"
EOF

# fix #!%{_bindir}/env python -> #!%{__python}:
%{__sed} -i -e '1s,^#!.*python,#!%{__python},' emesene Controller.py

%build
%{__python} setup.py build_ext -i

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,%{_libdir}/%{name},%{_datadir}/%{name},%{_desktopdir},%{_pixmapsdir}}

cp -a *.py hotmlog.htm *.png $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a abstract conversation_themes emesenelib plugins_base po smilies sound_themes themes $RPM_BUILD_ROOT%{_datadir}/%{name}

cp -a misc/%{name}.1 $RPM_BUILD_ROOT%{_mandir}/man1/%{name}.1
cp -a misc/%{name}.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png
cp -a misc/%{name}.desktop $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop
install -p emesene.sh $RPM_BUILD_ROOT%{_bindir}/emesene
install -p libmimic.so $RPM_BUILD_ROOT%{_libdir}/%{name}

> %{name}.lang
for file in po/*; do
	dir=${file##*/}
	echo "%lang($dir) %{_datadir}/%{name}/po/$dir" >> %{name}.lang
done

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/emesene
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/libmimic.so
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.py
%{_datadir}/%{name}/emesene-logo.png
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
%dir %{_datadir}/%{name}/po
%{_mandir}/man1/emesene.1*
%{_desktopdir}/emesene.desktop
%{_pixmapsdir}/emesene.png
