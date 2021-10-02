
# Install PostgresSQL
sudo apt update \
sudo apt install postgresql postgresql-contrib

# Login to PSQL
sudo -i -u postgres \
psql

# Check listed users
\du

# Create User
CREATE USER admin_user WITH PASSWORD '@$!@123[45]';

# Grant Permission on table
alter user admin_user with superuser; \
alter user admin_user with login;

# Create Database
CREATE DATABASE icompaas;

# Exit and logout
\q
logout

# Install python3.8 if not installed already
sudo add-apt-repository ppa:deadsnakes/ppa \
sudo apt install python3.8

# Install virtualenv if not installed already
sudo apt install python3-pip

# Install and Create virtualenv
sudo apt install virtualenv \
virtualenv -p python3.8 venv

# Install serverless and dependencies
sudo apt install nodejs \
sudo apt install nodejs \
npm i

# Use the virtualenv
source venv/bin/activate

# Install requirement.txt
pip install -r requirements.txt

# Restore Backup in PostGres
psql xcpep < test.pgdump

# Apply Migrations
python manage.py makemigrations \
python manage.py migrate

# Runserver
serverless wsgi serve

# Create DB Backup in PostGres
sudo -u postgres pg_dump xcpep > test.pgdump
