import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

# Lade bereinigte Daten
df = pd.read_csv('/home/ubuntu/world_happiness_cleaned.csv')

# Setze Style
sns.set_theme(style="whitegrid")

# --- Diagramm 1: Multivariater Scatterplot ---
plt.figure(figsize=(12, 8))
# Skaliere GDP für die Punktgröße
size = df['GDP per capita'] * 100 
scatter = sns.scatterplot(data=df, x='Healthy life expectancy', y='Happiness score', 
                hue='Regional indicator', size=size, sizes=(20, 400), alpha=0.6)
sns.regplot(data=df, x='Healthy life expectancy', y='Happiness score', 
            scatter=False, color='black', line_kws={'linestyle':'--'})
plt.title('Zusammenhang zwischen Lebenserwartung und Glück (2015-2024)', fontsize=14)
plt.xlabel('Gesunde Lebenserwartung (Jahre)', fontsize=12)
plt.ylabel('Happiness Score', fontsize=12)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.tight_layout()
plt.savefig('/home/ubuntu/plot1_scatterplot.png')
plt.close()

# --- Diagramm 2: Duale Zeitreihe ---
df_yearly = df.groupby('Year')[['Happiness score', 'Healthy life expectancy']].mean().reset_index()
fig, ax1 = plt.subplots(figsize=(10, 6))

color = 'tab:blue'
ax1.set_xlabel('Jahr')
ax1.set_ylabel('Durchschnittlicher Happiness Score', color=color)
ax1.plot(df_yearly['Year'], df_yearly['Happiness score'], color=color, marker='o', label='Happiness')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Durchschnittliche Lebenserwartung (Jahre)', color=color)
ax2.plot(df_yearly['Year'], df_yearly['Healthy life expectancy'], color=color, marker='s', label='Lebenserwartung')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Globale Entwicklung von Glück und Gesundheit (2015-2024)')
fig.tight_layout()
plt.savefig('/home/ubuntu/plot2_timeseries.png')
plt.close()

# --- Diagramm 3: Relative Effizienz/Gap ---
# Z-Standardisierung
df['z_happiness'] = (df['Happiness score'] - df['Happiness score'].mean()) / df['Happiness score'].std()
df['z_health'] = (df['Healthy life expectancy'] - df['Healthy life expectancy'].mean()) / df['Healthy life expectancy'].std()
df['gap'] = df['z_happiness'] - df['z_health']

# Durchschnittlicher Gap pro Land über alle Jahre
country_gap = df.groupby('Country')['gap'].mean().sort_values()
top_5_pos = country_gap.tail(5)
top_5_neg = country_gap.head(5)
gap_plot_data = pd.concat([top_5_neg, top_5_pos])

plt.figure(figsize=(10, 6))
colors = ['red' if x < 0 else 'green' for x in gap_plot_data.values]
gap_plot_data.plot(kind='barh', color=colors)
plt.title('Länder mit der größten Abweichung (Happiness vs. Health Gap)', fontsize=14)
plt.xlabel('Differenz der z-standardisierten Werte (Glück - Gesundheit)', fontsize=12)
plt.tight_layout()
plt.savefig('/home/ubuntu/plot3_gap_analysis.png')
plt.close()

# --- Diagramm 4: Mediator-Analyse (Social Support) ---
# Wir teilen Social Support in Terzile (Low, Medium, High)
df['Social Support Level'] = pd.qcut(df['Social support'], 3, labels=['Niedrig', 'Mittel', 'Hoch'])

correlations = []
for level in ['Niedrig', 'Mittel', 'Hoch']:
    subset = df[df['Social Support Level'] == level]
    corr, _ = stats.pearsonr(subset['Healthy life expectancy'], subset['Happiness score'])
    correlations.append({'Social Support Level': level, 'Correlation': corr})

corr_df = pd.DataFrame(correlations)

plt.figure(figsize=(8, 6))
sns.barplot(data=corr_df, x='Social Support Level', y='Correlation', palette='viridis')
plt.title('Korrelation (Gesundheit & Glück) nach Sozialer Unterstützung', fontsize=14)
plt.ylabel('Pearson Korrelationskoeffizient', fontsize=12)
plt.ylim(0, 1)
for i, v in enumerate(corr_df['Correlation']):
    plt.text(i, v + 0.02, f"{v:.2f}", ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig('/home/ubuntu/plot4_mediator.png')
plt.close()

# --- Diagramm 5: Regionale Korrelations-Heatmap ---
# Da nur 4 Diagramme explizit beschrieben wurden, erstelle ich als 5. eine regionale Übersicht
plt.figure(figsize=(12, 8))
regional_corr = df.groupby('Regional indicator').apply(lambda x: stats.pearsonr(x['Healthy life expectancy'], x['Happiness score'])[0]).sort_values()
regional_corr.plot(kind='barh', color='skyblue')
plt.title('Korrelation zwischen Gesundheit und Glück nach Regionen', fontsize=14)
plt.xlabel('Pearson Korrelationskoeffizient', fontsize=12)
plt.tight_layout()
plt.savefig('/home/ubuntu/plot5_regional_corr.png')
plt.close()

print("Visualisierungen erfolgreich erstellt.")
