from django.core.management.base import BaseCommand
from moviegram.models import Movie, Genre

class Command(BaseCommand):
    help = 'Import data from DAT file to MySQL database'

    def add_arguments(self, parser):
        parser.add_argument('dat_file', type=str, help='Path to the DAT file')

    def handle(self, *args, **kwargs):
        dat_file_path = kwargs['dat_file']
        self.import_data(dat_file_path)

    def import_data(self, file_path):
        with open(file_path, 'r', encoding="latin-1") as file:
            for line in file:
                fields = line.strip().split("::")
                if len(fields) == 3:
                    name = fields[1]
                    genres_list = fields[2].split("|")

                    genre_objects = []
                    for genre in genres_list:
                        genre_exist = Genre.objects.filter(name=genre).first()
                        if genre_exist:
                            genre_objects.append(genre_exist)
                        else:
                            new_genre = Genre.objects.create(name=genre)
                            genre_objects.append(new_genre)

                    movie = Movie.objects.create(name=name)
                    movie.genres.add(*genre_objects)

        self.stdout.write(self.style.SUCCESS('Movies data imported successfully'))
