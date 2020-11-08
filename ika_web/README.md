# Ika Web

## Access and documentation
Host
```bash
http://127.0.0.1:8000/
```
API Documentation
```bash
http://127.0.0.1:8000/api/v1/docs/
```

## Using API

### S'inscrire
http://127.0.0.1:8000/api/v1/auth/signup

```json
{
	"email":"manitra@me.fr",
	"password":"test"
}
```

### Se connecter
http://127.0.0.1:8000/api/v1/auth/login

```json
{
	"email":"manitra@me.fr",
	"password":"test"
}
```
Cc le Token obtenu


## Using Web Views 

### Obtenir le credential Google propre à se compte
```
http://127.0.0.1:8080/api/v1/google/authorize

http://127.0.0.1:8000/api/v1/google/authorize
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

# serveur SMTP
Lancer serveur SMTP : 

```bash
python -m smtpd -n -c DebuggingServer localhost:1025 
```

### Notes 
Pour exécuter un test d'isolation
```
python -m unittest ika_web/tests/test_signup.py
```

Pour exécuter tous les tests en même temps, utilisez la commande:
```bash
python -m unittest --buffer

--bufferou -best utilisé pour ignorer la sortie lors d'un test réussi.
```

