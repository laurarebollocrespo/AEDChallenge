import json
import pandas as pd
from typing import List, Dict

def divide_by_skill(participants_df: pd.DataFrame):
    """
    Divide a DataFrame of participants into three skill-based groups.
    
    Args:
        participants_df (DataFrame): DataFrame containing participant information.
                                     Must include 'programming_skills' as a dictionary.
    
    Returns:
        Tuple: Three DataFrames of participants for high, mid, and low skill groups.
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

def group_by_languages(participants: List[Dict]) -> List[List[Dict]]:
    """
    Agrupa a los participantes en función de los idiomas que hablan, minimizando el número de grupos.
    Los participantes sin idiomas (`preferred_languages` vacío) se distribuyen equitativamente entre los grupos existentes.

    Args:
        participants (list): Lista de diccionarios con los detalles de los participantes.

    Returns:
        List[List[Dict]]: Lista de grupos con los participantes como diccionarios.
    """
    final_groups = []
    
    # Procesar participantes con idiomas
    for participant in participants:
        languages = set(participant.get("preferred_languages", []))

        if languages:
            # Intentar añadir al participante a un grupo existente
            for group in final_groups:
                # Verificar si este participante comparte idiomas con todos los miembros del grupo
                if all(languages & set(p.get("preferred_languages", [])) for p in group):
                    group.append(participant)
                    break
            else:
                # Si no es compatible con ningún grupo, crear uno nuevo
                final_groups.append([participant])
        else:
            # Marcar participantes sin idiomas para procesar al final
            participant["no_languages"] = True
    
    # Procesar participantes sin idiomas
    no_language_participants = [p for p in participants if p.get("no_languages")]
    for participant in no_language_participants:
        # Distribuir equitativamente entre los grupos más pequeños
        smallest_group = min(final_groups, key=len)
        smallest_group.append(participant)

    return final_groups

def main():
    # Cargar los datos desde el archivo JSON
    with open("datathon_participants.json", "r") as file:
        data = json.load(file)
    
    # Convertir los datos a un DataFrame
    participants_df = pd.DataFrame(data)
    
    # Dividir a los participantes según su habilidad
    high_skill, mid_skill, low_skill = divide_by_skill(participants_df)

    # Agrupar por idiomas para cada grupo de habilidad
    high_skill_groups = group_by_languages(high_skill.to_dict(orient="records"))
    mid_skill_groups = group_by_languages(mid_skill.to_dict(orient="records"))
    low_skill_groups = group_by_languages(low_skill.to_dict(orient="records"))

    # Combinar los grupos por habilidad y por idiomas
    grouped_data = {
        "high_skill_group": high_skill_groups,
        "mid_skill_group": mid_skill_groups,
        "low_skill_group": low_skill_groups
    }

    # Guardar la salida en un archivo JSON
    with open('output_grouped_participants.json', 'w') as f:
        json.dump(grouped_data, f, indent=4)
    
    # Mostrar la salida en consola
    print(json.dumps(grouped_data, indent=4))

if __name__ == '__main__':
    main()

