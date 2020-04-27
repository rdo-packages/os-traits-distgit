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
Version:        2.3.0
Release:        1%{?dist}
Summary:        A library containing standardized trait strings

License:        ASL 2.0
URL:            https://docs.openstack.org/developer/os-traits/
Source0:        http://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n     python3-%{sname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{sname}}

Requires:       python3-pbr >= 2.0.0

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools

%description -n python3-%{sname}
%{common_desc}

%package -n     python3-%{sname}-tests
Summary:        %{summary}

# Required for the test suite
BuildRequires:  python3-subunit
BuildRequires:  python3-oslotest
BuildRequires:  python3-testtools
BuildRequires:  python3-stestr
BuildRequires:  python3-testscenarios

Requires:       python3-%{sname} = %{version}-%{release}
Requires:       python3-subunit
Requires:       python3-oslotest
Requires:       python3-testtools
Requires:       python3-stestr
Requires:       python3-testscenarios

%description -n python3-%{sname}-tests
This package contains tests for python os-traits library.

%if 0%{?with_doc}
%package -n python-%{sname}-doc
Summary:        Documentation for os-traits

BuildRequires:  python3-sphinx
BuildRequires:  python3-openstackdocstheme

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
%{py3_build}

%if 0%{?with_doc}
# generate html docs
sphinx-build-3 -W -b html doc/source doc/build/html
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install.
%{py3_install}


%check
%{__python3} setup.py test

%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{upstream_version}-py?.?.egg-info
%exclude %{python3_sitelib}/%{pypi_name}/tests

%files -n python3-%{sname}-tests
%{python3_sitelib}/%{pypi_name}/tests

%if 0%{?with_doc}
%files -n python-%{sname}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Mon Apr 27 2020 RDO <dev@lists.rdoproject.org> 2.3.0-1
- Update to 2.3.0

