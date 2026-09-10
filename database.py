"""
Connexion à PostgreSQL + session SQLAlchemy.

Avant de lancer le projet :
1. Créer la base : CREATE DATABASE la_brigade;
2. Adapter DATABASE_URL ci-dessous avec vos identifiants.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Format : postgresql://utilisateur:mot_de_passe@localhost:5432/nom_de_la_base
# DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/la_brigade"
DATABASE_URL = "postgresql://postgres:GYb7XCe36SKefLk1@db.iomaeinaopqpdgzirjqo.supabase.co:5432/postgres"
#DATABASE_URL = "https://iomaeinaopqpdgzirjqo.supabase.co"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def get_session():
    """Retourne une nouvelle session de base de données."""
    return SessionLocal()


def init_db():
    """Crée toutes les tables si elles n'existent pas déjà."""
    import models  # noqa: F401 (nécessaire pour enregistrer les modèles)
    Base.metadata.create_all(bind=engine)