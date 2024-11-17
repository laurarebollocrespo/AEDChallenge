import streamlit as st
import matplotlib.pyplot as plt
import random
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Generador de Grupos", layout="centered", page_icon="👤")

# Título y bienvenida
st.title("Creación de equipos para la Datathon FME")
st.write("Bienvenido a nuestra herramienta interactiva para la formación de equipos.")

# Variable para almacenar los datos
df = None

# Comprobar si los datos han sido cargados
if 'df' not in st.session_state:
    st.session_state.df = None

# Pestañas: Controlamos el acceso a ellas
if st.session_state.df is None:
    tab_titles = ["Subir Datos y Crear Equipos"]
else:
    tab_titles = [
        "Subir Datos y Crear Equipos",
        "Gráficas de Equipos",
        "Ver Equipos",
        "Análisis de Equipos",
        "Buscar Miembros"
    ]

# Usa un número variable de pestañas
tabs = st.tabs(tab_titles)

# Pestaña 1: Subir datos y formar equipos
with tabs[0]:
    st.header("Subir Datos y Formar Equipos")
    st.write("Sube un archivo JSON con los datos de los participantes para comenzar.")

    # Campo para subir archivo
    file = st.file_uploader("Sube tu archivo JSON aquí", type="json")

    if file is not None:
        try:
            # Leer los datos subidos
            st.session_state.df = pd.read_json(file)
            df = st.session_state.df
            st.success("¡Archivo cargado exitosamente!")
            
            # Mostrar los datos cargados
            st.write("Vista previa de los datos cargados:")
            st.dataframe(df.head())
            
            # Botón para formar equipos
            if st.button("Formar Equipos"):
                st.write("Procesando...")
                st.success("¡Equipos formados exitosamente!")
        except Exception as e:
            st.error("Hubo un error al cargar el archivo. Por favor, verifica el formato.")
            
    # Mostrar mensaje si el archivo no ha sido subido
    if st.session_state.df is None:
        st.warning("Por favor, sube el archivo JSON para poder continuar con las demás funciones.")

# Pestaña 2: Gráficas de equipos
if len(tab_titles) > 1:  # Verifica si se deben mostrar las pestañas adicionales
    with tabs[1]:
        if st.session_state.df is None:
            st.warning("Primero debes subir los datos antes de acceder a esta pestaña.")
        else:
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

# Pestaña 3: 
if len(tab_titles) > 2:  # Verifica si se deben mostrar las pestañas adicionales
    with tabs[2]:
        if st.session_state.df is None:
            st.warning("Primero debes subir los datos antes de acceder a esta pestaña.")
        else:
