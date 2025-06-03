import pandas as pd
import json
import os
import gc

base_path = "/Users/andreybobua/PycharmProjects/commercialEstate/dataFiles/JSONs"

data_by_year = {2022: [], 2023: [], 2024: [], 2025: []}

cities = ["Башкортостан", "Красноярский край", "Москва", "Новосибирская область", "Ростовская область",
              "Самарская область", "Санкт-Петербург", "Свердловская область", "Татарстан", "Челябинская область"]

for city in cities:
  city_path = os.path.join(base_path, city)
  if os.path.isdir(city_path):
    for filename in os.listdir(city_path):
      if filename.endswith(".json"):
        try:
          city, year_str = filename.replace(".json", "").split("_")
          year = int(year_str)

          file_path = os.path.join(base_path, city, filename)
          print(file_path)
          with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
              obj = json.loads(line)
              ads = obj["data"]
              cur_df = pd.json_normalize(ads, sep="_", max_level=None)
              cur_df["city"] = city
              cur_df["year"] = year
              data_by_year[year].append(cur_df)

        except Exception as e:
          print(f"Error during processing {filename}: {e}")

for year, dfs in data_by_year.items():
    if dfs:
        df_combined = pd.concat(dfs, ignore_index=True)
        save_path = f"/Users/andreybobua/PycharmProjects/commercialEstate/dataFiles/cities_{year}.csv"
        df_combined.to_csv(save_path, index=False)
        print(f"Saved {year}: {df_combined.shape[0]} rows to {save_path}")
        del df_combined
        gc.collect()
