import pandas as pd
from scipy import stats

# Lade bereinigte Daten
df = pd.read_csv('/home/ubuntu/world_happiness_cleaned.csv')

# Berechne Pearson-Korrelation und p-Wert
corr, p_value = stats.pearsonr(df['Healthy life expectancy'], df['Happiness score'])

print("-" * 30)
print("STATISTISCHE VALIDIERUNG")
print("-" * 30)
print(f"Pearson-Korrelationskoeffizient: {corr:.4f}")
print(f"p-Wert: {p_value:.4e}")

if p_value < 0.05:
    print("Ergebnis: Statistisch signifikant (p < 0.05)")
else:
    print("Ergebnis: Nicht statistisch signifikant (p >= 0.05)")

# Zusätzliche Analyse: Korrelation unter Kontrolle von GDP und Social Support (Partial Correlation)
# Da wir keine spezialisierte Library für Partial Correlation haben, nutzen wir eine einfache lineare Regression
import statsmodels.api as sm

X = df[['Healthy life expectancy', 'GDP per capita', 'Social support']]
X = sm.add_constant(X)
y = df['Happiness score']

model = sm.OLS(y, X).fit()
print("\nRegressionsanalyse (Kontrolle von Drittvariablen):")
print(model.summary().tables[1])
