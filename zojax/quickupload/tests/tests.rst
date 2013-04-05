zojax.quickupload
=================

    >>> from zope import component, interface
    >>> from zope.testbrowser.testing import Browser
    >>> from zojax.extensions.interfaces import IExtensible
    >>> from zope.app.testing.functional import getRootFolder
    >>> from zojax.quickupload.tests.tests import TestContent, encode_multipart_formdata

    >>> root = getRootFolder()
    >>> interface.alsoProvides(root, IExtensible)

    >>> content = TestContent(title=u'Test content')
    >>> content.text = u'Test content body text.'
    >>> root['content'] = content
    >>> content2 = TestContent(title=u'Test content 2')
    >>> content2.text = u'Test content 2 body text.'
    >>> root['content']['content2'] = content2
    >>> user = Browser()
    >>> user.handleErrors = False
    >>> user.addHeader("Authorization", "Basic user:userpw")
    >>> manager = Browser()
    >>> manager.handleErrors = False
    >>> manager.addHeader("Authorization", "Basic mgr:mgrpw")

change portlet settings

    >>> manager.open("http://localhost/content/++extensions++/")
    >>> manager.getLink('Portlets').click()

set portlets manager

    >>> manager.getLink('Left column portlets').click()
    >>> manager.open('http://localhost/content/++extensions++/portlets/columns.left/?form.widgets.portletIds:list=portlet.quickupload&form.buttons.save=Save&form.widgets.status=1')

setup portlet

    >>> manager.open('http://localhost/content/++extensions++/portlets/columns.left/')
    >>> manager.getLink('Quick Upload').click()
    >>> manager.open('http://localhost/content/++extensions++/portlets/columns.left/portlet.quickupload/?form.widgets.portletIds:list=portlet.quickupload&form.widgets.propagate:list=true&form.buttons.save=Save&form.widgets.status=1')
    >>> manager.url
    'http://localhost/content/++extensions++/portlets/columns.left/portlet.quickupload/index.html'

check portlet

    >>> manager.open("http://localhost/content/portlets/columns.left/portlet.quickupload/check")
    >>> print manager.contents
    Ok
    >>> manager.open("http://localhost/content/context.html")
    >>> print manager.contents
    <html>
    ...<h2 class="z-portlet-header">Quick Upload</h2>...
    </html>

Check Resources

    >>> manager.open("http://localhost/@@/fineuploader/fineuploader-3.3.1.min.js")
    >>> manager.contents !=''
    True
    >>> manager.open("http://localhost/@@/fineuploader/fineuploader-3.3.1.css")
    >>> manager.contents !=''
    True
    >>> manager.open("http://localhost/@@/fineuploader/fineuploader-3.3.1.js")
    >>> manager.contents !=''
    True
    >>> manager.open("http://localhost/@@/fineuploader/fineuploader-3.3.1.min.js")
    >>> manager.contents !=''
    True
    >>> manager.open("http://localhost/@@/fineuploader/iframe.xss.response-3.3.1.js")
    >>> manager.contents !=''
    True
    >>> manager.open("http://localhost/@@/fineuploader/loading.gif")
    >>> manager.contents !=''
    True
    >>> manager.open("http://localhost/@@/fineuploader/processing.gif")
    >>> manager.contents !=''
    True
    

    >>> containerUrl = "http://localhost/quickuploadAddContent"
    >>> import os
    >>> filename = 'testFile.pdf'
    >>> testfile = file(os.path.join(os.path.split(__file__)[0],filename))
    >>> qqfile = (('qqfile', filename, testfile.read()),)
    >>> qqfields = (
    ...             ('title', filename),
    ...             ('shortname', filename.split('.')[0]),
    ...             ('description', 'Test Description'),
    ...             )
    >>> encoded_multipart = encode_multipart_formdata(qqfields, qqfile)

Upload upload as user

    >>> user.post(
    ...             containerUrl,
    ...             encoded_multipart[1],
    ...             encoded_multipart[0],
    ...             )
    Traceback (most recent call last):
    ...
    Unauthorized: (...)

Upload upload as manage

    >>> manager.post(
    ...             containerUrl,
    ...             encoded_multipart[1],
    ...             encoded_multipart[0],
    ...             )
    >>> 'testFile.pdf' in root.keys()
    True

Test fields:

    >>> qqfields = (
    ...             ('title', 'test title'),
    ...             ('shortname', 'test short name'),
    ...             ('description', 'Test Description\n new line'),
    ...             )
    >>> encoded_multipart = encode_multipart_formdata(qqfields, qqfile)
    >>> manager.post(
    ...             containerUrl,
    ...             encoded_multipart[1],
    ...             encoded_multipart[0],
    ...             )
    >>> root['testFile-2.pdf'].title = qqfields[0][1]
    >>> root['testFile-2.pdf'].shortname = qqfields[1][1]
    >>> root['testFile-2.pdf'].description = qqfields[2][1]
