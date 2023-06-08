import json

from django.core.management.base import BaseCommand

from api.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        """
        Для импорта файлов .json:
        1. Удалите файл db.sqlite3 если он уже существует
        Если этот файл содержит важные данные, создать резервную копию.
        2. Выполните команду: python manage.py migrate --run-syncdb
        Будет создан новый файл БД с пустыми таблицами.
        3. Выполнитет команду: python manage.py import_files_json
        Будет произведен импорт .json файлов в БД.
        В случае необходимости повторного импорта повторите операции
        начиная с пункта 1.
        """
        print('Начинаю импорт файла')

        with open(('D:\\Dev\\foodgram-project-react\\data\\ingredients.json'),
                  'r', encoding='utf-8') as json_file:

            datareader = json.load(json_file)
            for row in datareader:
                data = Ingredient(name=row['name'],
                                  measurement_unit=row['measurement_unit'])

                data.save()
            print('Файл успешно импортирован')
        print('Импорт данных окончен')
