### RPM external p5-poe-component-child 1.39
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
# a comment to build from scratch increase this number 15
%define perl /usr/bin/env perl
%if "%(echo %cmsplatf | cut -f1 -d_ | sed -e 's|\([A-Za-z]*\)[0-9]*|\1|')" == "osx"
%define perl /usr/bin/perl
%endif

%define perlversion %(%perl -e 'printf "%%vd", $^V')
%define perlarch %(%perl -MConfig -e 'print $Config{archname}')
%define downloadn POE-Component-Child

Source: http://search.cpan.org/CPAN/authors/id/E/EC/ECALDER/%{downloadn}-%{realversion}.tar.gz
# fix wheel cleanup
Patch0: p5-poe-component-child

Requires:  p5-poe

%prep
%setup -n %downloadn-%realversion
%patch0 -p0
%build
LC_ALL=C; export LC_ALL
%perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
make

case %{cmsos} in
    slc4_ia32)
    if ldd /usr/bin/gcc | grep -q /lib64/
    then
        make install
        mv %i/lib/site_perl/%perlversion/x86_64-linux-thread-multi  %i/lib/site_perl/%perlversion/i386-linux-thread-multi
        make clean
        export PATH=/usr/bin/:$PATH
        export GCC_EXEC_PREFIX=/usr/lib/gcc/
        %perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
        make
        make install
     else
        make install
     fi;;
    *)
        make install
    ;;
esac

%install

