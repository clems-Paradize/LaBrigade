from nicegui import ui
from database import get_session
from models import Recette, Commentaire, Note
from auth import utilisateur_connecte, get_current_user_id
from pages.navbar import navbar


def page_detail_recette(recette_id: int):
    navbar()

    session = get_session()
    try:
        recette = session.query(Recette).filter_by(id=recette_id).first()
        if not recette:
            ui.label("Recette introuvable.").classes("p-8 text-red-600")
            return

        with ui.column().classes("w-full p-8 gap-4 max-w-3xl mx-auto"):
            if recette.image_path:
                ui.image(recette.image_path).classes("w-full h-64 object-cover rounded")

            ui.label(recette.titre).classes("text-3xl font-bold")
            if recette.est_bistronomique:
                ui.badge("Bistronomique ⭐").classes("bg-amber-500")

            ui.label(recette.description or "").classes("text-gray-700")

            ui.label("Ingrédients").classes("text-xl font-bold mt-4")
            ui.label(recette.ingredients or "").style("white-space: pre-line")

            ui.label("Étapes de préparation").classes("text-xl font-bold mt-4")
            ui.label(recette.etapes or "").style("white-space: pre-line")

            note = recette.note_moyenne
            ui.label(f"Note moyenne : {note}/5" if note else "Pas encore noté")

            # --- Notation ---
            if utilisateur_connecte():
                ui.label("Votre note").classes("font-bold mt-4")
                with ui.row():
                    for valeur in range(1, 6):
                        ui.button(
                            str(valeur),
                            on_click=lambda v=valeur: noter(recette_id, v),
                        )

            # --- Commentaires ---
            ui.label("Commentaires").classes("text-xl font-bold mt-6")
            commentaires_container = ui.column().classes("gap-2 w-full")

            def charger_commentaires():
                commentaires_container.clear()
                s = get_session()
                try:
                    coms = (
                        s.query(Commentaire)
                        .filter_by(recette_id=recette_id)
                        .order_by(Commentaire.date_creation.desc())
                        .all()
                    )
                finally:
                    s.close()
                with commentaires_container:
                    if not coms:
                        ui.label("Aucun commentaire pour l'instant.")
                    for c in coms:
                        with ui.card().classes("w-full"):
                            ui.label(f"{c.auteur.nom} — {c.date_creation:%d/%m/%Y}").classes(
                                "text-xs text-gray-500"
                            )
                            ui.label(c.texte)

            charger_commentaires()

            if utilisateur_connecte():
                nouveau_commentaire = ui.textarea("Ajouter un commentaire").classes("w-full")

                def envoyer_commentaire():
                    if not nouveau_commentaire.value:
                        return
                    s = get_session()
                    try:
                        c = Commentaire(
                            texte=nouveau_commentaire.value,
                            recette_id=recette_id,
                            user_id=get_current_user_id(),
                        )
                        s.add(c)
                        s.commit()
                    finally:
                        s.close()
                    nouveau_commentaire.value = ""
                    charger_commentaires()

                ui.button("Envoyer", on_click=envoyer_commentaire)
            else:
                ui.label("Connectez-vous pour commenter ou noter cette recette.")
    finally:
        session.close()


def noter(recette_id: int, valeur: int):
    session = get_session()
    try:
        user_id = get_current_user_id()
        note_existante = (
            session.query(Note)
            .filter_by(recette_id=recette_id, user_id=user_id)
            .first()
        )
        if note_existante:
            note_existante.valeur = valeur
        else:
            session.add(Note(recette_id=recette_id, user_id=user_id, valeur=valeur))
        session.commit()
        ui.notify("Merci pour votre note !")
    finally:
        session.close()