import pandas as pd

# Datos de ejemplo
data = {'Color': ['Rojo', 'Azul', 'Verde', 'Rojo']}
df = pd.DataFrame(data)

# Usar get_dummies
one_hot = pd.get_dummies(df, columns=['Color'])

# Usar pandas.Categorical
df['Color_Num'] = pd.Categorical(df['Color']).codes

print(one_hot)  # Codificación one-hot
print(df)       # Codificación numérica
