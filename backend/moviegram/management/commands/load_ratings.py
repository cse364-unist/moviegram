from django.core.management.base import BaseCommand
from django.db import transaction
from moviegram.models import Movie, Rate
from django.contrib.auth.models import User
from multiprocessing import Pool, cpu_count
import time


def process_line(line):
    fields = line.strip().split("::")
    if len(fields) == 4:
        user_id = int(fields[0])
        movie_id = int(fields[1])
        rating_given = int(fields[2])

        try:
            user = User.objects.get(pk=user_id)
            movie = Movie.objects.get(pk=movie_id)
        except:
            return

        # Update movie rating
        total_people_rated = movie.total_people_rated + 1
        rating_sum = movie.rating_sum + rating_given
        movie.average_rating = rating_sum / total_people_rated
        movie.total_people_rated = total_people_rated
        movie.rating_sum = rating_sum
        movie.save()

        # Save rating instance
        rating = Rate.objects.create(
            user=user, movie=movie, rate=rating_given)


class Command(BaseCommand):
    help = 'Import data from DAT file to MySQL database'

    def add_arguments(self, parser):
        parser.add_argument('dat_file', type=str, help='Path to the DAT file')

    def handle(self, *args, **kwargs):
        pool = Pool(cpu_count())
        dat_file_path = kwargs['dat_file']
        with open(dat_file_path, 'r', encoding="latin-1") as file:
            lines = file.readlines()
            pool.map(process_line, lines)

        self.stdout.write(self.style.SUCCESS(
            'Ratings data imported successfully'))
