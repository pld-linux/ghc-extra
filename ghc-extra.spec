#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	extra
Summary:	Extra functions I use
Name:		ghc-%{pkgname}
Version:	1.7.1
Release:	1
License:	LGPL
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/extra
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	6af7bca1d01928042f9c09f236db607f
URL:		http://hackage.haskell.org/package/extra
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4.4
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-clock >= 0.7
BuildRequires:	ghc-directory
BuildRequires:	ghc-filepath
BuildRequires:	ghc-process
BuildRequires:	ghc-semigroups
BuildRequires:	ghc-time
BuildRequires:	ghc-unix
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 4.4
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-clock-prof >= 0.7
BuildRequires:	ghc-directory-prof
BuildRequires:	ghc-filepath-prof
BuildRequires:	ghc-process-prof
BuildRequires:	ghc-semigroups-prof
BuildRequires:	ghc-time-prof
BuildRequires:	ghc-unix-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 4.4
Requires:	ghc-base < 5
Requires:	ghc-clock >= 0.7
Requires:	ghc-directory
Requires:	ghc-filepath
Requires:	ghc-process
BuildRequires:	ghc-semigroups
Requires:	ghc-time
Requires:	ghc-unix
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
A library of extra functions for the standard Haskell libraries. Most
functions are simple additions, filling out missing functionality. A
few functions are available in later versions of GHC, but this package
makes them available back to GHC 7.2. 

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof < 6
Requires:	ghc-bytestring-prof
Requires:	ghc-semigroups-prof
Requires:	ghc-text-prof

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSextra-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSextra-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSextra-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Exception
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Exception/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Exception/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Either
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Either/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Either/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/IORef
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/IORef/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/IORef/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/List
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/List/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/List/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/List/NonEmpty
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/List/NonEmpty/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/List/NonEmpty/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Tuple
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Tuple/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Tuple/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Typeable
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Typeable/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Typeable/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Version
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Version/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Version/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Numeric
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Numeric/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Numeric/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Directory
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Directory/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Directory/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Environment
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Environment/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Environment/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/IO
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/IO/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/IO/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Info
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Info/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Info/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Process
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Process/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Process/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Time
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Time/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Time/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Read
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Read/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Read/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSextra-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Exception/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Either/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/IORef/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/List/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/List/NonEmpty/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Tuple/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Typeable/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Version/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Numeric/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Directory/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Environment/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/IO/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Info/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Process/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Time/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Read/*.p_hi
%endif
