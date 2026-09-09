from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, HttpResponse
from myapp.models import User_Info
from django.forms import ModelForm
from django import forms
from django.views.decorators.csrf import csrf_exempt
import json

class User_login(forms.Form):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)


# Create your views here.
def login(request):
    if request.method == "GET":
        form = User_login()
        return render(request, "login.html", {"form": form})
    form = User_login(request.POST)
    if not form.is_valid():
        return render(request, "login.html", {"form": form})
    obj = User_Info.objects.filter(**form.cleaned_data).first()
    if obj:
        request.session['info'] = {'id':obj.username, 'password':obj.password, 'is_login':True}
        return HttpResponseRedirect('/home')
    else:
        form.add_error('password', 'username or password is incorrect')
        return render(request, "login.html", {"form": form})


def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')


import time

"""
status 功能
"""
# 暂时保存在内存里
latest_status = {
    "device_id": "unknown",
    "online": False,
    "cpu_usage": 0.0,
    "cpu_temp": 0.0,
    "ram_usage": 0.0,
    "fps": 0.0,
    "camera": "offline",
    "uptime": 0,
}

last_seen = 0

@csrf_exempt
def device_status(request):
    global latest_status
    global last_seen
    if request.method == 'POST':
        try:
            # request.body 是 bytes
            # json.loads() 将 JSON 转成 Python 字典
            # request.body 里是 HTTP 请求体（body）的原始字节数据
            data = json.loads(request.body)
        except json.JSONDecodeError:
            # 出错后执行这里
            return JsonResponse(
                {
                    "status":"error",
                    "message":"invalid json",
                },
                status=400,
            )
        # save the latest info
        latest_status = {
            "device_id": data.get('device_id', 'unknown'),
            "online": data.get('online', False),
            "cpu_usage": data.get('cpu_usage', 0.0),
            "cpu_temp": data.get('cpu_temp', 0.0),
            "ram_usage": data.get('ram_usage', 0.0),
            "fps": data.get('fps', 0.0),
            "uptime": data.get('uptime', 0),
            "camera": data.get('camera', 'offline'),
        }

        last_seen = time.time()

        print("Received status: ", latest_status)
        return JsonResponse(latest_status)

    # GET
    elif request.method == 'GET':

        if (time.time() - last_seen > 10):

            latest_status["online"] = False
            latest_status["cpu_usage"] = 0.0
            latest_status["cpu_temp"] = 0.0
            latest_status["ram_usage"] = 0.0
            latest_status["fps"] = 0.0
            latest_status["uptime"] = 0.0
            latest_status["camera"] = "offline"

        return JsonResponse(
            latest_status
        )

        return JsonResponse(
            latest_status
        )

    return JsonResponse({
        "status": "error",
        "message": "invalid method",
        },
        status=405,
    )