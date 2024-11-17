
import numpy as np
import pandas as pd
from typing import List, Dict
from dataclasses import dataclass
from transformers import pipeline
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
    Verifies the absolute restrictions between two participants.
    Returns: True if they are compatible, False if not.
    """
    # 1. Verify preferred languages
    if not bool(set(p1.preferred_languages) & set(p2.preferred_languages)):
        return False

    # 2. Verify friend registration
    if not (p1.id in p2.friend_registration or p2.id in p1.friend_registration):
        return False

    return True
def calculate_compatibility_score(p1: Participant, participants: List[Participant]) -> float:
    """Calculates the overall compatibility score for a single participant"""
    scores = [
        (calculate_objective_score(p1.objective), 0.45),
        (calculate_role_score(p1.preferred_role), 0.20),
        (calculate_experience_score(p1.experience_level), 0.12),
        (calculate_hackathon_score(p1.hackathons_done), 0.08),
        (calculate_study_year_score(p1.year_of_study), 0.08),
        (calculate_availability_score(p1.availability), 0.05),
        (calculate_team_size_score(p1.preferred_team_size), 0.02)
    ]

    # Apply absolute restrictions
    for p2 in participants:
        if not check_absolute_restrictions(p1, p2):
            return 0.0

    return sum(score * weight for score, weight in scores)


def calculate_objective_score(objective: str) -> int:
    """Calculates the score based on the participant's objective (45%)"""
    classifier = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")
    long_labels = [
        "I want to socialize or meet new people",
        "I want to level up my programming skills",
        "I want to have fun and enjoy",
        "I want to win."
    ]
    short_labels = ["socialize", "learn", "enjoy", "win"]

    result = classifier(objective, candidate_labels=long_labels)
    best_label_index = long_labels.index(result["labels"][0])
    return short_labels.index(short_labels[best_label_index]) + 1

def calculate_role_score(preferred_role: str) -> float:
    """Calculates the score based on the preferred role (20%)"""
    roles = ["Analysis", "Visualization", "Development", "Design"]
    if preferred_role not in roles:
        return 0.5  # Neutral value for "Don't know" or "Don't care"
    return 1.0 - (roles.index(preferred_role) / (len(roles) - 1))

def calculate_experience_score(experience_level: str) -> int:
    """Calculates the score based on the experience level (12%)"""
    exp_levels = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}
    return exp_levels.get(experience_level, 1)

def calculate_hackathon_score(hackathons_done: int) -> int:
    """Calculates the score based on the number of hackathons (8%)"""
    return hackathons_done

def calculate_study_year_score(year_of_study: str) -> int:
    """Calculates the score based on the study year (8%)"""
    years = {"1st year": 1, "2nd year": 2, "3rd year": 3, "4th year": 4, "Masters": 5, "PhD": 6}
    return years.get(year_of_study, 1)

def calculate_team_size_score(preferred_team_size: int) -> int:
    """Calculates the score based on the preferred team size (2%)"""
    return preferred_team_size

def calculate_availability_score(availability: Dict[str, bool]) -> int:
    """Calculates the score based on the participant's availability (5%)"""
    return sum(1 for value in availability.values() if value)
def create_teams(participants: List[Participant], max_team_size: int = 4) -> List[List[Participant]]:
    """Creates teams by optimizing compatibility and respecting restrictions"""
    teams = []
    unassigned = participants.copy()

    # Process friend groups (absolute restriction)
    friend_groups = {}
    for p in participants:
        if p.friend_registration:
            group = set([p.id])
            group.update(p.friend_registration)
            key = tuple(sorted(group))
            if key not in friend_groups:
                friend_groups[key] = []
            friend_groups[key].append(p)

    # Add friend groups to the teams
    for group in friend_groups.values():
        if len(group) <= max_team_size:
            teams.append(group)
            for p in group:
                if p in unassigned:
                    unassigned.remove(p)

    # Create teams for the remaining participants
    while unassigned:
        current_team = [unassigned.pop(0)]
        while len(current_team) < max_team_size and unassigned:
            best_score = -1
            best_candidate = None
            for candidate in unassigned:
                avg_score = calculate_compatibility_score(candidate, participants)
                if avg_score > best_score:
                    best_score = avg_score
                    best_candidate = candidate
            if best_candidate:
                current_team.append(best_candidate)
                unassigned.remove(best_candidate)
            else:
                break
        teams.append(current_team)

    return teams


def print_team_analysis(teams: List[List[Participant]]):
    """Prints a detailed analysis of the formed teams"""
    print("\nTEAM ANALYSIS:")
    print("-" * 50)

    for i, team in enumerate(teams, 1):
        print(f"\nTeam {i} ({len(team)} members):")
        print("Members:", ", ".join(p.name for p in team))

        # Analyze team characteristics
        roles = [p.preferred_role for p in team]
        objectives = [calculate_objective_score(p.objective) for p in team]
        exp_levels = [p.experience_level for p in team]

        print(f"Roles: {', '.join(roles)}")
        print(f"Objectives: {', '.join(map(str, objectives))}")
        print(f"Experience Levels: {', '.join(exp_levels)}")

        # Calculate average team compatibility
        if len(team) > 1:
            avg_score = np.mean([calculate_compatibility_score(team[i]) for i in range(len(team))])
            print(f"Average Team Compatibility: {avg_score:.2f}")

        print("-" * 30)


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

def main() -> None:
    llista_participants = load_participants_from_file("data/datathon_participants.json")
    
    teams = create_teams(llista_participants)
    print_team_analysis(teams)
    
if __name__ == '__main__':
    main()