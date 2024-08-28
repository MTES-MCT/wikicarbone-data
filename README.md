# Ecobalyse data

Ce dépôt contient les scripts (principalement python) utilisés pour
importer et exporter les données du projet [Ecobalyse](https://github.com/MTES-MCT/ecobalyse).


### Backend

    $ pipenv install

Assurez-vous d'avoir un PostgreSQL >=16 qui tourne localement si vous souhaitez vous rapprocher de l'environnement de production. À défaut, `sqlite` sera utilisé.

Pour créer et lancer un PostgreSQL sur le port 5433 en local en utilisant `docker` :

    # Création du volume pour persister les données
    docker volume create ecobalyse_postgres_data

    # Lancement du docker postgres 16
    docker run --name ecobalyse-postgres -e POSTGRES_PASSWORD=password -d -p 5433:5432 -v ecobalyse_postgres_data:/var/lib/postgresql/data postgres:16

    # Création de la base de données ecobalyse_dev
    docker exec -it ecobalyse-postgres createdb -U postgres ecobalyse_dev

Vous devriez pouvoir y accéder via votre `psql` local avec la commande suivante :

    psql -U postgres -p 5433 -h localhost ecobalyse_dev

## Configuration

Les variables d'environnement suivantes doivent être définies :

- `BACKEND_ADMINS` : la liste des emails des administrateurs initiaux, séparés par une virgule
- `DEFAULT_FROM_EMAIL` : l'email utilisé comme origine pour les mails liés à l'authentification (par défaut ecobalyse@beta.gouv.fr)
- `DJANGO_DEBUG`: la valeur du mode DEBUG de Django (par défaut `True`)
- `DJANGO_SECRET_KEY` : la [clé secrète de Django](https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-SECRET_KEY)
- `ECOBALYSE_DATA_DIR`: l'emplacement du dépôt de données détaillées sur le système de fichier. Note: à terme, cette valeur deviendra optionnelle pour autoriser un fonctionnement en mode restreint.
- `EMAIL_HOST` : le host SMTP pour envoyer les mail liés à l'authentification
- `EMAIL_HOST_USER`: l'utilisateur du compte SMTP
- `EMAIL_HOST_PASSWORD` : le mot de passe du compte SMTP pour envoyer les mail liés à l'authentification

En développement, copiez le fichier `.env.sample`, renommez-le `.env`, et mettez à jour les valeurs qu'il contient ; le serveur de développement node chargera les variables en conséquences.

## Chargement des données par défaut

Pour initialiser la base de données (attention, toutes les données présentes, si il y en a, seront supprimées) :

    $ pipenv run ./backend/update.sh



Comment générer les données json utilisées par le frontal elm :

# Avec docker

- Installez `docker` et `make`
- Si vous êtes sur Mac avec architecture ARM, affectez 6Go de RAM à Docker dans Docker Desktop :
  Settings → Ressources → Advanced → Memory = 6G
- Préparez les bases de données à importer, elle ne font pas partie du dépôt :
  - Agribalyse : compressé dans un fichier `AGB3.1.1.20230306.CSV.zip` dans ce dossier data/
  - Ecoinvent : décompressé dans un dossier `ECOINVENT3.9.1` dans ce même dossier
- Lancez **`make`** ce qui va successivement :
  - construire l'image docker
  - importer agribalyse et EF 3.1 adapted dans un projet `food` de Brightway
  - importer ecoinvent et EF 3.1 adapted dans un projet `textile` de Brightway
  - exporter les données json utilisées côté front-end

Le processus entier prend environ 1h. En cas de problème vous pouvez redémarrer de zéro en faisant
d'abord un `make clean_data` (qui supprime le volume docker).

## Autres commandes :

- `make image` : pour construire l'image docker choisie
- `make import_agribalyse` : pour importer Agribalyse 3.1.1 dans Brightway (projet food).
  Assurez-vous d'avoir le fichier `AGB3.1.1.20230306.CSV.zip` dans le dossier `data/`
- `make import_food_method` : pour importer EF 3.1 adapted dans Brightway (projet food).
  Assurez-vous d'avoir le fichier `Environmental Footprint 3.1 (adapted).CSV` dans le dossier
  `data/`
- `make import_textile_method` : pour importer EF 3.1 adapted dans Brightway (projet textile).
  Assurez-vous d'avoir le fichier `Environmental Footprint 3.1 (adapted).CSV` dans le dossier
  `data/`
- `make import_ecoinvent` : pour importer Ecoinvent 3.9.1. Brightway (projet textile). Assurez-vous
  d'avoir le dossier `ECOINVENT3.9.1/` dans le dossier `data/`
- `make export_food` : pour exporter les json pour le builder alimentaire
- `make compare_food` : pour exporter des PNG pour chaque procédé montrant les différences entre Brightway et SimaPro
- `make export_textile` : pour exporter les json pour le builder textile
- `make delete_textile_method` : pour supprimer la méthode utilisée dans le projet textile
- `make json` : lance toutes les commandes précédentes dans l'ordre
- `make shell` : lance un shell bash à l'intérieur du conteneur
- `make python` : lance un interpréteur Python à l'intérieur du conteneur
- `make jupyter_password` : définit le mot de passe jupyter. Doit être lancé avant son démarrage.
- `make root_shell` : lance un shell root à l'intérieur du conteneur
- `make jupyter_password` : pour définir le mot de passe de Jupyter avant de le lancer
- `make start_notebook` : lance le serveur Jupyter dans le conteneur
- `make stop_notebook` : arrête le serveur Jupyter donc aussi le conteneur
- `make clean_data` : supprime toutes les données (celles de brightway et jupyter mais pas les json
  générés)
- `make clean_image` : supprime l'image docker
- `make clean` : lance `clean_data` et `clean_image`

## Travailler dans le conteneur :

Vous pouvez entrer dans le conteneur avec `make shell`.

Toutes les données du conteneur, notamment celles de Brightway et de Jupyter, sont dans
`/home/jovyan` qui est situé dans un volume docker (`/var/lib/docker/volume/jovyan` sur le _host_).
Le dépôt git ecobalyse se retrouve (via un bind mount) aussi à l'intérieur du conteneur dans
`/home/jovyan/ecobalyse`. Les fichiers json générés arrivent directement sur place au bon endroit
pour être comparées puis commités.

## Lancer le serveur Jupyter de dev

Avant de lancer Jupyter vous pouvez définir son mot de passe avec `make jupyter_password`. Ensuite
vous le démarrez avec `make start_notebook`.

## Lancer le serveur Jupyter pour l'éditeur d'ingrédients

Avant de lancer Jupyter vous pouvez définir son mot de passe avec `make jupyter_password`. Ensuite
vous le démarrez avec `JUPYTER_PORT=8889 make start_notebook`.

## Lancer l'explorateur Brightway

Créez un notebook dans Jupyter puis tapez `import notebooks.explore`, puis shift-Enter

## Lancer l'éditeur de procédés/ingrédients

Créez un notebook dans Jupyter puis tapez `import notebooks.ingredients`, puis shift-Enter

## Remarques

Si l'`export` prend plus de 2 secondes par procédé, c'est un problème d'installation de `pypardiso`
ou de la bibliothèque `mkl` (Math Kernel Library d'Intel) ou une incompatibilité avec l'architecture
CPU utilisée. Dans ce cas c'est le solveur de Scipy qui est utilisé. Il est possible que cela
explique les très légères différences d'arrondi rencontrées dans les résultats.
