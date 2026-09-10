from nicegui import ui
from database import get_session
from models import Recette
from auth import est_admin, utilisateur_connecte
from pages.navbar import navbar


def page_validation_admin():
    navbar()

    if not utilisateur_connecte() or not est_admin():
        ui.label("Accès réservé à l'équipe du chef.").classes("p-8 text-red-600")
        return

    with ui.column().classes("w-full p-8 gap-4"):
        ui.label("Recettes en attente de validation").classes("text-2xl font-bold")

        container = ui.column().classes("gap-3 w-full")

        def charger():
            container.clear()
            session = get_session()
            try:
                recettes = (
                    session.query(Recette)
                    .filter_by(statut="en_attente")
                    .order_by(Recette.date_creation)
                    .all()
                )
            finally:
                session.close()

            with container:
                if not recettes:
                    ui.label("Aucune recette en attente.")
                for r in recettes:
                    with ui.card().classes("w-full"):
                        ui.label(r.titre).classes("font-bold")
                        ui.label(r.description or "")
                        with ui.row():
                            ui.button(
                                "Valider",
                                on_click=lambda r=r: changer_statut(r.id, "validee"),
                            ).classes("bg-green-600")
                            ui.button(
                                "Marquer bistronomique",
                                on_click=lambda r=r: marquer_bistronomique(r.id),
                            ).classes("bg-amber-600")
                            ui.button(
                                "Refuser",
                                on_click=lambda r=r: changer_statut(r.id, "refusee"),
                            ).classes("bg-red-600")

        def changer_statut(recette_id, statut):
            session = get_session()
            try:
                r = session.query(Recette).filter_by(id=recette_id).first()
                r.statut = statut
                session.commit()
            finally:
                session.close()
            ui.notify("Statut mis à jour.")
            charger()

        def marquer_bistronomique(recette_id):
            session = get_session()
            try:
                r = session.query(Recette).filter_by(id=recette_id).first()
                r.statut = "validee"
                r.est_bistronomique = True
                session.commit()
            finally:
                session.close()
            ui.notify("Recette marquée bistronomique et validée.")
            charger()

        charger()