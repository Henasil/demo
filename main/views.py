from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ApplicationForm, CourseReviewForm, LoginForm, RegisterForm
from .models import Application


ADMIN_USERNAME = 'Admin26'


def index(request):
    if request.user.is_authenticated:
        return redirect('profile')
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно. Теперь войдите в систему.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('admin_panel' if request.user.username == ADMIN_USERNAME else 'profile')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        if user is None:
            messages.error(request, 'Неверный логин или пароль')
        else:
            login(request, user)
            return redirect('admin_panel' if user.username == ADMIN_USERNAME else 'profile')

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    applications = (
        Application.objects
        .filter(user=request.user)
        .select_related('course')
        .prefetch_related('review')
    )
    return render(request, 'profile.html', {'applications': applications})


@login_required
def create_application_view(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            # Пользователь заполняет только курс, дату, время и оплату; статус ставится автоматически.
            application = form.save(commit=False)
            application.user = request.user
            application.status = Application.NEW
            application.save()
            messages.success(request, 'Заявка создана и получила статус «Новое».')
            return redirect('profile')
    else:
        form = ApplicationForm()

    return render(request, 'create_application.html', {'form': form})


@login_required
def review_view(request, application_id):
    application = get_object_or_404(Application, pk=application_id, user=request.user)
    # Отзыв открывается только после перевода заявки в статус завершенного обучения.
    if application.status != Application.COMPLETED:
        messages.error(request, 'Оставить отзыв можно только после завершения обучения.')
        return redirect('profile')
    if hasattr(application, 'review'):
        messages.info(request, 'Отзыв по этой заявке уже оставлен.')
        return redirect('profile')

    if request.method == 'POST':
        form = CourseReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.application = application
            review.save()
            messages.success(request, 'Спасибо! Ваш отзыв сохранен.')
            return redirect('profile')
    else:
        form = CourseReviewForm()

    return render(request, 'review.html', {'form': form, 'application': application})


def admin_required(view_func):
    # Перед открытием дашборда проверяем, что вошел именно демонстрационный администратор.
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.username != ADMIN_USERNAME:
            messages.error(request, 'Доступ разрешен только администратору.')
            return redirect('profile')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def admin_panel_view(request):
    if request.method == 'POST':
        application = get_object_or_404(Application, pk=request.POST.get('application_id'))
        new_status = request.POST.get('status')
        valid_statuses = [status[0] for status in Application.STATUS_CHOICES]
        if new_status in valid_statuses:
            application.status = new_status
            application.save(update_fields=['status'])
            messages.success(request, f'Статус заявки #{application.id} изменен.')
        else:
            messages.error(request, 'Передан некорректный статус.')
        return redirect(f"{request.path}?{request.GET.urlencode()}")

    status_filter = request.GET.get('status', '')
    sort = request.GET.get('sort', 'desc')

    applications = Application.objects.select_related('user', 'user__profile', 'course')
    if status_filter:
        # Администратор может оставить в таблице заявки только с выбранным статусом.
        applications = applications.filter(status=status_filter)
    applications = applications.order_by('created_at' if sort == 'asc' else '-created_at')

    paginator = Paginator(applications, 6)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'status_choices': Application.STATUS_CHOICES,
        'status_filter': status_filter,
        'sort': sort,
    }
    return render(request, 'admin_panel.html', context)
