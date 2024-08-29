from django.http import Http404
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException, NotAuthenticated, AuthenticationFailed, Throttled
from rest_framework.response import Response
from rest_framework.views import APIView, set_rollback
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from exceptions.excptions import CreatifyException


class CreatifyView(APIView):
    permission_classes = (IsAuthenticated,)

    @property
    def allowed_methods(self):
        return ['GET', 'POST', 'PUT', 'DELETE']

    def initial(self, request, *args, **kwargs):
        """
        视图处理前
        """
        return super(CreatifyView, self).initial(request, *args, **kwargs)

    def finalize_response(self, request, response, *args, **kwargs):
        if response == None:
            response = ""

        if isinstance(response, (dict, list, str)):
            # response = Response({'code': '10000', 'message': '', 'data': response})
            response = Response(response)

        if hasattr(request, "_SET_COOKIE"):
            response.set_cookie('Authorization', 'Bearer %s' % request._SET_COOKIE, max_age=86400 * 7)
        elif hasattr(request, "_DEL_COOKIE"):
            response.delete_cookie('Authorization')
        return super(CreatifyView, self).finalize_response(request, response, *args, **kwargs)

    def handle_exception(self, exc):
        """
        Handle any exception that occurs, by returning an appropriate response,
        or re-raising the error.
        """
        set_rollback()

        response = None
        if isinstance(exc, CreatifyException):
            response = Response({'code': exc.error_code, 'message': exc.error_message, 'data': exc.data},
                                exception=False)
        elif isinstance(exc, APIException):
            if isinstance(exc, NotAuthenticated):
                response = Response({'code': '10001', 'message': _('请重新登录')})
            elif isinstance(exc, AuthenticationFailed):
                response = Response({'code': '10002', 'message': _('登录失效，请重新登录')})
            elif isinstance(exc, Throttled):
                response = Response({'code': '80000', 'message': _('请求次数超出限制')})
            else:
                response = Response({'code': str(exc.default_code), 'message': exc.detail},
                                    exception=True)
        elif isinstance(exc, Http404):
            response = Response({'code': '404', 'message': '404 Not Found'},
                                status=404, exception=True)
        elif isinstance(exc, PermissionDenied):
            response = Response({'code': '403', 'message': '403 Forbidden'},
                                status=403, exception=True)
        if response:
            exc.__traceback__ = None
            return response
        self.raise_uncaught_exception(exc)