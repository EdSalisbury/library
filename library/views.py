from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
import json

def index(request):
    return render_to_response('index.html')

def user_login(request):
    auth = {}
    auth['authenticated'] = False
    if request.method == 'POST':
        user = authenticate(username = request.POST['username'], password = request.POST['password'])
        if user is not None:
            auth['authenticated'] = True
            auth['username'] = user.username
            login(request, user)

    response = json.dumps(auth)

    return HttpResponse(response)

def user_logout(request):
    logout(request)

    return HttpResponse("")
