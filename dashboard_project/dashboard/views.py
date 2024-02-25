from django.shortcuts import render, redirect, get_object_or_404
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, FeedbackForm
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime
from django.conf import settings
from .models import Feedback, UserProfile, ActivityLog, Analytics
from django.contrib.auth.models import User
from .handlers import log_activity
import os
import logging

logger = logging.getLogger(__name__)

def home_view(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            ActivityLog.objects.create(user=request.user, action='Registered a new account')
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            ActivityLog.objects.create(user=user, action='Logged in')
            return redirect('home')
        else:
            # Handle invalid login
            pass
    return render(request, 'login.html')

def logout_view(request):
    ActivityLog.objects.create(user=request.user, action='Logged out')
    logout(request)
    return redirect('home')

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            ActivityLog.objects.create(user=request.user, action='Provided feedback')
            return redirect('feedback')
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})

@login_required
def user_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    if request.method == 'POST':
        profile.bio = request.POST.get('bio', '')
        # Update other fields as needed for the user profile
        profile.save()
        return redirect('user_profile')
    return render(request, 'user_profile.html', {'user': user, 'profile': profile})

@user_passes_test(lambda u: u.is_superuser)
def feedback_list(request):
    feedback_list = Feedback.objects.all()
    return render(request, 'feedback_list.html', {'feedback_list': feedback_list})

@user_passes_test(lambda u: u.is_superuser)
def admin_page(request):
    feedback_list = Feedback.objects.all()
    return render(request, 'admin_page.html', {'feedback_list': feedback_list})

@user_passes_test(lambda u: u.is_superuser)
def user_management(request):
    users = User.objects.all()
    return render(request, 'user_management.html', {'users': users})

def activity_log_page(request):
    logs = ActivityLog.objects.all().order_by('-timestamp')  # Fetch all logs ordered by timestamp
    return render(request, 'activity_log_page.html', {'logs': logs})

def calendar_view(request):
    return render(request, 'calendar.html')

@user_passes_test(lambda u: u.is_superuser)
def analytics_page(request):
    analytics = Analytics.objects.all()
    return render(request, 'analytics_page.html', {'analytics': analytics})

@user_passes_test(lambda u: u.is_superuser)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        # Update user details
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        return redirect('user_management')
    return render(request, 'edit_user.html', {'user': user})

@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('user_management')

@user_passes_test(lambda u: u.is_superuser)
def delete_feedback(request, feedback_id):
    feedback = Feedback.objects.get(id=feedback_id)
    feedback.delete()
    return redirect('feedback_list')

def get_last_file_update_time(service, spreadsheet_id):
    # Get the file metadata to retrieve the last modified timestamp
    try:
        file_metadata = service.files().get(fileId=spreadsheet_id, fields='modifiedTime').execute()
        modified_time_str = file_metadata.get('modifiedTime', None)
        if modified_time_str:
            modified_time = datetime.datetime.fromisoformat(modified_time_str.replace('Z', '+00:00'))
            return modified_time
    except Exception as e:
        print(f"Failed to get file metadata: {e}")

    return None

@login_required
def dashboard_view(request):
    # Path to the JSON file containing your OAuth client credentials
    CLIENT_SECRET_FILE = 'C:\OrderBlockWebsite\client_secret_291062463602-u0s437gfu4dlno0hr8798s1fju0ahtt7.apps.googleusercontent.com.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
       creds = Credentials.from_authorized_user_file('token.json')
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
       if creds and creds.expired and creds.refresh_token:
           creds.refresh(Request())
       else:
           flow = InstalledAppFlow.from_client_secrets_file(
               CLIENT_SECRET_FILE, SCOPES)
           creds = flow.run_local_server(port=8080)
       # Save the credentials for the next run
       with open('token.json', 'w') as token:
           token.write(creds.to_json())

    # Use creds to create a client to interact with the Google Sheets API
    service = build('sheets', 'v4', credentials=creds)

    # The ID of the spreadsheet.
    SPREADSHEET_ID = '1ZtWa2gPxK-t7qITh4O5QXhS5ZtM9xR4IDn6zm4TxNbw'

    # The range of the data to retrieve.
    RANGE_NAME = 'Discord_Export_Data!A2:F'

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    values = result.get('values', [])

    # Get the selected symbol and timeframe from the request
    symbol = request.GET.get('symbol', 'All')
    timeframe = request.GET.get('timeframe', 'All')

    # Filter the data based on the selected symbol and timeframe
    filtered_data = []
    for row in values:
        if (symbol == 'All' or row[0] == symbol) and (timeframe == 'All' or row[1] == timeframe):
            filtered_data.append(row)
            
    # Determine if new data is available
    last_update_timestamp = get_last_file_update_time(service, SPREADSHEET_ID)
    last_fetch_timestamp = request.session.get('last_fetch_timestamp')
    new_data_available = last_fetch_timestamp is None or (last_update_timestamp and last_update_timestamp > last_fetch_timestamp)

    # Update the last fetch timestamp in the session
    request.session['last_fetch_timestamp'] = datetime.now().timestamp()

    context = {
        'symbols': ['All'] + list(set([row[0] for row in values])),
        'timeframes': ['All'] + list(set([row[1] for row in values])),
        'filtered_data': filtered_data,
        'new_data_available': new_data_available,
        'last_update_timestamp': last_update_timestamp
    }
    
    if 'reload' in request.POST:
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        values = result.get('values', [])
        context['filtered_data'] = values

    return render(request, 'dashboard/dashboard.html', context)
