#
# Conditional build:
%bcond_with	tests	# make check (requires BES server)
#
Summary:	HDF4 data handler module for the OPeNDAP data server
Summary(pl.UTF-8):	Moduł obsługujący dane HDF4 dla serwera danych OPeNDAP
Name:		opendap-hdf4_handler
Version:	3.11.6
Release:	1
License:	LGPL v2.1+
Group:		Daemons
Source0:	http://www.opendap.org/pub/source/hdf4_handler-%{version}.tar.gz
# Source0-md5:	7496894e20a10e067eefffb71653b96b
URL:		http://opendap.org/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.10
%{?with_tests:BuildRequires:	bes >= 3.13.0}
BuildRequires:	bes-devel >= 3.13.0
BuildRequires:	hdf-devel >= 4
BuildRequires:	hdf-eos-devel >= 2
BuildRequires:	libdap-devel >= 3.13.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
Requires:	bes >= 3.13.0
Requires:	hdf >= 4
Requires:	hdf-eos >= 2
Requires:	libdap >= 3.13.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the HDF4 data handler module for the OPeNDAP data server. It
reads HDF4 and HDF-EOS2 files and returns DAP responses that are
compatible with DAP2 and the dap-server software.

%description -l pl.UTF-8
Ten pakiet zawiera moduł obsługujący dane HDF4 dla serwera danych
OPeNDAP. Odczytuje pliki HDF4 oraz HDF-EOS2 i zwraca odpowiedzi DAP
zgodne z oprogramowaniem DAP2 i dap-server.

%prep
%setup -q -n hdf4_handler-%{version}

# don't use -L/usr/lib for hdfeos2
%{__sed} -i -e '/LDFLAGS.*HDFEOS2_DIR/d' configure.ac

%build
# rebuild autotools for -as-needed to work
%{__libtoolize}
%{__aclocal} -I conf
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-cache-dir=/var/cache/bes \
	--with-hdfeos2=/usr
%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/bes/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYRIGHT_URI ChangeLog NEWS README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bes/modules/h4.conf
%attr(755,root,root) %{_libdir}/bes/libhdf4_module.so
%dir %{_datadir}/hyrax/data/hdf4
%{_datadir}/hyrax/data/hdf4/*.HDF.gz
%{_datadir}/hyrax/data/hdf4/*.hdf.gz
