import streamlit as st
import matplotlib.pyplot as plt
import random
import json
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Generador de Grupos", layout="centered", page_icon="👤")

with open('datathon_participants.json', 'r') as file:
    datos = json.load(file)


st.title("Creación de Equipos para la Datathon FME")
st.write("Bienvenido a nuestra herramienta interactiva.")

if st.button("Formar Equipos"):
    st.write("Procesando...")
    # Aquí llamarías a la lógica de tu backend para formar los equipos.

if st.button("¿Cuantos equipos hay de x integrantes?"):
    miembros = {'Dos': 10, 'Tres': 15, 'Cuatro': 7}

    fig, ax = plt.subplots(figsize=(4, 2))  
    ax.bar(miembros.keys(), miembros.values())
    ax.tick_params(axis='both', labelsize=6)
    ax.bar(miembros.keys(), miembros.values(), color='#189578')

    ax.set_title("Número de integrantes", fontsize= 6)
    ax.set_xlabel("", fontsize= 6)
    ax.set_ylabel("Equipos", fontsize= 6)

    st.pyplot(fig)

if st.button("Ver equipos"):
    st.write("**Esta es nuestra propuesta de equipos:**")

if st.button("Análisis equipos"):
    st.write("**El número total de equipos es:**")

    data = {'Tryhards': 10, 'Pasarlo bien': 15, 'Hacer amigos': 7}

    fig, ax = plt.subplots(figsize=(4, 2))
    ax.bar(data.keys(), data.values())
    ax.tick_params(axis='both', labelsize=8)
    ax.bar(data.keys(), data.values(), color='#189578')

    ax.set_title("Intenciones", fontsize= 8)
    ax.set_xlabel("", fontsize= 8)
    ax.set_ylabel("Personas", fontsize= 8)

    st.pyplot(fig)

nombres = [persona['name'] for persona in datos]

# Generación de nombre aleatorio
nombre_leer = st.text_input("Introduce un nombre para saber en qué equipo va:")
if nombre_leer:
    if nombre_leer in nombres:
        st.session_state.nombre_input = nombre_leer
    else:
        st.write(f'{nombre_leer} no es miembro de ningún grupo.')

if st.button("Generar nombre aleatorio"):
    nombre_random = random.choice(nombres)
    st.session_state.nombre_input = nombre_random

df = pd.read_json("datathon_participants.json")

if 'nombre_input' in st.session_state:
    nombre = st.session_state.nombre_input

    st.write(f"**Nombre seleccionado:** {nombre}")
    st.write()
    st.write(f"**{nombre} va en el equipo con:**") # Falta relacionarlo con los grupos que hagamos.

    # Botón para mostrar más detalles
    if st.button("Mostrar más detalles"):
        si = df.loc[df['name'] == nombre]
        
        edad = si['age'].iloc[0]
        year_of_study = si['year_of_study'].iloc[0]
        experience_level = si['experience_level'].iloc[0]
        
        # Mostrar los datos en Streamlit
        st.write(f"**Edad:** {edad}")
        st.write(f"**Año de estudio:** {year_of_study}")
        st.write(f"**Nivel de experiencia:** {experience_level}")


st.markdown(
    """
    <style>
    .stButton>button {
        color: white;
        background-color: #59c8ae;
        font-size: 16px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

