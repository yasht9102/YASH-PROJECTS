

import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv(r"C:\Users\91798\Desktop\python\Alcohol_analysis\drinks.csv")


continent_mapping = {
    'Africa': [...],
    'Asia': [...],
    'Europe': [...],
    'North America': [...],
    'South America': [...],
    'Oceania': [...]
}


country_to_continent = {}
for continent, countries in continent_mapping.items():
    for country in countries:
        country_to_continent[country] = continent


name_corrections = {
    'Antigua & Barbuda': 'Antigua and Barbuda',
    "Cote d'Ivoire": 'Ivory Coast',
    'Cabo Verde': 'Cape Verde',
    'DR Congo': 'Congo (Democratic Republic of)',
    'Russian Federation': 'Russia',
    'St. Kitts & Nevis': 'Saint Kitts and Nevis',
    'St. Lucia': 'Saint Lucia',
    'St. Vincent & the Grenadines': 'Saint Vincent and the Grenadines',
    'Sao Tome & Principe': 'São Tomé and Príncipe',
    'Swaziland': 'Eswatini',
    'Macedonia': 'North Macedonia',
    'Trinidad & Tobago': 'Trinidad and Tobago',
    'USA': 'United States'
}
df['country'] = df['country'].replace(name_corrections)


df['continent'] = df['country'].map(country_to_continent)
df.loc[df['country'].isin(['Cook Islands', 'Niue']), 'continent'] = 'Oceania'


df.to_csv("cleaned_drinks.csv", index=False)


conn = sqlite3.connect(":memory:")
df.to_sql("drinks", conn, index=False, if_exists="replace")


queries = {
    "Top 5 by Alcohol": "SELECT country, total_litres_of_pure_alcohol FROM drinks ORDER BY total_litres_of_pure_alcohol DESC LIMIT 5",
    
}

for desc, q in queries.items():
    print(f"\n{desc}")
    print(pd.read_sql(q, conn))


sns.set(style="whitegrid")


fig, axs = plt.subplots(1, 3, figsize=(18, 5))
sns.barplot(x="beer_servings", y="country", data=df.nlargest(5, "beer_servings"), ax=axs[0], palette="Blues_d")
axs[0].set_title("Top Beer")
sns.barplot(x="wine_servings", y="country", data=df.nlargest(5, "wine_servings"), ax=axs[1], palette="Reds_d")
axs[1].set_title("Top Wine")
sns.barplot(x="spirit_servings", y="country", data=df.nlargest(5, "spirit_servings"), ax=axs[2], palette="Greens_d")
axs[2].set_title("Top Spirits")
plt.tight_layout()
plt.show()


sizes = [df['beer_servings'].sum(), df['wine_servings'].sum(), df['spirit_servings'].sum()]
labels = ['Beer', 'Wine', 'Spirits']
plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.title('Alcohol Type Distribution')
plt.axis('equal')
plt.show()


fig, axs = plt.subplots(1, 3, figsize=(18, 5))
sns.boxplot(x='continent', y='beer_servings', data=df, ax=axs[0])
sns.boxplot(x='continent', y='wine_servings', data=df, ax=axs[1])
sns.boxplot(x='continent', y='spirit_servings', data=df, ax=axs[2])
axs[0].set_title('Beer')
axs[1].set_title('Wine')
axs[2].set_title('Spirits')
plt.tight_layout()
plt.show()
