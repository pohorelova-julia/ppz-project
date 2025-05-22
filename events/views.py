from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Event, Comment
from .forms import EventForm, CommentForm, UserPasswordChangeForm, CustomUserCreationForm

def is_admin(user):
    return user.is_superuser

def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    comments = event.comments.all()

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.event = event
            comment.author = request.user
            comment.save()
            messages.success(request, 'Ваш коментар додано.')
            return redirect('event_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'events/event_detail.html', {
        'event': event,
        'comments': comments,
        'form': form
    })

@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, 'Подію успішно створено!')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()

    return render(request, 'events/event_form.html', {'form': form, 'action': 'Створити'})

@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)

    # Check if user is the organizer or an admin
    if request.user != event.organizer and not request.user.is_superuser:
        messages.error(request, 'Ви не маєте дозволу редагувати цю подію.')
        return redirect('event_detail', pk=pk)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Подію успішно оновлено!')
            return redirect('event_detail', pk=pk)
    else:
        form = EventForm(instance=event)

    return render(request, 'events/event_form.html', {'form': form, 'action': 'Редагувати'})

@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)

    # Check if user is the organizer or an admin
    if request.user != event.organizer and not request.user.is_superuser:
        messages.error(request, 'Ви не маєте дозволу на видалення цієї події.')
        return redirect('event_detail', pk=pk)

    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Подію успішно видалено!')
        return redirect('event_list')

    return render(request, 'events/event_confirm_delete.html', {'event': event})

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    event_pk = comment.event.pk

    if request.user != comment.author and not request.user.is_superuser:
        messages.error(request, 'У вас немає прав для видалення цього коментаря.')
        return redirect('event_detail', pk=event_pk)

    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Коментар успішно видалено!')

    return redirect('event_detail', pk=event_pk)

@user_passes_test(is_admin)
def admin_dashboard(request):
    users = User.objects.all()
    events = Event.objects.all()
    comments = Comment.objects.all()

    return render(request, 'admin/dashboard.html', {
        'users': users,
        'events': events,
        'comments': comments
    })

@user_passes_test(is_admin)
def change_user_password(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = UserPasswordChangeForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            messages.success(request, f'Password for {user.username} changed successfully!')
            return redirect('admin_dashboard')
    else:
        form = UserPasswordChangeForm()

    return render(request, 'admin/change_password.html', {'form': form, 'user': user})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Обліковий запис успішно створено! Тепер ви можете увійти.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'auth/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('event_list')