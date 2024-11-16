import streamlit as st
import matplotlib.pyplot as plt

st.title("Creación de Equipos para la Datathon FME")
st.write("Bienvenido a nuestra herramienta interactiva.")

if st.button("Formar Equipos"):
    st.write("Procesando...")
    # Aquí llamarías a la lógica de tu backend para formar los equipos.
    
    

if st.button("¿Cuantos equipos hay de x integrantes?"):
    # Datos de ejemplo
    miembros = {'Dos': 10, 'Tres': 15, 'Cuatro': 7}

    fig, ax = plt.subplots(figsize=(4, 2))  # Tamaño ajustado (4 pulgadas de ancho por 2 de alto)
    ax.bar(miembros.keys(), miembros.values())
    ax.tick_params(axis='both', labelsize=6)
    ax.bar(miembros.keys(), miembros.values(), color='#189578')

    # Agregar título y etiquetas
    ax.set_title("Número de integrantes", fontsize= 6)
    ax.set_xlabel("", fontsize= 6)
    ax.set_ylabel("Equipos", fontsize= 6)

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

if st.button("Análisis equipos"):
    # Datos de ejemplo
    data = {'Tryhards': 10, 'Pasarlo bien': 15, 'Hacer amigos': 7}

    # Crear el gráfico con un tamaño más pequeño
    fig, ax = plt.subplots(figsize=(4, 2))  # Tamaño ajustado (6 pulgadas de ancho por 4 de alto)
    ax.bar(data.keys(), data.values())
    ax.tick_params(axis='both', labelsize=8)
    ax.bar(data.keys(), data.values(), color='#189578')

    # Agregar título y etiquetas
    ax.set_title("Intenciones", fontsize= 8)
    ax.set_xlabel("", fontsize= 8)
    ax.set_ylabel("Personas", fontsize= 8)

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

email = st.text_input("¿Qué equipo quieres analizar?")

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

