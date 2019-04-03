%global realname rebar
%global upstream rebar
%global debug_package %{nil}

# Set this to true when starting a rebuild of the whole erlang stack. There's
# a cyclical dependency between erlang-rebar and erlang-getopt so this package
# (rebar) needs to get built first in bootstrap mode.
%global need_bootstrap_set 1


%{!?need_bootstrap: %global need_bootstrap  %{need_bootstrap_set}}


Name:		erlang-%{realname}
Version:	2.6.4
Release:	2
Summary:	Erlang Build Tools
Group:		Development/Tools
License:	MIT
URL:		https://github.com/%{upstream}/%{realname}
Source0:	https://github.com/%{upstream}/%{realname}/archive/%{version}/%{realname}-%{version}.tar.gz
Source1:	rebar.escript
# Fedora/EPEL-specific
Patch1:		rebar-0001-Load-templates-from-the-filesystem-first.patch
# Fedora/EPEL-specific
Patch2:		rebar-0002-Remove-bundled-mustache.patch
# The bundled getopt is necessary to do the initial bootstrap since
# erlang-getopt requires erlang-rebar to build and vice versa.
# Fedora/EPEL-specific
Patch3:		rebar-0003-Remove-bundled-getopt.patch
# Will be proposed for inclusion
Patch4:		rebar-0004-Allow-discarding-building-ports.patch
# Fedora/EPEL-specific - we're using at least R16B03
Patch5:		rebar-0005-Remove-any-traces-of-long-time-obsolete-escript-fold.patch
Patch6:		rebar-0006-remove-abnfc.patch
Patch7:		rebar-0007-Remove-support-for-gpb-compiler.patch
# Fedora/EPEL-specific - we're using at least R16B03
Patch8:		rebar-0008-Remove-pre-R15B02-workaround.patch
# Fedora/EPEL-specific - keep until we dump R16B03-1 and 17.x.y entirely
Patch9:		rebar-0009-No-such-function-erlang-timestamp-0.patch
# Fedora/EPEL-specific - allow vsn variable override
Patch10:	rebar-0010-Try-shell-variable-VSN-first.patch
# Fedora/EPEL-specific - allow overriding missind deps error (versions
# mismatch)
Patch11:	rebar-0011-Allow-ignoring-missing-deps.patch
Patch12:	rebar-0012-Don-t-use-deprecated-crypto-rand_uniform-2.patch

%if 0%{?need_bootstrap} < 1
BuildRequires:	erlang-rebar
# FIXME remove later and revisit getopt<->rebar bootstrapping
BuildRequires:  erlang-getopt
%else
BuildRequires:	erlang-asn1
BuildRequires:	erlang-common_test
BuildRequires:	erlang-compiler
#BuildRequires:	erlang-crypto
#BuildRequires:	erlang-dialyzer
#BuildRequires:	erlang-diameter
#BuildRequires:	erlang-edoc
#BuildRequires:	erlang-eflame
#BuildRequires:	erlang-erl_interface
#BuildRequires:	erlang-erlydtl
#BuildRequires:	erlang-erts
BuildRequires:	erlang-eunit
#BuildRequires:	erlang-getopt
#BuildRequires:	erlang-kernel
#BuildRequires:	erlang-lfe
#BuildRequires:	erlang-mustache
#BuildRequires:	erlang-neotoma
BuildRequires:	erlang-parsetools
#BuildRequires:	erlang-protobuffs
#BuildRequires:	erlang-reltool
BuildRequires:	erlang-rpm-macros
#BuildRequires:	erlang-sasl
#BuildRequires:	erlang-snmp
#BuildRequires:	erlang-stdlib
BuildRequires:	erlang-syntax_tools
#BuildRequires:	erlang-tools
%endif

# FIXME wip
#Requires:	erlang-abnfc%{?_isa}
#Requires:	erlang-gpb%{?_isa}

# This one cannot be picked up automatically
# See https://bugzilla.redhat.com/960079
Requires:	erlang-common_test
# Requires for port compiling - no direct references in Rebar's src/*.erl files
Requires:	erlang-erl_interface
# This one cannot be picked up automatically
# See https://bugzilla.redhat.com/960079
Requires:	erlang-parsetools

# FIXME (ROSA): should be detected automatically
Requires:	erlang-asn1
Requires:	erlang-compiler
Requires:	erlang-crypto
Requires:	erlang-dialyzer
Requires:	erlang-diameter
Requires:	erlang-edoc
#Requires:	erlang-eflame
#Requires:	erlang-erlydtl
#Requires:	erlang-erts
Requires:	erlang-eunit
#Requires:	erlang-getopt
#Requires:	erlang-kernel
Requires:	erlang-lfe
#Requires:	erlang-mustache
#Requires:	erlang-neotoma
#Requires:	erlang-protobuffs
Requires:	erlang-reltool
Requires:	erlang-rpm-macros
#Requires:	erlang-sasl
Requires:	erlang-snmp
#Requires:	erlang-stdlib
Requires:	erlang-syntax_tools
Requires:	erlang-tools


Requires:	erlang-rpm-macros >= 0.2.2
Provides:	%{realname} = %{version}-%{release}


%description
Erlang Build Tools.


%prep
%setup -q -n %{realname}-%{version}
%patch1 -p1 -b .load_templates_from_fs
%patch2 -p1 -b .remove_bundled_mustache
%if 0%{?need_bootstrap} < 1
%patch3 -p1 -b .remove_bundled_getopt
%endif
%patch4 -p1 -b .allow_discarding_ports
%patch5 -p1 -b .remove_escript_foldl_3
%patch6 -p1 -b .remove_abnfc
%patch7 -p1 -b .remove_gpb
%patch8 -p1 -b .remove_pre_R15B02
%patch9 -p1 -b .erlang_timestamp_0
%patch10 -p1 -b .vsn_override
%patch11 -p1 -b .skip_deps_checking
%patch12 -p1 -b .erl20

%build
%if 0%{?need_bootstrap} < 1
%{erlang_compile}
%else
./bootstrap
./rebar compile -v
%endif


%install
%{erlang_install}
# Install rebar script itself
install -D -p -m 0755 %{SOURCE1} %{buildroot}%{_bindir}/rebar
# Copy the contents of priv folder
cp -a priv %{buildroot}%{_erllibdir}/%{realname}-%{version}/


%check
%if 0%{?need_bootstrap} < 1
# For using during tests
install -D -p -m 0755 %{SOURCE1} ./rebar
sed -i -e "s,-noshell -noinput,-noshell -noinput -pa .,g" ./rebar
%{rebar_eunit}
%endif


%files
%doc README.md THANKS rebar.config.sample
%doc LICENSE
%{_bindir}/rebar
%{erlang_appdir}/
