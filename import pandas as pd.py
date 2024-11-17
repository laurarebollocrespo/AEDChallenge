import pandas as pd

def divide_by_skill(participants_df):
    """
    Divide a DataFrame of participants into three skill-based groups.
    
    Args:
        participants_df (DataFrame): DataFrame containing participant information.
                                     Must include 'programming_skills' as a dictionary.
    
    Returns:
        Tuple: Three lists of participant names for high, mid, and low skill groups.
    """
    # Calcular la habilidad promedio para cada participante
    participants_df["average_skill"] = participants_df["programming_skills"].apply(
        lambda skills: sum(skills.values()) / len(skills) if skills else 0
    )
    
    # Ordenar por habilidad promedio en orden descendente
    sorted_df = participants_df.sort_values(by="average_skill", ascending=False)
    
    # Dividir a los participantes en tres grupos según la habilidad promedio
    total = len(sorted_df)
    high_skill = sorted_df.iloc[: total // 3]["name"].tolist()
    mid_skill = sorted_df.iloc[total // 3 : 2 * total // 3]["name"].tolist()
    low_skill = sorted_df.iloc[2 * total // 3 :]["name"].tolist()
    
    return high_skill, mid_skill, low_skill

def form_teams_by_skill(high_skill, mid_skill, low_skill, max_team_size=4):
    """
    Form teams from participants in each skill group.
    
    Args:
        high_skill, mid_skill, low_skill (list): Lists of participant names grouped by skill levels.
        max_team_size (int): Maximum size of each team.
    
    Returns:
        Dict: Dictionary with teams for each skill group.
    """
    def form_teams_from_group(group):
        teams = []
        while group:
            team = []
            while len(team) < max_team_size and group:
                team.append(group.pop(0))  # Añadir participante al equipo
            teams.append(team)
        return teams
    
    # Formar equipos por cada grupo de habilidad
    high_skill_teams = form_teams_from_group(high_skill)
    mid_skill_teams = form_teams_from_group(mid_skill)
    low_skill_teams = form_teams_from_group(low_skill)
    
    return {
        "High Skill": high_skill_teams,
        "Mid Skill": mid_skill_teams,
        "Low Skill": low_skill_teams
    }


import json

# Leer el archivo JSON
with open("datathon_participants.json", "r") as file:
    data = json.load(file)

# Crear un DataFrame de pandas
participants_df = pd.DataFrame(data)

# Dividir participantes en grupos de habilidades
high_skill, mid_skill, low_skill = divide_by_skill(participants_df)

# Formar equipos por habilidad
teams_by_skill = form_teams_by_skill(high_skill, mid_skill, low_skill)

print (teams_by_skill)
# Mostrar los equipos formados por habilidad
for skill_level, teams in teams_by_skill.items():
    print(f"\nEquipos de habilidad {skill_level}:")
    for i, team in enumerate(teams, 1):
        print(f"  Equipo {i}: {', '.join(team)}")