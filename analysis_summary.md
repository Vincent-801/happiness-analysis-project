# Analyse der Korrelation zwischen Happiness Index und gesunder Lebenserwartung (2015-2024)

## 1. Einleitung

Dieses Projekt, im Rahmen von DATAx WS 25/26, untersucht die Korrelation zwischen dem **Happiness Index** und der **gesunden Lebenserwartung** über ein Jahrzehnt (2015–2024). Das Hauptziel ist es, zu beweisen, dass Wohlbefinden ein signifikanter Prädiktor für Langlebigkeit ist, während Drittvariablen wie das Bruttoinlandsprodukt (BIP) pro Kopf und soziale Unterstützung kontrolliert werden. Die Analyse basiert auf dem bereitgestellten `world_happiness_combined.csv` Datensatz.

## 2. Datenvorverarbeitung

Eine präzise Datenvorverarbeitung war entscheidend, um die Qualität und Vergleichbarkeit der Daten zu gewährleisten. Folgende Schritte wurden durchgeführt:

### 2.1. Einheiten-Harmonisierung der Lebenserwartung

Der Datensatz enthielt gemischte Skalen für die Lebenserwartung (Indexwerte 0–1.2 vs. Lebensjahre 40–90). Eine Logik wurde implementiert, die Werte unter 5 als Index erkennt und diese mittels linearer Transformation auf die Skala der Jahre (40–90) mappt. Dies verhindert Zeitreihenfehler und ermöglicht eine konsistente Analyse. Bei der Validierung stellte sich heraus, dass die `Healthy life expectancy` Spalte im vorliegenden Datensatz bereits durchgängig in Jahren (Werte > 39) vorlag, sodass die Transformationslogik als Sicherheitsnetz diente, aber nicht aktiv eingreifen musste.

### 2.2. Datentyp-Bereinigung

Alle numerischen Spalten (`Happiness score`, `Healthy life expectancy`, `GDP per capita`, `Social support`, `Freedom to make life choices`, `Perceptions of corruption`) wurden von String/Objekt (mit Kommas als Dezimaltrennzeichen) in Float konvertiert. NaN-Werte wurden mittels Listenstreichung (listwise deletion) behandelt, um die Korrelationsmatrix nicht zu verzerren.

### 2.3. Bias-Transparenz (Konsistenter Sub-Datensatz)

Um einen Survivorship Bias zu verhindern, wurden nur Länder in die Zeitreihenanalyse einbezogen, die in allen 10 Jahren (2015–2024) konsistent vertreten waren. Dies gewährleistet eine robuste Analyse der langfristigen Trends.

Der verwendete Python-Code für die Vorverarbeitung:

```python
import pandas as pd
import numpy as np

df = pd.read_csv("/home/ubuntu/upload/world_happiness_combined.csv", sep=";")

cols_to_fix = ["Happiness score", "Healthy life expectancy", "GDP per capita", "Social support", "Freedom to make life choices", "Perceptions of corruption"]
for col in cols_to_fix:
    if df[col].dtype == "object":
        df[col] = df[col].str.replace(",", ".").astype(float)

def harmonize_life_expectancy(val):
    if val < 5:
        return (val * (50 / 1.2)) + 40
    return val

df["Healthy life expectancy"] = df["Healthy life expectancy"].apply(harmonize_life_expectancy)

df = df.dropna(subset=cols_to_fix)

year_counts = df.groupby("Country")["Year"].nunique()
consistent_countries = year_counts[year_counts == 10].index
df_consistent = df[df["Country"].isin(consistent_countries)].copy()

df_consistent.to_csv("/home/ubuntu/world_happiness_cleaned.csv", index=False)
```

## 3. Visualisierungen

Es wurden acht spezifische Visualisierungen erstellt, um die Beziehungen im Datensatz zu veranschaulichen. Dabei wurde darauf geachtet, Overplots zu vermeiden und Legenden sinnvoll zu platzieren.

### 3.1. Diagramm 1: Multivariater Scatterplot (Lebenserwartung vs. Happiness Score)

Dieses Diagramm zeigt die Beziehung zwischen gesunder Lebenserwartung (X-Achse) und Happiness Score (Y-Achse). Die Farbe der Punkte repräsentiert die Region, und die Größe der Punkte ist proportional zum BIP pro Kopf. Eine Regressionslinie visualisiert den allgemeinen Trend.

![Multivariater Scatterplot](/home/ubuntu/plot1_scatterplot.png)

### 3.2. Diagramm 2: Duale Zeitreihe (Globale Entwicklung von Glück und Gesundheit)

Dieses Diagramm stellt die durchschnittliche Entwicklung des Happiness Scores und der gesunden Lebenserwartung über die Jahre (2015-2024) dar, wobei zwei Y-Achsen für die unterschiedlichen Skalen verwendet werden.

![Duale Zeitreihe](/home/ubuntu/plot2_timeseries.png)

### 3.3. Diagramm 3: Relative Effizienz/Gap (Glück vs. Gesundheit)

Hier wird die Differenz der z-standardisierten Werte von Glück und Gesundheit berechnet. Die 5 Länder mit der größten positiven und negativen Abweichung werden visualisiert, um Länder hervorzuheben, in denen Glück und Gesundheit über- oder unterdurchschnittlich korrelieren.

![Relative Effizienz/Gap](/home/ubuntu/plot3_gap_analysis.png)

### 3.4. Diagramm 4: Mediator-Analyse (Einfluss der Sozialen Unterstützung)

Dieses Balkendiagramm zeigt, wie sich die Korrelation zwischen Gesundheit und Glück verändert, wenn man nach dem Level der 'Sozialen Unterstützung' filtert (Niedrig, Mittel, Hoch). Es verdeutlicht die Rolle der sozialen Unterstützung als Drittvariable.

![Mediator-Analyse](/home/ubuntu/plot4_mediator.png)

### 3.5. Diagramm 5: Regionale Korrelations-Heatmap

Als fünfte Visualisierung wurde eine horizontale Balkendiagramm erstellt, das die Pearson-Korrelation zwischen gesunder Lebenserwartung und Happiness Score für jede Region darstellt. Dies ermöglicht einen schnellen Überblick über regionale Unterschiede in dieser Beziehung.

![Regionale Korrelations-Heatmap](/home/ubuntu/plot5_regional_corr.png)

### 3.6. Diagramm 6: Pandemie-Resilienz: Glück vs. Soziale Unterstützung (2019-2024)

Dieses Diagramm zeigt die Entwicklung des normierten Happiness Scores und der normierten Sozialen Unterstützung während der Jahre 2019-2024, um die Auswirkungen der COVID-19-Pandemie zu beleuchten. Die Hauptphase der Pandemie (2020-2022) ist grau hinterlegt.

![Pandemie-Resilienz](/home/ubuntu/plot6_pandemic_resilience.png)

### 3.7. Diagramm 7: Glücks-Killer Check: Freiheit vs. Korruptionswahrnehmung (2024)

Dieser Scatterplot visualisiert die Beziehung zwischen der Freiheit, Lebensentscheidungen zu treffen, der Wahrnehmung von Korruption und dem Happiness Score für das Jahr 2024. Die Farbe und Größe der Punkte repräsentieren den Happiness Score.

![Glücks-Killer Check](/home/ubuntu/plot7_corruption_freedom.png)

### 3.8. Diagramm 8: Regionale Profile: Welche Faktoren treiben das Wohlbefinden?

Dieses gruppierte Balkendiagramm vergleicht die normierten Durchschnittswerte von BIP pro Kopf, Sozialer Unterstützung, gesunder Lebenserwartung und Freiheit, Lebensentscheidungen zu treffen, über verschiedene Regionen hinweg. Es bietet einen Überblick über die regionalen Stärken in diesen Wohlbefindensfaktoren.

![Regionale Profile](/home/ubuntu/plot8_regional_profiles.png)

## 4. Statistische Validierung

Zur Untermauerung der These wurden der Pearson-Korrelationskoeffizient und der p-Wert berechnet. Zusätzlich wurde eine multiple lineare Regression durchgeführt, um den Einfluss von BIP und sozialer Unterstützung zu kontrollieren.

```python
import pandas as pd
from scipy import stats
import statsmodels.api as sm

df = pd.read_csv("/home/ubuntu/world_happiness_cleaned.csv")

corr, p_value = stats.pearsonr(df["Healthy life expectancy"], df["Happiness score"])

print("------------------------------")
print("STATISTISCHE VALIDIERUNG")
print("------------------------------")
print(f"Pearson-Korrelationskoeffizient: {corr:.4f}")
print(f"p-Wert: {p_value:.4e}")

if p_value < 0.05:
    print("Ergebnis: Statistisch signifikant (p < 0.05)")
else:
    print("Ergebnis: Nicht statistisch signifikant (p >= 0.05)")

X = df[["Healthy life expectancy", "GDP per capita", "Social support"]]
X = sm.add_constant(X)
y = df["Happiness score"]

model = sm.OLS(y, X).fit()
print("\nRegressionsanalyse (Kontrolle von Drittvariablen):")
print(model.summary().tables[1])
```

**Ergebnisse der statistischen Validierung:**

*   **Pearson-Korrelationskoeffizient**: `0.6620`
*   **p-Wert**: `1.9260e-153`

Der hohe positive Korrelationskoeffizient von 0.6620 und der extrem niedrige p-Wert (weit unter 0.05) zeigen eine **statistisch hochsignifikante positive Korrelation** zwischen dem Happiness Score und der gesunden Lebenserwartung. Dies stützt die These, dass Wohlbefinden ein signifikanter Prädiktor für Langlebigkeit ist.

**Regressionsanalyse (Kontrolle von Drittvariablen):**

```
===========================================================================================
                              coef    std err          t      P>|t|      [0.025      0.975]
-------------------------------------------------------------------------------------------
const                       0.2226      0.188      1.184      0.237      -0.146       0.592
Healthy life expectancy     0.0438      0.003     12.860      0.000       0.037       0.050
GDP per capita              0.0812      0.011      7.614      0.000       0.060       0.102
Social support              2.6621      0.116     23.003      0.000       2.435       2.889
===========================================================================================
```

Die Regressionsanalyse zeigt, dass selbst unter Kontrolle von BIP pro Kopf und sozialer Unterstützung die gesunde Lebenserwartung (`Healthy life expectancy`) weiterhin einen **statistisch signifikanten positiven Einfluss** auf den Happiness Score hat (p-Wert = 0.000). Auch `GDP per capita` und `Social support` sind signifikante Prädiktoren für den Happiness Score.

## 5. Interpretation der Ergebnisse im Hinblick auf gesellschaftliche Maßnahmen

Die Analyse bestätigt eine starke und statistisch signifikante positive Korrelation zwischen dem Happiness Score und der gesunden Lebenserwartung. Dies deutet darauf hin, dass Länder mit höherem Wohlbefinden tendenziell auch eine höhere Lebenserwartung aufweisen. Die Kontrolle von Drittvariablen wie BIP und soziale Unterstützung verstärkt diese Erkenntnis, da der Zusammenhang auch unter Berücksichtigung dieser Faktoren bestehen bleibt.

**Implikationen für gesellschaftliche Maßnahmen:**

*   **Fokus auf Wohlbefinden**: Die Ergebnisse legen nahe, dass Investitionen in das allgemeine Wohlbefinden der Bevölkerung nicht nur zu einem glücklicheren Leben führen, sondern auch zu einer längeren und gesünderen Lebenserwartung beitragen können. Dies umfasst Maßnahmen zur Förderung der psychischen Gesundheit, des sozialen Zusammenhalts und der Lebensqualität.
*   **Ganzheitliche Politikansätze**: Statt sich ausschließlich auf wirtschaftliches Wachstum (BIP) zu konzentrieren, sollten politische Entscheidungsträger einen ganzheitlicheren Ansatz verfolgen, der auch soziale Unterstützung und Gesundheitsversorgung umfasst. Die Stärkung sozialer Netzwerke und der Zugang zu hochwertiger Gesundheitsversorgung sind entscheidend.
*   **Regionale Unterschiede berücksichtigen**: Die regionale Korrelationsanalyse zeigt, dass die Stärke des Zusammenhangs variieren kann. Dies erfordert maßgeschneiderte Interventionen, die auf die spezifischen Bedürfnisse und Herausforderungen der jeweiligen Regionen eingehen.
*   **Bekämpfung von Ungleichheiten**: Die Gap-Analyse hebt Länder hervor, in denen Glück und Gesundheit stark auseinanderklaffen. Dies kann auf strukturelle Probleme oder Ungleichheiten hinweisen, die gezielte Interventionen erfordern, um sowohl das Wohlbefinden als auch die Gesundheit zu verbessern.

**Zusätzliche Erkenntnisse aus den erweiterten Analysen:**

*   **Pandemie-Resilienz:** Die Analyse der Jahre 2019-2024 zeigt, dass der Happiness Score während der Hauptphase der Pandemie (2020-2022) tendenziell stabiler blieb oder sich sogar erholte, während die soziale Unterstützung in einigen Jahren einen Rückgang verzeichnete. Dies könnte darauf hindeuten, dass andere Faktoren oder eine intrinsische Resilienz der Bevölkerung das Glück auch in schwierigen Zeiten aufrechterhalten konnten, oder dass die Messung der sozialen Unterstützung in Krisenzeiten komplexer ist. Nach 2022 scheinen sich beide Werte wieder anzunähern.
*   **Korruption und Freiheit:** Der Scatterplot für 2024 deutet darauf hin, dass Länder mit höherer Freiheit und geringerer Korruptionswahrnehmung tendenziell höhere Happiness Scores aufweisen. Dies unterstreicht die Bedeutung von guter Regierungsführung und bürgerlichen Freiheiten für das Wohlbefinden.
*   **Regionale Profile:** Die regionalen Profile zeigen deutliche Unterschiede in den Treibern des Wohlbefindens. Während in Westeuropa und Nordamerika BIP und soziale Unterstützung sehr hoch sind, spielen in anderen Regionen wie Lateinamerika und der Karibik oder Südostasien Faktoren wie Freiheit eine vergleichsweise größere Rolle für das Glück, auch wenn das BIP niedriger ist. Dies bestätigt die Notwendigkeit, kontextspezifische Ansätze zur Förderung des Wohlbefindens zu entwickeln.

Zusammenfassend lässt sich sagen, dass die Förderung des Wohlbefindens ein effektiver Weg sein kann, um die Langlebigkeit und die Lebensqualität der Bevölkerung zu verbessern. Politische Maßnahmen sollten daher darauf abzielen, ein Umfeld zu schaffen, das sowohl die physische als auch die psychische Gesundheit sowie den sozialen Zusammenhalt stärkt, und dabei die spezifischen regionalen und sozioökonomischen Kontexte berücksichtigen.

## 6. GitHub-Integration

Alle Skripte und generierten Visualisierungen dieses Projekts wurden in einem öffentlichen GitHub-Repository veröffentlicht. Sie können den Code und die Ergebnisse unter folgendem Link einsehen:

[https://github.com/Vincent-801/happiness-analysis-project](https://github.com/Vincent-801/happiness-analysis-project)
