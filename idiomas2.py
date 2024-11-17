import json
from typing import List, Dict

def find_groups(participants: List[Dict]) -> List[List[Dict]]:
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
        name = participant["name"]
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

# Cargar los datos desde el archivo JSON
'''
def main():
    # Leer el archivo JSON
    with open("datathon_participants.json", "r") as file:
        data = json.load(file)
    
    # Encontrar los grupos basados en idiomas
    groups = find_groups(data)
    
    # Mostrar los resultados en el formato de salida requerido
    output = []
    for group in groups:
        output.append([participant for participant in group])
    
    # Imprimir la salida
    print(json.dumps(output, indent=4))

if __name__ == "__main__":
    main()

'''


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

    groups1 = find_groups(high_skill)
    groups2 =find_groups(mid_skill)
    groups3 = find_groups(low_skill)
    
    # Mostrar los resultados en el formato de salida requerido
    output1 = []
    for group1 in groups1:
        output.append([participant for participant in group1])

    
    # Imprimir la salida
    print(json.dumps(output1, indent=4))

        # Mostrar los resultados en el formato de salida requerido
    output2 = []
    for group2 in groups2:
        output.append([participant for participant in group2])
    
    
    
    # Imprimir la salida
    print(json.dumps(output2, indent=4))


        # Mostrar los resultados en el formato de salida requerido
    output3 = []
    for group3 in groups3:
        output.append([participant for participant in group3])
    
    
    
    # Imprimir la salida
    print(json.dumps(output3, indent=4))
    
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