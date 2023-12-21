import pandas as pd

# Exemple de deux DataFrames
df1 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
df2 = pd.DataFrame({'C': [10, 11, 12],'A': [7, 8, 9]})

# Concaténer les deux DataFrames
resultat = pd.concat([df1, df2], sort=False)

# Remplacer les valeurs manquantes par des zéros
resultat = resultat.fillna(0)

# Afficher le résultat
print(resultat)