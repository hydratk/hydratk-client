# -*- coding: utf-8 -*-
"""HTTP client

.. module:: client.core.httpclient
   :platform: Windows, Unix
   :synopsis: HTTP client
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

import requests
from requests.exceptions import RequestException
from requests.packages.urllib3 import disable_warnings
from requests.auth import HTTPBasicAuth, HTTPDigestAuth

mime_types = {
    'file' : 'multipart/form-data',
    'form' : 'application/x-www-form-urlencoded',
    'html' : 'text/html',
    'json' : 'application/json',
    'text' : 'text/plain',
    'xml'  : 'application/xml'
}

class HTTPClient(object):
    """Class HTTPClient
    """
    
    _url = None
    _proxies = None
    _cert = None
    _req_header = None
    _req_body = None
    _res_status = None
    _res_header = None
    _res_body = None
    _cookies = None

    def __init__(self):
        """Class constructor

        Called when object is initialized

        Args:
           none
           
        """

        disable_warnings()

    @property
    def url(self):
        """ URL property getter """

        return self._url

    @property
    def proxies(self):
        """ proxies property getter """

        return self._proxies

    @property
    def cert(self):
        """ cert property getter """

        return self._cert

    @property
    def req_header(self):
        """ request header property getter """

        return self._req_header

    @property
    def req_body(self):
        """ request body property getter """

        return self._req_body

    @property
    def res_status(self):
        """ response status code property getter """

        return self._res_status

    @property
    def res_header(self):
        """ response header property getter """

        return self._res_header

    @property
    def res_body(self):
        """ response body property getter """

        return self._res_body

    @property
    def cookies(self):
        """ cookies property getter """

        return self._cookies

    def send_request(self, url, proxies=None, user=None, passw=None, auth='Basic', cert=None, verify_cert=True, method='GET', headers=None,
                     cookies=None, body=None, params=None, content_type=None, timeout=10):
        """Method sends request to server

        Args:
           url (str): URL
           proxies (dict): HTTP proxies {http: url, https: url}
           user (str): username
           passw (str): password
           auth (str): authentication type Basic|Digest
           cert (obj): str (path to cert.perm path), tuple (path to cert.pem path, path to key.pem path)
           verify_cert (bool): verify certificate
           method (str): HTTP method GET|POST|PUT|DELETE|HEAD|OPTIONS
           headers (dict): HTTP headers
           cookies (dict): cookies (name:value)
           body (str): request body, POST method used by default
           params (dict): parameters, sent in URL for GET method, in body for POST|PUT|DELETE method
           content_type (str): type of content, file|form|html|json|text|xml
           timeout (int): timeout

        Returns:
           tuple: status (int), body (str)

        """

        try:

            if (user != None):
                if (auth == 'Basic'):
                    auth = HTTPBasicAuth(user, passw)
                elif (auth == 'Digest'):
                    auth = HTTPDigestAuth(user, passw)
                else:
                    auth = HTTPBasicAuth(user, passw)
            else:
                auth = None

            self._url = url
            self._proxies = proxies
            self._cert = cert
            self._req_header = headers
            self._req_body = body
            verify = True if (cert != None and verify_cert) else False

            method = method.lower() if (method.lower() in ['get', 'post', 'put', 'delete', 'head', 'options']) else 'get'
            if (params != None and method in ('post', 'put', 'delete')):
                content_type = 'form'
            if (content_type != None and content_type in mime_types):
                if (headers == None):
                    headers = {}
                headers['Content-Type'] = mime_types[content_type]

            res = None
            res = getattr(requests, method)(self._url, proxies=proxies, auth=auth, cert=cert, params=params, data=body, headers=headers,
                                            cookies=cookies, timeout=timeout, verify=verify)
            self._res_status, self._res_header, body, self._cookies = res.status_code, res.headers, res.text, res.cookies

            if (body.__class__.__name__ == 'bytes'):
                body = body.decode('latin-1')
            self._res_body = body

            return (self._res_status, self._res_body)

        except RequestException as ex:
            if (str(ex) == 'WWW-Authenticate'):
                return (401, None)
            status = res.status_code if (res != None) else None
            body = res.text if (res != None) else None
            return status, body

    def get_header(self, title):
        """Method gets response header

        Args:
           title (str): header title

        Returns:
           str: header

        """

        title = title.lower()
        if (title in self._res_header):
            return self._res_header[title]
        else:
            return None
