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
""" zojax.quickupload tests

$Id$
"""
__docformat__ = "reStructuredText"

import unittest

import zope.testing
import zope.component

def setUp(test):
    """This method is used to set up the test environment. We pass it to the
    DocFileSuite initialiser. We also pass a tear-down, but in this case,
    we use the tear-down from zope.component.testing, which takes care of
    cleaning up Component Architecture registrations.
    """

def test_suite():
    return unittest.TestSuite((

        # Here, we tell the test runner to execute the tests in the given
        # file. The setUp and tearDown methods employed make use of the Zope 3
        # Component Architecture, but really there is nothing Zope-specific
        # about this. If you want to test "plain-Python" this way, the setup
        # is the same.

        zope.testing.doctest.DocFileSuite('README.rst',
                     package='zojax.quickupload',
                     setUp=setUp,
                     tearDown=zope.component.testing.tearDown),
        ))
