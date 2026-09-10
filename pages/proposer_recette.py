import os
import uuid

from nicegui import ui, events
from database import get_session
from models import Recette
from auth import get_current_user_id, utilisateur_connecte
from pages.navbar import navbar

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def page_proposer_recette():
    navbar()

    if not utilisateur_connecte():
        ui.label("Vous devez être connecté pour proposer une recette.").classes(
            "p-8 text-red-600"
        )
        return

    with ui.column().classes("w-full items-center p-8 gap-3 max-w-2xl mx-auto"):
        ui.label("Proposer une nouvelle recette").classes("text-2xl font-bold")

        titre = ui.input("Titre de la recette").classes("w-full")
        description = ui.textarea("Description courte").classes("w-full")
        ingredients = ui.textarea(
            "Ingrédients (un par ligne)"
        ).classes("w-full")
        etapes = ui.textarea("Étapes de préparation (une par ligne)").classes("w-full")

        image_path_holder = {"path": None}

        def gerer_upload(e: events.UploadEventArguments):
            extension = os.path.splitext(e.name)[1]
            nom_fichier = f"{uuid.uuid4().hex}{extension}"
            chemin_complet = os.path.join(UPLOAD_DIR, nom_fichier)
            with open(chemin_complet, "wb") as f:
                f.write(e.content.read())
            image_path_holder["path"] = "/" + chemin_complet
            ui.notify("Image téléchargée avec succès.")

        ui.upload(on_upload=gerer_upload, label="Ajouter une image").classes("w-full")

        erreur_label = ui.label("").classes("text-red-600")

        def soumettre():
            if not titre.value or not ingredients.value or not etapes.value:
                erreur_label.text = "Titre, ingrédients et étapes sont obligatoires."
                return

            session = get_session()
            try:
                recette = Recette(
                    titre=titre.value,
                    description=description.value,
                    ingredients=ingredients.value,
                    etapes=etapes.value,
                    image_path=image_path_holder["path"],
                    statut="en_attente",
                    auteur_id=get_current_user_id(),
                )
                session.add(recette)
                session.commit()
            finally:
                session.close()

            ui.notify("Recette soumise ! Elle sera examinée par l'équipe du chef.")
            ui.navigate.to("/profil")

        ui.button("Soumettre la recette", on_click=soumettre)