from django.shortcuts import render_to_response, get_object_or_404

def index(request):
    return render_to_response('index.html')

def login(request):
    return render_to_response("login.html")
