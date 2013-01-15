#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import urllib,urllib2,cookielib,zlib
from gzip import GzipFile
from StringIO import StringIO
import sys

class HttpWrapperException(Exception): pass
class HttpWrapperResponseData:
    """
    Response data returned by HttpWrapper.Request 
    """
    content = None
    url = None
    headers = None
    #Response http code
    code = None

    def __init__(self,content,url,headers,code):
        self.content = content
        self.url = url
        self.headers
        self.code = code


class HttpWrapper:
  """
  A wrapper of http Request, integrated with cookie handler and smart referer handler

  Usage:
      HttpWrapper('http://xxx.com',data=dict)
  """

  def __init__(self):
    self.opener = urllib2.build_opener(urllib2.HTTPSHandler)
    urllib2.install_opener(self.opener)
    
  def EnableProxyHandler(self,proxyDict):
    """
    enable proxy handler
    params:
        proxyDict:proxy info for connect, eg. {'http':'10.182.45.231:80','https':'10.182.45.231:80'} 
    """
    if proxyDict == None:
        raise HttpWrapperException('you must specify proxyDict when enabled Proxy')
    self.opener.add_handler(urllib2.ProxyHandler(proxyDict))

  def EnableAutoRedirectHandler(self):
    """
    enable auto redirect 301,302... pages
    """
    self.opener.add_handler(urllib2.HTTPRedirectHandler())

  def EnableCookieHandler(self):
    """
    enable cookie, need this after your login
    """
    cj = cookielib.CookieJar()
    self.opener.add_handler(urllib2.HTTPCookieProcessor(cj))

  def EnableConetntEncodingHandler(self):
    """
    enable content encoding when transmite content, support gzip and deflate
    """
    self.opener.add_handler(self.ContentEncodingProcessor())

  class ContentEncodingProcessor(urllib2.BaseHandler):
    """
    A handler to add gzip capabilities to urllib2 requests 
    """
     
    # add headers to requests
    def http_request(self, req):
        req.add_header("Accept-Encoding", "gzip,deflate")
        return req
     
    # decode
    def http_response(self, req, resp):
        old_resp = resp
        # gzip
        if resp.headers.get("content-encoding") == "gzip":
            gz = GzipFile( fileobj = StringIO(resp.read()), mode="r")
            resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)
            resp.msg = old_resp.msg
        # deflate
        if resp.headers.get("content-encoding") == "deflate":
            gz = StringIO(self.deflate(resp.read()) )
            resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)  # 'class to add info() and
            resp.msg = old_resp.msg
        return resp
    
    def deflate(self,data):   # zlib only provides the zlib compress format, not the deflate format;
      try:               # so on top of all there's this workaround:
        return zlib.decompress(data, -zlib.MAX_WBITS)
      except zlib.error:
        return zlib.decompress(data)
    
  def Request(self,url,data=None,headers={}):
    """
    send a request using specified url
    params:
        url     : url you want to send
        data    : additional post data
        headers : headers you want to attach, eg. {'referer' : 'http : //www.baiud.com'}
    """
    #setup request info
    if url is None or url == '':
        raise HttpWrapperException("url can't be empty!")
    if 'user-agent' not in headers:
        headers['user-agent'] = 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16'

    if data is not None:
        req = urllib2.Request(url, urllib.urlencode(data),headers = headers)
    else:
        req = urllib2.Request(url,headers = headers)

    try:
        r = urllib2.urlopen(req)
        resData = HttpWrapperResponseData(r.read(),r.geturl(),r.info().dict,r.getcode())
        r.close()
        return resData
    except urllib2.HTTPError,e:
        return HttpWrapperResponseData(e.fp.read(),'',e.headers,e.code)
        #print e.code
        #print e.msg
        #print e.headers
        #print e.fp.read()
        #print u"error happended:\r\n Location: HttpWrapper.__SendRequest \r\n Error Information:",  sys.exc_info()[1]

if __name__ == '__main__':
    r = HttpWrapper()
    d = r.Request('http://www.baidu.com')
    print d.content.decode('utf-8')
