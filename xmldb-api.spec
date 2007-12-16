# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define _with_gcj_support 1
%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

%define bname        xmldb
%define cvs_version    20011111cvs

Name:       xmldb-api
Version:    0.1
Release:    %mkrel 0.1.%{cvs_version}.1.2.3
Epoch:      1
Summary:    XML:DB API for Java
License:    BSD
Group:      Development/Java
# wget http://trumpetti.atm.tut.fi/gentoo/distfiles/xmldb-api-11112001.tar.gz
Source0:     xmldb-xapi-%{cvs_version}-src.tar.gz
# http://sources.gentoo.org/viewcvs.py/gentoo-x86/dev-java/xmldb/files/build-20011111.xml?rev=1.1.1.1&view=markup
Source1:    %{name}-build.xml
Source2:    %{name}-license.txt
Patch0:     %{name}-syntaxfix.patch
Url:        http://xmldb-org.sourceforge.net
BuildRequires:    ant >= 0:1.6
BuildRequires:    java-rpmbuild >= 0:1.6
BuildRequires:    junit
BuildRequires:    xalan-j2
Requires(pre):    jpackage-utils >= 0:1.6
Requires(post):   jpackage-utils >= 0:1.6
Requires:         junit
Requires:         xalan-j2
%if %{gcj_support}
BuildRequires:          java-gcj-compat-devel
%endif
%if ! %{gcj_support}
BuildArch:      noarch
%endif
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root

%description
The API interfaces are what driver developers must implement when creating a
new driver and are the interfaces that applications are developed against. 
Along with the interfaces a concrete DriverManager implementation is also
provides.

%package sdk
Summary:    SDK for %{name}
Group:      Development/Java
Requires:   %{name} = %{epoch}:%{version}-%{release}

%description sdk
The reference implementation provides a very simple file system based
implementation of the XML:DB API. This provides what is basically a very
simple native XML database that uses directories to represent collections and
just stores the XML in files.

The driver development kit provides a set of base classes that can be 
extended to simplify and speed the development of XML:DB API drivers. These
classes are used to provide the basis for the reference implementation and
therefore a simple example of how a driver can be implemented. Using the SDK
classes significantly reduces the amount of code that must be written to
create a new driver.

Along with the SDK base classes the SDK also contains a set of jUnit test
cases that can be used to help validate the driver while it is being
developed. The test cases are still in development but there are enough tests
currently to be useful.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n xmldb 
# remove all binary libs
for j in $(find . -name "*.jar"); do
    rm -f $j
done

cp %{SOURCE1} build.xml

%patch0

%build
export CLASSPATH=$(build-classpath junit xalan-j2)
usejikes=false %{ant} -Dsrc=. -Djarname=%{name} -Dsdk.jarname=%{name}-sdk jar javadoc

%install
rm -rf %{buildroot}

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 dist/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
install -m 644 dist/%{name}-sdk.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-sdk-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} ${jar/-%{version}/}; done)
# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/doc/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

#license
install -d -m 755 $RPM_BUILD_ROOT/%{_docdir}/%{name}-%{version}
cp %{SOURCE2} $RPM_BUILD_ROOT/%{_docdir}/%{name}-%{version}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf %{buildroot}

%if %{gcj_support}
%post
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(-,root,root)
%doc %{_docdir}/%{name}-%{version}
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}.jar
%if %{gcj_support}
%attr(-,root,root) %dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.*
%endif

%files sdk
%defattr(-,root,root)
%{_javadir}/%{name}-sdk-%{version}.jar
%{_javadir}/%{name}-sdk.jar
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-sdk-%{version}.jar.*
%endif

%files javadoc
%defattr(-,root,root)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
