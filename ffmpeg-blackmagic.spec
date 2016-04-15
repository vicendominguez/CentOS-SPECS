%global bmdsdk_path /tmp/Blackmagic_DeckLink_SDK_10.6.1/Linux/include/
# you need to unzip Blackmagic_DeckLink_SDK_10.1.1.zip to Blackmagic_DeckLink_SDK_10.1.1 directory name in /tmp

%define srcname ffmpeg
%define bmd %{srcname}-blackmagic

%{?_with_nodist:Name:  %{bmd}-nodist}
%{!?_with_nodist:Name: %{bmd}}

Summary:       Hyper fast MPEG1/MPEG4/H263/RV and AC3/MPEG audio encoder + fdk_aac + x264 + x265
Version:       2.8.6
Release:       2%{?dist}
License:       GPLv3+
Group:         System Environment/Libraries

Source:        http://ffmpeg.org/releases/%{srcname}-%{version}.tar.gz
URL:           http://ffmpeg.sourceforge.net/
BuildRoot:     %{_tmppath}/%{name}-root

Provides:      ffmpeg = %{version}-%{release}

BuildRequires: SDL-devel
BuildRequires: a52dec-devel
BuildRequires: bzip2-devel
BuildRequires: faad2-devel
BuildRequires: freetype-devel
BuildRequires: gsm-devel
BuildRequires: imlib2-devel
BuildRequires: lame-devel
BuildRequires: libdc1394-devel, libraw1394-devel
BuildRequires: libstdc++-devel
BuildRequires: libvorbis-devel
BuildRequires: libtheora-devel
BuildRequires: libva-devel
BuildRequires: schroedinger-devel
BuildRequires: speex-devel
BuildRequires: libass-devel
BuildRequires: opus-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: libv4l-devel
BuildRequires: openal-soft-devel
#BuildRequires: soxr-devel
BuildRequires: libvdpau-devel
BuildRequires: libvpx-devel >= 1.3.0
BuildRequires: opencore-amr-devel
BuildRequires: openjpeg-devel
BuildRequires: openssl-devel
#BuildRequires: texi2html
#BuildRequires: vo-aacenc-devel
%{!?_without_x264:BuildRequires: x264-devel}
%{!?_without_x265:BuildRequires: x265-devel}
BuildRequires: xvidcore-devel
BuildRequires: yasm
BuildRequires: zlib-devel
# License incompatible with x264 We mark the package as nonredistributable
# (nodist) if we enable these additonal decoders.
# *Never* make these binaries public!
%{?_with_nodist:
BuildRequires: fdk-aac-devel
BuildRequires: faac-devel
}
Requires:      %{name}-libs = %{version}-%{release}
Requires:       libvpx >= 1.3.0

%package libs
Summary:        Library for ffmpeg
Group:          System Environment/Libraries

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}


%description
FFmpeg is a very fast video and audio converter. It can also grab from a
live audio/video source.
The command line interface is designed to be intuitive, in the sense that
ffmpeg tries to figure out all the parameters, when possible. You have
usually to give only the target bitrate you want. FFmpeg can also convert
from any sample rate to any other, and resize video on the fly with a high
quality polyphase filter.

%description devel
FFmpeg is a complete and free Internet live audio and video broadcasting
solution for Linux/Unix. It also includes a digital VCR. It can encode in real
time in many formats including MPEG1 audio and video, MPEG4, h263, ac3, asf,
avi, real, mjpeg, and flash.
This package contains development files for ffmpeg

%description libs
FFmpeg is a complete and free Internet live audio and video broadcasting
solution for Linux/Unix. It also includes a digital VCR. It can encode in real
time in many formats including MPEG1 audio and video, MPEG4, h263, ac3, asf,
avi, real, mjpeg, and flash.
This package contains the libraries for ffmpeg



%prep
%setup -q -n %{srcname}-%{version}
test -f version.h || echo "#define FFMPEG_VERSION \"%{evr}\"" > version.h

%build
./configure --prefix=%{_prefix} --libdir=%{_libdir} \
            --shlibdir=%{_libdir} --mandir=%{_mandir} \
   --enable-shared \
   --disable-static \
   --enable-runtime-cpudetect \
   --enable-gpl \
   --enable-version3 \
   --enable-postproc \
   --enable-avfilter \
   --enable-pthreads \
   --enable-x11grab \
   --enable-vdpau \
   --disable-avisynth \
   --enable-libdc1394 \
   --enable-libgsm \
   --enable-libmp3lame \
   --enable-libopencore-amrnb \
   --enable-libopencore-amrwb \
   --enable-libopenjpeg \
   --enable-libschroedinger \
   --enable-libspeex \
   --enable-libtheora \
   --enable-bzlib \
   --enable-libass \
   --enable-libdc1394 \
   --enable-libfreetype \
   --enable-openal \
   --enable-libopus \
   --enable-libpulse \
   --enable-libv4l2 \
   --disable-debug \
   --enable-libvorbis \
   --enable-libvpx \
   %{!?_without_x264:--enable-libx264} \
   %{!?_without_x265:--enable-libx265} \
   --enable-libxvid \
%ifarch %ix86
   --extra-cflags="%{optflags}" \
%else
   --extra-cflags="%{optflags} -fPIC" \
%endif
%{?_with_nodist: \
%if 0%{?rhel} <= 6
   --extra-libs="-lstdc++" \
%endif
   --enable-libfdk-aac \
   --enable-nonfree \
   --enable-libfaac \
} \
   --disable-stripping \
   --extra-libs="-lstdc++" \
   --enable-libfdk-aac \
   --enable-nonfree \
   --enable-decklink \
   --extra-cflags=-I%{bmdsdk_path} \
   --extra-ldflags=-L%{bmdsdk_path}

make
# remove some zero-length files, ...
pushd doc
rm -f general.html.d platform.html.d git-howto.html.d \
   developer.html.d texi2pod.pl faq.html.d
popd


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} incdir=%{buildroot}%{_includedir}/ffmpeg
# Remove from the included docs
rm -f doc/Makefile
rm -f %{buildroot}/usr/share/doc/ffmpeg/*.html


%clean
rm -rf %{buildroot}


%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING* CREDITS README* MAINTAINERS LICENSE* RELEASE doc/ RELEASE_NOTES VERSION
%{_bindir}/*
%{_datadir}/ffmpeg
%{_mandir}/man1/*


%files libs
%defattr(-,root,root,-)
%doc COPYING* CREDITS README* MAINTAINERS LICENSE* RELEASE doc/ RELEASE_NOTES VERSION
%{_libdir}/*.so.*
%{_mandir}/man3/*


%files devel
%defattr(-,root,root,-)
%doc COPYING* CREDITS README* MAINTAINERS LICENSE* RELEASE doc/ RELEASE_NOTES VERSION
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so


%changelog
* Wed Apr 13 2016 Vicente Dominguez <twitter:@vicendominguez> - 2.8.6
- FFmpeg-blackmagic 2.8.6 DecLink SDK + libx265 libx264 fdk-aac 3.1

* Tue Dec 20 2015 Vicente Dominguez <twitter:@vicendominguez> - 2.8.4
- FFmpeg 2.8.4 libx265 libx264 fdk-aac 3.1

* Tue Dec 20 2015 Vicente Dominguez <twitter:@vicendominguez> - 2.8.1.2
- FFmpeg 2.8.1-2 libx265 dependencies

* Sun Nov  1 2015 Lars Kiesow <lkiesow@uos.de> - 2.8.1-1
- Update to FFmpeg 2.8.1

* Tue Aug 11 2015 Lars Kiesow <lkiesow@uos.de> - 2.7.2-1
- Update to FFmpeg 2.7.2

* Mon Jun 15 2015 Lars Kiesow <lkiesow@uos.de> - 2.7-1
- Update to FFmpeg 2.7

* Sun Apr  5 2015 Lars Kiesow <lkiesow@uos.de> - 2.6.1-1
- Update to FFmpeg 2.6.1

* Mon Mar  9 2015 Lars Kiesow <lkiesow@uos.de> - 2.6-1
- Update to FFmpeg 2.6

* Mon Feb 23 2015 Lars Kiesow <lkiesow@uos.de> - 2.5.4-1
- Update to FFmpeg 2.5.4

* Wed Jan  7 2015 Lars Kiesow <lkiesow@uos.de> - 2.5.2-1
- Update to FFmpeg 2.5.2

* Tue Dec  9 2014 Lars Kiesow <lkiesow@uos.de> - 2.5-1
- Update to FFmpeg 2.5

* Mon Nov 10 2014 Lars Kiesow <lkiesow@uos.de> - 2.4.3-1
- Update to FFmpeg 2.4.3

* Wed Oct  8 2014 Lars Kiesow <lkiesow@uos.de> - 2.4.2-1
- Update to FFmpeg 2.4.2
- Some condition clean-up

* Fri Sep 26 2014 Lars Kiesow <lkiesow@uos.de> - 2.4.1-1
- Update to FFmpeg 2.4.1
- Removed frei0r dependency for RHEL 6.x
- Removed librtmp dependency for RHEL 6.x

* Mon Aug  4 2014 Lars Kiesow <lkiesow@uos.de> - 2.3.1-1
- Update to FFmpeg 2.3.1

* Wed Jul 16 2014 Lars Kiesow <lkiesow@uos.de> - 2.3-1
- Update to FFmpeg 2.3

* Sat Jun 28 2014 Lars Kiesow <lkiesow@uos.de> - 2.2.4-1
- Update to FFmpeg 2.2.4

* Mon May  5 2014 Lars Kiesow <lkiesow@uos.de> - 2.2.2-1
- Update to FFmpeg 2.2.2

* Sat Apr 12 2014 Lars Kiesow <lkiesow@uos.de> - 2.2.1-1
- Update to FFmpeg 2.2.1

* Fri Feb 28 2014 Lars Kiesow <lkiesow@uos.de> - 2.1.4-2
- Fixed libvpx dependency

* Fri Feb 28 2014 Lars Kiesow <lkiesow@uos.de> - 2.1.4-1
- Update to FFmpeg 2.1.4

* Sun Jan 19 2014 Lars Kiesow <lkiesow@uos.de> - 2.1.3-1
- Update to FFmpeg 2.1.3

* Wed Jan 15 2014 Lars Kiesow <lkiesow@uos.de> - 2.1.2-1
- Update to FFmpeg 2.1.2

* Thu Nov 21 2013 Lars Kiesow <lkiesow@uos.de> - 2.1.1-1
- Update to FFmpeg 2.1.1

* Thu Oct 31 2013 Lars Kiesow <lkiesow@uos.de> - 2.1-1
- Update to FFmpeg 2.1

* Sat Oct 12 2013 Lars Kiesow <lkiesow@uos.de> - 2.0.2-1
- Update to FFmpeg 2.0.2

* Tue Sep 24 2013 Lars Kiesow <lkiesow@uos.de> - 2.0.1-1
- Update to FFmpeg 2.0.1

* Sat Jul 13 2013 Lars Kiesow <lkiesow@uos.de> - 2.0-1
- Update to version 2.0

* Sun May 19 2013 Lars Kiesow <lkiesow@uos.de> - 1.2.1-1
- Update to version 1.2.1

* Mon Apr 29 2013 Lars Kiesow <lkiesow@uos.de> - 1.1.4-3
- Update to version 1.1.4
- Enabled fdk-aacenc

* Sun Apr 28 2013 Lars Kiesow <lkiesow@uos.de> - 1.1.1-2
- Enabled more build opetion
- Updated libvpx

* Mon Jan 28 2013 Lars Kiesow <lkiesow@uos.de> - 1.1.1-1
- Update to ffmpeg 1.1.1

* Thu Aug 23 2012 Lars Kiesow <lkiesow@uos.de> - 0.10-59
- Fixed dependency and added libvorbis on el5

* Fri Aug 17 2012 Lars Kiesow <lkiesow@uos.de> - 0.10-58
- Port to RHEL 5.x (with schroedinger, speex and theora disabled)

* Tue Mar  6 2012 Lars Kiesow <lkiesow@uos.de> - 0.10-57
- Added requirements for manpages

* Tue Mar  6 2012 Lars Kiesow <lkiesow@uos.de> - 0.10-56
- Fixed some packaging issues.

* Thu Feb 16 2012 Lars Kiesow <lkiesow@uos.de> - 0.10-55
- Enabled libvo-aacenc AAC encoder
- Added missing build dependency for librtmp-devel

* Thu Feb 16 2012 Lars Kiesow <lkiesow@uos.de> - 0.10-54
- Fixed issues with CentOS
- Build devel and libs package

* Fri Feb 10 2012 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.10-53
- Update to 0.10.

* Tue Jan  3 2012 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.9-52
- Update to 0.9.

* Tue Jan  3 2012 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.8.9-51
- Update to 0.8.9.

* Sat Nov 26 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.8.7-50
- Update to 0.8.7.

* Sat Nov 12 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.8.6-49
- Update to 0.8.6.

* Fri Sep 23 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.8.4-48
- Update to 0.8.4.

* Mon Jul 25 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.8-47
- Update to 0.8.

* Mon Jul 25 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.7.1-46
- Update to 0.7.1.

* Thu Jun  2 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.6.3-43
- Update to 0.6.3.

* Fri Mar 25 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.6.1-42_git20110322
- Update to latest git master.

* Mon Mar 14 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.6.1-39_git20110314
- Update to latest git master.

* Sat Jan 15 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.6.1-38_git20110115
- Update to latest git master.

* Sun Oct 24 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.6-37_git20101024
- Update to latest git master.

* Thu Jul 22 2010 Paulo Roma <roma@lcg.ufrj.br> - 0.6-35
- Added BR libva-devel.

* Tue Jul 20 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.6-34
- Update to 0.6.

* Sun Apr  4 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.5-32_git20100404
- Update to latest git.

* Fri Nov 20 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.5-31_git20091120
- Update to latest git.

* Sun Jan 18 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.4.9-29_r16671
- Update to latest svn version.

* Sun Nov 16 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.4.9-28_r15845
- ffmpeg-libs from a 3rd party repo generates conflicts.

* Sun Nov  9 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.4.9-27_r15797
- Update to latest svn version.

* Mon Feb 18 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.4.9-26_r12135
- Update to latest svn version.

* Sat Jan 12 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.4.9-25_r11517
- Update to latest svn version.
- libdca nd libogg are not (directly) needed anymore.

* Sat Oct 27 2007 Paulo Roma <roma@lcg.ufrj.br> - 0.4.9-24_r8743
- Compiling with --enable-liba52 for vob->avi using AC3.
- Added --enable-libaad.
- Added libnut-devel as a conditional BuildRequires.
- Using libdc1394-1.2.2, because version 2 does not work.

* Mon Apr 23 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.4.9-23_r8743
- Add some more dependencies (#1172).

* Sun Apr 22 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.4.9-21_r8743
- Add some dependencies on the devel package (#1172).

* Sun Apr 15 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.4.9-20_r8742
- Update to latest svn version.

* Wed Jan  3 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.4.9_19_r7407
- Update to latest svn version.

* Fri Oct 27 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.4.9-18_r6524
- Add faac support.

* Mon Oct  2 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.4.9-17_r6524
- Update to latest svn version.
- Fix revision in release tag.

* Wed Sep  6 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.4.9-15_r19707
- Update to latest svn version.

* Wed Mar  1 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to cvs20060301.
- Fix bug #752.

* Mon Feb 27 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Move compatibility provides to devel package (bug #750).

* Wed Feb 15 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to cvs20060215.

* Sun Jun 12 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to cvs20050612.

* Tue May 17 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to cvs 20050517.

* Mon Apr 18 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to cvs 20050418.

* Tue Nov 23 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.4.9-pre1.

* Thu Oct 16 2003 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.4.8.

* Tue Jul  1 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to a CVS snapshot as videolan-client 0.6.0 needs it.
- Enable faad, imlib2 and SDL support.
- Disable mmx until it doesn't make the build fail anymore :-/

* Mon Mar 31 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt for Red Hat Linux 9.
- Hardcode provides in order to get it right :-/

* Tue Feb 25 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Moved libavcodec.so to the main package to fix dependency problems.

* Wed Feb 19 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Major spec file updates, based on a very nice Mandrake spec.
- Revert to the 0.4.6 release as CVS snapshots don't build.

* Tue Feb  4 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Initial RPM release.

