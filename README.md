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



http://localhost:8040/api/auth/signup

{
	"email":"manitra@me.fr",
	"password":"test"
}

http://localhost:8040/api/auth/login
{
	"email":"manitra@me.fr",
	"password":"test"
}
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODc1MDExNTAsIm5iZiI6MTU4NzUwMTE1MCwianRpIjoiOTlkMTU1YjYtZjg1Yy00ZmU0LWE5ZGYtYTVjNDJmZTkxZjRlIiwiZXhwIjoxNTg4MTA1OTUwLCJpZGVudGl0eSI6IjVlOWY1N2RhMmQwNDBjMmE3OTE0NDg2ZCIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.dkIwfZ78zMxYVJkKk3CaKNLUSpmjPZZEYFDyPrahnPU"
}

uvicorn src.app.ika_streamer.main:app --reload