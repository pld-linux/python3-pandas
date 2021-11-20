# TODO: finish apidocs and tests
#
# Conditional build:
%bcond_with	doc	# Sphinx documentation
%bcond_with	tests	# unit tests [R: python-zoneinfo for hypothesis?]

Summary:	Powerful data structures for data analysis, time series and statistics
Summary(pl.UTF-8):	Elastyczne struktury danych do analizy danych, szeregów chronologicznych i statystyki
Name:		python3-pandas
Version:	1.0.4
Release:	3
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pandas/
Source0:	https://files.pythonhosted.org/packages/source/p/pandas/pandas-%{version}.tar.gz
# Source0-md5:	ddd27554a81c35cbd0d0f693a0f3c81f
URL:		https://pypi.org/project/pandas/
BuildRequires:	python3-Cython >= 0.29.13
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-numpy-devel >= 1.13.3
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-dateutil >= 2.6.1
BuildRequires:	python3-pytest
BuildRequires:	python3-pytz >= 2017.2
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg >= 2
BuildRequires:	python3-docutils
BuildRequires:	python3-ipython
BuildRequires:	python3-jinja2
BuildRequires:	python3-matplotlib
BuildRequires:	python3-nbconvert
BuildRequires:	python3-nbsphinx
BuildRequires:	python3-numpydoc
%endif
Requires:	python3-modules >= 1:3.6
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

%build
%py3_build

%if %{with tests}
cd build-3/lib.*
%{__python3} -m pytest pandas
cd ../..
%endif

%if %{with doc}
cd doc
%{__python3} make.py --python-path=$(readlink -f ../build-3/lib.*) html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/pandas/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md RELEASE.md
%dir %{py3_sitedir}/pandas
%{py3_sitedir}/pandas/*.py
%{py3_sitedir}/pandas/__pycache__
%{py3_sitedir}/pandas/_config
%dir %{py3_sitedir}/pandas/_libs
%attr(755,root,root) %{py3_sitedir}/pandas/_libs/*.cpython-*.so
%{py3_sitedir}/pandas/_libs/__init__.py
%{py3_sitedir}/pandas/_libs/__pycache__
%dir %{py3_sitedir}/pandas/_libs/tslibs
%attr(755,root,root) %{py3_sitedir}/pandas/_libs/tslibs/*.cpython-*.so
%{py3_sitedir}/pandas/_libs/tslibs/__init__.py
%{py3_sitedir}/pandas/_libs/tslibs/__pycache__
%dir %{py3_sitedir}/pandas/_libs/window
%attr(755,root,root) %{py3_sitedir}/pandas/_libs/window/*.cpython-*.so
%{py3_sitedir}/pandas/_libs/window/__init__.py
%{py3_sitedir}/pandas/_libs/window/__pycache__
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
%dir %{py3_sitedir}/pandas/io/sas
%attr(755,root,root) %{py3_sitedir}/pandas/io/sas/_sas.cpython-*.so
%{py3_sitedir}/pandas/io/sas/*.py
%{py3_sitedir}/pandas/io/sas/__pycache__
%{py3_sitedir}/pandas/plotting
%{py3_sitedir}/pandas/tseries
%{py3_sitedir}/pandas/util
%{py3_sitedir}/pandas-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
# TODO: actual apidocs
%doc doc/cheatsheet/Pandas_Cheat_Sheet.pdf
%lang(ja) %doc doc/cheatsheet/Pandas_Cheat_Sheet_JA.pdf
%endif
