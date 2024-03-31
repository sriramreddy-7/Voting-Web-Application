from django.shortcuts import render,redirect
from django.http import HttpResponse
# from user.models import User
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from accounts.models import Organization

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        myuser = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        myuser.save()
        print("User is Created")
        return redirect("success")
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
        return render(request, 'dashboard/voter_dashboard.html')
    return redirect("index")


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')

def success(request):
    return render(request,'success.html')

def voter_register(request):
    return render(request,'auth/voter_register.html')


def trail(request):
    return render(request,'trail.html')


def test2(request):
    return render(request,'test2.html')

def voter_login(request):
    return render(request,'auth/voter_login.html')


def org_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            org=Organization.objects.get(admin__username=username)
            return redirect('org_dashboard', org_name=org.name)
        return HttpResponse("This is login")
    return render(request,'auth/org_login.html')

def admin_login(request):
    return render(request,'auth/admin_login.html')


def voter_dashboard(request):
    return render(request,'dashboard/voter_dashboard.html')

def org_register(request):
    if request.method == 'POST':
        # Extracting form data from POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        org_name = request.POST.get('org_name')
        role = request.POST.get('role')
        id_number = request.POST.get('id')
        department = request.POST.get('department')
        id_proof = request.FILES.get('id_proof')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password1)
        user.save()

        organization = Organization.objects.create(
            name=org_name,
            admin=user,
            role=role,
            id_number=id_number,
            department=department,
            id_proof=id_proof
        )

    return render(request,'auth/org_register.html')


def admin_dashboard(request):
    return render(request,'dashboard/admin_dashboard.html')

def org_dashboard(request,org_name):
    username=request.user.username
    org=Organization.objects.get(admin__username=username)
    print(org)
    context={'org':org}
    return render(request,'dashboard/org_dashboard.html',context)