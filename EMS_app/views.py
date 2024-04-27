import json

from django.db.models import Count, F
from django.db.models.functions import TruncMonth
from django.shortcuts import render

# Create your views here.


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from django.contrib import messages
from django.contrib import sessions
from .models import Organizer, Participant, Event, Registration
from .forms import RegistrationForm,EventForm
# from actions.models import Action
from django.core.exceptions import ObjectDoesNotExist


def main(request):
    request.session.clear()
    return render(request, 'EMS/html_files/main.html')


# login page view is to have login functionality, here credentials are hardcoded. we use this view for login page.
def login(request):
    return render(request, 'EMS/html_files/login_participant.html')

def home_page(request):
    events = Event.objects.all()
    registered_counts = {}
    for event in events:
        registered_count = Registration.objects.filter(event_id=event.event_id, status='registered').count()
        registered_counts[event.event_id] = registered_count
        print(registered_counts)
    return render(request, 'EMS/html_files/home_page.html', {'registered_counts': registered_counts, 'events': events})

def login_page_organizer(request):
        error_message = None
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        try:
            user = Organizer.objects.get(name=username, password=password)
            if user is not None and user.password == password:
                request.session['organizer_name'] = username
                # Authentication successful
                request.session['role'] = "organizer"
                return redirect('EMS:home_page')
            else:
                error_message = "Invalid Password"
        except ObjectDoesNotExist:
            error_message = "Organizer with the given username does not exist"
        return render(request, 'EMS/html_files/login_organizer.html')


def login_page_participant(request):
    error_message = None
    username = request.POST.get('username')
    password = request.POST.get('password')
    print(username)
    print(password)
    try:
        user = Participant.objects.get(name=username, password=password)
        if user is not None and user.password == password:
            request.session['participant_name'] = username
            print(request.session['participant_name'])
            # Authentication successful
            request.session['role'] = "participant"
            return redirect('EMS:home_page')
        else:
            error_message = "Invalid Password"
    except ObjectDoesNotExist:
        error_message = "Organizer with the given username does not exist"
    return render(request, 'EMS/html_files/login_participant.html')

#logout is to logout for the user. It redirects to the home page after logout
#
# def logout_page(request):
#     if 'username' in request.session:
#         del request.session['username']
#     if 'access' in request.session:
#         del request.session['access']
#     return redirect('tripobeatApp:home_page')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            gender = form.cleaned_data['gender']
            role = form.cleaned_data['role']
            phone_number = form.cleaned_data['phone_number']
            request.session['organizer_name'] = username
            if role == 'Organizer':
                user = Organizer.objects.create(name=username, email=email, password=password, phone_number=phone_number,
                                                gender=gender)
            if role == 'Participant':
                user = Participant.objects.create(name=username, email=email, password=password, phone_number=phone_number,
                                                gender=gender)
            #details, created = Organizer.objects.get_or_create(user=user)
            #details.gender = gender
            #details.save()

            #request.session['username'] = user.username
            #messages.success(request, f"{user.username} registered successfully")
            return redirect('EMS:home_page')
    else:
        form = RegistrationForm()
    return render(request, 'EMS/html_files/register.html', {'form': form})

def event_registration(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            location = form.cleaned_data['location']
            description = form.cleaned_data['description']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            org_name = request.session['organizer_name']
            organiser = Organizer.objects.get(name=org_name)
            org_id = organiser.organizer_id
            # Create a new Event object
            event = Event.objects.create(
                name=name,
                location=location,
                description=description,
                start_date=start_date,
                end_date=end_date,
                org_id_id=org_id,
            )

            # Redirect to a success page or do something else
            print("event added succesfully")
            return redirect('EMS:home_page')
            # return render(request, 'EMS/html_files/home_page.html') # Redirect to home page after successful event creation
    else:
        form = EventForm()

    return render(request, 'EMS/html_files/event_registration.html', {'form': form})



def event_edit(request, id):
    event = get_object_or_404(Event, pk=id)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            location = form.cleaned_data['location']
            description = form.cleaned_data['description']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Update event object with new data
            event.name = name
            event.location = location
            event.description = description
            event.start_date = start_date
            event.end_date = end_date
            event.save()

            return redirect('EMS:home_page')
    # Redirect to home page after successful event update
    else:
        initial_data = {
            'name': event.name,
            'location': event.location,
            'description': event.description,
            'start_date': event.start_date,
            'end_date': event.end_date,
        }
        form = EventForm(initial=initial_data)
    return render(request, 'EMS/html_files/events_page.html', {'form': form})
def delete_event(request, id):
    event = Event.objects.get(event_id = id)
    event.delete()
    return redirect('EMS:home_page')


# from django.contrib.auth.decorators import login_required
#
#
# @login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Participant, Registration

def event_view(request, event_id):
    # Fetch the event object using the event_id
    event = get_object_or_404(Event, pk=event_id)

    # Initialize variables to be used in context
    is_registered = False
    registration_status = None
    registration_id = None

    # Check if 'participant_name' exists in session
    participant_name = request.session.get('participant_name', None)

    if participant_name:
        try:
            # Retrieve the participant based on the name
            participant = Participant.objects.get(name=participant_name)
            # Try to fetch the registration object for this participant and event
            registration = Registration.objects.filter(participant=participant, event=event).first()

            if registration:
                is_registered = True
                registration_status = registration.status
                registration_id = registration.id
        except Participant.DoesNotExist:
            # Handle case where participant is not found, which might involve logging an error or redirecting
            pass

    context = {
        'event_name': event,
        'is_registered': is_registered,
        'registration_status': registration_status,
        'registration_id': registration_id,
    }

    return render(request, 'EMS/html_files/event_view.html', context)


from django.db.models import Count

def statistics_page(request):
    # Events by month query (existing code)
    events_by_month = Event.objects.annotate(month=TruncMonth('start_date')).values('month').annotate(
        count=Count('event_id')).order_by('month')

    # Top 5 events by registration count
    top_events = Event.objects.annotate(registration_count=Count('registrations')).order_by('-registration_count')[:5]

    # Preparing data for Chart.js (existing code)
    months = [event['month'].strftime("%B") for event in events_by_month]
    counts = [event['count'] for event in events_by_month]

    # Passing data to template (existing code)
    context = {
        'months': json.dumps(months),
        'counts': json.dumps(counts),
        'top_events': top_events,
    }
    return render(request, 'EMS/html_files/statistics.html', context)



def register_for_event(request, event_id):
    print("Entered", event_id)
    participant = get_object_or_404(Participant, name=request.session['participant_name'])
    event=get_object_or_404(Registration,id=event_id)
    print(participant.name)
    event = get_object_or_404(Event, pk=event_id)
    print(event.name)
    Registration.objects.get_or_create(participant=participant, event=event)
    return redirect('EMS:event_view', event_id=event_id)


def register_for_event(request, event_id):
    participant_name = request.session.get('participant_name')
    participant = get_object_or_404(Participant, name=participant_name)
    event = get_object_or_404(Event, pk=event_id)
    registration, created = Registration.objects.get_or_create(participant=participant, event=event)
    if created:
        Event.objects.filter(pk=event_id).update(count=F('count') + 1)
    else:
        registration.status = "registered"
        registration.save()

    return redirect('EMS:event_view', event_id=event_id)

def unregister_from_event(request, registration_id):
    print("fvjhdksjhf", registration_id)
    registration = get_object_or_404(Registration, id=registration_id)
    # registration = get_object_or_404(Registration, pk=registration_id, participant__user=request.user)
    registration.status = 'unregistered'
    registration.save()
    return redirect('EMS:event_view', event_id=registration.event_id)

