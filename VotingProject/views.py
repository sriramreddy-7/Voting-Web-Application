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
from django.contrib import messages
from datetime import datetime


def index(request):
    return render(request, 'index.html')


def voter_register(request):
    if request.method == 'POST':
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
     
        
        if password1 != password2:
            return render(request, 'auth/voter_register.html', {'error': 'Passwords do not match'})

        user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name, last_name=last_name)
        user.save()
        organization = Organization.objects.get(pk=org_id)
        voter = Voter.objects.create(user=user, organization=organization, aadhar_number=aadhar_number,
                                     role=role, id_number=id_number, department=department,)
        voter.save()
        messages.success(request, 'Voter registered successfully.')
        return redirect('voter_login')
    else:
        org_name = Organization.objects.all()
        context = {'org_name': org_name}
        return render(request, 'auth/voter_register.html', context)


def voter_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                voter = Voter.objects.get(user=user)
            except :
                messages.error(request, 'Invalid credentials. Please try again!')
                return render(request, 'auth/voter_login.html')
            return redirect('voter_dashboard', voter_id=voter.id)
        messages.error(request, 'Invalid credentials. Please try again!')
        return render(request, 'auth/voter_login.html')
    else:
        return render(request, 'auth/voter_login.html')


def org_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                org=Organization.objects.get(admin__username=username)
            except:
                messages.error(request, 'Invalid credentials. Please try again!')
                return render(request,'auth/org_login.html')
            return redirect('org_dashboard', org_name=org.name)
        messages.error(request, 'Invalid credentials. Please try again!')
        return render(request,'auth/org_login.html')
        # return render(request,'auth/org_login.html')
    return render(request,'auth/org_login.html')


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
          
        )
        organization.save()
        messages.success(request, 'Organization registered successfully.')
        return redirect('org_login')
    return render(request,'auth/org_register.html')


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




def trail(request):
    return render(request,'trail.html')


def test2(request):
    return render(request,'test2.html')





def admin_login(request):
    return render(request,'auth/admin_login.html')

def voter_dashboard(request,voter_id):
    try:
        voter = Voter.objects.select_related('organization').get(id=voter_id)
    except Voter.DoesNotExist:
        return HttpResponse("Voter does not exist.")

    recent_votes = PollVote.objects.filter(user=voter.user).order_by('-id')[:5]
    organization = voter.organization
    org_name = organization.name
    admin_username = organization.admin.username
    role = organization.role
    id_number = organization.id_number
    department = organization.department
   
    context={
        'voter': voter,
        'org_name': org_name,
        'admin_username': admin_username,
        'role': role,
        'id_number': id_number,
        'department': department,
        'recent_votes': recent_votes,  
        
    }
    
    return render(request, 'voter/voter_dashboard.html',context)




def admin_dashboard(request):
    return render(request,'dashboard/admin_dashboard.html')

def org_dashboard(request,org_name):
    username=request.user.username
    org=Organization.objects.get(admin__username=username)
    organization = Organization.objects.get(name=org_name)
    total_votes = PollVote.objects.filter(poll__admin__organization=organization).count()
    registered_users = Voter.objects.filter(organization=organization).count()
    active_elections = Poll.objects.filter(admin__organization=organization).count()
    recent_polls = Poll.objects.filter(admin__organization=organization).order_by('-start_time')[:5]

    verified_voters = Voter.objects.filter(organization=organization, aadhar_number__isnull=False).count()
    total_voters = registered_users

    print(org)
    context={'org':org,'org_name': org_name, 'total_votes': total_votes,
        'registered_users': registered_users,
        'active_elections': active_elections,
        'recent_polls': recent_polls,
        'verified_voters': verified_voters,
        'total_voters': total_voters,}
    return render(request,'org/org_dashboard.html',context)



def org_profile_view(request, org_name):
    organization = get_object_or_404(Organization, name=org_name)
    username=request.user.username
    org=Organization.objects.get(admin__username=username)
    
    context = {'organization': organization,'org':org,'org_name': org_name}
    return render(request, 'org/organization_profile.html', context)


@login_required
def create_poll(request, org_name):
    username = request.user.username
    org = Organization.objects.get(admin__username=username)
    now = datetime.now().strftime('%Y-%m-%dT%H:%M')
    context = {'org': org, 'org_name': org_name,'now':now}

    if request.method == 'POST':
        question = request.POST.get('question')
        choices = request.POST.getlist('choice')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        if question and choices:
            poll = Poll.objects.create(question=question, start_time=start_time, end_time=end_time, admin=request.user)
            for choice in choices:
                Choice.objects.create(poll=poll, choice_text=choice)
            
            
            messages.success(request, 'Poll created successfully.')
            return redirect('create_poll', org_name=org.name)  
        
        messages.error(request, 'Failed to create poll. Please fill in all required fields.')
        return redirect('create_poll', org_name=org.name)
    
    return render(request, 'org/create_poll.html', context)


@login_required
def poll_list(request):
    polls = Poll.objects.all()
    return render(request, 'poll_list.html', {'polls': polls})


@login_required
def org_vote_view(request, org_name, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    username = request.user.username
    org = Organization.objects.get(admin__username=username)
    context = {'org': org, 'org_name': org_name, 'poll': poll}
    return render(request, 'org/org_vote_view.html', context)

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


def edit_poll(request, org_name, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    org = Organization.objects.get(admin=request.user)
    now = datetime.now().strftime('%Y-%m-%dT%H:%M')
    
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'edit':
            poll.question = request.POST.get('question')
            poll.start_time = request.POST.get('start_time')
            poll.end_time = request.POST.get('end_time')
            poll.save()
            messages.success(request, 'Poll updated successfully.')
            return redirect('manage_poll_list', org_name=org_name)
        elif action == 'stop':
            poll.stopped = True
            poll.save()
            messages.success(request, 'Poll stopped successfully.')
            return redirect('manage_poll_list', org_name=org_name)
        elif action=='enable':
            poll.stopped = False
            poll.save()
            messages.success(request, 'Poll enabled successfully.')
            return redirect('manage_poll_list', org_name=org_name)
        elif action == 'delete':
            poll.delete()
            messages.success(request, 'Poll deleted successfully.')
            return redirect('manage_poll_list', org_name=org_name)
        elif action == 'add_choice':
            choice_text = request.POST.get('new_choice')
            if choice_text:
                Choice.objects.create(poll=poll, choice_text=choice_text)
                messages.success(request, 'Choice added successfully.')
            else:
                messages.error(request, 'Enter a valid choice text.')
        elif action == 'delete_choice':
            choice_id = int(request.POST.get('delete_choice'))
            choice = get_object_or_404(Choice, pk=choice_id)
            choice.delete()
            messages.success(request, 'Choice deleted successfully.')

        return redirect('edit_poll', org_name=org_name, poll_id=poll_id)

    context = {'org_name': org_name, 'poll': poll, 'org': org,'now':now}
    return render(request, 'org/edit_poll.html', context)


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

   
def poll_results(request, org_name, poll_id):
    poll = Poll.objects.get(id=poll_id)
    choices = poll.choice_set.all()
    votes_data = []

   
    for choice in choices:
        votes_count = PollVote.objects.filter(poll=poll, choice=choice).count()
        votes_data.append({
            'choice_text': choice.choice_text,
            'votes_count': votes_count,
        })

    
    total_votes = sum([data['votes_count'] for data in votes_data])

   
    voters_count = Voter.objects.filter(organization__name=org_name).count()


    casted_voters = PollVote.objects.filter(poll=poll).values('user').distinct().count()
    remaining_voters = voters_count - casted_voters

    org = Organization.objects.get(name=org_name)
    voters = org.voter_set.all()
    casted_voter_ids = PollVote.objects.filter(poll=poll).values_list('user__id', flat=True)
    not_casted_voters = voters.exclude(user__id__in=casted_voter_ids)

   
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



from django.utils import timezone

def active_polls_list(request, voter_id):
    voter = Voter.objects.select_related('organization').get(id=voter_id)
    organization = voter.organization
    org_name = organization.name
    
   
    current_time = timezone.now()
    active_polls = Poll.objects.filter(
        start_time__lte=current_time,
        end_time__gte=current_time,
        admin=organization.admin  
    )
    
    context = {'active_polls': active_polls, 'voter': voter, 'org': organization, 'org_name': org_name}
    return render(request, 'voter/active_polls.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from accounts.models import Poll, Choice, PollVote
from django.utils import timezone

   
    
def vote_poll(request, voter_id, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    voter = get_object_or_404(Voter, pk=voter_id)
    already_voted = PollVote.objects.filter(user=voter.user, poll=poll).exists()
    context = {
        'voter': voter,
        'poll': poll,
        'already_voted': already_voted,
    }

    if request.method == 'POST' and not already_voted:
        choice_id = request.POST.get('choice')
        choice = get_object_or_404(Choice, pk=choice_id)
        PollVote.objects.create(user=voter.user, poll=poll, choice=choice)
        messages.success(request, 'Your vote has been recorded.')
        return redirect('active_polls_list', voter_id=voter.id)
    elif already_voted:
        messages.error(request, 'You have already voted in this poll.')
    return render(request, 'voter/poll_voting.html', context)

    
    
@login_required
def voter_poll_results(request, voter_id, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    voter = get_object_or_404(Voter, pk=voter_id)
    
    
    has_voted = PollVote.objects.filter(user=voter.user, poll=poll).exists()
    
    
    voters_in_organization = Voter.objects.filter(organization=voter.organization)
    
    
    voters_ordered = []
    casted_voter_ids = set(PollVote.objects.filter(poll=poll).values_list('user__id', flat=True))
    for voter_in_org in voters_in_organization:
        voters_ordered.append({
            'user': voter_in_org.user.username,
            'organization': voter_in_org.organization.name,
            'status': 'Voted' if voter_in_org.id in casted_voter_ids else 'Not Voted'
        })
    
    return render(request, 'voter/voter_poll_results.html', {
        'poll': poll,
        'voter': voter,
        'has_voted': has_voted,
        'voters_ordered': voters_ordered,
    })