# Projet neomail

# Présentation du projet
Le projet neomail est un outil qui permet de trier/classer vos mails grace à des labels construit par un modèle de clustering.

neomail project can to classify your mail from labels. labelling is build from clustering model.

# Lancer le projet en local

Vous devez d'abord vous rendre au lien suivant afin de générer votre compte de service :

1 . https://developers.google.com/gmail/api/quickstart/python

![Python Quickstart](docs/images/python_quickstart.png)

cliquer sur "Enable the Gmail API"

2 . Choisir "Desktop app" et cliquer sur "CREATE"
![Generate Json](docs/images/python_quickstart_generate_json.png)

3 . renommé le en client_secret_localhost.json et placé le dans dossier "resources".

Information : client_secret_localhost.json : Fichier d'autorisation pour l'API Gmail. Ce fichier est propre à votre mail.

## Lancer à partir d'un environnement virtual python

1. Installer les libraries dont vous avez besoin
```
pip install -r requirements.txt
```

2. Lancer le programme

```
bash run_neomail_localhost.sh
```

## Lancer à partir du docker-compose


Creer un Compte
http://127.0.0.1:8040/api/v1/auth/signup

```json
{
	"email":"manitra@me.fr",
	"password":"test"
}
```

Se connecter
http://127.0.0.1:8040/api/v1/auth/login

```json
{
	"email":"manitra@me.fr",
	"password":"test"
}
```
Cc le Token obtenu

Obtenir le credential Google propre à se compte

```
http://127.0.0.1:8040/api/v1/credentials
```

Sur postman :
Get
1. Authorization
2. Type : Bearer Token
3. Coller le Token

```json
{
    "token": "XXX"
}
```

## Lautch Streamer
```
uvicorn src.app.ika_streamer.main:app --reload
```

Lancer serveur SMTP : 
```bash
python -m smtpd -n -c DebuggingServer localhost:1025 
```