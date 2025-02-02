from django.db import models

from django.db import models

class Continent(models.Model):
    CONTINENT_CHOICES = [
        ('Europe', 'Европа'),
        ('Africa', 'Африка'),
        ('Asia', 'Азия'),
        ('Oceania', 'Океания'),
        ('North_Central_America', 'Северная и Центральная Америка'),
        ('South_America', 'Южная Америка'),
    ]

    name = models.CharField(max_length=50, choices=CONTINENT_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()

class Federation(models.Model):
    short_name = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=100, unique=True)
    continent = models.OneToOneField(Continent, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name

class Language(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name="Код языка")
    name = models.CharField(max_length=100, unique=True, verbose_name="Название языка")

    def __str__(self):
        return self.name

class Country(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name="Код страны")
    short_name = models.CharField(max_length=100, unique=True, verbose_name="Краткое название страны")
    full_name = models.CharField(max_length=255, unique=True, verbose_name="Полное название страны")
    flag = models.URLField(verbose_name="Ссылка на флаг")
    description = models.TextField(verbose_name="Описание страны")
    federation = models.ForeignKey("Federation", on_delete=models.CASCADE, verbose_name="Федерация")
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name="Основной язык страны", related_name="countries")

    def __str__(self):
        return f"{self.full_name} ({self.language.name})"


class NationalFirstName(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Национальное имя")
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name="Язык", related_name="national_first_names")

    def __str__(self):
        return f"{self.first_name} ({self.language.name})"

class NationalLastName(models.Model):
    last_name = models.CharField(max_length=100, verbose_name="Национальная фамилия")
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name="Язык", related_name="national_last_names")

    def __str__(self):
        return f"{self.last_name} ({self.language.name})"
