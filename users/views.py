from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import WorkSession
from django.utils import timezone
from django.http import HttpResponse

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RegistrationForm
import pandas as pd
from openpyxl import load_workbook
from openpyxl.worksheet.protection import SheetProtection

def home(request):
    return render(request, 'home.html')  # Render a simple home page template

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            login(request, user)  # Log the user in immediately after registration
            messages.success(request, f'Account created for {user.username}!')
            return redirect('dashboard')  # Redirect to dashboard or any other page
        else:
            messages.error(request, 'There was an error with your registration. Please try again.')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    if request.method == 'POST':
        if 'start' in request.POST:
            session = WorkSession(user=request.user)
            session.save()
        elif 'stop' in request.POST:
            session = WorkSession.objects.filter(user=request.user, end_time__isnull=True).first()
            if session:
                session.end_time = timezone.now()
                session.save()
        elif 'reset' in request.POST:  # Reset the work sessions if confirmed
            # Delete all sessions for the user
            WorkSession.objects.filter(user=request.user).delete()
        elif 'export' in request.POST:  # Export data to Excel
            work_sessions = WorkSession.objects.filter(user=request.user)
            
            # Create a DataFrame to hold the session data
            data = []
            for session in work_sessions:
                start_time = session.start_time.replace(tzinfo=None) if session.start_time else None
                end_time = session.end_time.replace(tzinfo=None) if session.end_time else 'Ongoing'
                data.append({
                    'Start Time': start_time,
                    'End Time': end_time
                })

            df = pd.DataFrame(data)

            # Create an HTTP response for the Excel file
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=working_records.xlsx'

            # Write to Excel using openpyxl
            with pd.ExcelWriter(response, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Working Records')

            # Now, let's access the generated workbook
            workbook = writer.book
            sheet = workbook['Working Records']

            # Apply sheet protection
            sheet.protection.sheet = True  # Enable protection on the sheet
            sheet.protection.set_password('your_password')  # Optional: set a password

            # Disallow editing of cells and other elements
            sheet.protection.format_cells = False  # Prevent editing cells
            sheet.protection.format_columns = False  # Prevent column resizing
            sheet.protection.format_rows = False  # Prevent row resizing
            sheet.protection.insert_columns = False  # Prevent inserting columns
            sheet.protection.insert_rows = False  # Prevent inserting rows
            sheet.protection.delete_columns = False  # Prevent deleting columns
            sheet.protection.delete_rows = False  # Prevent deleting rows
            sheet.protection.sort = False  # Prevent sorting
            sheet.protection.auto_filter = False  # Disable auto filter
            sheet.protection.pivot_tables = False  # Disable pivot table changes

            # Save and return the protected Excel file
            workbook.save(response)
            return response  # Return the response to download the file

    work_sessions = WorkSession.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'work_sessions': work_sessions})

def user_logout(request):
    logout(request)
    return redirect('login')

import logging
from datetime import datetime
from django.http import JsonResponse

# Get the logger
logger = logging.getLogger('django')

def test_logging(request):
    logger.info("Test log message from Django.")
    return HttpResponse("Check work_sessions.log for the test message.")

# Get the custom logger
work_logger = logging.getLogger("worklog")

def start_work(request):
    user = request.user.username  # Assuming the user is logged in
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_message = f"{user} started working at {now}."
    work_logger.info(log_message)

    return JsonResponse({"message": "Work started", "timestamp": now})

def stop_work(request):
    user = request.user.username  # Assuming the user is logged in
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_message = f"{user} stopped working at {now}."
    work_logger.info(log_message)

    return JsonResponse({"message": "Work stopped", "timestamp": now})


