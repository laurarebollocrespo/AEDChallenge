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
        "Skills Analysis",
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
        st.session_state.teams = grups

        if st.session_state.df is None:
            st.warning("You must first upload the data before accessing this tab.")
        else:
            st.header("The Teams")
            st.write("Below are the teams formed based on the uploaded data.")

            if "teams" not in st.session_state or not st.session_state.teams:
                st.warning("Teams have not been formed yet. Please go to 'Create Teams' and generate teams.")
            else:
                team_input = st.text_input("Enter the team number to view details:", "")

                if team_input:
                    if team_input.isdigit():
                        team_number = int(team_input)
                        if 1 <= team_number <= len(st.session_state.teams):
                            selected_team_data = st.session_state.teams[team_number - 1]
                            st.subheader(f"Details of Team {team_number}")
                            st.write("**Members:**")
                            for member in selected_team_data["members"]:
                                st.write(f"- {member}")
                        else:
                            st.warning(f"Team {team_number} does not exist. Please enter a number between 1 and {len(st.session_state.teams)}.")
                    else:
                        st.warning("Please enter a valid number.")

                for i, team in enumerate(st.session_state.teams):
                    team_name = f"Team {i+1}" if not team.get("team_group") else team["team_group"]
                    with st.expander(team_name):
                        st.write("**Members:**")
                        for member in team["members"]:
                            st.write(f"- {member}")          

# Pestaña 3: 
if len(tab_titles) > 2: 
    with tabs[2]:
        if st.session_state.df is None:
            st.warning("You must first upload the data before accessing this tab.")
        else:
            st.header("Participants Analysis")
            st.write("A continuación, podréis ver un resumen de las características de los participantes.")

            df = st.session_state.df

            # Experience Level of Participants (Graphic)
            level_order = ["Beginner", "Intermediate", "Advanced"]
            niveles = df['experience_level'].value_counts().reindex(level_order, fill_value=0)
            fig1, ax1 = plt.subplots(figsize=(4, 3))
            ax1.bar(niveles.index, niveles.values, color='#189578')
            ax1.set_title("Experience Level of Participants", fontsize=10)
            ax1.set_xlabel("Experience Level", fontsize=8)
            ax1.set_ylabel("Number of Participants", fontsize=8)
            st.pyplot(fig1)
            st.write()
            st.write()

            # Year of Study (Graphic)
            year_order = ["1st year", "2nd year", "3rd year", "4th year", "Masters", "PhD"]
            years = df['year_of_study'].value_counts().reindex(year_order, fill_value=0)
            fig3, ax3 = plt.subplots(figsize=(4, 3))
            ax3.bar(years.index, years.values, color='#189578')
            ax3.set_title("Year of Study of Participants", fontsize=10)
            ax3.set_xlabel("Year of Study", fontsize=8)
            ax3.set_ylabel("Number of Participants", fontsize=8)
            ax3.tick_params(axis='x', rotation=45)
            st.pyplot(fig3)

            # Summary of the TOP interests
            intereses = df.explode('interests')['interests'].value_counts().head(10)
            st.subheader("Top Interests of Participants")
            for i, (interest, count) in enumerate(intereses.items(), start=1):
                st.write(f"{i}. {interest}: {count} participants")

# Pestaña 4: 
if len(tab_titles) > 3:  
    with tabs[3]:
        if st.session_state.df is None:
            st.warning("You must first upload the data before accessing this tab.")
        else:
            st.header("Search for a Member in a Team")
            st.write("Enter a name or generate a random one to see which team they are in.")
            
            nombre_leer = st.text_input("Enter a name to see which team they belong to:")
            if nombre_leer:
                if nombre_leer in st.session_state.df['name'].tolist():
                    st.session_state.nombre_input = nombre_leer
                else:
                    st.warning(f'{nombre_leer} is not a member of any group.')

            if st.button("Generate random name"):
                nombre_random = random.choice(st.session_state.df['name'].tolist())
                st.session_state.nombre_input = nombre_random

            if 'nombre_input' in st.session_state:
                nombre = st.session_state.nombre_input

                found_team = None
                for team in st.session_state.teams:
                    if nombre in team["members"]:
                        found_team = team
                        break

                if found_team:
                    st.write(f"**Selected name:** {nombre}")
                    st.write(f"**Team Name:** {found_team['team_group']}")
                    st.write(f"**Teammates:**")
                    for member in found_team["members"]:
                        if member != nombre: 
                            st.write(f"- {member}")
                else:
                    st.warning(f"{nombre} is not assigned to any team.")

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