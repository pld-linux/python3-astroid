#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_with	python2	# Python 2.x module
%bcond_without	python3	# Python 3.x module

%define	module	astroid
Summary:	An abstract syntax tree for Python 2 with inference support
Summary(pl.UTF-8):	Abstrakcyjnego drzewa składniowe dla Pythona 2 z obsługą wywodu
Name:		python-%{module}
Version:	2.3.2
Release:	1
License:	LGPL v2.1+
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/astroid/
Source0:	https://files.pythonhosted.org/packages/source/a/astroid/astroid-%{version}.tar.gz
# Source0-md5:	b2cd5c0383ff33c1410e737c2607aa7a
Patch0:		%{name}-deps.patch
URL:		https://github.com/PyCQA/astroid
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-pytest-runner
BuildRequires:	python-setuptools >= 7.0
%if %{with tests}
BuildRequires:	python-lazy-object-proxy >= 1.4
BuildRequires:	python-pytest
BuildRequires:	python-six >= 1.12
BuildRequires:	python-typed_ast >= 1.4.0
BuildRequires:	python-typed_ast < 1.5
BuildRequires:	python-wrapt >= 1.11
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-pytest-runner
BuildRequires:	python3-setuptools >= 7.0
%if %{with tests}
BuildRequires:	python3-lazy-object-proxy >= 1.4
BuildRequires:	python3-pytest
BuildRequires:	python3-six >= 1.12
%if "%{py3_ver}" < "3.8"
BuildRequires:	python3-typed_ast >= 1.4.0
BuildRequires:	python3-typed_ast < 1.5
%endif
BuildRequires:	python3-wrapt >= 1.11
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.7
Obsoletes:	python-logilab-astng
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The aim of this module is to provide a common base representation of
Python source code for projects such as pychecker, pyreverse,
pylint... Well, actually the development of this library is
essentially governed by pylint's needs. It used to be called
logilab-astng.

%description -l pl.UTF-8
Celem tego modułu jest dostarczenie wspólnej bazowej reprezentacji
kodu źródłowego Pythona dla projektów takich jak pychecker, pyreverse,
pylint... Właściwie tworzenie tej biblioteki jest istotnie kierowane
potrzebami pylinta. Dawniej nazywała się logilab-astng.

%package -n python3-%{module}
Summary:	An abstract syntax tree for Python 3 with inference support
Summary(pl.UTF-8):	Abstrakcyjnego drzewa składniowe dla Pythona 3 z obsługą wywodu
Group:		Development/Languages/Python
Requires:	python3-modules >= 1:3.5
%if "%{py3_ver}" < "3.8"
# not detected by rpm from rule:
# [:implementation_name == "cpython" and python_version < "3.8"]
Requires:	python3-typed_ast >= 1.4.0
Requires:	python3-typed_ast < 1.5
%endif
Obsoletes:	python3-logilab-astng

%description -n python3-%{module}
The aim of this module is to provide a common base representation of
Python source code for projects such as pychecker, pyreverse,
pylint... Well, actually the development of this library is
essentially governed by pylint's needs. It used to be called
logilab-astng.

%description -n python3-%{module} -l pl.UTF-8
Celem tego modułu jest dostarczenie wspólnej bazowej reprezentacji
kodu źródłowego Pythona dla projektów takich jak pychecker, pyreverse,
pylint... Właściwie tworzenie tej biblioteki jest istotnie kierowane
potrzebami pylinta. Dawniej nazywała się logilab-astng.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

# non-deterministic (skipped if numpy not installed; unittest_brain_numpy_core_multiarray.py fails with numpy 1.16.5
%{__rm} astroid/tests/unittest_brain_numpy_*
# test_knownValues_get_builtin_module_part fails
%{__rm} astroid/tests/unittest_modutils.py

%build
%if %{with python2}
%py_build

%if %{with tests}
%{__python} -m pytest astroid/tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
%{__python3} -m pytest astroid/tests
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
%py3_install
%endif

%if %{with python2}
%py_install

%py_postclean
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc ChangeLog README.rst
%{py_sitescriptdir}/astroid
%{py_sitescriptdir}/astroid-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc ChangeLog README.rst
%{py3_sitescriptdir}/astroid
%{py3_sitescriptdir}/astroid-%{version}-py*.egg-info
%endif
