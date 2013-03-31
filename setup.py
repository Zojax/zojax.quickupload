##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Setup for zojax.quickupload package

$Id$
"""
import sys, os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.0.0'


setup(name='zojax.quickupload',
      version=version,
      description="Extensible TALES fomratter expression.",
      long_description=(
          'Detailed Dcoumentation\n' +
          '======================\n'
          + '\n\n' +
          read('README.rst')
          + '\n\n' +
          read('CHANGES.txt')
          ),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3'],
      author='Bogdan Girman',
      author_email='bogdan.girman@gmail.com',
      url='http://zojax.net/',
      license='ZPL 2.1',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['zojax'],
      install_requires = ['setuptools',
                          'pytz',
                          'zope.component',
                          'zope.interface',
                          'zope.app.container',
                          'zope.publisher',
                          'zope.schema',
                          'zope.proxy',
                          'zope.tales',
                          'zope.i18n',
                          'zope.i18nmessageid',
                          'zope.app.appsetup',
                          'zope.app.zapi',
                          'zope.app.pagetemplate',
                          'zope.app.publisher',
                          'zope.app.folder',
                          'z3c.pt',
                          'collective.monkeypatcher',
                          'zojax.layoutform',
                          'zojax.portlet',
                          'z3c.jsonrpc',
                          ],
      extras_require = dict(test=['zojax.portlet [test]',
                                  'zope.testing',
                                  'zope.app.zcmlfiles',]),
      include_package_data = True,
      zip_safe = False
      )
