from nicegui import ui
from database import get_session
from models import Recette
from pages.navbar import navbar


def page_accueil():
    navbar()

    with ui.column().classes("w-full items-center p-8 gap-6"):
        ui.label("Bienvenue sur La Brigade !").classes("text-3xl font-bold")
        ui.label(
            "Découvrez des recettes bistronomiques validées par l'équipe du chef."
        ).classes("text-gray-600")
        ui.button("Voir les recettes", on_click=lambda: ui.navigate.to("/recettes"))

        ui.label("Recettes à la une").classes("text-xl font-bold mt-8")

        session = get_session()
        try:
            recettes = (
                session.query(Recette)
                .filter_by(statut="validee")
                .order_by(Recette.date_creation.desc())
                .limit(3)
                .all()
            )
        finally:
            session.close()

        with ui.row().classes("gap-4 flex-wrap justify-center"):
            if not recettes:
                ui.label("Aucune recette validée pour le moment.")
            for r in recettes:
                with ui.card().classes("w-64"):
                    if r.image_path:
                        ui.image(r.image_path).classes("h-32 w-full object-cover")
                    ui.label(r.titre).classes("font-bold")
                    ui.label(r.description or "").classes("text-sm text-gray-500 line-clamp-2")
                    ui.button(
                        "Voir la recette",
                        on_click=lambda r=r: ui.navigate.to(f"/recette/{r.id}"),
                    )