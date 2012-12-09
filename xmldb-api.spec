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

%define gcj_support 0

%define bname        xmldb
%define cvs_version    20011111cvs

Name:       xmldb-api
Version:    0.1
Release:    %mkrel 0.1.%{cvs_version}.1.2.6
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
BuildRequires:    xerces-j2
BuildRequires:    xml-commons-jaxp-1.3-apis
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
%remove_java_binaries

cp %{SOURCE1} build.xml

%patch0

%build
export CLASSPATH=$(build-classpath junit xalan-j2)
usejikes=false 
%{ant} -Dant.build.javac.source=1.5 -Dant.build.javac.target=1.5 -Dsrc=. -Djarname=%{name} -Dsdk.jarname=%{name}-sdk jar javadoc

%install
rm -rf %{buildroot}

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 dist/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
install -m 644 dist/%{name}-sdk.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-sdk-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} ${jar/-%{version}/}; done)
# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/doc/api $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

#license
install -d -m 755 $RPM_BUILD_ROOT/%{_docdir}/%{name}-%{version}
cp %{SOURCE2} $RPM_BUILD_ROOT/%{_docdir}/%{name}-%{version}

%{gcj_compile}

%clean
rm -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}
%endif

%if %{gcj_support}
%postun
%{clean_gcjdb}
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


%changelog
* Tue Apr 26 2011 Paulo Andrade <pcpa@mandriva.com.br> 1:0.1-0.1.20011111cvs.1.2.6mdv2011.0
+ Revision: 659454
- Rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 1:0.1-0.1.20011111cvs.1.2.5mdv2009.1
+ Revision: 350884
- rebuild

* Mon Jul 28 2008 Alexander Kurtakov <akurtakov@mandriva.org> 1:0.1-0.1.20011111cvs.1.2.4mdv2009.0
+ Revision: 251948
- fix build

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Anssi Hannula <anssi@mandriva.org>
    - buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 1:0.1-0.1.20011111cvs.1.2.2mdv2008.0
+ Revision: 87281
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Tue Jul 03 2007 David Walluck <walluck@mandriva.org> 1:0.1-0.1.20011111cvs.1.2.1mdv2008.0
+ Revision: 47333
- Import xmldb-api



* Mon Feb 12 2007 Deepak Bhole <dbhole@redhat.com> 1:0.1-0.1.20011111cvs.1jpp.1.fc7
- Update to Fedora specs

* Fri Sep 08 2006 Ralph Apel <r.apel at r-apel.de> 0:0.1-0.20041010.3jpp
- Add post/postun Requires for javadoc
- Add gcj_support option

* Mon May 29 2006 Fernando Nasser <fnasser@redhat.com> 0:0.1-0.20041010.2jpp
- First JPP 1.7 build

* Thu Oct 20 2005 Ralph Apel <r.apel at r-apel.de> 0:0.1-0.20041010.1jpp
- Upgrade to recent
- Add  -common

* Tue Apr 26 2005 Fernando Nasser <fnasser@redhat.com> 0:0.1-0.20011111.3jpp
- Rebuild with standard version scheme

* Thu Aug 26 2004 Ralph Apel <r.apel at r-apel.de> 0:20011111-3jpp
- Build with ant-1.6.2

* Mon May 05 2003 David Walluck <david@anti-microsoft.org> 0:20011111-2jpp
- update for JPackage 1.5
- fix sdk package summary
- fix for newer javac's

* Thu Mar 28 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 20011111-1jpp 
- first JPackage release
