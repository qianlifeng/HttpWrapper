HttpWrapper Intro
===========

A wrapper of http Request, integrated with cookie handler and content encoding handler(gzip).  
All instance of HttpWrapper are designed to be signal, that means if you set proxy in first HttpWrapper,it will not affect the second HttpWrapper instance, of course urllib2.urlopen neither.

**Usage**:  
first you must init a HttpWrapper instance like this:  
`h = HttpWrapper()`  
after that, you can fetch everything you want  
`res = h.Request(url)`  
or:  
`res = h.Request(url,data = dict,headers = dict)`
        
If you just want **request header of the url**,use:  
`h.RequestHeader(url)`
  
**Enable Proxy:**  
`h.EnableProxyHandler({'http':'ip:80','https':'ip:80'})`  
**Disable Proxy:**    
`h.DisableProxyHandler()`

sometims, maybe we don't want **auto redirect**(By default, AutoRedirect is enabled),use:  
`h.DisableAutoRedirectHandler()`
