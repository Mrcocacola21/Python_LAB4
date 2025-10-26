import pandas as pd
import matplotlib.pyplot as plt

# ------------------------
# 1. Імпорт бібліотек і налаштування
# ------------------------

plt.rcParams["font.family"] = "DejaVu Sans"  # щоб кирилиця нормально відображалась на графіках

# ------------------------
# 2. Завантаження початкових даних
# ------------------------

df = pd.read_csv("WorldPopulation2023.csv", encoding="utf-8-sig")

# ------------------------
# 3. Уніфікація назв стовпців
#    (щоб далі було зручно звертатись до стовпців по стабільних іменах)
# ------------------------

rename_map = {
    "Population2023": "Population_2023",
    "Population (2023)": "Population_2023",
    "Density(P/Km²)": "Density_per_km2",
    "Density (per km²)": "Density_per_km2",
    "Land Area(Km²)": "Land_Area_km2",
    "Migrants(net)": "Migrants_net",
    "Fert.Rate": "Fert_Rate",
    "MedianAge": "Median_Age",
    "UrbanPop%": "UrbanPop_pct",
    "WorldShare": "WorldShare_pct",
    "World Region": "Region",
    "Continent": "Region",
}
df = df.rename(columns=rename_map)

# ------------------------
# 4. Первинний огляд сирих даних
# ------------------------

print("=== Перші рядки датафрейму (сирі дані) ===")
print(df.head())

print("\n=== Інформація про датафрейм (сирі дані) ===")
print(df.info())

# ------------------------
# 5. Очищення даних (працюємо на копії df_clean)
# ------------------------

df_clean = df.copy()

# 5.1) Прибрати зайві пробіли у текстових полях, замінити 'N.A.' на NaN
for col in df_clean.select_dtypes(include="object").columns:
    df_clean[col] = (
        df_clean[col]
        .astype(str)
        .str.strip()
        .replace({"nan": pd.NA, "N.A.": pd.NA, "N.A": pd.NA})
    )

# 5.2) Колонки з відсотками типу "12.3 %" → перетворити в числа (12.3)
for pc in ["UrbanPop_pct", "WorldShare_pct", "YearlyChange"]:
    if pc in df_clean.columns:
        df_clean[pc] = (
            df_clean[pc]
            .astype(str)
            .str.replace("%", "", regex=False)
            .str.replace("N.A.", "", regex=False)
            .str.replace("N.A", "", regex=False)
            .str.strip()
        )
        df_clean[pc] = pd.to_numeric(df_clean[pc], errors="coerce")

# 5.3) Перетворити числові стовпці до числового типу
for c in [
    "Population_2023",
    "Density_per_km2",
    "Land_Area_km2",
    "Migrants_net",
    "Fert_Rate",
    "Median_Age",
    "NetChange",
    "Rank",
]:
    if c in df_clean.columns:
        df_clean[c] = pd.to_numeric(df_clean[c], errors="coerce")

# 5.4) Видалити рядки, де критично важливі значення відсутні
need_cols = [c for c in ["Country", "Population_2023", "Land_Area_km2"] if c in df_clean.columns]
df_clean = df_clean.dropna(subset=need_cols)

# ------------------------
# 6. Оновлена структура після очищення
# ------------------------

print("\n=== Інфо після очищення / типи даних ===")
print(df_clean.info())

# 6.1) Описова статистика числових колонок
numeric_cols = df_clean.select_dtypes(include=["number"])
print("\n=== Описова статистика (числові колонки) ===")
print(numeric_cols.describe().T)

# 6.2) Описова статистика текстових колонок
object_cols = df_clean.select_dtypes(include=["object"])
print("\n=== Описова статистика (текстові колонки) ===")
print(object_cols.describe().T)

# ------------------------
# 7. Додати регіон / континент (оскільки в датасеті немає Region)
#    Тут ми будуємо мапу країна -> континент і створюємо стовпець Region
# ------------------------

continent_map = {
    "Afghanistan": "Asia",
    "Albania": "Europe",
    "Algeria": "Africa",
    "American Samoa": "Oceania",
    "Andorra": "Europe",
    "Angola": "Africa",
    "Anguilla": "North America",
    "Antarctica": "Antarctica",
    "Antigua and Barbuda": "North America",
    "Argentina": "South America",
    "Armenia": "Asia",
    "Aruba": "North America",
    "Australia": "Oceania",
    "Austria": "Europe",
    "Azerbaijan": "Asia",
    "Bahamas": "North America",
    "Bahrain": "Asia",
    "Bangladesh": "Asia",
    "Barbados": "North America",
    "Belarus": "Europe",
    "Belgium": "Europe",
    "Belize": "North America",
    "Benin": "Africa",
    "Bermuda": "North America",
    "Bhutan": "Asia",
    "Bolivia": "South America",
    "Bosnia and Herzegovina": "Europe",
    "Botswana": "Africa",
    "Brazil": "South America",
    "British Virgin Islands": "North America",
    "Brunei": "Asia",
    "Bulgaria": "Europe",
    "Burkina Faso": "Africa",
    "Burundi": "Africa",
    "Cabo Verde": "Africa",
    "Cambodia": "Asia",
    "Cameroon": "Africa",
    "Canada": "North America",
    "Caribbean Netherlands": "North America",
    "Cayman Islands": "North America",
    "Central African Republic": "Africa",
    "Chad": "Africa",
    "Channel Islands": "Europe",
    "Chile": "South America",
    "China": "Asia",
    "Colombia": "South America",
    "Comoros": "Africa",
    "Congo": "Africa",  # Republic of the Congo
    "Cook Islands": "Oceania",
    "Costa Rica": "North America",
    "Côte d'Ivoire": "Africa",
    "Croatia": "Europe",
    "Cuba": "North America",
    "Curaçao": "North America",
    "Cyprus": "Asia",
    "Czech Republic (Czechia)": "Europe",
    "DR Congo": "Africa",  # Democratic Republic of the Congo
    "Denmark": "Europe",
    "Djibouti": "Africa",
    "Dominica": "North America",
    "Dominican Republic": "North America",
    "Ecuador": "South America",
    "Egypt": "Africa",
    "El Salvador": "North America",
    "Equatorial Guinea": "Africa",
    "Eritrea": "Africa",
    "Estonia": "Europe",
    "Eswatini": "Africa",
    "Ethiopia": "Africa",
    "Faeroe Islands": "Europe",
    "Falkland Islands": "South America",
    "Fiji": "Oceania",
    "Finland": "Europe",
    "France": "Europe",
    "French Guiana": "South America",
    "French Polynesia": "Oceania",
    "Gabon": "Africa",
    "Gambia": "Africa",
    "Gaza Strip": "Asia",
    "Georgia": "Asia",
    "Germany": "Europe",
    "Ghana": "Africa",
    "Gibraltar": "Europe",
    "Greece": "Europe",
    "Greenland": "North America",
    "Grenada": "North America",
    "Guadeloupe": "North America",
    "Guam": "Oceania",
    "Guatemala": "North America",
    "Guernsey": "Europe",
    "Guinea": "Africa",
    "Guinea-Bissau": "Africa",
    "Guyana": "South America",
    "Haiti": "North America",
    "Hong Kong": "Asia",
    "Honduras": "North America",
    "Hungary": "Europe",
    "Iceland": "Europe",
    "India": "Asia",
    "Indonesia": "Asia",
    "Iran": "Asia",
    "Iraq": "Asia",
    "Ireland": "Europe",
    "Isle of Man": "Europe",
    "Israel": "Asia",
    "Italy": "Europe",
    "Jamaica": "North America",
    "Japan": "Asia",
    "Jersey": "Europe",
    "Jordan": "Asia",
    "Kazakhstan": "Asia",
    "Kenya": "Africa",
    "Kiribati": "Oceania",
    "Kuwait": "Asia",
    "Kyrgyzstan": "Asia",
    "Laos": "Asia",
    "Latvia": "Europe",
    "Lebanon": "Asia",
    "Lesotho": "Africa",
    "Liberia": "Africa",
    "Libya": "Africa",
    "Liechtenstein": "Europe",
    "Lithuania": "Europe",
    "Luxembourg": "Europe",
    "Macao": "Asia",
    "Madagascar": "Africa",
    "Malawi": "Africa",
    "Malaysia": "Asia",
    "Maldives": "Asia",
    "Mali": "Africa",
    "Malta": "Europe",
    "Marshall Islands": "Oceania",
    "Martinique": "North America",
    "Mauritania": "Africa",
    "Mauritius": "Africa",
    "Mayotte": "Africa",
    "Mexico": "North America",
    "Micronesia": "Oceania",
    "Moldova": "Europe",
    "Monaco": "Europe",
    "Mongolia": "Asia",
    "Montenegro": "Europe",
    "Montserrat": "North America",
    "Morocco": "Africa",
    "Mozambique": "Africa",
    "Myanmar": "Asia",
    "Namibia": "Africa",
    "Nauru": "Oceania",
    "Nepal": "Asia",
    "Netherlands": "Europe",
    "New Caledonia": "Oceania",
    "New Zealand": "Oceania",
    "Nicaragua": "North America",
    "Niger": "Africa",
    "Nigeria": "Africa",
    "Niue": "Oceania",
    "North Korea": "Asia",
    "North Macedonia": "Europe",
    "Northern Mariana Islands": "Oceania",
    "Norway": "Europe",
    "Oman": "Asia",
    "Pakistan": "Asia",
    "Palau": "Oceania",
    "Panama": "North America",
    "Papua New Guinea": "Oceania",
    "Paraguay": "South America",
    "Peru": "South America",
    "Philippines": "Asia",
    "Poland": "Europe",
    "Portugal": "Europe",
    "Puerto Rico": "North America",
    "Qatar": "Asia",
    "Réunion": "Africa",
    "Romania": "Europe",
    "Russia": "Europe/Asia",
    "Rwanda": "Africa",
    "Saint Barthélemy": "North America",
    "Saint Helena": "Africa",
    "Saint Kitts & Nevis": "North America",
    "Saint Lucia": "North America",
    "Saint Martin": "North America",
    "Saint Pierre & Miquelon": "North America",
    "Saint Vincent and the Grenadines": "North America",
    "Samoa": "Oceania",
    "San Marino": "Europe",
    "São Tomé & Príncipe": "Africa",
    "Saudi Arabia": "Asia",
    "Senegal": "Africa",
    "Serbia": "Europe",
    "Seychelles": "Africa",
    "Sierra Leone": "Africa",
    "Singapore": "Asia",
    "Sint Maarten": "North America",
    "Slovakia": "Europe",
    "Slovenia": "Europe",
    "Solomon Islands": "Oceania",
    "Somalia": "Africa",
    "South Africa": "Africa",
    "South Korea": "Asia",
    "South Sudan": "Africa",
    "Spain": "Europe",
    "Sri Lanka": "Asia",
    "State of Palestine": "Asia",
    "Sudan": "Africa",
    "Suriname": "South America",
    "Sweden": "Europe",
    "Switzerland": "Europe",
    "Syria": "Asia",
    "Taiwan": "Asia",
    "Tajikistan": "Asia",
    "Tanzania": "Africa",
    "Thailand": "Asia",
    "Timor-Leste": "Asia",
    "Togo": "Africa",
    "Tokelau": "Oceania",
    "Tonga": "Oceania",
    "Trinidad and Tobago": "North America",
    "Tunisia": "Africa",
    "Turkey": "Europe/Asia",
    "Turkmenistan": "Asia",
    "Turks and Caicos": "North America",
    "Tuvalu": "Oceania",
    "Uganda": "Africa",
    "Ukraine": "Europe",
    "United Arab Emirates": "Asia",
    "United Kingdom": "Europe",
    "United States": "North America",
    "U.S. Virgin Islands": "North America",
    "Uruguay": "South America",
    "Uzbekistan": "Asia",
    "Vanuatu": "Oceania",
    "Vatican City": "Europe",
    "Venezuela": "South America",
    "Vietnam": "Asia",
    "Wallis & Futuna": "Oceania",
    "Western Sahara": "Africa",
    "Yemen": "Asia",
    "Zambia": "Africa",
    "Zimbabwe": "Africa",
}

df_clean["Region"] = df_clean["Country"].map(continent_map)

print("\n=== Перевірка доданої колонки Region ===")
print(df_clean[["Country", "Region", "Median_Age"]].head())

# ------------------------
# 8. СЕРЕДНЄ НАСЕЛЕННЯ ЗА РЕГІОНАМИ
# ------------------------

avg_pop_by_region = (
    df_clean.dropna(subset=["Region"])
    .groupby("Region")["Population_2023"]
    .mean()
    .sort_values(ascending=False)
)
print("\n=== Середнє населення за регіонами (Population_2023, середнє значення) ===")
print(avg_pop_by_region)

# ------------------------
# 9. ТОП-10 КРАЇН З НАЙБІЛЬШОЮ ЩІЛЬНІСТЮ НАСЕЛЕННЯ
# ------------------------

top_density = (
    df_clean.sort_values("Density_per_km2", ascending=False)
    .loc[:, ["Country", "Density_per_km2"]]
    .head(10)
)
print("\n=== ТОП-10 за щільністю населення (осіб на км²) ===")
print(top_density)

# ------------------------
# 10. ГРАФІК: ТОП-10 КРАЇН ЗА НАСЕЛЕННЯМ
# ------------------------

top10_pop = (
    df_clean.sort_values("Population_2023", ascending=False)
    .head(10)
    .copy()
)
top10_pop["Population_mln"] = top10_pop["Population_2023"] / 1e6

top10_pop.plot(
    kind="bar",
    x="Country",
    y="Population_mln",
    legend=False,
    figsize=(10, 5),
)
plt.ylabel("Населення, млн осіб")
plt.title("ТОП-10 країн за населенням (2023)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# ------------------------
# 11. САМОСТІЙНЕ ЗАВДАННЯ (1): 5 КРАЇН З НАЙМЕНШОЮ ПЛОЩЕЮ
# ------------------------

smallest_area = df_clean.nsmallest(5, "Land_Area_km2")[["Country", "Land_Area_km2"]]
print("\n=== 5 країн з найменшою площею (км²) ===")
print(smallest_area)

# ------------------------
# 12. САМОСТІЙНЕ ЗАВДАННЯ (2): 'ТРИВАЛІСТЬ ЖИТТЯ' ЗА РЕГІОНАМИ
#     У наборі немає Life Expectancy, тому використовуємо Median_Age як наближення.
# ------------------------

avg_age_by_region = (
    df_clean.dropna(subset=["Region"])
    .groupby("Region")["Median_Age"]
    .mean()
    .sort_values(ascending=False)
)
print("\n=== Середній медіанний вік населення (Median_Age) за регіонами ===")
print(avg_age_by_region)

# ------------------------
# 13. САМОСТІЙНЕ ЗАВДАННЯ (3): НОВИЙ СТОВПЕЦЬ Population_per_km2_calc
#     (співвідношення населення до площі)
# ------------------------

df_clean["Population_per_km2_calc"] = (
    df_clean["Population_2023"] / df_clean["Land_Area_km2"]
)

print("\n=== Перевірка нової колонки Population_per_km2_calc (перші 5 рядків) ===")
print(
    df_clean[
        ["Country", "Population_2023", "Land_Area_km2", "Population_per_km2_calc"]
    ].head()
)

# ------------------------
# 14. САМОСТІЙНЕ ЗАВДАННЯ (4): ГРАФІК 'ТРИВАЛІСТЬ ЖИТТЯ ПО КОНТИНЕНТАХ'
#     Малюємо середній Median_Age по Region
# ------------------------

age_plot = (
    df_clean.dropna(subset=["Region"])
    .groupby("Region")["Median_Age"]
    .mean()
    .reset_index()
    .sort_values("Median_Age", ascending=False)
)

age_plot.plot(
    kind="bar",
    x="Region",
    y="Median_Age",
    legend=False,
    figsize=(8, 4),
)
plt.ylabel("Середній вік, років")
plt.title("Середній вік населення за регіонами")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# ------------------------
# 15. САМОСТІЙНЕ ЗАВДАННЯ (5): ЗБЕРЕЖЕННЯ ОЧИЩЕНИХ ДАНИХ
# ------------------------

df_clean.to_csv("cleaned_population.csv", index=False, encoding="utf-8-sig")
print("\nОчищені дані збережено у файлі: cleaned_population.csv")
