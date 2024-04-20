from django.core.management.base import BaseCommand
from moviegram.models import Movie

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
                if len(fields) == 4:
                    user_id = int(fields[0])
                    movie_id = int(fields[1])
                    rating_given = int(fields[2]) 

                    try: 
                        movie = Movie.objects.get(pk=movie_id)
                    except: 
                        continue 
                    
                    if movie: 
                        total_people_rated = movie.total_people_rated + 1
                        rating_sum = movie.rating_sum + rating_given
                        movie.average_rating = rating_sum / total_people_rated
                        movie.total_people_rated = total_people_rated
                        movie.rating_sum = rating_sum
                        movie.save() 

        self.stdout.write(self.style.SUCCESS('Ratings data imported successfully'))
