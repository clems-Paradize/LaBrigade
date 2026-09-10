from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, Text, Boolean, ForeignKey, DateTime,
    UniqueConstraint
)
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    mot_de_passe_hash = Column(String(255), nullable=False)
    est_admin = Column(Boolean, default=False)
    date_creation = Column(DateTime, default=datetime.utcnow)

    recettes = relationship("Recette", back_populates="auteur")
    commentaires = relationship("Commentaire", back_populates="auteur")
    notes = relationship("Note", back_populates="auteur")


class Recette(Base):
    __tablename__ = "recettes"

    id = Column(Integer, primary_key=True)
    titre = Column(String(150), nullable=False)
    description = Column(Text)
    ingredients = Column(Text)   # simple texte, un ingrédient par ligne
    etapes = Column(Text)        # simple texte, une étape par ligne
    image_path = Column(String(255), nullable=True)

    # en_attente | validee | refusee
    statut = Column(String(20), default="en_attente")
    est_bistronomique = Column(Boolean, default=False)

    auteur_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date_creation = Column(DateTime, default=datetime.utcnow)

    auteur = relationship("User", back_populates="recettes")
    commentaires = relationship(
        "Commentaire", back_populates="recette", cascade="all, delete-orphan"
    )
    notes = relationship(
        "Note", back_populates="recette", cascade="all, delete-orphan"
    )

    @property
    def note_moyenne(self):
        if not self.notes:
            return None
        return round(sum(n.valeur for n in self.notes) / len(self.notes), 1)


class Commentaire(Base):
    __tablename__ = "commentaires"

    id = Column(Integer, primary_key=True)
    texte = Column(Text, nullable=False)
    date_creation = Column(DateTime, default=datetime.utcnow)

    recette_id = Column(Integer, ForeignKey("recettes.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    recette = relationship("Recette", back_populates="commentaires")
    auteur = relationship("User", back_populates="commentaires")


class Note(Base):
    __tablename__ = "notes"
    __table_args__ = (
        UniqueConstraint("recette_id", "user_id", name="unique_note_par_user"),
    )

    id = Column(Integer, primary_key=True)
    valeur = Column(Integer, nullable=False)  # 1 à 5

    recette_id = Column(Integer, ForeignKey("recettes.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    recette = relationship("Recette", back_populates="notes")
    auteur = relationship("User", back_populates="notes")