from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'counseling/index.html')

def signIn(request):
    if request.method == 'GET':
        return render(request, 'counseling/login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'counseling/login.html')

def signOut(request):
    logout(request)
    return redirect('index')

@login_required
def counsel(request):
    return render(request, 'counseling/offcanvas.html')