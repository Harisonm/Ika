# Métriques pour évaluer les algorithmes d'apprentissage automatique en Python

Les mesures que vous choisissez pour évaluer vos algorithmes d'apprentissage machine sont très importantes.

Le choix des métriques influence la manière dont la performance des algorithmes d'apprentissage automatique est mesurée et comparée. Ils influencent la manière dont vous pondérez l'importance des différentes caractéristiques dans les résultats et votre choix ultime de l'algorithme à choisir.




# Quelle est la difference entre categorical_accuracy et sparse_categorical_accuracy in Keras?

Pour l'exemple suivant : 
```
def categorical_accuracy(y_true, y_pred):
    return K.cast(K.equal(K.argmax(y_true, axis=-1),
                          K.argmax(y_pred, axis=-1)),
                  K.floatx())


def sparse_categorical_accuracy(y_true, y_pred):
    return K.cast(K.equal(K.max(y_true, axis=-1),
                          K.cast(K.argmax(y_pred, axis=-1), K.floatx())),
                  K.floatx())
```

## Categorical_accuracy :
vérifie si l' index de la valeur vraie maximale est égal à l' index de la valeur prédite maximale.

## sparse_categorical_accuracy : 
vérifie si la valeur vraie maximale est égale à l' index de la valeur prédite maximale.

## Confrontation 
Donc, categorical_accuracyvous devez spécifier votre target ( y) en tant que vecteur codé à une seule étape (par exemple, dans le cas de 3 classes, lorsqu'une vraie classe est une seconde classe, elle ydevrait l'être (0, 1, 0). sparse_categorical_accuracyVous devez uniquement fournir un entier de la vraie classe (dans cas de l'exemple précédent - ce serait 1comme l'indexation des classes est 0basée sur).


# Précision binaire:

def binary_accuracy ( y_true , y_pred ):
 retourner K . moyenne ( K . égale ( y_true , K . rond ( y_pred )), axe = - 1 )
K.round (y_pred) implique que le seuil est 0.5, tout ce qui est supérieur à 0.5 sera considéré comme correct.

# Exactitude catégorique:

def catégorical_accuracy ( y_true , y_pred ):
 retourner K . coulée ( K . égale ( K . argmax ( y_true , axe = - 1 ),
K . argmax ( y_pred , axis = - 1 )),
K . floatx ())
K.argmax (y_true) prend la valeur la plus élevée pour être la prédiction et correspond au jeu de comparaison.

# Précision catégorique clairsemée:

def sparse_categorical_accuracy ( y_true , y_pred ):
 retourner K . coulée ( K . égale ( K . max ( y_true , axe = - 1 ),
K . coulée ( K . argmax ( y_pred , axe = - 1 ), K . floatx ())),
K . floatx ())
Peut-être une meilleure métrique que catégorical_accuracy dans certains cas, en fonction de vos données.

# Précision catégorique maximale:

def top_k_categorical_accuracy ( y_true , y_pred , k = 5 ):
 retourner K . moyenne ( K . in_top_k ( y_pred , K . argmax ( y_true , axe = - 1 ), k ), l' axe = - 1 )
Le top-k est mesuré sur la précision de la prédiction correcte dans les prédictions du top-k. La plupart des articles exposeront l'efficacité des modèles en fonction de la précision du top 5.