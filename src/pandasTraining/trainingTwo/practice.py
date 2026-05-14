import pandas as pd
from sqlalchemy import create_engine, text

# 模擬 DSE 原始感測器數據
raw_data = {
    "timestamp": [
        "2026-05-12 08:00",
        "2026-05-12 08:01",
        "2026-05-12 08:02",
        "2026-05-12 08:03",
        "2026-05-12 08:04",
        "2026-05-12 08:05",
    ],
    "Dept": ["Etch", "Etch", "Etch", "Photo", "Photo", "Photo"],
    "Temperature": [70.2, 71.5, 70.8, 85.0, 72.1, 71.3],  # 85.0 為突升異常
    "Pressure": [100, 102, 101, 95, 115, 110],  # 115 為劇烈波動
}

engine = create_engine(
    "mssql+pyodbc://sa:Password123@127.0.0.1/Micron?driver=ODBC+Driver+17+for+SQL+Server"
)
df = pd.DataFrame(raw_data)
df.to_sql("Sensor_Logs", engine, if_exists="replace", index=False)
df = pd.read_sql("SELECT * FROM Sensor_Logs", engine)

# 第一階段：高效資料轉換 (Data Engineering)
# 1. 請將原始數據中的 timestamp 轉換為正確的 datetime64 格式。
# 2. 將該欄位設定為 DataFrame 的索引 (Index)，並檢查資料的時間範圍（從幾點到幾點）。

# df.astype(): 精確控制記憶體與資料型別（例如將分類字串轉為 Category）。
df["Dept"] = df["Dept"].astype("category")
df["Temperature"] = df["Temperature"].astype("float32")
df["Pressure"] = df["Pressure"].astype("float32")
# pd.to_datetime(): 處理時間維度的核心，DSE 必須對時間極度敏感。
df["timestamp"] = pd.to_datetime(df["timestamp"])
# df.set_index(): 將時間設定為索引，便於進行時序切片。
df = df.set_index("timestamp")
start_time = df.index.min()
end_time = df.index.max()
print(f"開始時間： {start_time}，結束時間： {end_time}")

print("任務 1 結束")

# 第二階段：特徵工程與異常檢測 (Feature Engineering)
# 1. 針對 Temperature 欄位，計算 3 筆資料長度的移動平均，並存入新欄位 temp_ma。
# 2. 計算 Pressure 的瞬間變化絕對值（當前與前一筆的差），存入 press_delta。
# 3. 標註異常：建立 Is_Anomaly 欄位，若 Temperature 高於其移動平均 5 度，或 Pressure 變化大於 10，則標註為 1，否則為 0。

# .rolling(window=n).mean(): 移動平均（Smoothing），過濾掉隨機雜訊，找出趨勢。
df["temp_ma"] = df["Temperature"].rolling(window=3).mean()
df["temp_ma"] = df["temp_ma"].fillna(df["Temperature"])
# .diff(): 計算與上一筆的差異，用於偵測瞬間突發狀況。
df["press_delta"] = df["Pressure"].diff().abs()
df["press_delta"] = df["press_delta"].fillna(0)


# df.apply(axis=1)，axis會逐個處理，0是Column，1是row: 建立自定義的複雜業務邏輯判斷。
def isAnomaly(row):
    if (row["Temperature"] > row["temp_ma"] + 5) | (row["press_delta"] > 10):
        return 1
    return 0


df["Is_Anomaly"] = df.apply(isAnomaly, axis=1)
# 也可以使用 pandas 內建判斷。
isAnomalyPD = (df["Temperature"] > df["temp_ma"] + 5) | (df["press_delta"] > 10)
df["Is_Anomaly"] = isAnomalyPD.astype("int")

print("任務 2 結束")

# 第三階段：高級聚合與模型準備 (Analytics & Aggregation)
# 1. 按 Dept (部門) 分組。
# 2. 計算每個部門的 平均溫度、最大壓力 以及 異常發生次數 (Sum of Is_Anomaly)。
# 3. 按照「異常發生次數」由高到低排序，找出目前風險最高的部門。

# .agg({'col': ['func1', 'func2']}): 對不同欄位執行不同的聚合邏輯。
report = df.groupby("Dept").agg(
    {"Temperature": "mean", "Pressure": "max", "Is_Anomaly": "sum"}
)
report = report.sort_values(by="Is_Anomaly", ascending=False)
print(f"風險最高部門： {report.index[0]}")
# .pivot_table(): 將數據轉換為橫向對比格式（例如：各機台在各時段的表現）。
pivot_report = df.pivot_table(
    index=df.index,  # 使用 timestamp 作為縱軸
    columns="Dept",  # 使用 Dept 作為橫軸
    values="Is_Anomaly",  # 觀察異常狀態
    aggfunc="max",  # 若同時間有多筆，取最大值(有異常則顯示1)
)
# .to_dict(orient='records'): 將分析結果實體化，準備對接 API 或是 Web 展示。
web_output = report.reset_index().to_dict(orient="records")
print("\n--- 準備提供給前端 API 的數據結構 ---")
print(web_output)

print("任務 3 結束")
