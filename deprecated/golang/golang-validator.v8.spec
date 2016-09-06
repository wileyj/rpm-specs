%define url https://gopkg.in/go-playground/validator.v8
%global provider        gopkg
%global provider_tld    in
%global repo_owner      go-playground
%global project         validator.v8
%global import_path     %{provider}.%{provider_tld}/%{repo_owner}/%{project}
%define _summary        %(echo `curl -s %{url} | grep "<title>" | cut -f2 -d ":" | sed 's|</title>||'`)
%define repo %{url}.git
%define gitversion %(echo `date +%s`)
%global _python_bytecompile_errors_terminate_build 0

Name:           golang-%{project}
Version:        %{gitversion}
Release:        1.%{dist}
Summary:        %{_summary}
License:        Go License
Vendor:         %{vendor}
Packager:       %{packager}

BuildRequires:  git golang >= 1.5.0
Requires:       golang >= 1.5.0
Requires:	golang-assert.v1
Provides:       golang-%{provider}
Provides:       golang(%{import_path}) = %{version}-%{release}

%include %{_rpmconfigdir}/macros.d/macros.golang
%description
%{summary}

%prep
if [ -d %{buildroot} ]; then
  %{__rm} -rf %{buildroot}
fi

%build
export GOPATH=%{buildroot}%{gopath}

go get -d -t -u %{import_path}/...
%{__rm} -rf %{buildroot}%{gopath}/src/%{import_path}/.git
%{__rm} -rf %{buildroot}%{gopath}/src/%{provider}.%{provider_tld}/%{repo_owner}/assert.v1
%{__rm} -rf %{buildroot}%{gopath}/src/%{provider}.%{provider_tld}/%{repo_owner}/assert.v1
%{__rm} -f %{buildroot}%{gopath}/src/%{import_path}/.travis.yml
(
    echo '%defattr(-,root,root,-)'
    find %{buildroot}%{gopath}/src/%{import_path} -type d -printf '%%%dir "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot}%{gopath}/src/%{import_path} -type f -printf '"%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot}%{gopath}/pkg/linux_amd64/%{provider}.%{provider_tld}/%{repo_owner} -type f -printf '"%p"\n' | %{__sed} -e 's|%{buildroot}||g'
) > %{name}-%{version}-filelist
echo '%dir "%{gopath}/src/%{import_path}"' >> %{name}-%{version}-filelist
%{__sed} -i -e 's/%dir ""//g' %{name}-%{version}-filelist
%{__sed} -i -e '/^$/d' %{name}-%{version}-filelist


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}
%__rm -f %{__builddir}/%{name}-%{version}-filelist

%files -f %{name}-%{version}-filelist

%changelog
