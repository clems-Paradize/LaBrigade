from nicegui import ui
from database import get_session
from models import Recette
from pages.navbar import navbar


def page_liste_recettes():
    navbar()

    with ui.column().classes("w-full p-8 gap-4"):
        ui.label("Toutes les recettes").classes("text-2xl font-bold")

        cartes_container = ui.row().classes("gap-4 flex-wrap")

        def charger(filtre_texte: str = ""):
            cartes_container.clear()
            session = get_session()
            try:
                query = session.query(Recette).filter_by(statut="validee")
                if filtre_texte:
                    query = query.filter(Recette.titre.ilike(f"%{filtre_texte}%"))
                recettes = query.order_by(Recette.date_creation.desc()).all()
            finally:
                session.close()

            with cartes_container:
                if not recettes:
                    ui.label("Aucune recette trouvée.")
                for r in recettes:
                    with ui.card().classes("w-64"):
                        if r.image_path:
                            ui.image(r.image_path).classes("h-32 w-full object-cover")
                        ui.label(r.titre).classes("font-bold")
                        note = r.note_moyenne
                        ui.label(f"⭐ {note}/5" if note else "Pas encore noté")
                        ui.button(
                            "Voir la recette",
                            on_click=lambda r=r: ui.navigate.to(f"/recette/{r.id}"),
                        )

        recherche = ui.input(
            "Rechercher une recette", on_change=lambda e: charger(e.value)
        ).classes("w-96")

        charger()