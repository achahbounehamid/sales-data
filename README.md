# Sales Data Pipeline

##  Description

Ce projet a été réalisé dans le cadre d’un exercice Data Engineering.

L’objectif est de mettre en place une architecture Docker permettant :

* l’exécution de scripts Python
* le stockage des données avec SQLite
* l’import de données CSV
* l’analyse des ventes avec SQL

---

##  Architecture
..
![MCD](../sales-data/asset/mcd_new.PNG)
Le projet repose sur deux services :

* un service Python pour les scripts
* un service SQLite pour le stockage des données

Les données sont partagées via un volume Docker.

---

## Structure du projet

```text
sales-data/

├── app/
│   ├── analyse.py 
│   ├── import_data.py
│   └── main.py
├── asset/
│   ├── mcd.png
├── data/
│   ├── magasins.csv
│   ├── produits.csv
│   ├── ventes.csv
│   └── ventes.db
├──scripts
├── .gitignore
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

## Technologies utilisées

* Python 3.11
* SQLite
* Docker
* Docker Compose
* Pandas

---

##  Lancement du projet

### Construire et lancer les conteneurs

```bash
docker-compose up --build
```

---

## Fonctionnalités

* création automatique de la base SQLite
* création des tables relationnelles
* import des fichiers CSV
* gestion des doublons
* analyses SQL :

  * chiffre d’affaires total
  * ventes par produit
  * ventes par région

---

##  Analyses réalisées

Les résultats des analyses sont stockés dans la table :

```text
resultats_analyses
```

---

## Auteur

Projet réalisé par Hamid ACHAHBOUNE dans le cadre d’un exercice Data Engineering.
