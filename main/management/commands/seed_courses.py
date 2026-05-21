from django.core.management.base import BaseCommand

from main.models import Course


class Command(BaseCommand):
    help = 'Создает начальные курсы для портала Пассажиры РФ'

    def handle(self, *args, **options):
        courses = [
            {
                'title': 'Курс водителя автобуса',
                'course_type': Course.BUS,
                'description': 'Очное обучение управлению автобусом для пассажирских перевозок в городе.',
                'duration_hours': 144,
            },
            {
                'title': 'Курс водителя электробуса',
                'course_type': Course.ELECTROBUS,
                'description': 'Подготовка водителей современного электрического пассажирского транспорта.',
                'duration_hours': 120,
            },
            {
                'title': 'Курс водителя трамвая',
                'course_type': Course.TRAM,
                'description': 'Очный курс по безопасному управлению трамваем на городских маршрутах.',
                'duration_hours': 160,
            },
        ]

        created = 0
        for course_data in courses:
            # Команда обновляет существующие курсы и не создает дубликаты.
            _, was_created = Course.objects.update_or_create(
                title=course_data['title'],
                defaults=course_data,
            )
            created += int(was_created)

        self.stdout.write(self.style.SUCCESS(f'Курсы готовы. Новых создано: {created}.'))
