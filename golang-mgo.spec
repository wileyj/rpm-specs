%define srcname mgo

%global provider        gopkg
%global provider_tld    in
%global project        	mgo.v2-unstable
%global import_path     %{provider}.%{provider_tld}/%{project}

Name:           golang-%{srcname}
Version:        2.0.0
Release:        1.%{dist}
Summary:	A lightweight RESTful web framework for Go.
License:        MIT
Vendor: %{vendor}
Packager: %{packager}
Source0:        golang-%{srcname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:	git
BuildRequires:	golang-check
BuildRequires:  golang >= 1.2.1-3
#BuildRequires: mongo
Requires:       golang >= 1.2.1-3
Requires:       golang
Provides:       golang-%{srcname}
Provides:       golang(%{import_path}) = %{version}-%{release}
Provides:       golang(%{import_path}/bson) = %{version}-%{release}
Provides:       golang(%{import_path}/testdb) = %{version}-%{release}
Provides:       golang(%{import_path}/txn) = %{version}-%{release}
Provides:       golang(%{import_path}/internal/scram) = %{version}-%{release}

%description
%{summary}

This package contains library source intended for 
building other packages which use %{project}.

%prep
%setup -q -n golang-%{srcname}-%{version}

%build
git pull

%install
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
cp -pav *.go %{buildroot}/%{gopath}/src/%{import_path}/
cp -rpav bson %{buildroot}/%{gopath}/src/%{import_path}/
cp -rpav testdb %{buildroot}/%{gopath}/src/%{import_path}/
cp -rpav txn %{buildroot}/%{gopath}/src/%{import_path}/  
cp -rpav internal %{buildroot}/%{gopath}/src/%{import_path}/

%{__mkdir_p} %{buildroot}/%{gopath}/src/labix.org/v2
cd %{buildroot}/%{gopath}/src
%{__ln_s} -f %{gopath}/src/%{import_path}/ labix.org/v2/mgo

%check
#GOPATH=%{buildroot}/%{gopath}:%{gopath} go test %{import_path}

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%doc README.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%{gopath}/src/%{import_path}
%{gopath}/src/labix.org/v2/mgo
%changelog
