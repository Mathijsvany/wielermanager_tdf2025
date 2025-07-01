# %%
import json
import pandas as pd

with open(r"C:\Users\mvanysac\OneDrive - MINFIN\Bureaublad\wielermanager\Tour_2025.json", "r") as f:
    data = json.load(f)

df_players = pd.json_normalize(data["players"]) #we pakken enkel deel onder players

df_active_players = df_players[df_players["active"] == 1] #enkel deelnemende renners

df_value = pd.DataFrame(df_active_players[["name", "value"]]) #renners en hun wielermanagerwaarde

#data zoals onedayraces enzo zijn colommen geworden met "speciality...."
speciality_columns = [col for col in df_players.columns if col.startswith('speciality.')]

df_speciality_expanded = df_players[speciality_columns].copy()


df_speciality_expanded.columns = [col.replace('speciality.', '') for col in df_speciality_expanded.columns]

df_speciality = pd.concat([df_active_players[['name', "value"]], df_speciality_expanded], axis=1) #renners en hun pro cycling stats
df_speciality.reset_index(drop=True, inplace=True)
df_speciality.index = df_speciality.index + 1
df_speciality.head()

# %%
df_gt_all_normalized  = pd.json_normalize(data['players'], record_path=['GT'], meta=['id','name', 'value', 'active'], errors='ignore')

df_recent_gt_active_players = df_gt_all_normalized[(df_gt_all_normalized['active'] == 1) & (df_gt_all_normalized["seasonId"] >= 2024)].copy()

df_gt_final = df_recent_gt_active_players[['name', 'value', "seasonId",'competitionFeed', 'GC', 'points', 'youth', 'mountain', 'best']].copy()
df_gt_final['GC'] = df_gt_final['GC'].replace(0, 999).fillna(999)
df_gt_final[['points', 'youth', 'mountain', 'best']] = df_gt_final[['points', 'youth', 'mountain', 'best']].fillna(0)

#gewogen gemiddeldes pakken waarbij tour harder doortelt
df_gt_final['gewicht'] = 1 # 1 als standaard
df_gt_final.loc[df_gt_final['competitionFeed'] == 'TOUR', 'gewicht'] = 2 # Tour telt 2x zo zwaar



def weighted_mean(rank, weights):
    return (rank * weights).sum() / weights.sum()



df_gt_tour_multiple_agg = df_gt_final.groupby("name").agg(
    gc_average=('GC', lambda x: weighted_mean(x, df_gt_final.loc[x.index, 'gewicht'])),
    groen_average=('points', lambda x: weighted_mean(x, df_gt_final.loc[x.index, 'gewicht'])),
    best_result=('best', 'min'), 
    count=('seasonId', 'count')
)

for col in df_gt_tour_multiple_agg:
    df_gt_tour_multiple_agg[col] = df_gt_tour_multiple_agg[col].round(0).astype(int)
    

df_gt_tour_multiple_agg = df_gt_tour_multiple_agg.sort_values(by=["gc_average", "best_result"])

df_gt_tour_multiple_agg.head()


# %%
df_seasonStats_normalized  = pd.json_normalize(data['players'], record_path=['seasonStats'], meta=['id','name', 'value', 'active'], errors='ignore')

# enkel seizoen 2025
df_2025_active_players = df_seasonStats_normalized[(df_seasonStats_normalized['active'] == 1) & (df_seasonStats_normalized["season"] == 2025)].copy()

df_season2025 = df_2025_active_players[['name', 'value', "season",'racedays', 'wins', 'top3s', 'top10s']].copy()

df_season2025[['wins', 'top3s', 'top10s']] = df_season2025[['wins', 'top3s', 'top10s']].fillna(0)

df_season2025.sort_values(by=["wins", "top3s", "top10s"], ascending=False, inplace=True)
df_season2025.reset_index(drop=True, inplace=True)
df_season2025.index = df_season2025.index + 1

df_season2025.head()

# %%
#alles naar excel op verschillende werkbaden

excel_bestandsnaam = 'TOUR2025.xlsx'
writer = pd.ExcelWriter(excel_bestandsnaam, engine='xlsxwriter')
df_speciality.to_excel(writer, sheet_name='Procyclingstats', index=False)
df_gt_tour_multiple_agg.to_excel(writer, sheet_name='GT_average')
df_season2025.to_excel(writer, sheet_name='Season2025', index=False)

print(f"Alle DataFrames zijn succesvol geëxporteerd naar '{excel_bestandsnaam}' met verschillende werkbladen.")
writer.close()
print("Excel-bestand is opgeslagen.")


