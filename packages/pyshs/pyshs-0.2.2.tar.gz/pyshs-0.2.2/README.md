# Bibliothèque PySHS

La bibliothèque PySHS a pour but de réunir des outils utiles à un public de praticiens des sciences humaines et sociales francophones pour traiter des données. Elle a pour but de s'enrichir progressivement pour permettre à Python de devenir une alternative (réaliste) à R avec des fonctions facilement utilisables sur les opérations habituelles.

Actuellement, son principal objectif est de pouvoir rapidement obtenir les traitements statistiques nécessaires à l'analyse d'une enquête, en complément avec Pandas.

La version actuelle est la **0.2.0**

## Contenu

### Traiter des données issues d'enquêtes par questionnaires (avec pondération)

- Description d'un tableau de données
- Tri à plat et tableau croisé avec pondération
- Tableau croisant une variable dépendante avec une série de variables indépendantes, avec pondération
- Wrapper pour réaliser une régression logistique binomiale pondérée

## Installation

:warning: PySHS est uniquement compatible avec **Python 3**

:warning: La bibliothèque est encore en construction donc des changements peuvent arriver vite. Pensez à la mettre à jour, le nom des fonctions change encore.

**Via PyPI**

```sh
$ pip install pyshs --upgrade
```

## Utilisation

### Tri à plat d'une variable qualitative pondérée

```python
>> import pyshs
>> data = pd.read_excel("enquete.xlsx")
>> pyshs.tri_a_plat(data,"age","weight")
```

| age     |   Effectif redressé |   Pourcentage (%) |
|:--------|--------------------:|------------------:|
| [0-25[  |               260.4 |              13.0 |
| [25-45[ |               731.1 |              36.5 |
| [45-65[ |               755.1 |              37.7 |
| [65+    |               256.4 |              12.8 |
| Total   |                2003 |               100 |


### Autres utilisations

Voir le Notebook **Exemple PySHS.ipynb**
