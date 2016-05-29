import base64
from django.utils.encoding import smart_text, DjangoUnicodeDecodeError
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

def basic_auth(http_request):

    if 'HTTP_AUTHORIZATION' in http_request.META:
        authdata = http_request.META['HTTP_AUTHORIZATION'].split()
        if len(authdata) == 2 and authdata[0].lower() == "basic":
            try:
                raw = authdata[1].encode('ascii')
                auth_parts = base64.b64decode(raw).split(b':')
            except:
                response = HttpResponse()
                response.status_code = 555
                return response
            try:
                uname, passwd = (smart_text(auth_parts[0]),
                                 smart_text(auth_parts[1]))
            except DjangoUnicodeDecodeError:
                response = HttpResponse()
                response.status_code = 555
                return response

            user = authenticate(username=uname, password=passwd)
            if user is not None and user.is_active:
                login(http_request, user)
                http_request.user = user
                response = HttpResponse()
                response.status_code = 222
                return response
    response = HttpResponse()
    response.status_code = 555
    return response

from django.contrib.auth.middleware import RemoteUserMiddleware

class CustomHeaderMiddleware(RemoteUserMiddleware):
    header = 'HTTP_AUTHORIZATION'