from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # URL для аутентифікації
    path('accounts/login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/register/', views.register, name='register'),

    # URL для подій
    path('', views.event_list, name='event_list'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/new/', views.event_create, name='event_create'),
    path('events/<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('events/<int:pk>/delete/', views.event_delete, name='event_delete'),

    # URL для коментарів
    path('comments/<int:pk>/delete/', views.comment_delete, name='comment_delete'),

    # URL для адміністратора - ось цей URL потрібно використовувати
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/users/<int:pk>/change-password/', views.change_user_password, name='change_user_password'),
]