%define libname %mklibname apparmor
%define devname %mklibname -d apparmor
%define staticname %mklibname -d -s apparmor

# For the python module
%define _disable_ld_no_undefined 1
#define beta beta2

Summary:	AppArmor userlevel parser utility
Name:		apparmor
Version:	3.1.7
Release:	%{?beta:0.%{beta}.}1
License:	GPL
Group:		System/Base
URL:		https://gitlab.com/apparmor/apparmor
Source0:	https://gitlab.com/apparmor/apparmor/-/archive/v%{version}%{?beta:-%{beta}}/apparmor-v%{version}%{?beta:-%{beta}}.tar.bz2
BuildRequires:  flex
BuildRequires:  latex2html
BuildRequires:  bison
BuildRequires:  swig
BuildRequires:  pkgconfig
BuildRequires:  perl-devel
BuildRequires:	perl(Pod::Checker)
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	slibtool
BuildRequires:	gettext
BuildRequires:	pkgconfig(pam)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	gawk
BuildRequires:	which
BuildRequires:	apache-devel
BuildRequires:	make
%rename apparmor-utils
%rename apparmor-parser
%rename apparmor-profiles

%description
AppArmor is a security framework that proactively protects the operating system
and applications.

AppArmor Parser is a userlevel program that is used to load in program
profiles to the AppArmor Security kernel module.

%package -n %{libname}
Summary: Libraries for the AppArmor security system
Group: System/Libraries

%description -n %{libname}
Libraries for the AppArmor security system

%package -n %{devname}
Summary: Development files for the AppArmor security system
Group: Development/C and C++
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files for the AppArmor security system

%package -n %{staticname}
Summary: Static libraries for the AppArmor security system
Group: Development/C and C++/Static
Requires: %{devname} = %{EVRD}

%description -n %{staticname}
Static libraries for the AppArmor security system

%package -n python-apparmor
Summary: Python bindings for the AppArmor security system
Group: Development/Python

%description -n python-apparmor
Python bindings for the AppArmor security system

%package -n perl-apparmor
Summary: Perl bindings for the AppArmor security system
Group: Development/Perl

%description -n perl-apparmor
Perl bindings for the AppArmor security system

%package -n pam_apparmor
Summary: PAM module for the AppArmor security system
Group: System/Libraries

%description -n pam_apparmor
PAM module for the AppArmor security system

%package -n apache-mod_apparmor
Summary: AppArmor support for the Apache web server
Group: Servers

%description -n apache-mod_apparmor
AppArmor support for the Apache web server

%prep
%autosetup -p1 -n apparmor-v%{version}%{?beta:-%{beta}}

if ! echo %{__cc} |grep -q gcc; then
	sed -i -e 's,-flto-partition=none,,' libraries/libapparmor/src/Makefile.am parser/Makefile
fi

cd libraries/libapparmor
sh ./autogen.sh
%configure --with-perl --with-python
cd ../..

%build
%serverbuild

cd libraries/libapparmor
%make_build LIBTOOL=slibtool

cd ../../binutils
%make_build CFLAGS="$RPM_OPT_FLAGS" TESTBUILDDIR=$(pwd) LIBTOOL=slibtool SBINDIR=%{_bindir}

cd ../parser
%make_build CFLAGS="$RPM_OPT_FLAGS" TESTBUILDDIR=$(pwd) LIBTOOL=slibtool SBINDIR=%{_bindir} USR_SBINDIR=%{buildroot}%{_bindir}

cd ../utils
%make_build CFLAGS="$RPM_OPT_FLAGS" TESTBUILDDIR=$(pwd) LIBTOOL=slibtool BINDIR=%{_bindir}

cd ../changehat/mod_apparmor
%make_build LIBTOOL=slibtool LTFLAGS="--tag=CC"

cd ../pam_apparmor
%make_build LIBTOOL=slibtool SECDIR=%{_libdir}/security

cd ../../profiles
%make_build LIBTOOL=slibtool


%install
cd libraries/libapparmor
%make_install LIBTOOL=slibtool

cd ../../binutils
%make_install LIBTOOL=slibtool SBINDIR=%{buildroot}%{_bindir}

cd ../parser
%make_install DISTRO=redhat TESTBUILDDIR=$(pwd) LIBTOOL=slibtool SBINDIR=%{buildroot}%{_bindir} USR_SBINDIR=%{buildroot}%{_bindir}

cd ../utils
%make_install LIBTOOL=slibtool BINDIR=%{buildroot}%{_bindir}

cd ../changehat/mod_apparmor
%make_install LIBTOOL=slibtool LTFLAGS="--tag=CC"

cd ../pam_apparmor
%make_install LIBTOOL=slibtool SECDIR=%{buildroot}%{_libdir}/security

cd ../../profiles
%make_install LIBTOOL=slibtool
cd ..

%find_lang aa-binutils
%find_lang apparmor-parser
%find_lang apparmor-utils

%files -n %{libname}
%{_libdir}/libapparmor.so.1*

%files -n %{devname}
%{_includedir}/aalogparse
%{_includedir}/sys/*.h
%{_libdir}/libapparmor.so
%{_libdir}/pkgconfig/libapparmor.pc
%{_mandir}/man2/*.2*
%{_mandir}/man3/*.3*

%files -n %{staticname}
%{_libdir}/libapparmor.a

%files -n python-apparmor
%{py_puresitedir}/apparmor
%{py_puresitedir}/apparmor*.*-info
%{py_platsitedir}/LibAppArmor
%{py_platsitedir}/LibAppArmor*.*-info

%files -n perl-apparmor
%{perl_vendorarch}/auto/LibAppArmor
%{perl_vendorarch}/LibAppArmor.pm

%files -f aa-binutils.lang -f apparmor-parser.lang -f apparmor-utils.lang
%defattr(-,root,root)
%doc README*
%{_sysconfdir}/apparmor
%{_sysconfdir}/apparmor.d
%{_prefix}/lib/systemd/system/apparmor.service
# no lib64
%dir /lib/apparmor
/lib/apparmor/rc.apparmor.functions
/lib/apparmor/apparmor.systemd
/lib/apparmor/profile-load
%{_bindir}/*
%{_datadir}/apparmor
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_mandir}/man7/*.7*
%{_mandir}/man8/*.8*
%{_var}/lib/apparmor

%files -n pam_apparmor
%{_libdir}/security/pam_apparmor.so

%files -n apache-mod_apparmor
%{_libdir}/apache/mod_apparmor.so
