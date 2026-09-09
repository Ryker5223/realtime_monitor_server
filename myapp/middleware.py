from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class LoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 获取当前请求路劲
        path = request.path_info

        if path == "/login/":
            return None

        if path == "/api/device/status/":
            return None

        info_dict = request.session.get('info')
        if info_dict:
            return None
        return  redirect("/login/")