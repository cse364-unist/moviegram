# Start MySQL server and create a moviegram database
service mysql start
sleep 5
mysql -uroot -pasdf -e "CREATE DATABASE IF NOT EXISTS moviegram;"

# Clone the git repository
git clone https://github.com/cse364-unist/moviegram.git
cd moviegram

pip install --upgrade pip
pip install -r requirements.txt
git checkout milestone2 
cd backend
python3 manage.py makemigrations
python3 manage.py migrate

# Populate database with initial data. Change later to have sql snapshot only 
python3 manage.py load_movies moviegram/management/data/movies.dat
# python3 manage.py load_ratings moviegram/management/data/real_ratings.dat #Taking too much time 

# Run the server
python3 manage.py runserver