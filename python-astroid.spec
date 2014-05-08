#
# Conditional build:
%bcond_without  python2 # Python 2.x module
%bcond_without  python3 # Python 3.x module

%define	module	astroid
Summary:	Rebuild a new abstract syntax tree from Python's AST
Summary(pl.UTF-8):	Tworzenie nowego abstrakcyjnego drzewa składniowego z pythonowego AST
Name:		python-%{module}
Version:	1.1.1
Release:	1
License:	LGPL v2.1+
Group:		Development/Languages/Python
Source0:	https://pypi.python.org/packages/source/a/astroid/astroid-%{version}.tar.gz
# Source0-md5:	b8153df72670f62bd8d6bc8be99cd184
URL:		http://www.astroid.org/
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-modules >= 1:2.5
%endif
%if %{with python3}
BuildRequires:	python3-2to3
BuildRequires:	python3-devel
BuildRequires:	python3-distribute
BuildRequires:	python3-modules >= 1:3.1
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%endif
Requires:	python-logilab-common >= 0.60.0
Requires:	python-modules
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
Summary:	Rebuild a new abstract syntax tree from Python's AST
Summary(pl.UTF-8):	Tworzenie nowego abstrakcyjnego drzewa składniowego z pythonowego AST
Group:		Development/Languages/Python
Requires:	python3-logilab-common >= 0.60.0
Requires:	python3-modules
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
# drop python 2.5 egg deps
%{__rm} */*/*py2.5.egg

%build
%if %{with python2}
%{__python} setup.py build
%endif
%if %{with python3}
%{__python3} setup.py build --build-base=build3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
%{__python3} setup.py build --build-base=build3 install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%endif

%if %{with python2}
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

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
