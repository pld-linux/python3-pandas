# TODO: finish apidocs and tests
#
# Conditional build:
%bcond_with	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (some files missing in sdist, some inaccuracy errors, some with 32-bit time_t)

Summary:	Powerful data structures for data analysis, time series and statistics
Summary(pl.UTF-8):	Elastyczne struktury danych do analizy danych, szeregów chronologicznych i statystyki
Name:		python3-pandas
Version:	2.2.3
Release:	3
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pandas/
Source0:	https://files.pythonhosted.org/packages/source/p/pandas/pandas-%{version}.tar.gz
# Source0-md5:	67cae6d658e0e0716518afd84d7d43ce
Patch0:		no-strict-deps.patch
URL:		https://pypi.org/project/pandas/
BuildRequires:	libstdc++-devel
BuildRequires:	meson >= 1.2.1
BuildRequires:	patchelf
BuildRequires:	python3-Cython >= 3.0.5
BuildRequires:	python3-Cython < 3.1
BuildRequires:	python3-build
BuildRequires:	python3-devel >= 1:3.9
BuildRequires:	python3-installer
BuildRequires:	python3-meson-python >= 0.13.1
BuildRequires:	python3-numpy-devel >= 2.0
BuildRequires:	python3-versioneer
BuildRequires:	python3-wheel
%if %{with tests}
BuildRequires:	python3-dateutil >= 2.8.2
# used by hypothesis
BuildRequires:	python3-dateutil-zoneinfo >= 2.8.1
BuildRequires:	python3-hypothesis >= 5.5.3
%if "%{py3_ver}" < "3.11"
BuildRequires:	python3-numpy >= 1.22.4
%endif
%if "%{py3_ver}" == "3.11"
BuildRequires:	python3-numpy >= 1.23.2
%endif
%if "%{py3_ver}" >= "3.12"
BuildRequires:	python3-numpy >= 1.26.0
%endif
BuildRequires:	python3-pytest >= 6.0
BuildRequires:	python3-pytest-asyncio
BuildRequires:	python3-pytest-xdist >= 1.31
BuildRequires:	python3-pytz >= 2020.1
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	sphinx-pdg >= 2
BuildRequires:	python3-ipython
BuildRequires:	python3-jinja2
BuildRequires:	python3-matplotlib
BuildRequires:	python3-nbconvert
BuildRequires:	python3-nbsphinx
BuildRequires:	python3-numpydoc
BuildRequires:	python3-sphinx_panels
%endif
Requires:	python3-modules >= 1:3.8
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

%package apidocs
Summary:	API documentation for Python pandas module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pandas
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Python pandas module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pandas.

%prep
%setup -q -n pandas-%{version}
%patch -P0 -p1

%build
%py3_build_pyproject

%if %{with tests}
cd build-3/lib.*
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_asyncio.plugin,xdist.plugin \
%{__python3} -m pytest pandas
cd ../..
%endif

%if %{with doc}
cd doc
%{__python3} make.py --python-path=$(readlink -f ../build-3/lib.*) html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/pandas/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%dir %{py3_sitedir}/pandas
%{py3_sitedir}/pandas/*.py
%{py3_sitedir}/pandas/__pycache__
%{py3_sitedir}/pandas/_config
%dir %{py3_sitedir}/pandas/_libs
%attr(755,root,root) %{py3_sitedir}/pandas/_libs/*.cpython-*.so
%{py3_sitedir}/pandas/_libs/__init__.py
%{py3_sitedir}/pandas/_libs/*.py[ix]
%{py3_sitedir}/pandas/_libs/__pycache__
%dir %{py3_sitedir}/pandas/_libs/tslibs
%attr(755,root,root) %{py3_sitedir}/pandas/_libs/tslibs/*.cpython-*.so
%{py3_sitedir}/pandas/_libs/tslibs/__init__.py
%{py3_sitedir}/pandas/_libs/tslibs/*.py[ix]
%{py3_sitedir}/pandas/_libs/tslibs/__pycache__
%dir %{py3_sitedir}/pandas/_libs/window
%attr(755,root,root) %{py3_sitedir}/pandas/_libs/window/*.cpython-*.so
%{py3_sitedir}/pandas/_libs/window/__init__.py
%{py3_sitedir}/pandas/_libs/window/*.py[ix]
%{py3_sitedir}/pandas/_libs/window/__pycache__
%{py3_sitedir}/pandas/_testing
%{py3_sitedir}/pandas/api
%{py3_sitedir}/pandas/arrays
%{py3_sitedir}/pandas/compat
%{py3_sitedir}/pandas/core
%{py3_sitedir}/pandas/errors
%dir %{py3_sitedir}/pandas/io
%{py3_sitedir}/pandas/io/*.py
%{py3_sitedir}/pandas/io/__pycache__
%{py3_sitedir}/pandas/io/clipboard
%{py3_sitedir}/pandas/io/excel
%{py3_sitedir}/pandas/io/formats
%{py3_sitedir}/pandas/io/json
%{py3_sitedir}/pandas/io/parsers
%dir %{py3_sitedir}/pandas/io/sas
%{py3_sitedir}/pandas/io/sas/*.py
%{py3_sitedir}/pandas/io/sas/__pycache__
%{py3_sitedir}/pandas/plotting
%{py3_sitedir}/pandas/tseries
%{py3_sitedir}/pandas/util
%{py3_sitedir}/pandas-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
# TODO: actual apidocs
%doc doc/cheatsheet/Pandas_Cheat_Sheet.pdf
%lang(ja) %doc doc/cheatsheet/Pandas_Cheat_Sheet_JA.pdf
%endif
