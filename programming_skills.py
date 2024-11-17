from typing import List, Dict, Tuple

# Clase para representar a un participante
class Participant:
    def __init__(self, id: int, name: str, programming_skills: Dict[str, int]):
        self.id = id
        self.name = name
        self.programming_skills = programming_skills  # Diccionario: {'language': level}
        self.average_skill = sum(programming_skills.values()) / len(programming_skills)  # Promedio de habilidades
        
    def __str__(self):
        return f"{self.name}"

# Función para calcular la compatibilidad entre dos participantes
def calculate_compatibility(p1: Participant, p2: Participant) -> float:
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

# Función para dividir participantes en tres grupos según nivel de habilidad
def divide_by_skill(participants: List[Participant]) -> Tuple[List[Participant], List[Participant], List[Participant]]:
    # Ordenar por habilidad promedio de mayor a menor
    participants.sort(key=lambda p: p.average_skill, reverse=True)
    
    # Clasificar participantes en tres grupos según el nivel de habilidad promedio
    high_skill = [p for p in participants if p.average_skill > 7]  # Habilidades altas
    mid_skill = [p for p in participants if 4 <= p.average_skill <= 7]  # Habilidades medias
    low_skill = [p for p in participants if p.average_skill < 4]  # Habilidades bajas
    
    return high_skill, mid_skill, low_skill

# Función para optimizar compatibilidad dentro de un grupo
def optimize_group(group: List[Participant]) -> List[Participant]:
    optimized_group = []
    
    while group:
        if not optimized_group:
            # Añadir el primer participante al grupo optimizado
            optimized_group.append(group.pop(0))
        else:
            # Encontrar el participante más compatible con el grupo optimizado
            best_match = None
            best_score = float('-inf')
            
            for participant in group:
                score = sum(calculate_compatibility(participant, g) for g in optimized_group)
                if score > best_score:
                    best_match = participant
                    best_score = score
            
            # Añadir el participante más compatible al grupo optimizado
            optimized_group.append(best_match)
            group.remove(best_match)
    
    return optimized_group

# Ejemplo de uso
def main():
    # Lista de participantes con habilidades
    participants = [
        Participant(1, "Alice", {"Python": 8, "JavaScript": 9, "Java": 7}),
        Participant(2, "Bob", {"Python": 7, "C++": 6, "JavaScript": 8}),
        Participant(3, "Charlie", {"Python": 5, "React": 6, "HTML/CSS": 4}),
        Participant(4, "David", {"JavaScript": 3, "Node.js": 2}),
        Participant(5, "Eve", {"Java": 5, "Python": 4}),
        Participant(6, "Frank", {"Java": 2, "C++": 3}),
        Participant(7, "Grace", {"C++": 9, "Python": 8}),
        Participant(8, "Hank", {"Python": 6, "Java": 7}),
        Participant(9, "Ivy", {"React": 3, "JavaScript": 2, "Node.js": 4}),
        Participant(10, "Jack", {"Python": 1, "JavaScript": 2}),
    ]
    
    # Dividir en tres grupos por habilidad
    high_skill, mid_skill, low_skill = divide_by_skill(participants)
    
    
    # Optimizar compatibilidad dentro de cada grupo
    group1 = optimize_group(high_skill)
    group2 = optimize_group(mid_skill)
    group3 = optimize_group(low_skill)
    
    # Mostrar los resultados
    for i, group in enumerate([group1, group2, group3], 1):
        print(f"Group {i}:")
        for participant in group:
            print(f"  {participant}")
        print()

if __name__ == "__main__":
    main()
