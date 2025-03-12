# HBNB Project Documentation

## Introduction

Le projet **HBNB** est une application web complète qui permet de gérer et d'afficher divers lieux, commodités et interactions des utilisateurs. Il suit une architecture à trois couches, garantissant la modularité, la scalabilité et la maintenabilité. Ce document présente l'architecture du système, ses composants clés et le flux d'interaction des API.

---

## Architecture du Système

### Diagramme de Packages

L'architecture du projet repose sur une structure à trois couches, chacune ayant des responsabilités distinctes. Voici un aperçu de ces couches :

1. **Couche de Présentation**  
   Cette couche contient le **package de l'interface utilisateur**, qui gère les interactions avec l'utilisateur et l'affichage des données.

2. **Couche Métier**  
   La couche métier gère la logique principale de l'application. Elle est composée de quatre packages clés :
   - **User** : Gère les informations et interactions des utilisateurs.
   - **Place** : Gère les informations relatives aux lieux.
   - **Review** : Gère les avis laissés par les utilisateurs sur les lieux.
   - **Amenity** : Gère les commodités disponibles dans les lieux.

3. **Couche de Persistance**  
   Cette couche comprend les accès aux données et les agents de service, responsables des opérations sur la base de données.

Les couches interagissent de manière séquentielle, où la **couche de présentation** communique avec la **couche métier**, et cette dernière s'appuie sur la **couche de persistance** pour la gestion des données.

---

### Diagramme de Séquence pour les Appels API

Voici un aperçu des processus principaux impliqués dans les appels API du projet :

1. **Inscription de l'utilisateur**  
   - **But** : Validation et enregistrement des informations de l'utilisateur.  
   - **Composants** : API, Logique métier, Base de données.

2. **Création de lieu**  
   - **But** : Permet à l'utilisateur de créer une annonce pour un lieu.  
   - **Composants** : API, Logique métier, Base de données.

3. **Soumission d'un avis**  
   - **But** : Soumettre un avis après un séjour.  
   - **Composants** : API, Logique métier, Base de données.

4. **Liste des lieux disponibles**  
   - **But** : Récupérer la liste des lieux selon les critères de recherche fournis.  
   - **Composants** : API, Logique métier, Base de données.

---

## Classes et Composants

### La classe `User`

La classe `User` représente un utilisateur de la plateforme. Un utilisateur peut être un hôte, un invité ou un administrateur et interagir avec le système (profil, réservations, etc.).

#### Attributs :
- `firstName` : Prénom de l'utilisateur.
- `lastName` : Nom de l'utilisateur.
- `email` : Adresse e-mail de l'utilisateur.
- `password` : Mot de passe de l'utilisateur.
- `isAdmin` : Indicateur s'il s'agit d'un administrateur.

#### Méthodes :
- `register()` : Inscrit un nouvel utilisateur.
- `updateProfile()` : Met à jour le profil de l'utilisateur.
- `delete()` : Supprime l'utilisateur.

---

### La classe `Place`

La classe `Place` représente un lieu ou un emplacement que l'utilisateur peut choisir dans le système. Ce lieu peut être réservé, décrit et mis à jour par les utilisateurs (ex : appartement, maison, chambre, etc.).

#### Attributs :
- `title` : Titre du lieu.
- `description` : Description du lieu.
- `price` : Prix de la location.
- `latitude` : Latitude du lieu.
- `longitude` : Longitude du lieu.

#### Méthodes :
- `create()` : Crée un nouveau lieu.
- `update()` : Met à jour un lieu existant.
- `delete()` : Supprime un lieu.
- `list()` : Liste tous les lieux disponibles.

---

### La classe `Review`

La classe `Review` représente les commentaires et évaluations laissés par les utilisateurs après un séjour dans un lieu. Les utilisateurs peuvent partager leur expérience, donner une note et rédiger un commentaire.

#### Attributs :
- `rating` : Note attribuée au lieu.
- `comment` : Commentaire sur l'expérience de l'utilisateur.

#### Méthodes :
- `create()` : Crée un avis.
- `update()` : Met à jour un avis.
- `delete()` : Supprime un avis.
- `listByPlace()` : Liste tous les avis pour un lieu spécifique.

---

### La classe `Amenity`

La classe `Amenity` décrit les équipements et les caractéristiques disponibles dans un logement ou un lieu, tels que des meubles, des appareils, ou d'autres commodités importantes pour le séjour des utilisateurs.

#### Attributs :
- `name` : Nom de la commodité.
- `description` : Description de la commodité.

#### Méthodes :
- `create()` : Crée une nouvelle commodité.
- `update()` : Met à jour une commodité.
- `delete()` : Supprime une commodité.
- `list()` : Liste toutes les commodités disponibles.

---

## Conclusion

Dans le système de location de logements HBNB, l'utilisateur choisit un lieu (ou **Place**) qu'il souhaite louer. Après son séjour, l'utilisateur peut laisser un avis sur ce lieu, ce qui aide d'autres utilisateurs à faire leur choix. Les commodités disponibles dans chaque lieu (comme le mobilier, les appareils électroménagers, etc.) influencent également l'expérience de l'utilisateur. Chaque **Place** est reliée à des **Amenities** spécifiques, et l'utilisateur peut interagir avec les différents éléments du système pour réserver un lieu, laisser un avis, et voir les commodités disponibles.

---

## Technologies utilisées

- **Backend** : Python, Flask
- **Base de données** : SQLite / MySQL
- **Framework** : Flask-RESTful pour l'API

---

### Contact

Pour toute question ou contribution, n'hésitez pas à me contacter via [email@example.com](mailto:email@example.com).

---

### License

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.
