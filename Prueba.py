
import numpy as np
from typing import List, Dict
from dataclasses import dataclass
import uuid
from transformers import pipeline


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

def check_language_compatibility(p1: Participant, p2: Participant) -> bool:
    """Verifica si dos participantes comparten al menos un idioma común"""
    return bool(set(p1.preferred_languages) and set(p2.preferred_languages))

def calculate_friend_score(p1: Participant, p2: Participant) -> float:
    """Calcula la puntuación basada en registro de amigos (20%)"""
    if p1.id in p2.friend_registration or p2.id in p1.friend_registration:
        return 1.0
    return 0.0

def calculate_objective_score(p1: Participant, p2: Participant) -> float:
    """Calcula la puntuación basada en objetivos usando el clasificador AI (15%)"""
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
    """Calcula la puntuación basada en roles preferidos (14%) - premia la diferencia"""
    roles = ["Analysis", "Visualization", "Development", "Design"]
    if p1.preferred_role not in roles or p2.preferred_role not in roles:
        return 0.5  # Valor neutral para "Don't know" o "Don't care"
    return 1.0 if p1.preferred_role != p2.preferred_role else 0.0

def calculate_experience_score(p1: Participant, p2: Participant) -> float:
    """Calcula la puntuación basada en nivel de experiencia (12%)"""
    exp_levels = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}
    diff = abs(exp_levels[p1.experience_level] - exp_levels[p2.experience_level])
    return 1.0 - (diff / 2)  # Normalizado entre 0 y 1

def calculate_language_programming_score(p1: Participant, p2: Participant) -> float:
    """Calcula la puntuación basada en lenguajes de programación preferidos (10%)"""
    common_languages = set(p1.preferred_languages) & set(p2.preferred_languages)
    total_languages = set(p1.preferred_languages) | set(p2.preferred_languages)
    return len(common_languages) / len(total_languages) if total_languages else 0.0

def calculate_programming_skills_score(p1: Participant, p2: Participant) -> float:
    """Calcula la puntuación basada en habilidades de programación (10%)"""
    common_skills = set(p1.programming_skills.keys()) & set(p2.programming_skills.keys())
    if not common_skills:
        return 1.0  # Habilidades complementarias
    
    skill_diff = sum(abs(p1.programming_skills[skill] - p2.programming_skills[skill]) 
                    for skill in common_skills)
    return 1.0 - (skill_diff / (len(common_skills) * 10))

def calculate_hackathon_score(p1: Participant, p2: Participant) -> float:
    """Calcula la puntuación basada en experiencia en hackathons (8%)"""
    max_diff = 10  # Diferencia máxima considerada
    diff = abs(p1.hackathons_done - p2.hackathons_done)
    return 1.0 - min(diff, max_diff) / max_diff

def calculate_study_year_score(p1: Participant, p2: Participant) -> float:
    """Calcula la puntuación basada en año de estudio (5%)"""
    years = {"1st year": 1, "2nd year": 2, "3rd year": 3, "4th year": 4, 
            "Masters": 5, "PhD": 6}
    diff = abs(years[p1.year_of_study] - years[p2.year_of_study])
    return 1.0 - (diff / 5)

def calculate_challenge_interest_score(p1: Participant, p2: Participant) -> float:
    """Calcula la puntuación basada en interés en desafíos (3%)"""
    common_interests = set(p1.interest_in_challenges) & set(p2.interest_in_challenges)
    total_interests = set(p1.interest_in_challenges) | set(p2.interest_in_challenges)
    return len(common_interests) / len(total_interests) if total_interests else 0.0

def calculate_availability_score(p1: Participant, p2: Participant) -> float:
    """Calcula la puntuación basada en disponibilidad (2%)"""
    common_available = sum(1 for time in p1.availability
                         if p1.availability[time] and p2.availability[time])
    total_slots = len(p1.availability)
    return common_available / total_slots

def calculate_team_size_score(p1: Participant, p2: Participant) -> float:
    """Calcula la puntuación basada en tamaño de equipo preferido (1%)"""
    return 1.0 if p1.preferred_team_size == p2.preferred_team_size else 0.0

def calculate_compatibility_score(p1: Participant, p2: Participant) -> float:
    """Calcula la puntuación total de compatibilidad entre dos participantes"""
    # Verificar restricciones absolutas
    if not check_language_compatibility(p1, p2):
        return 0.0

    # Calcular puntuaciones individuales con sus pesos
    scores = [
        (calculate_friend_score(p1, p2), 0.20),
        (calculate_objective_score(p1, p2), 0.15),
        (calculate_role_score(p1, p2), 0.14),
        (calculate_experience_score(p1, p2), 0.12),
        (calculate_language_programming_score(p1, p2), 0.10),
        (calculate_programming_skills_score(p1, p2), 0.10),
        (calculate_hackathon_score(p1, p2), 0.08),
        (calculate_study_year_score(p1, p2), 0.05),
        (calculate_challenge_interest_score(p1, p2), 0.03),
        (calculate_availability_score(p1, p2), 0.02),
        (calculate_team_size_score(p1, p2), 0.01)
    ]
    
    return sum(score * weight for score, weight in scores)

def create_teams(participants: List[Participant], max_team_size: int = 4) -> List[List[Participant]]:
    """Crea equipos optimizando la compatibilidad y respetando las restricciones"""
    teams = []
    unassigned = participants.copy()
    
    # Primero, crear grupos con amigos registrados
    friend_groups = {}
    for p in participants:
        if p.friend_registration:
            for friend_id in p.friend_registration:
                if friend_id not in friend_groups:
                    friend_groups[friend_id] = set([p.id])
                friend_groups[friend_id].add(friend_id)
    
    # Procesar grupos de amigos
    processed_ids = set()
    for group in friend_groups.values():
        if not group & processed_ids:  # Si ningún miembro ha sido procesado
            team = [p for p in participants if p.id in group]
            if len(team) <= max_team_size:
                teams.append(team)
                processed_ids.update(group)
                for p in team:
                    if p in unassigned:
                        unassigned.remove(p)
    
    # Crear matriz de compatibilidad para participantes restantes
    n = len(unassigned)
    compatibility_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i+1, n):
            score = calculate_compatibility_score(unassigned[i], unassigned[j])
            compatibility_matrix[i,j] = compatibility_matrix[j,i] = score
    
    # Formar equipos con participantes restantes
    while unassigned:
        current_team = [unassigned.pop(0)]
        while len(current_team) < max_team_size and unassigned:
            # Encontrar el mejor candidato para el equipo actual
            best_score = -1
            best_candidate = None
            for candidate in unassigned:
                avg_score = np.mean([calculate_compatibility_score(member, candidate) 
                                   for member in current_team])
                if avg_score > best_score:
                    best_score = avg_score
                    best_candidate = candidate
            
            if best_candidate and best_score > 0:
                current_team.append(best_candidate)
                unassigned.remove(best_candidate)
            else:
                break
        
        teams.append(current_team)
    
    return teams


# Crear lista de participantes
participants = [...]  # Lista de objetos Participant

# Crear equipos
teams = create_teams(participants)

# Revisar equipos formados
for i, team in enumerate(teams, 1):
    print(f"\nEquipo {i}:")
    for member in team:
        print(f"- {member.name}")

