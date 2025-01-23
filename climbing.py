import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import plotly.express as px
import ast
from folium import IFrame

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
locations = df[['latitude', 'longitude']].values.tolist()
marker_cluster = MarkerCluster().add_to(map_folium)



# Carte Folium
m = folium.Map(location=[44.1, 5.1], zoom_start=12)

columns_to_convert = ["rocks"]
for col in columns_to_convert:
    df[col] = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    

# Boucle pour ajouter les marqueurs
for index, row in df.iterrows():
    rocks = ", ".join(row["rocks"]) # Transformation de la liste en chaîne
    popup_html = f"""
    <div style='width:300px'>
    <b>Nom :</b> {row['name']}<br>
    <b>Region :</b> {row['region']}<br>
    <b>Nombre de voies :</b> {row['route_count']}<br>
    <b>Roche :</b> {rocks}<br>
    <img src="{row['photo']}" alt="Photo" width="150">
    </div>
    """

    # Créer un IFrame pour encapsuler le contenu HTML
    iframe = IFrame(popup_html, width=300, height=200)
    popup = folium.Popup(iframe, max_width=300)

    # Créer le marqueur avec le popup et l'icône personnalisée
    marker = folium.Marker(
        location=[row['latitude'], row['longitude']],
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