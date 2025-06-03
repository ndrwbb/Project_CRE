import os
import json
import pandas as pd

# Папка с JSON по СПб
base_path = "/Users/andreybobua/PycharmProjects/commercialEstate/dataFiles/JSONs"
spb_path = os.path.join(base_path, "Санкт-Петербург")

# Структура по годам
spb_data_by_year = {2022: [], 2023: [], 2024: [], 2025: []}

# Проходим по всем JSON-файлам в папке СПб
for filename in os.listdir(spb_path):
    if filename.endswith(".json"):
        try:
            city_raw, year_str = filename.replace(".json", "").split("_")
            year = int(year_str)

            file_path = os.path.join(spb_path, filename)
            print("Processing:", file_path)

            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    obj = json.loads(line)
                    ads = obj.get("data", [])
                    if not ads:
                        continue
                    cur_df = pd.json_normalize(ads, sep="_", max_level=None)
                    cur_df["city"] = "Санкт-Петербург"
                    cur_df["year"] = year
                    spb_data_by_year[year].append(cur_df)

        except Exception as e:
            print(f"❌ Ошибка в файле {filename}: {e}")

# Обновляем CSV по годам
for year, dfs in spb_data_by_year.items():
    if dfs:
        df_spb = pd.concat(dfs, ignore_index=True)
        csv_path = f"/Users/andreybobua/PycharmProjects/commercialEstate/dataFiles/cities_{year}.csv"

        # Читаем существующий CSV (с проверкой на существование)
        if os.path.exists(csv_path):
            df_existing = pd.read_csv(csv_path)
            df_updated = pd.concat([df_existing, df_spb], ignore_index=True)
        else:
            df_updated = df_spb  # если файла еще не существует

        # Удалим дубликаты по id, если он есть
        if "id" in df_updated.columns:
            df_updated.drop_duplicates(subset=["id"], inplace=True)

        # Сохраняем обновлённый файл
        df_updated.to_csv(csv_path, index=False)
        print(f"✅ {year}: Добавлено {df_spb.shape[0]} строк СПб → {csv_path}")