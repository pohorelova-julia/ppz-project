from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Головна сторінка
    path('', views.event_list, name='event_list'),

    # Події
    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('events/<int:pk>/delete/', views.event_delete, name='event_delete'),

    # Коментарі та відповіді
    path('events/<int:event_pk>/comment/<int:comment_pk>/reply/', views.add_reply, name='add_reply'),
    path('comments/<int:pk>/delete/', views.delete_comment, name='delete_comment'),

    # Аутентифікація
    path('accounts/login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/register/', views.register, name='register'),

    # Адміністрування
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]