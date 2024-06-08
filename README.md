# `Aubouleau` project

This repository contains the code of the `Aubouleau` project. As of now, the project is only made of one `django` application: `aubouleau_web`, which contains the code of the [aubouleau.fr](https://aubouleau.fr) web application.

The `Aubouleau` project allows students of ISEP to visualize various information regarding rooms and equipment available in the different ISEP facilities.
This project also allows ISEP personnel to manage the content displayed on the web application as well as visualizing different problems that may have been reported by the students.

## Development

To start developing on this project, start by cloning this repository.

### Setting up the local development database

To start developing using a local database, perform the following operations:
- [Install MariaDB](https://mariadb.org/download/?t=repo-config)
- Create a new database named `aubouleau`
- Create a new user with all privileges on the `aubouleau` database

### Setting up environment variables

Different sensitive and environment-dependent variables are populated using a `.env` file that is not commited to this repository.
In order to start developing on the project, create a `.env` file at the root of this project using the following template:
```properties
# Set to 0 to disable Debug mode (the Django webserver will NOT serve static files !)
DEBUG=1
# Generate your own SECRET_KEY and do not share it !
# (See: https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-SECRET_KEY)
SECRET_KEY=[a secure string]
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
CSRF_TRUSTED_ORIGINS=http://localhost http://127.0.0.1
# Change the database backend to fit your needs
DB_ENGINE=django.db.backends.mysql
# Change the database settings to fit your needs
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=aubouleau
DB_USERNAME=[name of the database user]
DB_PASSWORD=[password of the database user]
# Hyperplanning
HP_USERNAME=[Hyperplanning username]
# HP_PASSWORD must be in base64 ! (make sure NOT to include the newline character)
HP_PASSWORD=[Hyperplanning password in base64]
```

### Setting up `tailwindcss`

The user interface (UI) uses [tailwindcss](https://tailwindcss.com/) and [Flowbite](https://flowbite.com/), which are provided though `npm`. You can install these dependencies by first installing `nodejs` and `npm` and then typing:
```shell
npm install
```

Once the dependencies have been installed, you can instruct `tailwindcss` to watch for changes in Django templates so that it dynamically generates the `style.css` file, which contains the entire styling of the web application:
```shell
npx tailwindcss -i aubouleau_web/static/aubouleau_web/input.css -o aubouleau_web/static/aubouleau_web/style.css --watch
```

## Deployment

As of now, the application can be deployed as a `Docker Compose` stack. The provided `docker-compose.yml` allows the creation of multiple containers that include everything needed to deploy the `Aubouleau` web application:
- A `gunicorn` container, which hosts the `aubouleau_web` django application
- A `mariadb` container, which is the backend database used by `Aubouleau`
- A `phpmyadmin` container, which is a web interface for `MariaDB`
- An `NGINX` container, which proxies requests to `gunicorn` as well as serving static content.

If you haven't done it already, [install Docker](https://docs.docker.com/engine/install/). Refer to the linked documentation for the installation instructions specific to your distribution.

To create the `Docker Compose` stack, simply run the following command in a terminal:
```shell
sudo docker compose up -d --build
```

The following ports will be exposed on the host machine :

- `8888`: `NGINX`. To access the application, open http://localhost:8888 in your browser.
- `5080`: `phpmyadmin`. To access the `phpmyadmin` web interface, open http://localhost:5080 in your browser. You will be able to log in using the user account declared in `docker-compose.yml`.

To completely delete the stack and remove all created containers, run the following command in a terminal:
```shell
sudo docker compose down
```

**NB: In order to preserve the data when redeploying the application later, make sure to set the `INITIAL_DEPLOY` parameter to `false` in the `docker-compose.yml` file !**

### Uninstallation

If you want to undeploy the application as well as deleting all its data, run the following command:
```shell
sudo docker compose down -v --remove-orphans
```

If you wish to remove the images pulled and created by `Aubouleau`, run the following command in a terminal:
```shell
sudo docker image rm aubouleau-web:1.0 phpmyadmin:5.2.1 mariadb:11.3.2 nginx:1.26.0
```
