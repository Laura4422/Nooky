import streamlit as st
import pandas as pd
from streamlit_authenticator import Authenticate
from streamlit_option_menu import option_menu
from PIL import Image, ExifTags

# Fonction pour lire les données des comptes à partir d'un fichier CSV
def lire_donnees_comptes(csv_file):
    df = pd.read_csv(csv_file)
    comptes = {'usernames': {}}
    for index, row in df.iterrows():
        comptes['usernames'][row['name']] = {
            'name': row['name'],
            'password': row['password'],
            'email': row['email'],
            'failed_login_attempts': row['failed_login_attempts'],
            'logged_in': row['logged_in'],
            'role': row['role']
        }
    return comptes

# Lire les données des comptes à partir du fichier CSV
lesDonneesDesComptes = lire_donnees_comptes('comptes_utilisateurs.csv')

authenticator = Authenticate(
    lesDonneesDesComptes,  # Les données des comptes
    "cookie_name",  # Le nom du cookie, un str quelconque
    "cookie_key",  # La clé du cookie, un str quelconque
    30  # Le nombre de jours avant que le cookie expire
)

# Authentification
authenticator.login()

# Fonction pour ouvrir et corriger l'orientation des images
def open_and_correct_image(image_path):
    image = Image.open(image_path)
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())
        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # Les images peuvent ne pas avoir d'informations EXIF
        pass
    return image

if "authentication_status" in st.session_state and st.session_state["authentication_status"] is not None:
    if st.session_state["authentication_status"]:
        st.sidebar.title(f"Bienvenue {st.session_state['name']}!")  # Titre de bienvenue dans la barre latérale

        # Création du menu dans la barre latérale
        selection = st.sidebar.selectbox(
            "Menu",  # Titre du menu
            ["Accueil", "Photos"]  # Options du menu
        )

        # On indique au programme quoi faire en fonction du choix
        if selection == "Accueil":
            st.title("Bienvenue sur ma page")
            st.image(open_and_correct_image("Bienvenue chez mon chat.jpg"))
        elif selection == "Photos":
            st.title("Bienvenue dans l'album photo de Nooky 🐱")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.image(open_and_correct_image("IMG_20220403_170023.jpg"))
            with col2:
                st.image(open_and_correct_image("IMG_20230813_183711.jpg"))
            with col3:
                st.image(open_and_correct_image("IMG_20240521_113557_676.jpg"))
            st.write("Trop beau, n'est-ce pas !")

        # Le bouton de déconnexion
        st.sidebar.button("Déconnexion", on_click=authenticator.logout, args=("Déconnexion",))
    else:
        st.error("L'username ou le password est/sont incorrect")
else:
    st.warning('Les champs username et mot de passe doivent être remplis')
