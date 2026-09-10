# LaBrigade
Le projet consiste à développer une application web collaborative nommée "La Brigade", initiée par un célèbre cuisinier français. Cette plateforme permettra aux utilisateurs passionnés de cuisine de proposer, partager et découvrir des recettes centrées sur la cuisine "bistronomique"


# La Brigade —  projet

Stack : **Python + NiceGUI + PostgreSQL + SQLAlchemy**

## Installation

```bash
python -m venv venv
source venv/bin/activate      # Windows : venv\Scripts\activate
pip install -r requirements.txt
```

## Base de données

1. Installer PostgreSQL en local (ou via Docker).
2. Créer la base :
   ```sql
   CREATE DATABASE la_brigade;
   ```
3. Adapter l'URL de connexion dans `database.py` (`DATABASE_URL`) avec vos
   identifiants (utilisateur, mot de passe, port).

## Lancer l'application

```bash
python main.py
```

L'application est accessible sur http://localhost:8080

Au premier lancement, `init_db()` crée automatiquement les tables
(`users`, `recettes`, `commentaires`, `notes`) dans PostgreSQL.

## Créer un compte administrateur (équipe du chef)

Il n'y a pas encore d'interface pour ça : après une première inscription
classique via `/inscription`, passez la colonne `est_admin` à `true`
directement en base :

```sql
UPDATE users SET est_admin = true WHERE email = 'chef@example.com';
```

## Structure du projet

```
la_brigade/
├── main.py                 # déclaration des routes (@ui.page)
├── database.py              # connexion PostgreSQL + session SQLAlchemy
├── models.py                 # User, Recette, Commentaire, Note
├── auth.py                   # inscription, connexion, gestion de session
├── pages/
│   ├── navbar.py              # barre de navigation commune
│   ├── accueil.py
│   ├── comptes.py             # connexion + inscription
│   ├── liste_recettes.py
│   ├── detail_recette.py      # + commentaires + notes
│   ├── proposer_recette.py    # formulaire + upload image
│   ├── profil.py
│   └── validation_admin.py    # espace équipe du chef
├── static/uploads/           # images des recettes uploadées
└── requirements.txt
```

## État du squelette

Ce qui fonctionne déjà :
- Inscription / connexion (mots de passe hashés avec bcrypt)
- Publication d'une recette (statut "en_attente" par défaut)
- Consultation des recettes validées (accueil + liste + détail)
- Commentaires et notation (1 à 5) sur une recette
- Espace admin : valider / refuser / marquer "bistronomique"
- Upload d'image de recette

Pistes à compléter par l'équipe :
- Filtres avancés sur la liste des recettes (par ingrédient, difficulté...)
- Pagination si le nombre de recettes grandit
- Meilleure gestion des erreurs d'upload (taille, format de fichier)
- Amélioration visuelle (respect plus poussé de la charte graphique)
- Tests automatisés
