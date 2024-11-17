import json
from typing import List

def find_groups(participants):
    """
    Agrupa a los participantes según los idiomas que hablan. 
    Todos los participantes de un grupo deben compartir al menos un idioma común con todos los demás del grupo.
    
    Args:
        participants (list): Lista de diccionarios con los detalles de los participantes. Cada participante tiene un campo 'preferred_languages'.
    
    Returns:
        List[List[str]]: Listado de grupos con los nombres de los participantes que comparten al menos un idioma.
    """
    # Crear una lista de grupos vacíos
    groups = []
    
    # Usaremos un conjunto para asegurarnos de que no repetimos participantes en los grupos
    visited = set()
    
    # Función auxiliar para buscar el grupo de un participante mediante DFS
    def dfs(participant_idx, group_idx):
        # Marcamos el participante como visitado
        visited.add(participant_idx)
        groups[group_idx].append(participants[participant_idx]['name'])
        
        # Verificamos con qué otros participantes comparte al menos un idioma
        for i, participant in enumerate(participants):
            if i not in visited and any(lang in participants[participant_idx]['preferred_languages'] for lang in participant['preferred_languages']):
                dfs(i, group_idx)

    # Iteramos sobre todos los participantes
    for i, participant in enumerate(participants):
        if i not in visited:
            # Creamos un nuevo grupo
            groups.append([])
            # Iniciamos DFS para encontrar todos los participantes conectados
            dfs(i, len(groups) - 1)
    
    # Ahora aseguramos que los grupos son coherentes: 
    # Verificamos que todos los miembros de cada grupo comparten al menos un idioma entre ellos.
    final_groups = []
    
    for group in groups:
        # Extraemos los idiomas de todos los miembros del grupo
        if len(group) > 1:
            group_languages = [set(participants[i]['preferred_languages']) for i in range(len(participants)) if participants[i]['name'] in group]
            common_languages = set.intersection(*group_languages)
            if common_languages:
                final_groups.append(group)
    
    # Ahora asignamos a los participantes sin idiomas al grupo con menos personas
    no_language_participants = [i for i, p in enumerate(participants) if not p['preferred_languages']]
    
    # Creamos un conjunto para asegurarnos de no añadir dos veces a la misma persona
    for participant_idx in no_language_participants:
        # Encontramos el grupo con menos participantes (con al menos dos personas)
        smallest_group = final_groups
        smallest_group.append(participants[participant_idx]['name'])

    # Eliminar grupos que tienen solo un participante (si los hubiera)
    final_groups = [group for group in final_groups if len(group) > 1]
    
    return final_groups

# Cargar los datos desde el archivo JSON
def main():
    # Leer el archivo JSON
    with open("datathon_participants.json", "r") as file:
        data = json.load(file)
    
    # Encontrar los grupos de participantes que hablan al menos un idioma común
    groups = find_groups(data)
    
    # Mostrar los resultados
    for i, group in enumerate(groups, 1):
        print(f"Group {i}: {group}")

if __name__ == "__main__":
    main()

