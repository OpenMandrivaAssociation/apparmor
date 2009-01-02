%define rev 1349

Summary:	AppArmor userlevel parser utility
Name:		apparmor-parser
Version:	2.3.1
Release:	%mkrel 1.%{rev}.1
License:	GPL
Group:		System/Base
URL:		http://forge.novell.com/modules/xfmod/project/?apparmor
Source0:	%{name}-%{version}-%{rev}.tar.gz
Patch:          apparmor-2.1-961-condreload.patch
BuildRequires:  flex
BuildRequires:  latex2html
BuildRequires:  bison
BuildRequires:  swig
BuildRequires:  pkgconfig
BuildRequires:  perl-devel
Requires(preun): rpm-helper
Requires(post): rpm-helper
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
AppArmor is a security framework that proactively protects the operating system
and applications.

AppArmor Parser is a userlevel program that is used to load in program
profiles to the AppArmor Security kernel module.


%prep
%setup -q
%patch -p0 -b .condrestart

%build
%serverbuild

%make CFLAGS="$RPM_OPT_FLAGS" TESTBUILDDIR=$(pwd)

%install
rm -rf %{buildroot}

%{makeinstall_std} DISTRO=redhat TESTBUILDDIR=$(pwd)

cat > README.urpmi << EOF
Mandriva RPM specific notes 

AppArmor is no longer a kernel module: instead, it is built in to the kernel.
To enable it, you can pass the apparmor=1 parameter to the kernel command line.
Kernel parameters can be added with the drakboot utility, Mandriva's boot
configuration tool, available from the Mandriva Control Center; by editing the
bootloader configuration file - /boot/grub/menu.lst for GRUB or /etc/lilo.conf
for LILO - manually; or by entering the kernel parameter after selecting the
desired kernel on the boot menu screen. 
EOF

%post
%_post_service apparmor
%_post_service aaeventd

%preun
%_preun_service apparmor
%_preun_service aaeventd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING.GPL README*
%dir %{_sysconfdir}/apparmor
%config(noreplace) %{_sysconfdir}/apparmor/subdomain.conf
%{_sysconfdir}/init.d/aaeventd
%{_sysconfdir}/init.d/apparmor
# no lib64
%dir /lib/apparmor
/lib/apparmor/rc.apparmor.functions
/sbin/*
%{_datadir}/locale/*/*/apparmor-parser.mo
%{_mandir}/man5/apparmor.d.5*
%{_mandir}/man5/apparmor.vim.5*
%{_mandir}/man5/subdomain.conf.5*
%{_mandir}/man7/apparmor.7*
%{_mandir}/man8/apparmor_parser.8*
%{_var}/lib/apparmor

