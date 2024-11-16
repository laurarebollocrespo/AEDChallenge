# Definimos las conversiones de texto a números

def convertir_a_numeros(participante):
    # Mapeo de los valores textuales a números 
    mapeo_year_of_study = {
        "1st year": 1,
        "2nd year": 2,
        "3rd year": 3,
        "4th year": 4,
        "Masters": 5,
        "PhD": 6
    }

    mapeo_experience_level = {
        "Beginner": 1,
        "Intermediate": 2,
        "Advanced": 3
    }

    # Convertir los valores del participante a números
    participante_numerico = {}

    participante_numerico["year_of_study"] = mapeo_year_of_study.get(participante["year_of_study"], 0)
    participante_numerico["experience_level"] = mapeo_experience_level.get(participante["experience_level"], 0)
    participante_numerico["rol_preferido"] = mapeo_rol_preferido.get(participante["rol_preferido"], 0)
    participante_numerico["availability"] = {day: (1 if availability else 0) for day, availability in participante["availability"].items()}

    # Para habilidades de programación (asumimos un valor numérico para cada lenguaje)
    participante_numerico["habilidades_de_programacion"] = {lenguaje: nivel for lenguaje, nivel in participante["habilidades_de_programacion"].items()}

    # Convertimos la disponibilidad a números (True = 1, False = 0)
     participante_numerico["availability"] = {day: (1 if availability else 0) for day, availability in participante["availability"].items()}

    return participante_numerico

# Ejemplo de un participante
participante = {
    "year_of_study": "2nd year",
    "experience_level": "Intermediate",
    "rol_preferido": "Desarrollo",
    "habilidades_de_programacion": {"Python": 7, "Java": 5},
    "availability": {"Monday": True, "Thus": False, "Miércoles": True, "Jueves": True, "Viernes": False},
}

# Convertimos los atributos del participante a números
participante_numerico = convertir_a_numeros(participante)

# Mostrar el resultado
print(participante_numerico)



def map_availability(availability):
    """
    Función que recibe un diccionario de disponibilidad y retorna un número basado en la cantidad de valores True.
    
    Parámetros:
    availability (dict): Diccionario con las franjas horarias como claves y valores booleanos.
    
    Retorna:
    int: Número de True en el diccionario.
    """
    # Contar cuántos valores son True en el diccionario de disponibilidad
    true_count = sum(1 for value in availability.values() if value)
    
    return true_count

# Ejemplo de uso
availability = {
    "Saturday morning": False,
    "Saturday afternoon": False,
    "Saturday night": True,
    "Sunday morning": True,
    "Sunday afternoon": True
}

# Llamada a la función y resultado
score = map_availability(availability)
print(f"Puntuación de disponibilidad: {score}")
