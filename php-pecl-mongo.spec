%define		_modname	mongo
%define		_status		stable
Summary:	%{_modname} - MongoDB database driver
Summary(pl.UTF-8):	%{_modname} - dostęp do bazy danych MongoDB
Name:		php-pecl-%{_modname}
Version:	1.2.6
Release:	1
License:	Apache
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	b471f3d9309c2caa52ea90122042d3f4
URL:		http://pecl.php.net/package/mongo
BuildRequires:	php-devel >= 3:5.1.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.1.0
Obsoletes:	php-mongo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module provides an interface for communicating with the MongoDB
database in PHP.

In PECL status of this extension is: %{_status}.

%description -l pl.UTF-8
Moduł umożliwia dostęp do serwera MongoDB w aplikacjach PHP.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} -C %{_modname}-%{version} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
