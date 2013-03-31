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
"""

$Id$
"""
from rwproperty import setproperty, getproperty

from zope.component import getMultiAdapter

from zojax.portlet.manager import PortletManagerBase
from zojax.portlet.portlet import PortletBase
from zojax.portlet.interfaces import IPortlet
from zojax.portlet.browser.portlet import PortletPublicAbsoluteURL
from zojax.layout.interfaces import ILayout

from interfaces import IQuickUploadPortlet
from zojax.resourcepackage.library import includeInplaceSource

class QuickUploadPortlet(object):
    """ quick upload portlet """

    def __init__(self, context, request, manager, view):
        super(QuickUploadPortlet, self).__init__(context, request, manager, view)

    def isAvailable(self):
        return True

    def render(self):
        return super(QuickUploadPortlet, self).render()

