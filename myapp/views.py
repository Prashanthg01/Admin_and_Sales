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
from datetime import datetime


def home_view(request):
    if request.user.is_authenticated:
        return render(request, 'home.html', {'username': request.user.username})
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:  # Check if the user is authenticated
            if user.is_staff:  # Check if the user has admin privileges
                login(request, user)
                return redirect('dashboard')  # Redirect to the Dashboard page for admin users
            else:
                login(request, user)
                return redirect('home')  # Redirect to the Home page for regular users
        else:
            return HttpResponse('Invalid username or password.')  # Error message for invalid credentials

    return render(request, 'login.html')

# def register_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         if User.objects.filter(username=username).exists():
#             return HttpResponse('Username already exists.')
#         user = User.objects.create_user(username=username, password=password)
#         user.save()
#         return redirect('login')
#     return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@user_passes_test(lambda user: user.is_staff)  # Restrict access to admin users
def dashboard_view(request):
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
                start_idx = end_idx  # Update the start index for the next user

        return redirect('dashboard')  # Redirect to dashboard after processing

    users = User.objects.all()
    return render(request, 'dashboard.html', {'users': users})