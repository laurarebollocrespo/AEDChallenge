import streamlit as st
import matplotlib.pyplot as plt
import random
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Generador de Grupos", layout="centered", page_icon="👤")

# Cargar datos
df = pd.read_json("datathon_participants.json")

# Título principal
st.title("Creación de Equipos para la Datathon FME")
st.write("Bienvenido a nuestra herramienta interactiva para la formación de equipos.")

# Crear pestañas para organizar la interfaz
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Formar Equipos",
    "Gráficas de Equipos",
    "Ver Equipos",
    "Análisis de Equipos",
    "Buscar Miembros"
])

# Pestaña 1: Formar equipos
with tab1:
    st.header("Formar Equipos")
    st.write("Haz clic en el botón para generar equipos.")
    if st.button("Formar Equipos"):
        st.write("Procesando...")
        # Aquí llamarías a la lógica de tu backend para formar los equipos.

# Pestaña 2: Gráficas de Equipos
with tab2:
    st.header("Análisis de Integrantes por Equipo")
    st.write("Visualiza la cantidad de equipos con un número específico de integrantes.")
    if st.button("¿Cuántos equipos hay de x integrantes?"):
        miembros = {'Dos': 10, 'Tres': 15, 'Cuatro': 7}

        fig, ax = plt.subplots(figsize=(4, 2))
        ax.bar(miembros.keys(), miembros.values(), color='#189578')
        ax.tick_params(axis='both', labelsize=6)
        ax.set_title("Número de integrantes", fontsize=6)
        ax.set_xlabel("", fontsize=6)
        ax.set_ylabel("Equipos", fontsize=6)

        st.pyplot(fig)

# Pestaña 3: Ver equipos
with tab3:
    st.header("Propuesta de Equipos")
    st.write("Aquí puedes ver nuestra propuesta de equipos.")
    if st.button("Ver equipos"):
        st.write("**Esta es nuestra propuesta de equipos:**")
        # Aquí podrías añadir más lógica para mostrar equipos formados.

# Pestaña 4: Análisis de equipos
with tab4:
    st.header("Análisis por Intenciones")
    st.write("Visualiza la cantidad de equipos según sus intenciones principales.")
    if st.button("Análisis equipos"):
        data = {'Tryhards': 10, 'Pasarlo bien': 15, 'Hacer amigos': 7}

        fig, ax = plt.subplots(figsize=(4, 2))
        ax.bar(data.keys(), data.values(), color='#189578')
        ax.tick_params(axis='both', labelsize=8)
        ax.set_title("Intenciones", fontsize=8)
        ax.set_xlabel("", fontsize=8)
        ax.set_ylabel("Personas", fontsize=8)

        st.pyplot(fig)

# Pestaña 5: Buscar miembros
with tab5:
    st.header("Buscar Miembro en un Equipo")
    st.write("Introduce un nombre o genera uno aleatorio para saber en qué equipo está.")

    # Campo para buscar por nombre
    nombre_leer = st.text_input("Introduce un nombre para saber en qué equipo va:")
    if nombre_leer:
        if nombre_leer in df['name'].tolist():
            st.session_state.nombre_input = nombre_leer
        else:
            st.write(f'{nombre_leer} no es miembro de ningún grupo.')

    # Botón para generar un nombre aleatorio
    if st.button("Generar nombre aleatorio"):
        nombre_random = random.choice(df['name'].tolist())
        st.session_state.nombre_input = nombre_random

    # Mostrar información del miembro seleccionado
    if 'nombre_input' in st.session_state:
        nombre = st.session_state.nombre_input

        st.write(f"**Nombre seleccionado:** {nombre}")
        st.write(f"**{nombre} va en el equipo con:**")  # Aquí puedes enlazarlo con el equipo correspondiente.

        # Mostrar más detalles del miembro
        if st.button("Mostrar más detalles"):
            si = df.loc[df['name'] == nombre]
            edad = si['age'].iloc[0]
            year_of_study = si['year_of_study'].iloc[0]
            experience_level = si['experience_level'].iloc[0]

            st.write(f"**Edad:** {edad}")
            st.write(f"**Año de estudio:** {year_of_study}")
            st.write(f"**Nivel de experiencia:** {experience_level}")

# Estilo personalizado para los botones
st.markdown(
    """
    <style>
    .stButton>button {
        color: white;
        background-color: #59c8ae;
        font-size: 16px;
        border-radius: 10px;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
