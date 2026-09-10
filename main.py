from nicegui import ui

from database import init_db
from pages.accueil import page_accueil
from pages.comptes import page_connexion, page_inscription
from pages.liste_recettes import page_liste_recettes
from pages.detail_recette import page_detail_recette
from pages.proposer_recette import page_proposer_recette
from pages.profil import page_profil
from pages.validation_admin import page_validation_admin


@ui.page("/")
def accueil():
    page_accueil()


@ui.page("/connexion")
def connexion():
    page_connexion()


@ui.page("/inscription")
def inscription():
    page_inscription()


@ui.page("/recettes")
def recettes():
    page_liste_recettes()


@ui.page("/recette/{recette_id}")
def detail(recette_id: int):
    page_detail_recette(recette_id)


@ui.page("/proposer")
def proposer():
    page_proposer_recette()


@ui.page("/profil")
def profil():
    page_profil()


@ui.page("/admin")
def admin():
    page_validation_admin()


if __name__ in {"__main__", "__mp_main__"}:
    init_db()
    ui.run(
        title="La Brigade",
        storage_secret="changez-cette-cle-secrete-en-production",
    )