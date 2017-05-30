%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname os-traits
%global pypi_name os_traits

%if 0%{?fedora}
# Disabling python 3 as Ansible is not yet ported to Python3.
# Package does not support python3.
%global with_python3 0
%endif

Name:           python-%{sname}
Version:        XXX
Release:        XXX
Summary:        A library containing standardized trait strings

License:        ASL 2.0
URL:            http://www.openstack.org/
Source0:        http://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools

%description
 ostraits A library containing standardized trait strings.Traits are strings
that represent a feature of some resource provider. This library contains the
catalog of constants that have been standardized in the OpenStack community to
refer to a particular hardware, virtualization, storage, network, or device
trait.


%package -n     python2-%{sname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{sname}}

Requires:       python-pbr
Requires:       python-six
%description -n python2-%{sname}
 ostraits A library containing standardized trait strings.Traits are strings
that represent a feature of some resource provider. This library contains the
catalog of constants that have been standardized in the OpenStack community to
refer to a particular hardware, virtualization, storage, network, or device
trait.

%package -n     python2-%{sname}-tests
Summary:        %{summary}

# Required for the test suite
BuildRequires:  python-coverage
BuildRequires:  python-subunit
BuildRequires:  python-oslotest
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
BuildRequires:  python-testtools

Requires:       python2-%{sname} = %{version}-%{release}
Requires:       python-coverage
Requires:       python-subunit
Requires:       python-oslotest
Requires:       python-testrepository
Requires:       python-testscenarios
Requires:       python-testtools

%description -n python2-%{sname}-tests
This package contains tests for python os-traits library.

%if 0%{?with_python3}
%package -n     python3-%{sname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{sname}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools

Requires:       python3-pbr
Requires:       python3-six

%description -n python3-%{sname}
 ostraits A library containing standardized trait strings.Traits are strings
that represent a feature of some resource provider. This library contains the
catalog of constants that have been standardized in the OpenStack community to
refer to a particular hardware, virtualization, storage, network, or device
trait.

%package -n python3-%{sname}-tests
Summary:        %{summary}

# Required for the test suite
BuildRequires:  python3-coverage
BuildRequires:  python3-subunit
BuildRequires:  python3-oslotest
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools

Requires:       python3-%{sname} = %{version}-%{release}
Requires:       python3-coverage
Requires:       python3-subunit
Requires:       python3-oslotest
Requires:       python3-testrepository
Requires:       python3-testscenarios
Requires:       python3-testtools

%description -n python3-%{sname}-tests
This package contains tests for python os-traits library.
%endif


%package -n python-%{sname}-doc
Summary:        os-traits documentation

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx

%description -n python-%{sname}-doc
Documentation for os-traits

%prep
%autosetup -n %{sname}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
# remove requirements
rm -rf {test-,}requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif
# generate html docs 
%{__python2} setup.py build_sphinx
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install.
%if 0%{?with_python3}
%py3_install
%endif

%py2_install


%check
%{__python2} setup.py testr
%if 0%{?with_python3}
%{__python3} setup.py testr
%endif

%files -n python2-%{sname}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{upstream_version}-py?.?.egg-info
%exclude %{python2_sitelib}/%{pypi_name}/tests

%files -n python2-%{sname}-tests
%{python2_sitelib}/%{pypi_name}/tests

%if 0%{?with_python3}
%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{upstream_version}-py?.?.egg-info
%exclude %{python3_sitelib}/%{pypi_name}/tests

%files -n python3-%{sname}-tests
%{python3_sitelib}/%{pypi_name}/tests
%endif

%files -n python-%{sname}-doc
%doc doc/build/html

%changelog
