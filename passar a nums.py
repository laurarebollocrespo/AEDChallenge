# Definimos las conversiones de texto a números

def convertir_a_numeros(participante):
    # Mapeo de los valores textuales a números 
    mapeo_año_estudio = {
        "1st year": 1,
        "2nd year": 2,
        "3rd year": 3,
        "4th year": 4,
        "Masters": 5,
        "PhD": 6
    }

    mapeo_experiencia = {
        "Beginner": 1,
        "Intermediate": 2,
        "Advanced": 3
    }

    mapeo_rol_preferido = {  #esta ns
        "Análisis": 1,
        "Visualización": 2,
        "Desarrollo": 3,
        "Diseño": 4,
        "No sé": 5,
        "No me importa": 6
    }
    
 'hackathons_done: int'
    mapeo_hackathons_done = {
            "Beginner": 1,
            "Intermediate": 2,
            "Advanced": 3
    }



    # Convertir los valores del participante a números
    participante_numerico = {}

    participante_numerico["año_de_estudio"] = mapeo_año_estudio.get(participante["año_de_estudio"], 0)
    participante_numerico["nivel_de_experiencia"] = mapeo_experiencia.get(participante["nivel_de_experiencia"], 0)
    participante_numerico["rol_preferido"] = mapeo_rol_preferido.get(participante["rol_preferido"], 0)
    participante_numerico["lenguage_preferido"] = mapeo_lenguage_preferido.get(participante["lenguage_preferido"], 0)
    participante_numerico["disponibilidad"] = {dia: (1 if disponible else 0) for dia, disponible in participante["disponibilidad"].items()}

    # Para habilidades de programación (asumimos un valor numérico para cada lenguaje)
    participante_numerico["habilidades_de_programacion"] = {lenguaje: nivel for lenguaje, nivel in participante["habilidades_de_programacion"].items()}

    # Convertimos la disponibilidad a números (True = 1, False = 0)
    participante_numerico["disponibilidad"] = {dia: (1 if disponible else 0) for dia, disponible in participante["disponibilidad"].items()}

    return participante_numerico

# Ejemplo de un participante
participante = {
    "año_de_estudio": "2do año",
    "nivel_de_experiencia": "Intermedio",
    "rol_preferido": "Desarrollo",
    "habilidades_de_programacion": {"Python": 7, "Java": 5},
    "disponibilidad": {"Lunes": True, "Martes": False, "Miércoles": True, "Jueves": True, "Viernes": False},
    'lenguage_preferido': 'Spanish'
}

# Convertimos los atributos del participante a números
participante_numerico = convertir_a_numeros(participante)

# Mostrar el resultado
print(participante_numerico)
