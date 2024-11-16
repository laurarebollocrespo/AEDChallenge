import streamlit as st
import matplotlib.pyplot as plt
import random

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
    st.write("Esta es nuestra propuesta de equipos:")

if st.button("Análisis equipos"):
    st.write("El número total de equipos es:")

    data = {'Tryhards': 10, 'Pasarlo bien': 15, 'Hacer amigos': 7}

    fig, ax = plt.subplots(figsize=(4, 2))
    ax.bar(data.keys(), data.values())
    ax.tick_params(axis='both', labelsize=8)
    ax.bar(data.keys(), data.values(), color='#189578')

    ax.set_title("Intenciones", fontsize= 8)
    ax.set_xlabel("", fontsize= 8)
    ax.set_ylabel("Personas", fontsize= 8)

    st.pyplot(fig)



# Nombres que tengamos en la base de datos
nombres = ['Carlos', 'Ana', 'Pedro', 'María', 'Juan', 'Sofia']

# Por si quieres poner tu el nombre.
nombre_input = st.text_input("Introduce un nombre para saber en qué equipo va:")

if st.button("Generar nombre aleatorio"):
    nombre_random = random.choice(nombres) 
    nombre_input = nombre_random 

if nombre_input:
    st.write(f"Nombre seleccionado: {nombre_input}")
    st.write()
    st.write(f"{nombre_input} va en el equipo con:") # Falta relacionarlo con los grupos que hagamos.

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

