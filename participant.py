import numpy as np
import pandas as pd
from typing import List, Dict
from dataclasses import dataclass
from transformers import pipeline
from typing import Dict, List
import uuid
import json


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

def calculate_objective_score(p1: Participant) -> int:
    """Calcula la puntuación basada en objetivos usando el clasificador AI (45%)"""
    
    p1_intention = classificador_ai(p1.objective)
    if p1_intention == 'socialize':
        return 1
    elif p1_intention == 'learn':
        return 2
    elif p1_intention == 'enjoy':
        return 3
    else:
        return 4
def calculate_objective_score(p1: Participant) -> int:
    """Calcula la puntuación basada en objetivos usando el clasificador AI (45%)"""
    
    p1_intention = classificador_ai(p1.objective)
    if p1_intention == 'socialize':
        return 1
    elif p1_intention == 'learn':
        return 2
    elif p1_intention == 'enjoy':
        return 3
    else:
        return 4


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

def calculate_experience_score(p1: Participant) -> int:
    """Calcula la puntuación basada en nivel de experiencia (12%)"""
    exp_levels = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}

    return exp_levels[p1.experience_level]

def calculate_hackathon_score(p1: Participant) -> int:
    """Calcula la puntuación basada en experiencia en hackathons (8%)"""
    return p1.hackathons_done

def calculate_study_year_score(p1: Participant) -> int:
    """Calcula la puntuación basada en año de estudio (8%)"""
    years = {"1st year": 1, "2nd year": 2, "3rd year": 3, "4th year": 4, 
            "Masters": 5, "PhD": 6}

    return years[p1.year_of_study]

def calculate_team_size_score(p1: Participant) -> int:
    """Calcula la puntuación basada en tamaño de equipo preferido (2%)"""
    return p1.preferred_team_size

def calculate_availability_score(p1: Participant) -> int:
    """Calcula la puntuación basada en disponibilidad (5%)"""
    p1_availability_score  = p1.availability
    comptar = sum(1 for value in p1_availability_score.values() if value)

    return comptar



def calculate_compatibility_score(p1: Participant) -> float:
    """Calcula la puntuación total de compatibilidad entre dos participantes"""

    # Calcular puntuaciones individuales con sus pesos
    scores = [
        (calculate_objective_score(p1)),
        (calculate_role_score(p1)),
        (calculate_experience_score(p1)),
        (calculate_hackathon_score(p1)),
        (calculate_study_year_score(p1)),
        (calculate_availability_score(p1)),
        (calculate_team_size_score(p1))
    ]
    
    return scores #sense ponderar!


def create_teams(participants: List[Participant], max_team_size: int = 4) -> List[List[Participant]]:
    """Crea equipos optimizando la compatibilidad y respetando las restricciones"""
    teams = []
    unassigned = participants.copy()
    
    # Primero, procesar grupos con amigos registrados (restricción absoluta)
    friend_groups = {}
    for p in participants:
        if p.friend_registration:
            group = set([p.id])
            group.update(p.friend_registration)
            key = tuple(sorted(group))
            if key not in friend_groups:
                friend_groups[key] = []
            friend_groups[key].extend([p for p in participants if p.id in group])
    
    # Añadir grupos de amigos a los equipos
    for group in friend_groups.values():
        if len(group) <= max_team_size:
            teams.append(group)
            for p in group:
                if p in unassigned:
                    unassigned.remove(p)
    
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
                    avg_score = np.mean([calculate_compatibility_score(member, candidate) 
                                       for member in current_team])
                    
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
        # Analizar características del equipo
        roles = [p.preferred_role for p in team]
        objectives = [classificador_ai(p.objective) for p in team]
        exp_levels = [p.experience_level for p in team]
        
        print(f"Roles: {', '.join(roles)}")
        print(f"Objetivos: {', '.join(objectives)}")
        print(f"Niveles de experiencia: {', '.join(exp_levels)}")
        
        # Calcular compatibilidad promedio del equipo
        if len(team) > 1:
            scores = []
            for i in range(len(team)):
                for j in range(i + 1, len(team)):
                    scores.append(calculate_compatibility_score(team[i], team[j]))
            avg_score = np.mean(scores)
            print(f"Compatibilidad promedio del equipo: {avg_score:.2f}")
        
        print("-" * 30)
   

def main() -> None:
    with open("data/datathon_participants.json", "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)  # Cargar el contenido como un diccionario de Python

    df = pd.read_json("data/datathon_participants.json")
    print(df.loc[df['id'] == "2ebad15c-c0ef-4c04-ba98-c5d98403a90c" ])

def calcular_afinitat (p1,p2):
    score_p1 = calculate_compatibility_score(p1)
    score_p2 = calculate_compatibility_score(p2)

    resultado = [
    v1**2 - v2**2 if i != 1 else score_p1[1] == score_p2[1]
    for i, (v1, v2) in enumerate(zip(score_p1, score_p2))
]
    return resultado

def noumain() -> None:
    df = pd.read_json('data/datathon_participants.json')

    persona1= df.loc[0]
    persona2= df.loc[1]

    print(calcular_afinitat(persona1, persona2))

if __name__ == '__main__':
    noumain()