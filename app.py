
# bibliotecas
import streamlit as st
import pandas as pd
import folium 
import openpyxl
from streamlit_folium import folium_static


# importar dados
dados_municipios = pd.read_excel("dados-dos-municipios.xlsx", engine="openpyxl")
cod_estados = pd.read_excel("codigo-estados.xlsx", engine="openpyxl")
coordenadas = pd.read_excel("coordenadas-dos-estados.xlsx", engine="openpyxl")


# config
st.set_page_config(
    
    layout="wide", 
    page_title="Estatística dos Municípios",
    page_icon="⭐",
    initial_sidebar_state="expanded"
    
)

# título
st.title("Estatística dos Municípios Brasileiros")


#### CONFIGURAR MAPA #### 

# botões de seleção
estatistica = st.selectbox("Estatística:", dados_municipios.columns[4:len(dados_municipios)])
estado = st.sidebar.radio("Estado:", dados_municipios["Estado Nome"].unique())

# filtro seleção
filtro_estado = dados_municipios[dados_municipios["Estado Nome"] == estado]["Estado Sigla"].unique()[0]
filtro_geo = cod_estados[cod_estados["Estado Sigla"] == filtro_estado]["Código"].unique()[0]

# coordenadas
latitude = coordenadas[coordenadas["Estado Sigla"] == filtro_estado]["Latitude"].iloc[0]
longitude = coordenadas[coordenadas["Estado Sigla"] == filtro_estado]["Longitude"].iloc[0]

# gerar mapa
mapa = folium.Map(
    [latitude, longitude], 
    zoom_start=7, 
    tiles="cartodbpositron" 
    )

# filtros
dados_geograficos_filtro = "https://raw.githubusercontent.com/tbrugz/geodata-br/refs/heads/master/geojson/geojs-" + str(filtro_geo) + "-mun.json"
dados_municipios_filtro = dados_municipios[dados_municipios["Estado Sigla"] == filtro_estado]

# mapa coropletico
folium.Choropleth(
    
    geo_data = dados_geograficos_filtro,
    data = dados_municipios_filtro,
    columns = ["Código", estatistica],
    key_on = "feature.properties.id",
    fill_color = "GnBu",
    fill_opacity = 0.9,
    line_opacity = 0.5,
    legend_name = estatistica,
    nan_fill_color = "white",
    name = "Dados"
    
    ).add_to(mapa)

# adicionando estilo
estilo = lambda x: {
    "fillColor": "white",
    "color": "black",
    "fillOpacity": 0.001,
    "weight": 0.001
    }

estilo_destaque = lambda x: {
    "fillColor": "darkblue",
    "color": "black",
    "fillOpacity": 0.5,
    "weight": 1
    }

highlight = folium.features.GeoJson(
    data = dados_geograficos_filtro,
    style_function = estilo,
    highlight_function = estilo_destaque,
    name = "Destaque"
    )

mapa.add_child(highlight)

# adicionando caixa de texto
folium.features.GeoJsonTooltip(
    fields = ["name"],
    aliases = ["Município"],
    labels = False,
    style = ("background-color: white; color: black; font-family: arial; font-size: 12px; padding: 10px;")
    ).add_to(highlight)

# Exibindo o mapa no Streamlit
folium_static(mapa, width=850, height=500)






