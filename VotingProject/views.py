from django.shortcuts import render,redirect
from django.http import HttpResponse
# from user.models import User
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from accounts.models import Organization,Voter
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from accounts.models import Poll, Choice, PollVote
from django.db.models import Count
from django.shortcuts import render
from accounts.models import Poll, PollVote, Organization,Voter,Choice,PollVote


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
    if request.method == 'POST':
        # Extracting data from the POST request
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        aadhar_number = request.POST['aadhar_number']
        org_id = request.POST['org_name']  
        role = request.POST['role']
        id_number = request.POST['id']
        department = request.POST['department']
        id_proof = request.FILES['id_proof']
        
        if password1 != password2:
            return render(request, 'auth/voter_register.html', {'error': 'Passwords do not match'})

        user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name, last_name=last_name)
        user.save()

        organization = Organization.objects.get(pk=org_id)
        voter = Voter.objects.create(user=user, organization=organization, aadhar_number=aadhar_number,
                                     role=role, id_number=id_number, department=department, id_proof=id_proof)
        voter.save()
        return HttpResponse('Voter registered successfully.')
        # user = authenticate(request, username=username, password=password1)
        # if user is not None:
        #     login(request, user)
        #     return redirect('home')  # Redirect to home page after successful registration
        # else:
        #     return redirect('login')  # Redirect to login page if login fails

    else:
        org_name = Organization.objects.all()
        context = {'org_name': org_name}
        return render(request, 'auth/voter_register.html', context)


def trail(request):
    return render(request,'trail.html')


def test2(request):
    return render(request,'test2.html')

def voter_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            voter = Voter.objects.get(user=user)
            return redirect('voter_dashboard', voter_id=voter.id)
        return HttpResponse("Invalid email or password.")
    else:
        return render(request, 'auth/voter_login.html')


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

def voter_dashboard(request, voter_id):
    try:
        voter = Voter.objects.select_related('organization').get(id=voter_id)
    except Voter.DoesNotExist:
        return HttpResponse("Voter does not exist.")
    
   
    
    organization = voter.organization
    org_name = organization.name
    admin_username = organization.admin.username
    role = organization.role
    id_number = organization.id_number
    department = organization.department
    id_proof_url = organization.id_proof.url if organization.id_proof else None
    context={
        'voter': voter,
        'org_name': org_name,
        'admin_username': admin_username,
        'role': role,
        'id_number': id_number,
        'department': department,
        'id_proof_url': id_proof_url,
        
    }
    
    return render(request, 'voter/voter_dashboard.html',context)

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
    organization = Organization.objects.get(name=org_name)
    total_votes = PollVote.objects.filter(poll__admin__organization=organization).count()
    registered_users = Voter.objects.filter(organization=organization).count()
    active_elections = Poll.objects.filter(admin__organization=organization).count()

    print(org)
    context={'org':org,'org_name': org_name, 'total_votes': total_votes,
        'registered_users': registered_users,
        'active_elections': active_elections }
    return render(request,'org/org_dashboard.html',context)

# def create_poll(request,org_name):
#     username=request.user.username
#     org=Organization.objects.get(admin__username=username)
#     context={'org':org,'org_name': org_name}
#     return render(request,'org/create_poll.html',context)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
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
def vote(request,org_name, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    username=request.user.username
    org=Organization.objects.get(admin__username=username)
    context={'org':org,'org_name': org_name,'poll': poll}
    if request.method == 'POST':
        choice_id = request.POST.get('choice')
        choice = get_object_or_404(Choice, pk=choice_id)
        if not PollVote.objects.filter(user=request.user, poll=poll).exists():
            PollVote.objects.create(user=request.user, poll=poll, choice=choice)
            return HttpResponse('Your vote has been recorded.')
            # return redirect('poll_results', poll_id=poll_id)
        else:
            return render(request, 'error.html', {'message': 'You have already voted in this poll.'})
    return render(request, 'org/poll_vote.html', context)

@login_required
def poll_results(request,org_name,poll_id):
    username=request.user.username
    org=Organization.objects.get(admin__username=username)
    org_name=org.name
    poll = get_object_or_404(Poll, pk=poll_id)
    votes = PollVote.objects.filter(poll=poll)
    choices = poll.choice_set.all()
    results = {choice.choice_text: votes.filter(choice=choice).count() for choice in choices}
    return render(request, 'poll_results.html', {'poll': poll, 'results': results,'org':org,'org_name':org_name})


# from django.contrib import messages

# @login_required
# def vote(request, poll_id):
#     poll = get_object_or_404(Poll, pk=poll_id)
#     if request.method == 'POST':
#         choice_id = request.POST.get('choice')
#         choice = get_object_or_404(Choice, pk=choice_id)
        
#         # Check if the user has already voted in this poll
#         if PollVote.objects.filter(user=request.user, poll=poll).exists():
#             messages.error(request, "You have already voted in this poll.")
#             return redirect('poll_list')
        
#         PollVote.objects.create(user=request.user, poll=poll, choice=choice)
#         return redirect('poll_results', poll_id=poll_id)
    
#     return render(request, 'org/poll_vote.html', {'poll': poll})

def manage_poll_list(request,org_name):
    polls = Poll.objects.filter(admin=request.user)
    username=request.user.username
    org=Organization.objects.get(admin__username=username)
    context={'org':org,'org_name': org_name,'polls':polls}
    return render(request, 'org/manage_poll_list.html', context)


def voter_list(request,org_name):
    voters = Voter.objects.filter(organization__admin=request.user)
    username=request.user.username
    org=Organization.objects.get(admin__username=username)
    context={'org':org,'org_name': org_name,'voters':voters}
    return render(request, 'org/voter_list.html', context)


"""from faker import Faker
import random

fake = Faker()

def voter_register(request):
    # if request.method == 'POST':
        # Generate fake data
    for i in range(50):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name}{last_name}@mail.com".lower()
        aadhar_number = ''.join([str(random.randint(0, 9)) for _ in range(12)])
        org_id =1  # Assuming organization IDs are integers
        role = fake.job()
        id_number = fake.random_number(digits=5)
        department = fake.job()
        id_proof = None  # Assuming ID proof is not generated here

        username = f"{first_name}{last_name}{id_number}"
        password1=f"{first_name}{id_number}"
        # You might want to add validation checks here for the generated data

        # Perform the registration process
        user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name, last_name=last_name)
        user.save()
        organization = Organization.objects.get(pk=org_id)
        voter = Voter.objects.create(user=user, organization=organization, aadhar_number=aadhar_number,
                                     role=role, id_number=id_number, department=department, id_proof=id_proof)
        voter.save()
        print(user)
        print("--------------------------------------------------------------------------------------")
        print(voter)
    return HttpResponse('Voter registered successfully.')"""

    # else:
    #     org_name = Organization.objects.all()
    #     context = {'org_name': org_name}
    #     return render(request, 'auth/voter_register.html', context)
    
    



def poll_results(request, org_name, poll_id):
    poll = Poll.objects.get(id=poll_id)
    choices = poll.choice_set.all()
    votes_data = []

    # Count votes for each choice
    for choice in choices:
        votes_count = PollVote.objects.filter(poll=poll, choice=choice).count()
        votes_data.append({
            'choice_text': choice.choice_text,
            'votes_count': votes_count,
        })

    # Count total votes
    total_votes = sum([data['votes_count'] for data in votes_data])

    # Count total voters
    voters_count = Voter.objects.filter(organization__name=org_name).count()

    # Count casted voters
    casted_voters = PollVote.objects.filter(poll=poll).values('user').distinct().count()

    # Count voters who haven't casted their votes
    remaining_voters = voters_count - casted_voters

    # Get the list of voters who haven't casted their votes
    org = Organization.objects.get(name=org_name)
    voters = org.voter_set.all()
    casted_voter_ids = PollVote.objects.filter(poll=poll).values_list('user__id', flat=True)
    not_casted_voters = voters.exclude(user__id__in=casted_voter_ids)

    # Order voters by those who have voted and those who haven't
    voted_voters = Voter.objects.filter(id__in=casted_voter_ids)
    voters_ordered = list(voted_voters) + list(not_casted_voters)
    username=request.user.username
    org=Organization.objects.get(admin__username=username)

    context = {
        'org':org,
        'org_name': org_name,
        'poll': poll,
        'votes_data': votes_data,
        'total_votes': total_votes,
        'voters_count': voters_count,
        'casted_voters': casted_voters,
        'remaining_voters': remaining_voters,
        'voters_ordered': voters_ordered,
    }
    return render(request, 'org/poll_results.html', context)





def active_polls_list(request,voter_id):
    voter = Voter.objects.select_related('organization').get(id=voter_id)
    # active_polls = Poll.objects.filter(start_time__lte=timezone.now(), end_time__gte=timezone.now())
    active_polls = Poll.objects.all()
    return render(request, 'voter/active_polls.html', {'active_polls': active_polls,'voter':voter})

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from accounts.models import Poll, Choice, PollVote
from django.utils import timezone

'''def vote_poll(request, voter_id, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    voter = get_object_or_404(Voter, pk=voter_id)
    
    # Check if the poll is active
    # if poll.start_time <= timezone.now() <= poll.end_time:
    
    if request.method == 'POST':
        choice_id = request.POST.get('choice')
        choice = get_object_or_404(Choice, pk=choice_id)
        
        # Check if the user has already voted in this poll
        if not PollVote.objects.filter(user=voter.user, poll=poll).exists():
            PollVote.objects.create(user=voter.user, poll=poll, choice=choice)
            message = 'Your vote has been recorded.'
            context={
                'message':message,
            }
            return render(request,'message.html',context) 
        else:
            message = 'You have already voted in this poll.'
            context={
                'message':message,
            }
            return render(request,'message.html',context)
    else:
        return render(request, 'voter/poll_voting.html', {'voter': voter, 'poll': poll})'''
    # else:
    #     return HttpResponse('This poll is not currently active.')
    
def vote_poll(request, voter_id, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    voter = get_object_or_404(Voter, pk=voter_id)
    
    # Check if the user has already voted in this poll
    already_voted = PollVote.objects.filter(user=voter.user, poll=poll).exists()
    
    if request.method == 'POST' and not already_voted:
        choice_id = request.POST.get('choice')
        choice = get_object_or_404(Choice, pk=choice_id)
        
        # Check if the user has already voted in this poll
        if not already_voted:
            PollVote.objects.create(user=voter.user, poll=poll, choice=choice)
            message = 'Your vote has been recorded.'
        else:
            message = 'You have already voted in this poll.'
    else:
        message = 'You have already voted in this poll.'

    context = {
        'voter': voter,
        'poll': poll,
        'already_voted': already_voted,
        'message': message,
    }
    return render(request, 'voter/poll_voting.html', context)

    
    
    