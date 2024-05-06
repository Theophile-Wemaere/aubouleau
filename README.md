# aubouleau.fr codebase

This repository is the codebase for the [aubouleau.fr](https:/aubouleau.fr) web application.

It's a webapp allowing ISEP students to find and manage availables rooms and equipments inside ISEP buildings.

### How to run

For now it's just a dummy django application, and will evolve in time
The dockers containers (mariadb, django server and phpmyadmin) can be runned with :
```shell
$ docker-compose up --build
```

it will expose the following ports :

- 5050 -> gunicorn server with the main webapp
- 5080 -> phpmyadmin server
- 3306 -> mysql server