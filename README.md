# Ecobalyse data

Ce dépôt contient les scripts (principalement python) utilisés pour
importer et exporter les données du projet [Ecobalyse](https://github.com/MTES-MCT/ecobalyse).

Ces scripts se trouvent dans `data/`, et un fichier [README](data/README.md) spécifique
en détaille l'installation et l'utilisation.


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

## Développement

### Hooks Git avec pre-commit et Formatage de Code avec Prettier et Ruff

Ce projet utilise https://pre-commit.com/ pour gérer les hooks Git ainsi que Prettier et Ruff pour le formatage automatique du code.
Le build sur le CI échouera si les fichiers python, javascript et json ne sont pas proprement formattés.

#### Vérification Automatique avant chaque Commit


