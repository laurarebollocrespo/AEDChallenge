from dataclasses import dataclass
import pandas as pd
import uuid
from typing import Dict, List, Literal

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

def load_participants_from_file(file_path: str) -> List[Participant]:
    """
    Lee un archivo JSON usando pandas y convierte los datos en objetos de tipo Participant.
    """
    # Usamos pandas para leer el archivo JSON
    df = pd.read_json(file_path)
    
    participants = []
    
    # Convertimos cada fila del dataframe en un objeto Participant
    for _, row in df.iterrows():
        participant = Participant(
            id=uuid.UUID(row["id"]),
            name=row["name"],
            year_of_study=row["year_of_study"],
            programming_skills=row["programming_skills"],
            experience_level=row["experience_level"],
            hackathons_done=row["hackathons_done"],
            interests=row["interests"],
            preferred_role=row["preferred_role"],
            objective=row["objective"],
            interest_in_challenges=row["interest_in_challenges"],
            preferred_languages=row["preferred_languages"],
            friend_registration=[uuid.UUID(fid) for fid in row["friend_registration"]],
            preferred_team_size=row["preferred_team_size"],
            availability=row["availability"]
        )
        participants.append(participant)
    
    return participants