from django.shortcuts import render,redirect
from django.http import HttpResponse
# from user.models import User
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(username,email,password)
        myuser = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        myuser.save()
        print("User is Created")
    return render(request,'register.html')

def user_login(request):
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("user_dashboard")
        return HttpResponse("This is login")
    return render(request,'user_login.html')
    
def user_dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'user_dashboard.html')
    return redirect("index")


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')