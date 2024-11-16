import streamlit as st

st.title("Sistema de Formación de Equipos para la Datathon FME")
st.write("Bienvenido a nuestra herramienta interactiva.")

# Personal data
st.sidebar.title("Información del Participante")
name = st.sidebar.text_input("Nombre")
email = st.sidebar.text_input("Email")
age = st.sidebar.number_input("Edad", min_value=16, max_value=100, step=1, value=16)
year_of_study = st.sidebar.selectbox("Ocupación", ["1st year", "2nd year", "3rd year", "4th year", "Masters", "PhD"])
shirt_size = st.sidebar.selectbox("¿Qué talla de camiseta quieres?", ["S", "M", "L", "XL"])
university = st.sidebar.text_input("En el caso de ser estudiante, ¿en qué universidad estudias?")
dietary_restrictions = st.sidebar.selectbox("¿Tienes alguna restricción alimentaria?", ["None", "Vegetarian", "Vegan", "Gluten-free", "Other"])



rol = st.sidebar.selectbox("Rol", ["Data Scientist", "Ingeniero", "Analista", "Otro"])
experiencia = st.sidebar.slider("Experiencia (años):", 0, 10)
objetivos = st.sidebar.text_area("Describe tus objetivos:")

if st.button("Formar Equipos"):
    st.write("Procesando...")
    # Aquí llamarías a la lógica de tu backend para formar los equipos.
