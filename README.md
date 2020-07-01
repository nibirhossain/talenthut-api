# Talent Hut - IT Professionals Hiring Software

An online application helps the companies to recruit the competitive IT professionals.

## Getting Started

### Prerequisites

Install Python >=3.6, virtualenv and create and activate virtualenv for the project


### Installing required packages

To install the required packages, execute the following command into 

```
pip install -r requirements.txt
```

### Setting up Database

Before running the application you need to create a Database into Postgresql named 'talenthut' manually and change the database information in settings.py file

PostgreSQL setup
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'talenthut',
        'USER': 'postgres',
        'PASSWORD': 'your_db_pass',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

```
"""
import dj_database_url
DATABASES = {'default': dj_database_url.config(default='postgres://hwuztopkwbvgqm:75515684c3efee160c5f86f257fcb9fa0fe24ee086c475583878aa3b27f3813b@ec2-23-21-164-107.compute-1.amazonaws.com:5432/dfkujtbrsdnamt')}
"""
```

Now execute the following command to create necessary DB tables:

```
python manage.py migrate
```

### Loading initial data

Find the json file in the root directory and execute the following command.

```
python manage.py loaddata initial_data.json
```

### Running the application

Now you can run the development web server:

```
python manage.py runserver
```

To access the application, go to the URL http://localhost:8000/
