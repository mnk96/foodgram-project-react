import csv

import os
from django.core.management.base import BaseCommand

from recipes.models import Ingredients


class Command(BaseCommand):
    help = 'Импорт данных из csv для модели Ingredients.'

    def handle(self, *args, **options):
        file_path = os.fspath('data/ingredients.csv')
        with open(file_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for name, measurement_unit in reader:
                try:
                    obj, created = Ingredients.objects.get_or_create(
                        name=name, measurement_unit=measurement_unit)
                except Exception as error:
                    print(f'Ошибка в {name}-{measurement_unit}:{error}')
