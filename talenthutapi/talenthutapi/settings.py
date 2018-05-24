from talenthutapi.conf.dev import *

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
# MySQL setup
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'talenthut',
        'USER': 'root',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
"""

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
"""

# PostgreSQL setup
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'talenthutapi',
        'USER': 'postgres',
        'PASSWORD': 'T@ubeTech1720',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

"""
# Parse database configuration from $DATABASE_URL
import dj_database_url
# DATABASES['default'] =  dj_database_url.config()
#updated
DATABASES = {'default': dj_database_url.config(default='postgres://hwuztopkwbvgqm:75515684c3efee160c5f86f257fcb9fa0fe24ee086c475583878aa3b27f3813b@ec2-23-21-164-107.compute-1.amazonaws.com:5432/dfkujtbrsdnamt')}
"""

