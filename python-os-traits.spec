# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1

%global sname os-traits
%global pypi_name os_traits
%global common_desc \
OS-traits A library containing standardized trait strings. Traits are strings \
that represent a feature of some resource provider. This library contains the \
catalog of constants that have been standardized in the OpenStack community to \
refer to a particular hardware, virtualization, storage, network, or device \
trait.

Name:           python-%{sname}
Version:        XXX
Release:        XXX
Summary:        A library containing standardized trait strings

License:        ASL 2.0
URL:            https://docs.openstack.org/developer/os-traits/
Source0:        http://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n     python%{pyver}-%{sname}
Summary:        %{summary}
%{?python_provide:%python_provide python%{pyver}-%{sname}}

Requires:       python%{pyver}-pbr >= 2.0.0
Requires:       python%{pyver}-six >= 1.10.0

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools

%description -n python%{pyver}-%{sname}
%{common_desc}

%package -n     python%{pyver}-%{sname}-tests
Summary:        %{summary}

# Required for the test suite
BuildRequires:  python%{pyver}-subunit
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-testtools
BuildRequires:  python%{pyver}-stestr
BuildRequires:  python%{pyver}-testscenarios

Requires:       python%{pyver}-%{sname} = %{version}-%{release}
Requires:       python%{pyver}-subunit
Requires:       python%{pyver}-oslotest
Requires:       python%{pyver}-testtools
Requires:       python%{pyver}-stestr
Requires:       python%{pyver}-testscenarios

%description -n python%{pyver}-%{sname}-tests
This package contains tests for python os-traits library.

%if 0%{?with_doc}
%package -n python-%{sname}-doc
Summary:        os-traits documentation

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-openstackdocstheme

%description -n python-%{sname}-doc
Documentation for os-traits
%endif

%prep
%autosetup -n %{sname}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
# remove requirements
%py_req_cleanup

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
%{pyver_bin} setup.py build_sphinx -b html
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install.
%{pyver_install}


%check
%{pyver_bin} setup.py test

%files -n python%{pyver}-%{sname}
%license LICENSE
%doc README.rst
%{pyver_sitelib}/%{pypi_name}
%{pyver_sitelib}/%{pypi_name}-%{upstream_version}-py?.?.egg-info
%exclude %{pyver_sitelib}/%{pypi_name}/tests

%files -n python%{pyver}-%{sname}-tests
%{pyver_sitelib}/%{pypi_name}/tests

%if 0%{?with_doc}
%files -n python-%{sname}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
