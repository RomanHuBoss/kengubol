# запускать с использованием команды
# python manage.py populate_continents

from django.core.management.base import BaseCommand
from core.models import Continent

CONTINENTS = [
    "Европа",
    "Африка",
    "Азия",
    "Океания",
    "Северная и Центральная Америка",
    "Южная Америка",
]

class Command(BaseCommand):
    help = "Добавляет континенты в базу данных"

    def handle(self, *args, **kwargs):
        for name in CONTINENTS:
            continent, created = Continent.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Добавлен континент: {name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Континент уже существует: {name}'))

