
# Conditional build:
%bcond_without  python2 # Python 2.x module
%bcond_without  python3 # Python 3.x module

%define	module	astroid
Summary:	Rebuild a new abstract syntax tree from Python's ast
Summary(pl.UTF-8):	Abstrakcyjne drzewa składniowe Pythona nowej generacji
Name:		python-%{module}
Version:	1.0.0
Release:	1
License:	LGPL v2.1+
Group:		Development/Languages/Python
Source0:	https://pypi.python.org/packages/source/a/astroid/astroid-1.0.0.tar.gz
# Source0-md5:	e74430dfbbe09cd18ef75bd76f95425a
URL:		http://www.astroid.org/
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-modules >= 1:2.5
%endif
%if %{with python3}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	python3-2to3
BuildRequires:	python3-devel
BuildRequires:	python3-distribute
BuildRequires:	python3-modules >= 1:3.1
%endif
%pyrequires_eq	python-modules
Requires:	python-logilab-common >= 0.53.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The aim of this module is to provide a common base representation of python source code for projects such as pychecker, pyreverse, pylint... Well, actually the development of this library is essentially governed by pylint's needs. It used to be called logilab-astng.

%description -l pl.UTF-8
Celem tego modułu jest dostarczenie wspólnej bazowej reprezentacji
kodu źródłowego Pythona dla projektów takich jak pychecker, pyreverse,
pylint... Właściwie tworzenie tej biblioteki jest istotnie kierowane
potrzebami pylinta.

%package -n python3-%{module}
Summary:	Python Abstract Syntax Tree New Generation
Summary(pl.UTF-8):	Abstrakcyjne drzewa składniowe Pythona nowej generacji
Group:		Development/Languages/Python
%pyrequires_eq	python3-modules
Requires:	python3-logilab-common >= 0.53.0

%description -n python3-%{module}
The aim of this module is to provide a common base representation of python source code for projects such as pychecker, pyreverse, pylint... Well, actually the development of this library is essentially governed by pylint's needs. It used to be called logilab-astng.

%description -n python3-%{module} -l pl.UTF-8
Celem tego modułu jest dostarczenie wspólnej bazowej reprezentacji
kodu źródłowego Pythona dla projektów takich jak pychecker, pyreverse,
pylint... Właściwie tworzenie tej biblioteki jest istotnie kierowane
potrzebami pylinta.

%prep
%setup -q -n %{module}-%{version}
# drop python 2.5 egg deps
rm */*/*py2.5.egg

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

# this file is packaged with python3-logilab-common
#rm $RPM_BUILD_ROOT%{py3_sitescriptdir}/logilab/__init__.py
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
#%{py_sitescriptdir}/astroid-%{version}-py*-nspkg.pth
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc ChangeLog README
%{py3_sitescriptdir}/astroid
%{py3_sitescriptdir}/astroid-%{version}-py*.egg-info
#%{py3_sitescriptdir}/astroid-%{version}-py*-nspkg.pth
%endif
