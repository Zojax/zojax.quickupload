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
from zojax.contenttype.file.file import File
from zojax.contenttype.file.factory import FileFactory
from zojax.filefield.data import FileData
from zojax.isodocument.document import ISODocument, ISODocumentNameChooser, ISODocumentContentType
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from zojax.catalog.interfaces import ICatalog
import re

class QuickUpload(object):
    adapts(IContainer)
    
    def __call__(self, *args, **kwargs):
        return self.quickuploadAddContent(*args, **kwargs)

    def quickuploadAddContent(self, *args, **kwargs):
        uploadFile = self.request.get('qqfile')
        if uploadFile is None:
            return '{"success": false, "error": "File is None"}'
        title = self.request.get('title') or uploadFile.filename
        description = self.request.get('description')
        factory = FileFactory(self.context)
        obj = factory(uploadFile.filename, uploadFile.headers['content-type'], uploadFile)
        name = obj.title
        shortname = self.request.get('shortname') or re.sub(r'(\W)\1*',r'-',re.sub(r'(\W)\1*',r'-', obj.title))
        obj.title = title
        obj.data = FileData(uploadFile)
        obj.shortname = shortname 
        obj.description = description or ''
        name = INameChooser(self.context, obj).chooseName(name, obj)
        self.context[name] = obj
        return '{"success": true}'

class QuickUploadISODocument(object):
    adapts(IContainer)
    
    def __call__(self, *args, **kwargs):
        return self.quickuploadAddContent(*args, **kwargs)

    def quickuploadAddContent(self, *args, **kwargs):
        uploadFile = self.request.get('qqfile')
        if uploadFile is None:
            return '{"success": false, "error": "File is None"}'
        title = self.request.get('title')
        shortname = self.request.get('shortname')
        description = self.request.get('description')
        docClass = self.request.get('docClass')
        name = title
        obj = ISODocument()
        obj.file = FileData(uploadFile)
        obj.docClass = docClass or [i for i in getUtility(IVocabularyFactory, 'zojax.isodocument.classes')()][0].value
        catalog = getUtility(ICatalog)
        num = len(catalog.apply({'isoDocClass': {'any_of': (obj.docClass, )}})) + 1
        while catalog.apply({'isoDocClass': {'any_of': (obj.docClass, )},
                             'isoDocSeqNumber': {'any_of': (num, )}}):
            num += 1
        obj.versionNumber = 1
        obj.sequenceNumber = num
        name = ISODocumentNameChooser(self.context, obj).chooseName(name, obj)
        obj.title = name
        self.context[name] = obj
        return '{"success": true}'
