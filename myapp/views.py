from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test, login_required 
from django.shortcuts import redirect, render
from django.http import HttpResponse

from .models import ClientData
import pandas as pd
from datetime import datetime, date

from .models import ClientData, UserSubmits


def sales_dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'sales_dashboard.html', {'username': request.user.username, "dashboard_name": "Sales Dashboard"})
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                login(request, user)
                return redirect('sales_dashboard')
        else:
            return HttpResponse('Invalid username or password.')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@user_passes_test(lambda user: user.is_staff)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@user_passes_test(lambda user: user.is_staff)
def work_status(request):
    return render(request, 'work_status.html')

@user_passes_test(lambda user: user.is_staff)
def change_user(request):
    return render(request, 'change_user.html')

@login_required
def assigned_data(request):
    user = request.user.username
    data = ClientData.objects.filter(assigned_user=user)

    if request.method == "POST":
        # Get data from the form and save it to UserSubmits table
        for key, value in request.POST.items():
            if key.startswith("name_"):  # this identifies each row of data
                index = key.split('_')[1]
                name = request.POST.get(f'name_{index}')
                email = request.POST.get(f'email_{index}')
                phonenumber = request.POST.get(f'phonenumber_{index}')
                investigate_date = request.POST.get(f'investigate_date_{index}')
                schedule_date = request.POST.get(f'schedule_date_{index}')
                lead = request.POST.get(f'lead_{index}')
                response = request.POST.get(f'response_{index}')

                # Save to UserSubmits model
                UserSubmits.objects.create(
                    name=name,
                    email=email,
                    phonenumber=phonenumber,
                    investigate_date=investigate_date,
                    schedule_date=schedule_date,
                    lead=lead,
                    response=response,
                    assigned_user=request.user.username
                )

        return redirect('assigned_data')

    return render(request, 'assigned_data.html', {"data": data})

@login_required
def scheduled_calls(request):
    user = request.user.username
    today_date = date.today()
    data = UserSubmits.objects.filter(assigned_user=user, schedule_date=today_date).exclude(investigate_date=today_date)

    
    return render(request, 'scheduled_calls.html', {"data": data})

@user_passes_test(lambda user: user.is_staff)
def upload_file(request):
    if request.method == 'POST' and 'csv_file' in request.FILES:
        csv_file = request.FILES['csv_file']
        selected_users = request.POST.getlist('selected_users')

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file)
        
        # Convert 'Investigate_Date' and 'Schedule_Date' to the correct format
        df['Investigate_Date'] = pd.to_datetime(df['Investigate_Date'], format='%d-%m-%Y', errors='coerce')
        df['Schedule_Date'] = pd.to_datetime(df['Schedule_Date'], format='%d-%m-%Y', errors='coerce')
        
        # Add Timestamp column
        df['Timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Split the data based on the number of records specified for each user
        start_idx = 0
        for user in selected_users:
            num_records = int(request.POST.get(f'split_number_{user}', 0))
            
            if num_records > 0:
                # Get chunk of data for this user
                end_idx = start_idx + num_records if start_idx + num_records < len(df) else len(df)
                user_data = df.iloc[start_idx:end_idx]

                # Assign the user to each row in the chunk
                assigned_user = User.objects.get(username=user)
                for _, row in user_data.iterrows():
                    ClientData.objects.create(
                        name=row['Name'],
                        email=row['Email'],
                        phonenumber=row['phonenumber'],
                        investigate_date=row['Investigate_Date'].date() if pd.notnull(row['Investigate_Date']) else None,
                        schedule_date=row['Schedule_Date'].date() if pd.notnull(row['Schedule_Date']) else None,
                        lead=row['Lead'],
                        response=row['Response'],
                        assigned_user=assigned_user
                    )
                start_idx = end_idx

        return redirect('upload_file')

    users = User.objects.all()
    return render(request, 'upload_file.html', {'users': users})

