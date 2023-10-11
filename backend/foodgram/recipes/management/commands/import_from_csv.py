import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredients


class Command(BaseCommand):
    help = 'Импорт данных из csv для модели Ingredients'

    def add_arguments(self, parser) -> None:
        parser.add_argument('--path', type=str, help="Путь к файлу")

    def handle(self, *args, **options):
        file_path = options['path'] + 'ingredients.csv'
        with open(file_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                try:
                    obj, created = Ingredients.objects.get_or_create(
                        name=row[0], measurement_unit=row[1])
                except Exception as error:
                    print(f'Ошибка в {row}:{error}')
