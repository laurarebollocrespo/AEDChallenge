import uuid
from typing import List, Literal, Dict

class Participant:
    def __init__(
        self,
        name: str,
        year_of_study: Literal["1st year", "2nd year", "3rd year", "4th year", "Masters", "PhD"],
        programming_skills: Dict[str, int],
        experience_level: Literal["Beginner", "Intermediate", "Advanced"],
        hackathons_done: int,
        interests: List[str],
        preferred_role: Literal["Analysis", "Visualization", "Development", "Design", "Don't know", "Don't care"],
        objective: str,
        interest_in_challenges: List[str],
        preferred_languages: List[str],
        friend_registration: List[uuid.UUID],
        preferred_team_size: int,
        availability: Dict[str, bool],
    ):
        # Aquí definimos los atributos de cada participante
        self.name = name
        self.year_of_study = year_of_study
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

def create_teams(participants: List[Participant]) -> List[List[Participant]]:
    # Aquí creamos los equipos de participantes
    teams = []  # Lista vacía para almacenar los equipos
    available_participants = participants.copy()  # Copia de la lista de participantes para no modificar la original

    # Mientras haya participantes disponibles
    while available_participants:
        team = []  # Creamos un equipo vacío
        # Agregamos hasta 4 participantes al equipo, o todos los participantes restantes si son menos de 4
        for _ in range(min(4, len(available_participants))):
            if available_participants:
                team.append(available_participants.pop(0))  # Agregamos el participante al equipo y lo removemos de la lista de participantes disponibles
        teams.append(team)  # Agregamos el equipo a la lista de equipos

    return teams  # Devolvemos la lista de equipos

# Ejemplo de uso
participant1 = Participant(
    # Aquí creamos un objeto Participant con los datos del primer participante
    name="Sara Vilar",
    year_of_study="4th year",
    programming_skills={"Data Visualization": 2, "Flask": 4, "React Native": 6},
    experience_level="Intermediate",
    hackathons_done=2,
    interests=["Fintech", "Blockchain", "Cybersecurity", "Productivity"],
    preferred_role="Design",
    objective="I'm super stoked to be participating in this datathon!",
    interest_in_challenges=["Mango Challenge", "Restb.ai Challenge", "AED Challenge"],
    preferred_languages=["English", "Catalan"],
    friend_registration=[],
    preferred_team_size=4,
    availability={
        "Saturday morning": True,
        "Saturday afternoon": True,
        "Saturday night": False,
        "Sunday morning": True,
        "Sunday afternoon": True,
    },
)

participant2 = Participant(
    # Aquí creamos un objeto Participant con los datos del segundo participante
    name="Aurora Wells",
    year_of_study="3rd year",
    programming_skills={"React": 4, "PostgreSQL": 5, "Figma": 7, "SQL": 2},
    experience_level="Intermediate",
    hackathons_done=5,
    interests=[
        "Productivity",
        "Enterprise",
        "DevOps",
        "Health",
        "Robotic Process Automation",
        "AR/VR",
    ],
    preferred_role="Analysis",
    objective="For me, this datathon is all about leveling up my skills.",
    interest_in_challenges=["AED Challenge", "Mango Challenge", "Restb.ai Challenge"],
    preferred_languages=["English"],
    friend_registration=[],
    preferred_team_size=3,
    availability={
        "Saturday morning": True,
        "Saturday afternoon": False,
        "Saturday night": True,
        "Sunday morning": False,
        "Sunday afternoon": True,
    },
)

# Aquí creamos una lista con los dos participantes
participants = [participant1, participant2]

# Llamamos a la función create_teams para crear los equipos
teams = create_teams(participants)

# Imprimimos los equipos
for team in teams:
    print("Team members:")
    for participant in team:
        print(f"- {participant.name}")
    print()
    