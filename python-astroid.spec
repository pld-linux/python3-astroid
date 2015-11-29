#
# Conditional build:
%bcond_without  python2 # Python 2.x module
%bcond_without  python3 # Python 3.x module

%define	module	astroid
Summary:	An abstract syntax tree for Python 2 with inference support
Summary(pl.UTF-8):	Abstrakcyjnego drzewa składniowe dla Pythona 2 z obsługą wywodu
Name:		python-%{module}
Version:	1.3.6
Release:	5
License:	LGPL v2.1+
Group:		Development/Languages/Python
#Source0Download: https://pypi.python.org/pypi/astroid/
Source0:	https://pypi.python.org/packages/source/a/astroid/astroid-%{version}.tar.gz
# Source0-md5:	0d387f5b2e878f424b95af3bfe44e106
Patch0:		modules_without_sources.patch
URL:		http://www.astroid.org/
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools >= 7.0
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.3
BuildRequires:	python3-modules >= 1:3.3
BuildRequires:	python3-setuptools >= 7.0
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%endif
Requires:	python-logilab-common >= 0.60.0
Requires:	python-modules >= 1:2.7
Requires:	python-six
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
Requires:	python3-logilab-common >= 0.60.0
Requires:	python3-modules >= 1:3.3
Requires:	python3-six
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
# drop python 2.5 egg deps
%{__rm} */*/*/*/*/*py2.5.egg

%build
%if %{with python2}
%py_build
%endif
%if %{with python3}
%py3_build --build-base=build3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
%py3_build --build-base=build3 install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
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
%doc ChangeLog README
%{py_sitescriptdir}/astroid
%{py_sitescriptdir}/astroid-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc ChangeLog README
%{py3_sitescriptdir}/astroid
%{py3_sitescriptdir}/astroid-%{version}-py*.egg-info
%endif
