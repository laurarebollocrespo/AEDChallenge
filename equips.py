import pandas as pd
import json

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
    Form teams from participants in all skill groups and return a JSON-like structure with sequential team names.
    
    Args:
        high_skill, mid_skill, low_skill (list): Lists of participant names grouped by skill levels.
        max_team_size (int): Maximum size of each team.
    
    Returns:
        List: List of dictionaries with team names and members.
    """
    def form_teams_from_group(group):
        teams = []
        while group:
            team_members = []
            while len(team_members) < max_team_size and group:
                team_members.append(group.pop(0))  # Add participant to the team
            teams.append(team_members)
        return teams

    # Combine all groups and form teams
    combined_groups = high_skill + mid_skill + low_skill
    all_teams = form_teams_from_group(combined_groups)
    
    # Create JSON-like structure
    teams_json = [
        {"team_group": f"Team {i + 1}", "members": team}
        for i, team in enumerate(all_teams)
    ]
    
    return teams_json

def create_teams():
    # Create a pandas DataFrame
    participants_df = pd.read_json("datathon_participants.json")

    # Divide participants into skill groups
    high_skill, mid_skill, low_skill = divide_by_skill(participants_df)

    # Form teams and return JSON-like structure
    teams_by_skill = form_teams_by_skill(high_skill, mid_skill, low_skill)
    
    return teams_by_skill  # Convert to JSON string for readability

print (create_teams())