
# Módulos
import streamlit as st
import folium
import pandas as pd
import json
from streamlit_folium import folium_static

# Configurações da página
st.set_page_config(
    layout="wide", 
    page_title="Estatística Municípios",
    page_icon="⭐",
    initial_sidebar_state="expanded"
)


# Info 
# latitude, longitude = [-27.5954, -48.5480]
locali

# Criar o mapa base
mapa = folium.Map(location=[latitude, longitude], 
                  tiles="cartodbpositron",
                  zoom_start=7
                  )

# Ler os dados do Excel
dados_estatisticos = pd.read_excel("dados.xlsx")

# Carregar o arquivo GeoJSON
with open("geojs-42-mun.json", encoding='utf-8') as f:
    dados_geograficos = json.load(f)


# Filtrar os dados para a cidade selecionada
dados_SC = dados_estatisticos[dados_estatisticos["Estado"] == "SC"]

# Adicionar o Choropleth ao mapa
folium.Choropleth(
    geo_data=dados_geograficos,
    data=dados_estatisticos,
    name="População 2022",
    legend_name="População 2022",
    columns=["Código", "Pop_2022"], 
    key_on="feature.properties.id",  
    fill_color="YlOrRd",
    nan_fill_color="black",
    highlight=True,
    fill_opacity=0.9,
    line_opacity=0.5,
).add_to(mapa)

# Adicionar os geojson
# folium.features.GeoJson(
#     dados_geograficos,
#     popup=folium.features.GeoJsonPopup(fields=["name"])
# ).add_to(mapa)

# Adicionar destaque
estilo = lambda x: {}


# Renderizar o mapa no Streamlit
# folium_static(mapa, width=640, height=480)
folium_static(mapa)


