from typing import List, Dict, Tuple

# Estructura para almacenar la información de cada participante
class Participant:
    def __init__(self, id: int, name: str, programming_skills: Dict[str, int]):
        self.id = id
        self.name = name
        self.programming_skills = programming_skills  # Diccionario: {'language': level}
        
    def __str__(self):
        return f"{self.name} (ID: {self.id})"

# Función para calcular la compatibilidad entre dos participantes
def compatibillity_programming_skills(p1: Participant, p2: Participant) -> float:
    compatibility_score = 0
    common_languages = set(p1.programming_skills.keys()) & set(p2.programming_skills.keys())
    
    # Si tienen lenguajes en común, sumamos la compatibilidad en función de los niveles
    for lang in common_languages:
        level_diff = abs(p1.programming_skills[lang] - p2.programming_skills[lang])
        if level_diff <= 2:
            compatibility_score += (10 - level_diff)  # Si la diferencia de nivel es baja, es más compatible
        else:
            compatibility_score -= (level_diff - 2)  # Si la diferencia es alta, se penaliza la compatibilidad
    
    # Buscamos lenguajes complementarios
    unique_languages_p1 = set(p1.programming_skills.keys()) - common_languages
    unique_languages_p2 = set(p2.programming_skills.keys()) - common_languages
    
    for lang1 in unique_languages_p1:
        for lang2 in unique_languages_p2:
            # Complementariedad de habilidades
            compatibility_score += 1  # Valor de compatibilidad por tener habilidades complementarias

    return compatibility_score

# Función para agrupar los participantes basados en la compatibilidad
def group_participants(participants: List[Participant], group_size: int) -> List[List[Participant]]:
    groups = []
    # Inicializamos una lista para agruparlos según la compatibilidad
    while participants:
        # Tomamos el primer participante
        group = [participants.pop(0)]
        
        # Buscamos los demás participantes compatibles
        for p in participants[:]:
            if all(compatibillity_programming_skills(p, g) > 0 for g in group):
                group.append(p)
                participants.remove(p)
            
            if len(group) >= group_size:
                break
        
        # Añadimos el grupo al resultado
        groups.append(group)
    
    return groups

# Ejemplo de uso
def main():
    # Definimos algunos participantes con sus lenguajes y niveles de habilidad
    participants = [
        Participant(1, "Alice", {"Python": 8, "JavaScript": 5, "Java": 6}),
        Participant(2, "Bob", {"Python": 7, "C++": 5, "JavaScript": 9}),
        Participant(3, "Charlie", {"Python": 6, "React": 7, "HTML/CSS": 9}),
        Participant(4, "David", {"JavaScript": 8, "Node.js": 7}),
        Participant(5, "Eve", {"Java": 7, "Python": 5}),
        Participant(6, "Frank", {"Java": 6, "C++": 8}),
    ]
    
    # Agrupar a los participantes en grupos de tamaño 3
    groups = group_participants(participants, group_size=3)
    
    # Mostrar los resultados
    for i, group in enumerate(groups, 1):
        print(f"Group {i}:")
        for participant in group:
            print(f"  {participant}")
        print()

if __name__ == "__main__":
    main()
