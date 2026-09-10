from nicegui import ui
from database import get_session
from models import User, Recette
from auth import get_current_user_id, utilisateur_connecte
from pages.navbar import navbar


def page_profil():
    navbar()

    if not utilisateur_connecte():
        ui.label("Vous devez être connecté pour voir cette page.").classes(
            "p-8 text-red-600"
        )
        return

    session = get_session()
    try:
        user = session.query(User).filter_by(id=get_current_user_id()).first()
        mes_recettes = (
            session.query(Recette).filter_by(auteur_id=user.id)
            .order_by(Recette.date_creation.desc()).all()
        )

        with ui.column().classes("w-full p-8 gap-3 max-w-2xl mx-auto"):
            ui.label(f"Profil de {user.nom}").classes("text-2xl font-bold")
            ui.label(user.email).classes("text-gray-600")

            ui.label("Mes recettes").classes("text-xl font-bold mt-6")
            if not mes_recettes:
                ui.label("Vous n'avez encore proposé aucune recette.")
            for r in mes_recettes:
                statut_couleur = {
                    "en_attente": "text-amber-600",
                    "validee": "text-green-600",
                    "refusee": "text-red-600",
                }.get(r.statut, "")
                with ui.card().classes("w-full"):
                    ui.label(r.titre).classes("font-bold")
                    ui.label(f"Statut : {r.statut}").classes(statut_couleur)
    finally:
        session.close()