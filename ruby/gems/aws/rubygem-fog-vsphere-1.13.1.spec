%define filelist %{name}-%{version}-filelist
%global sensu_base %{_sysconfdir}/sensu
%global plugins    %{sensu_base}/plugins
%global metrics    %{sensu_base}/metrics
%global handlers   %{sensu_base}/handlers
%global extensions %{sensu_base}/extensions
%global mutators   %{sensu_base}/mutators

%global gem_name fog-vsphere
Name: rubygem-fog-vsphere
Version: 1.13.1
Release: 1.%{dist}
Summary: rubygem fog-vsphere
Group: Development/Languages
License: MIT
URL: https://github.com/fog/fog-vsphere
Vendor: %{vendor}
Packager: %{packager}
Requires: ruby rubygems
Provides: rubygem-fog-vsphere = %{version}
Provides: rubygem(fog-vsphere) = %{version}
Obsoletes: rubygem-fog-vsphere < %{version}
Obsoletes: rubygem(fog-vsphere) < %{version}


Requires: rubygem-fog-core 
Requires: rubygem-rbvmomi   = 1.9


%description
This library can be used as a module for `fog` or as standalone provider to use vSphere in applications.

%prep
%build
%install
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
gem install --install-dir %{buildroot}/%{gem_dir} --bindir %{buildroot}/%{_bindir} --force --no-rdoc --no-ri --no-doc --ignore-dependencies fog-vsphere -v %{version}
(
    cd %{buildroot}
    echo '%defattr(-,root,root,-)'
    find %{buildroot} -type d -not \( -path */u/* -o -path */u -o -path */etc -o -path */etc/* -o -path */var -o -path */var/* -prune \) -printf '%%%dir "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot} -type f -not \( -path */u/* -o -path */u -o -path */etc -o -path */etc/* -o -path */var -o -path */var/* -prune \) -printf '"%p"\n' | %{__sed} -e 's|%{buildroot}||g'
) >  %{filelist}
sed -i -e 's|%dir ""||g' %{filelist}
%{__sed} -i -e 's/%dir ""//g' %{filelist}
%{__sed} -i -e '/^$/d' %{filelist}

find %{buildroot} -type f -exec sed -i -e 's|/usr/local/bin/ruby|/usr/bin/ruby|g' {} \;

if [[ "%{name}" == *plugins* || "%{name}" == *metrics* || "%{name}" == *mutator* || "%{name}" == *handler* ]]; then
  if [ -d %{buildroot}%{_bindir} ]; then
    for file in `ls %{buildroot}%{_bindir}`
    do
      if [[ $file == metric* ]]; then
        if [ ! -d %{buildroot}%{metrics} ];then
            %__mkdir_p %{buildroot}%{metrics}
        fi
        %{__ln_s} -f %{_bindir}/$file %{buildroot}%{metrics}/$file
        echo "%{metrics}/$file" >> %{filelist}
      elif [[ $file == check* ]]; then
        if [ ! -d %{buildroot}%{plugins} ];then
            %__mkdir_p %{buildroot}%{plugins}
        fi
        %{__ln_s} -f %{_bindir}/$file %{buildroot}%{plugins}/$file
        echo "%{plugins}/$file" >> %{filelist}

      elif [[ $file == mutator* ]]; then
        if [ ! -d %{buildroot}%{mutators} ];then
            %__mkdir_p %{buildroot}%{mutators}
        fi
        %{__ln_s} -f %{_bindir}/$file %{buildroot}%{mutators}/$file
        echo "%{mutators}/$file" >> %{filelist}

      elif [[ $file == handle* ]]; then
        if [ ! -d %{buildroot}%{handlers} ];then
            %__mkdir_p %{buildroot}%{handlers}
        fi
        %{__ln_s} -f %{_bindir}/$file %{buildroot}%{handlers}/$file
        echo "%{handlers}/$file" >> %{filelist}

      else
        if [ ! -d %{buildroot}%{plugins} ];then
            %__mkdir_p %{buildroot}%{plugins}
        fi
        %{__ln_s} -f %{_bindir}/$file %{buildroot}%{plugins}/$file
        echo "%{plugins}/$file" >> %{filelist}
      fi
    done
  fi
fi
exit 0

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{filelist}" != "/" ] && %__rm -rf %{_builddir}/%{filelist}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files -f %{filelist}

## end file