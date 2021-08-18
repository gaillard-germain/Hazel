# Hazel
Hazel is the result of my final project as part of my OpenClassRooms training as a Python developer.
## About
It is a django web application that I created for the recreation center in my town. It allows families to register their children directly on-line and the director (as an admin user) can display the bookings and access to the children's infos. Also, he can update some informations about the facility.
## Sources
The data relating to the holidays periods are from [data.education.gouv.fr](https://data.education.gouv.fr/explore/dataset/fr-en-calendrier-scolaire/api/?disjunctive.description&disjunctive.location&disjunctive.zones&disjunctive.annee_scolaire&disjunctive.population) API.
## Languages, libraries and frameworks
This web app was developed with **python 3** and the **Django** framework version 3.  
It use a [PostgreSQL](https://www.postgresql.org/) database.  
Dynamic part of the site use [JQuery](https://jquery.com/).  
Icones are from [Font Awesome](https://fontawesome.com/).  
All required python's libraries are in the requirements.txt file.
## In local mode
### Install
If you want to try it on localhost.
- Fake and clone the [hazel github's repository](https://github.com/screw-pack/hazel.git).
- Create a python 3 virtual environement.
- Install the required modules with `pip install -r requirements.txt`.
- Install [postgresql](https://www.postgresql.org/download/).
- Create a data base with it ([Official Documentation](https://www.postgresql.org/docs/)).
- Create a `.env` file to hazel/config/settings which contain:
  ```
  ENV='local'
  ```
- Create a `local.py` file to hazel/config/settings which contain:
  ```
  SECRET_KEY = <your secret key>

  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': <your DB name>,
        'USER': <your DB user>,
        'PASSWORD': <your DB password>,
        'HOST': 'localhost',
        'PORT': '',
    }
  }
  ```
- You may populate the periods table with a custom command `./manage.py get_holidays`.  
*the script for this command is in hazel/booking/management/commands/get_holidays.py, you can modify it as you wish.*
- To launch the server `./manage.py runserver`.
- Open your web browser at http://127.0.0.1:8000/
### Tests
Some tests are available: run `./manage.py test` to perform them.  
Note: You'll need [mozilla/geckodriver](https://github.com/mozilla/geckodriver/releases/) to perform Selenium test. Put it in the directory that is mentioned in the PATH environment variable. (`echo $PATH` on linux to display a list of all directories that are registered in the PATH variable.)
## Online
You can try it online at the following address: [128.199.53.172](http://128.199.53.172)
