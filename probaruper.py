def calcular_afinitat (p1,p2) -> float:
    score_p1 = calculate_compatibility_score(p1)
    score_p2 = calculate_compatibility_score(p2)

    resultado = [
    v1**2 - v2**2 if i != 1 else score_p1[1] == score_p2[1]
    for i, (v1, v2) in enumerate(zip(score_p1, score_p2))
]