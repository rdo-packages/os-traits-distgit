%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
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

License:        Apache-2.0
URL:            https://docs.openstack.org/developer/os-traits/
Source0:        http://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        http://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  git-core
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n     python3-%{sname}
Summary:        %{summary}

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
%description -n python3-%{sname}
%{common_desc}

%package -n     python3-%{sname}-tests
Summary:        %{summary}

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

%description -n python-%{sname}-doc
Documentation for os-traits
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{sname}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
# generate html docs
%tox -e docs
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install.
%pyproject_install


%check
%tox -e %{default_toxenv}

%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{upstream_version}-py%{python3_version}.dist-info
%exclude %{python3_sitelib}/%{pypi_name}/tests

%files -n python3-%{sname}-tests
%{python3_sitelib}/%{pypi_name}/tests

%if 0%{?with_doc}
%files -n python-%{sname}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
