import json
from typing import List, Dict

# Clase para los participantes
class Participant:
    def __init__(self, id: int, name: str, programming_skills: Dict[str, int]):
        self.id = id
        self.name = name
        self.programming_skills = programming_skills

    def average_skill_level(self) -> float:
        """Calcula el nivel promedio de habilidades del participante."""
        return sum(self.programming_skills.values()) / len(self.programming_skills)

# Función para calcular compatibilidad (puedes ajustar según necesidad)
def calculate_compatibility(p1: Participant, p2: Participant) -> float:
    compatibility_score = 0
    common_languages = set(p1.programming_skills.keys()) & set(p2.programming_skills.keys())
    for lang in common_languages:
        level_diff = abs(p1.programming_skills[lang] - p2.programming_skills[lang])
        compatibility_score += max(0, 10 - level_diff)
    return compatibility_score

# Función para agrupar participantes según niveles de habilidad
def group_participants(participants: List[Participant]) -> List[List[Participant]]:
    group_1 = []
    group_2 = []
    group_3 = []

    for participant in participants:
        avg_skill = participant.average_skill_level()
        if avg_skill >= 7:
            group_1.append(participant)
        elif 4 <= avg_skill < 7:
            group_2.append(participant)
        else:
            group_3.append(participant)

    return [group_1, group_2, group_3]

# Función principal para cargar datos y procesar
def main():
    # Leer datos desde el archivo JSON
    with open("datathon_participants.json", "r") as file:
        data = json.load(file)

    # Crear objetos de Participant
    participants = [
        Participant(p["id"], p["name"], p["programming_skills"]) for p in data
    ]

    # Agrupar participantes
    groups = group_participants(participants)

    # Mostrar los nombres de los participantes en cada grupo
    for i, group in enumerate(groups, 1):
        print(f"Group {i}:")
        for participant in group:
            print(f"  {participant.name}")
        print()

if __name__ == "__main__":
    main()
