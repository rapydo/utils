# -*- coding: utf-8 -*-

"""
### HTTP status codes ===
http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html

Should take a look here also:
http://www.restapitutorial.com/httpstatuscodes.html
http://racksburg.com/choosing-an-http-status-code/

"""

# RESPONSE TO BE VERIFIED
HTTP_CONTINUE = 100
HTTP_SWITCHING_PROTOCOLS = 101

# RESPONSE RECEIVED
HTTP_OK_BASIC = 200
HTTP_OK_CREATED = 201
HTTP_OK_ACCEPTED = 202
HTTP_OK_NORESPONSE = 204
HTTP_PARTIAL_CONTENT = 206

# THE THRESHOLD BETWEEN GOOD AND BAD
HTTP_PARTIAL_CONTENT = 206

HTTP_TRESHOLD = 299

# WARNINGS
HTTP_MULTIPLE_CHOICES = 300
HTTP_FOUND = 302
HTTP_NOT_MODIFIED = 304
HTTP_TEMPORARY_REDIRECT = 307

# SOFTWARE ERROR
HTTP_BAD_REQUEST = 400
HTTP_BAD_UNAUTHORIZED = 401
HTTP_BAD_FORBIDDEN = 403
HTTP_BAD_NOTFOUND = 404
HTTP_BAD_METHOD_NOT_ALLOWED = 405
HTTP_BAD_CONFLICT = 409
HTTP_BAD_RESOURCE = 410

# SERVER ERROR
HTTP_SERVER_ERROR = 500
HTTP_NOT_IMPLEMENTED = 501
HTTP_SERVICE_UNAVAILABLE = 503
HTTP_INTERNAL_TIMEOUT = 504