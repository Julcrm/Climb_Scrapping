import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import ast

# Fonction pour charger les données
@st.cache_data
def load_data():
    return pd.read_csv("spots_grimpe.csv")

# Charger les données
df = load_data()

# Créer une carte avec un style "Stadia AlidadeSmoothDark"
map_folium = folium.Map(
    location=[46.603354, 1.888334],  # Coordonnées pour centrer la carte (par exemple, la France)
    zoom_start=6,  # Zoom initial plus large
    tiles='https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png',
    attr='&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> contributors'
)

# Ajouter les données avec FastMarkerCluster
locations = df[['coor_1', 'coor_2']].values.tolist()
marker_cluster = MarkerCluster().add_to(map_folium)

# Ajouter les marqueurs
icon_image = "https://img.icons8.com/?size=100&id=Gp8yKV8izL1K&format=png&color=000000"

# Contenu du popup avec les informations à la ligne


# Appliquer ast.literal_eval sur toutes les colonnes concernées
columns_to_convert = ["type_escalade", "public", "exposition", "saison"]
for col in columns_to_convert:
    df[col] = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

# Carte Folium
m = folium.Map(location=[44.1, 5.1], zoom_start=12)

# Boucle pour ajouter les marqueurs
for index, row in df.iterrows():
    # Construire le contenu du popup
    types = ", ".join(row["type_escalade"])  # Transformation de la liste en chaîne
    public = ", ".join(row["public"])
    exposition = ", ".join(row["exposition"])
    saison = ", ".join(row["saison"])
    
    popup_html = f"""
    <div style='width:300px'>
    <b>Nom :</b> {row['nom']}<br>
    <b>Type d'escalade :</b> {types}<br>
    <b>Difficulté :</b> {public}<br>
    <b>Exposition :</b> {exposition}<br>
    <b>Période :</b> {saison}<br>
    </div>
    """
    # Créer le marqueur avec le popup et l'icône personnalisée
    marker = folium.Marker(
        location=[row['coor_1'], row['coor_2']],
        popup= popup_html,
        icon=folium.DivIcon(
            html=f"""
            <div style="text-align: center;">
                <img src="https://img.icons8.com/?size=100&id=ng7jZBZRRJlo&format=png&color=000000" 
                    style="width: 30px; height: 30px;"><br>
            </div>
            """
        )
    )
    # Ajouter le marqueur au cluster
    marker.add_to(marker_cluster)


# Afficher la carte dans Streamlit avec un affichage plus large
st.components.v1.html(map_folium._repr_html_(), height=1100, width=1100)  # Ajuster la taille de la carte