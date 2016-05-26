1. Install pre-requisites
=========================

Virtualenv
----------
Standard installation with virtualevnwrapper.

PostgreSQL
----------
Standard installation.

Redis server
------------
Standard installation.



# Standard project initialization
## 1. Create virtual environment


1. Clone repository: ``git clone https://bitbucket.org/razortheory/iwg_blog.git``
2. Create virtual environment: ``mkvirtualenv iwg_blog``
3. Install requirements ``pip install -r requirements/dev.txt``
4. Edit ``$VIRTUAL_ENV/bin/postactivate`` to contain the following lines:

        export DATABASE_URL=your_psql_url
        export DEV_ADMIN_EMAIL=your_email

5. Deactivate and re-activate virtualenv:

        deactivate
        workon iwg_blog


## 2. Database

1. Create database table:

        psql -Uyour_psql_user
        CREATE DATABASE iwg_blog;

2. Migrations: ``./manage.py migrate``
3. Create admin: ``./manage.py createsuperuser``
4. Run the server ``./manage.py runserver``


# Alternative project initialization

1. Clone repository: ``git clone https://bitbucket.org/razortheory/iwg_blog.git``
2. Execute the following command to setup database credentials:

        echo DATABASE_URL=your_psql_url >> env.config
        
3. **Make sure that you are not in any of existing virtual envs**
4. run ``./initproject.bash`` - will run all commands listed in standard initialization, including edition of postactivate
5. activate virtualenv ``workon iwg_blog``
6. run ``./manage.py runserver``

