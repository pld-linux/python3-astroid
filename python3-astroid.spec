#
# Conditional build:
%bcond_with	tests	# unit tests (not included in sdist)

%define	module	astroid
Summary:	An abstract syntax tree for Python 3 with inference support
Summary(pl.UTF-8):	Abstrakcyjnego drzewa składniowe dla Pythona 3 z obsługą wywodu
Name:		python3-%{module}
# keep version compatible with pylint.spec (2.9.x for 2.12.x)
Version:	2.9.3
Release:	2
License:	LGPL v2.1+
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/astroid/
Source0:	https://files.pythonhosted.org/packages/source/a/astroid/astroid-%{version}.tar.gz
# Source0-md5:	5194ffb97eafaff6afbe1869606b7d4d
URL:		https://github.com/PyCQA/astroid
BuildRequires:	python3-devel >= 1:3.6.2
BuildRequires:	python3-modules >= 1:3.6.2
BuildRequires:	python3-pytest-runner
BuildRequires:	python3-setuptools >= 1:20.0
%if %{with tests}
BuildRequires:	python3-lazy-object-proxy >= 1.4
BuildRequires:	python3-pytest
BuildRequires:	python3-six >= 1.12
%if "%{py3_ver}" < "3.8"
BuildRequires:	python3-typed_ast >= 1.4.0
BuildRequires:	python3-typed_ast < 2.0
%endif
BuildRequires:	python3-typing_extensions >= 3.10
BuildRequires:	python3-wrapt >= 1.11
BuildRequires:	python3-wrapt < 1.14
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-modules >= 1:3.6.2
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
%{__python3} -m pytest tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{py3_sitescriptdir}/astroid
%{py3_sitescriptdir}/astroid-%{version}-py*.egg-info
