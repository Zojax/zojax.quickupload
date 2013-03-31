zojax.quickupload
=================

    >>> from zope import component, interface
    >>> from zope.testbrowser.testing import Browser
    >>> from zojax.extensions.interfaces import IExtensible
    >>> from zope.app.testing.functional import getRootFolder
    >>> from zojax.quickupload.tests.tests import TestContent

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
    ...<div class="portlet-quickupload-wrapper">...
    </html>

Check Resources

    >>> manager.open("http://localhost/@@/fineuploader/jquery.fineuploader-3.3.1.min.js")
    >>> manager.contents !=''
    True
    >>> manager.open("http://localhost/@@/fineuploader/fineuploader-3.3.1.css")
    >>> manager.contents !=''
    True
    >>> manager.open("http://localhost/@@/fineuploader/jquery.fineuploader-3.3.1.js")
    >>> manager.contents !=''
    True
    >>> manager.open("http://localhost/@@/fineuploader/jquery.fineuploader-3.3.1.min.js")
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
    
Upload apload as user

    >>> containerUrl = "http://localhost/"
    >>> user.post(containerUrl, "{'method':'quickuploadAddContent', 'params':{'data':'data', 'title':'Test Title', 'file': 'File'}}", content_type='application/json')
    Traceback (most recent call last):
    ...
    Unauthorized: (<z3c.jsonrpc.zcml.QuickUpload object at ...>, '__call__', 'zojax.ModifyContent')

Upload apload as manage

    >>> manager.post(containerUrl, "{'method':'quickuploadAddContent', 'params':{'data':'data', 'title':'Test Title', 'file': 'File'}}", content_type='application/json')
    >>> 'Test Title' in root.keys()
    True
