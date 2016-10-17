# Created by pyp2rpm-1.1.1
%global sname wrapt
%global with_python3 1


%{!?_licensedir: %global license %%doc}

Name:           python-%{sname}
Version:        1.10.8
Release:        1%{?dist}~mos1
Summary:        A Python module for decorators, wrappers and monkey patching

License:        BSD
URL:            https://github.com/GrahamDumpleton/wrapt
Source0:        %{sname}-%{version}.tar.gz

BuildRequires:  python2-devel

%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif

%description
The aim of the wrapt module is to provide a transparent object proxy
for Python, which can be used as the basis for the construction of
function wrappers and decorator functions.

%package doc
Summary:        Documentation for the wrapt module

BuildRequires:  python-sphinx >= 1.2.1

%description doc
Documentation for the wrapt module

%if 0%{?with_python3}
%package -n python3-wrapt
Summary:        A Python module for decorators, wrappers and monkey patching

%description -n python3-wrapt
The aim of the wrapt module is to provide a transparent object proxy
for Python, which can be used as the basis for the construction of
function wrappers and decorator functions.
%endif

%prep
%setup -q -n %{sname}-%{version}

# Remove bundled egg-info in case it exists
rm -rf %{sname}.egg-info

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
CFLAGS="" %{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="" %{__python3} setup.py build
popd
%endif

# for docs
pushd docs
export READTHEDOCS=True
sphinx-build -b html -d build/doctrees . build/html
popd


%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif
%{__python2} setup.py install --skip-build --root %{buildroot}

%files
%doc README.rst
%license LICENSE
%{python2_sitearch}/%{sname}
%{python2_sitearch}/%{sname}-%{version}-py?.?.egg-info

%files doc
%doc docs/build/html
%doc blog

%if 0%{?with_python3}
%files -n python3-wrapt
%doc README.rst
%license LICENSE
%{python3_sitearch}/%{sname}
%{python3_sitearch}/%{sname}-%{version}-py?.?.egg-info
%endif

%changelog
* Mon Oct 03 2016 Andrii Kroshchenko <akroshchenko@mirantis.com> - 1.10.8-1~mos1
- Update package version
- Change condition for building python3 subpackage

* Mon Sep 07 2015 Mikhail Ivanov <mivanov@mirantis.com> - 1.10.4-5~mos8.0.1
- Make source local
- Based on source and .spec from [1]
  [1] http://cbs.centos.org/kojifiles/packages/python-wrapt/1.10.4/5.el7/src/python-wrapt-1.10.4-5.el7.src.rpm

* Sat Apr 11 2015 Ralph Bean <rbean@redhat.com> - 1.10.4-5
- Add python3 subpackage

* Wed Mar 25 2015 Chandan Kumar <chkumar246@gmail.com> - 1.10.4-4
- Added doc files for doc subpackage

* Wed Mar 25 2015 Chandan Kumar <chkumar246@gmail.com> - 1.10.4-3
- Fixed Docs

* Tue Mar 24 2015 Chandan Kumar <chkumar246@gmail.com> - 1.10.4-2
- Removed cflags and group section fro doc subpackage

* Tue Mar 24 2015 Chandan Kumar <chkumar246@gmail.com> - 1.10.4-1
- Bumped to upstream version 1.10.4
- Add docs

* Wed Mar 11 2015 Chandan Kumar <chkumar246@gmail.com> - 1.10.2-1
- Initial package.
