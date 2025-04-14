""" Project initialization '"""

import os
import django
from django.core.management import call_command
from colorama import init, Fore, Style

init(autoreset=True)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

DATABASE_NAME = 'news_now_database'
DJANGO_SETTINGS_FILENAME = 'config'
APPLICATIONS = ['website_info', 'users', 'news']


def database_creations():
    from psycopg2 import connect, errors, OperationalError

    try:
        db_connect = connect(host='localhost',
                                user='postgres',
                                port='5432',
                                password='1111')
        db_connect.autocommit = True
    except OperationalError:
        print(Fore.RED + f'Postgres server connection error!\n')
        return False
    else:
        db_cursor = db_connect.cursor()

        try:
            db_cursor.execute(f'create database {DATABASE_NAME};')
        except errors.ObjectInUse:
            print(Fore.RED + f"Database in use!")
            return False
        except errors.DuplicateDatabase:
            try:
                print(f'Database already exist')
                db_cursor.execute(f'drop database {DATABASE_NAME};')
                print('Database successfully deleted')
                db_cursor.execute(f'create database {DATABASE_NAME};')
                print(f'Database `{DATABASE_NAME}` has been created')
            except errors.ObjectInUse:
                print(Fore.RED + f"Database in use!")
                return False
            else:
                return True
        else:
            print(f'Database `{DATABASE_NAME}` has been created')
            return True


def database_migrations():
    from django.db import connections
    from django.db.utils import OperationalError

    try:
        connections['default'].cursor()
    except OperationalError:
        return False
    else:
        for application in APPLICATIONS:
            try:
                files_list = os.listdir(f'{application}/migrations')

                for file in files_list:
                    if file != '__init__.py' and file != '__pycache__':
                        os.remove(f'{application}/migrations/{file}')

                call_command("makemigrations")
                call_command("migrate")
                print()
            except OperationalError:
                return False
    return True


def upload_test_data():
    from django.core .serializers.base import DeserializationError
    from users.models import CustomUser

    try:
        call_command('loaddata', 'website_information_fixture.json')
        call_command('loaddata', 'users_fixture.json')
        call_command('loaddata', 'news_categories_fixture.json')
        call_command('loaddata', 'news_fixture.json')
        call_command('loaddata', 'favorite_news_fixture.json')
        call_command('loaddata', 'comments_fixture.json')
        call_command('loaddata', 'reactions_fixture.json')

        for user in CustomUser.objects.all():  # hash test user passwords
            user.set_password(user.password)
            user.save()

        return True
    except DeserializationError:
        return False


def starting_initialization_modules():
    if not database_creations():
        print(Fore.RED + Style.BRIGHT + 'Database initialization failed!')
    else:
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'Database initialization successful!\n\n')
        if not database_migrations():
            print(Fore.RED + Style.BRIGHT + 'Database migrations failed!')
        else:
            print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'Database migrations successful!\n\n')
            if not upload_test_data():
                print(Fore.RED + Style.BRIGHT + 'Test data upload failed!')
            else:
                print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'Test data upload successful!\n')


if __name__ == '__main__':
    starting_initialization_modules()
