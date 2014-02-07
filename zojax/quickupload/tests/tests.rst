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
    >>> manager.open("http://localhost/content/index.html")
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
    >>> 'testfile.pdf' in root.keys()
    True

1. shortname set via the portlet is not applied to the file. To understand how it should work you can use Add file link from Actions portlet. For example, you upload a file named 'Test word document.doc' to http://staging.quickoasis.com/corporate/exec/documents/'. If user has set shortname name in corresponding field, then url for the uploaded file should look like http://staging.quickoasis.com/corporate/exec/documents/shortnamesetbyuser.doc It's important here to check that file extension is added to the end of the shorname.

    >>> filename = 'Test word document.doc'
    >>> testfile = file(os.path.join(os.path.split(__file__)[0],filename))
    >>> qqfile = (('qqfile', filename, testfile.read()),)
    >>> qqfields = (
    ...             ('shortname', 'short name set by user'),
    ...             )
    >>> encoded_multipart = encode_multipart_formdata(qqfields, qqfile)
    >>> manager.post(
    ...             containerUrl,
    ...             encoded_multipart[1],
    ...             encoded_multipart[0],
    ...             )
    >>> print root['shortnamesetbyuser.doc']
    <... object at ...>

In case user hasn't set a custom shortname, it should be generated from uploaded filename, but without spaces, special chars, etc. In our case it should look like http://staging.quickoasis.com/corporate/exec/documents/testworddocument.doc
In any case, short name shouldn't contain spaces, special chars etc. The should be excluded from shorname field value set by user.

    >>> qqfields = ()
    >>> encoded_multipart = encode_multipart_formdata(qqfields, qqfile)
    >>> manager.post(
    ...             containerUrl,
    ...             encoded_multipart[1],
    ...             encoded_multipart[0],
    ...             )
    >>> print root['testworddocument.doc']
    <... object at ...>

2. Uploaded filename shouldn't contain spaces and special chars too. They should be excluded before upload. See Test word document.docx in http://staging.quickoasis.com/corporate/exec/documents/ for how it shouldn't be.

    >>> filename = 'Test word-.-.-:\'],document.doc'
    >>> testfile = file(os.path.join(os.path.split(__file__)[0],filename))
    >>> qqfile = (('qqfile', filename, testfile.read()),)
    >>> qqfields = ()
    >>> encoded_multipart = encode_multipart_formdata(qqfields, qqfile)
    >>> manager.post(
    ...             containerUrl,
    ...             encoded_multipart[1],
    ...             encoded_multipart[0],
    ...             )
    >>> print root['testworddocument-2.doc']
    <... object at ...>

3. A bit of ui improvement - let's add cursor:pointer style when user hover a filename in the portlet, so it would be more obvious that it's expanable.
4. I would also collapse the form with custom fields under file name after Upload now button is pressed, but it's not a must. 
