import numpy as np
import pandas as pd
from typing import List, Dict
from dataclasses import dataclass
from transformers import pipeline
from typing import Dict, List
import uuid
import json
from math import sqrt
from collections import defaultdict

@dataclass
class Participant:
    id: uuid.UUID
    name: str
    year_of_study: str
    programming_skills: Dict[str, int]
    experience_level: str
    hackathons_done: int
    interests: List[str]
    preferred_role: str
    objective: str
    interest_in_challenges: List[str]
    preferred_languages: List[str]
    friend_registration: List[uuid.UUID]
    preferred_team_size: int
    availability: Dict[str, bool]

def check_absolute_restrictions(p1: Participant, p2: Participant) -> bool:
    """
    Verifica las restricciones absolutas entre dos participantes
    Return: True si son compatibles, False si no lo son
    """
    # 1. Verificar lenguajes preferidos
    if not bool(set(p1.preferred_languages) and set(p2.preferred_languages)):
        return False
    
    # 2. Verificar friend registration

    if not (p1.id in p2.friend_registration or p2.id in p1.friend_registration):
        return  False
    
    return True

def calculate_objective_score(p1: Participant) -> float:
    """Calcula la puntuación basada en objetivos usando el clasificador AI (45%)"""
    
    p1_intention = classificador_ai(p1.objective)
    if p1_intention == 'socialize':
        return 1*45
    elif p1_intention == 'learn':
        return 2*45
    elif p1_intention == 'enjoy':
        return 3*45
    else:
        return 4*45
    


def classificador_ai(text: str) -> str:
    '''
    Dado un un texto devuelve la predicción de las intenciones de las personas.
    Posibles etiquetas: socialize, learn, enjoy, win.
    '''

    # Crear el pipeline de clasificación "zero-shot"
    clasificador = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")

    # Definir las etiquetas de intenciones y su mapeo a etiquetas cortas
    long_label = [
        "I want to socialize or meet new people",
        "I want to level up my programming skills",
        "I want to have fun and enjoy",
        "I want to win."
    ]

    short_label = [
        "socialize",
        "learn",
        "enjoy",
        "win"
    ]

    # Clasificar el texto según las etiquetas
    resultado = clasificador(text, candidate_labels=long_label)

    # Encontrar la etiqueta con mayor puntaje y mapearla a la etiqueta corta
    mejor_equivalencia = resultado['labels'][0]
    indice = long_label.index(mejor_equivalencia)
    short_label = long_label[indice]

    return short_label

def calculate_role_score(p1: Participant) -> str:
    """Calcula la puntuación basada en roles preferidos (20%) - premia la diferencia"""
    return p1.preferred_role

def calculate_experience_score(p1: Participant) -> float:
    """Calcula la puntuación basada en nivel de experiencia (12%)"""
    exp_levels = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}

    return exp_levels[p1.experience_level]*12

def calculate_hackathon_score(p1: Participant) -> float:
    """Calcula la puntuación basada en experiencia en hackathons (8%)"""
    return p1.hackathons_done*8

def calculate_study_year_score(p1: Participant) -> float:
    """Calcula la puntuación basada en año de estudio (8%)"""
    years = {"1st year": 1, "2nd year": 2, "3rd year": 3, "4th year": 4, 
            "Masters": 5, "PhD": 6}

    return years[p1.year_of_study]*8

def calculate_team_size_score(p1: Participant) -> float:
    """Calcula la puntuación basada en tamaño de equipo preferido (2%)"""
    return p1.preferred_team_size*2


def calculate_availability_score(p1: Participant) -> float:
    """Calcula la puntuación basada en disponibilidad (5%)"""
    p1_availability_score  = p1.availability
    comptar = sum(1 for value in p1_availability_score.values() if value)

    return comptar*5



def calculate_compatibility_score(p1: Participant) -> list[int|str]:
    """Calcula la puntuación total de compatibilidad entre dos participantes"""

    # Calcular puntuaciones individuales con sus pesos
    scores: list = [int|str]
    scores= [
        (calculate_objective_score(p1)),
        (calculate_role_score(p1)),
        (calculate_experience_score(p1)),
        (calculate_hackathon_score(p1)),
        (calculate_study_year_score(p1)),
        (calculate_availability_score(p1)),
        (calculate_team_size_score(p1)) ]
    
    return scores 

def compara (p1:Participant , p2:Participant) -> float:
    p1_score= calculate_compatibility_score(p1)
    p2_score = calculate_compatibility_score(p2)
    suma_score = 0
    for i in range(len(p1_score)):
        p1_element= p1_score[i]
        p2_element= p2_score[i]
        if isinstance(p1_element, str) and isinstance(p2_element, str):
            if p1_element != p2_element:
                suma_score = suma_score + 20
            else:
                pass
        else:
            suma_score = suma_score + abs(p1_element - p2_element)**2
    
    compatibilitat_p1_p2=sqrt(suma_score)
    return compatibilitat_p1_p2
            
def create_list_lenguages(participants: List[Dict], max_group_size: int = 4) -> List[List[Dict]]:
    """
    Agrupa a los participantes en función de los idiomas que hablan, minimizando el número de grupos.
    Los participantes sin idiomas (`preferred_languages` vacío) se distribuyen equitativamente entre los grupos existentes.

    Args:
        participants (list): Lista de diccionarios con los detalles de los participantes.

    Returns:
        List[List[Dict]]: Lista de grupos con los participantes como diccionarios.
    """
    final_groups = create_list_friends(participants, max_group_size)
    
    language_groups = defaultdict(list)
    
    # Primero, agrupar por idiomas
    for participant in participants:
        languages = set(participant.get("preferred_languages", []))
        if languages:
            language_groups[frozenset(languages)].append(participant)
    
    # Añadir los participantes a los grupos existentes o crear nuevos, respetando el tamaño máximo del grupo
    for language_group in language_groups.values():
        for participant in language_group:
            added = False
            for group in final_groups:
                # Intentar añadir al participante a un grupo existente solo si no supera el límite de tamaño
                if all(languages & set(p.get("preferred_languages", [])) for p in group) and len(group) < max_group_size:
                    group.append(participant)
                    added = True
                    break
            
            # Si no se ha añadido, crear un nuevo grupo
            if not added:
                # Crear un nuevo grupo solo si no excede el límite
                if len(language_group) <= max_group_size:
                    final_groups.append([participant])
                else:
                    # Si el grupo de idioma es más grande que el límite, dividirlo en subgrupos
                    subgroups = [language_group[i:i + max_group_size] for i in range(0, len(language_group), max_group_size)]
                    final_groups.extend(subgroups)
    
    # Procesar los participantes sin idioma
    no_language_participants = [p for p in participants if not p.get("preferred_languages")]
    for participant in no_language_participants:
        # Distribuir los participantes sin idioma entre los grupos más pequeños
        smallest_group = min(final_groups, key=len)
        if len(smallest_group) < max_group_size:
            smallest_group.append(participant)
        else:
            # Si el grupo más pequeño ya tiene 4 personas, buscar otro grupo adecuado
            for group in final_groups:
                if len(group) < max_group_size:
                    group.append(participant)
                    break
    
    return final_groups

def create_list_friends(participants: List[Participant], max_team_size: int = 4) -> List[List[Participant]]:
    """Crea equipos optimizando la compatibilidad y respetando las restricciones"""
    teams = []
    unassigned = participants.copy()
    
    # Primero, procesar grupos con amigos registrados (restricción absoluta)
    friend_groups = {}
    for p in participants:
        if p['friend_registration']:
            group = set(p['id'])
            group.update(p['friend_registration'])
            key = tuple(sorted(group))
            if key not in friend_groups:
                friend_groups[key] = []
            friend_groups[key].extend([p for p in participants if p['id'] in group])
    
    # Añadir grupos de amigos a los equipos
    for group in friend_groups.values():
        if len(group) <= max_team_size:
            teams.append(group)
            for p in group:
                if p in unassigned:
                    unassigned.remove(p)

    return teams     

def create_teams(participants: List[Participant], max_team_size: int = 4) -> List[List[Participant]]: 
    teams = []
    unassigned = participants.copy()

    # Crear matriz de compatibilidad para participantes restantes
    while unassigned:
        current_team = [unassigned.pop(0)]
        
        while len(current_team) < max_team_size and unassigned:
            # Encontrar el mejor candidato compatible
            best_score = -1
            best_candidate = None
            
            for candidate in unassigned:
                # Verificar compatibilidad con todos los miembros actuales
                compatible = all(check_absolute_restrictions(member, candidate) 
                               for member in current_team)
                
                if compatible:
                    # Calcular score promedio con el equipo actual
                    avg_score = np.mean([calculate_compatibility_score(member, candidate) for member in current_team])
                    
                    if avg_score > best_score:
                        best_score = avg_score
                        best_candidate = candidate
            
            if best_candidate:
                current_team.append(best_candidate)
                unassigned.remove(best_candidate)
            else:
                break  # No hay más candidatos compatibles
        
        teams.append(current_team)
    
    return teams

def print_team_analysis(teams: List[List[Participant]]):
    """Imprime un análisis detallado de los equipos formados"""
    print("\nANÁLISIS DE EQUIPOS FORMADOS:")
    print("-" * 50)
    
    for i, team in enumerate(teams, 1):
        print(f"\nEquipo {i} ({len(team)} miembros):")
        print("Miembros:", ", ".join(p.name for p in team))

def main() -> None:
    with open("data/datathon_participants.json", "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)  # Cargar el contenido como un diccionario de Python

    df = pd.read_json("data/datathon_participants.json")
    print(df.loc[df['id'] == "2ebad15c-c0ef-4c04-ba98-c5d98403a90c" ])
          

def noumain() -> None:
    df = pd.read_json('data/datathon_participants.json')

<<<<<<< HEAD
    persona1 = df.loc[0]
    persona2 = df.loc[3]
=======
    persona1= df.loc[0]
    persona2= df.loc[4]
>>>>>>> 63d57658ee29c876c7e86c4b9f4bfbb99f70288f

    print(compara(persona1, persona2))

    with open("datathon_participants.json", "r") as file:
        data = json.load(file)
    
    # Encontrar los grupos basados en idiomas
    groups_json = create_list_lenguages(data)
    
    # Mostrar los resultados en el formato de salida requerido
    grups_llista = []
    for group in groups_json:
        grups_llista.append([participant for participant in group])

    # Imprimir cada grupo por separado
    for i, group in enumerate(grups_llista, 1):  # Para enumerar los grupos y añadir un número de grupo
        print(f"Grupo {i}:")
        for persona in group:
            print(persona['name'])
        print()  # Añadir una línea en blanco entre grupos

if __name__ == '__main__':
    noumain()