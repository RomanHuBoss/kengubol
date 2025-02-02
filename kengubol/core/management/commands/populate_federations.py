# запускать с использованием команды
# python manage.py populate_federations

from django.core.management.base import BaseCommand
from core.models import Federation, Continent

FEDERATIONS = [
    ("КОНКАКАФ", "Конфедерация футбола Северной, Центральной Америки и стран Карибского бассейна", "Северная и Центральная Америка"),
    ("КОНМЕБОЛ", "Южноамериканская футбольная конфедерация", "Южная Америка"),
    ("УЕФА", "Союз европейских футбольных ассоциаций", "Европа"),
    ("КАФ", "Африканская конфедерация футбола", "Африка"),
    ("АФК", "Азиатская конфедерация футбола", "Азия"),
    ("ОФК", "Конфедерация футбола Океании", "Океания"),
]

class Command(BaseCommand):
    help = "Добавляет федерации в базу данных"

    def handle(self, *args, **kwargs):
        for short_name, full_name, continent_name in FEDERATIONS:
            try:
                continent = Continent.objects.get(name=continent_name)
                federation, created = Federation.objects.get_or_create(
                    short_name=short_name,
                    defaults={"full_name": full_name, "continent": continent},
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Добавлена федерация: {full_name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Федерация уже существует: {full_name}'))
            except Continent.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Ошибка: Континент "{continent_name}" не найден'))