import uuid
from typing import List, Dict, Literal
import random

# Definición de la clase Participant
class Participant:
    def __init__(self, name: str, email: str, age: int, year_of_study: str, shirt_size: str,
                 university: str, dietary_restrictions: str, programming_skills: Dict[str, int],
                 experience_level: str, hackathons_done: int, interests: List[str], preferred_role: str,
                 objective: str, interest_in_challenges: List[str], preferred_languages: List[str],
        self.university = university
        self.dietary_restrictions = dietary_restrictions
        self.programming_skills = programming_skills
        self.experience_level = experience_level
        self.hackathons_done = hackathons_done
        self.interests = interests
        self.preferred_role = preferred_role
        self.objective = objective
        self.interest_in_challenges = interest_in_challenges
        self.preferred_languages = preferred_languages
        self.friend_registration = friend_registration
        self.preferred_team_size = preferred_team_size
        self.availability = availability
        self.introduction = introduction
        self.technical_project = technical_project
        self.future_excitement = future_excitement
        self.fun_fact = fun_fact

    def __repr__(self):
        return f"Participant({self.name}, {self.year_of_study}, {self.experience_level})"

# Función para crear grupos de hasta 4 personas
def create_groups(participants: List[Participant]):
    # Aquí se pueden definir los criterios para formar los grupos
    groups = []
    
    # Primera aproximación: organizar a los participantes por su año de estudio
    study_years = {"1st year": [], "2nd year": [], "3rd year": [], "4th year": [], "Masters": [], "PhD": []}
    
    for participant in participants:
        study_years[participant.year_of_study].append(participant)
    
    # Formar los grupos balanceados
    while any(study_years.values()):
        group = []
        
        # Intentamos que cada grupo tenga al menos un participante de cada año de estudio
        for year in ["1st year", "2nd year", "3rd year", "4th year", "Masters", "PhD"]:
            if study_years[year]:
                participant = study_years[year].pop(0)
                group.append(participant)
        
        # Si el grupo tiene menos de 4 personas, intentamos llenar con los que quedan en otras categorías
        while len(group) < 4:
            for year in study_years:
                if study_years[year]:
                    participant = study_years[year].pop(0)
                    group.append(participant)
                    if len(group) == 4:
                        break
        
        groups.append(group)
    
    return groups

# Ejemplo de cómo crear participantes
participants = [
    Participant(
        name="Juan Pérez", email="juan@university.com", age=21, year_of_study="3rd year", shirt_size="M",
        university="Universidad X", dietary_restrictions="None", programming_skills={"Python": 4, "Java": 3},
        experience_level="Intermediate", hackathons_done=2, interests=["Data Science", "AI"], preferred_role="Development",
        objective="Aprender nuevas habilidades", interest_in_challenges=["Data Challenges"], preferred_languages=["Python"],
        friend_registration=[], preferred_team_size=4, availability={"Monday": True, "Tuesday": False},
        introduction="Soy apasionado de la ciencia de datos.", technical_project="Análisis de datos con Python",
        future_excitement="Desarrollar aplicaciones inteligentes", fun_fact="Tengo una colección de robots.")
]

# Crear más participantes de ejemplo (repitiendo para ilustrar)
for _ in range(5):
    participants.append(Participant(
        name="Ana Gómez", email="ana@university.com", age=22, year_of_study="2nd year", shirt_size="S",
        university="Universidad Y", dietary_restrictions="Vegetarian", programming_skills={"Python": 3, "R": 4},
        experience_level="Beginner", hackathons_done=1, interests=["Data Visualization", "AI"], preferred_role="Visualization",
        objective="Crear portafolio", interest_in_challenges=["AI Challenges"], preferred_languages=["Python", "R"],
        friend_registration=[], preferred_team_size=4, availability={"Monday": True, "Tuesday": True},
        introduction="Me encanta la visualización de datos.", technical_project="Visualización de datos con R",
        future_excitement="Explorar el impacto de la IA", fun_fact="Amo el yoga.")
)

# Crear los grupos
groups = create_groups(participants)

# Imprimir los grupos formados
for i, group in enumerate(groups):
    print(f"Grupo {i+1}:")
    for participant in group:
        print(f"- {participant.name} ({participant.year_of_study}, {participant.experience_level})")
    print()
