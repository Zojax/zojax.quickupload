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
"""Bulk file upload view

$Id$
"""
from zope.app.component.hooks import getSite
from zope.i18n import translate
from zope.security.interfaces import Unauthorized
from zope.security.proxy import removeSecurityProxy
from zope.traversing.browser import absoluteURL
from zojax.resourcepackage.library import includeInplaceSource
from zope.app.container.interfaces import IContainer, INameChooser
from zope.component import adapts, queryAdapter
from zope.filerepresentation.interfaces import IFileFactory
from zope.app.folder.interfaces import IFolder
from zope.app.file.file import File
from zojax.filefield.data import FileData
from zojax.isodocument.document import ISODocument, ISODocumentNameChooser
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility

class QuickUpload(object):
    adapts(IContainer)
    
    def __call__(self, *args, **kwargs):
        return self.quickuploadAddContent(*args, **kwargs)

    def quickuploadAddContent(self, *args, **kwargs):
        uploadFile = self.request.get('qqfile')
        if uploadFile is None:
            return '{"success": false, "error": "File is None"}'
        title = self.request.get('title')
        name = title
        obj = ISODocument()
        obj.file = FileData(uploadFile)
        obj.docClass = [i for i in getUtility(IVocabularyFactory, 'zojax.isodocument.classes')()][0].value
        obj.versionNumber = 1
        obj.sequenceNumber = 1
        name = ISODocumentNameChooser(self.context, obj).chooseName(name, obj)
        obj.title = name
        self.context[name] = obj
        return '{"success": true}'
