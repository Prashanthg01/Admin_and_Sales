from django.urls import path
from . import views

urlpatterns = [
    path('sales_dashboard', views.sales_dashboard, name='sales_dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('work_history/', views.work_history, name='work_history'),
    path('change_user/', views.change_user, name='change_user'),
    path('scheduled_calls/', views.scheduled_calls, name='scheduled_calls'),
    path('assigned_data/', views.assigned_data, name='assigned_data'),
    path('review_work/', views.review_work, name='review_work'),
]
