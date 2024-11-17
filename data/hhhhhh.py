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

import json

# Leer el archivo JSON
with open("datathon_participants.json", "r") as file:
    data = json.load(file)

# Crear un DataFrame de pandas
participants_df = pd.DataFrame(data)


# Dividir participantes en grupos de habilidades
high_skill, mid_skill, low_skill = divide_by_skill(participants_df)

# Mostrar los resultados
'''
print("High Skill Group:", high_skill)
print("Mid Skill Group:", mid_skill)
print("Low Skill Group:", low_skill)

'''
participants = pd.read_json("data/datathon_participants.json")
 # Dividir en tres grupos por habilidad
high_skill, mid_skill, low_skill = divide_by_skill(participants)

