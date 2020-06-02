# TODO: finish apidocs and tests
#
# Conditional build:
%bcond_with	doc	# Sphinx documentation
%bcond_with	tests	# unit tests [R: python-zoneinfo for hypothesis?]
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Powerful data structures for data analysis, time series and statistics
Summary(pl.UTF-8):	Elastyczne struktury danych do analizy danych, szeregów chronologicznych i statystyki
Name:		python-pandas
# keep 0.24.x here for python2 support
Version:	0.24.2
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pandas/
Source0:	https://files.pythonhosted.org/packages/source/p/pandas/pandas-%{version}.tar.gz
# Source0-md5:	6640de14a934a701129b635c6d75801d
URL:		https://pypi.org/project/pandas/
%if %{with python2}
BuildRequires:	python-Cython >= 0.28.2
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-numpy-devel >= 1.12.0
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-dateutil >= 2.5.0
BuildRequires:	python-pytest
BuildRequires:	python-pytz >= 2011k
%endif
%endif
%if %{with python3}
BuildRequires:	python3-Cython >= 0.28.2
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-numpy-devel >= 1.12.0
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-dateutil >= 2.5.0
BuildRequires:	python3-pytest
BuildRequires:	python3-pytz >= 2011k
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg
BuildRequires:	python3-docutils
BuildRequires:	python3-nbconvert
BuildRequires:	python3-nbsphinx
%endif
Requires:	python-modules >= 1:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pandas is a Python package providing fast, flexible, and expressive
data structures designed to make working with structured (tabular,
multidimensional, potentially heterogeneous) and time series data both
easy and intuitive. It aims to be the fundamental high-level building
block for doing practical, real world data analysis in Python.
Additionally, it has the broader goal of becoming the most powerful
and flexible open source data analysis/manipulation tool available in
any language. It is already well on its way toward this goal.

%description -l pl.UTF-8
pandas to pakiet Pythona zapewniający szybkie, elastyczne i wyraziste
struktury danych, zaprojektowane w celu uczynienia pracy z danymi
strukturalnymi (tabelarycznymi, wielowymiarowymi, potencjalnie
heterogenicznymi) oraz szeregami chronologicznymi łatwiejszą i
bardziej intyicyjną. Celem projektu jest pozycja podstawowego bloku
wysokopoziomowego do praktycznej analizy rzeczywistych danych w
Pythonie. Dodatkowym, szerszym celem jest pozycja najbardziej
funkcjonalnego i elastycznego narzędzia o otwartych źródłach,
służącego do analizy i obróbki danych niezależnie od języka.

%package -n python3-pandas
Summary:	Powerful data structures for data analysis, time series and statistics
Summary(pl.UTF-8):	Elastyczne struktury danych do analizy danych, szeregów chronologicznych i statystyki
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-pandas
pandas is a Python package providing fast, flexible, and expressive
data structures designed to make working with structured (tabular,
multidimensional, potentially heterogeneous) and time series data both
easy and intuitive. It aims to be the fundamental high-level building
block for doing practical, real world data analysis in Python.
Additionally, it has the broader goal of becoming the most powerful
and flexible open source data analysis/manipulation tool available in
any language. It is already well on its way toward this goal.

%description -n python3-pandas -l pl.UTF-8
pandas to pakiet Pythona zapewniający szybkie, elastyczne i wyraziste
struktury danych, zaprojektowane w celu uczynienia pracy z danymi
strukturalnymi (tabelarycznymi, wielowymiarowymi, potencjalnie
heterogenicznymi) oraz szeregami chronologicznymi łatwiejszą i
bardziej intyicyjną. Celem projektu jest pozycja podstawowego bloku
wysokopoziomowego do praktycznej analizy rzeczywistych danych w
Pythonie. Dodatkowym, szerszym celem jest pozycja najbardziej
funkcjonalnego i elastycznego narzędzia o otwartych źródłach,
służącego do analizy i obróbki danych niezależnie od języka.

%package apidocs
Summary:	API documentation for Python pandas module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pandas
Group:		Documentation
%if "%{_rpmversion}" >= "4.6"
BuildArch:	noarch
%endif

%description apidocs
API documentation for Python pandas module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pandas.

%prep
%setup -q -n pandas-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
cd build-2/lib.*
%{__python} -m pytest pandas
cd ../..
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
cd build-3/lib.*
%{__python3} -m pytest pandas
cd ../..
%endif
%endif

%if %{with doc}
cd doc
%{__python3} make.py --python-path=$(readlink -f ../build-3/lib.*) html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/pandas/tests
%py_postclean
%endif

%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/pandas/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE README.md RELEASE.md
%dir %{py_sitedir}/pandas
%{py_sitedir}/pandas/*.py[co]
%dir %{py_sitedir}/pandas/_libs
%attr(755,root,root) %{py_sitedir}/pandas/_libs/*.so
%{py_sitedir}/pandas/_libs/__init__.py[co]
%dir %{py_sitedir}/pandas/_libs/tslibs
%attr(755,root,root) %{py_sitedir}/pandas/_libs/tslibs/*.so
%{py_sitedir}/pandas/_libs/tslibs/__init__.py[co]
%{py_sitedir}/pandas/api
%{py_sitedir}/pandas/arrays
%{py_sitedir}/pandas/compat
%{py_sitedir}/pandas/core
%{py_sitedir}/pandas/errors
%dir %{py_sitedir}/pandas/io
%{py_sitedir}/pandas/io/*.py[co]
%{py_sitedir}/pandas/io/clipboard
%{py_sitedir}/pandas/io/formats
%{py_sitedir}/pandas/io/json
%dir %{py_sitedir}/pandas/io/msgpack
%attr(755,root,root) %{py_sitedir}/pandas/io/msgpack/_*.so
%{py_sitedir}/pandas/io/msgpack/*.py[co]
%dir %{py_sitedir}/pandas/io/sas
%attr(755,root,root) %{py_sitedir}/pandas/io/sas/_sas.so
%{py_sitedir}/pandas/io/sas/*.py[co]
%{py_sitedir}/pandas/plotting
%{py_sitedir}/pandas/tseries
%dir %{py_sitedir}/pandas/util
%attr(755,root,root) %{py_sitedir}/pandas/util/_move.so
%{py_sitedir}/pandas/util/*.py[co]
%{py_sitedir}/pandas-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-pandas
%defattr(644,root,root,755)
%doc LICENSE README.md RELEASE.md
%dir %{py3_sitedir}/pandas
%{py3_sitedir}/pandas/*.py
%{py3_sitedir}/pandas/__pycache__
%dir %{py3_sitedir}/pandas/_libs
%attr(755,root,root) %{py3_sitedir}/pandas/_libs/*.cpython-*.so
%{py3_sitedir}/pandas/_libs/__init__.py
%{py3_sitedir}/pandas/_libs/__pycache__
%dir %{py3_sitedir}/pandas/_libs/tslibs
%attr(755,root,root) %{py3_sitedir}/pandas/_libs/tslibs/*.cpython-*.so
%{py3_sitedir}/pandas/_libs/tslibs/__init__.py
%{py3_sitedir}/pandas/_libs/tslibs/__pycache__
%{py3_sitedir}/pandas/api
%{py3_sitedir}/pandas/arrays
%{py3_sitedir}/pandas/compat
%{py3_sitedir}/pandas/core
%{py3_sitedir}/pandas/errors
%dir %{py3_sitedir}/pandas/io
%{py3_sitedir}/pandas/io/*.py
%{py3_sitedir}/pandas/io/__pycache__
%{py3_sitedir}/pandas/io/clipboard
%{py3_sitedir}/pandas/io/formats
%{py3_sitedir}/pandas/io/json
%dir %{py3_sitedir}/pandas/io/msgpack
%attr(755,root,root) %{py3_sitedir}/pandas/io/msgpack/_*.cpython-*.so
%{py3_sitedir}/pandas/io/msgpack/*.py
%{py3_sitedir}/pandas/io/msgpack/__pycache__
%dir %{py3_sitedir}/pandas/io/sas
%attr(755,root,root) %{py3_sitedir}/pandas/io/sas/_sas.cpython-*.so
%{py3_sitedir}/pandas/io/sas/*.py
%{py3_sitedir}/pandas/io/sas/__pycache__
%{py3_sitedir}/pandas/plotting
%{py3_sitedir}/pandas/tseries
%dir %{py3_sitedir}/pandas/util
%attr(755,root,root) %{py3_sitedir}/pandas/util/_move.cpython-*.so
%{py3_sitedir}/pandas/util/*.py
%{py3_sitedir}/pandas/util/__pycache__
%{py3_sitedir}/pandas-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
# TODO: actual apidocs
%doc doc/cheatsheet/Pandas_Cheat_Sheet.pdf
%lang(ja) %doc doc/cheatsheet/Pandas_Cheat_Sheet_JA.pdf
%endif
