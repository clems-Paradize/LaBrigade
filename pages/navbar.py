from nicegui import ui
from auth import utilisateur_connecte, est_admin, deconnecter_session


def navbar():
    with ui.header().classes("items-center justify-between bg-red-700"):
        with ui.row().classes("items-center gap-4"):
            ui.label("🧑‍🍳 La Brigade").classes("text-xl font-bold text-white")
            ui.link("Accueil", "/").classes("text-white")
            ui.link("Recettes", "/recettes").classes("text-white")
            if utilisateur_connecte():
                ui.link("Proposer une recette", "/proposer").classes("text-white")
                ui.link("Mon profil", "/profil").classes("text-white")
                if est_admin():
                    ui.link("Validation", "/admin").classes("text-white")

        with ui.row().classes("items-center gap-2"):
            if utilisateur_connecte():
                ui.button("Déconnexion", on_click=lambda: (
                    deconnecter_session(), ui.navigate.to("/")
                ))
            else:
                ui.link("Connexion", "/connexion").classes("text-white")
                ui.link("Inscription", "/inscription").classes("text-white")