from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField('ФИО', max_length=150)
    phone = models.CharField('Телефон', max_length=30)
    email = models.EmailField('E-mail')

    def __str__(self):
        return self.full_name


class Course(models.Model):
    BUS = 'Вождение автобуса'
    ELECTROBUS = 'Вождение электробуса'
    TRAM = 'Вождение трамвая'

    COURSE_TYPES = [
        (BUS, BUS),
        (ELECTROBUS, ELECTROBUS),
        (TRAM, TRAM),
    ]

    title = models.CharField('Название', max_length=100)
    course_type = models.CharField('Тип курса', max_length=40, choices=COURSE_TYPES)
    description = models.TextField('Описание')
    duration_hours = models.PositiveIntegerField('Длительность, часов')

    def __str__(self):
        return self.title


class Application(models.Model):
    # Заявка проходит путь от подачи пользователем до завершения обучения.
    NEW = 'Новое'
    IN_PROGRESS = 'Идет обучение'
    COMPLETED = 'Обучение завершено'

    STATUS_CHOICES = [
        (NEW, NEW),
        (IN_PROGRESS, IN_PROGRESS),
        (COMPLETED, COMPLETED),
    ]

    CARD = 'Банковская карта'
    CASH = 'Наличные'
    TRANSFER = 'Банковский перевод'

    PAYMENT_CHOICES = [
        (CARD, CARD),
        (CASH, CASH),
        (TRANSFER, TRANSFER),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications', verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='applications', verbose_name='Название курса')
    start_date = models.DateField('Дата начала обучения')
    start_time = models.TimeField('Время начала обучения')
    payment_method = models.CharField('Способ оплаты', max_length=30, choices=PAYMENT_CHOICES)
    status = models.CharField('Статус', max_length=40, choices=STATUS_CHOICES, default=NEW)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Заявка #{self.pk} - {self.user.username}'


class CourseReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name='Пользователь')
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='review', verbose_name='Заявка')
    text = models.TextField('Текст отзыва')
    rating = models.PositiveSmallIntegerField('Оценка')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Отзыв {self.rating}/5 от {self.user.username}'
