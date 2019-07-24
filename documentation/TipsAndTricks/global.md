# Optimiseur
```
Algorithme qui permet de minimiser la fonction de perte pondérée.

SGD(lr=0.1, momentum=0.9, decay=0.0, nesterov=False)
Descente de gradient stochastique (SGD)(modifié)
Momentum : Momentum prend en compte les gradients passés pour aplanir les étapes de la descente. Il peut être appliqué avec une descente par gradient en batch, une descente en gradient par mini-batch ou une descente par gradient stochastique.
batch_size indique la taille du sous-ensemble de votre échantillon d'apprentissage (par exemple, 100 sur 1 000) qui sera utilisée pour former le réseau au cours de son processus d'apprentissage. Chaque lot entraîne le réseau dans un ordre successif, en tenant compte des poids mis à jour provenant de l'appliance du lot précédent. return_sequence indique si une couche récurrente du réseau doit renvoyer la totalité de sa séquence de sortie (c'est-à-dire une séquence de vecteurs de dimension spécifique) à la couche suivante du réseau, ou tout simplement sa dernière sortie, qui est un vecteur unique de la même dimension. Cette valeur peut être utile pour les réseaux conformes à une architecture RNN. batch_input_shape définit que la classification séquentielle du réseau de neurones peut accepter des données d'entrée de la taille de lot définie uniquement, limitant ainsi la création de tout vecteur de dimension variable. Il est largement utilisé dans les réseaux LSTM empilés.
```

# Dropout
```
Dropout prend la sortie des activations de la couche précédente et définit de manière aléatoire une certaine fraction (taux d'abandon) des activations sur 0, en les annulant ou en les «supprimant».

C'est une technique de régularisation courante utilisée pour prévenir les surajustements dans les réseaux de neurones. Le taux d'abandon est l'hyperparamètre ajustable qui est ajusté pour mesurer les performances avec différentes valeurs. Il est généralement défini entre 0,2 et 0,5 (mais peut être défini de manière arbitraire).
Le décrochage n’est utilisé que pendant la formation ; Au moment du test, aucune activation n'est abandonnée, mais réduite par un facteur de taux d'abandon. Cela tient compte du nombre d'unités actives pendant la période de test par rapport à la durée de formation.
```

```
Lr : Le taux d'apprentissage est un hyper-paramètre qui contrôle à quel point nous ajustons les poids de notre réseau en fonction du gradient de perte. Plus la valeur est basse, plus nous roulons lentement sur la pente descendante. Bien que cela puisse être une bonne idée (en utilisant un taux d’apprentissage faible) pour nous assurer que nous ne manquons aucun minimum local, cela pourrait également signifier que nous allons prendre beaucoup de temps pour converger - surtout si nous restons coincés. une région de plateau.

new_weight = existing_weight — learning_rate * gradient
```

# Fonctions de perte dans les réseaux de neurones


## The currently available loss functions for Keras are as follows:
```
mean_squared_error
mean_absolute_error
mean_absolute_percentage_error
mean_squared_logarithmic_error
squared_hinge
hinge
categorical_hinge
logcosh
categorical_crossentropy
sparse_categorical_crossentropy
binary_crossentropy
kullback_leibler_divergence
poisson
cosine_proximity
```

```
Le régularisateur d'activité fonctionne en fonction de la sortie du réseau et est principalement utilisé pour régulariser des unités cachées, tandis que weight_regularizer, comme son nom l'indique, agit sur les poids, les faisant se décomposer. Fondamentalement, vous pouvez exprimer la perte de régularisation en fonction de la sortie ( activity_regularizer) ou des poids ( weight_regularizer).

Le nouveau kernel_regularizerremplace weight_regularizer- bien que ce ne soit pas très clair dans la documentation.

De la définition de kernel_regularizer:

kernel_regularizer: fonction de régularisation appliquée à la kernelmatrice de pondération (voir régularisateur).

Et activity_regularizer:

activity_regularizer: fonction de régularisation appliquée à la sortie de la couche (son "activation"). (voir régularisateur).

Modifier Important : Notez qu'il ya un bug dans le activity_regularizer qui a été fixée que dans la version 2.1.4 de Keras (au moins avec back - end tensorflow). En effet, dans les versions plus anciennes, la fonction de régularisateur d'activité est appliquée à l'entrée du calque, au lieu d'être appliquée à la sortie (les activations réelles du calque, comme prévu). Donc, méfiez-vous si vous utilisez une version plus ancienne de Keras (antérieure à 2.1.4), la régularisation des activités risque de ne pas fonctionner correctement.
```

```
Que fait une contrainte de poids max_norm?

maxnorm(m)Si votre poids dépasse la norme L2 m, modifiez votre matrice de poids en fonction d’un facteur qui réduit la norme à m. Comme vous pouvez le trouver dans le code keras dans class MaxNorm(Constraint):

def __call__(self, w):
    norms = K.sqrt(K.sum(K.square(w), axis=self.axis, keepdims=True))
    desired = K.clip(norms, 0, self.max_value)
    w *= (desired / (K.epsilon() + norms))
    return w
En plus, maxnorma un axis argument, le long duquel la norme est calculée. Dans votre exemple, vous ne spécifiez pas d'axe. La norme est donc calculée sur toute la matrice de pondération. Si, par exemple, vous voulez contraindre la norme de chaque filtre de convolution, en supposant que vous utilisiez le tfclassement des dimensions, la matrice de pondération aura la forme (rows, cols, input_depth, output_depth). Le calcul de la norme sur axis = [0, 1, 2]contraindra chaque filtre à la norme donnée.

Pourquoi le faire

Le fait de contraindre directement la matrice de poids est un autre type de régularisation. Si vous utilisez un simple terme de régularisation L2, vous pénalisez les poids élevés avec votre fonction de perte. Avec cette contrainte, vous régularisez directement. Comme cela est également lié dans le kerascode, cela semble fonctionner particulièrement bien en combinaison avec une dropoutcouche. Plus d'informations au chapitre 5.1 de cet article
```


```
3. régularisation
Les réseaux neuronaux profonds avec un grand nombre de paramètres sont des systèmes d’apprentissage automatique très puissants. Cependant, la suralimentation est un problème sérieux dans de tels réseaux. On trouvera ci-dessous quelques techniques proposées récemment et qui sont devenues une norme générale dans les réseaux de neurones à convolution.

Le décrochage est une technique permettant de résoudre ce problème. L'idée principale est de supprimer au hasard des unités (ainsi que leurs connexions) du réseau de neurones pendant l'entraînement. La réduction du nombre de paramètres à chaque étape de l'entraînement a un effet de régularisation. Le décrochage a montré des améliorations dans les performances des réseaux de neurones en ce qui concerne les tâches d’apprentissage supervisé dans les domaines de la vision, de la reconnaissance vocale, de la classification de documents et de la biologie computationnelle, obtenant des résultats à la pointe de la technologie sur de nombreux ensembles de données de référence [1].

Kernel_regularizer   permet d'appliquer des pénalités sur les paramètres de la couche lors de l'optimisation. Ces pénalités sont intégrées à la fonction de perte que le réseau optimise. Cet argument en couche convolutive n'est rien d'autre que  L2 regularisation des poids. Cela pénalise les poids en pointe et garantit que toutes les entrées sont prises en compte. Lors de la mise à jour des paramètres de descente de gradient, la régularisation ci-dessus de L2 signifie en fin de compte que chaque poids est décomposé de manière linéaire.

BatchNormalization  normalise l'activation de la couche précédente à chaque lot, c'est-à-dire qu'il applique une transformation qui maintient l'activation moyenne proche de 0 et l'écart type d'activation proche de 1. Il résout le problème du décalage de la covariable interne. Il agit également comme un régularisateur, éliminant dans certains cas la nécessité de l’abandon scolaire. La normalisation par lots permet d'obtenir la même précision avec moins d'étapes d'entraînement, accélérant ainsi le processus d'entraînement [2].
```
![epoch](https://github.com/Harisonm/4aibd-s1-project-ml/blob/master/docs/pictures/epoch.png)







