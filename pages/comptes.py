from nicegui import ui
from auth import creer_utilisateur, authentifier, connecter_session
from pages.navbar import navbar


def page_connexion():
    navbar()
    with ui.column().classes("w-full items-center p-8 gap-3"):
        ui.label("Connexion").classes("text-2xl font-bold")
        email = ui.input("Email").classes("w-80")
        password = ui.input("Mot de passe", password=True).classes("w-80")
        erreur_label = ui.label("").classes("text-red-600")

        def se_connecter():
            user, erreur = authentifier(email.value, password.value)
            if erreur:
                erreur_label.text = erreur
                return
            connecter_session(user)
            ui.navigate.to("/")

        ui.button("Se connecter", on_click=se_connecter)


def page_inscription():
    navbar()
    with ui.column().classes("w-full items-center p-8 gap-3"):
        ui.label("Créer un compte").classes("text-2xl font-bold")
        nom = ui.input("Nom").classes("w-80")
        email = ui.input("Email").classes("w-80")
        password = ui.input("Mot de passe", password=True).classes("w-80")
        erreur_label = ui.label("").classes("text-red-600")

        def s_inscrire():
            if not nom.value or not email.value or not password.value:
                erreur_label.text = "Tous les champs sont obligatoires."
                return
            user, erreur = creer_utilisateur(nom.value, email.value, password.value)
            if erreur:
                erreur_label.text = erreur
                return
            connecter_session(user)
            ui.navigate.to("/")

        ui.button("S'inscrire", on_click=s_inscrire)