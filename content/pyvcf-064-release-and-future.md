Title: PyVCF 0.6.4 Release: Considering the future
Date: 2013-07-15 12:00
Category: Python
Tags: python, biology, VCF
Slug: pyvcf-064-release-considering the future
Author: James Casbon
Summary: New release and where do we go

I just pushed the PyVCF 0.6.4 release to
[github](https://github.com/jamescasbon/PyVCF) and [pypi](https://pypi.python.org/pypi/PyVCF/0.6.4).
It's mainly a bugfix release, but I'm pleased that so many people are
contributing code and thank everyone for there commits, especially Martijn who
is normally super fast to respond.

I want to take the opportunity to ask users of PyVCF about a few questions about
the future.  These relate to the future of the project and how the project is
supported.

Firstly, with regard to the project itself.  I think PyVCF has been a relative
success and I'm happy that I took it over from  jdoughertyii and made it into something
useful for the community.   However, I'm not currently working day to day with
sequence data, and so cannot really pay full attention to developments in the
field.  Nevertheless, I am aware that many power users move away from PyVCF when
they need to do large scale analysis to something more optimized to a particular
use.  PyVCF has fit the role of a relatively compliant and liberal parser.  If
you know your data fits a certain form, you can normally optmize the parser and
get better performance.  Nevertheless, there are certain improvements we could
undertake if we wanted a better parser: 

 * Optimize the INFO parsing code (which can be the slowest part for small number
  of sample VCFs)
 *  Return numpy arrays for call data, which would flow into downstreamm large
  scale analysis with less friction
 * Target BCF file formats

So I want to know if these are targets users need, or are the power users
already looking elsewhere?  Is anyone willing to step up and contribute, e.g., a
cythonized INFO parser.  Is there a better parser that people are switching to
and I should just give up?

Secondly, I want to find out about the best way to help PyVCF users get help.  I
get quite a few requests for help from people trying to analyze their data or
who have a small fix to contribute.  I am often pretty derelict at responding as
these people are sometimes very new to coding.  Github is not the most welcoming
of place for people at this level.  What would be better: a mailing list?
Trying to find a project to host (e.g. BioPython)?  A users mailing  list might
well be too low traffic to really work.

If you have any opinions on these matters, please get in touch.  Leave a comment
here, email me or tweet me.  I'd love to hear from you.

Also one final plea:  as I don't get to deal with sequence data these days, I'd
really like to hear any stories of PyVCF in the wild, if you can share them.  Knowing
that it is helping people with real biological problems would be a great
motivator!

 
