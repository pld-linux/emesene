# TODO
# - locales to glibc dirs
Summary:	Instant messaging client for Windows Live Messenger (tm) network
Name:		emesene
Version:	1.0.1
Release:	1
License:	GPL v2+
Group:		Applications/Networking
URL:		http://www.emesene.org/
Source0:	http://dl.sourceforge.net/emesene/%{name}-%{version}.tar.gz
# Source0-md5:	49f77e190b8c991c32a07ac07cf88d13
Source1:	%{name}.desktop
Patch0:		python2.6.patch
Requires:	gtk+2
Requires:	python
Requires:	python-gnome-extras
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
emesene is an instant messaging client for Windows Live Messenger (tm)
network.

%prep
%setup -q
%patch0 -p1

cat <<'EOF' > emesene.sh
#!/bin/sh
exec %{__python} %{_datadir}/%{name}/%{name} "$@"
EOF

# fix #!/usr/bin/env python -> #!/usr/bin/python:
%{__sed} -i -e '1s,^#!.*python,#!%{__python},' emesene Controller.py

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name},%{_desktopdir},%{_pixmapsdir}}

cp -a . $RPM_BUILD_ROOT%{_datadir}/%{name}
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/emesene.sh
install emesene.sh $RPM_BUILD_ROOT%{_bindir}/emesene
ln $RPM_BUILD_ROOT{%{_datadir}/%{name}/themes/default/trayicon.png,%{_pixmapsdir}/emesene.png}
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

# handling locale files
#%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs
%attr(755,root,root) %{_bindir}/emesene
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/po
%lang(ar) %{_datadir}/%{name}/po/ar
%lang(ca) %{_datadir}/%{name}/po/ca
%lang(de) %{_datadir}/%{name}/po/de
%lang(es) %{_datadir}/%{name}/po/es
%lang(et) %{_datadir}/%{name}/po/et
%lang(fi) %{_datadir}/%{name}/po/fi
%lang(fr) %{_datadir}/%{name}/po/fr
%lang(hu) %{_datadir}/%{name}/po/hu
%lang(it) %{_datadir}/%{name}/po/it
%lang(nb_NO) %{_datadir}/%{name}/po/nb_NO
%lang(nl) %{_datadir}/%{name}/po/nl
%lang(pt) %{_datadir}/%{name}/po/pt
%lang(pt_BR) %{_datadir}/%{name}/po/pt_BR
%lang(sv) %{_datadir}/%{name}/po/sv
%lang(tr) %{_datadir}/%{name}/po/tr
%lang(zh_CN) %{_datadir}/%{name}/po/zh_CN
%lang(zh_TW) %{_datadir}/%{name}/po/zh_TW
%lang(da) %{_datadir}/%{name}/po/da
%lang(el) %{_datadir}/%{name}/po/el
%lang(en_GB) %{_datadir}/%{name}/po/en_GB
%lang(eu) %{_datadir}/%{name}/po/eu
%lang(ga) %{_datadir}/%{name}/po/ga
%lang(gl) %{_datadir}/%{name}/po/gl
%lang(he) %{_datadir}/%{name}/po/he
%lang(hr) %{_datadir}/%{name}/po/hr
%lang(is) %{_datadir}/%{name}/po/is
%lang(ja) %{_datadir}/%{name}/po/ja
%lang(lv) %{_datadir}/%{name}/po/lv
%lang(nds) %{_datadir}/%{name}/po/nds
%lang(nn) %{_datadir}/%{name}/po/nn
%lang(sl) %{_datadir}/%{name}/po/sl
%lang(sq) %{_datadir}/%{name}/po/sq
%lang(sr) %{_datadir}/%{name}/po/sr
%lang(th) %{_datadir}/%{name}/po/th
%lang(nb) %{_datadir}/%{name}/po/nb
%{_datadir}/%{name}/[A-Za-oq-z_]*
%{_datadir}/%{name}/plugins_base
%{_datadir}/%{name}/pygif
%{_desktopdir}/emesene.desktop
%{_pixmapsdir}/emesene.png
