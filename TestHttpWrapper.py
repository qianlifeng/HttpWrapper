#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from HttpWrapper import HttpWrapper
from nose.tools import assert_raises
import os,urllib2

h = HttpWrapper()

def setUp():
    #proxy info
    #self.h.EnableProxyHandler({'http':'10.182.45.231:80','https':'10.182.45.231:80'})
    #auto direct 301,302... page
    #h.EnableAutoRedirectHandler()
    #save cookie info between requests
    #h.EnableCookieHandler()
    #enable gzip and deflate encoding, which will reduce transmite time
    #h.EnableConetntEncodingHandler()

    #r = h.Request('image url')

    #h.RequestAsyc('http://www.baidu.com',data = {},header = {},callback = funcname )
    #h.RequestAsyc('http://www.sina.com.cn',callback = funcname )


    #h1 = HttpWrapper()
    #h1的设定应该不和h混淆
    pass


def Test_ProxyHandler_NoProxyHandler():
    if 'HTTP_PROXY' in os.environ:
        #exist proxy setting
        r = HttpWrapper()
        r.DisableProxyHandler()
        with assert_raises(urllib2.URLError):
            r.Request('http://www.baidu.com')
    else:
        print 'no proxy detected,skip proxy test...'

def Test_Request():
    r = h.Request('http://www.cnblogs.com')
    assert r.code == 200

def Test_Request_PageNotFind():
    r = h.Request('http://www.cnblogs.com/scottqiantest')
    assert r.code == 404
def Test_Request_PostData():
    data = {'tbUserName'        : '1',
            'tbPassword'        : '1',
            '__EVENTTARGET'     : 'btnLogin',
            '__EVENTARGUMENT'   : '',
            '__VIEWSTATE'       : '/wEPDwULLTE1MzYzODg2NzZkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBQtjaGtSZW1lbWJlcm1QYDyKKI9af4b67Mzq2xFaL9Bt',
            '__EVENTVALIDATION' : '/wEWBQLWwpqPDQLyj/OQAgK3jsrkBALR55GJDgKC3IeGDE1m7t2mGlasoP1Hd9hLaFoI2G05'}
    r = h.Request('http://passport.cnblogs.com/login.aspx',data)
    assert r.content.decode('utf-8').find(u'用户不存在') > 0

def Test_Request_RefererHeader():
    #tell server I'm from baidu.com
    headers = {'referer':'http://www.baidu.com'}
    r = h.Request('http://www.stardrifter.org/cgi-bin/ref.cgi',headers=headers)
    assert r.code == 200
    assert r.content.find(u'www.baidu.com') > 0

def Test_Request_AutoRedirect():
    h.DisableAutoRedirectHandler()
    h.EnableAutoRedirectHandler()
    #auto redirect is enabled by default in HttpWrapper
    r = h.Request('http://jigsaw.w3.org/HTTP/300/301.html')
    assert r.url == 'http://jigsaw.w3.org/HTTP/300/Overview.html'

    r = h.Request('http://jigsaw.w3.org/HTTP/300/302.html')
    assert r.url == 'http://jigsaw.w3.org/HTTP/300/Overview.html'

def Test_Request_RemoveAutoRedirectHandler():
    h.DisableAutoRedirectHandler()
    r = h.Request('http://jigsaw.w3.org/HTTP/300/302.html')
    assert r.url != 'http://jigsaw.w3.org/HTTP/300/Overview.html'

def Test_Request_RequestHead():
    res = h.RequestHeader('http://www.baidu.com')
    assert res.code == 200
    assert res.content == ''

def Test_DownloadImageFile():
    r = h.Request('http://www.google.com/images/logo.png')
    assert r.content is not None and len(r.content) > 0
