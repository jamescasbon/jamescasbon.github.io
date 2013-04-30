Title: A Comparison of openelec.tv, yavdr, mythtv and a sony bravia
Date: 2012-02-16 10:20
Category: PVR
Tags: mythtv, pvr
Slug: a-comparison-of-openelectv-yavdr-mythtv-and-a
Author: James Casbon
Summary: Short version for index and feeds

I recently had all my electronic goods stolen.  One of the pieces that went was
my [MythTV](1) box, a little mini PC that recorded TV and played youtube, etc.
Fortunately, I was insured so I received a new TV and empty box.  Things have
changed a lot since I first starting using MythTV over [nine years ago](http://www.mythtv.org/pipermail/mythtv-users/2003-November/019043.html) so 
I thought it would be a good opportunity to try out some of the other
contenders for homebrew PVRs.  In my list were: 

 * [openelec.tv](2), an extremely minimal XBMC frontend with a TVHeadend backend
 * [yaVDR](3): an ubuntu based VDR setup with VDR or XBMC frontends
 * Sony Bravia TV.  You could plug a HD into the replacement TV I got, it also
   supported internet video from lovefilm, etc

I will first run down my experience with each...

Sony Bravia TV
--------------

The TV has the option to use an external HDD to record via USB.  It also
supports DLNA (more later) and has some internet TV apps (BBC iplayer,
LoveFilm).  Upon unboxing, I was surprised to receive a copy of the GPL.  It
seems some Bravias are running Linux.

The setup with the HDD was pure Sony crap.  The HDD needed to be initialized to work
with the TV.  This initialization was designed to make the disk unreadable
anywhere else and to ensure nothing recorded elsewhere could be played back via
USB (despite the fact it supports DLNA to access network shares).

Setting up a recording involved navigating to the show in the guide and hitting
record, or setting a manual timer.  There are no search options or series
records.  No management of expiry on the disk.  No watching of things being
broadcast on the same multiplex.  All in all, this resembled an 80's video
recorder for all the features it had:  basically unusable.

The internet videos are OK.  Iplayer and lovefilm work well, but the interfaces
are pretty slow.  There is a scroll effect in iplayer that takes ages.  But the
interesting thing, for me, is that here we have LoveFilm working on a linux box
despite the fact that it now requires Silverlight.  The only reasonable
conclusions are that Sony has a Silverlight implementation on linux or that they
have negotiated a position to allow non silverlight streaming to their device.
Vertical market/DRM integration, FTW!  

openelec.tv
-----------

This is a super minimal install of XBMC's pvr branch backed by TVHeadend.
Installation was easy, boots are super fast.  TVHeadend is configured via its
web interface and is easy to set up.  After install, the box sits with SAMBA and
other file sharing set up, so you can copy content straight on or off the box.

TVHeadend, although easy to set up, is still lacking a lot in terms of the finer
points of scheduling.  It's duplication detection just doesn't really work
expecially in terms of channels with many repeats and +1 versions.  If they fix
these, this will be a killer set up.  But as it was, I just couldn't live with
it.  It needed too much management to do a series record.

It also is worth noting that you cannot change anything about the openelec
install, even the ssh password.  Doing so requires that you recompile the image
which you might find a pain.  This means you can't use many things that you
would be used to on a linux install (gcc, perl, python, wget, rsync, etc).
However, that is what keeps it lightweight and robust.

yaVDR
-----

yaVDR is a ubuntu setup with VDR installed.  It claims to be minimal, but
actually installs a whole bunch of crap.  VDR is the other big linux PVR project
to MythTV, but it has typically helped that you speak German if you want to read
the documentation.

The yaVDR install is pretty much the normal ubuntu one, and startup is similar
to a normal ubuntu box. yaVDR has a custom web front end for configuring yaVDR
and you can drop into the VDR frontend to control the PVR.  I found that the 
XBMC-pvr branch they were using was too unreliable to use and
so I was using the VDR frontend.  This was a little tricky as it is designed
around a remote (which I didn't have).

My experience with VDR was almost as frustrating as with TVHeadend.  You can
have automated recordings, but for channels with +1s and repeats and different
episodes it never seemed to get things correct.  VDR is based around plugins so
it may have been that I could have found something to rectify that, but I never
could get a satisfactory set up.


Aside: XBMC-pvr, uPNP, DLNA
---------------------------

While I was trying these setups, I was also testing out whether they could
stream direct to the Bravia TV which supports DLNA.  This is a subset of
uPNP with certain codecs.  TVHeadend did not support DLNA and neither did VDR.
However, there was a plugin for VDR that supports uPNP.  However, I could not
get this to work with streaming DVB broadcasts to the Sony TV.  

I had higher hopes for XBMC.  It has a reasonable uPNP server, but you soon find
the problems (including unsorted albums: http://forum.xbmc.org/showthread.php?t=105141) 
but more troublesome is the fact that the TV shows in XBMC are not served via
uPNP at all.  

Back to Myth
------------

After all this, I installed a linux distribution and put Myth on top.  The Myth
setup was pretty painless (channel scan even worked), but partly this is because 
I know all the problems too well.

The worst thing about Myth is that the frontend is pretty awful.  I did try to
go the XBMC-pvr route, but the integration is very alpha quality.  However, I
was pleased to find that this didn't matter.  The uPNP server from myth is
awesome, everything is listed in various categories (date, title, etc) and
playback is fine.

Add in MythWeb and I think you have a perfect PVR.  Mythweb is good for
searching, scheduling and the flash based streaming is great.

Conclusions
-----------

So TL;DR: MythTV is awesome with a DLNA television.  Openelec.tv will be awesome
when TVHeadend's scheduling is better.

Also: there's nothing on TV so save your money and buy a book.


 [1]: http://www.mythtv.org/
 [2]: http://openelec.tv/
 [3]: http://www.yavdr.org/
