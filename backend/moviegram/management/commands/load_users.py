from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from multiprocessing import Pool, cpu_count
import time


def create_user(username):
    User.objects.create_user(username=username)


class Command(BaseCommand):
    help = 'Create 6040 user accounts with fake usernames and password "asdf"'

    def handle(self, *args, **kwargs):
        pool = Pool(cpu_count())  # Create a multiprocessing Pool
        usernames = self.generate_users()  # Generate unique usernames
        start = time.perf_counter()

        pool.map(create_user, usernames)  # Create users in parallel

        print(f'Duration = {time.perf_counter()-start}')

        self.stdout.write(self.style.SUCCESS(
            '6040 users created successfully'))


    def generate_users(self):
        faker = Faker()
        usernames = set()
        while len(usernames) < 6040:
            usernames.add(faker.user_name())
        return list(usernames)
