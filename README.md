# Projet neomail

# Présentation du projet
Le projet neomail est un outil qui permet de trier/classé vos mails grace à des labels construit par un modèle de clustering

neomail project can to classify your mail from labels. labelling is build from clustering model.

# Présentation du repository

Le projet neomail englobe 3 environnement :
- environnement  dev : 
Vous pouvez lancer les différents fichiers '.py' des dossiers 'tests' sans passer par flask.

Docker de dev:


- environnement datalab
Des notebooks sont disponible pour faire des tests de modele. 

docker datalab:

- environnement production
Vous trouverez diverses APIs dans chaque block que vous pourrez lancer via flask.

Docker de production:











Chaque brique des components a besoin d'un compote de service de type .json pour fonctionner.

Les comptes de service et fichier d'env :

.env : Spécifie tout les paramètre lié à vôtre environnement global (ici GCP)

service_account.json : Fichier qui permet d'accèder aux service lié à GCP

gmail_service.jon : Fichier d'autorisation pour l'API Gmail. Ce fichier est propre à votre mail 
pour le généré : 
1 . https://developers.google.com/gmail/api/quickstart/python
2 . cliquer sur "ENABLE THE GMAIL API"
3 . renommé le en gmail_service.json et placé le dans dossier "resources" lié à votre cas d'usage.

chaque credential en .json se trouve dans resources