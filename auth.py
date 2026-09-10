from passlib.hash import bcrypt
from nicegui import app

from database import get_session
from models import User


def hash_password(password: str) -> str:
    return bcrypt.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.verify(password, password_hash)


def creer_utilisateur(nom: str, email: str, password: str):
    """Crée un nouvel utilisateur. Retourne (user, erreur)."""
    session = get_session()
    try:
        existant = session.query(User).filter_by(email=email).first()
        if existant:
            return None, "Un compte existe déjà avec cet email."

        user = User(
            nom=nom,
            email=email,
            mot_de_passe_hash=hash_password(password),
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user, None
    finally:
        session.close()


def authentifier(email: str, password: str):
    """Vérifie les identifiants. Retourne (user, erreur)."""
    session = get_session()
    try:
        user = session.query(User).filter_by(email=email).first()
        if not user or not verify_password(password, user.mot_de_passe_hash):
            return None, "Email ou mot de passe incorrect."
        return user, None
    finally:
        session.close()


def connecter_session(user: User):
    """Stocke l'utilisateur connecté dans la session NiceGUI."""
    app.storage.user["user_id"] = user.id
    app.storage.user["nom"] = user.nom
    app.storage.user["est_admin"] = user.est_admin


def deconnecter_session():
    app.storage.user.clear()


def utilisateur_connecte() -> bool:
    return "user_id" in app.storage.user


def est_admin() -> bool:
    return app.storage.user.get("est_admin", False)


def get_current_user_id():
    return app.storage.user.get("user_id")