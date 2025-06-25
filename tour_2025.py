import json
import pandas as pd

with open(r"C:\Users\mvanysac\OneDrive - MINFIN\Bureaublad\wielermanager\Tour_2025.json", "r") as f:
    data = json.load(f)

df_players = pd.json_normalize(data["players"]) #we pakken enkel deel onder players

df_active_players = df_players[df_players["active"] == 1] #enkel deelnemende renners

df_value = pd.DataFrame(df_active_players[["name", "value"]]) #renners en hun wielermanagerwaarde

#data zoals onedayraces enzo zijn colommen geworden met "speciality...."
speciality_columns = [col for col in df_players.columns if col.startswith('speciality.')]

# Creëer een DataFrame met alleen deze specialiteitskolommen
df_speciality_expanded = df_players[speciality_columns].copy()

# Hernoem de kolommen om de 'speciality.' prefix te verwijderen
df_speciality_expanded.columns = [col.replace('speciality.', '') for col in df_speciality_expanded.columns]

# Optioneel: Voeg de id en naam van de speler toe voor context
# We voegen de 'id' en 'name' kolommen toe aan de df_speciality_expanded DataFrame
# Omdat de rijen van df_players en df_speciality_expanded overeenkomen in volgorde,
# kunnen we ze direct samenvoegen.
df_speciality = pd.concat([df_active_players[['name', "value"]], df_speciality_expanded], axis=1)
print(df_speciality.head())