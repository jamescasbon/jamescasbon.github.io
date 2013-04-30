Title: HTML Templating in Python using the with statement
Date: 2012-01-09 10:20
Category: Python
Tags: python, templates
Slug: html-templating-in-python-using-the-with-stat
Author: James Casbon
Summary: Short version for index and feeds

A few weeks back, I hacked up a simple templating language using
python's 'with' statement:

https://gist.github.com/1585116

It was inspired by coffeekup and haml, since I find it much easier to
code html in those DSLs than with raw HTML (presumably, I need a
better editor to help match tags and indent).  HTML I write these days
tends to be as minimal as possible, and indent based languages help me
see the structure much better, which is a product of too long spent
with python.  See the gist below for the full description.

I posted this to [Hacker
News](https://news.ycombinator.com/item?id=3340369) and it got into
the top ten brieflt, with a few nice comments, a few why bothers and a
lot of prior art.  In particular, jperla's
[weby](http://www.jperla.com/blog/post/weby-templates-are-easier-faster-and-more-flexible)
was very similar with a more involved syntax.  However, this getting
to the top ten shows how easy it is to have 15 seconds of fame these
days.  Next time, to number one.

Anyway, here is the gist:

https://gist.github.com/1461441
