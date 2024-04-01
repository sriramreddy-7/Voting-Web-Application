from django.shortcuts import render,redirect
from django.http import HttpResponse
# from user.models import User
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from accounts.models import Organization
from django.shortcuts import get_object_or_404


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
    context={'org':org,'org_name': org_name}
    return render(request,'org/org_dashboard.html',context)

# def create_poll(request,org_name):
#     username=request.user.username
#     org=Organization.objects.get(admin__username=username)
#     context={'org':org,'org_name': org_name}
#     return render(request,'org/create_poll.html',context)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Poll, Choice, PollVote
from django.utils import timezone

@login_required
def create_poll(request,org_name):
    username=request.user.username
    org=Organization.objects.get(admin__username=username)
    context={'org':org,'org_name': org_name}
    if request.method == 'POST':
        question = request.POST.get('question')
        choices = request.POST.getlist('choice')

        if question and choices:
            poll = Poll.objects.create(question=question, start_time=timezone.now(), end_time=timezone.now(), admin=request.user)
            for choice in choices:
                Choice.objects.create(poll=poll, choice_text=choice)
            return HttpResponse('Poll created successfully.')
            # return redirect('poll')
    return render(request,'org/create_poll.html',context)

@login_required
def poll_list(request):
    polls = Poll.objects.all()
    return render(request, 'poll_list.html', {'polls': polls})

@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.method == 'POST':
        choice_id = request.POST.get('choice')
        choice = get_object_or_404(Choice, pk=choice_id)
        if not Vote.objects.filter(user=request.user, poll=poll).exists():
            Vote.objects.create(user=request.user, poll=poll, choice=choice)
            return redirect('poll_results', poll_id=poll_id)
        else:
            return render(request, 'error.html', {'message': 'You have already voted in this poll.'})
    return render(request, 'vote.html', {'poll': poll})

@login_required
def poll_results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    votes = PollVote.objects.filter(poll=poll)
    choices = poll.choice_set.all()
    results = {choice.choice_text: votes.filter(choice=choice).count() for choice in choices}
    return render(request, 'poll_results.html', {'poll': poll, 'results': results})


from django.contrib import messages

@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.method == 'POST':
        choice_id = request.POST.get('choice')
        choice = get_object_or_404(Choice, pk=choice_id)
        
        # Check if the user has already voted in this poll
        if Vote.objects.filter(user=request.user, poll=poll).exists():
            messages.error(request, "You have already voted in this poll.")
            return redirect('poll_list')
        
        PollVote.objects.create(user=request.user, poll=poll, choice=choice)
        return redirect('poll_results', poll_id=poll_id)
    
    return render(request, 'vote.html', {'poll': poll})

