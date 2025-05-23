from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import Event, Comment
from .forms import EventForm, CustomUserCreationForm, CommentForm, ReplyForm


def event_list(request):
    events = Event.objects.all().order_by('-created_at')
    return render(request, 'events/event_list.html', {'events': events})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    comments = Comment.objects.filter(event=event, parent=None).order_by('created_at')

    # Форма для нового коментаря
    if request.method == 'POST' and 'comment_submit' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid() and request.user.is_authenticated:
            new_comment = comment_form.save(commit=False)
            new_comment.event = event
            new_comment.author = request.user
            new_comment.save()
            messages.success(request, 'Коментар додано успішно!')
            return redirect('event_detail', pk=event.pk)
    else:
        comment_form = CommentForm()

    # Форма для відповіді на коментар
    reply_form = ReplyForm()

    context = {
        'event': event,
        'comments': comments,
        'comment_form': comment_form,
        'reply_form': reply_form,
    }
    return render(request, 'events/event_detail.html', context)


@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, 'Подію створено успішно!')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()
    # Використовуємо спільний шаблон event_form.html
    return render(request, 'events/event_form.html', {'form': form})


@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user != event.organizer and not request.user.is_superuser:
        messages.error(request, 'У вас немає прав для редагування цієї події.')
        return redirect('event_detail', pk=pk)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Подію оновлено успішно!')
            return redirect('event_detail', pk=pk)
    else:
        form = EventForm(instance=event)
    # Використовуємо спільний шаблон event_form.html і передаємо event для розрізнення
    return render(request, 'events/event_form.html', {'form': form, 'event': event})


@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user != event.organizer and not request.user.is_superuser:
        messages.error(request, 'У вас немає прав для видалення цієї події.')
        return redirect('event_detail', pk=pk)

    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Подію видалено успішно!')
        return redirect('event_list')
    # Використовуємо шаблон для підтвердження видалення
    return render(request, 'events/event_confirm_delete.html', {'event': event})


@login_required
def add_reply(request, event_pk, comment_pk):
    event = get_object_or_404(Event, pk=event_pk)
    parent_comment = get_object_or_404(Comment, pk=comment_pk)

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.event = event
            reply.author = request.user
            reply.parent = parent_comment
            reply.save()
            messages.success(request, 'Відповідь додано успішно!')

    return redirect('event_detail', pk=event_pk)


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    event_pk = comment.event.pk

    # Перевірка, чи користувач є автором коментаря або адміністратором
    if request.user == comment.author or request.user.is_superuser:
        comment.delete()
        messages.success(request, 'Коментар видалено успішно!')
    else:
        messages.error(request, 'У вас немає прав для видалення цього коментаря.')

    return redirect('event_detail', pk=event_pk)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Реєстрацію завершено успішно!')
            return redirect('event_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})


def admin_dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, 'У вас немає прав доступу до цієї сторінки.')
        return redirect('event_list')

    events = Event.objects.all().order_by('-created_at')
    comments = Comment.objects.all().order_by('-created_at')

    context = {
        'events': events,
        'comments': comments,
    }
    return render(request, 'admin/dashboard.html', context)


# Власне представлення для виходу з системи
def logout_view(request):
    logout(request)
    messages.success(request, 'Ви успішно вийшли з системи.')
    return redirect('event_list')
