Title: PyVCF 0.6 Release: Cython and Performance
Date: 2012-06-03 10:20
Category: Python
Tags: python, biology
Slug: pyvcf-06-release-cython-and-performance
Author: James Casbon
Summary: Short version for index and feeds

<p>I just uploaded the <a href="https://crate.io/packages/PyVCF/">PyVCF 0.6 release</a> to pypi. &nbsp;This release concentrated on performance and will use a cythonized inner loop if you install it with cython. &nbsp;There is a small backwards incompatible change, which is that the call data (the cells in a VCF file) are now stored as a namedtuple.</p>
<p>A simple performance benchmark parsing a 1kg file:&nbsp;</p>
<ul>
<li>pyvcf: 1.8s / 100%</li>
<li>cyvcf: 2.3s / 127%</li>
<li>vcftools: 2.9s / 161%</li>
</ul>
