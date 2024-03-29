# TODO
# - Enabling enterprise features:
#   To connect to MongoDB Enterprise using SASL (GSSAPI) or LDAP (PLAIN) you
#   need to build the driver against cyrus-sasl2 (external library).
# NOTE
# - see comprehensive release notes here https://github.com/mongodb/mongo-php-driver/releases
%define		php_name	php%{?php_suffix}
%define		modname	mongo
%define		status		stable
Summary:	%{modname} - MongoDB database driver
Summary(pl.UTF-8):	%{modname} - dostęp do bazy danych MongoDB
Name:		%{php_name}-pecl-%{modname}
Version:	1.6.16
Release:	3
License:	Apache v2.0
Group:		Development/Languages/PHP
Source0:	https://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	cde37cae4fafbb66903ce81d44f7f492
URL:		https://docs.mongodb.com/ecosystem/drivers/php/
BuildRequires:	%{php_name}-devel >= 3:5.3.0
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Provides:	php(%{modname}) = %{version}
Obsoletes:	php-pecl-mongo < 1.5.1-1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module provides an interface for communicating with the MongoDB
database in PHP.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
Moduł umożliwia dostęp do serwera MongoDB w aplikacjach PHP.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
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
%doc README.md
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
