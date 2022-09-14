#
# Conditional build:
%bcond_with	tests	# unit tests (not included in sdist)

%define	module	astroid
Summary:	An abstract syntax tree for Python 3 with inference support
Summary(pl.UTF-8):	Abstrakcyjnego drzewa składniowe dla Pythona 3 z obsługą wywodu
Name:		python3-%{module}
# keep version compatible with pylint.spec (2.12.x for pylint 2.15.x)
Version:	2.12.9
Release:	1
License:	LGPL v2.1+
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/astroid/
Source0:	https://files.pythonhosted.org/packages/source/a/astroid/astroid-%{version}.tar.gz
# Source0-md5:	5aba64ba978ad52fc19e80c0a93ff223
URL:		https://github.com/PyCQA/astroid
BuildRequires:	python3-devel >= 1:3.7.2
BuildRequires:	python3-modules >= 1:3.7.2
BuildRequires:	python3-setuptools >= 1:62.6
%if %{with tests}
BuildRequires:	python3-lazy-object-proxy >= 1.4
BuildRequires:	python3-pytest
BuildRequires:	python3-six >= 1.12
%if "%{py3_ver}" == "3.7"
BuildRequires:	python3-typed_ast >= 1.4.0
BuildRequires:	python3-typed_ast < 2.0
%endif
%if "%{_ver_lt '%{py3_ver}' '3.10'}" == "1"
BuildRequires:	python3-typing_extensions >= 3.10
%endif
%if "%{_ver_lt '%{py3_ver}' '3.11'}" == "1"
BuildRequires:	python3-wrapt >= 1.11
%else
BuildRequires:	python3-wrapt >= 1.14
%endif
BuildRequires:	python3-wrapt < 2
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-modules >= 1:3.7.2
Obsoletes:	python3-logilab-astng < 1
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

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd) \
%{__python3} -m pytest tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS.txt README.rst
%{py3_sitescriptdir}/astroid
%{py3_sitescriptdir}/astroid-%{version}-py*.egg-info
