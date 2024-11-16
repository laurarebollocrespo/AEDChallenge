import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass
import uuid
from transformers import pipeline
from data import json

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
    
    # 3. Verificar programming skills (al menos un skill en común)
    if not bool(set(p1.programming_skills.keys()) and set(p2.programming_skills.keys())):
        return False
    
    return True

def calculate_objective_score(p1: Participant, p2: Participant) -> float:
    """Calcula la puntuación basada en objetivos usando el clasificador AI (40%)"""
    p1_intention = classificador_ai(p1.objective)
    p2_intention = classificador_ai(p2.objective)
    return 1.0 if p1_intention == p2_intention else 0.0



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

def calculate_role_score(p1: Participant, p2: Participant) -> float:
    """Calcula la puntuación basada en roles preferidos (20%) - premia la diferencia"""
    roles = ["Analysis", "Visualization", "Development", "Design"]
    if p1.preferred_role not in roles or p2.preferred_role not in roles:
        return 0.5  # Valor neutral para "Don't know" o "Don't care"
    return 1.0 if p1.preferred_role != p2.preferred_role else 0.0

def calculate_experience_score(p1: Participant, p2: Participant) -> float:
    """Calcula la puntuación basada en nivel de experiencia (12%)"""
    exp_levels = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}
    diff = abs(exp_levels[p1.experience_level] - exp_levels[p2.experience_level])
    return 1.0 - (diff / 2)  # Normalizado entre 0 y 1

def calculate_hackathon_score(p1: Participant, p2: Participant) -> float:
    """Calcula la puntuación basada en experiencia en hackathons (8%)"""
    max_diff = 10  # Diferencia máxima considerada
    diff = abs(p1.hackathons_done - p2.hackathons_done)
    return 1.0 - min(diff, max_diff) / max_diff

def calculate_study_year_score(p1: Participant, p2: Participant) -> float:
    """Calcula la puntuación basada en año de estudio (8%)"""
    years = {"1st year": 1, "2nd year": 2, "3rd year": 3, "4th year": 4, 
            "Masters": 5, "PhD": 6}
    diff = abs(years[p1.year_of_study] - years[p2.year_of_study])
    return 1.0 - (diff / 5)

def calculate_challenge_interest_score(p1: Participant, p2: Participant) -> float:
    """Calcula la puntuación basada en interés en desafíos (5%)"""
    common_interests = set(p1.interest_in_challenges) & set(p2.interest_in_challenges)
    total_interests = set(p1.interest_in_challenges) | set(p2.interest_in_challenges)
    return len(common_interests) / len(total_interests) if total_interests else 0.0

def calculate_availability_score(p1: Participant, p2: Participant) -> float:
    """Calcula la puntuación basada en disponibilidad (5%)"""
    common_available = sum(1 for time in p1.availability
                         if p1.availability[time] and p2.availability[time])
    total_slots = len(p1.availability)
    return common_available / total_slots

def calculate_team_size_score(p1: Participant, p2: Participant) -> float:
    """Calcula la puntuación basada en tamaño de equipo preferido (2%)"""
    return 1.0 if p1.preferred_team_size == p2.preferred_team_size else 0.0

def calculate_compatibility_score(p1: Participant, p2: Participant) -> float:
    """Calcula la puntuación total de compatibilidad entre dos participantes"""
    # Primero verificar restricciones absolutas
    if not check_absolute_restrictions(p1, p2):
        return 0.0

    # Calcular puntuaciones individuales con sus nuevos pesos
    scores = [
        (calculate_objective_score(p1, p2), 0.40),
        (calculate_role_score(p1, p2), 0.20),
        (calculate_experience_score(p1, p2), 0.12),
        (calculate_hackathon_score(p1, p2), 0.08),
        (calculate_study_year_score(p1, p2), 0.08),
        (calculate_challenge_interest_score(p1, p2), 0.05),
        (calculate_availability_score(p1, p2), 0.05),
        (calculate_team_size_score(p1, p2), 0.02)
    ]
    
    return sum(score * weight for score, weight in scores)

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
    participants = json.open("data/datathon_participants.json")
    llista_participants : list = []
    teams = create_teams(participants)
    print_team_analysis(teams)
    print(participants)

if __name__ == '__main__':
    main()