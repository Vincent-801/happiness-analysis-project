import pandas as pd
import numpy as np

# 1. Daten laden
df = pd.read_csv('/home/ubuntu/upload/world_happiness_combined.csv', sep=';')

# 2. Datentyp-Bereinigung
# Konvertiere numerische Spalten von String (mit Kommas) in Float
cols_to_fix = ['Happiness score', 'Healthy life expectancy', 'GDP per capita', 'Social support']
for col in cols_to_fix:
    if df[col].dtype == 'object':
        df[col] = df[col].str.replace(',', '.').astype(float)

# 3. Einheiten-Harmonisierung für Lebenserwartung
# Logik: Werte < 5 als Index erkennen und via linearer Transformation auf 40-90 mappen
# Annahme: Index 0 -> 40 Jahre, Index 1.2 -> 90 Jahre (oder ähnliche Skalierung)
# Da die Anforderung "Werte < 5" sagt, prüfen wir das
def harmonize_life_expectancy(val):
    if val < 5:
        # Lineare Transformation: y = mx + c
        # Wir mappen [0, 1.2] auf [40, 90]
        # m = (90 - 40) / (1.2 - 0) = 50 / 1.2 = 41.666...
        # y = 41.666 * x + 40
        return (val * (50 / 1.2)) + 40
    return val

df['Healthy life expectancy'] = df['Healthy life expectancy'].apply(harmonize_life_expectancy)

# 4. NaN-Werte behandeln (Listwise Deletion)
df = df.dropna(subset=cols_to_fix)

# 5. Bias-Transparenz: Konsistenter Sub-Datensatz
# Identifiziere Länder, die in allen 10 Jahren (2015-2024) vertreten sind
year_counts = df.groupby('Country')['Year'].nunique()
consistent_countries = year_counts[year_counts == 10].index
df_consistent = df[df['Country'].isin(consistent_countries)].copy()

# Speichere den bereinigten Datensatz
df_consistent.to_csv('/home/ubuntu/world_happiness_cleaned.csv', index=False)

print(f"Ursprüngliche Zeilen: {len(df)}")
print(f"Konsistente Zeilen: {len(df_consistent)}")
print(f"Anzahl konsistenter Länder: {len(consistent_countries)}")
print(df_consistent.head())
