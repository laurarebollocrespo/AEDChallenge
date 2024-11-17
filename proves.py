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

# Variable para almacenar el estado de los equipos formados
if 'equipos_formados' not in st.session_state:
    st.session_state.equipos_formados = False

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
                st.session_state.equipos_formados = False  # Reiniciar antes de formar equipos
                st.write("Procesando...")  # Mostrar mensaje mientras se procesan los equipos
                
                # Aquí llamas a tu lógica para formar los equipos, por ejemplo:
                # Formar los equipos (esto es solo un ejemplo)
                # Supón que después de un retraso simulado o lógica, los equipos se forman.
                # Actualizar el estado
                st.session_state.equipos_formados = True
                st.success("¡Equipos formados exitosamente!")
                st.write("**¡Los equipos ya han sido formados!**")

        except Exception as e:
            st.error("Hubo un error al cargar el archivo. Por favor, verifica el formato.")
            
    # Mostrar mensaje si el archivo no ha sido subido
    if st.session_state.df is None:
        st.warning("Por favor, sube el archivo JSON para poder continuar con las demás funciones.")

    # Si los equipos están formados, no mostrar "Procesando..."
    if st.session_state.equipos_formados:
        st.write("**¡Los equipos han sido formados!**")
    else:
        st.write("Haz clic en 'Formar Equipos' para comenzar.")

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
            st.header("Propuesta de Equipos")
            st.write("Aquí puedes ver nuestra propuesta de equipos.")
            if st.button("Ver equipos"):
                st.write("**Esta es nuestra propuesta de equipos:**")
                # Aquí podrías añadir más lógica para mostrar equipos formados.

# Pestaña 4: 
if len(tab_titles) > 3:  # Verifica si se deben mostrar las pestañas adicionales
    with tabs[3]:
        if st.session_state.df is None:
            st.warning("Primero debes subir los datos antes de acceder a esta pestaña.")
        else:
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

# Pestaña 5: 
if len(tab_titles) > 4:  # Verifica si se deben mostrar las pestañas adicionales
    with tabs[4]:
        if st.session_state.df is None:
            st.warning("Primero debes subir los datos antes de acceder a esta pestaña.")
        else:
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
                    objective = si['objective'].iloc[0]

                    st.write(f"**Edad:** {edad}")
                    st.write(f"**Año de estudio:** {year_of_study}")
                    st.write(f"**Nivel de experiencia:** {experience_level}")
                    st.write(f"**Objetivos:** {objective}")

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
