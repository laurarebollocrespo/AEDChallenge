from transformers import pipeline

# Crear el pipeline de clasificación "zero-shot"
clasificador = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")

# Definir las etiquetas de intenciones
etiquetas = ["I want to socialize or meet new people", "I want to level up my programming skills", "I want to have fun and enjoy", "I want to win."]

# Texto de ejemplo
texto = "I'm all about vibin' with fellow datathoners! For me, this datathon is about making new friends and having an absolute blast. I'm excited to participate in as many events as I can, like workshops, mini-competitions, and even social activities. I want to explore new skills and techniques, but mostly, I want to connect with like-minded people and share laughter and memories. Let's do this!"

# Clasificar el texto según las etiquetas
resultado = clasificador(texto, candidate_labels=etiquetas)

# Mostrar el resultado
print("Clasificación completa:")
for label, score in zip(resultado['labels'], resultado['scores']):
    print(f"- {label}: {score:.2f}")
