import pandas as pd
import json

def divide_by_skill(participants_df):
    """
    Divide a DataFrame of participants into three skill-based groups.
    
    Args:
        participants_df (DataFrame): DataFrame containing participant information.
                                     Must include 'programming_skills' as a dictionary.
    
    Returns:
        Tuple: Three lists of participants for high, mid, and low skill groups.
    """
    # Calcular la habilidad promedio para cada participante
    participants_df["average_skill"] = participants_df["programming_skills"].apply(
        lambda skills: sum(skills.values()) / len(skills) if skills else 0
    )
    
    # Ordenar por habilidad promedio en orden descendente
    sorted_df = participants_df.sort_values(by="average_skill", ascending=False)
    
    # Dividir a los participantes en tres grupos según la habilidad promedio
    total = len(sorted_df)
    high_skill = sorted_df.iloc[: total // 3]
    mid_skill = sorted_df.iloc[total // 3 : 2 * total // 3]
    low_skill = sorted_df.iloc[2 * total // 3 :]
    
    return high_skill, mid_skill, low_skill

def main():
    # Cargar los datos desde el archivo JSON
    with open("datathon_participants.json", "r") as file:
        data = json.load(file)
    
    # Convertir los datos a un DataFrame
    participants_df = pd.DataFrame(data)
    
    # Dividir a los participantes según su habilidad
    high_skill, mid_skill, low_skill = divide_by_skill(participants_df)
    
    # Organizar los grupos según habilidad
    grouped_data = {
        "high_skill_group": high_skill.to_dict(orient="records"),
        "mid_skill_group": mid_skill.to_dict(orient="records"),
        "low_skill_group": low_skill.to_dict(orient="records")
    }
    
    # Guardar la salida en un archivo JSON
    with open('output_grouped_participants.json', 'w') as f:
        json.dump(grouped_data, f, indent=4)
    
    # Mostrar la salida en consola
    print(json.dumps(grouped_data, indent=4))

if __name__ == '__main__':
    main()

