## Run the project
### Create virtual enviroment and install the dependencies
```bash
virtualenv -p python3.11 venv
source venv/bin/activate
poetry install
```

### Create Database and User (PostgreSQL)
```sql
CREATE DATABASE dzmo_db;
CREATE USER dzmo_user WITH PASSWORD 'dzmo_password';
GRANT ALL PRIVILEGES ON DATABASE dzmo_db TO dzmo_user;
```

### Run migrations
```bash
python manage.py migrate
```

### Run server
```bash
python manage.py runserver
```

## Development
### Code formatting
We use *black* for code formatting.

