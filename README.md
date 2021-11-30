# Application permettant de remonter et suivre des problèmes techniques (issue tracking system).

Application de suivi des problèmes pour les trois plateformes (site web, applications Android et iOS).
- L'application permettra essentiellement aux utilisateurs de créer divers projets, d'ajouter des utilisateurs à des projets spécifiques, de créer des problèmes au sein des projets et d'attribuer des libellés à ces problèmes en fonction de leurs priorités, de balises, etc.
- L'application exploite les points de terminaison d'API qui serviront les données.


Développement d'un API RESTful pour traiter les données relatives :
- au projets,
- à ses contributeurs, 
- aux problèmes relevés,
- aux commentaires associés.

## Structuration de l'API via Postman

L'API se structure autour de 2 collections :
1. Login
   
2. Global project
    * Projects
    * Contributors
    * Issues
    * Comments


Elles permettent d'acceder aux points de terminaison suivants :

|	#	|	Point de terminaison d'API	|	Méthode HTTP	|	URL	|
|	-----	|	-----------------------------	|	--------------	|	--------------------------------------------------------	|
|	1.	|	Inscription de l'utilisateur	|	POST	|	/signup/	|
|	2.	|	Connexion de l'utilisateur	|	POST	|	/login/	|
|	3.	|	Récupérer la liste de tous les projets (projects) rattachés à l'utilisateur (user) connecté	|	GET	|	/projects/	|
|	4.	|	Créer un projet	|	POST	|	/projects/	|
|	5.	|	Récupérer les détails d'un projet (project) via son id	|	GET	|	/projects/{id}/	|
|	6.	|	Mettre à jour un projet	|	PUT	|	/projects/{id}/	|
|	7.	|	Supprimer un projet et ses problèmes	|	DELETE	|	/projects/{id}/	|
|	8.	|	Ajouter un utilisateur (collaborateur) à un projet	|	POST	|	/projects/{id}/users/	|
|	9.	|	Récupérer la liste de tous les utilisateurs (users) attachés à un projet (project)	|	GET	|	/projects/{id}/users/	|
|	10.	|	Supprimer un utilisateur d'un projet	|	DELETE	|	/projects/{id}/users/{id}	|
|	11.	|	Récupérer la liste des problèmes (issues) liés à un projet (project)	|	GET	|	/projects/{id}/issues/	|
|	12.	|	Créer un problème dans un projet	|	POST	|	/projects/{id}/issues/	|
|	13.	|	Mettre à jour un problème dans un projet	|	PUT	|	/projects/{id}/issues/{id}	|
|	14.	|	Supprimer un problème d'un projet	|	DELETE	|	/projects/{id}/issues/{id}	|
|	15.	|	Créer des commentaires sur un problème	|	POST	|	/projects/{id}/issues/{id}/comments/	|
|	16.	|	Récupérer la liste de tous les commentaires liés à un problème (issue)	|	GET	|	/projects/{id}/issues/{id}/comments/	|
|	17.	|	Modifier un commentaire	|	PUT	|	/projects/{id}/issues/{id}/comments/{id}	|
|	18.	|	Supprimer un commentaire	|	DELETE	|	/projects/{id}/issues/{id}/comments/{id}	|
|	19.	|	Récupérer un commentaire (comment) via son id	|	GET	|	/projects/{id}/issues/{id}/comments/{id}	|


Retrouvez la [documentation Postman Login ici](https://documenter.getpostman.com/view/18184212/UVJeEG8B).
Retrouvez la [documentation Global project ici](https://documenter.getpostman.com/view/18184212/UVJeEG8C).







## Informations d'installation et d'exécution avec venv et pip


**Configurations et exécution du programme**
Installation :
- Cloner ce dépôt de code à l'aide de la commande `$ git clone clone https://github.com/C22660/SoftDesk_API.git` (vous pouvez également télécharger le code [en temps qu'archive zip](https://github.com/C22660/SoftDesk_API/archive/refs/heads/master.zip))
- Rendez-vous depuis un terminal à la racine du répertoire ocmovies-api-fr avec la commande `$ cd SoftDesk`
- Créer un environnement virtuel pour le projet avec `$ python -m venv env` sous windows ou `$ python3 -m venv env` sous macos ou linux.
- Activez l'environnement virtuel avec `$ env\Scripts\activate` sous windows ou `$ source env/bin/activate` sous macos ou linux.
- Installez les dépendances du projet avec la commande `$ pip install -r requirements.txt`

Une fois cette installation effectuée :

- Création du superuser (utilisateur avec droits d'administration) :
depuis le terminal > `$ python manage.py createsuperuser`
entrer le nom d'utilisateur (Username), Email, et mot de passe (invisible lors de la frappe dans le terminal)

- Lancement du serveur :
depuis le terminal > `$ python manage.py runserver`

- Accès aux URLs depuis Postman :
Dans la barre d'adresse, ajouter /administration-application
(127.0.0.1:8000/administration-application)
L'interface d'administration apparaît

- L'accès à la page d'accueil (page de connexion/inscription) directement depuis 127.0.0.1:8000

## Technologies
Python 3.9
Package ajouté : Django 3.2.9 ; djangorestframework 3.12.4 ; djangorestframework-simplejwt 5.0.0

## Auteur        
Cédric M
