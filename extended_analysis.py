import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Lade bereinigte Daten
df = pd.read_csv('/home/ubuntu/world_happiness_cleaned.csv')

# Fixe Korruptionsspalte (Kommas zu Punkten)
if df['Perceptions of corruption'].dtype == 'object':
    df['Perceptions of corruption'] = df['Perceptions of corruption'].str.replace(',', '.').astype(float)
if df['Freedom to make life choices'].dtype == 'object':
    df['Freedom to make life choices'] = df['Freedom to make life choices'].str.replace(',', '.').astype(float)

sns.set_theme(style="whitegrid")

# --- Diagramm 6: Pandemie-Resilienz (2019-2024) ---
plt.figure(figsize=(10, 6))
df_pandemic = df[df['Year'] >= 2019].groupby('Year')[['Happiness score', 'Social support']].mean().reset_index()

# Normalisierung für besseren Vergleich
df_pandemic['Happiness (norm)'] = (df_pandemic['Happiness score'] - df_pandemic['Happiness score'].min()) / (df_pandemic['Happiness score'].max() - df_pandemic['Happiness score'].min())
df_pandemic['Social Support (norm)'] = (df_pandemic['Social support'] - df_pandemic['Social support'].min()) / (df_pandemic['Social support'].max() - df_pandemic['Social support'].min())

plt.plot(df_pandemic['Year'], df_pandemic['Happiness (norm)'], marker='o', label='Happiness (normiert)', linewidth=2)
plt.plot(df_pandemic['Year'], df_pandemic['Social Support (norm)'], marker='s', label='Social Support (normiert)', linestyle='--', linewidth=2)
plt.axvspan(2020, 2022, color='gray', alpha=0.2, label='Hauptphase Pandemie')
plt.title('Pandemie-Resilienz: Glück vs. Soziale Unterstützung (2019-2024)', fontsize=14)
plt.xlabel('Jahr')
plt.ylabel('Normierte Werte (0-1)')
plt.legend()
plt.tight_layout()
plt.savefig('/home/ubuntu/plot6_pandemic_resilience.png')
plt.close()

# --- Diagramm 7: Korruption vs. Freiheit (Die "weichen" Faktoren) ---
plt.figure(figsize=(10, 6))
# Wir nehmen das Jahr 2024 für eine aktuelle Momentaufnahme
df_2024 = df[df['Year'] == 2024]
scatter = sns.scatterplot(data=df_2024, x='Freedom to make life choices', y='Perceptions of corruption', 
                hue='Happiness score', size='Happiness score', palette='coolwarm', sizes=(40, 400))
plt.title('Glücks-Killer Check: Freiheit vs. Korruptionswahrnehmung (2024)', fontsize=14)
plt.xlabel('Freiheit, Lebensentscheidungen zu treffen', fontsize=12)
plt.ylabel('Wahrnehmung von Korruption (höher = mehr Korruption)', fontsize=12)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('/home/ubuntu/plot7_corruption_freedom.png')
plt.close()

# --- Diagramm 8: Regionales Profil (Radar-Chart Ersatz: Grouped Bar) ---
# Wir vergleichen die 4 Hauptfaktoren nach Regionen (Durchschnitt 2015-2024)
factors = ['GDP per capita', 'Social support', 'Healthy life expectancy', 'Freedom to make life choices']
# Normalisierung der Faktoren für den Vergleich
df_norm = df.copy()
for f in factors:
    df_norm[f] = (df_norm[f] - df_norm[f].min()) / (df_norm[f].max() - df_norm[f].min())

regional_profile = df_norm.groupby('Regional indicator')[factors].mean().reset_index()
regional_profile_melted = regional_profile.melt(id_vars='Regional indicator', var_name='Faktor', value_name='Score')

plt.figure(figsize=(12, 8))
sns.barplot(data=regional_profile_melted, x='Score', y='Regional indicator', hue='Faktor')
plt.title('Regionale Profile: Welche Faktoren treiben das Wohlbefinden?', fontsize=14)
plt.xlabel('Normierter Score (Durchschnitt 2015-2024)', fontsize=12)
plt.ylabel('Region', fontsize=12)
plt.legend(title='Einflussfaktoren', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('/home/ubuntu/plot8_regional_profiles.png')
plt.close()

print("Erweiterte Visualisierungen erfolgreich erstellt.")
