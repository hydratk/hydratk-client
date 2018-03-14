.. _module_ext_client_core_httpclient:

httpclient
==========

This sections contains module documentation of httpclient module.

HTTPClient
^^^^^^^^^^

Class for HTTP client with usage of external module `requests <http://docs.python-requests.org/en/master/>`_ in version >= 2.11.1.

**Attributes** :

* _url - URL
* _proxies - HTTP proxies configuration
* _cert - path to certificate file
* _req_header - request headers
* _req_body - request body
* _res_status - response status
* _res_header - response headers
* _res_body - response body
* _cookies - cookies

**Properties (Getters)** :

* url - _returns url
* proxies - _returns _proxies
* cert - returns _cert
* req_header - returns _req_header
* req_body - returns _req_body
* res_status - returns _req_status
* res_headers - returns _res_headers
* res_body - returns _res_body
* cookies - returns _cookies

**Methods** :

* __init__ 

Constructor.

* get_header

Method returns given response HTTP header.
     
* send_request

Method send request to server. 

url should start with http:// or https://. proxies is dictionary configuration of HTTP proxies (see requests documentation). auth is authentication type 
(supported types: Basic, Digest). method is HTTP method (supported methods: GET, POST, PUT, DELETE, HEAD, OPTIONS). headers is dictionary of
request HTTP headers. cookies is dictionary (cookie name and value). 

params is dictionary (parameters name and value), they are sent as part of URL for GET methods otherwise in body. content_type is user friendly mime type translated to valid HTTP
Content-Type header. Request timeout is 10s by default (parameter timeout).

Supported mime types:
file -> multipart/form-data            
form -> application/x-www-form-urlencoded
html -> text/html  
json -> application/json  
text -> text/plain
xml -> application/xml