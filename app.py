import streamlit as st
import matplotlib.pyplot as plt
import random
import pandas as pd
import equips

st.set_page_config(page_title="Group Generator", layout="centered", page_icon="👤")

st.title("Team Generator for the Datathon FME")
st.write("Welcome to our interactive tool for team formation.")

df = None
if 'df' not in st.session_state:
    st.session_state.df = None

if st.session_state.df is None:
    tab_titles = ["Create teams"]
else:
    tab_titles = [
        "Create Teams",
        "The Teams",
        "Team graphs",
        "Team Analysis",
        "Search Members"
    ]


tabs = st.tabs(tab_titles)

# Pestaña 1:
with tabs[0]:
    st.header("Create teams")
    st.write("Upload a JSON file with participant data to get started.")

    file = st.file_uploader("Upload your JSON file here", type="json")

    if file is not None:
        try:
            st.session_state.df = pd.read_json(file)
            df = st.session_state.df
            st.success("File uploaded successfully!")
            
            st.write("Preview of the uploaded data:")
            st.dataframe(df.head())  
           
            if st.button("Create Teams"):
                # Llista dels equips
                grups = equips.create_teams()
                st.session_state.teams = grups
                st.success("Teams formed successfully!")
        except Exception as e:
            st.error("There was an error uploading the file. Please check the format.")
            
    if st.session_state.df is None:
        st.warning("Please upload the JSON file to continue with the other functions.")

# Pestaña 2: 
if len(tab_titles) > 1: 
    with tabs[1]:
        grups = equips.create_teams()
        st.write(f"**El nombre d'equips és:** {len(grups)}")
        st.write()

        with st.expander("View Teams"): 
            if 'df' not in st.session_state or st.session_state.df is None:
                st.warning("You must first upload the data before accessing this tab.")
            else:
                grups = equips.create_teams()
                st.header("Team Proposal")
                st.write("Here you can see the teams proposed based on the uploaded data.")
                
                
                if st.button("View Teams"):
                    # Si los equipos ya están creados en session_state, los mostramos.
                    if 'teams' in st.session_state and st.session_state.teams:
                        st.write("**This is our team proposal:**")
                        
                        for team in st.session_state.teams:
                            with st.expander(grups['team_grup']):  # Usamos expander para cada equipo
                                # Mostrar los miembros de cada equipo
                                st.write("**Members:**")
                                for member in team['members']:
                                    st.write(f"- {member}")

                    else:
                        st.warning("Teams have not been formed yet. Please upload data and generate teams.")
                

# Pestaña 3: 
if len(tab_titles) > 2: 
    with tabs[2]:
        if st.session_state.df is None:
            st.warning("You must first upload the data before accessing this tab.")
        else:
            st.header("Team Members Analysis")
            st.write("Visualize the number of teams with a specific number of members.")
            if st.button("¿How many teams have x members?"):
                miembros = {'Dos': 10, 'Tres': 15, 'Cuatro': 7}

                fig, ax = plt.subplots(figsize=(4, 2))
                ax.bar(miembros.keys(), miembros.values(), color='#189578')
                ax.tick_params(axis='both', labelsize=6)
                ax.set_title("Number of Members", fontsize=6)
                ax.set_xlabel("", fontsize=6)
                ax.set_ylabel("Teams", fontsize=6)

                st.pyplot(fig)

# Pestaña 4: 
if len(tab_titles) > 3:  
    with tabs[3]:
        if st.session_state.df is None:
            st.warning("You must first upload the data before accessing this tab.")
        else:
            st.header("Analysis by Intentions")
            st.write("Visualize the teams based on their main intentions.")
            
            data = {'Tryhards': 10, 'Having fun': 15, 'Making friends': 7}

            fig, ax = plt.subplots(figsize=(4, 2))
            ax.bar(data.keys(), data.values(), color='#189578')
            ax.tick_params(axis='both', labelsize=8)
            ax.set_title("Intentions", fontsize=8)
            ax.set_xlabel("", fontsize=8)
            ax.set_ylabel("People", fontsize=8)

            st.pyplot(fig)

# Pestaña 5: 
if len(tab_titles) > 4: 
    with tabs[4]:
        if st.session_state.df is None:
            st.warning("You must first upload the data before accessing this tab.")
        else:
            st.header("Search for a Member in a Team")
            st.write("Enter a name or generate a random one to see which team they are in.")
            
            nombre_leer = st.text_input("Enter a name to see which team they belong to:")
            if nombre_leer:
                if nombre_leer in df['name'].tolist():
                    st.session_state.nombre_input = nombre_leer
                else:
                    st.write(f'{nombre_leer} is not a member of any group.')

            if st.button("Generate random name"):
                nombre_random = random.choice(df['name'].tolist())
                st.session_state.nombre_input = nombre_random

            if 'nombre_input' in st.session_state:
                nombre = st.session_state.nombre_input

                st.write(f"**Selected name:** {nombre}")
                st.write(f"**{nombre}'s teammates:**")  # Enlazar con el equipo correspondiente.

                if st.button("Show more details"):
                    si = df.loc[df['name'] == nombre]
                    edad = si['age'].iloc[0]
                    year_of_study = si['year_of_study'].iloc[0]
                    experience_level = si['experience_level'].iloc[0]
                    objective = si['objective'].iloc[0]

                    st.write(f"**Age:** {edad}")
                    st.write(f"**Year of study:** {year_of_study}")
                    st.write(f"**Experience level:** {experience_level}")
                    st.write(f"**Objectives:** {objective}")


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